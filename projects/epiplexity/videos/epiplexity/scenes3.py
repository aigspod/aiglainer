"""Paradox 3 (induction, Fig. 5; emergence, Fig. 6), real data (Fig. 8a-c), the measures side by side, limits, questions
and the end card (arXiv:2601.03220v2). Accuracy notes from projects/epiplexity/AGENTS.md are shown on screen."""
from epikit import *

INFERNO = ['#8a62c8', '#a8418e', '#d0497a', '#e8605e', '#f5853f', '#fcc229']     # Fig. 5's h = 0..5, lifted for the dark ground

# ======================================================================= INDUCTION
class Induction(Scene):
    """§5.3, §5.3.1: Sutskever's murder mystery; hard induction (rule 30, 4 steps, n = 32, first h bits hidden), Fig. 5b."""
    dur = 36.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (6.5, 'pop'), (15.5, 'draw'), (22.5, 'draw'), (29.0, 'pop')]

    def __init__(self):
        self.d = tdata('fig5_induction.json')['fig5b_hard']
        z = np.random.default_rng(17).integers(0, 2, 32)
        self.rows = eca(30, 32, 5, init=z)               # Z, then 4 steps of rule 30: f(Z) is the last row
        self.h = 4

    def draw(self, c, t):
        hdr(self, c, t, '05', 'paradox three', 'The reader works *harder* than the author',
            sub='§5.3: likelihood is minimized by the true distribution, so (the view goes) a model can only match its generator')
        tex(c, 'mle', W / 2, 372, 36, window(t, 1.5, 15.0, 0.8, 0.6))
        # the murder mystery (two lanes)
        km = window(t, 6.5, 15.0, 0.7, 0.6)
        if km > 0:
            for i, (who, steps, colr) in enumerate((('the author', ['picks the murderer', 'writes the clues'], 'f'),
                                                   ('the reader', ['reads the clues', 'deduces the murderer'], 'y'))):
                k = ramp(t, 6.8 + i * 2.5, 0.7) * km
                y = 440 + i * 190
                text(c, who, MX, y + 44, 34, 400, colr, k, kind='italic')
                for j, s_ in enumerate(steps):
                    x = 480 + j * 600
                    rrect(c, x, y, 470, 76, 14, fill='panel2', stroke=colr, sw=1.6, a=k)
                    text(c, s_, x + 235, y + 48, 26, 500, 'ink', k, 'center')
                    if j == 0:
                        arrow(c, x + 486, y + 38, x + 584, y + 38, colr, k, 3, 14, prog=ramp(t, 7.2 + i * 2.5, 0.6, e_io))
            text(c, '“If the model can predict [the name] then it must have figured out [who did it]”  (Ilya Sutskever, 2019)',
                 W / 2, 860, 22, 400, 'muted', km, 'center', kind='italic')
        # the paper's version (Fig. 5a), computed exactly
        kz = ramp(t, 15.5, 0.7)
        if kz > 0:
            cell = 15
            x0, y0 = MX, 400
            text(c, 'Z: random bits', x0, y0 - 14, 18, 500, 'ink', kz, kind='mono')
            z = self.rows[0]
            for j in range(32):
                hid = j < self.h
                rrect(c, x0 + j * cell, y0, cell * 0.82, cell * 0.82, 3, fill='faint' if hid else ('y' if z[j] else 'faint'),
                      fa=kz * (0.9 if hid else (1 if z[j] else 0.45)))
                if hid:
                    text(c, '?', x0 + j * cell + cell * 0.41, y0 + cell * 0.72, 13, 700, 'r', kz, 'center', kind='mono')
            note(c, f'the first h = {self.h} are hidden', x0, y0 + 40, kz, 16, 'r')
            draw_eca(c, self.rows, x0, y0 + 70, 32 * cell, color=FIG3_COLORS['30'], a=kz, bg_a=0.08)
            text(c, 'rule 30, 4 steps', x0 + 32 * cell + 16, y0 + 120, 17, 500, FIG3_COLORS['30'], kz, kind='mono')
            text(c, 'f(Z): to predict', x0, y0 + 70 + 5 * cell + 36, 18, 500, 'ink', kz, kind='mono')
            note(c, 'the model sees the visible bits, then predicts f(Z)', x0, y0 + 70 + 5 * cell + 66, kz, 16)
            tag(c, EXACT + ' · after Fig. 5a', x0, y0 + 70 + 5 * cell + 96, kz)
        # Fig. 5b: loss vs compute
        kc = ramp(t, 22.5, 0.8)
        if kc > 0:
            ax = LogAxes(870, 400, 500, 420, (13.7, 16.3), (-0.4, 1.6), ylog=True)
            ax.draw(c, kc, (14, 15, 16), (1, 10), fs=18)
            text(c, 'train loss (bits, log)', 870, 382, 18, 500, 'muted', kc, kind='mono')
            text(c, 'compute (FLOPs)', 1370, 885, 17, 500, 'muted', kc, 'right', kind='mono')
            c.save()
            c.clipRect(skia.Rect.MakeXYWH(870, 400, 500, 420))
            for h in range(6):
                d = self.d['loss']['curves'][f'h={h}']
                colr = INFERNO[h]
                if h > 0:
                    lv = d.get('dashed_level', h)
                    _, Y = ax.px(1e14, lv)
                    line(c, 870, float(Y), 1370, float(Y), colr, kc * 0.5, 1.4, dash=[6, 6])
                curve_reveal(c, ax, d['x'], np.maximum(np.array(d['y']), 10 ** -0.39), colr, t, 22.8 + h * 0.35, 2.0, w=2.6)
            c.restore()
            for h in range(1, 6):
                _, Y = ax.px(1e14, h)
                text(c, f'h={h}', 1380, float(Y) + 6, 16, 500, INFERNO[h], kc, kind='mono')
            note(c, 'dashed: h bits, where each loss settles', 870, 925, kc, 15)
        # Fig. 5b: measured epiplexity vs h
        ke = ramp(t, 29.0, 0.8)
        if ke > 0:
            e = self.d['epiplexity']
            x0, yb, hh = 1500, 820, 400
            text(c, 'epiplexity (×10⁶ bits)', x0, 382, 19, 500, 'ink', ke)
            line(c, x0, yb, x0 + 300, yb, 'muted', ke, 1.6)
            for i, (h, v) in enumerate(zip(e['h'], e['value'])):
                kk = ramp(t, 29.2 + i * 0.25, 0.8, e_expo) * ke
                bh = hh * v / 6e6 * kk
                rrect(c, x0 + 10 + i * 48, yb - bh, 38, bh, 4, fill=INFERNO[h], fa=ke * 0.9)
                text(c, str(h), x0 + 29 + i * 48, yb + 28, 17, 500, 'muted', ke, 'center', kind='mono')
                text(c, f'{v / 1e6:.1f}', x0 + 29 + i * 48, yb - bh - 10, 15, 600, INFERNO[h], kk, 'center', kind='mono')
            text(c, 'hidden bits h', x0 + 150, yb + 60, 16, 500, 'muted', ke, 'center', kind='mono')
        src(c, 'Fig. 5b', W - MX, 975, kc, 'right')

