"""Rebuilding a hidden state: attention as a delay embedding (§2.3 Takens, §4.1 Van der Pol, Table 1, Fig. 6 of
arXiv:2512.21113v2). Drawing pieces come from dynamics/videos/sign/dynkit.py; Van der Pol curves are OUR simulation of
the paper's equations (vdp.json, written by sign/simulate.py); bar values are typed from Table 1."""
from dynkit import *

VDP = load_json('vdp.json')
PER = VDP['period']
CT, CX, CV = (np.array(VDP[k]) for k in ('cycle_t', 'cycle_x', 'cycle_v'))
A_PT, B_PT = VDP['same_x']['points']            # x = 1.0 on the cycle: A rising (v > 0), B falling (v < 0)
WIN_A = A_PT['window'][::-1]                     # oldest first: x(t−4) ... x(t)
WIN_B = B_PT['window'][::-1]
LAGS = ['x(t−4)', 'x(t−3)', 'x(t−2)', 'x(t−1)', 'x(t)']

def cyc_x(tt):
    return np.interp(np.mod(tt, PER), CT, CX)

# our calculation: around the simulated cycle, x(t) against x(t) minus the plain average of the last five samples
# (dt = 0.1). The average is what attention with uniform weights takes; with the current sample, a linear map can
# form this difference. Not the paper's trained latent.
_TS = np.linspace(0, PER, 400, endpoint=False)
_XT = cyc_x(_TS)
GAP_LOOP = np.stack([_XT, _XT - np.mean([cyc_x(_TS - 0.1 * k) for k in range(5)], 0)], 1)
GAP_A, GAP_B = 1.0 - float(np.mean(WIN_A)), 1.0 - float(np.mean(WIN_B))   # +0.44 (rising) and −0.25 (falling)

# Table 1 (App. A.2.1), one-step test MSE on the limit cycle, mean over 10 seeds
FULL = [('MLP only', 1.455e-7, 'c'), ('attention, no PE', 2.765e-7, 'g'), ('attention, PE', 9.504e-8, 'y')]

def timed_bars(c, x, y, w, rows, t, lo=1e-5, hi=1e-1, label_w=470, bh=34, dy=74, fs=24, a=1.0, t_axis=0.6,
               note_s='lower is better', glow_last=None):
    """log_bars with its own start time per row: rows [(label, value, colour, t0)]."""
    bx = x + label_w
    sc = w / (math.log10(hi) - math.log10(lo))
    k0 = ramp(t, t_axis, 0.6) * a
    if k0 <= 0:
        return
    for e in range(int(round(math.log10(lo))), int(round(math.log10(hi))) + 1):
        X = bx + (e - math.log10(lo)) * sc
        line(c, X, y - 30, X, y + dy * len(rows) - 24, 'line', k0 * 0.8, 1)
        text(c, decade(e), X, y - 42, fs * 0.85, 500, 'muted', k0, 'center')
    if note_s:
        text(c, note_s, bx + w, y + dy * len(rows) + 6, fs * 0.72, 400, 'muted', k0, 'right', kind='mono')
    for i, (lab, v, colr, ti) in enumerate(rows):
        k = ramp(t, ti, 0.6) * a
        if k <= 0:
            continue
        yy = y + i * dy
        text(c, lab, bx - 20, yy + bh * 0.74, fs, 600, 'ink', k, 'right')
        ww = max(3, (math.log10(v) - math.log10(lo)) * sc * ramp(t, ti, 1.0, e_expo))
        g = 10 if (glow_last is not None and i == len(rows) - 1 and t > glow_last) else 0
        rrect(c, bx, yy, ww, bh, 5, fill=colr, a=k, fa=k * 0.85, glow=g)
        text(c, sci(v), bx + ww + 12, yy + bh * 0.74, fs * 0.9, 600, colr, k)


