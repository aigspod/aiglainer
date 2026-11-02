"""Video 2 of 3: can the gap be explained away? Fig. 1 (redrawn from its vector paths, data/fig1.json in errors-gap),
Table 4 (reweighting, enrichment), Table 7 and §3 (margin matching), §3 and Table 4 (the subject-logit nudge)."""
from errkit import *
import scenes as part1

class Piles(part1.TwoPiles):
    chapter, NUM = 0, '01'

class Gap(part1.Table1):
    chapter, NUM = 0, '01'

class Title(TitleCard):
    TITLE = 'Can the gap be *explained away*?'
    STICKY = ['circuits & errors', 'three excuses']

# ---------------------------------------------------------------- Fig. 1 redrawn
LIN = 14.35 / 32.29          # width of the linear 0..0.1 stretch of Fig. 1's x-axis, in decades

def xu(v):
    v = np.asarray(v, float)
    return np.where(v <= 0.1, v / 0.1 * LIN, LIN + np.log10(np.maximum(v, 1e-9) / 0.1))

class Fig1(Scene):
    dur = 36.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (12.0, 'draw'), (21.0, 'pop')]
    ORDER = ['a', 'b', 'c', 'd', 'e', 'f']

    def __init__(self):
        self.d = load_json('fig1.json')

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '02'), 'excuse one: errors are rare', 'More *mistakes* to learn from', sub='Bigger models, multiple-choice science (ARC) and subtraction · Fig. 1, redrawn from the paper’s vector data')
        pw, ph, gx, gy = 470, 190, 120, 125
        x0, y0 = 200, 370
        k = ramp(t, 10.0, 0.8)
        umax = float(xu(50))
        for i, key in enumerate(self.ORDER):
            p = self.d[key]
            cx, cy = x0 + (i % 3) * (pw + gx), y0 + (i // 3) * (ph + gy)
            focus = 1.0
            if t >= 21.0:
                focus = 1.0 if key == 'b' else 1 - 0.65 * ramp(t, 21.0, 0.8)
            a = k * focus
            if a <= 0:
                continue
            ax = Axes(cx, cy, pw, ph, (0, umax), (0, 100))
            ax.draw(c, a, [], [0, 50, 100], prog=1, fmt='{:g}', grid=True)
            for v, lab in ((0, '0'), (0.1, '0.1'), (1, '1'), (10, '10'), (50, '50')):
                X, _ = ax.px(float(xu(v)), 0)
                text(c, lab, X, cy + ph + 30, 18, 500, 'muted', a, 'center', kind='mono')
            text(c, p['title'], cx, cy - 22, 22, 600, 'ink', a)
            pr = ramp(t, 12.0, 2.0, e_io)
            for series, colr, dash in (('ok', 'g', None), ('err', 'c', [9, 6])):
                xs = xu([q[0] for q in p[series]]); ys = [q[1] for q in p[series]]
                draw_poly(c, ax.pts(xs, ys), colr, a, 3.4, prog=pr, dash=dash)
                for X, Y in ax.pts(xs, ys)[:max(0, int(round(pr * 9)))]:
                    circle(c, X, Y, 4, fill=colr, a=a)
        kl = ramp(t, 12.0, 0.6)
        legend_item(c, 200, 1000 - 30, 'g', 'agrees where the model is right', kl, size=21)
        legend_item(c, 700, 1000 - 30, 'c', 'same mistake where the model is wrong', kl, dash=True, size=21)
        text(c, 'x: retained edges (%)   ·   y: agreement (%)', W - MX, 1000 - 30, 19, 500, 'muted', kl, 'right', kind='mono')
        kb = ramp(t, 21.0, 0.8)
        if kb > 0:
            with layer(c, kb):
                panel(c, 1440, 132, 360, 178, stroke='y')
                text(c, '38%', 1466, 204, 56, 760, 'y', 1)
                rich(c, 'of the examples used to find {y:Gemma’s} circuit are its own mistakes (430 of 1,119, Table 5)', 1466, 244, 19, 320, t, 21.3, 0.02, 0.4)

ROWS_RW = [('baseline search', 98.7, 9.3, None), ('errors given half the weight', 91.0, 37.0, None),
           ('500 errors + 500 successes', 91.4, 44.2, None)]   # Table 4 / §3: the ACDC follow-up on IOI

class Reweight(Scene):
    dur = 24.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (5.0, 'pop'), (16.5, 'pop')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '02'), 'excuse one: errors are rare', 'Weight the *mistakes*', sub='A follow-up on the name task, with ACDC · §3 and Table 4')
        n = 1 if t < 5 else (2 if t < 16.5 else 3)
        pair_bars(c, ROWS_RW[:n], 120, 470, 1180, t, 0.8, label_w=440, show_f=False)
        bars_legend(c, MX, 960, ramp(t, 1.0, 0.6), 21)
        caption(c, t, 'More exposure helps, and it {c:costs} you on the right pile. Rarity is {y:part} of the story, not all of it.', 18.0, None, y=890, size=30)

