"""Native 9:16 scenes for the dynamics/shorts/* projects (KIND = 'short', SOURCES = ['dynamics/videos/sign'],
SCENE_MODULES = ['dynshorts']). Each draws in aiglainer.short.BOX (720 x 700), origin top-left. Big type: labels >= 19 px,
numbers >= 28 px. Numbers come from projects/dynamics/AGENTS.md (the paper's sections), via dynkit's constants; spring
and two-mass data are OUR simulations of the paper's equations (sign's simulate.py -> data/), labelled on screen.

Scenes for shorts/average, twoheads and sensor. (The updown, unfold and reynolds shorts use dynshorts2.py.)
"""
from dynkit import *

STIFF, SOFT = SDOF['k2000'], SDOF['k500']

# =============================================================== group 0: average, twoheads, sensor

def _alpha(t, t0=4.0, lo=0.3, amp=0.45, per=7.0):
    """An illustrative softmax weight on x(t) that drifts between lo and lo + amp (never 0 or 1)."""
    return lo + amp * (0.5 - 0.5 * math.cos(2 * math.pi * max(t - t0, 0) / per))

class AvgMix(Scene):
    """shorts/average, part 1: one head's two weights are positive and add up to one; one output number scales both."""
    vertical = True
    dur = 19.0
    cues = [(0.8, 'draw'), (6.4, 'pop'), (12.0, 'pop')]

    def draw(self, c, t):
        text(c, 'one attention head · nothing else', 360, 34, 21, 400, 'muted', ramp(t, 0.3, 0.6), 'center', kind='mono',
             tracking=0.06)
        alpha = _alpha(t)
        k = ramp(t, 0.8, 0.7)
        convex_mix(c, 120, 170, 480, alpha, t, 0.8, 1, color='f', fs=34, show_rule=False)
        text(c, 'weight on each past position', 360, 92, 22, 500, 'ink', k, 'center')
        kr = ramp(t, 6.4, 0.6)
        text(c, 'always > 0, and they add up to 1', 360, 378, 30, 600, 'f', kr, 'center')
        rrect(c, 90, 340, 540, 54, 12, stroke='f', sw=2, a=kr * (1 - ramp(t, 11.6, 0.6)), glow=6)
        illustration(c, 700, 418, k, 'weights: illustration', 19, 'right')
        # then one shared output number scales both: the coefficients share its sign
        ko = ramp(t, 12.0, 0.7)
        if ko > 0:
            wo = lerp(1.0, -1.0, ramp(t, 14.2, 1.4, e_io))
            text(c, f'× one output number wₒ = {wo:+.1f}'.replace('-', '−'), 360, 458, 30, 600, 'g', ko, 'center')
            signed_bars(c, 170, 462, 380, 170, (alpha * wo, (1 - alpha) * wo), t, 12.0, labels=['a₁', 'a₂'], vmax=1.25,
                        fs=28, zero_label=False)
        rich(c, '{y:a₁} and {y:a₂} always share {g:its sign}', 360, 690, 30, 700, t, 15.8, 0.04, 0.4, align='center')