class ColdOpen(Scene):
    dur = 21.0
    fade_in = 0.3
    cues = [(0.4, 'whoosh_soft'), (10.0, 'pop')]
    GX, GY0, GY1 = 330, 300, 840                 # the gauge: x = +2.2 at GY0, −2.2 at GY1

    def gy(self, v):
        return lerp(self.GY1, self.GY0, (v + 2.2) / 4.4)

    def draw(self, c, t):
        k = ramp(t, 0.2, 0.8)
        gx = self.GX
        kicker(c, 'all you can see: the height x', gx, self.GY0 - 48, k, 'muted', 18, align='center')
        line(c, gx, self.GY0, gx, self.GY1, 'muted', k, 3)
        for v in (-2, -1, 0, 1, 2):
            Y = self.gy(v)
            line(c, gx - 14, Y, gx + 14, Y, 'muted', k, 2)
            text(c, f'{v:+d}'.replace('-', '−') if v else '0', gx - 30, Y + 8, 22, 500, 'muted', k, 'right', kind='mono')
        # the dot runs once round the (simulated) cycle and lands on x = 1, on its way up
        p = (1.0 + A_PT['t'] / PER) * e_io(clamp((t - 0.3) / 4.6))
        xv = float(cyc_x(p * PER))
        circle(c, gx, self.gy(xv), 22, fill='y', a=k, glow=14)
        kq = ramp(t, 5.0, 0.7, e_expo)
        if kq > 0:
            Y = self.gy(1.0)
            text(c, 'x = 1.00', gx + 46, Y + 12, 40, 600, 'y', kq, kind='mono')
            arrow(c, gx + 260, Y - 20, gx + 260, Y - 100, 'f', kq, 3, 14)
            text(c, 'up?', gx + 290, Y - 60, 34, 400, 'f', kq, kind='italic')
            arrow(c, gx + 260, Y + 20, gx + 260, Y + 100, 'c', kq, 3, 14)
            text(c, 'down?', gx + 290, Y + 80, 34, 400, 'c', kq, kind='italic')
        for i, (win, colr, lab, t0) in enumerate(((WIN_A, 'f', 'climbing to 1: on the way up', 10.0),
                                                  (WIN_B, 'c', 'falling to 1: on the way down', 11.2))):
            kk = ramp(t, t0, 0.7, e_expo)
            if kk <= 0:
                continue
            yy = 300 + i * 270
            with layer(c, kk):
                panel(c, 900, yy, 900, 230)
                kicker(c, f'history {"ab"[i]} · last five samples', 936, yy + 46, 1, 'muted', 17)
            token_row(c, win, 936, yy + 72, t, t0 + 0.2, bw=124, bh=60, gap=16, fs=26, fmt='{:.2f}',
                      colors=[colr] * 5, labels=LAGS, lab_fs=18)
            text(c, lab, 1764, yy + 46, 24, 600, colr, kk, 'right')
        sim_label(c, 200, 1010, ramp(t, 0.8, 0.6), 16)          # the dot's path and both windows: vdp.json
        caption(c, t, 'The {c:velocity} is hidden. The {y:history} holds it.', 15.0, None, y=930, size=46)


class Title(TitleCard):
    TITLE = 'Rebuilding a *hidden* state'
    STICKY = ['attention as', 'delay embedding']


