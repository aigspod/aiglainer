"""Attention can only average: the sign problem (§2.3, §3.1, App. A.1, §3.2 of arXiv:2512.21113v2).
Spring and two-mass data are OUR simulations of the paper's equations (simulate.py -> data/), labelled on screen;
the one-head fit and the two-head construction are ours. Numbers typed from the paper: §3.1 (a1, a2 for k = 2000,
f_n), App. A.1 (W_O), §3.2 (which settings work). Case 2's coefficients (+1.24, -0.98) are our calculation."""
from dynkit import *

STIFF, SOFT = SDOF['k2000'], SDOF['k500']

def _frame(c, x, y, w, h, a, tag=None, colr='muted'):
    panel(c, x, y, w, h, a)
    if tag:                                  # mono tag that keeps unit case (N/m, Hz)
        text(c, tag, x + 28, y + 42, 17, 500, colr, a, kind='mono', tracking=0.08)

class ColdOpen(Scene):
    dur = 21.0
    fade_in = 0.3
    cues = [(0.4, 'whoosh_soft'), (9.5, 'pop'), (14.0, 'pop')]

    def __init__(self):
        d = load_json('sdof.json')['cases']['k500']
        self.tf, self.xf = np.array(d['tf']), np.array(d['xf'])
        self.t, self.x = np.array(d['t']), np.array(d['x'])

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8)
        # the doodle moves slowly (an illustration of the motion); the trace on the right is the simulated response
        disp = 46 * math.exp(-0.07 * max(t - 0.6, 0)) * math.cos(2 * math.pi * 0.7 * max(t - 0.6, 0)) if t > 0.6 else 46
        spring_mass(c, 190, 470, (disp,), k, s=1.25, rest=True, arrow_on=0)
        illustration(c, 190, 610, k, 'illustration (slowed)')
        m = self.tf <= 4.0
        ms = self.t <= 4.0
        trace_plot(c, 900, 360, 860, 210, [dict(x=self.tf[m], y=self.xf[m], color='y', w=2.6, t0=1.0, dur=3.0),
                                          dict(x=self.t[ms], y=self.x[ms], color='g', dots=True, line=False, r=4.5, t0=5.0, dur=1.6)],
                   t, 0.8, xr=(0, 4), yr=(-11, 11), xticks=(0, 1, 2, 3, 4), yticks=(-10, 0, 10), xlabel='time (s)',
                   ylabel='position (mm)', fs=19)
        sim_label(c, 1760, 660, ramp(t, 1.5, 0.6), 15, 'right', extra='k = 500 N/m')
        ke = ramp(t, 5.0, 0.8)
        if ke > 0:
            tex(c, 'ar2', 1330, 720, 46, ke)
        for i, (big, small, colr, mark, ti) in enumerate(
                (('stiff spring', 'one attention head learns its recipe', 'f', '✓', 9.5),
                 ('soft spring', 'the same head can’t', 'c', '✗', 14.0))):
            kk = ramp(t, ti, 0.8, e_expo)
            if kk <= 0:
                continue
            x = 170 + i * 820
            with layer(c, kk):
                with xform(c, 0, (1 - kk) * 24):
                    panel(c, x, 800, 760, 120, stroke=colr)
                    text(c, mark, x + 36, 880, 54, 700, colr, 1)
                    text(c, big, x + 110, 852, 34, 400, colr, 1, kind='italic')
                    text(c, small, x + 110, 894, 24, 500, 'ink', 1)
        caption(c, t, 'Not for lack of data. Because of a {c:minus sign}.', 17.0, None, y=1000, size=34)

class Title(TitleCard):
    TITLE = 'Attention can only *average*'
    STICKY = ['the sign', 'problem']

