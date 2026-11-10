"""Native 9:16 scenes for dynamics/shorts/{updown, unfold, reynolds}. Each draws in aiglainer.short.BOX (720 x 700),
origin top-left. Big type: labels >= 19 px, numbers >= 28 px.

Sources (via projects/dynamics/AGENTS.md): Table 1 (Van der Pol, x only), §4.2 / App. A.4 (Chafee-Infante),
§4.3 / App. A.5 (cylinder flow) of arXiv:2512.21113v2. Van der Pol curves and windows are OUR simulation (data/vdp.json,
written by simulate.py); the Chafee-Infante fold is OUR simulation (unfold/data/ci.json). Latent pictures, Re loops and
the wake are illustrations and say so on screen. (A second module, dynshorts.py, belongs to the other shorts.)"""
import importlib.util, os, sys
from dynkit import *

_HERE = os.path.dirname(os.path.abspath(__file__))

def _unfold():
    """dynamics/videos/unfold/scenes.py, loaded by path under its own name ('scenes' is taken by several pieces)."""
    key = '_dynshorts2_unfold_scenes'
    if key not in sys.modules:
        spec = importlib.util.spec_from_file_location(key, os.path.join(_HERE, '..', 'unfold', 'scenes.py'))
        m = importlib.util.module_from_spec(spec)
        sys.modules[key] = m
        spec.loader.exec_module(m)
    return sys.modules[key]

LAGS = ['x(t−4)', 'x(t−3)', 'x(t−2)', 'x(t−1)', 'x(t)']

