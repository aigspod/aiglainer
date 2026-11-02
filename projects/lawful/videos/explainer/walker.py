"""Procedural 53-marker walker + physically computed micro-Doppler (illustration only)."""
import math
import numpy as np

LAMBDA = 3e8 / 5.8e9          # ~5.2 cm, a 5.8 GHz radar
STRIDE = 1.35

def _rot_z(v, psi):
    c, s = math.cos(psi), math.sin(psi)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], v[2]])

def skeleton(phi, lean=0.0):
    """Joint positions in body frame (x fwd, y left, z up) for gait phase phi."""
    bob = 0.025 * math.cos(2 * phi)
    J = {}
    pel = np.array([0.0, 0.0, 0.97 + bob])
    J['pelvis'] = pel
    chest = pel + np.array([0.04 + lean, 0, 0.34])
    J['chest'] = chest
    J['neck'] = chest + np.array([0.01, 0, 0.17])
    J['head'] = J['neck'] + np.array([0.02, 0, 0.13])
    twist = 0.08 * math.sin(phi)
    for side, sg, ph in (('L', 1, phi), ('R', -1, phi + math.pi)):
        # legs
        hip = pel + np.array([0, 0.10 * sg, -0.03])
        th = 0.45 * math.sin(ph)
        kf = 0.10 + 0.70 * max(0.0, math.sin(ph + 2.07)) ** 2.2
        knee = hip + 0.45 * np.array([math.sin(th), 0, -math.cos(th)])
        sh = th - kf
        ank = knee + 0.43 * np.array([math.sin(sh), 0, -math.cos(sh)])
        fa = sh + math.pi / 2 - 0.15 * math.sin(ph)
        toe = ank + 0.19 * np.array([math.sin(fa), 0, -math.cos(fa)])
        heel = ank + 0.06 * np.array([-math.sin(fa), 0, math.cos(fa)]) + np.array([0, 0, -0.04])
        J['hip' + side], J['knee' + side], J['ank' + side], J['toe' + side], J['heel' + side] = hip, knee, ank, toe, heel
        # arms (counter-swing)
        sho = chest + np.array([-0.01 - sg * twist * 0.3, 0.19 * sg, 0.12])
        ap = -0.28 * math.sin(ph)
        elb = sho + 0.30 * np.array([math.sin(ap), 0.04 * sg, -math.cos(ap)])
        ef = ap + 0.30 + 0.30 * max(0.0, -math.sin(ph))
        wri = elb + 0.27 * np.array([math.sin(ef), 0.0, -math.cos(ef)])
        hand = wri + 0.08 * np.array([math.sin(ef), 0, -math.cos(ef)])
        J['sho' + side], J['elb' + side], J['wri' + side], J['hand' + side] = sho, elb, wri, hand
    return J

BONES = [('pelvis', 'chest'), ('chest', 'neck'), ('neck', 'head'),
         ('hipL', 'kneeL'), ('kneeL', 'ankL'), ('ankL', 'toeL'), ('heelL', 'toeL'),
         ('hipR', 'kneeR'), ('kneeR', 'ankR'), ('ankR', 'toeR'), ('heelR', 'toeR'),
         ('hipL', 'hipR'), ('shoL', 'shoR'), ('shoL', 'elbL'), ('elbL', 'wriL'), ('wriL', 'handL'),
         ('shoR', 'elbR'), ('elbR', 'wriR'), ('wriR', 'handR'), ('pelvis', 'hipL'), ('pelvis', 'hipR')]

def markers(J):
    """53 markers. Returns (53,3) array and weights (rough RCS ~ body-surface share)."""
    M, Wt = [], []
    def add(p, w):
        M.append(p); Wt.append(w)
    hd = J['head']
    for dx, dy in ((0.08, 0.06), (0.08, -0.06), (-0.08, 0.06), (-0.08, -0.06)):
        add(hd + np.array([dx, dy, 0.03]), 1.2)
    add(J['neck'] + np.array([-0.06, 0, 0]), 1.5)          # C7
    add(J['neck'] + np.array([0.07, 0, -0.04]), 1.5)       # clavicle
    add(J['chest'] + np.array([0.11, 0, 0.02]), 3.0)       # sternum
    add(J['chest'] + np.array([-0.11, 0, -0.08]), 3.0)     # T10
    add(J['chest'] + np.array([0.10, 0.09, 0.06]), 3.0)    # chest L
    add(J['chest'] + np.array([0.10, -0.09, 0.06]), 3.0)   # chest R
    add(J['chest'] + np.array([-0.10, 0.07, 0.10]), 3.0)   # back offset
    for s, sg in (('L', 1), ('R', -1)):
        off = np.array([0, 0.035 * sg, 0])
        add(J['sho' + s] + np.array([0, 0, 0.03]), 1.4)
        add((J['sho' + s] + J['elb' + s]) / 2 + off, 1.4)
        add(J['elb' + s] + off, 0.9); add(J['elb' + s] - off, 0.9)
        add((J['elb' + s] + J['wri' + s]) / 2 + off, 1.0)
        add(J['wri' + s] + off * 0.7, 0.6); add(J['wri' + s] - off * 0.7, 0.6)
        add(J['hand' + s], 0.8)
        add(J['hip' + s] + np.array([0.09, 0.03 * sg, 0.08]), 2.0)   # ASIS
        add(J['hip' + s] + np.array([-0.09, 0.0, 0.10]), 2.0)        # PSIS
        add(J['hip' + s] * 0.45 + J['knee' + s] * 0.55 + off * 2, 2.6)
        add(J['hip' + s] * 0.2 + J['knee' + s] * 0.8 + np.array([0.05, 0, 0]), 2.6)
        add(J['knee' + s] + off * 1.5, 1.2); add(J['knee' + s] - off * 1.5, 1.2)
        add(J['knee' + s] * 0.55 + J['ank' + s] * 0.45 + off * 1.5, 1.6)
        add(J['knee' + s] * 0.25 + J['ank' + s] * 0.75 + np.array([0.04, 0, 0]), 1.6)
        add(J['ank' + s] + off, 0.5); add(J['ank' + s] - off, 0.5)
        add(J['heel' + s], 0.6)
        add(J['toe' + s], 0.6)
        add(J['ank' + s] * 0.35 + J['toe' + s] * 0.65 + off * 1.5, 0.5)
    assert len(M) == 53, len(M)
    return np.array(M), np.array(Wt)