class Recipe(Scene):
    dur = 27.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (4.5, 'draw'), (12.0, 'pop'), (18.0, 'pop')]

    def __init__(self):
        d = load_json('sdof.json')['cases']['k2000']
        self.tf, self.xf = np.array(d['tf']), np.array(d['xf'])
        self.t, self.x = np.array(d['t']), np.array(d['x'])

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the recipe', 'A spring is a two-step *recipe*',
            sub='§3.1: m = 1 kg, c = 0.5 Ns/m, sampled 25 times a second; only the position is observed')
        m, ms = self.tf <= 1.0, self.t <= 1.0
        ax = trace_plot(c, 190, 380, 760, 170, [dict(x=self.tf[m], y=self.xf[m], color='y', w=2.2, a=0.45, t0=0.5, dur=1.0),
                                               dict(x=self.t[ms], y=self.x[ms], color='g', dots=True, line=False, r=6, t0=0.7, dur=1.4)],
                        t, 0.3, xr=(0, 1.0), yr=(-11, 11), xticks=(0, 0.5, 1.0), yticks=(-10, 0, 10), fs=19,
                        xlabel='time (s)', ylabel='position (mm)')
        sim_label(c, 950, 360, ramp(t, 0.8, 0.6), 15, 'right', extra='k = 2000 N/m')
        # the last two samples feed the next one
        kh = ramp(t, 4.5, 0.6)
        if kh > 0:
            for j, colr in ((19, 'y'), (20, 'y'), (21, 'f')):
                X, Y = ax.px(self.t[j], self.x[j])
                circle(c, X, Y, 12, stroke=colr, sw=3, a=kh, glow=6)
            X0, Y0 = ax.px(self.t[20], self.x[20])
            X1, Y1 = ax.px(self.t[21], self.x[21])
            arrow(c, X0 + 8, Y0, X1 - 10, Y1, 'f', kh, 2.4, 10, prog=ramp(t, 4.8, 0.6, e_io))
        ke = ramp(t, 5.0, 0.8)
        if ke > 0:
            tex(c, 'ar2', 1400, 470, 52, ke)
            note(c, 'an autoregressive model of order 2: exact for a free spring', 1400, 560, ke, 17, 'muted', 'center')
        for i, (tag, vals, src, ti) in enumerate(
                (('stiff spring · k = 2000 N/m · 7.12 Hz', (STIFF['a1'], STIFF['a2']), ('the paper, §3.1',), 12.0),
                 ('soft spring · k = 500 N/m · 3.56 Hz', (SOFT['a1'], SOFT['a2']), (CALC, 'the paper gives the signs'), 18.0))):
            kk = ramp(t, ti, 0.7, e_expo)
            if kk <= 0:
                continue
            x = 170 + i * 820
            with layer(c, kk):
                _frame(c, x, 645, 760, 310, 1, tag, 'ink')
                signed_bars(c, x + 120, 722, 360, 196, vals, t, ti, labels=['a₁', 'a₂'], vmax=1.45,
                            fmt='{:+.4f}' if i == 0 else '{:+.2f}', fs=22, zero_label=False)
                verdict = ('both negative', 'c') if i == 0 else ('one plus, one minus', 'y')
                kv = ramp(t, ti + 1.2, 0.6)
                text(c, verdict[0], x + 500, 800, 30, 400, verdict[1], kv, kind='italic')
                for j, s_ in enumerate(src):
                    note(c, s_, x + 500, 840 + j * 26, kv, 15)

class OneHead(Scene):
    dur = 28.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (4.5, 'draw'), (17.0, 'pop'), (22.0, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '02', 'attention as a recipe', 'One head can only *average*',
            sub='§2.3, §3.1: one attention head, nothing else (no residual, no feed-forward; positional encoding only adds a constant)')
        k = ramp(t, 0.8, 0.7)
        if k > 0:
            _frame(c, 150, 380, 760, 380, k, 'the head’s weights on the last two samples', 'muted')
            illustration(c, 882, 422, k, align='right')
        alpha = 0.3 + 0.45 * (0.5 - 0.5 * math.cos(2 * math.pi * max(t - 6.0, 0) / 7.0))
        convex_mix(c, 250, 540, 560, alpha, t, 1.0, k, color='f', fs=26)
        kr = ramp(t, 10.0, 0.6) * (1 - ramp(t, 16.0, 0.6))
        if kr > 0:
            rrect(c, 300, 684, 460, 44, 10, stroke='f', sw=2, a=kr, glow=6)
        ko = ramp(t, 17.0, 0.8)
        if ko > 0:
            tex(c, 'onehead', 1400, 470, 50, ko)
            note(c, 'wₒ: one shared output number', 1400, 545, ko, 17, 'g', 'center')
        kb = ramp(t, 21.5, 0.8)
        if kb > 0:
            tex(c, 'betas', 1400, 640, 50, kb)
        kp = ramp(t, 24.0, 0.8, e_expo)
        if kp > 0:
            with layer(c, kp):
                panel(c, 1030, 720, 740, 130, stroke='y')
                rich(c, '{y:a₁} and {y:a₂} always share the sign of {g:wₒ}', 1400, 798, 32, 700, t, 24.2, 0.03, 0.4,
                     align='center')

