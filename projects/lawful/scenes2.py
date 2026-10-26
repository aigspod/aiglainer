"""Framework, instantiation, counterfactuals, score, domain of validity."""
import math
import numpy as np
import skia
from explainer.core import *
from explainer.kit import *
from explainer.timeline import Scene

FIG4 = None
def fig4():
    global FIG4
    if FIG4 is None:
        d = load_json('fig4.json')
        FIG4 = {k: smooth_curve(v) for k, v in d.items()}
    return FIG4

def interp_curve(key, a):
    cv = fig4()[key]
    return float(np.interp(a, cv[:, 0], cv[:, 1]))

def box(c, x, y, w, h, title, colr, a, k=1.0, sub=None):
    if a <= 0:
        return
    with layer(c, a * k):
        with xform(c, 0, 0, 0.92 + 0.08 * k, 0, x + w / 2, y + h / 2):
            rrect(c, x, y, w, h, 16, fill='panel', fa=0.85)
            rrect(c, x, y, w, h, 16, stroke=colr, sw=2.2, a=1)
            text(c, title, x + w / 2, y + h / 2 + (0 if sub is None else -8) + 10, 28, 650, 'ink', 1, 'center')
            if sub:
                text(c, sub, x + w / 2, y + h / 2 + 34, 20, 500, 'muted', 1, 'center')

def curve_arrow(c, p0, p1, bend, color, a, prog=1.0, w=2.5, dash=None, head=12):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    mid = (p0 + p1) / 2 + np.array([-(p1 - p0)[1], (p1 - p0)[0]]) * bend
    ts = np.linspace(0, 1, 40)[:, None]
    pts = (1 - ts) ** 2 * p0 + 2 * (1 - ts) * ts * mid + ts ** 2 * p1
    if a <= 0 or prog <= 0:
        return pts
    draw_poly(c, pts, color, a, w, prog, dash=dash)
    e = end_point(pts, prog)
    e0 = end_point(pts, max(0, prog - 0.03))
    ang = math.atan2(e[1] - e0[1], e[0] - e0[0])
    pth = skia.Path()
    pth.moveTo(*e)
    pth.lineTo(e[0] - head * math.cos(ang - 0.42), e[1] - head * math.sin(ang - 0.42))
    pth.lineTo(e[0] - head * math.cos(ang + 0.42), e[1] - head * math.sin(ang + 0.42))
    pth.close()
    c.drawPath(pth, paint(color, a))
    return pts

