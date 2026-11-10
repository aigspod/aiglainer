"""Our simulations of the paper's stated systems -> data/*.json. Everything written here is OUR simulation from the
equations and parameters in arXiv:2512.21113v2, not the paper's trained-model output; label it on screen
("simulated from the paper's equations"). Choices the paper doesn't state are marked "our choice" below and in each
file's "notes".

    pixi run python projects/dynamics/videos/sign/simulate.py      (no make target; rerun after changing anything here)

Writes
  data/sdof.json   §3.1: SDOF free vibration, k = 2000 and k = 500 (Eq. 20-21); exact AR(2) coefficients; |H(f)|;
                   the best one-head (convex, positive-weight) fit for each case; a two-head construction for Case 2.
  data/twodof.json §3.2: 2-DOF free response (Eq. 22, stated parameters), spectrum, modal frequencies; our AR(p) fits of
                   x1 alone (p = 2, 3, 4) as the linear analogue of "how many delays are enough".
  data/vdp.json    §4.1: Van der Pol (Eq. 23, mu = 0.5, dt = 0.1): the limit cycle, a few transients, the
                   "same x, two phases" points with their 5-sample delay windows, delay-coordinate loops.
"""
import os, json
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
SRC = 'arXiv:2512.21113v2'
LABEL = 'simulated from the paper’s equations (our simulation)'

def r(v, nd=5):
    """Round arrays/floats for compact JSON."""
    a = np.asarray(v, float)
    return np.round(a, nd).tolist() if a.ndim else round(float(a), nd)

def save(name, obj):
    os.makedirs(DATA, exist_ok=True)
    with open(os.path.join(DATA, name), 'w') as f:
        json.dump(obj, f, separators=(',', ':'))
    print(f'wrote data/{name}  ({os.path.getsize(os.path.join(DATA, name)) / 1024:.0f} kB)')

def ar_response(coefs, f, dt):
    """|H(f)| of x_{t+1} = sum_l coefs[l-1] x_{t+1-l}: H(z) = 1 / (1 - sum_l a_l z^-l), z = exp(i 2 pi f dt)."""
    z = np.exp(1j * 2 * np.pi * np.asarray(f) * dt)
    den = 1 - sum(a * z ** -(l + 1) for l, a in enumerate(coefs))
    return np.abs(1 / den)

def ar_lstsq(x, p):
    """Least-squares AR(p) fit x_{t+1} = sum a_l x_{t+1-l}; returns coefs, relative one-step rms error."""
    X = np.stack([x[p - l - 1:len(x) - l - 1] for l in range(p)], 1)
    y = x[p:]
    a, *_ = np.linalg.lstsq(X, y, rcond=None)
    return a, float(np.sqrt(np.mean((X @ a - y) ** 2)) / np.sqrt(np.mean(y ** 2)))

def peaks(f, mag, rel=0.05):
    """Local maxima of mag above rel * max (including a peak at the f = 0 edge)."""
    out = []
    for i in range(len(mag)):
        lo = mag[i - 1] if i > 0 else -np.inf
        hi = mag[i + 1] if i < len(mag) - 1 else -np.inf
        if mag[i] >= lo and mag[i] > hi and mag[i] >= rel * mag.max():
            out.append(round(float(f[i]), 3))
    return out