class Plane(Scene):
    dur = 26.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (5.5, 'sweep'), (9.5, 'pop'), (15.0, 'pop'), (20.5, 'draw')]
    BEST = (0.613, 0.0)          # our best fixed-alpha one-head fit for k = 500 (simulate.py): alpha = 1, w_o = 0.613

    def draw(self, c, t):
        hdr(self, c, t, '02', 'what one head can reach', 'Half the plane is out of *reach*')
        cx, cy, size = 600, 650, 500
        ax = coef_plane(c, cx, cy, size, t, 0.6, reach=False, fs=19, ticks=(-1, 1),
                        xlabel='a₁  (coefficient on x(t))', ylabel='a₂  (coefficient on x(t−1))')
        kr = ramp(t, 5.5, 0.8)
        if kr > 0:                               # the two same-sign quadrants (coef_plane's shading, timed to the line)
            x0, y0, q = cx - size / 2, cy - size / 2, size / 2
            rrect(c, cx, y0, q, q, 0, fill='f', a=kr, fa=kr * 0.13)
            rrect(c, x0, cy, q, q, 0, fill='f', a=kr, fa=kr * 0.13)
            for xx, yy, s, colr in ((cx + q / 2, y0 + 34, 'signs agree', 'f'), (cx - q / 2, cy + q - 16, 'signs agree', 'f'),
                                    (cx + q / 2, cy + q - 16, 'out of reach', 'c'), (cx - q / 2, y0 + 34, 'out of reach', 'c')):
                text(c, s, xx, yy, 18, 600, colr, kr, 'center', kind='mono')
        pts = [(STIFF['a1'], STIFF['a2'], 'g', 'stiff', 9.5, -1), (SOFT['a1'], SOFT['a2'], 'y', 'soft', 15.0, 1)]
        for a1, a2, colr, lab, ti, side in pts:
            kk = ramp(t, ti, 0.5, e_back)
            if kk <= 0:
                continue
            X, Y = ax.px(a1, a2)
            circle(c, X, Y, 13 * min(kk, 1.2), fill=colr, a=min(kk, 1), glow=10)
            text(c, lab, X + side * 22, Y + 8, 22, 700, colr, min(kk, 1), 'right' if side < 0 else 'left')
        kb = ramp(t, 20.5, 0.9)
        if kb > 0:
            X0, Y0 = ax.px(SOFT['a1'], SOFT['a2'])
            X1, Y1 = ax.px(*self.BEST)
            arrow(c, X0, Y0 - 14, X1 + 6, Y1 + 12, 'v', kb, 2.4, 12, prog=ramp(t, 20.5, 0.9, e_io), dash=[8, 6])
            circle(c, X1, Y1, 10, stroke='v', sw=2.6, a=kb)
        cards = [('stiff spring', '({:+.2f}, {:+.2f})'.format(STIFF['a1'], STIFF['a2']), 'inside: one head matches it, with wₒ < 0', 'g', 9.5, 'the paper, §3.1'),
                 ('soft spring', '({:+.2f}, {:+.2f})'.format(SOFT['a1'], SOFT['a2']), 'outside: no single head can get there', 'y', 15.0, CALC),
                 ('best fixed-weight head (our fit)', '(+0.61, 0)', 'drop the older sample: no ringing left', 'v', 20.5, 'our fit: one fixed weight, no positional encoding')]
        for i, (big, nums, body, colr, ti, src) in enumerate(cards):
            kk = ramp(t, ti + 0.3, 0.8, e_expo)
            if kk <= 0:
                continue
            yy = 380 + i * 190
            with layer(c, kk):
                with xform(c, (1 - kk) * 30, 0):
                    panel(c, 1000, yy, 790, 165)
                    line(c, 1036, yy + 1, 1156, yy + 1, colr, 1, 4, cap='butt')
                    text(c, big, 1036, yy + 58, 32, 400, colr, 1, kind='italic')
                    text(c, nums.replace('-', '−'), 1754, yy + 58, 26, 600, colr, 1, 'right', kind='mono')
                    text(c, body, 1036, yy + 104, 24, 500, 'ink', 1)
                    note(c, src, 1036, yy + 140, 1, 15)