def log_col(c, x, floor, w, hmax, v, lo, hi, colr, k, prog, label=None, size=30, glow=0):
    """A column whose height is log10(v) on [lo, hi]; its value printed above."""
    if k <= 0:
        return floor
    hh = hmax * (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * prog
    rrect(c, x - w / 2, floor - hh, w, max(hh, 3), 8, fill=colr, a=k, fa=k * 0.88, glow=glow)
    text(c, label or sci(v), x, floor - hh - 16, size, 700, colr, k, 'center')
    return floor - hh

def log_grid(c, x0, x1, floor, hmax, lo, hi, k, fs=26):
    e0, e1 = int(round(math.log10(lo))), int(round(math.log10(hi)))
    for e in range(e0, e1 + 1):
        Y = floor - hmax * (e - e0) / (e1 - e0)
        line(c, x0, Y, x1, Y, 'line', k * (1.0 if e == e0 else 0.6), 2 if e == e0 else 1)
        text(c, decade(e), x0 - 12, Y + fs * 0.36, fs, 500, 'muted', k, 'right')


# ================================================================ updown: Van der Pol, x only
class UpDownGauge(Scene):
    """A dot seen only by its height reaches x = 1: up or down? Then the two five-sample histories (our simulation)."""
    vertical = True
    dur = 20.0
    cues = [(0.3, 'pop'), (4.5, 'pop'), (11.0, 'tick'), (11.8, 'tick')]
    GX, GY0, GY1 = 150, 80, 380                # gauge: x = +2.2 at GY0, −2.2 at GY1

    def __init__(self):
        d = load_json('vdp.json')
        self.per = d['period']
        self.ct, self.cx = np.array(d['cycle_t']), np.array(d['cycle_x'])
        a, b = d['same_x']['points']               # x = 1.0 on the cycle: a rising, b falling
        self.ta = a['t']
        self.win = (a['window'][::-1], b['window'][::-1])     # oldest first

    def gy(self, v):
        return lerp(self.GY1, self.GY0, (v + 2.2) / 4.4)

    def draw(self, c, t):
        k = ramp(t, 0.1, 0.6)
        gx = self.GX
        kicker(c, 'all you see: the height x', 360, 34, k, 'muted', 19, align='center')
        line(c, gx, self.GY0, gx, self.GY1, 'muted', k, 3)
        for v in (-2, -1, 0, 1, 2):
            Y = self.gy(v)
            line(c, gx - 14, Y, gx + 14, Y, 'muted', k, 2)
            text(c, f'{v:+d}'.replace('-', '−') if v else '0', gx - 28, Y + 10, 28, 500, 'muted', k, 'right', kind='mono')
        # once round the simulated cycle, landing on x = 1 on the way up
        p = (1.0 + self.ta / self.per) * e_io(clamp((t - 0.2) / 4.2))
        xv = float(np.interp(np.mod(p * self.per, self.per), self.ct, self.cx))
        circle(c, gx, self.gy(xv), 22, fill='y', a=k, glow=14)
        kq = ramp(t, 4.5, 0.7, e_expo)
        if kq > 0:
            Y = self.gy(1.0)
            text(c, 'x = 1.00', gx + 44, Y + 14, 40, 600, 'y', kq, kind='mono')
            ax = 520
            arrow(c, ax, Y - 18, ax, Y - 92, 'f', kq, 3, 14)
            text(c, 'up?', ax + 26, Y - 46, 36, 400, 'f', kq, kind='italic')
            arrow(c, ax, Y + 18, ax, Y + 92, 'c', kq, 3, 14)
            text(c, 'down?', ax + 26, Y + 80, 36, 400, 'c', kq, kind='italic')
        for i, (win, colr, lab, t0) in enumerate(((self.win[0], 'f', 'climbing to 1: on the way up', 11.0),
                                                  (self.win[1], 'c', 'falling to 1: on the way down', 11.8))):
            kk = ramp(t, t0, 0.6, e_expo)
            if kk <= 0:
                continue
            yy = 452 + i * 120
            text(c, lab, 41, yy - 14, 24, 600, colr, kk)
            token_row(c, win, 41, yy, t, t0 + 0.1, bw=118, bh=58, gap=12, fs=28, fmt='{:.2f}', colors=[colr] * 5,
                      labels=LAGS if i == 1 else None, lab_fs=19)
        sim_label(c, 360, 692, ramp(t, 0.6, 0.6), 19, 'center')


class UpDownBars(Scene):
    """Table 1, velocity hidden: the MLP on x(t) alone vs the best transformer on five samples (log columns)."""
    vertical = True
    dur = 17.0
    cues = [(1.0, 'pop'), (6.0, 'pop'), (9.0, 'chime')]
    LO, HI, FLOOR, HMAX = 1e-6, 1e-1, 520, 400

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.6)
        kicker(c, 'van der pol oscillator · velocity hidden', 360, 34, k, 'muted', 19, align='center')
        log_grid(c, 120, 700, self.FLOOR, self.HMAX, self.LO, self.HI, ramp(t, 0.6, 0.6), 28)
        cols = ((280, 2.485e-2, 'c', 1.0, 'MLP', ['sees x(t) only']),
                (560, 2.065e-5, 'y', 6.0, 'transformer', ['last 5 samples', '2-D latent, PE']))
        tops = []
        for x, v, colr, t0, lab, subs in cols:
            kk = ramp(t, t0, 0.6)
            tops.append(log_col(c, x, self.FLOOR, 150, self.HMAX, v, self.LO, self.HI, colr, kk,
                                ramp(t, t0, 1.1, e_expo), size=30, glow=8 if colr == 'y' else 0))
            text(c, lab, x, self.FLOOR + 40, 26, 700, 'ink', kk, 'center')
            for j, s in enumerate(subs):
                text(c, s, x, self.FLOOR + 72 + j * 28, 21, 500, 'muted', kk, 'center')
        # Table 1 means: 2.485e-2 / 2.065e-5 ≈ 1203
        ks = ramp(t, 9.0, 0.7, e_expo)
        if ks > 0:
            line(c, 360, tops[0], 640, tops[0], 'c', ks * 0.7, 1.6, dash=[8, 7])
            arrow(c, 560, tops[0] + 10, 560, tops[1] - 50, 'y', ks, 3, 14, prog=ramp(t, 9.0, 0.8, e_io))
            text(c, '≈ 1200×', 700, 100, 60, 760, 'y', ks, 'right')
            text(c, 'lower error than the MLP', 700, 140, 22, 500, 'ink', ks, 'right')
        kf = ramp(t, 1.0, 0.6)
        text(c, 'Table 1 · one-step test MSE, mean of 10 seeds', 360, 664, 19, 400, 'muted', kf, 'center', kind='mono')
        text(c, 'log scale · lower is better · PE: positional encoding', 360, 692, 19, 400, 'muted', kf, 'center', kind='mono')