class AvgPlane(Scene):
    """shorts/average, part 2: the coefficient plane; the stiff spring sits where signs agree, the soft one outside."""
    vertical = True
    dur = 18.0
    cues = [(1.2, 'pop'), (5.0, 'pop'), (13.0, 'chime')]

    def draw(self, c, t):
        cx, cy, size = 380, 290, 440
        ax = coef_plane(c, cx, cy, size, t, 0.2, reach=False, fs=23, ticks=(-1, 1),
                        xlabel='a₁ · on x(t)', ylabel='a₂ · on x(t−1)')
        kr = ramp(t, 0.5, 0.8)
        if kr > 0:
            x0, y0, q = cx - size / 2, cy - size / 2, size / 2
            rrect(c, cx, y0, q, q, 0, fill='f', a=kr, fa=kr * 0.13)
            rrect(c, x0, cy, q, q, 0, fill='f', a=kr, fa=kr * 0.13)
            for xx, yy, s, colr in ((cx + q / 2, y0 + 36, 'signs agree', 'f'), (cx - q / 2, cy + q - 18, 'signs agree', 'f'),
                                    (cx + q / 2, cy + q - 18, 'out of reach', 'c'), (cx - q / 2, y0 + 36, 'out of reach', 'c')):
                text(c, s, xx, yy, 20, 600, colr, kr, 'center', kind='mono')
        for a1, a2, colr, lab, ti, side in ((STIFF['a1'], STIFF['a2'], 'g', 'stiff', 1.2, -1),
                                            (SOFT['a1'], SOFT['a2'], 'y', 'soft', 5.0, -1)):
            kk = ramp(t, ti, 0.5, e_back)
            if kk <= 0:
                continue
            X, Y = ax.px(a1, a2)
            circle(c, X, Y, 13 * min(kk, 1.2), fill=colr, a=min(kk, 1), glow=10)
            text(c, lab, X + side * 22, Y - 16, 30, 700, colr, min(kk, 1), 'right')
        note(c, 'stiff (−0.44, −0.98): the paper, §3.1', 40, 600, ramp(t, 1.4, 0.6), 19, 'g')
        note(c, 'soft (+1.24, −0.98): our calculation', 40, 630, ramp(t, 5.2, 0.6), 19, 'y')
        kp = ramp(t, 9.5, 0.6) * (1 - ramp(t, 12.6, 0.5))
        text(c, 'the paper, Fig. 2b: too smooth, no resonance peak', 360, 684, 22, 500, 'c', kp, 'center')
        kb = ramp(t, 13.0, 0.6)
        text(c, 'one head, attention only: a boundary case', 360, 684, 22, 500, 'ink', kb, 'center')

class TwoHeadsMix(Scene):
    """shorts/twoheads, part 1: each head averages, but each has its own output number, of opposite sign (App. A.1)."""
    vertical = True
    dur = 22.0
    cues = [(1.0, 'draw'), (10.0, 'pop'), (13.0, 'pop'), (17.5, 'chime')]

    def draw(self, c, t):
        for i, (colr, wo, ph) in enumerate((('f', TWO_HEAD_WO[0], 0.0), ('c', TWO_HEAD_WO[1], 2.2))):
            k = ramp(t, 0.4 + i * 0.4, 0.7)
            if k <= 0:
                continue
            y = i * 255
            panel(c, 10, y, 700, 245, k, stroke=colr if t > 17.5 else 'line')
            text(c, f'head {i + 1}', 40, y + 36, 24, 600, colr, k, kind='mono', tracking=0.08)
            alpha = _alpha(t, 1.0 + ph, 0.25, 0.5, 6.0)
            convex_mix(c, 80, y + 106, 300, alpha, t, 1.0 + 0.4 * i, k, color=colr, fs=26, show_rule=False)
            kw = ramp(t, 10.0 + 3.0 * i, 0.6)
            text(c, '× its own output number', 680, y + 60, 21, 500, 'muted', kw, 'right')
            if kw > 0:
                text(c, f'{wo:+.3f}'.replace('-', '−'), 680, y + 150, 60, 760, colr, kw, 'right', glow=6)
            illustration(c, 680, y + 226, ramp(t, 1.0, 0.6), 'illustration', 19, 'right')
        ks = ramp(t, 10.6, 0.6)
        note(c, 'output numbers: the paper’s trained model, App. A.1', 360, 534, ks, 19, 'muted', 'center')
        kf = ramp(t, 17.5, 0.7, e_expo)
        if kf > 0:
            with layer(c, kf):
                panel(c, 10, 556, 700, 140, stroke='y')
                rich(c, 'guess = {f:1.087} × head 1 {c:− 1.244} × head 2', 360, 614, 32, 700, t, 17.6, 0.04, 0.4, align='center')
                text(c, 'one head adds, the other subtracts', 360, 666, 28, 400, 'y', ramp(t, 18.6, 0.6), 'center',
                     kind='italic')