# ======================================================================= FRAMEWORK
class Framework(Scene):
    dur = 32.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (0.8, 'pop'), (4.5, 'pop'), (8.8, 'pop'), (13.0, 'pop'), (18.0, 'pop'), (22.0, 'chime'), (26.5, 'tick')]
    STEPS = [
        (0.8, 'Start with a {f:learned model f} that maps raw inputs to outputs.'),
        (4.5, 'Pair it with a {g:physics model g}: the known law, written over interpretable, continuous variables Ω.'),
        (8.8, "An {y:input bridge B} extracts those physical variables from f's raw input."),
        (13.0, 'A family of {x:perturbations} moves the physical state. A matching counterfactual input x′ lets f and g be compared at the same state.'),
        (18.0, 'Two {y:output bridges} project both models onto one shared physical observable Z.'),
        (22.0, 'A scalar {y:consistency score} compares them. Larger means closer agreement.'),
        (26.5, 'Because α ranges over a {y:continuous} set, consistency is measured across the space, not on a few discrete pairs.'),
    ]

    def draw(self, c, t):
        header(c, t, '03', 'The framework', 'Step 1: does its behavior follow the *law*?')
        # geometry
        X = (170, 360, 230, 110); OM = (170, 700, 230, 110)
        F = (700, 330, 380, 170); G = (700, 690, 380, 150)
        Z = (1250, 500, 250, 170); M = (1580, 520, 230, 130)
        P = (450, 556, 230, 64)
        k1 = ramp(t, 0.8, 0.9, e_expo)
        box(c, *X, 'input  x', 'ink', 1, k1, sub='raw MoCap')
        box(c, *F, 'Learned model  f', 'f', 1, k1, sub='the transformer')
        ka = ramp(t, 1.4, 0.8)
        arrow(c, X[0] + X[2] + 8, X[1] + 55, F[0] - 8, F[1] + 85, 'f', ka, 2.5, prog=ka)
        tex(c, 'fmap', F[0] + F[2] / 2, F[1] - 32, 34, k1)
        k2 = ramp(t, 4.5, 0.9, e_expo)
        box(c, *OM, 'physics state  ω', 'ink', 1, k2, sub='continuous space Ω')
        box(c, *G, 'Physics model  g', 'g', 1, k2, sub='the known law')
        kb = ramp(t, 5.1, 0.8)
        arrow(c, OM[0] + OM[2] + 8, OM[1] + 55, G[0] - 8, G[1] + 65, 'g', kb, 2.5, prog=kb)
        tex(c, 'gmap', G[0] + G[2] / 2, G[1] + G[3] + 36, 34, k2)
        # B bridge
        k3 = ramp(t, 8.8, 1.0)
        arrow(c, X[0] + 60, X[1] + X[3] + 8, OM[0] + 60, OM[1] - 8, 'y', k3, 3, prog=k3, glow=6 * k3)
        text(c, 'B', X[0] + 30, (X[1] + X[3] + OM[1]) / 2 + 10, 34, 700, 'y', k3, 'center', kind='italic')
        tex(c, 'bmap', X[0] + 150, (X[1] + X[3] + OM[1]) / 2 - 28, 26, ramp(t, 9.4, 0.6) * (1 - ramp(t, 12.6, 0.4)))
        # P perturbations
        k4 = ramp(t, 13.0, 0.9, e_expo)
        if k4 > 0:
            with layer(c, k4):
                rrect(c, *P, 32, fill='x', fa=0.14)
                rrect(c, *P, 32, stroke='x', sw=2)
                text(c, 'perturbations  P', P[0] + P[2] / 2, P[1] + 41, 24, 600, 'x', 1, 'center')
            curve_arrow(c, (P[0] + 40, P[1] + P[3] + 4), (OM[0] + OM[2] - 30, OM[1] - 6), -0.25, 'x', k4, k4)
            curve_arrow(c, (P[0] + 40, P[1] - 4), (X[0] + X[2] - 30, X[1] + X[3] + 6), 0.25, 'x', k4, k4, dash=[8, 6])
            text(c, 'pα', P[0] - 6, OM[1] - 40, 24, 600, 'x', k4, 'center', kind='italic')
            text(c, 'x′', P[0] - 6, X[1] + X[3] + 52, 26, 600, 'x', k4, 'center', kind='italic')
        kp = window(t, 13.4, 18.0, 0.6, 0.5)
        tex(c, 'pfam', 890, 610, 30, kp)
        # output bridges
        k5 = ramp(t, 18.0, 1.0)
        pf = curve_arrow(c, (F[0] + F[2] + 8, F[1] + 85), (Z[0] - 8, Z[1] + 50), -0.18, 'f', k5, k5)
        pg = curve_arrow(c, (G[0] + G[2] + 8, G[1] + 75), (Z[0] - 8, Z[1] + 120), 0.18, 'g', k5, k5)
        tex(c, 'dfmap', 1170, 400, 26, k5)
        tex(c, 'dgmap', 1170, 810, 26, k5)
        kz = ramp(t, 18.4, 0.9, e_expo)
        if kz > 0:
            with layer(c, kz):
                panel(c, *Z, 1.0, 16, stroke='y', fa=0.85)
                text(c, 'observable  Z', Z[0] + Z[2] / 2, Z[1] + 38, 24, 650, 'ink', 1, 'center')
                xs = np.linspace(Z[0] + 24, Z[0] + Z[2] - 24, 80)
                for colr, ph, amp in (('g', 0.0, 1.0), ('f', 0.25, 0.9)):
                    ys = Z[1] + 112 - amp * 34 * np.sin((xs - Z[0]) / 26 + ph + t * 1.4) * np.sin((xs - Z[0]) / 75 + 0.5)
                    draw_poly(c, np.stack([xs, ys], 1), colr, 1, 2.6)
        # consistency
        k6 = ramp(t, 22.0, 0.9, e_expo)
        arrow(c, Z[0] + Z[2] + 8, Z[1] + 85, M[0] - 8, M[1] + 55, 'y', k6, 2.5, prog=k6)
        if k6 > 0:
            with layer(c, k6):
                rrect(c, *M, 16, fill='y', fa=0.12, glow=0)
                rrect(c, *M, 16, stroke='y', sw=2.4)
                text(c, 'CONSISTENCY', M[0] + M[2] / 2, M[1] + 42, 18, 600, 'y', 1, 'center', kind='mono', tracking=0.14)
                text(c, 'M', M[0] + M[2] / 2 - 10, M[1] + 100, 52, 500, 'ink', 1, 'center', kind='italic')
                text(c, 'P', M[0] + M[2] / 2 + 22, M[1] + 110, 24, 500, 'ink', 1, 'center', kind='italic')
            tex(c, 'mscore', M[0] + M[2] / 2 - 40, M[1] + M[3] + 46, 27, k6)
        # flowing data
        kf = ramp(t, 26.0, 1.0)
        if kf > 0:
            flow_dots(c, np.array([[X[0] + X[2] + 8, X[1] + 55], [F[0] - 8, F[1] + 85]]), t, 'f', kf, 2, 0.5)
            flow_dots(c, np.array([[OM[0] + OM[2] + 8, OM[1] + 55], [G[0] - 8, G[1] + 65]]), t, 'g', kf, 2, 0.5)
            flow_dots(c, pf, t + 0.3, 'f', kf, 2, 0.5)
            flow_dots(c, pg, t + 0.3, 'g', kf, 2, 0.5)
            flow_dots(c, np.array([[X[0] + 60, X[1] + X[3] + 8], [OM[0] + 60, OM[1] - 8]]), t, 'y', kf, 2, 0.5)
        # captions
        for i, (t0, s) in enumerate(self.STEPS):
            t1 = self.STEPS[i + 1][0] - 0.35 if i + 1 < len(self.STEPS) else None
            caption(c, t, s, t0, t1, y=950, size=31, maxw=1560)

