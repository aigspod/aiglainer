"""OUR simulation of the paper's Chafee-Infante setup (§4.2, App. A.4 of arXiv:2512.21113v2), for "Room to unfold".
Writes data/ci.json. Label everything drawn from it "simulated from the paper's equations".

  cd aiglainer && nice -n 5 .pixi/envs/default/bin/python projects/dynamics/videos/unfold/simulate.py

Equation (24): u_t = u - u^3 + nu u_xx on [0, pi], u = 0 at both ends, nu = 0.16. Galerkin with three sine modes
(Eq. 25-26): u(x, t) = sum_k phi_k(t) sin(kx). We derive f(phi) ourselves by projecting onto sin(kx) with quadrature
(the paper does not print it). Sensor: the 10th of 256 grid points, x10 ~ 0.111 (§4.2). Sampling step of the
paper's short trajectories: 10 points over [0, 4], so dt = 4/9; we use tau = dt for the two-delay view of App. A.4.

What we draw (all ours, not the paper's figures):
- 'rod': one trajectory starting near the two-hump steady state, relaxing to the (negative) one-hump state, as profiles
  and the sensor trace u10(t).
- 'branches': curves that sketch the 2-D inertial manifold in (phi1, phi2): the four connecting orbits between the
  non-zero steady states, plus orbits leaving the origin. Each also mapped to (u10(t - tau), u10(t)).
  'half' = sign of phi2: the two mirror halves of the manifold.
"""
import json, os
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import fsolve

HERE = os.path.dirname(os.path.abspath(__file__))
NU = 0.16
XQ = np.linspace(0, np.pi, 801)
S = np.array([np.sin(k * XQ) for k in (1, 2, 3)])
WQ = np.full(XQ.size, XQ[1] - XQ[0]); WQ[0] = WQ[-1] = WQ[0] / 2
LAM = np.array([1 - NU * k * k for k in (1, 2, 3)])
X10 = float(np.linspace(0, np.pi, 256)[9])
S10 = np.sin(np.array([1, 2, 3]) * X10)
DT = 4 / 9

def f(t, p):
    u = p @ S
    return LAM * p - (2 / np.pi) * (S * u ** 3 * WQ).sum(1)

def run(p0, T, dt):
    te = np.arange(0, T + 1e-9, dt)
    s = solve_ivp(f, (0, te[-1]), p0, t_eval=te, rtol=1e-10, atol=1e-12, method='LSODA')
    return s.t, s.y.T

def delay_pairs(ph, lag):
    u = ph @ S10
    return np.stack([u[:-lag], u[lag:]], 1), ph[lag:]

def r(a, n=5):
    return np.round(np.asarray(a, float), n).tolist()

def main():
    fp1 = fsolve(lambda p: f(0, p), [1.1, 0, 0.15], xtol=1e-12)
    fp2 = fsolve(lambda p: f(0, p), [0, 0.69, 0], xtol=1e-12)
    sub = 8                                     # integrate at dt/8 for smooth curves; lag = 8 samples = tau
    h = DT / sub
    branches = []
    # the four connecting orbits: from the two-hump states (0, +-a, 0) to the one-hump states (+-b, 0, +-c)
    for s1 in (1, -1):
        for s2 in (1, -1):
            p0 = np.array([s1 * 5e-3, s2 * fp2[1], 0.0])
            _, ph = run(p0, 45, h)
            D, P = delay_pairs(ph, sub)
            keep = np.linalg.norm(P[:, :2] - P[-1, :2], axis=1) > 2e-3
            keep &= np.linalg.norm(P[:, :2] - np.array([0, s2 * fp2[1]]), axis=1) > 2e-3
            branches.append(dict(kind='edge', half=s2, phi=r(P[keep][:, :2]), delay=r(D[keep], 6)))
    # orbits leaving the origin (they hug the faster-growing first mode)
    for th in np.deg2rad([10, 30, 60, 85, 95, 120, 150, 170, 190, 210, 240, 265, 275, 300, 330, 350]):
        p0 = 1e-3 * np.array([np.cos(th), np.sin(th), 0.0])
        _, ph = run(p0, 30, h)
        D, P = delay_pairs(ph, sub)
        keep = (np.linalg.norm(P[:, :2], axis=1) > 0.02) & (np.linalg.norm(np.abs(P[:, :2]) - [fp1[0], 0], axis=1) > 2e-3)
        branches.append(dict(kind='inner', half=int(np.sign(np.sin(th))), phi=r(P[keep][:, :2]), delay=r(D[keep], 6)))
    # rod: start near the two-hump state, tilted negative, relax to the negative one-hump state (sensor swings sign)
    t, ph = run(np.array([-0.06, fp2[1], 0.0]), 20, 0.05)
    xg = np.linspace(0, np.pi, 129)
    prof = ph @ np.array([np.sin(k * xg) for k in (1, 2, 3)])
    out = dict(
        label='simulated from the paper’s equations (Chafee–Infante, §4.2): our 3-mode Galerkin run, not the paper’s data',
        notes=['u_t = u - u^3 + 0.16 u_xx, u(0)=u(pi)=0; three sine modes; f(phi) derived by us by quadrature',
               'sensor x10 = %.4f (10th of 256 points on [0, pi]); tau = dt = 4/9' % X10,
               'steady states: one-hump (+-%.4f, 0, +-%.4f), two-hump (0, +-%.4f, 0)' % (fp1[0], fp1[2], fp2[1]),
               'branches sketch the inertial manifold: connecting orbits + orbits leaving the origin'],
        nu=NU, x10=X10, dt=DT, tau=DT, fp_one=r(fp1), fp_two=r(fp2), s10=r(S10),
        branches=branches,
        rod=dict(x=r(xg, 4), t=r(t, 3), u=[r(p, 4) for p in prof], u10=r(ph @ S10, 5), phi=r(ph)),
    )
    os.makedirs(os.path.join(HERE, 'data'), exist_ok=True)
    with open(os.path.join(HERE, 'data', 'ci.json'), 'w') as fh:
        json.dump(out, fh, separators=(',', ':'))
    print('fp one-hump', fp1, 'two-hump', fp2, 'x10', X10)
    allD = np.concatenate([np.array(b['delay']) for b in branches])
    print('delay range', allD.min(0), allD.max(0), 'branches', len(branches))

if __name__ == '__main__':
    main()