# ------------------------------------------------------------------ §3.1 SDOF
def sdof():
    m, cd, x0, fs = 1.0, 0.5, 10.0, 25.0          # kg, Ns/m, mm, Hz (all stated in §3.1)
    dt = 1 / fs
    T = 10.0                                      # our choice: the paper gives no record length
    f = np.linspace(0, fs / 2, 501)
    out = dict(source=SRC + ' §3.1, Eq. 20-21, A.1', label=LABEL, units=dict(x='mm', t='s', f='Hz'),
               m=m, c=cd, x0=x0, fs=fs, dt=dt, T=T, f=r(f, 4),
               notes=['exact free response x(t) = x0 e^{-st}(cos wd t + s/wd sin wd t), s = c/2m; no ODE solver needed',
                      'record length 10 s is our choice; the paper does not state one',
                      'AR(2) target x_{t+1} = a1 x_t + a2 x_{t-1}; exact for sampled free vibration: '
                      'a1 = 2 e^{-s dt} cos(wd dt), a2 = -e^{-2 s dt}',
                      'one-head fit: x_{t+1} = wo (alpha x_t + (1 - alpha) x_{t-1}), 0 <= alpha <= 1, fixed alpha, '
                      'no PE/bias (signal is zero-mean); least squares over the record. The paper’s head is '
                      'data-adaptive, but its weights are still positive and sum to one at every step, so its '
                      'effective coefficients always share a sign (Eq. 29)',
                      'two-head construction is ours (head A all on x_t, head B all on x_{t-1}); the paper’s trained '
                      'W_O = [1.087, -1.244] (A.1) is a different solution with PE and bias'],
               cases={})
    t = np.arange(0, T + 1e-9, dt)
    tf = np.arange(0, T + 1e-9, 1 / 250.0)                        # fine curve for drawing
    for case, k in (('k2000', 2000.0), ('k500', 500.0)):
        wn = np.sqrt(k / m)
        s = cd / (2 * m)
        wd = np.sqrt(wn ** 2 - s ** 2)
        resp = lambda tt: x0 * np.exp(-s * tt) * (np.cos(wd * tt) + s / wd * np.sin(wd * tt))
        x, xf = resp(t), resp(tf)
        a1, a2 = 2 * np.exp(-s * dt) * np.cos(wd * dt), -np.exp(-2 * s * dt)
        (b1, b2), err_free = ar_lstsq(x, 2)
        H = ar_response([a1, a2], f, dt)
        # best convex (one-head) fit: grid over alpha, closed-form wo, then refine
        y, X1, X0 = x[2:], x[1:-1], x[:-2]

        def fit(al):
            u = al * X1 + (1 - al) * X0
            wo = (u @ y) / (u @ u)
            return wo, float(np.mean((wo * u - y) ** 2))
        grid = np.linspace(0, 1, 20001)
        errs = np.array([fit(al)[1] for al in grid])
        i0 = int(errs.argmin())
        res = minimize_scalar(lambda q: fit(q)[1], bounds=(grid[max(i0 - 1, 0)], grid[min(i0 + 1, len(grid) - 1)]),
                              method='bounded', options=dict(xatol=1e-12))
        al = float(res.x) if res.fun < errs[i0] else float(grid[i0])
        wo, mse = fit(al)
        c1, c2 = wo * al, wo * (1 - al)
        rel = np.sqrt(mse) / np.sqrt(np.mean(y ** 2))
        onestep = np.concatenate([x[:2], c1 * X1 + c2 * X0])
        roll = np.zeros_like(x)
        roll[:2] = x[:2]
        for i in range(2, len(x)):
            roll[i] = c1 * roll[i - 1] + c2 * roll[i - 2]
        Hc = ar_response([c1, c2], f, dt)
        exact_roll = np.zeros_like(x)
        exact_roll[:2] = x[:2]
        for i in range(2, len(x)):
            exact_roll[i] = a1 * exact_roll[i - 1] + a2 * exact_roll[i - 2]
        out['cases'][case] = dict(
            k=k, fn=r(wn / (2 * np.pi), 4), fd=r(wd / (2 * np.pi), 4), zeta=r(s / wn, 6),
            a1=r(a1, 5), a2=r(a2, 5), same_sign=bool(a1 * a2 > 0),
            a_lstsq=[r(b1, 5), r(b2, 5)], a_lstsq_rel_err=err_free,
            exact_rollout_max_err=r(np.abs(exact_roll - x).max(), 9),
            t=r(t, 4), x=r(x, 5), tf=r(tf, 4), xf=r(xf, 4),
            H=r(H, 4), H_peak_f=peaks(f, H), H_db=r(20 * np.log10(H / H.max()), 3),
            spectrum_note='|H(f)| of the exact AR(2) recurrence (the paper’s Fig. 2 quantity, from our coefficients)',
            convex=dict(alpha=r(al, 5), wo=r(wo, 5), beta1=r(c1, 5), beta2=r(c2, 5), rel_rms_err=r(rel, 5),
                        exact=bool(rel < 1e-6), rel_rms_err_exact=float(f'{rel:.3g}'), onestep=r(onestep, 5), rollout=r(roll, 5),
                        H=r(Hc, 4), H_peak_f=peaks(f, Hc), H_db=r(20 * np.log10(Hc / H.max()), 3),
                        note='best single-head (positive weights summing to one, times one output weight) fit; '
                             'rollout iterates the fit from the first two true samples; one-step uses true history'))
        if case == 'k500':
            out['cases'][case]['two_head'] = dict(
                heads=[dict(alpha=[1.0, 0.0], wo=r(a1, 5)), dict(alpha=[0.0, 1.0], wo=r(a2, 5))],
                beta=[r(a1, 5), r(a2, 5)], paper_WO=[1.087, -1.244],
                note='our construction: two heads with opposite-sign output weights give the mixed-sign AR(2) exactly')
    return out