class TwoHeadsSpec(Scene):
    """shorts/twoheads, part 2: the soft spring's spectrum: one head (our fit) loses the peak; our two-head version
    (head 1 all on x(t) x +1.24, head 2 all on x(t-1) x -0.98) gives the exact recipe back."""
    vertical = True
    dur = 12.0
    cues = [(1.4, 'draw'), (3.8, 'pop'), (8.0, 'chime')]

    def __init__(self):
        D = load_json('sdof.json')
        d = D['cases']['k500']
        self.f, self.H, self.Hc = np.array(D['f']), np.array(d['H']), np.array(d['convex']['H'])

    def draw(self, c, t):
        text(c, 'the soft spring · 3.56 Hz', 360, 34, 22, 500, 'y', ramp(t, 0.3, 0.6), 'center', kind='mono', tracking=0.06)
        spectrum_plot(c, 110, 120, 560, 290, self.f,
                      [dict(mag=self.H, color='ink', a=0.6, t0=0.8),
                       dict(mag=self.Hc, color='c', t0=1.4),
                       dict(mag=self.H, color='f', t0=3.8, dash=[12, 8], w=3.4)],
                      t, 0.4, db=True, norm='first', db_floor=-45, yticks=(0, -20, -40), fs=22, ylabel=None,
                      marks=[(SOFT['fn'], None, 'y')], xlabel='frequency (Hz) · gain in dB')
        legend_item(c, 60, 530, 'ink', 'the true spring', ramp(t, 0.8, 0.6), size=24)
        legend_item(c, 60, 575, 'c', 'one head (our best fit): no peak', ramp(t, 1.4, 0.6), size=24)
        legend_item(c, 60, 620, 'f', 'two heads (our version): peak back', ramp(t, 3.8, 0.6), dash=True, size=24)
        sim_label(c, 360, 684, ramp(t, 1.0, 0.6), 19, 'center')

class SensorWindow(Scene):
    """shorts/sensor, part 1: two masses, one sensor or two, three or four steps of history (§3.2's three cases)."""
    vertical = True
    dur = 24.0
    cues = [(3.0, 'draw'), (8.5, 'pop'), (14.0, 'pop'), (19.5, 'pop')]
    CARDS = [('both positions · 3 steps', 'finds both modes', 'f', '✓', 8.5),
             ('first mass only · 3 steps', 'modes lost', 'c', '✗', 14.0),
             ('first mass only · 4 steps', 'both modes back', 'f', '✓', 19.5)]

    def __init__(self):
        d = load_json('twodof.json')
        self.tf, self.x1, self.x2 = np.array(d['tf']), np.array(d['x1f']), np.array(d['x2f'])

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.7)
        tv = (max(t - 0.4, 0) / 12.0) % 6.0              # the simulated response, slowed 12x
        s = 0.92
        d1, d2 = 3.0 * float(np.interp(tv, self.tf, self.x1)), 3.0 * float(np.interp(tv, self.tf, self.x2))
        partial = t >= 14.0
        spring_mass(c, 46, 150, (d1, d2), k, s=s, colors=['y', 'faint' if partial else 'y'], fs=26)
        for j, sx in enumerate((46 + s * (170 + 46 + d1), 46 + s * (170 + 92 + 170 + 46 + d2))):
            if j == 1 and partial:
                text(c, 'no sensor', sx, 78, 21, 600, 'c', k * ramp(t, 14.0, 0.5), 'center', kind='mono')
                continue
            pill(c, sx, 44, 'sensor', 'g', k, size=19, cx=True)
        kn = ramp(t, 3.0, 0.6)
        note(c, 'slow mode + fast mode · slowed 12×', 360, 236, kn, 19, 'muted', 'center')
        note(c, 'motion ' + SIM, 360, 262, kn, 19, 'muted', 'center')
        # what the transformer sees: one token per time step, x2 drops out at 14, a fourth step slides in at 19.5
        kw = ramp(t, 8.5, 0.6)
        if kw > 0:
            text(c, 'what it sees · one token per step', 360, 316, 21, 500, 'ink', kw, 'center', kind='mono')
            k2 = 1 - ramp(t, 14.0, 0.6)
            k4 = ramp(t, 19.5, 0.6, e_io)
            bw, bh, gap = 120, 96, 14
            x0 = lerp(166, 99, k4)
            for j, lab in enumerate(['t−3', 't−2', 't−1', 't']):
                kb = kw * (k4 if j == 0 else ramp(t, 8.5 + 0.1 * (j - 1), 0.45, e_out))
                if kb <= 0:
                    continue
                bx = x0 + (j - 1 + k4) * (bw + gap)
                rrect(c, bx, 336, bw, bh, 12, fill='panel', a=kb, fa=kb * 0.85)
                rrect(c, bx, 336, bw, bh, 12, stroke='g' if k2 < 0.5 else 'line', sw=1.8, a=kb)
                y1 = 336 + bh / 2 + 11 - 20 * k2
                text(c, 'x1', bx + bw / 2, y1, 30, 600, 'g', kb, 'center', kind='mono')
                if k2 > 0:
                    text(c, 'x2', bx + bw / 2, 336 + bh / 2 + 11 + 20, 30, 600, 'y', kb * k2, 'center', kind='mono')
                text(c, lab, bx + bw / 2, 336 + bh + 28, 21, 400, 'muted', kb, 'center', kind='mono')
        for i, (big, small, colr, mark, ti) in enumerate(self.CARDS):
            kk = ramp(t, ti, 0.7, e_expo) * (1 - (ramp(t, self.CARDS[i + 1][4] - 0.4, 0.4) if i < 2 else 0))
            if kk <= 0:
                continue
            with layer(c, kk):
                with xform(c, (1 - kk) * 30, 0):
                    panel(c, 40, 486, 640, 150, stroke=colr)
                    text(c, mark, 80, 584, 60, 700, colr, 1)
                    text(c, big, 160, 546, 28, 600, 'ink', 1)
                    text(c, small, 160, 600, 32, 400, colr, 1, kind='italic')
        note(c, 'the paper’s trained transformer, §3.2', 360, 684, ramp(t, 9.0, 0.6), 19, 'muted', 'center')