# ================================================================ unfold: Chafee-Infante, latent of two or three
class FoldV(Scene):
    """Our Chafee-Infante simulation: the two mirror halves in true coordinates, then folded in the one-sensor view."""
    vertical = True
    dur = 19.0
    cues = [(0.3, 'draw'), (11.0, 'sweep'), (13.5, 'pop')]

    def __init__(self):
        F = _unfold().Fold()                   # reuse its data and its computed far-apart / nearly-touching pair
        self.br, self.pair = F.br, F.pair

    def draw(self, c, t):
        colr = {1: 'y', -1: 'g'}
        k = ramp(t, 0.2, 0.6)
        A = Axes(80, 60, 560, 290, (-1.3, 1.3), (-0.87, 0.87))
        text(c, 'true coordinates', 40, 34, 21, 600, 'ink', k, kind='mono')
        text(c, 'chafee–infante, ν = 0.16', 690, 34, 19, 400, 'muted', k, 'right', kind='mono')
        if k > 0:
            X0, Y0 = A.px(0, 0)
            line(c, A.x, Y0, A.x + A.w, Y0, 'faint', k, 1.2)
            line(c, X0, A.y, X0, A.y + A.h, 'faint', k, 1.2)
            text(c, 'φ₁', A.x + A.w + 10, Y0 + 8, 24, 500, 'muted', k)
            text(c, 'φ₂', X0 + 12, A.y + 16, 24, 500, 'muted', k)
            pr = ramp(t, 0.3, 2.2, e_io)
            for kd, h, p, q in self.br:
                draw_poly(c, A.pts(p[:, 0], p[:, 1]), colr[h], k * (0.95 if kd == 'edge' else 0.55), 3.4 if kd == 'edge' else 1.4, pr)
            kh = ramp(t, 5.5, 0.6)
            text(c, 'upper half', A.px(-0.62, 0)[0] - 14, A.px(0, 0.5)[1], 22, 600, 'y', kh, 'right')
            text(c, 'lower half', A.px(-0.62, 0)[0] - 14, A.px(0, -0.5)[1] + 14, 22, 600, 'g', kh, 'right')
            text(c, 'mirror images', A.px(0.7, 0)[0], A.px(0, -0.62)[1] + 14, 21, 500, 'muted', kh, 'center', kind='italic')
        kd_ = ramp(t, 11.0, 0.7)
        B = Axes(210, 430, 240, 230, (-0.2, 0.2), (-0.2, 0.2))
        if kd_ > 0:
            arrow(c, 330, 368, 330, 418, 'y', kd_, 2.6, 12, prog=ramp(t, 11.0, 0.6, e_io))
            text(c, 'one sensor, two readings', 360, 400, 19, 600, 'y', kd_, kind='mono')
            rrect(c, B.x, B.y, B.w, B.h, 6, stroke='line', sw=1.4, a=kd_)
            X0, Y0 = B.px(0, 0)
            line(c, B.x, Y0, B.x + B.w, Y0, 'faint', kd_, 1.2)
            line(c, X0, B.y, X0, B.y + B.h, 'faint', kd_, 1.2)
            text(c, 'what one', 480, 470, 22, 600, 'ink', kd_)
            text(c, 'sensor sees', 480, 498, 22, 600, 'ink', kd_)
            text(c, 'across: u(t − τ)', 480, 534, 19, 400, 'muted', kd_, kind='mono')
            text(c, 'up: u(t)', 480, 560, 19, 400, 'muted', kd_, kind='mono')
            pr = ramp(t, 11.4, 1.8, e_io)
            for kd, h, p, q in self.br:
                draw_poly(c, B.pts(q[:, 0], q[:, 1]), colr[h], kd_ * (0.95 if kd == 'edge' else 0.55), 3.0 if kd == 'edge' else 1.4, pr)
        kp = ramp(t, 13.5, 0.6, e_back)
        if kp > 0:
            u, l = self.pair
            kk = min(kp, 1)
            pa, pb = A.px(u[0], u[1]), A.px(l[0], l[1])
            line(c, pa[0], pa[1], pb[0], pb[1], 'ink', kk * 0.7, 1.6, dash=[6, 6])
            for (p, cc) in ((pa, 'y'), (pb, 'g')):
                circle(c, p[0], p[1], 10 * min(kp, 1.2), fill=cc, a=kk, glow=10)
                circle(c, p[0], p[1], 16, stroke='ink', sw=1.6, a=kk * 0.8)
            qa, qb = B.px(u[2], u[3]), B.px(l[2], l[3])
            for (p, cc) in ((qa, 'y'), (qb, 'g')):
                circle(c, p[0], p[1], 9 * min(kp, 1.2), fill=cc, a=kk, glow=10)
            mq = ((qa[0] + qb[0]) / 2, (qa[1] + qb[1]) / 2)
            circle(c, mq[0], mq[1], 24, stroke='ink', sw=1.6, a=kk * 0.8)
            text(c, 'far apart', (pa[0] + pb[0]) / 2 + 14, (pa[1] + pb[1]) / 2 - 10, 24, 700, 'ink', kk)
            text(c, 'nearly touch', mq[0] - 34, mq[1] + 8, 24, 700, 'ink', kk, 'right')
        sim_label(c, 360, 692, ramp(t, 0.6, 0.6), 19, 'center')