# ======================================================================= INSTANTIATION
class Instantiation(Scene):
    dur = 24.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (6.5, 'pop'), (12.0, 'pop'), (17.5, 'pop')]
    CARDS = [
        ('Input bridge · B', 'vrad', 'Each marker’s {g:radial velocity}: central difference of its range to the radar.', 'y', 44),
        ('Perturbations · P', 'doppler_s', 'p_α scales every radial velocity by α. The law is linear, so the physics-side Doppler scales by exactly α.', 'x', 44),
        ('Output bridge · learned side', 'dfeq', 'Power-weighted mean Doppler frequency, the {y:centroid}, of the predicted spectrum.', 'f', 40),
        ('Output bridge · physics side', 'dgeq', 'Per-marker Doppler averaged with weights approximating radar cross-section (body-surface-area shares).', 'g', 40),
    ]

    def draw(self, c, t):
        header(c, t, '03', 'The framework', 'Instantiated for the Doppler law')
        cw, chh = 828, 300
        for i, (lab, key, desc, colr, sz) in enumerate(self.CARDS):
            t0 = 1.0 + i * 5.5
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + (i % 2) * (cw + 24)
            y = 320 + (i // 2) * (chh + 24)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    panel(c, x, y, cw, chh)
                    line(c, x + 30, y + 1, x + 150, y + 1, colr, 1, 4, cap='butt')
                    kicker(c, lab.replace('D_f', 'Df').replace('D_g', 'Dg'), x + 30, y + 44, 1, colr, 18)
                    tex(c, key, x + cw / 2, y + 128, sz, ramp(t, t0 + 0.3, 0.6), reveal=ramp(t, t0 + 0.3, 0.9, e_io))
                    rich(c, desc.replace('p_α', 'pα'), x + 30, y + 228, 26, cw - 60, t, t0 + 0.8, 0.02, 0.4, base='ink')

# ======================================================================= COUNTERFACTUAL
def make_path(n=260, seed=5):
    rng = np.random.default_rng(seed)
    ts = np.linspace(0, 1, n)
    x = 0.0 * ts
    y = 0.0 * ts
    for k in range(1, 5):
        a, b = rng.normal(0, 1.0 / k ** 1.3, 2)
        x += a * np.sin(2 * np.pi * k * ts + rng.uniform(0, 6))
        y += b * np.sin(2 * np.pi * k * ts + rng.uniform(0, 6))
    x += 1.2 * np.cos(2 * np.pi * ts) ; y += 0.9 * np.sin(2 * np.pi * ts)
    return np.stack([x, y], 1)

def counterfactual(path, radar, alpha, mode='radial'):
    """Eq. (8): x'_t = x'_{t-1} + alpha*dx_rad + dx_tan, with r-hat at the ORIGINAL x_{t-1}."""
    out = np.zeros_like(path)
    out[0] = path[0]
    for i in range(1, len(path)):
        dx = path[i] - path[i - 1]
        rh = path[i - 1] - radar
        rh = rh / np.linalg.norm(rh)
        drad = np.dot(dx, rh) * rh
        dtan = dx - drad
        if mode == 'radial':
            out[i] = out[i - 1] + alpha * drad + dtan
        else:
            out[i] = out[i - 1] + alpha * dtan
    return out

class Counterfactual(Scene):
    dur = 28.5
    chapter = 3
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (6.0, 'sweep'), (11.0, 'sweep'), (15.0, 'sweep'), (19.5, 'sweep')]
    KEYS = [(0, 1.0), (6.0, 1.0), (8.5, 0.3), (11.0, 0.3), (13.0, -0.6), (15.0, -0.6), (17.0, 1.16), (19.5, 1.16), (22.0, 0.0), (30, 0.0)]

    def __init__(self):
        p = make_path()
        self.radar_px = np.array([260.0, 610.0])
        self.path = p * 112 + np.array([700, 600])

    def alpha(self, t):
        for (t0, a0), (t1, a1) in zip(self.KEYS, self.KEYS[1:]):
            if t0 <= t <= t1:
                return lerp(a0, a1, e_io((t - t0) / (t1 - t0)) if t1 > t0 else 1)
        return self.KEYS[-1][1]

    def draw(self, c, t):
        header(c, t, '04', 'Counterfactuals', 'Building a *what-if* input')
        al = self.alpha(t)
        k0 = ramp(t, 0.8, 0.9, e_expo)
        px, py, pw, ph = MX, 300, 1000, 620
        with layer(c, k0):
            panel(c, px, py, pw, ph)
            kicker(c, 'top-down view · one marker', px + 28, py + 42, 1, 'muted', 16)
            note(c, 'illustration', px + pw - 24, py + 42, 0.8, 15, align='right')
            radar_icon(c, *self.radar_px, 1.0, 1, t, ping=True)
            cf = counterfactual(self.path, self.radar_px, al)
            # keep within panel visually (clip)
            c.save(); c.clipRect(skia.Rect.MakeXYWH(px + 4, py + 60, pw - 8, ph - 64))
            # range rings
            for r in range(150, 1000, 110):
                circle(c, *self.radar_px, r, stroke='line', sw=1, a=0.6)
            draw_poly(c, self.path, 'ink', 0.35, 2, dash=[7, 7])
            draw_poly(c, cf, 'x', 1.0, 3.2, glow=8)
            u = (t * 0.06) % 1.0
            i = int(u * (len(cf) - 1))
            line(c, *self.radar_px, *cf[i], 'g', 0.35, 1.5, dash=[5, 6])
            circle(c, *self.path[i], 6, fill='ink', a=0.6)
            circle(c, *cf[i], 9, fill='x', glow=12)
            c.restore()
            legend_item(c, px + 30, py + ph - 30, 'ink', 'original path', 0.7, dash=True, size=20)
            legend_item(c, px + 300, py + ph - 30, 'x', 'counterfactual x′', 1, size=20)
        # step decomposition inset
        k1 = ramp(t, 2.0, 0.9, e_expo)
        ix, iy, iw, ih = 1150, 300, 650, 300
        if k1 > 0:
            with layer(c, k1):
                panel(c, ix, iy, iw, ih)
                kicker(c, 'one step, decomposed', ix + 26, iy + 40, 1, 'muted', 16)
                O = np.array([ix + 250, iy + 190])
                rdir = np.array([1.0, 0.0])  # line of sight (radar to the left)
                dx = np.array([150.0, -95.0])
                drad = np.dot(dx, rdir) * rdir
                dtan = dx - drad
                line(c, ix + 40, O[1], ix + iw - 40, O[1], 'g', 0.25, 1.5, dash=[5, 6])
                text(c, 'line of sight', ix + iw - 44, O[1] - 12, 17, 500, 'g', 0.7, 'right', kind='mono')
                arrow(c, *O, *(O + dx), 'ink', 0.45, 2.5, 11, dash=[6, 5])
                arrow(c, *O, *(O + drad), 'g', 0.5, 4, 13)
                new = O + al * drad
                if abs(al) > 0.02:
                    arrow(c, *O, *new, 'x', 1, 5, 14)
                arrow(c, *new, *(new + dtan), 'v', 1, 3.5, 12)
                arrow(c, *O, *(new + dtan), 'x', 0.9, 2.5, 12, dash=[7, 5])
                text(c, 'α × radial', new[0] + (10 if al >= 0 else -10), O[1] + 34, 20, 600, 'x', 1, 'left' if al >= 0 else 'right')
                text(c, 'tangential', new[0] + dtan[0] + 12, new[1] + dtan[1] / 2, 20, 600, 'v', 1)
        # equation + alpha readout
        k2 = ramp(t, 3.0, 0.9)
        tex(c, 'palpha', 1475, 668, 38, k2, reveal=ramp(t, 3.0, 1.2, e_io))
        k3 = ramp(t, 4.0, 0.8)
        if k3 > 0:
            text(c, 'α =', 1180, 800, 56, 600, 'y', k3, kind='italic')
            number(c, al, 1290, 800, 72, 'y', k3, '{:+.2f}')
            text(c, 'radial motion scaled · tangential kept', 1180, 846, 22, 500, 'muted', k3)
            note(c, 'B(x′) ≈ α·B(x)', 1180, 884, k3, 20, 'g')
        caption(c, t, 'Scale only the {g:radial} part of each step and keep the {v:tangential} part, so the radial velocity scales by α.', 4.8, 10.6, y=985, size=29)
        caption(c, t, 'α < 0 also flips the direction of radial motion. Approaching becomes receding.', 11.2, 16.6, y=985, size=29)
        caption(c, t, 'α ≈ 1.16 pushes the fastest frames right up to the radar’s resolvable limit.', 17.0, 21.6, y=985, size=29)
        caption(c, t, 'α = 0: the range never changes. The marker slides along range rings and should produce {y:no Doppler at all}.', 22.0, None, y=985, size=29)

