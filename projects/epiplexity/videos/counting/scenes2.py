"""Who's Counting? part 2: epiplexity, how it is measured, our laptop run, the three rules revisited, the family map,
the verdict, questions and the end card. Facts: arXiv:2601.03220v2 §3 (Def. 8, Thm 9), §4, §5 (Figs. 3, 4a, 6), §7.
Charts: Fig. 3 and Fig. 4a are redrawn from data/fig3_eca.json and data/fig4_owf_chess.json (extracted from the
paper's vector paths); the laptop chart is OUR run (data/ours_rules_n32_k16*.json, projects/epiplexity/lab/eca_lab.py)."""
from countkit import *
from scenes1 import title_line

def hourglass(c, x, y, s=1.0, a=1.0, fill=0.5, color='y'):
    """A small line-drawn hourglass: the time budget T."""
    if a <= 0:
        return
    with xform(c, x, y, s):
        p = skia.Path()
        p.moveTo(-40, -60); p.lineTo(40, -60); p.lineTo(6, 0); p.lineTo(40, 60); p.lineTo(-40, 60); p.lineTo(-6, 0); p.close()
        c.drawPath(p, paint('pencil', a * 0.9, stroke=2.4))
        line(c, -50, -62, 50, -62, 'pencil', a, 3)
        line(c, -50, 62, 50, 62, 'pencil', a, 3)
        top = skia.Path()
        h = 52 * (1 - fill)
        top.moveTo(-34 * h / 52 - 4, -h); top.lineTo(34 * h / 52 + 4, -h); top.lineTo(3, -4); top.lineTo(-3, -4); top.close()
        c.drawPath(top, paint(color, a * 0.8))
        bot = skia.Path()
        hb = 52 * fill
        bot.moveTo(-36, 58); bot.lineTo(36, 58); bot.lineTo(36 - 30 * fill, 58 - hb); bot.lineTo(-36 + 30 * fill, 58 - hb); bot.close()
        c.drawPath(bot, paint(color, a * 0.8))

class Epiplexity(Scene):
    dur = 26.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (6.5, 'chime'), (14.0, 'pop'), (20.0, 'pop')]

    def draw(self, c, t):
        header(c, t, '05', 'the paper, 2026', 'A *bounded* observer')
        kb = ramp(t, 0.5, 0.8)
        hourglass(c, 220, 420, 0.9, kb, fill=0.15 + 0.7 * ramp(t, 0.5, 25, e_lin))
        if kb > 0:
            text(c, 'one time budget, T', 320, 410, 40, 400, 'ink', kb, kind='italic')
            text(c, 'for learning the model, and for using it', 320, 456, 26, 400, 'muted', kb)
            tag(c, 'def. 8 · a two-part code under a time bound', 320, 494, kb, 'muted', 15)
        # the two-part code, assembled from pieces so the braces know where each part is
        size = 62
        keys = ('mdl_a', 'mdl_b', 'mdl_plus', 'mdl_c')
        ws = [tex_size(k, size)[0] for k in keys]
        gap = 22
        x = W / 2 - (sum(ws) + gap * 3) / 2
        xs = []
        for i, (k, wd) in enumerate(zip(keys, ws)):
            kk = ramp(t, 6.5 + i * 0.25, 0.7)
            tex(c, k, x, 640, size, kk, align='left')
            xs.append((x, x + wd))
            x += wd + gap
        kl = ramp(t, 9.0, 0.6)
        text(c, 'bits for the model', (xs[1][0] + xs[1][1]) / 2, 560, 22, 600, 'y', kl, 'center')
        text(c, 'bits for the data, given the model', (xs[3][0] + xs[3][1]) / 2, 560, 22, 600, 'c', kl, 'center')
        kt = ramp(t, 8.0, 0.6)
        tag(c, 'the shortest total code among programs that run within T', W / 2, 735, kt, 'muted', 16, 'center')
        # the split
        ks = ramp(t, 14.0, 0.8)
        if ks > 0:
            brace(c, xs[1][0] - 6, xs[1][1] + 6, 695, 'y', ks, ramp(t, 14.0, 0.6, e_io))
            cx = (xs[1][0] + xs[1][1]) / 2
            tex(c, 'st', 560, 835, 52, ks)
            text(c, 'epiplexity: epistemic complexity', 560, 905, 26, 600, 'y', ks, 'center')
            text(c, 'the structure', 560, 940, 22, 400, 'muted', ks, 'center')
        kh = ramp(t, 20.0, 0.8)
        if kh > 0:
            brace(c, xs[3][0] - 6, xs[3][1] + 6, 695, 'c', kh, ramp(t, 20.0, 0.6, e_io))
            cx = (xs[3][0] + xs[3][1]) / 2
            tex(c, 'ht', 1360, 830, 52, kh)
            text(c, 'time-bounded entropy', 1360, 905, 26, 600, 'c', kh, 'center')
            text(c, 'what still looks random to this observer', 1360, 940, 22, 400, 'muted', kh, 'center')