class Walk:
    """A random-walk path in the floor plane. pos(t) -> (x,y), heading, speed."""
    def __init__(self, seed=3, dur=60.0, fps=120, speed=1.25, area=3.2):
        rng = np.random.default_rng(seed)
        n = int(dur * fps) + 1
        self.fps = fps
        ang = rng.uniform(0, 2 * np.pi)
        p = np.zeros((n, 2))
        turn = 0.0
        for i in range(1, n):
            turn = 0.97 * turn + rng.normal(0, 0.06)
            # steer back toward origin when far away
            r = np.linalg.norm(p[i - 1])
            if r > area:
                want = math.atan2(-p[i - 1][1], -p[i - 1][0])
                d = (want - ang + math.pi) % (2 * math.pi) - math.pi
                turn += 0.02 * d
            ang += turn / fps * 6
            sp = speed * (0.8 + 0.25 * math.sin(i / fps * 0.7))
            p[i] = p[i - 1] + sp / fps * np.array([math.cos(ang), math.sin(ang)])
        self.p = p
        v = np.gradient(p, axis=0) * fps
        self.v = v
        self.sp = np.linalg.norm(v, axis=1)
        self.head = np.unwrap(np.arctan2(v[:, 1], v[:, 0]))
        self.phase = np.cumsum(self.sp / fps) / STRIDE * 2 * np.pi

    def _i(self, t):
        f = t * self.fps
        i = int(np.clip(math.floor(f), 0, len(self.p) - 2))
        return i, f - i

    def state(self, t):
        i, fr = self._i(t)
        L = lambda a: a[i] * (1 - fr) + a[i + 1] * fr
        return L(self.p), L(self.head), L(self.phase), L(self.sp)

    def markers_world(self, t):
        pos, psi, ph, sp = self.state(t)
        J = skeleton(ph, lean=0.03 * sp)
        M, Wt = markers(J)
        Mw = np.array([_rot_z(m, psi) for m in M]) + np.array([pos[0], pos[1], 0])
        Jw = {k: _rot_z(v, psi) + np.array([pos[0], pos[1], 0]) for k, v in J.items()}
        return Mw, Wt, Jw

def doppler_column(walk, t, radar, fbins, dt=1 / 120, sigma=3.0, noise=None):
    """Spectrum (dB, normalized 0..1) at time t from per-marker radial velocities."""
    M0, Wt, _ = walk.markers_world(t - dt)
    M1, _, _ = walk.markers_world(t + dt)
    r0 = np.linalg.norm(M0 - radar, axis=1)
    r1 = np.linalg.norm(M1 - radar, axis=1)
    vrad = (r1 - r0) / (2 * dt)
    fd = 2 * vrad / LAMBDA
    P = (Wt[:, None] * np.exp(-0.5 * ((fbins[None, :] - fd[:, None]) / sigma) ** 2)).sum(0)
    db = 10 * np.log10(P + 0.02)
    if noise is not None:
        db = db + noise
    return db, vrad, Wt

class Camera:
    def __init__(self, yaw=-0.55, pitch=0.22, dist=9.0, focal=1150, cx=960, cy=600, target=(0, 0, 0.9)):
        self.yaw, self.pitch, self.dist, self.focal, self.cx, self.cy = yaw, pitch, dist, focal, cx, cy
        self.target = np.array(target, float)

    def project(self, P):
        P = np.atleast_2d(P) - self.target
        cy, sy = math.cos(self.yaw), math.sin(self.yaw)
        x = P[:, 0] * cy + P[:, 1] * sy
        y = -P[:, 0] * sy + P[:, 1] * cy
        z = P[:, 2]
        cp, sp = math.cos(self.pitch), math.sin(self.pitch)
        depth = x * cp + z * sp + self.dist
        up = -x * sp + z * cp
        s = self.focal / np.maximum(depth, 0.1)
        return np.stack([self.cx + y * s * -1, self.cy - up * s], 1), depth