# ------------------------------------------------------------------ §3.2 2-DOF
def twodof():
    m1 = m2 = 1.0
    c1 = c2 = 0.5
    k1, k2 = 1000.0, 1500.0
    M = np.diag([m1, m2])
    C = np.array([[c1 + c2, -c2], [-c2, c2]])
    K = np.array([[k1 + k2, -k2], [-k2, k2]])
    fs = 25.0                                     # our assumption: §3.2 doesn't restate the rate; §3.1 uses 25 Hz
    dt, T = 1 / fs, 6.0                           # 6 s record: our choice (mode 2 decays ~7x faster than mode 1)
    w2, phi = np.linalg.eigh(K)                   # M = I, so K phi = w^2 phi
    fu = np.sqrt(w2) / (2 * np.pi)
    A = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.linalg.solve(M, K), -np.linalg.solve(M, C)]])
    lam = np.linalg.eigvals(A)
    fdamp = sorted(set(float(v) for v in np.round(np.abs(lam.imag) / (2 * np.pi), 4)))
    zeta = sorted(set(float(v) for v in np.round(-lam.real / np.abs(lam), 6)))
    sol = solve_ivp(lambda tt, s: A @ s, (0, T), [10.0, 0.0, 0.0, 0.0], method='RK45', rtol=1e-10, atol=1e-12,
                    dense_output=True)
    t = np.arange(0, T + 1e-9, dt)
    tf = np.arange(0, 6.0 + 1e-9, 1 / 250.0)      # fine curve, first 6 s, for drawing
    S, Sf = sol.sol(t), sol.sol(tf)
    x1, x2 = S[0], S[1]
    # amplitude spectrum of the sampled displacements (Hann window, zero-padded)
    nfft = 8192
    win = np.hanning(len(t))
    F = np.fft.rfftfreq(nfft, dt)
    spec = {}
    for nm, sig in (('x1', x1), ('x2', x2)):
        A_ = np.abs(np.fft.rfft(sig * win, nfft))
        spec[nm] = A_
    top = max(v.max() for v in spec.values())
    keep = F <= fs / 2
    f = np.linspace(0, fs / 2, 501)
    ar = {}
    for p in (2, 3, 4):
        a, err = ar_lstsq(x1, p)
        Hp = ar_response(a, f, dt)
        roots = np.roots(np.concatenate([[1.0], -a]))
        fr = sorted(set(float(v) for v in np.round(np.abs(np.angle(roots)) / (2 * np.pi * dt), 3)))
        ar[f'p{p}'] = dict(coefs=r(a, 6), rel_rms_err=float(f'{err:.3g}'), H=r(Hp, 4), H_db=r(20 * np.log10(Hp / Hp.max()), 3),
                           H_peak_f=peaks(f, Hp), pole_f=fr)
    out = dict(source=SRC + ' §3.2, Eq. 22', label=LABEL, units=dict(x='mm', t='s', f='Hz'),
               m=[m1, m2], c=[c1, c2], k=[k1, k2], x0=[10.0, 0.0], v0=[0.0, 0.0], fs=fs, dt=dt, T=T,
               f_undamped=r(fu, 4), f_damped=fdamp, zeta=zeta, modes=r(phi.T, 5),
               paper_reported_f=[4.1, 9.5],
               t=r(t, 4), x1=r(x1, 5), x2=r(x2, 5), tf=r(tf, 4), x1f=r(Sf[0], 4), x2f=r(Sf[1], 4),
               spec_f=r(F[keep], 4), spec_x1=r(spec['x1'][keep] / top, 5), spec_x2=r(spec['x2'][keep] / top, 5),
               spec_peak_f=dict(x1=peaks(F[keep], spec['x1'][keep], 0.1), x2=peaks(F[keep], spec['x2'][keep], 0.1)),
               ar_f=r(f, 4), ar_x1=ar,
               notes=['RK45, rtol 1e-10, atol 1e-12, x(0) = [10, 0], v(0) = 0, as stated in §3.2',
                      'parameters as stated give undamped modes 3.26 and 9.52 Hz; the paper reports 4.1 and 9.5 Hz '
                      '(see the accuracy note in projects/dynamics/AGENTS.md)',
                      'sampling at 25 Hz and the 6 s record are our assumptions; relative peak heights depend on record length '
                      '(mode 2 is more damped, so a longer record shrinks its peak)',
                      'ar_x1: OUR least-squares AR(p) fits of x1 alone (unconstrained signs), the linear analogue of '
                      'the delay count; x1 of a 2-DOF system is exactly AR(4), so p = 4 fits to rounding error. '
                      'Not the paper’s transformer.'])
    return out