class SensorCount(Scene):
    """shorts/sensor, part 2: a rough count (ours): the state is 4 numbers; each sensor adds one number per step."""
    vertical = True
    dur = 17.0
    cues = [(0.4, 'draw'), (6.5, 'pop'), (7.7, 'pop'), (9.2, 'pop'), (12.0, 'chime')]
    ROWS = [('both positions × 3 steps', 6, 2, 'f', '✓', 6.5),
            ('one position × 3 steps', 3, 1, 'c', '✗', 7.7),
            ('one position × 4 steps', 4, 1, 'f', '✓', 9.2)]

    def draw(self, c, t):
        k = ramp(t, 0.4, 0.7)
        text(c, 'the hidden state: 4 numbers', 360, 40, 28, 600, 'ink', k, 'center')
        for j, lab in enumerate(['x₁', 'x₂', 'v₁', 'v₂']):
            kk = ramp(t, 0.8 + 0.15 * j, 0.5, e_out)
            bx = 80 + j * 145
            rrect(c, bx, 66, 125, 78, 12, fill='panel', a=kk, fa=kk * 0.85)
            rrect(c, bx, 66, 125, 78, 12, stroke='v', sw=1.8, a=kk)
            text(c, lab, bx + 62, 118, 32, 600, 'v', kk, 'center', kind='italic')
        kl = ramp(t, 2.6, 0.6)
        text(c, 'positions', 222, 178, 21, 500, 'muted', kl, 'center', kind='mono')
        text(c, 'velocities', 512, 178, 21, 500, 'muted', kl, 'center', kind='mono')
        cell, x0 = 46, 40
        kneed = ramp(t, 4.6, 0.6)
        if kneed > 0:
            X = x0 + 4 * cell - 5                    # beside the squares only, clear of the row labels
            for i in range(3):
                y = 250 + i * 118
                line(c, X, y + 14, X, y + 70, 'v', kneed, 2.4, dash=[8, 7])
            text(c, '4 needed', X, 616, 21, 600, 'v', kneed, 'center', kind='mono')
        for i, (lab, n, per, colr, mark, ti) in enumerate(self.ROWS):
            kr = ramp(t, ti, 0.6)
            if kr <= 0:
                continue
            y = 250 + i * 118
            text(c, lab, x0, y + 4, 24, 600, 'ink', kr)
            for q in range(n):
                kq = ramp(t, ti + 0.3 + 0.12 * q, 0.35, e_out)
                cc = ('g' if q % per == 0 else 'y') if per == 2 else 'g'
                rrect(c, x0 + q * cell, y + 22, cell - 10, cell - 10, 7, fill=cc, a=kq, fa=kq * 0.75)
            text(c, f'{n}', 600, y + 58, 48, 760, colr, kr, 'right')
            text(c, mark, 680, y + 58, 48, 700, colr, kr, 'right')
        kn = ramp(t, 6.8, 0.6)
        text(c, 'each square: one number per step', 360, 652, 20, 500, 'muted', kn, 'center', kind='mono')
        note(c, 'our rough count · results: the paper, §3.2', 360, 686, ramp(t, 1.0, 0.6), 19, 'muted', 'center')