class ScoreEpi(ScoreScene):
    dur = 21.0
    chapter = 4
    COLS_DONE, COLS_NOW, TIMES, WIN = (0, 1, 2, 3, 4), (5, 6), (1.8, 5.0, 9.8, 15.0), 18.0
    NUM, KICK, TITLE = '05', 'the paper, 2026', 'The new *scores*'
    NOTE = 'qualitative, from the paper: Thm 9 (pseudorandom), Fig. 3 (rule 54)'

# ---------------------------------------------------------------- measuring
def _fig3():
    d = load_json('fig3_eca.json')['panels']['epiplexity']['frontier']
    return {int(k): (np.array(v['x']), np.array(v['y'])) for k, v in d.items()}

class Measuring(Scene):
    dur = 30.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (3.5, 'draw'), (19.0, 'draw')]

    def __init__(self):
        self.f3 = _fig3()

    def draw(self, c, t):
        header(c, t, '06', 'measuring it', 'Watch the *loss*')
        # left: sketch loss curves (illustration)
        ax = Axes(170, 380, 640, 420, (0, 1), (0, 1.1))
        ka = ramp(t, 0.8, 0.8)
        if ka > 0:
            line(c, ax.x, ax.y + ax.h, ax.x + ax.w, ax.y + ax.h, 'muted', ka, 1.6)
            line(c, ax.x, ax.y, ax.x, ax.y + ax.h, 'muted', ka, 1.6)
            text(c, 'training →', ax.x + ax.w, ax.y + ax.h + 34, 18, 400, 'muted', ka, 'right', kind='mono')
            text(c, 'loss', ax.x, ax.y - 18, 18, 400, 'muted', ka, kind='mono')
            tag(c, 'illustration', ax.x + ax.w, ax.y - 18, ka, 'muted', 15, 'right')
        u = np.linspace(0, 1, 200)
        curves = [('random: never falls', 'v', 0.95 + 0 * u, 3.5),
                  ('simple: falls fast, then stops', 'f', 0.08 + 0.87 * np.exp(-u / 0.07), 5.5),
                  ('structured: keeps falling', 'y', 0.42 + 0.53 * np.exp(-u / 0.42), 7.5)]
        for lab, colr, y, t0 in curves:
            k = ramp(t, t0, 0.5)
            if k <= 0:
                continue
            if colr == 'y':
                kf = ramp(t, 10.5, 0.9)
                if kf > 0:
                    pts = ax.pts(u, y)
                    pth = skia.Path()
                    pth.moveTo(*pts[0])
                    for p in pts[1:]:
                        pth.lineTo(*p)
                    _, Yf = ax.px(1, y[-1])
                    pth.lineTo(pts[-1][0], Yf); pth.lineTo(pts[0][0], Yf); pth.close()
                    c.drawPath(pth, paint('y', 0.22 * kf))
                    line(c, ax.x, Yf, ax.x + ax.w, Yf, 'y', kf * 0.8, 1.6, dash=[7, 6])
                    text(c, '↑ area above the final loss', ax.x + 230, Yf + 40, 22, 600, 'y', kf)
                    text(c, '≈ bits the model absorbed', ax.x + 254, Yf + 68, 20, 400, 'ink', kf)
            draw_poly(c, ax.pts(u, y), colr, k, 4 if colr == 'y' else 3, prog=ramp(t, t0, 1.2, e_io), glow=4)
            X, Y = ax.px(1, y[-1])
            text(c, lab, X - 4, Y - (34 if colr == 'y' else 14), 19, 600, colr, ramp(t, t0 + 0.8, 0.5), 'right')
        kn = ramp(t, 14.0, 0.7)
        if kn > 0:
            note(c, 'prequential (this area): a heuristic', ax.x, ax.y + ax.h + 80, kn, 16, 'muted')
            note(c, 'requential (teacher → student): stricter, smaller, correlated (Fig. 2c)', ax.x, ax.y + ax.h + 106, kn, 16, 'muted')
        # right: Fig. 3, epiplexity against compute
        kr = ramp(t, 19.0, 0.8)
        if kr <= 0:
            return
        bx = Axes(1040, 380, 720, 420, (12, 17.3), (0, 6))
        bx.draw(c, kr, [12, 13, 14, 15, 16, 17], [0, 2, 4, 6], prog=kr, fmt='{:g}', xfmt='', grid=True)
        for e in (12, 13, 14, 15, 16, 17):
            X, _ = bx.px(e, 0)
            text(c, decade(e), X, bx.y + bx.h + 34, 20, 500, 'muted', kr, 'center')
        text(c, 'compute (FLOPs)', bx.x + bx.w / 2, bx.y + bx.h + 74, 18, 400, 'muted', kr, 'center', kind='mono')
        text(c, 'epiplexity S_T (millions of bits)', bx.x, bx.y - 18, 18, 400, 'muted', kr, kind='mono')
        tag(c, 'Fig. 3, redrawn  ·  predict Y = the rule, 48 steps on, from a random 64-cell X', bx.x + bx.w / 2, bx.y + bx.h + 104, kr, 'muted', 14, 'center')
        for rule, t0 in ((54, 19.3), (15, 22.5), (30, 23.5)):
            xs, ys = self.f3[rule]
            pts = bx.pts(np.log10(xs), ys / 1e6)
            k = ramp(t, t0, 0.5)
            draw_poly(c, pts, RULE_COL[rule], k, 4, prog=ramp(t, t0, 2.0, e_io), glow=4)
            pe = ramp(t, t0, 2.0, e_io)
            n = max(1, int(round(pe * len(pts))))
            for p in pts[:n]:
                circle(c, p[0], p[1], 5, fill=RULE_COL[rule], stroke='ink', sw=1.2, a=k)
            ke = ramp(t, t0 + 1.8, 0.5)
            X, Y = pts[-1]
            lab = {54: 'rule 54', 15: 'rule 15', 30: 'rule 30'}[rule]
            text(c, lab, X + 12, Y + {54: 6, 15: -12, 30: 22}[rule], 22, 600, RULE_COL[rule], ke)
        k5 = ramp(t, 21.3, 0.6)
        if k5 > 0:
            X, Y = bx.pts(np.log10(self.f3[54][0][-1:]), self.f3[54][1][-1:] / 1e6)[0]
            text(c, f'{self.f3[54][1][-1] / 1e6:.2f} M bits', X - 10, Y - 20, 20, 600, RULE_COL[54], k5, 'right')