class VdP(Scene):
    dur = 27.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (5.0, 'draw'), (12.5, 'tick')]
    SETUP = [('1,500 starting points', 'x and velocity drawn from [−3, 3]'), ('sampled every 0.1', 'time units, over [0, 6.5]'),
             ('task', 'predict the next sample'), ('ten training runs', 'per model, different seeds')]

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the test system', 'The Van der Pol *oscillator*', sub='§4.1 · μ = 0.5')
        trans = [(np.array(r['x']), np.array(r['v'])) for r in VDP['transients']]
        mv = ((t - 7.5) / 4.0) % 1.0 if t > 7.5 else None
        ax = phase_portrait(c, 200, 380, 540, 540, t, 4.4, cycle=(CX, CV), transients=trans, mover=mv, fs=20,
                            xlabel='position x', ylabel='velocity')
        sim_label(c, 200, 1010, ramp(t, 5.0, 0.6), 16)
        k1 = ramp(t, 0.5, 0.8)
        if k1 > 0:
            with layer(c, k1):
                panel(c, 900, 360, 900, 220)
                tex(c, 'vdp', 1350, 440, 54, 1)
                text(c, 'x: position', 960, 540, 26, 500, 'ink', 1)
                text(c, 'ẋ: velocity (how fast x changes)', 1170, 540, 26, 500, 'ink', 1)
        for i, (big, small) in enumerate(self.SETUP):
            kk = ramp(t, 12.5 + i * 0.5, 0.6, e_expo)
            if kk <= 0:
                continue
            yy = 620 + i * 66
            with layer(c, kk):
                with xform(c, (1 - kk) * 24, 0):
                    circle(c, 920, yy - 9, 6, fill='y', a=1)
                    w = text(c, big, 944, yy, 28, 600, 'ink', 1)
                    text(c, small, 944 + w + 16, yy, 24, 400, 'muted', 1)
        k4 = ramp(t, 20.0, 0.7, e_expo)
        if k4 > 0 and mv is not None:
            p = end_point(ax.pts(CX, CV), mv)
            circle(c, p[0], p[1], 20, stroke='ink', sw=2.4, a=k4)
        caption(c, t, 'Each point is a {y:full state}: know both numbers, and the next step is fixed.', 20.0, None,
                x=1350, y=905, size=28, maxw=880)