class Springs(Scene):
    dur = 31.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (6.0, 'draw'), (10.5, 'pop'), (16.0, 'draw'), (22.0, 'pop')]

    def __init__(self):
        D = load_json('sdof.json')
        self.f = np.array(D['f'])
        self.cases = []
        for key in ('k2000', 'k500'):
            d = D['cases'][key]
            self.cases.append(dict(tf=np.array(d['tf']), xf=np.array(d['xf']), t=np.array(d['t']),
                                   one=np.array(d['convex']['onestep']), H=np.array(d['H']), Hc=np.array(d['convex']['H'])))

    def draw(self, c, t):
        hdr(self, c, t, '03', 'two springs', 'One rings, one goes *flat*',
            sub='true response vs. our best fixed-weight one-head fit (not the paper’s trained model)')
        spec = [('stiff spring · 7.12 Hz', 'g', 7.12, 6.0, 10.5), ('soft spring · 3.56 Hz', 'y', 3.56, 16.0, 22.0)]
        for i, (tag, colr, fn, tt, ts) in enumerate(spec):
            d = self.cases[i]
            x = 150 + i * 840
            k = ramp(t, 0.6 + i * 0.3, 0.7)
            if k <= 0:
                continue
            text(c, tag, x + 30, 370, 18, 500, colr, k, kind='mono', tracking=0.1)
            m, ms = d['tf'] <= 1.6, d['t'] <= 1.6
            trace_plot(c, x + 100, 420, 600, 170,
                       [dict(x=d['tf'][m], y=d['xf'][m], color='ink', w=2.2, a=0.55, t0=0.9 + i * 0.3, dur=1.4, label='true', label_xy=(1.62, 7)),
                        dict(x=d['t'][ms], y=d['one'][ms], color='f' if i == 0 else 'c', w=2.6, dots=True, r=4.5, t0=tt, dur=2.0,
                             label='one head', label_xy=(1.62, -5))],
                       t, 0.6 + i * 0.3, xr=(0, 1.6), yr=(-11, 11), xticks=(0, 0.5, 1.0, 1.5), yticks=(-10, 0, 10), fs=18,
                       xlabel='time (s)', label_room=160)
            spectrum_plot(c, x + 100, 700, 600, 190, self.f,
                          [dict(mag=d['H'], color='ink', a=0.55, t0=ts - 0.4),
                           dict(mag=d['Hc'], color='f' if i == 0 else 'c', label=None, t0=ts, dash=[10, 6] if i == 0 else None)],
                          t, ts - 0.6, db=True, norm='first', db_floor=-45, yticks=(0, -20, -40), fs=18,
                          marks=[(fn, f'{fn:g} Hz', colr)], ylabel=None, xlabel='frequency (Hz) · gain in dB')
        text(c, 'the curves overlap', 270, 770, 24, 600, 'f', ramp(t, 11.6, 0.7), kind='italic')
        text(c, 'no resonance peak', 1400, 770, 24, 600, 'c', ramp(t, 22.6, 0.7), kind='italic')
        kp = ramp(t, 25.5, 0.6)                    # the paper's own result, not our fit
        note(c, 'the paper, Fig. 2b:', 1400, 800, kp, 15, 'c')
        note(c, 'over-smoothed, no resonance peak', 1400, 822, kp, 15, 'c')
        sim_label(c, W / 2, 985, ramp(t, 1.0, 0.6), 16, 'center', extra='one-step guesses from the true history')