class RoomV(Scene):
    """ILLUSTRATIONS of §4.2: a latent of 2 squashes the surface into a thick curve; a latent of 3 unfolds it."""
    vertical = True
    dur = 17.0
    cues = [(0.4, 'draw'), (8.5, 'sweep')]

    def __init__(self):
        U = _unfold()
        self.thick, self.sheet = U.Thick(), U.sheet3d

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                panel(c, 10, 10, 700, 330)
                kicker(c, 'a latent of 2 numbers', 40, 50, 1, 'c', 20)
            illustration(c, 690, 50, k, size=19, align='right')
            self.thick.draw(c, 110, 76, 520, 170, t, 0.5)
            text(c, 'collapses into a thick curve', 40, 294, 26, 600, 'ink', ramp(t, 1.5, 0.6))
            text(c, 'unstable across ten seeds', 40, 324, 21, 500, 'muted', ramp(t, 2.5, 0.6))
        k3 = ramp(t, 8.5, 0.7, e_expo)
        if k3 > 0:
            with layer(c, k3):
                panel(c, 10, 360, 700, 330, stroke='f')
                kicker(c, 'a latent of 3 numbers', 40, 400, 1, 'f', 20)
            illustration(c, 690, 400, k3, size=19, align='right')
            self.sheet(c, 370, 525, 120, 0.55 + 0.35 * math.sin(0.35 * t), k3, prog=ramp(t, 8.7, 1.6, e_io))
            text(c, 'unfolds into a surface', 40, 644, 26, 600, 'ink', ramp(t, 9.2, 0.6))
            text(c, 'sine-wave amplitudes readable', 40, 674, 21, 500, 'muted', ramp(t, 10.0, 0.6))
            text(c, '§4.2, Fig. 8–9', 690, 674, 19, 400, 'muted', ramp(t, 10.0, 0.6), 'right', kind='mono')