class FullState(Scene):
    dur = 22.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (4.5, 'pop'), (11.0, 'sweep')]

    def draw(self, c, t):
        hdr(self, c, t, '02', 'full observation', 'Give it the *whole* state')
        k0 = ramp(t, 0.8, 0.7, e_expo)
        if k0 > 0:
            with layer(c, k0):
                panel(c, 120, 340, 720, 250)
                kicker(c, 'the whole state: position and velocity' if t < 4.5 else 'mlp: the current state only', 156, 384, 1, 'muted', 17)
            token_row(c, ['x, ẋ'], 160, 440, t, 1.0, bw=130, bh=64, fs=24, colors=['y'], labels=['now'])
        k = ramp(t, 4.5, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                arrow(c, 310, 472, 400, 472, 'muted', 1, 2.4, 12)
                rrect(c, 410, 436, 150, 72, 14, stroke='ink', sw=2, a=1)
                text(c, 'MLP', 485, 482, 28, 600, 'ink', 1, 'center')
                arrow(c, 570, 472, 650, 472, 'muted', 1, 2.4, 12)
                text(c, 'next', 662, 482, 26, 600, 'f', 1)
        k2 = ramp(t, 7.0, 0.7, e_expo)
        if k2 > 0:
            with layer(c, k2):
                panel(c, 880, 340, 920, 250)
                kicker(c, 'transformer: the last five states', 916, 384, 1, 'muted', 17)
                token_row(c, ['x, ẋ'] * 5, 916, 440, t, 7.1, bw=96, bh=64, gap=10, fs=20, colors=['y'] * 5,
                          labels=['t−4', 't−3', 't−2', 't−1', 't'])
                arrow(c, 1446, 472, 1500, 472, 'muted', 1, 2.4, 12)
                rrect(c, 1510, 426, 170, 92, 14, stroke='ink', sw=2, a=1)
                text(c, 'attention', 1595, 466, 22, 600, 'g', 1, 'center')
                text(c, '+ MLP', 1595, 498, 22, 600, 'ink', 1, 'center')
                arrow(c, 1690, 472, 1726, 472, 'muted', 1, 2.4, 10)
                text(c, 'next', 1734, 482, 22, 600, 'f', 1)
        rows = [(lab, v, colr, 11.0 + i * 0.4) for i, (lab, v, colr) in enumerate(FULL)]
        timed_bars(c, 120, 720, 1180, rows, t, lo=1e-8, hi=1e-1, label_w=430, t_axis=10.6, note_s=None)
        kn = ramp(t, 11.6, 0.6)
        note(c, 'test error (MSE), Table 1, full observation · lower is better · the polynomial NARX baseline (7.1 × 10⁻⁴) is not shown',
             120, 960, kn, 16)
        caption(c, t, 'Complete state: history adds {y:nothing}.', 16.5, None, x=1560, y=790, size=36, maxw=440)


class Hide(Scene):
    dur = 29.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (4.5, 'pop'), (11.0, 'tick'), (18.5, 'draw')]

    def draw(self, c, t):
        hdr(self, c, t, '03', 'partial observation', 'Hide the *velocity*')
        ax = phase_portrait(c, 200, 380, 520, 520, t, 0.4, cycle=(CX, CV), fs=20, xlabel='position x: seen',
                            ylabel='velocity: hidden', cycle_color='y')
        sim_label(c, 200, 1010, ramp(t, 1.0, 0.6), 16)
        kx = ramp(t, 4.5, 0.6)
        if kx > 0:
            X, _ = ax.px(1.0, 0)
            line(c, X, 380, X, 900, 'ink', kx * 0.7, 1.8, dash=[8, 7])
            text(c, 'x = 1', X + 10, 406, 20, 600, 'ink', kx, kind='mono')
            for i, (pt, colr, lab) in enumerate(((A_PT, 'f', 'rising'), (B_PT, 'c', 'falling'))):
                kk = ramp(t, 5.0 + i * 0.6, 0.5, e_back)
                if kk <= 0:
                    continue
                PX, PY = ax.px(pt['x'], pt['v'])
                circle(c, PX, PY, 12 * min(kk, 1.2), fill=colr, a=min(kk, 1), glow=8)
                if i == 0:
                    text(c, lab, PX - 18, PY - 16, 24, 600, colr, min(kk, 1), 'right')
                else:
                    text(c, lab, PX + 20, PY + 30, 24, 600, colr, min(kk, 1))
        km = ramp(t, 11.0, 0.7, e_expo)
        if km > 0:
            with layer(c, km):
                panel(c, 860, 360, 940, 230)
                kicker(c, 'what the mlp sees, both times', 896, 404, 1, 'muted', 17)
                token_row(c, [1.0], 900, 450, t, 11.1, bw=130, bh=64, fs=26, fmt='{:.2f}', colors=['y'], labels=['x(t)'])
                arrow(c, 1050, 470, 1150, 430, 'f', 1, 2.4, 12)
                arrow(c, 1050, 494, 1150, 534, 'c', 1, 2.4, 12)
                text(c, 'going up?', 1166, 438, 26, 600, 'f', 1)
                text(c, 'coming down?', 1166, 548, 26, 600, 'c', 1)
                rich(c, 'same input: it can only {y:split the difference}', 1420, 470, 25, 360, t, 11.4, 0.02, 0.4)
        for i, (win, colr, lab, t0) in enumerate(((WIN_A, 'f', 'rising', 18.5), (WIN_B, 'c', 'falling', 19.3))):
            kk = ramp(t, t0, 0.6)
            if kk <= 0:
                continue
            yy = 650 + i * 150
            text(c, lab, 1020, yy + 40, 28, 600, colr, kk, 'right')
            token_row(c, win, 1050, yy, t, t0, bw=118, bh=60, gap=14, fs=26, fmt='{:.2f}', colors=[colr] * 5,
                      labels=LAGS if i == 1 else None, lab_fs=18)
        kicker(c, 'the last five samples · oldest on the left', 1050, 630, ramp(t, 18.5, 0.6), 'muted', 16)
        caption(c, t, 'History tells the two {y:apart}.', 25.0, None, x=1330, y=1000, size=34)