# ======================================================================= SCORE
class Score(Scene):
    dur = 22.5
    chapter = 3
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (3.0, 'sweep'), (9.0, 'pop'), (15.0, 'pop')]
    KEYS = [(0, 1.0), (3.0, 1.0), (5.0, 0.3), (7.0, 0.3), (9.0, -1.0), (11.0, -1.0), (13.5, 1.5), (16, 1.5), (18.5, 1.0), (25, 1.0)]

    def __init__(self):
        rng = np.random.default_rng(4)
        self.zb = rng.normal(0, 0.42, 70).clip(-0.95, 0.95)
        self.eps = rng.normal(0, 0.05, 70)

    def alpha(self, t):
        for (t0, a0), (t1, a1) in zip(self.KEYS, self.KEYS[1:]):
            if t0 <= t <= t1:
                return lerp(a0, a1, e_io((t - t0) / (t1 - t0)))
        return 1.0

    def draw(self, c, t):
        header(c, t, '04', 'Counterfactuals', 'Same *slope*, same physics')
        al = self.alpha(t)
        mf = interp_curve('a_f', al)
        mg = interp_curve('a_g', al)
        k0 = ramp(t, 0.8, 0.9, e_expo)
        ax = Axes(260, 330, 560, 560, (-1, 1), (-1.6, 1.6))
        with layer(c, k0):
            ax.draw(c, 1, [-1, 0, 1], [-1.5, 0, 1.5], fmt='{:g}')
            text(c, 'baseline centroid  z̄', ax.x + ax.w / 2, ax.y + ax.h + 74, 22, 500, 'muted', 1, 'center', kind='italic')
            c.save(); c.translate(ax.x - 70, ax.y + ax.h / 2); c.rotate(-90)
            text(c, 'perturbed centroid  z(α)', 0, 0, 22, 500, 'muted', 1, 'center', kind='italic')
            c.restore()
            c.save(); c.clipRect(skia.Rect.MakeXYWH(ax.x, ax.y, ax.w, ax.h))
            line(c, *ax.px(-1, -mg), *ax.px(1, mg), 'g', 0.9, 2.5, dash=[9, 7])
            line(c, *ax.px(-1, -mf), *ax.px(1, mf), 'f', 1, 3.5, glow=6)
            for zb, e in zip(self.zb, self.eps):
                X, Y = ax.px(zb, mf * zb + e * (0.4 + abs(mf)))
                circle(c, X, Y, 5.5, fill='f', a=0.75)
            c.restore()
            note(c, 'windows illustrative · slopes from Fig. 4a', ax.x, ax.y - 18, 0.8, 15)
        k1 = ramp(t, 1.6, 0.8)
        if k1 > 0:
            bx = 1000
            text(c, 'α', bx, 400, 40, 600, 'y', k1, kind='italic')
            number(c, al, bx + 46, 400, 46, 'y', k1, '{:+.2f}')
            legend_item(c, bx + 250, 392, 'f', '', k1)
            text(c, 'm̂f', bx + 300, 400, 30, 600, 'f', k1, kind='italic')
            number(c, mf, bx + 360, 400, 40, 'f', k1, '{:+.2f}')
            legend_item(c, bx + 520, 392, 'g', '', k1, dash=True)
            text(c, 'm̂g', bx + 570, 400, 30, 600, 'g', k1, kind='italic')
            number(c, mg, bx + 630, 400, 40, 'g', k1, '{:+.2f}')
        k2 = ramp(t, 3.4, 0.8)
        tex(c, 'slope', 1340, 540, 40, k2, reveal=ramp(t, 3.4, 1.0, e_io))
        rich(c, 'Each model’s response at α: the least-squares slope of perturbed vs. baseline centroid.', 1000, 660, 26, 780, t, 4.0, 0.02, 0.4, k2, base='muted')
        k3 = ramp(t, 9.0, 0.9)
        tex(c, 'score', 1380, 800, 33, k3, reveal=ramp(t, 9.0, 1.2, e_io))
        rich(c, '{w:1 = f matches g at every α.} Unbounded below, so patched scores can go negative.', 1000, 905, 26, 800, t, 10.0, 0.02, 0.4, k3, base='muted')
        caption(c, t, 'The physics-side slope comes from the {g:same counterfactual states}. The question is whether f bends the way g does.', 15.0, None, y=990, size=28, maxw=1700)