# ======================================================================= EMERGENCE
class Emergence(Scene):
    """§5.3.2: the Game of Life (a Gosper glider gun, simulated exactly); Fig. 6: rule 54, non-looped vs looped."""
    dur = 31.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (7.0, 'pop'), (15.0, 'draw'), (22.5, 'drop')]
    GPS = 7.0                     # Life generations per authored second

    def __init__(self):
        board = np.zeros((150, 200), np.uint8)
        board = place(board, GOSPER, 3, 3)
        n = int(self.dur * self.GPS) + 2
        self.gens = life_run(board, n)
        self.f6 = tdata('fig6_emergence.json')['panels']['epiplexity']['frontier']

    def draw(self, c, t):
        hdr(self, c, t, '05', 'emergence', 'Simple rules, *rich* structure',
            sub='§5.3.2: an unbounded observer simulates; a bounded one must learn the “species” and how they collide')
        kb = ramp(t, 0.6, 0.8)
        if kb > 0:
            g = self.gens[int(clamp((t - 0.6) * self.GPS, 0, len(self.gens) - 1))]
            win = g[0:40, 0:64]
            draw_eca(c, win, MX, 380, 840, color='y', a=kb, bg_a=0.05, gap=0.14)
            tag(c, 'the Game of Life, ' + EXACT + ' (a glider gun)', MX, 940, kb)
        # species labels
        kl = ramp(t, 7.0, 0.6)
        if kl > 0:
            cs = 840 / 64
            rrect(c, MX + 2 * cs, 380 + 2 * cs, 37 * cs, 10 * cs, 12, stroke='x', sw=2, a=kl)
            text(c, 'a gun', MX + 2 * cs, 380 + 12 * cs + 30, 22, 500, 'x', kl, kind='mono')
            text(c, 'gliders', MX + 690, 575, 22, 500, 'x', kl, kind='mono')
            hand_arrow(c, MX + 700, 590, MX + 600, 640, 'x', kl, ramp(t, 7.5, 0.5))
        kn = ramp(t, 11.0, 0.6)
        note(c, 'not proven for Life (Def. 14); the paper tests the idea on rule 54', MX, 972, kn, 16, 'r')
        # Fig. 6: epiplexity frontier
        kc = ramp(t, 15.0, 0.8)
        if kc > 0:
            ax = LogAxes(1100, 480, 660, 360, (13.4, 16.8), (0, 1.6))
            ax.draw(c, kc, (14, 15, 16), (0, 0.5, 1.0, 1.5), yfmt=lambda v: f'{v:g}', fs=18)
            text(c, 'epiplexity Sₜ (×10⁷ bits)', 1100, 392, 21, 500, 'ink', kc)
            text(c, 'compute (FLOPs)', 1760, 905, 17, 500, 'muted', kc, 'right', kind='mono')
            xs, ys, model = np.array(self.f6['x']), np.array(self.f6['y']) / 1e7, self.f6['model']
            nl = [i for i, m in enumerate(model) if m == 'non-looped']
            lo = [i for i, m in enumerate(model) if m == 'looped']
            curve_reveal(c, ax, xs[nl], ys[nl], LOOP_COLORS['non-looped'], t, 15.3, 2.4, w=3, dots=True, r=6)
            kj = ramp(t, 22.5, 0.5)
            if kj > 0:
                pts = ax.pts(xs[[nl[-1], lo[0]]], ys[[nl[-1], lo[0]]])
                draw_poly(c, pts, LOOP_COLORS['looped'], kj * 0.8, 2.5, dash=[7, 6], prog=kj)
            curve_reveal(c, ax, xs[lo], ys[lo], LOOP_COLORS['looped'], t, 22.9, 1.8, w=3, dots=True, r=6)
            kp = ramp(t, 18.0, 0.6)
            X, Y = ax.px(7.052e14, 1.456)
            circle(c, 1110, 420, 6, fill=LOOP_COLORS['non-looped'], a=kp)
            text(c, 'non-looped: predicts the far row directly', 1126, 426, 17, 600, LOOP_COLORS['non-looped'], kp, kind='mono')
            text(c, '1.46 × 10⁷', float(X) + 12, float(Y) + 2, 17, 600, LOOP_COLORS['non-looped'], kp)
            kq = ramp(t, 23.5, 0.6)
            circle(c, 1110, 450, 6, fill=LOOP_COLORS['looped'], a=kq)
            text(c, 'looped: unrolls the rule step by step', 1126, 456, 17, 600, LOOP_COLORS['looped'], kq, kind='mono')
            src(c, 'Fig. 6', 1760, 945, kc, 'right')