class Takens(Scene):
    dur = 35.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (6.0, 'draw'), (12.5, 'sweep'), (20.0, 'pop'), (27.0, 'pop')]
    I0, I1 = 395, 476                       # long trajectory samples 395-476: t = 39.5 to 47.6

    def draw(self, c, t):
        hdr(self, c, t, '04', 'delay embedding', 'Takens: the past *stands in*', sub='§2.3, Eq. 19')
        kq = ramp(t, 0.6, 0.8)
        if kq > 0:
            rich(c, 'Takens’ theorem: past values of {y:one measurement} can rebuild the hidden state',
                 MX, 340, 26, 1200, t, 0.6, 0.02, 0.4, base='muted')
        ts = np.array(VDP['long_t'][self.I0:self.I1])
        xs = np.array(VDP['long_x'][self.I0:self.I1])
        delay_window(c, 140, 430, 800, 200, ts, xs, 40, 5, t, 6.0, color='y', line_color='g', fs=19,
                     slide=(9.0, 3.0, 70), vec_xy=(1000, 422), vec_bw=118)
        note(c, 'x only, every 0.1 time units · ' + SIM, 140, 690, ramp(t, 6.4, 0.6), 16)
        latent_loop(c, 1370, 420, 410, 300, [np.array(VDP['pca_loop'])], t, 12.5, colors=['y'], square=False,
                    axis_labels=('pc 1', 'pc 2'), fs=18, dot_speed=0.3)
        kl = ramp(t, 13.0, 0.6)
        note(c, 'our delay coordinates: each 5-sample', 1370, 790, kl, 15)
        note(c, 'window, first two principal components', 1370, 812, kl, 15)
        note(c, '(axes scaled separately)', 1370, 834, kl, 15)
        kt = ramp(t, 20.0, 0.8, e_expo)
        if kt > 0:
            with layer(c, kt):
                panel(c, 120, 740, 760, 200)
                tex(c, 'takens', 290, 820, 60, 1)
                text(c, 'samples are enough', 470, 806, 24, 600, 'ink', 1)
                text(c, 'for an attractor of dimension d', 470, 840, 24, 400, 'muted', 1)
                text(c, 'and a generic measurement', 470, 872, 24, 400, 'muted', 1)
                note(c, 'a sufficient condition, not a minimum', 156, 912, 1, 16)
        kp = ramp(t, 27.0, 0.8, e_expo)
        if kp > 0:
            with layer(c, kp):
                panel(c, 920, 740, 400, 200, stroke='y')
                kicker(c, 'the paper', 956, 786, 1, 'muted', 17)
                text(c, 'd = 2  →  n = 5', 956, 852, 34, 600, 'y', 1, kind='mono')
                text(c, 'five past samples', 956, 904, 24, 500, 'ink', 1)
                note(c, 'd = 2: the state dimension · the loop itself is 1-D, so five is generous', 920, 978, 1, 16)


class Table1(Scene):
    dur = 38.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (24.0, 'sweep')]
    ROWS = [('MLP only', 2.485e-2, 'c', 5.5), ('polynomial NARX, 5 delays', 2.192e-3, 'v', 10.5),
            ('attention, 1D latent, no PE', 1.789e-3, 'g', 17.0), ('attention, 2D latent, no PE', 1.770e-3, 'g', 17.4),
            ('attention, 1D latent, PE', 5.848e-4, 'f', 24.0), ('attention, 2D latent, PE', 2.065e-5, 'y', 24.6)]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'results, x only', 'History *wins*',
            sub='Van der Pol, velocity hidden · one-step test error (MSE), mean of 10 seeds (NARX: one deterministic fit) · Table 1')
        timed_bars(c, 120, 440, 900, self.ROWS, t, label_w=500, t_axis=0.6, glow_last=24.6)
        kp = ramp(t, 17.0, 0.6)
        note(c, 'PE: positional encoding, a tag saying which sample is which', 120, 935, kp, 17)
        # ratios of Table 1 means: 2.485e-2 / 2.065e-5 ≈ 1203, 2.192e-3 / 2.065e-5 ≈ 106
        stat(c, 1570, 640, '≈ 1200×', 'MLP error ÷ best error', 'y', ramp(t, 31.0, 0.7, e_expo), 56)
        stat(c, 1570, 790, '≈ 106×', 'NARX error ÷ best error', 'v', ramp(t, 32.0, 0.7, e_expo), 42)