class TwoHeads(Scene):
    dur = 45.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (3.5, 'draw'), (9.0, 'pop'), (15.0, 'pop'), (22.0, 'draw')]

    def draw(self, c, t):
        hdr(self, c, t, '03', 'the fix', 'A second head brings the *minus*',
            sub='App. A.1: a two-head attention-only model reproduces the soft spring')
        # each head still averages
        for i, (colr, a0, ph) in enumerate((('f', 0.62, 0.0), ('c', 0.35, 2.0))):
            k = ramp(t, 0.8 + i * 0.4, 0.7)
            if k <= 0:
                continue
            yy = 360 + i * 290
            _frame(c, 150, yy, 640, 270, k, f'head {i + 1}', colr)
            text(c, '× its own output weight', 762, yy + 42, 20, 600, colr, k * ramp(t, 9.0, 0.6), 'right')
            alpha = a0 + 0.12 * math.sin(2 * math.pi * max(t - 4, 0) / 6.0 + ph)     # illustrative weights
            ko = ramp(t, 22.4 + i, 0.8, e_io)        # then our construction: head 1 all on x(t), head 2 all on x(t-1)
            alpha += ((1.0 if i == 0 else 0.0) - alpha) * ko
            convex_mix(c, 270, yy + 100, 400, alpha, t, 0.8 + i * 0.4, k, color=colr, fs=20)
            illustration(c, 762, yy + 256, k * (1 - ko), align='right', size=15)
        note(c, 'one-hot is the softmax limit (real weights stay > 0)', 150, 950, ramp(t, 23.0, 0.6), 15, 'y')
        kt = ramp(t, 9.0, 0.8)
        if kt > 0:
            tex(c, 'twohead', 1320, 410, 40, kt)
        kw = ramp(t, 15.0, 0.6)
        if kw > 0:
            _frame(c, 850, 480, 440, 440, kw, 'learned output weights', 'ink')
            signed_bars(c, 910, 540, 340, 300, TWO_HEAD_WO, t, 15.0, labels=['head 1', 'head 2'], vmax=1.5, fmt='{:+.3f}',
                        fs=22, zero_label=False)
            note(c, 'the paper, App. A.1', 1070, 895, kw, 15, 'muted', 'center')
        kc = ramp(t, 22.0, 0.8, e_expo)
        if kc > 0:
            with layer(c, kc):
                _frame(c, 1330, 480, 460, 440, 1, 'our construction', 'y')
                rows = [('head 1: all on x(t)', '× +1.24', 'f', 22.4), ('head 2: all on x(t−1)', '× −0.98', 'c', 23.4)]
                for j, (s1, s2, colr, ti) in enumerate(rows):
                    kk = ramp(t, ti, 0.6)
                    text(c, s1, 1362, 575 + j * 56, 24, 500, 'ink', kk)
                    text(c, s2, 1760, 575 + j * 56, 24, 700, colr, kk, 'right', kind='mono')
                signed_bars(c, 1420, 680, 300, 190, (SOFT['a1'], SOFT['a2']), t, 29.0, labels=['a₁', 'a₂'], vmax=1.5,
                            fs=20, zero_label=False)
                note(c, CALC, 1560, 895, ramp(t, 29.0, 0.6), 15, 'muted', 'center')
        caption(c, t, 'Each head still {f:averages}. The {c:minus} comes from how the heads are combined.', 33.0, 36.6, y=985, size=30)
        caption(c, t, 'A {y:boundary case}: one head, attention only. Real transformers have residual paths and many heads.',
                37.0, None, y=985, size=30)
        note(c, 'the paper, §3.1 and App. A.1', W / 2, 1024, ramp(t, 37.4, 0.6), 15, 'muted', 'center')