# ======================================================================= NATURAL DATA
class Natural(Scene):
    """§6.2 / Fig. 8a (requential, 6e18 FLOPs; 5B tokens per §6.2) and §6.3 / Fig. 8b (scaling-law estimates; the bars
    equal Fig. 9's infinite-compute S_inf, so labelled as that limit). Solid = S_T, hatched = H_T stacked on top."""
    dur = 27.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (0.8, 'draw'), (7.5, 'pop'), (14.5, 'draw')]

    def __init__(self):
        d = tdata('fig8_natural.json')
        self.a, self.b = d['fig8a_requential']['bars'], d['fig8b_scaling']['bars']

    def _bars(self, c, t, t0, bars, x0, y0, w, h, lo, hi, fs=17, labels=None, bw=None):
        k0 = ramp(t, t0, 0.7)
        if k0 <= 0:
            return
        L = lambda v: y0 + h - (math.log10(v) - lo) / (hi - lo) * h
        for e in range(lo, hi + 1):
            line(c, x0, L(10 ** e), x0 + w, L(10 ** e), 'line', k0 * 0.8, 1)
            text(c, decade(e), x0 - 10, L(10 ** e) + 6, fs, 500, 'muted', k0, 'right')
        n = len(bars)
        slot = w / n
        bw = bw or slot * 0.62
        for i, (name, b) in enumerate(bars.items()):
            k = ramp(t, t0 + 0.2 + i * 0.15, 0.9, e_expo) * k0
            if k <= 0:
                continue
            cx = x0 + slot * (i + 0.5)
            colr = b['color']
            if colr in ('#666666',):
                colr = '#9a97a6'
            ys, yt = L(b['S_T']), L(b['S_T_plus_H_T'])
            yb = y0 + h
            ys_, yt_ = yb - (yb - ys) * k, yb - (yb - yt) * k
            rrect(c, cx - bw / 2, ys_, bw, yb - ys_, 3, fill=colr, fa=k * 0.95)
            # hatched H_T segment, stacked on top (as in the paper's figure)
            c.save()
            c.clipRect(skia.Rect.MakeXYWH(cx - bw / 2, yt_, bw, max(0, ys_ - yt_)))
            rrect(c, cx - bw / 2, yt_, bw, ys_ - yt_, 0, fill=colr, fa=k * 0.18)
            for q in range(0, int((ys_ - yt_ + bw) / 11) + 2):
                yy = ys_ - q * 11
                line(c, cx - bw / 2, yy + bw, cx + bw / 2, yy, colr, k * 0.6, 1.4)
            c.restore()
            rrect(c, cx - bw / 2, yt_, bw, ys_ - yt_, 2, stroke=colr, sw=1.2, a=k)
            lab = (labels or {}).get(name, name)
            text(c, lab, cx, y0 + h + 30, fs, 500, 'ink', k0, 'center', kind='mono')

    def draw(self, c, t):
        hdr(self, c, t, '06', 'real data', 'Text is rich, pixels are *noisy*',
            sub='Fig. 8a: requential estimates at 6 × 10¹⁸ FLOPs, models up to 160M parameters, 5 billion tokens each')
        self._bars(c, t, 0.8, self.a, 220, 390, 640, 440, 7, 11, fs=17,
                   labels={'OWText': 'web text', 'Chess (R)': 'chess (rev.)', 'Chess': 'chess', 'CIFAR-5M': 'CIFAR-5M'})
        ka = ramp(t, 0.8, 0.7)
        text(c, 'information (bits, log)', 220, 372, 17, 500, 'muted', ka, kind='mono')
        # legend: solid = structure, hatched = randomness
        info_bar(c, 220, 905, 60, 0, 18, ka, labels=False)
        text(c, 'solid: epiplexity Sₜ', 292, 921, 16, 500, 'ink', ka, kind='mono')
        rrect(c, 560, 905, 60, 18, 2, stroke='muted', sw=1.2, a=ka)
        for q in range(7):
            line(c, 562 + q * 9, 921, 570 + q * 9, 907, 'muted', ka * 0.7, 1.4)
        text(c, 'hatched: Hₜ, stacked on top', 632, 921, 16, 500, 'ink', ka, kind='mono')
        kci = ramp(t, 7.5, 0.6)
        if kci > 0:
            x = 220 + 640 / 4 * 3.5
            yb = 390 + 440 - (math.log10(self.a['CIFAR-5M']['S_T']) - 7) / 4 * 440
            rrect(c, x - 62, yb - 86, 124, 70, 10, fill='panel', fa=kci * 0.92, stroke='#d8d5e4', sw=1.2, a=kci)
            text(c, '0.4%', x, yb - 50, 28, 600, '#e8e5f2', kci, 'center')
            text(c, 'is structure', x, yb - 26, 15, 500, '#d8d5e4', kci, 'center', kind='mono')
        src(c, 'Fig. 8a', 220, 965, ka)
        note(c, 'Fig. 8a’s caption says 1B tokens; §6.2 and the bars say 5B', 220, 992, ka, 16, 'c')
        # Fig. 8b
        kb = ramp(t, 14.5, 0.8)
        if kb > 0:
            labs = {'Language': 'language', 'Img VQ 32^2': 'img VQ 32²', 'Img VQ 16^2': 'img VQ 16²', 'Vid VQ 16^3': 'vid VQ 16³',
                    'Img 32^2': 'img 32²', 'Img 16^2': 'img 16²', 'Img 8^2': 'img 8²'}
            text(c, 'scaling-law estimates, 1T tokens each (bits, log)', 1000, 372, 17, 500, 'muted', kb, kind='mono')
            c.save()
            self._bars(c, t, 14.5, self.b, 1000, 390, 800, 440, 9, 13, fs=14, labels=labs)
            c.restore()
            note(c, 'shown at the infinite-compute limit (the bars equal Fig. 9’s S∞)', 1000, 935, kb, 15)
            src(c, 'Fig. 8b', 1800, 965, kb, 'right')