class Latent(Scene):
    dur = 32.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (4.5, 'draw'), (12.0, 'pop'), (19.0, 'draw'), (25.5, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '06', 'inside the model', 'Two *corrections* for one x')
        token_row(c, [''] * 5, 140, 360, t, 0.8, bw=84, bh=56, gap=10, fs=20, colors=['g'] * 5, labels=LAGS, lab_fs=16)
        k = ramp(t, 4.5, 0.7)
        if k > 0:
            with layer(c, k):
                arrow(c, 616, 388, 690, 388, 'muted', 1, 2.4, 12)
                rrect(c, 700, 350, 190, 76, 14, stroke='g', sw=2, a=1)
                text(c, 'attention', 795, 398, 26, 600, 'g', 1, 'center')
                arrow(c, 900, 388, 980, 388, 'muted', 1, 2.4, 12)
                text(c, 'correction z', 990, 398, 26, 600, 'g', 1)
                panel(c, 1180, 340, 330, 96, stroke='f')
                tex(c, 'hsum', 1345, 388, 46, 1)
                arrow(c, 1520, 388, 1580, 388, 'muted', 1, 2.4, 12)
                rrect(c, 1590, 350, 100, 76, 14, stroke='ink', sw=2, a=1)
                text(c, 'MLP', 1640, 398, 26, 600, 'ink', 1, 'center')
                arrow(c, 1698, 388, 1734, 388, 'muted', 1, 2.4, 10)
                text(c, 'next', 1742, 396, 22, 600, 'f', 1)
                note(c, 'e: the current sample, embedded · z: what attention adds from the window · the MLP reads h', 140, 500, 1, 16)
        for i, (tag, body, t0) in enumerate((('paper, fig. 6b', 'same x, {g:two different corrections z}: one for each phase', 12.0),
                                             ('paper, fig. 6d', 'with a {f:2-D latent}, h traces a {y:limit-cycle loop} (with or without PE)', 25.5))):
            kk = ramp(t, t0, 0.8, e_expo)
            if kk <= 0:
                continue
            yy = 590 + i * 190
            with layer(c, kk):
                with xform(c, (1 - kk) * 30, 0):
                    panel(c, 1060, yy, 740, 160)
                    kicker(c, tag, 1096, yy + 44, 1, 'muted', 16)
                    rich(c, body, 1096, yy + 92, 27, 680, t, t0 + 0.3, 0.02, 0.4)
        note(c, 'the paper’s figures are images: we describe them, we don’t redraw them', 1060, 960, ramp(t, 12.6, 0.6), 15)
        ax = trace_plot(c, 230, 610, 640, 310, [dict(x=np.r_[GAP_LOOP[:, 0], GAP_LOOP[:1, 0]],
                                                    y=np.r_[GAP_LOOP[:, 1], GAP_LOOP[:1, 1]], color='y', w=3.5, glow=4, dur=2.0)],
                        t, 19.0, xr=(-2.4, 2.4), yr=(-0.75, 0.75), xticks=(-2, -1, 0, 1, 2), yticks=(-0.5, 0, 0.5),
                        xlabel='x(t)', ylabel='x(t) minus the average of the last five', fs=18)
        kx = ramp(t, 20.5, 0.6)
        if kx > 0:
            X, _ = ax.px(1.0, 0)
            line(c, X, 610, X, 920, 'ink', kx * 0.6, 1.6, dash=[7, 6])
            for m, colr, lab in ((GAP_A, 'f', f'rising: {GAP_A:+.2f}'), (GAP_B, 'c', f'falling: {GAP_B:+.2f}')):
                PX, PY = ax.px(1.0, m)
                circle(c, PX, PY, 10, fill=colr, a=kx, glow=8)
                if colr == 'f':
                    text(c, lab.replace('-', '−'), PX - 18, PY - 14, 20, 600, colr, kx, 'right')
                else:
                    text(c, lab.replace('-', '−'), PX + 18, PY + 34, 20, 600, colr, kx)
        note(c, 'our calculation on the simulated cycle · uniform weights, not the paper’s trained model', 230, 1010,
             ramp(t, 19.4, 0.6), 15)