# ---------------------------------------------------------------- our laptop run
class Laptop(Scene):
    """OUR run (projects/epiplexity/lab/eca_lab.py): the 20,000-step run (data/ours_rules_n32_k16_s20000.json) as curves,
    and the prequential area at 4,000 steps (a separate run with the same setup, data/ours_rules_n32_k16.json) against
    20,000 steps. At the short budget rule 15's area is larger; at the long one rule 54's is."""
    dur = 27.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (6.5, 'draw'), (14.0, 'pop'), (17.5, 'pop')]
    COLORS = {'coin': ('coin flips', 'v'), '30': ('rule 30', RULE_COL[30]), '15': ('rule 15', RULE_COL[15]),
              '54': ('rule 54', RULE_COL[54]), '110': ('rule 110', '#5aa6ec')}
    START = {'coin': 6.5, '30': 6.9, '15': 7.3, '54': 9.5, '110': 10.0}

    def __init__(self):
        self.long = load_json('ours_rules_n32_k16_s20000.json')
        self.short = load_json('ours_rules_n32_k16.json')

    def draw(self, c, t):
        header(c, t, '06', 'our run, not the paper’s', 'A laptop-sized *check*')
        d = self.long
        k0 = ramp(t, 0.5, 0.7)
        note(c, f'a ~0.8 M-parameter transformer  ·  predict a {d["n"]}-cell row {d["k"]} steps ahead from a random row'
                f'  ·  {d["batch"]} fresh samples per step', MX, 332, k0, 16, 'muted')
        ax = Axes(200, 400, 980, 440, (0, d['steps']), (0, 40))
        ka = ramp(t, 1.5, 0.8)
        ax.draw(c, ka, [0, 5000, 10000, 15000, 20000], [0, 8, 16, 24, 32, 40], prog=ka, fmt='{:g}', xfmt='{:,.0f}')
        text(c, 'training step', ax.x + ax.w / 2, ax.y + ax.h + 70, 18, 400, 'muted', ka, 'center', kind='mono')
        text(c, 'loss on fresh samples (bits per row)', ax.x, ax.y - 18, 18, 400, 'muted', ka, kind='mono')
        tag(c, OUR_RUN, ax.x + ax.w, ax.y - 18, ka, 'y', 16, 'right')
        # the short budget, marked on the long run
        ks = ramp(t, 14.0, 0.6)
        if ks > 0:
            X, _ = ax.px(4000, 0)
            line(c, X, ax.y, X, ax.y + ax.h, 'y', ks, 2, dash=[6, 6])
            text(c, 'stop at 4,000?', X + 10, ax.y + 24, 18, 600, 'y', ks)
        keys = [k for k in ('coin', '30', '110', '15', '54') if k in d['runs']]
        for key in keys:
            lab, colr = self.COLORS[key]
            r = d['runs'][key]
            y = np.array(r['curve'])
            x = np.arange(len(y)) * r['every']
            k = ramp(t, self.START[key], 0.5)
            if k <= 0:
                continue
            pts = ax.pts(x, np.clip(y, 0, 40))
            draw_poly(c, pts, colr, k, 1.8, prog=ramp(t, self.START[key], 1.8, e_io))
            X, Y = pts[-1]
            ly = {'coin': -24, '30': -4, '15': -12, '54': 6, '110': 16}[key]
            text(c, lab, X + 12, Y + ly, 19, 600, colr, ramp(t, self.START[key] + 1.6, 0.5))
        # area above the final loss: 4,000 steps vs 20,000 steps
        kb = ramp(t, 14.0, 0.8)
        if kb <= 0:
            return
        x0, y0 = 1330, 420
        text(c, 'area above the final loss', x0, y0 - 20, 24, 400, 'ink', kb, kind='italic')
        tag(c, 'millions of bits  ·  our run', x0, y0 + 6, kb, 'muted', 14)
        vmax = 10e6
        bw = 330
        for g, (title, src, t0) in enumerate((('after 4,000 steps', self.short, 14.3), ('after 20,000 steps', self.long, 17.6))):
            gy = y0 + 50 + g * 210
            kg = ramp(t, t0, 0.6)
            text(c, title, x0, gy + 18, 19, 600, 'y' if g else 'muted', kg, kind='mono')
            for i, key in enumerate(('15', '54', '30')):
                if key not in src['runs']:
                    continue
                lab, colr = self.COLORS[key]
                v = src['runs'][key]['area_bits']
                yy = gy + 34 + i * 52
                kk = ramp(t, t0 + 0.2 + i * 0.2, 0.5)
                text(c, lab, x0, yy + 26, 19, 600, colr, kk)
                gr = ramp(t, t0 + 0.2 + i * 0.2, 0.9, e_io)
                ww = max(3, bw * v / vmax * gr)
                rrect(c, x0 + 104, yy + 6, ww, 28, 5, fill=colr, a=kk, fa=kk * 0.85)
                text(c, f'{v / 1e6:.2f}' if v > 5e4 else f'{v / 1e6:.3f}', x0 + 112 + ww, yy + 28, 19, 600, 'ink', kk)
        kn = ramp(t, 19.0, 0.6)
        note(c, 'two runs, same setup; each area is', x0, y0 + 490, kn, 14, 'muted')
        note(c, 'measured against that run’s final loss', x0, y0 + 512, kn, 14, 'muted')