# ======================================================================= SELECTION
class Selection(Scene):
    """§6.4 / Fig. 8c (adapted from Jiang et al. 2025): ADO vs natural sampling; then the MDL duality (§2.3)."""
    dur = 22.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (0.8, 'draw'), (7.0, 'pop'), (12.5, 'pop')]

    def __init__(self):
        self.c = tdata('fig8_natural.json')['fig8c_ado']

    def draw(self, c, t):
        hdr(self, c, t, '06', 'choosing data', 'Pick the data, not just the *model*',
            sub='Fig. 8c (from Jiang et al. 2025): ADO vs natural sampling; 1.3B parameters, 125B tokens of the Pile')
        A, N_ = LOOP_COLORS['non-looped'], LOOP_COLORS['looped']
        ka = ramp(t, 0.8, 0.7)
        ax = LinAxes(200, 400, 560, 300, (0, 60000), (1.9, 3.0))
        if ka > 0:
            ax.draw(c, ka, (0, 20000, 40000, 60000), (2.0, 2.5, 3.0), fmt='{:.1f}', xfmt='{:g}')
            text(c, 'training loss', 200, 382, 17, 500, 'muted', ka, kind='mono')
            text(c, 'step', 760, 760, 17, 500, 'muted', ka, 'right', kind='mono')
            for name, colr, t0 in (('Natural', N_, 1.0), ('ADO', A, 1.6)):
                d = self.c['loss'][name]
                curve_reveal(c, ax, d['x'], d['y'], colr, t, t0, 2.4, w=2.6)
            X, Y = ax.px(30000, 2.47)
            text(c, 'ADO', float(X), float(Y) - 14, 20, 600, A, ramp(t, 3.5, 0.5), kind='mono')
            X, Y = ax.px(14000, 2.0)
            text(c, 'natural', float(X), float(Y), 20, 600, N_, ramp(t, 3.0, 0.5), kind='mono')
        kb = ramp(t, 7.0, 0.7)
        if kb > 0:
            b = self.c['bars']
            rows = [('epiplexity (bits)', 'epiplexity_bits', lambda v: sci(v, 2), 2.7e10),
                    ('downstream accuracy', 'accuracy', '{:.3f}'.format, 0.7),
                    ('OOD perplexity, SlimPajama  (lower is better)', 'perplexity_1', '{:.2f}'.format, 18),
                    ('OOD perplexity, FineWeb  (lower is better)', 'perplexity_2', '{:.2f}'.format, 18)]
            # which perplexity is which corpus is not labelled in the figure; order per §6.4's listing
            for i, (lab, key, fmt, vmax) in enumerate(rows):
                y = 400 + i * 80
                text(c, lab if 'perplexity' not in key else lab.replace(', SlimPajama', ' 1').replace(', FineWeb', ' 2'),
                     900, y, 17, 500, 'ink', kb, kind='mono')
                for q, (name, colr) in enumerate((('ADO', A), ('Natural', N_))):
                    v = b[key][name]
                    kk = ramp(t, 7.2 + i * 0.3, 0.8, e_expo) * kb
                    bw = 620 * v / vmax * kk
                    rrect(c, 900, y + 12 + q * 22, max(bw, 2), 16, 4, fill=colr, fa=kb * 0.85)
                    text(c, fmt(v), 900 + bw + 10, y + 27 + q * 22, 17, 600, colr, kb)
            note(c, 'bars start at zero: the downstream gaps are small (the paper’s axes are truncated)', 900, 730, kb * 0.9, 15)
        # the duality
        for i, (who, fixed, choose, colr) in enumerate((('minimum description length', 'data fixed', 'choose the model', 'v'),
                                                        ('epiplexity', 'compute fixed', 'choose the data', 'y'))):
            k = ramp(t, 12.5 + i * 1.6, 0.8, e_expo)
            if k <= 0:
                continue
            x = MX + i * 850
            with layer(c, k):
                panel(c, x, 790, 800, 130, stroke=colr)
                text(c, who, x + 30, 840, 30, 400, colr, 1, kind='italic')
                text(c, f'{fixed}  →  {choose}', x + 30, 890, 24, 500, 'ink', 1, kind='mono')
        src(c, 'Fig. 8c', W - MX, 975, kb, 'right')