class Attention(Scene):
    dur = 36.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (8.0, 'tick'), (14.0, 'sweep'), (20.0, 'pop'), (27.5, 'pop')]
    UNIFORM = [0.2] * 5
    LAGGED = [0.07, 0.11, 0.17, 0.26, 0.39]       # an ILLUSTRATIVE lag-specific pattern (shape ours, not the paper's)

    def draw(self, c, t):
        hdr(self, c, t, '07', 'attention weights', 'Spread over the *window*', sub='§4.1, Fig. 6e–g (10 seeds each)')
        lab = 'without positional encoding: nearly uniform' if t < 14.4 else 'with positional encoding: lag-specific'
        kicker(c, lab, 170, 400, ramp(t, 8.0, 0.6) * (1 - ramp(t, 14.0, 0.3)) + ramp(t, 14.4, 0.4), 'g' if t < 14.4 else 'f', 18)
        attention_bars(c, 170, 470, 620, 290, self.UNIFORM, t, 0.8, color='g', fs=20, vmax=0.5,
                       morph=(14.0, self.LAGGED), highlight=None if t < 14.0 else {i: 'f' for i in range(5)})
        illustration(c, 170, 900, ramp(t, 1.2, 0.6), 'illustration of the patterns §4.1 describes; weights are not the paper’s', 15)
        kq = ramp(t, 20.0, 0.8, e_expo)
        if kq > 0:
            with layer(c, kq):
                panel(c, 920, 360, 880, 230)
                kicker(c, 'the text (§4.1)', 956, 404, 1, 'muted', 17)
                rich(c, 'positional encoding reshapes attention “without {c:systematically improving} prediction accuracy”',
                     956, 460, 28, 800, t, 20.3, 0.02, 0.4)
        kt = ramp(t, 27.5, 0.8, e_expo)
        if kt > 0:
            with layer(c, kt):
                panel(c, 920, 620, 880, 300, stroke='y')
                kicker(c, 'the table (table 1, 2d latent)', 956, 664, 1, 'muted', 17)
            rows = [('no PE', 1.770e-3, 'g', 27.8), ('PE', 2.065e-5, 'y', 28.2)]
            timed_bars(c, 956, 760, 520, rows, t, lo=1e-5, hi=1e-2, label_w=110, bh=32, dy=62, fs=22, t_axis=27.6, note_s=None)
            stat(c, 1620, 800, '≈ 86×', 'lower with PE', 'y', ramp(t, 28.8, 0.7, e_expo), 50)
            note(c, '§5.2 sides with the table: “a measurable improvement”', 956, 900, ramp(t, 29.0, 0.6), 16)


class Discussion(Scene):
    dur = 19.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (11.0, 'chime')]

    def draw(self, c, t):
        hdr(self, c, t, '08', 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('If attention without positions just {y:averages the window}, where is the state rebuilt: in attention, or in the {g:MLP} after it?', 3.0),
                              ('A climate emulator stepping from {y:today’s state alone} can’t see the {c:deep ocean}. How much {y:history} would it need?', 11.0)],
                       size=36)
        extrap_label(c, W - MX - 36, 330 + 250 + 46, ramp(t, 11.3, 0.6), 18, align='right')


class End(EndCard):
    TAKE = 'In these tests, attention helps only when the state is {y:incomplete}: then it rebuilds the {c:hidden} part from the recent past.'
    STATS = [('10⁻⁷', 'MLP and transformer, full state', 'f'), ('≈ 1200×', 'best transformer (2-D, PE) over MLP, x only', 'y'),
             ('≈ 86×', 'what PE adds, 2-D latent (Table 1)', 'g')]
    NEXT = 'journal club · nov 11'