# ------------------------------------------------------------------ §4.1 Van der Pol
def vdp():
    mu, dt = 0.5, 0.1
    fvec = lambda tt, s: [s[1], mu * (1 - s[0] ** 2) * s[1] - s[0]]
    tol = dict(rtol=1e-6, atol=1e-9)              # §4.1: BDF, rtol 1e-6, atol 1e-9
    # long test trajectory from [2, 0] over 65 time units (§4.1)
    tl = np.arange(0, 65 + 1e-9, dt)
    L = solve_ivp(fvec, (0, 65), [2.0, 0.0], method='BDF', t_eval=tl, **tol)
    # one clean period, tighter tolerance, starting on the cycle at an upward zero crossing of x
    S = solve_ivp(fvec, (0, 200), [2.0, 0.0], method='BDF', rtol=1e-10, atol=1e-12, dense_output=True)
    tt = np.linspace(150, 200, 200001)
    xs = S.sol(tt)[0]
    up = tt[1:][(xs[:-1] < 0) & (xs[1:] >= 0)]
    period = float(np.mean(np.diff(up)))
    t0 = up[0]
    P = solve_ivp(fvec, (0, period), S.sol(t0), method='DOP853', rtol=1e-12, atol=1e-12, dense_output=True)
    cyc_t = np.linspace(0, period, 401)
    cyc = P.sol(cyc_t)
    cyc_s = P.sol(np.arange(0, period, dt))       # the cycle sampled at dt = 0.1
    xamp = float(np.max(np.abs(cyc[0])))
    # transients over [0, 6.5] from a few initial conditions in U(-3, 3)^2 (fixed seed; our picks) + one near the origin
    rng = np.random.default_rng(11)
    ics = [[0.1, 0.0]] + rng.uniform(-3, 3, (5, 2)).round(2).tolist()
    te = np.arange(0, 6.5 + 1e-9, dt)
    trans = []
    for ic in ics:
        s = solve_ivp(fvec, (0, 6.5), ic, method='BDF', t_eval=te, **tol)
        sf = solve_ivp(fvec, (0, 6.5), ic, method='BDF', dense_output=True, **tol)
        fine = sf.sol(np.linspace(0, 6.5, 261))
        trans.append(dict(ic=ic, x=r(s.y[0], 4), v=r(s.y[1], 4), xf=r(fine[0], 4), vf=r(fine[1], 4)))
    # same x, two phases: where the cycle crosses x = X going right (v > 0) and going left (v < 0)
    X = 1.0
    two = []
    for sign in (+1, -1):
        idx = [i for i in range(len(cyc_t) - 1)
               if (cyc[0][i] - X) * (cyc[0][i + 1] - X) <= 0 and np.sign(cyc[1][i]) == sign]
        i = idx[0]
        # refine by bisection on the dense solution
        lo, hi = cyc_t[i], cyc_t[i + 1]
        for _ in range(60):
            mid = (lo + hi) / 2
            if (P.sol(lo)[0] - X) * (P.sol(mid)[0] - X) <= 0:
                hi = mid
            else:
                lo = mid
        ts = (lo + hi) / 2
        lags = np.array([ts - k * dt for k in range(5)]) % period      # x_t, x_{t-1}, ..., x_{t-4}
        win = P.sol(lags)[0]
        two.append(dict(t=r(ts, 5), x=r(P.sol(ts)[0], 5), v=r(P.sol(ts)[1], 5),
                        window=r(win, 5), window_order='x_t, x_{t-1}, x_{t-2}, x_{t-3}, x_{t-4} (dt = 0.1)'))
    # delay-coordinate loops of the cycle (what a delay embedding can see from x alone)
    def delay(tau):
        tq = np.linspace(0, period, 401)
        return r(np.stack([P.sol(tq)[0], P.sol((tq - tau) % period)[0]], 1), 4)
    win5 = np.stack([P.sol((np.linspace(0, period, 401) - k * dt) % period)[0] for k in range(5)], 1)
    mu_w = win5.mean(0)
    U, sv, Vt = np.linalg.svd(win5 - mu_w, full_matrices=False)
    pc = (win5 - mu_w) @ Vt[:2].T
    out = dict(source=SRC + ' §4.1, Eq. 23', label=LABEL, mu=mu, dt=dt, period=r(period, 5), x_amplitude=r(xamp, 4),
               cycle_t=r(cyc_t, 5), cycle_x=r(cyc[0], 5), cycle_v=r(cyc[1], 5),
               cycle_sampled_x=r(cyc_s[0], 5), cycle_sampled_v=r(cyc_s[1], 5),
               long_t=r(tl, 3), long_x=r(L.y[0], 5), long_v=r(L.y[1], 5),
               transients=trans, same_x=dict(X=X, points=two),
               delay_loops=dict(tau_0p1=delay(0.1), tau_quarter=delay(period / 4), tau_quarter_value=r(period / 4, 4)),
               pca_loop=r(pc, 4), pca_var=r(sv[:3] ** 2 / (sv ** 2).sum(), 6),
               notes=['BDF, rtol 1e-6, atol 1e-9, sampled at dt = 0.1 as in §4.1; the long trajectory starts at [2, 0] '
                      'and runs 65 time units (§4.1)',
                      'the clean period is ours (DOP853, tight tolerance) for drawing; period from upward zero crossings',
                      'transient initial conditions: one near the origin plus five from U(-3, 3)^2 with seed 11 (our picks); '
                      'each over [0, 6.5] like the paper’s training trajectories',
                      'same_x: the two points on the cycle with x = 1.0 (v > 0 and v < 0) and the 5-sample windows ending '
                      'there: same latest sample, different histories',
                      'delay_loops: (x(t), x(t - tau)) around the cycle; pca_loop: the first two principal components of '
                      '5-sample windows. Our delay coordinates, NOT the paper’s learned latent h_t'])
    return out