# ======================================================================= FAMILY
class Family(Scene):
    """The measures side by side: our summary of §2 and §7 (and the topic AGENTS.md comparison table)."""
    dur = 23.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (0.6, 'tick'), (8.0, 'tick'), (14.0, 'tick')]
    COLS = ['measure', 'observer', 'coin flips (n bits)', 'pseudorandom (k-bit seed)', 'what it counts']
    XS = [MX, 560, 860, 1100, 1420]
    ROWS = [(0.6, 'Shannon entropy · 1948', 'unlimited', 'n', 'k', 'randomness of a source', 'v'),
            (2.5, 'Kolmogorov complexity · 1960s', 'unlimited', '≈ n', '≈ k + a program', 'shortest description', 'v'),
            (8.0, 'sophistication · 1988', 'unlimited', '≈ 0', 'small', 'structure, much of it erased', 'v'),
            (14.0, 'usable information · 2020', 'limited (inference)', '≈ n', '≈ n', 'randomness only', 'g'),
            (17.0, 'time-bounded entropy Hₜ', 'limited (time T)', '≈ n', '≈ n', 'what looks random', 'g'),
            (18.5, 'epiplexity Sₜ', 'limited (time T)', '≈ 0', '≈ 0', 'learnable structure', 'y')]

    def draw(self, c, t):
        hdr(self, c, t, '07', 'in perspective', 'One question, many *measures*',
            sub='our summary of the paper’s §2 and §7 (usable information = Xu et al. 2020, V-information)')
        ka = ramp(t, 0.4, 0.6)
        for x, h in zip(self.XS, self.COLS):
            text(c, h, x, 380, 17, 500, 'muted', ka, kind='mono')
        line(c, MX, 398, W - MX, 398, 'line', ka, 1.5)
        for i, (ti, name, obs, coin, prng, what, colr) in enumerate(self.ROWS):
            k = ramp(t, ti, 0.6)
            if k <= 0:
                continue
            y = 450 + i * 82
            hi = colr == 'y'
            if hi:
                rrect(c, MX - 20, y - 44, W - 2 * MX + 40, 70, 12, fill='y', fa=k * 0.10, stroke='y', sw=1.6, a=k)
            vals = [name, obs, coin, prng, what]
            for j, (x, v) in enumerate(zip(self.XS, vals)):
                cc = colr if j == 0 else ('ink' if j != 1 else ('muted' if 'unlimited' in v else 'ink'))
                if j in (2, 3):
                    cc = 'g' if 'n' in v and v != '≈ 0' and 'k' not in v else ('y' if v == '≈ 0' and hi else 'ink')
                text(c, v, x, y, 23 if j == 0 else 22, 600 if j == 0 else 500, cc, k, kind='sans' if j in (0, 4) else 'mono')