class TwoMasses(Scene):
    dur = 29.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (8.0, 'pop'), (14.0, 'pop'), (20.5, 'pop')]
    CARDS = [('both positions · 3 steps', 'finds both modes', 'f', '✓', 8.0),
             ('first mass only · 3 steps', 'modes lost', 'c', '✗', 14.0),
             ('first mass only · 4 steps', 'both modes back', 'f', '✓', 20.5)]

    def __init__(self):
        d = load_json('twodof.json')
        self.tf, self.x1, self.x2 = np.array(d['tf']), np.array(d['x1f']), np.array(d['x2f'])

    def draw(self, c, t):
        hdr(self, c, t, '04', 'two masses', 'Time stands in for a *sensor*',
            sub='§3.2: m₁ = m₂ = 1 kg, k₁ = 1000, k₂ = 1500 N/m; positions only')
        k = ramp(t, 0.5, 0.8)
        # doodle driven by the simulated response, slowed 12x so the motion is visible
        tv = (max(t - 0.6, 0) / 12.0) % 6.0
        d1, d2 = (3.4 * float(np.interp(tv, self.tf, self.x1)), 3.4 * float(np.interp(tv, self.tf, self.x2)))
        partial = t >= 14.0
        cols = ['y', 'faint' if partial else 'y']
        spring_mass(c, 180, 520, (d1, d2), k, s=1.1, colors=cols)
        # the sensor(s)
        s1x = 180 + 1.1 * (170 + 46 + d1)
        s2x = 180 + 1.1 * (170 + 92 + 170 + 46 + d2)
        for j, sx in enumerate((s1x, s2x)):
            if j == 1 and partial:
                kq = ramp(t, 14.0, 0.5)
                text(c, 'no sensor', sx, 414, 20, 600, 'c', k * kq, 'center', kind='mono')
                continue
            pill(c, sx, 390, 'sensor', 'g', k, size=15, cx=True)
        kn = ramp(t, 4.0, 0.6)
        note(c, 'slow mode + fast mode in each position', 180, 645, kn, 17)
        note(c, 'motion ' + SIM + ', slowed 12×', 180, 674, kn, 15)
        # the window of past steps
        kw = ramp(t, 8.0, 0.6)
        if kw > 0:
            # one token per time step (§3.2: vector-valued x_t); full observation puts (x1, x2) in each token,
            # partial observation leaves x1 alone, and a fourth step slides in from the left at 20.5
            text(c, 'what the transformer sees · one token per step', 180, 730, 20, 500, 'muted', kw, kind='mono')
            k2 = 1 - ramp(t, 14.0, 0.6)                  # x2 fades out of every token
            k4 = ramp(t, 20.5, 0.6, e_io)                # the fourth token
            bw, bh, gap = 110, 84, 12
            for j, lab in enumerate(['t−3', 't−2', 't−1', 't']):
                kb = kw * (k4 if j == 0 else ramp(t, 8.0 + 0.1 * (j - 1), 0.45, e_out))
                if kb <= 0:
                    continue
                bx = 180 + (j - 1 + k4) * (bw + gap)
                rrect(c, bx, 760, bw, bh, 10, fill='panel', a=kb, fa=kb * 0.85)
                rrect(c, bx, 760, bw, bh, 10, stroke='g' if k2 < 0.5 else 'line', sw=1.6, a=kb)
                y1 = 760 + bh / 2 + 9 - 18 * k2               # x1 sits on top while x2 is there, centred after
                text(c, 'x1', bx + bw / 2, y1, 24, 600, 'g', kb, 'center', kind='mono')
                if k2 > 0:
                    text(c, 'x2', bx + bw / 2, 760 + bh / 2 + 9 + 18, 24, 600, 'y', kb * k2, 'center', kind='mono')
                text(c, lab, bx + bw / 2, 760 + bh + 27, 17, 400, 'muted', kb, 'center', kind='mono')
        for i, (big, small, colr, mark, ti) in enumerate(self.CARDS):
            kk = ramp(t, ti, 0.8, e_expo)
            if kk <= 0:
                continue
            yy = 370 + i * 180
            with layer(c, kk):
                with xform(c, (1 - kk) * 30, 0):
                    panel(c, 1080, yy, 710, 150, stroke=colr if i == 2 and t > 25.0 else 'line')
                    text(c, mark, 1116, yy + 98, 56, 700, colr, 1)
                    text(c, big, 1196, yy + 64, 28, 600, 'ink', 1)
                    text(c, small, 1196, yy + 112, 28, 400, colr, 1, kind='italic')
        note(c, 'the paper’s trained transformer, §3.2', 1790, 930, ramp(t, 8.5, 0.6), 15, 'muted', 'right')