if __name__ == '__main__':
    sd, td, vd = sdof(), twodof(), vdp()
    save('sdof.json', sd)
    save('twodof.json', td)
    save('vdp.json', vd)
    for k, cs in sd['cases'].items():
        cv = cs['convex']
        print(f"{k}: fn={cs['fn']} Hz  a1={cs['a1']}  a2={cs['a2']}  lstsq={cs['a_lstsq']}  |H| peak {cs['H_peak_f']}")
        print(f"   one head: alpha={cv['alpha']} wo={cv['wo']} beta=({cv['beta1']}, {cv['beta2']}) "
              f"rel err={cv['rel_rms_err']}  |H| peak {cv['H_peak_f']}")
    print(f"2-DOF: undamped {td['f_undamped']} Hz, damped {td['f_damped']}, spectrum peaks {td['spec_peak_f']}")
    for p, v in td['ar_x1'].items():
        print(f"   AR {p} on x1: rel err {v['rel_rms_err']:.2e}, |H| peaks {v['H_peak_f']}, pole freqs {v['pole_f']}")
    print(f"VdP: period {vd['period']}, |x| max {vd['x_amplitude']}, same-x points "
          f"{[(p['x'], p['v']) for p in vd['same_x']['points']]}, pca var {vd['pca_var']}")