# ======================================================================= LIMITS
class Limits(Scene):
    """Limits and an accuracy note (projects/epiplexity/AGENTS.md)."""
    dur = 24.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (0.6, 'pop'), (2.0, 'pop'), (9.5, 'pop'), (17.0, 'stamp_soft')]
    CARDS = [(0.6, 'a heuristic', 'The area under the curve is a heuristic. The rigorous {y:requential} estimate costs 2-10× more.', 'v'),
             (2.0, 'a particular observer', 'The numbers depend on the {y:architecture and optimizer} standing in for the observer.', 'v'),
             (9.5, 'how much, not what for', 'Epiplexity counts structure, not its {y:relevance} to your task. The real-data links are correlations.', 'v'),
             (17.0, 'text vs figure', 'Fig. 8a’s caption says {c:1B tokens}; §6.2 and the bars say {c:5B}. We follow the text.', 'c')]

    def draw(self, c, t):
        hdr(self, c, t, '07', 'limits', 'What it *doesn’t* say')
        cw, chh = 790, 250
        for i, (ti, title, body, colr) in enumerate(self.CARDS):
            k = ramp(t, ti, 0.8, e_expo)
            if k <= 0:
                continue
            r, q = divmod(i, 2)
            x, y = MX + q * (cw + 60), 360 + r * (chh + 40)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    panel(c, x, y, cw, chh, stroke=colr if colr == 'c' else 'line')
                    line(c, x + 30, y + 1, x + 150, y + 1, colr if colr == 'c' else 'y', 1, 4, cap='butt')
                    text(c, title, x + 30, y + 64, 34, 400, 'ink' if colr != 'c' else 'c', 1, kind='italic')
                    rich(c, body, x + 30, y + 124, 31, cw - 60, t, ti + 0.3, 0.025, 0.45, lh=1.36)

# ======================================================================= QUESTIONS
class Questions(Scene):
    dur = 22.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (8.5, 'pop'), (14.5, 'pop')]
    QS = [('Is information really {y:relative to the observer}, or is this a new quantity with an old name?', 2.0),
          ('Could we design {y:synthetic data} to maximize epiplexity, and what would go wrong?', 8.5),
          ('If physics could simulate everything, is nature’s structure an {y:artifact of our limits}?', 14.5)]

    def draw(self, c, t):
        hdr(self, c, t, '07', 'to think about', 'Questions to *sit* with')
        question_cards(c, t, self.QS, y0=360, dy=190, h=150, size=36)

# ======================================================================= END
class End(EndCard):
    TAKE = ('Information depends on {y:who is looking}. Bounded compute splits data into what looks {g:random} '
            'and what can be {y:learned}.')
    STATS = [('≈ 5 × 10⁶', 'bits of epiplexity, rule 54 (Fig. 3)', 'y'),
             ('> 99%', 'of CIFAR-5M’s information is random (Fig. 8a)', 'g'),
             ('28% vs 21%', 'centipawn accuracy, reverse vs forward (Fig. 7)', ORDER_COLORS['reverse'])]