# ======================================================================= DOMAIN
class Domain(Scene):
    dur = 21.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (4.0, 'tick'), (7.0, 'chime'), (13.0, 'count'), (15.2, 'impact_soft')]

    def draw(self, c, t):
        header(c, t, '04', 'Counterfactuals', 'Where should the law *hold*?')
        k0 = ramp(t, 0.8, 0.9, e_expo)
        x0, x1, y = 260, 1660, 470
        A = lambda a: x0 + (a + 2) / 4 * (x1 - x0)
        kb = ramp(t, 4.0, 1.2, e_io)
        if kb > 0:
            rrect(c, A(-1.16 * kb), y - 60, A(1.16 * kb) - A(-1.16 * kb), 120, 10, fill='f', fa=0.12 * k0)
            for s in (-1, 1):
                line(c, A(1.16 * kb * s), y - 70, A(1.16 * kb * s), y + 70, 'f', 0.9 * k0, 2, dash=[7, 6])
            text(c, 'radar-resolvable', W / 2 - 230, y - 78, 18, 400, 'f', kb * k0, 'center', kind='mono', tracking=0.16)
            text(c, '|α| ≤ 1.16', W / 2 + 230, y - 78, 24, 600, 'f', kb * k0, 'center', kind='italic')
        line(c, x0, y, x0 + (x1 - x0) * k0, y, 'muted', k0, 2.5)
        for a in np.arange(-2, 2.01, 0.5):
            kk = ramp(t, 1.0 + (a + 2) * 0.08, 0.4)
            line(c, A(a), y - (12 if a == int(a) else 7), A(a), y + (12 if a == int(a) else 7), 'muted', kk, 2)
            if a == int(a):
                text(c, f'{a:+.0f}'.replace('+0', '0').replace('-', '−'), A(a), y + 50, 24, 500, 'muted', kk, 'center', kind='mono')
        text(c, 'α', x1 + 30, y + 10, 34, 600, 'y', k0, kind='italic')
        # explanation
        k1 = ramp(t, 7.0, 0.9)
        if k1 > 0:
            with layer(c, k1):
                stat(c, MX + 120, 690, '2.6 m/s', 'max radial speed the Bumblebee radar resolves', 'ink', 1, 58)
                stat(c, MX + 680, 690, '2.24 m/s', 'max body-level radial speed in training data', 'ink', 1, 58)
                tex(c, 'amax', 1520, 670, 40, 1)
        # M0
        k2 = ramp(t, 13.0, 0.6)
        if k2 > 0:
            v = 0.988 * ramp(t, 13.0, 2.0, e_out)
            with layer(c, k2):
                rrect(c, MX, 800, 1680, 150, 18, fill='y', fa=0.08)
                rrect(c, MX, 800, 1680, 150, 18, stroke='y', sw=1.5, a=0.6)
                tex(c, 'm0', MX + 90, 875, 50, 1)
                text(c, '=', MX + 170, 897, 60, 300, 'y', 1)
                number(c, v, MX + 230, 905, 92, 'y', 1, '{:.3f}')
                rich(c, 'Unpatched consistency over the resolvable domain: {y:near-perfect agreement} with the Doppler law. This is the target a circuit must recover.',
                     MX + 560, 860, 28, 1080, t, 14.0, 0.02, 0.4, 1)