class Delay(Scene):
    dur = 30.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (6.0, 'draw'), (11.5, 'draw'), (19.0, 'pop')]

    def __init__(self):
        d = load_json('twodof.json')
        self.f = np.array(d['ar_f'])
        self.p3, self.p4 = np.array(d['ar_x1']['p3']['H']), np.array(d['ar_x1']['p4']['H'])

    def draw(self, c, t):
        hdr(self, c, t, '04', 'a linear check', 'Why *four* steps?',
            sub='our least-squares recipes on the first mass alone, not the paper’s transformer')
        fo = TWODOF['f_ours']
        for i, (tag, H, colr, ts, verdict, vc) in enumerate(
                (('3 past values', self.p3, 'c', 6.0, 'no sharp peaks: both modes missed', 'c'),
                 ('4 past values', self.p4, 'f', 11.5, 'both modes, fit to rounding error', 'f'))):
            x = 150 + i * 840
            k = ramp(t, 0.8 + i * 0.3, 0.7)
            if k <= 0:
                continue
            kicker(c, tag, x + 30, 380, k, colr, 20)
            spectrum_plot(c, x + 90, 450, 660, 300, self.f, [dict(mag=H, color=colr, t0=ts)], t, 0.8 + i * 0.3,
                          db=True, norm='peak', db_floor=-45, yticks=(0, -20, -40), fs=18, ylabel=None,
                          marks=[(fo[0], f'{fo[0]:g} Hz', 'muted'), (fo[1], f'{fo[1]:g} Hz', 'muted')],
                          xlabel='frequency (Hz) · gain in dB')
            text(c, verdict, x + 90, 850, 26, 400, vc, ramp(t, ts + 1.4, 0.6), kind='italic')
        sim_label(c, 150, 905, ramp(t, 1.0, 0.6), 15, extra='dashed lines: the modes of the stated parameters')
        kn = ramp(t, 19.0, 0.8, e_expo)
        if kn > 0:
            with layer(c, kn):
                panel(c, 150, 926, W - 300, 80, stroke='y')
                rich(c, 'An honest note: the stated parameters give {y:3.26} and {y:9.52} Hz; the paper reports {y:4.1} and {y:9.5} Hz.',
                     W / 2, 976, 28, 1560, t, 19.2, 0.025, 0.4, align='center')

class Discussion(Scene):
    dur = 23.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (12.0, 'chime')]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('Real models have many heads. How would you check that a trained model kept the {y:resonance}, rather than averaging it away?', 3.0),
                              ('A climate emulator steps forward from today’s state. Which {y:missing variables} could a longer history stand in for?', 12.0)],
                       size=36)
        extrap_label(c, W - MX - 36, 330 + 250 + 196, ramp(t, 12.3, 0.6), 18, 'right')

class End(EndCard):
    TAKE = 'One attention-only head can only {y:average}. To ring, it needs a {c:minus sign} from somewhere else, like a second head, and enough {g:history} to see the whole state.'
    STATS = [('+1.24 · −0.98', 'the soft spring’s recipe (our calculation)', 'y'),
             ('1.087 · −1.244', 'two-head output weights (App. A.1)', 'f'),
             ('4 steps', 'one sensor, two masses: 3 fail, 4 work (§3.2)', 'g')]
    NEXT = 'journal club · nov 11'