# ================================================================ reynolds: cylinder flow, with and without Re
class LoopsV(Scene):
    """ILLUSTRATIONS of §4.3: the wake and one sensor; latent loops overlapping without Re, ordered with Re."""
    vertical = True
    dur = 19.0
    cues = [(0.3, 'whoosh_soft'), (4.5, 'draw'), (11.5, 'sweep')]
    RES = (100, 133, 233, 333, 433, 533, 633, 733, 750)

    def __init__(self):
        self.over = illus_loops(self.RES, separated=False, seed=3)
        self.sep = illus_loops(self.RES, separated=True)
        self.cols = [mix('g', 'y', i / 8) for i in range(9)]
        self.wake = _unfold().wake

    def draw(self, c, t):
        k = ramp(t, 0.1, 0.6)
        sp = self.wake(c, 40, 20, 640, 190, t, k, sensor=ramp(t, 1.0, 0.6))
        if k > 0:
            lw = text_width('one sensor', 20, 600)
            rrect(c, sp[0] + 18, sp[1] - 52, lw + 22, 34, 8, fill='bg0', a=k, fa=k * 0.85)
            text(c, 'one sensor', sp[0] + 29, sp[1] - 28, 20, 600, 'y', ramp(t, 1.0, 0.6))
        illustration(c, 680, 240, k, size=19, align='right')
        text(c, 'Reynolds number 100 to 750', 40, 240, 21, 600, 'ink', ramp(t, 1.5, 0.6))
        for i, (lab, loops, t0, colr) in enumerate((('without Re', self.over, 4.5, 'c'),
                                                    ('with Re as input', self.sep, 11.5, 'f'))):
            kk = ramp(t, t0, 0.7, e_expo)
            if kk <= 0:
                continue
            x = 10 + i * 360
            with layer(c, kk):
                panel(c, x, 270, 340, 420, stroke=colr)
                text(c, lab, x + 24, 308, 23, 700, colr, 1)
                text(c, 'its latent loops', x + 24, 336, 19, 400, 'muted', 1, kind='mono')
            latent_loop(c, x + 20, 352, 300, 250, loops, t, t0, kk, colors=self.cols, frame=False, stagger=0.12,
                        dur=1.4, dot_speed=0.18, widths=[2.4] * 9)
            kl = ramp(t, t0 + 1.6, 0.6) * kk
            text(c, 'Re 100', x + 24, 630, 19, 600, 'g', kl, kind='mono')
            text(c, '→ 750', x + 110, 630, 19, 600, 'y', kl, kind='mono')
            text(c, ('regimes overlap' if i == 0 else 'separate, in order'), x + 24, 668, 22, 600, 'ink', kl)


class ReconV(Scene):
    """§4.3 / App. A.5: full-field v_x reconstruction from the latent, with and without Re (log columns)."""
    vertical = True
    dur = 15.0
    cues = [(0.6, 'pop'), (6.0, 'pop'), (7.4, 'chime')]
    LO, HI, FLOOR, HMAX = 1e-5, 1e-1, 520, 340

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.6)
        kicker(c, 'rebuild the full vₓ field from the latent', 360, 34, k, 'muted', 19, align='center')
        log_grid(c, 110, 700, self.FLOOR, self.HMAX, self.LO, self.HI, ramp(t, 0.5, 0.6), 28)
        for g, (lab, v1, v2) in enumerate(CYL_RECON):
            cx = 255 + g * 300
            kg = ramp(t, 0.6, 0.6)
            text(c, lab, cx, self.FLOOR + 40, 26, 700, 'ink', kg, 'center')
            for j, (v, colr, t0) in enumerate(((v1, 'f', 0.6 + 0.3 * g), (v2, 'c', 6.0 + 0.4 * g))):
                kk = ramp(t, t0, 0.6)
                log_col(c, cx - 58 + j * 116, self.FLOOR, 96, self.HMAX, v, self.LO, self.HI, colr, kk,
                        ramp(t, t0, 1.1, e_expo), label=sci(v), size=28)
        kl = ramp(t, 0.6, 0.6)
        rrect(c, 130, 588, 22, 22, 5, fill='f', a=kl, fa=kl * 0.88)
        text(c, 'with Re', 162, 607, 22, 600, 'f', kl)
        kn = ramp(t, 6.0, 0.6)
        rrect(c, 360, 588, 22, 22, 5, fill='c', a=kn, fa=kn * 0.88)
        text(c, 'without Re', 392, 607, 22, 600, 'c', kn)
        # 7.45e-3 / 1.12e-4 = 66.5 (field); 1.33e-2 / 2.48e-4 = 53.6 (wake)
        ks = ramp(t, 7.4, 0.7, e_expo)
        if ks > 0:
            text(c, '≈ 70× worse', 360, 100, 58, 760, 'c', ks, 'center')
            text(c, 'without Re: 66.5× over the field, 53.6× in the wake', 360, 138, 20, 500, 'ink', ks, 'center')
        text(c, 'mean absolute error · log scale · §4.3, App. A.5', 360, 652, 19, 400, 'muted', k, 'center', kind='mono')
        text(c, 'largest one-step error, both models: ≈ 2.3 × 10⁻²', 360, 684, 19, 400, 'muted', ramp(t, 11.0, 0.6), 'center', kind='mono')