# ---------------------------------------------------------------- the rules, revisited
class Revisited(Scene):
    dur = 30.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (10.0, 'pop'), (18.0, 'pop')]

    def __init__(self):
        self.f4 = load_json('fig4_owf_chess.json')['fig4a_owf']['series']

    def _card(self, c, t, i, old, new, t0):
        cw, x = 532, MX + i * 574
        k = ramp(t, t0, 0.9, e_expo)
        if k <= 0:
            return None, 0
        with layer(c, k):
            with xform(c, 0, (1 - k) * 30):
                panel(c, x, 330, cw, 480)
                line(c, x + 36, 331, x + 156, 331, 'y', 1, 4, cap='butt')
                w = text(c, old, x + 36, 384, 24, 400, 'muted', 1, kind='italic')
                ks = ramp(t, t0 + 0.4, 0.5, e_io)
                line(c, x + 32, 376, x + 40 + w * ks, 376, 'c', 1, 2.4)
                text(c, new, x + 36, 432, 33, 400, 'y', ramp(t, t0 + 0.7, 0.6), kind='italic')
        return x, k

    def draw(self, c, t):
        header(c, t, '07', 'the rules, revisited', 'Three rules, *bent*')
        x, k = self._card(c, t, 0, 'processing can’t add', 'Processing creates it', 4.0)
        if k:
            with layer(c, k):
                rich(c, 'A generator stretches a short seed into bits that look random to any fast observer: {c:Hₜ jumps} (Thm 12).',
                     x + 36, 500, 24, 460, t, 5.0, 0.02, 0.45)
                rich(c, 'Rule 54 turns random rows plus a tiny rule into {y:millions of bits of structure} (Fig. 3).',
                     x + 36, 650, 24, 460, t, 6.5, 0.02, 0.45)
        x, k = self._card(c, t, 1, 'order doesn’t matter', 'Order matters', 10.0)
        if k:
            with layer(c, k):
                s = self.f4
                ax = Axes(x + 80, 480, 410, 210, (16, 64), (0, 80))
                ax.draw(c, 1, [16, 32, 48, 64], [0, 40, 80], fmt='{:g}', xfmt='{:g}')
                text(c, 'bits per (X, Y) pair', ax.x, ax.y - 14, 14, 400, 'muted', 1, kind='mono')
                text(c, 'state size n', ax.x + ax.w / 2, ax.y + ax.h + 60, 14, 400, 'muted', 1, 'center', kind='mono')
                kd = ramp(t, 11.0, 1.4, e_io)
                for key, lab, dy in (('entropy', 'entropy (n)', 26), ('forward', 'forward', 4), ('reverse', 'reverse', -8)):
                    pts = ax.pts(s[key]['x'], s[key]['y'])
                    draw_poly(c, pts, FIG4_COL[key], 1, 2.6 if key != 'entropy' else 2, prog=kd,
                              dash=[6, 5] if key == 'entropy' else None)
                    if key != 'entropy':
                        for p in pts[:max(1, int(kd * len(pts)))]:
                            circle(c, p[0], p[1], 4.5, fill=FIG4_COL[key], a=1)
                    li = {'reverse': 0, 'forward': 1, 'entropy': 2}[key]
                    kl = ramp(t, 12.2, 0.5)
                    line(c, ax.x + 16, ax.y + 16 + li * 24, ax.x + 44, ax.y + 16 + li * 24, FIG4_COL[key], kl, 2.6,
                         dash=[6, 5] if key == 'entropy' else None)
                    text(c, lab, ax.x + 54, ax.y + 22 + li * 24, 16, 600, FIG4_COL[key], kl)
                tag(c, 'Fig. 4a, redrawn  ·  rule 30, 8 steps', x + 36, 796, 1, 'muted', 14)
        x, k = self._card(c, t, 2, 'a model can’t outgrow its source', 'Models can outgrow it', 18.0)
        if k:
            with layer(c, k):
                rich(c, 'Predicting rule 54 far ahead, a compute-limited model reaches {y:Sₜ ≈ 1.5 × 10⁷ bits} (Fig. 6, its peak).',
                     x + 36, 500, 24, 460, t, 19.0, 0.02, 0.45)
                rich(c, 'The rule itself is an {f:8-bit table}. Given enough compute, a looped model unrolls it step by step, and Sₜ drops.',
                     x + 36, 650, 24, 460, t, 20.5, 0.02, 0.45)
        # the classical measures keep all three
        kt = ramp(t, 25.0, 0.8)
        if kt > 0:
            rows = [('Shannon, Kolmogorov', '✓  ✓  ✓', 'f', 'up to small terms, with unlimited compute'),
                    ('a bounded observer', '✗  ✗  ✗', 'c', 'Thms 12-13, Figs. 3, 4a, 5, 6')]
            for j, (who, marks, colr, sub) in enumerate(rows):
                y = 870 + j * 54
                kk = ramp(t, 25.0 + j * 0.5, 0.6)
                text(c, who, MX + 20, y, 26, 600, 'ink', kk)
                text(c, marks, MX + 420, y, 28, 700, colr, kk)
                text(c, sub, MX + 600, y - 2, 18, 400, 'muted', kk, kind='mono')