class CloseCalls(Scene):
    dur = 40.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (13.0, 'sweep'), (19.0, 'pop'), (33.0, 'pop')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '03'), 'excuse two: close calls', 'Barely *wrong*')
        # left: two sentences' scores for the two names (illustration)
        k = ramp(t, 4.0, 0.8)
        if k > 0:
            with layer(c, k):
                for j, (lab, a1, a2, colr) in enumerate((('a confident right answer', 0.82, 0.18, 'f'), ('a close-call mistake', 0.47, 0.53, 'r'))):
                    yy = 340 + j * 230
                    panel(c, MX, yy, 700, 190)
                    text(c, lab, MX + 30, yy + 46, 24, 600, colr, 1)
                    for r_, (nm, v, cc) in enumerate((('right name', a1, 'f'), ('wrong name', a2, 'r'))):
                        yb = yy + 80 + r_ * 46
                        text(c, nm, MX + 200, yb + 22, 20, 500, 'muted', 1, 'right')
                        rrect(c, MX + 220, yb, 420 * v * ramp(t, 4.3 + j * 0.4, 1.0, e_expo), 28, 5, fill=cc, a=1, fa=0.8)
                illustration(c, MX, 830, 1)
        # right: margin matching numbers
        k2 = ramp(t, 13.0, 0.8)
        if k2 > 0:
            with layer(c, k2):
                kicker(c, 'pair each mistake with an equally unsure correct answer', 900, 360, 1, 'muted', 16)
        if t >= 18.5:
            rows = [('', 80.0, 54.9, None), ('', 46.7, 54.9, None)]   # §3: Llama ARC-Challenge, 2% edges
            labs = ['Llama · hard science · 2% edges: all', '… among matched close calls']
            pair_bars(c, rows, 880, 470, 620, t, 18.6, label_w=0, show_f=False, dy=150)
            for i, lab in enumerate(labs):
                text(c, lab, 880, 455 + i * 150, 21, 600, 'ink', ramp(t, 19.0 + i * 0.5, 0.6))
        kr = ramp(t, 29.0, 0.7)
        if kr > 0:
            hand(c, 'the gap reverses (the paper says "narrowed")', 900, 790, 30, 'pencil', kr, -2.0, ramp(t, 29.0, 1.0, e_lin))
        caption(c, t, 'Name task, after matching: {f:94.9%} vs {c:14.8%} for the classic circuit. Every circuit keeps a positive gap (Table 7).', 33.0, None, y=985, size=29)

class Nudge(Scene):
    dur = 32.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (8.0, 'pop'), (16.0, 'tick'), (20.0, 'pop')]
    N = 24
    MODEL = {3, 9, 14, 20}       # illustration: which sentences the model gets wrong
    NUDGED = {5, 9, 17, 22}      # illustration: same count, mostly different sentences

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '04'), 'excuse three: a little too right', 'Just *nudge* it?', sub='Shift the circuit’s output toward the repeated name (§3, Table 4)')
        cell, x0 = 64, 160
        for r_, (lab, wrong, t0) in enumerate((('the model', self.MODEL, 6.0), ('the nudged circuit', self.NUDGED, 16.0))):
            k = ramp(t, t0, 0.7)
            if k <= 0:
                continue
            yy = 420 + r_ * 170
            text(c, lab, x0, yy - 24, 24, 600, 'ink', k)
            for i in range(self.N):
                X = x0 + i * cell
                bad = i in wrong
                kk = ramp(t, t0 + 0.03 * i, 0.4) * k
                rrect(c, X, yy, cell - 12, 70, 8, fill='r' if bad else 'f', a=kk, fa=kk * (0.85 if bad else 0.22))
                if bad:
                    text(c, '✗', X + (cell - 12) / 2, yy + 46, 30, 700, 'ink', kk, 'center')
            text(c, f'{len(wrong)} of {self.N} wrong', x0 + self.N * cell + 10, yy + 46, 22, 600, 'r', k)
        km = ramp(t, 20.0, 0.7)
        if km > 0:
            for i in self.MODEL & self.NUDGED:
                X = x0 + i * cell
                rrect(c, X - 6, 414, cell, 252, 10, stroke='y', sw=2.5, a=km)
            text(c, 'same error rate · only one shared mistake', x0, 760, 26, 600, 'y', km)
        illustration(c, x0, 800, ramp(t, 6.0, 0.6))
        caption(c, t, 'The {y:rate} of errors is not the {y:identity} of errors.', 27.0, None, y=930, size=40)

class Verdicts(Scene):
    dur = 20.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'pop'), (5.5, 'pop'), (8.0, 'pop'), (12.0, 'chime')]
    CARDS = [('rare errors?', 'explain {y:part} of the gap', 3.0), ('close calls?', 'explain part of it, in {y:some settings}', 5.5),
             ('a nudge?', 'gets the {y:rate}, not the errors', 8.0)]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '05'), 'so', 'Three *excuses*')
        cw, gap = 532, 42
        for i, (lab, body, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, 360, cw, 260)
                    line(c, x + 36, 361, x + 156, 361, 'c', 1, 4, cap='butt')
                    text(c, lab, x + 36, 450, 44, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 36, 520, 30, cw - 72, t, t0 + 0.3, 0.03, 0.45)
        caption(c, t, 'For the name task in GPT-2, the gap {y:survives all three}.', 12.0, None, y=780, size=44)

class Discussion(Scene):
    dur = 18.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (10.0, 'chime')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '06'), 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('Is {y:exact} error agreement the right test, when so many mistakes are {y:near ties}?', 3.0),
                              ('Which {y:knock-out} would you trust: averages, other sentences, or learned constants?', 10.0)])

class End(EndCard):
    TAKE = 'Matching {y:how often} a model is wrong is not the same as matching {y:where}.'
    STATS = [('38%', 'Gemma’s circuit search set: mistakes', 'y'), ('9 → 37%', 'error agreement, errors weighted up', 'c'),
             ('94.9 vs 14.8', 'name task, after matching close calls', 'f')]
    NEXT = 'also in this series: the gap  ·  how the wrong name wins'