# ---------------------------------------------------------------- the family map
MAP = [  # label, x, y (baseline-ish), colour, appears, aims at structure?
    ('Kolmogorov  1965', 290, 870, 'x', 8.0, False),
    ('logical depth  1988', 290, 800, 'f', 8.6, True),
    ('sophistication  1988', 590, 870, 'f', 9.2, True),
    ('effective complexity  1996', 590, 800, 'f', 9.8, True),
    ('Shannon entropy  1948', 990, 870, 'g', 8.0, False),
    ('excess entropy  1983', 990, 800, 'g', 13.0, False),
    ('speed prior  2002', 290, 400, 'v', 18.0, False),
    ('time-bounded K', 290, 470, 'v', 18.4, False),
    ('pseudoentropy  1999', 990, 400, 'c', 18.0, False),
    ('usable information  2020', 990, 470, 'c', 18.6, False),
    ('time-bounded entropy', 990, 540, 'c', 23.0, False),
]

class Map(Scene):
    dur = 32.0
    chapter = 7
    cues = [(0.2, 'whoosh'), (8.0, 'pop'), (13.0, 'pop'), (18.0, 'pop'), (23.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '08', 'the family  ·  ' + FRAMING, 'A *map* of the measures')
        x0, x1, y0, y1 = 270, 1490, 340, 920
        ka = ramp(t, 0.8, 0.8)
        if ka > 0:
            xm, ym = x0 + 0.56 * (x1 - x0), (y0 + y1) / 2 + 30
            rrect(c, xm, y0, x1 - xm, ym - y0, 16, fill='y', a=ka, fa=ka * 0.05)
            line(c, xm, y0, xm, y1, 'faint', ka, 1.4, dash=[6, 6])
            line(c, x0, ym, x1, ym, 'faint', ka, 1.4, dash=[6, 6])
            arrow(c, x0, y1, x1 + 10, y1, 'muted', ka, 2, 12, prog=ramp(t, 0.8, 0.8, e_io))
            arrow(c, x0, y1, x0, y0 - 10, 'muted', ka, 2, 12, prog=ramp(t, 0.8, 0.8, e_io))
            kl = ramp(t, 3.5, 0.6)
            text(c, 'one string', x0 + 10, y1 + 36, 20, 400, 'muted', kl, kind='mono')
            text(c, 'a distribution', x1, y1 + 36, 20, 400, 'muted', kl, 'right', kind='mono')
            text(c, 'unlimited', x0 - 16, y1 - 10, 18, 400, 'muted', kl, 'right', kind='mono')
            text(c, 'compute', x0 - 16, y1 + 12, 18, 400, 'muted', kl, 'right', kind='mono')
            text(c, 'bounded', x0 - 16, y0 + 8, 18, 400, 'muted', kl, 'right', kind='mono')
            text(c, 'observer', x0 - 16, y0 + 30, 18, 400, 'muted', kl, 'right', kind='mono')
            tag(c, FRAMING, x1, y0 - 14, kl, 'muted', 15, 'right')
        for lab, x, y, colr, t0, struct in MAP:
            k = ramp(t, t0, 0.5, e_back)
            if k <= 0:
                continue
            pill(c, x, y - 18, lab, colr, k, 0.8 + 0.2 * k, filled=not struct, size=17)
        ke = ramp(t, 23.0, 0.7, e_back)
        if ke > 0:
            w = text_width('epiplexity  Sₜ', 34, 700)
            ex, ey = 1130, 625
            rrect(c, ex - 24, ey - 50, w + 48, 72, 36, fill='y', a=ke, fa=ke * 0.2, glow=14)
            rrect(c, ex - 24, ey - 50, w + 48, 72, 36, stroke='y', sw=2.4, a=ke)
            text(c, 'epiplexity  Sₜ', ex, ey, 34, 700, 'y', ke)
        # legend and the MDL mirror
        kg = ramp(t, 8.0, 0.6)
        if kg > 0:
            lx = 1560
            pill(c, lx, 360, 'counts the total', 'g', kg, filled=True, size=15)
            pill(c, lx, 410, 'or the random part', 'c', kg, filled=True, size=15)
            pill(c, lx, 460, 'aims at structure', 'f', kg, filled=False, size=15)
        km = ramp(t, 27.5, 0.8, e_expo)
        if km > 0:
            with layer(c, km):
                panel(c, 1540, 560, 260, 330)
                text(c, 'a mirror', 1570, 610, 28, 400, 'ink', 1, kind='italic')
                text(c, 'MDL', 1570, 668, 22, 700, 'g', 1)
                text(c, 'data → best model', 1570, 700, 18, 400, 'ink', 1)
                note(c, 'rissanen, 1978', 1570, 726, 1, 14, 'muted')
                text(c, 'epiplexity', 1570, 790, 22, 700, 'y', 1)
                text(c, 'budget → best data', 1570, 822, 18, 400, 'ink', 1)
                note(c, 'the paper, §2.3', 1570, 848, 1, 14, 'muted')

# ---------------------------------------------------------------- verdict, questions, end
class Verdict(Scene):
    dur = 17.0
    chapter = 7
    cues = [(0.2, 'whoosh'), (8.5, 'pop')]

    def draw(self, c, t):
        header(c, t, '08', 'was shannon wrong?', 'Two different *questions*')
        for j, (who, q, colr, t0) in enumerate((('the engineer', 'How many bits must I send?', 'g', 0.6),
                                                 ('the learner', 'How much is there to learn, in the time I have?', 'y', 4.8))):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + j * 860
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    panel(c, x, 330, 820, 420)
                    line(c, x + 36, 331, x + 156, 331, colr, 1, 4, cap='butt')
                    note(c, who, x + 36, 384, 1, 18, colr)
                    rich(c, q, x + 36, 450, 36, 740, t, t0 + 0.3, 0.03, 0.45, base_w=500)
                    if j == 0:      # sender -> channel -> receiver
                        for bx, lab in ((x + 60, 'sender'), (x + 560, 'receiver')):
                            rrect(c, bx, 590, 200, 80, 12, fill='panel2', fa=0.9)
                            rrect(c, bx, 590, 200, 80, 12, stroke='g', sw=1.6)
                            text(c, lab, bx + 100, 640, 22, 500, 'ink', 1, 'center')
                        pth = skia.Path()
                        for i in range(61):
                            xx = x + 270 + i * 4.8
                            yy = 630 + 9 * math.sin(i * 0.6 + t * 3)
                            pth.moveTo(xx, yy) if i == 0 else pth.lineTo(xx, yy)
                        c.drawPath(pth, paint('g', 0.9, stroke=2.4))
                        note(c, 'the receiver already knows the code', x + 410, 715, 1, 15, 'muted', 'center')
                    else:           # data -> learner, under a budget
                        file_thumb(c, 'ca', x + 70, 590, 150, 1, cell=6)
                        arrow(c, x + 250, 640, x + 420, 640, 'y', 1, 2.4, 12)
                        for i in range(4):
                            for jj in range(3):
                                circle(c, x + 470 + i * 50, 600 + jj * 40, 7, fill='y', a=0.85)
                        hourglass(c, x + 720, 640, 0.6, 1, fill=0.4 + 0.3 * ramp(t, t0, 12, e_lin))
                        note(c, 'a model, built within budget T', x + 560, 715, 1, 15, 'muted', 'center')
        for i, (s, colr) in enumerate((('it depends on the observer', 'c'), ('it can only be estimated', 'c'),
                                       ('it counts structure, not usefulness', 'c'))):
            kk = ramp(t, 8.8 + i * 1.3, 0.6, e_back)
            pill(c, MX + i * 560, 820, s, colr, kk, 0.8 + 0.2 * kk, size=19)
        text(c, 'the price', MX, 800, 18, 400, 'muted', ramp(t, 8.6, 0.5), kind='mono')

class Questions(Scene):
    dur = 21.0
    chapter = 8
    cues = [(0.2, 'whoosh')]

    def draw(self, c, t):
        header(c, t, '09', 'to think about', 'Questions to *think about*')
        question_cards(c, t, [
            ('If information depends on the observer, is it still a {y:property of the data}?', 2.5),
            ('A much faster observer sees less randomness. Does it see {y:more structure, or less}?', 8.5),
            ('The laws of physics are short. Is the universe they generate {y:rich in epiplexity}, and for whom?', 14.5),
        ], y0=330, dy=200, h=170, size=36)

class End(Scene):
    dur = 13.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (12.0, 'outro')]

    def draw(self, c, t):
        k = ramp(t, 0.2, 0.8)
        kicker(c, 'who’s counting?', MX, 168, k, 'y', 18)
        title_line(c, 'Same four files, *different winners*', MX, 244, 60, k, align='left', prog=ramp(t, 0.8, 0.9, e_io))
        scorecard(c, t, cols_done=tuple(range(len(COLS))), win_all=1.0, a=ramp(t, 0.3, 0.8))
        k2 = ramp(t, 3.0, 0.9)
        text(c, CITE, MX, 990, 19, 500, 'ink', k2)
        text(c, ARXIV + '  ·  an unofficial explainer, not by the authors', MX, 1022, 17, 500, 'g', k2, kind='mono')
