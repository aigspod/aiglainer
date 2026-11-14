"""Native 9:16 scenes for projects/epiplexity/shorts/* (seed, rules, mystery, order, pixels).

Each scene has `vertical = True` and draws in aiglainer.short.BOX (720 x 700), origin top-left. Big type: labels
>= 19 px, numbers >= 28 px. Built on the topic kit `epikit.py` (projects/epiplexity/videos/epiplexity), so every short
lists SOURCES = ['epiplexity/videos/epiplexity']. This module lives in shorts/ itself; each short's project.py puts that
folder on sys.path (two lines; see shorts/AGENTS.md).

Data: figure numbers come from the topic's data/ via epikit.tdata (fig3_eca, fig4_owf_chess, fig5_induction,
fig7_chess_ood, fig8_natural) and our compressor check (ours_compress.json, labelled "our check"). Cellular automata and
SHA-256 bits are computed exactly at render time; the mystery diagram, the chessboard and the bar in SeedJudges are
illustrations and say so. Nothing is drawn by eye.

Scenes, by short:
  seed     SeedStretch (a 7-byte seed -> 1,048,576 SHA-256 bits), SeedJudges (Shannon / our compressor check /
           a bounded learner, Thm 9)
  rules    RulesGrow (rules 15, 30, 54 from random rows), RulesFig3 (Fig. 3 S_T frontier, then each rule's bits split)
  mystery  MysteryLanes (the author's direction vs the reader's), MysteryBits (Fig. 5a's setup computed, Fig. 5b bars)
  order    OrderTwoWays (Fig. 4b's two orderings; Shannon's chain rule), OrderData (Fig. 4c S_T, Fig. 7 bars)
  pixels   PixelsTotal (Fig. 8a totals), PixelsStructure (Fig. 8a S_T, and the share that is structure)
"""
import hashlib
from epikit import *
from scenes3 import INFERNO          # Fig. 5's h = 0..5 colours, as the long video lifts them


def lab(c, s, x, y, a=1.0, align='left', color='muted', size=19):
    """A lowercase mono label at the shorts' minimum size."""
    note(c, s, x, y, a, size, color, align)


def sha_bits(n, seed=b'seed:42'):
    """SHA-256 in counter mode on a 7-byte seed: the generator of our compressor check (lab/compress_lab.py)."""
    out, ctr = bytearray(), 0
    while len(out) * 8 < n:
        out += hashlib.sha256(seed + ctr.to_bytes(8, 'big')).digest(); ctr += 1
    return np.unpackbits(np.frombuffer(bytes(out), np.uint8))[:n]


def col_chart(c, t, t0, vals, x0, yb, hmax, vmax, slot, bw, colors, labels, fmt, fs=32, stagger=0.25):
    """Vertical columns from a zero baseline (heights linear in the value), values on top, labels beneath."""
    k0 = ramp(t, t0, 0.6)
    if k0 <= 0:
        return
    line(c, x0 - 6, yb, x0 + slot * len(vals) + 6, yb, 'muted', k0, 1.6)
    for i, v in enumerate(vals):
        k = ramp(t, t0 + 0.15 + i * stagger, 0.9, e_expo)
        cx = x0 + slot * (i + 0.5)
        for j, s in enumerate(labels[i].split('\n')):
            text(c, s, cx, yb + 32 + j * 25, 21 if j == 0 else 19, 500, 'ink' if j == 0 else 'muted', k0, 'center',
                 kind='mono')
        if k <= 0:
            continue
        h = hmax * v / vmax * k
        rrect(c, cx - bw / 2, yb - h, bw, max(h, 2), 6, fill=colors[i], fa=0.92)
        text(c, fmt(v), cx, yb - h - 14, fs, 700, colors[i], k, 'center')


# =============================================================== seed

class SeedStretch(Scene):
    """A 7-byte seed (56 bits), SHA-256 run in counter mode, 1,048,576 bits out (a slice drawn; computed exactly)."""
    vertical = True
    dur = 13.0
    cues = [(0.3, 'pop'), (1.4, 'draw')]
    ROWS, COLS = 50, 96

    def __init__(self):
        self.seed = sha_bits(56, b'the seed')
        self.field = sha_bits(self.ROWS * self.COLS).reshape(self.ROWS, self.COLS)

    def draw(self, c, t):
        k0 = ramp(t, 0.2, 0.6)
        lab(c, 'the seed: 7 bytes = 56 bits', 38, 30, k0, color='y', size=21)
        lab(c, 'computed exactly', 682, 30, k0, 'right')
        for r in range(2):
            bits_row(c, self.seed[r * 28:(r + 1) * 28], 38, 48 + r * 24, 23, 1, 'y', t, 0.2 + r * 0.3, 0.012)
        kg = ramp(t, 0.9, 0.5)
        arrow(c, 360, 112, 360, 150, 'muted', kg, 2.5, 11, prog=ramp(t, 0.9, 0.4, e_io))
        if kg > 0:
            rrect(c, 170, 156, 380, 52, 26, fill='panel2', stroke='ink', sw=1.6, a=kg)
            text(c, 'SHA-256, again and again', 360, 190, 22, 500, 'ink', kg, 'center', kind='mono')
        arrow(c, 360, 214, 360, 246, 'muted', kg, 2.5, 11, prog=ramp(t, 1.2, 0.4, e_io))
        draw_eca(c, self.field, 40, 258, 640, t, 1.4, 15.0, color='g', bg_a=0.12, gap=0.22)
        # the counter: the rows drawn are a slice; the count runs to the full output
        kc = ramp(t, 1.4, 0.5)
        if kc > 0:
            p = ramp(t, 1.4, 5.0, e_io)
            n = int(round(1048576 * p ** 2.2))
            text(c, f'{n:,}', 360, 652, 56, 700, 'g', kc, 'center', glow=4)
            lab(c, 'bits out  ·  a slice drawn', 360, 688, kc, 'center')
        kr = ramp(t, 7.0, 0.6, e_back)
        if kr > 0:
            with layer(c, clamp(kr)):
                rrect(c, 110, 390, 500, 68, 14, fill='panel', fa=0.94, stroke='y', sw=2.2)
                text(c, 'no randomness added', 360, 435, 34, 700, 'y', 1, 'center')


class SeedJudges(Scene):
    """Three verdicts on the same file: Shannon (56 bits), our compressor check (1.000 bits per bit, like coin flips),
    a learner with limited compute (Thm 9: H_T ~ n, S_T ~ 0; the bar is an illustration)."""
    vertical = True
    dur = 24.0
    cues = [(0.4, 'pop'), (5.6, 'pop'), (11.6, 'pop'), (18.0, 'chime')]

    def __init__(self):
        self.comp = tdata('ours_compress.json')['results']
        self.seed = sha_bits(56, b'the seed')

    @staticmethod
    def card(c, y, h, k, colr):
        with xform(c, (1 - k) * -40, 0):
            panel(c, 10, y, 700, h, 1, stroke=colr)

    def draw(self, c, t):
        # 1. Shannon
        k = ramp(t, 0.4, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                self.card(c, 10, 190, k, 'v')
                lab(c, 'shannon', 36, 52, 1, color='v', size=22)
                text(c, '56 bits', 36, 124, 60, 700, 'ink', 1)
                lab(c, 'only the seed was random', 36, 172, 1, size=20)
                for r in range(7):
                    bits_row(c, self.seed[r * 8:(r + 1) * 8], 500, 34 + r * 21, 21, 1, 'y')
        # 2. compressors (our check)
        k = ramp(t, 5.6, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                self.card(c, 216, 224, k, 'c')
                lab(c, 'real compressors', 36, 258, 1, color='c', size=22)
                lab(c, 'our check', 684, 258, 1, 'right', 'y', 20)
                text(c, 'no shrink at all', 36, 312, 42, 700, 'ink', 1)
                for i, (name, key, colr) in enumerate((('this file', 'prng', 'g'), ('coin flips', 'coin', 'v'))):
                    yy = 332 + i * 42
                    v = self.comp[key]['xz']
                    kb = ramp(t, 6.2 + i * 0.4, 0.8, e_expo)
                    lab(c, name, 36, yy + 24, 1, color='ink', size=21)
                    rrect(c, 186, yy + 4, 360 * min(v, 1.05) * kb, 28, 5, fill=colr, fa=0.9)
                    text(c, f'{v:.3f}', 684, yy + 29, 28, 700, colr, kb, 'right', kind='mono')
                lab(c, 'xz · compressed bits per bit · 1,048,576 bits', 36, 426, 1, size=19)
        # 3. a learner with limited compute
        k = ramp(t, 11.6, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                self.card(c, 452, 196, k, 'g')
                lab(c, 'a learner with limited compute', 36, 494, 1, color='g', size=22)
                info_bar(c, 36, 516, 4, 648, 48, 1, labels=False, prog=ramp(t, 12.0, 1.2, e_expo))
                text(c, 'structure ≈ 0', 36, 600, 30, 700, S_COL, ramp(t, 12.8, 0.5))
                text(c, 'noise ≈ all', 684, 600, 30, 700, H_COL, ramp(t, 13.2, 0.5), 'right')
                lab(c, 'theorem 9  ·  bar: illustration', 684, 626, 1, 'right')
        kq = ramp(t, 18.0, 0.7, e_back)
        if kq > 0:
            stamp(c, 'same file, 3 answers', 360, 678, 'y', 1, kq, rot=-3, size=28)


# =============================================================== rules

class RulesGrow(Scene):
    """Rules 15, 30 and 54 run from random rows of 64 cells (computed from the rules); each is lit when named. On top,
    the rule in focus as a table (Wolfram's 8 neighbourhoods -> the new cell)."""
    vertical = True
    dur = 14.0
    cues = [(0.3, 'draw'), (5.0, 'pop'), (7.0, 'pop'), (9.2, 'pop')]
    RULES = [(15, 'repeats', 5.0), (30, 'static', 7.0), (54, 'gliders', 9.2)]
    W, N, SKIP = 48, 92, 16          # 48 cells, rows 16..108: seed 1 shows rule 54's gliders (the diagonal tracks of
                                     # dark triangles) crossing its periodic background clearly at this size

    def __init__(self):
        self.grids = {r: eca(r, self.W, self.SKIP + self.N, seed=1)[self.SKIP:] for r, _, _ in self.RULES}

    def draw(self, c, t):
        focus = 54
        for r, _, ti in self.RULES:
            if t >= ti:
                focus = r
        fc = FIG3_COLORS[str(focus)]
        k0 = ramp(t, 0.2, 0.6)
        lab(c, f'rule {focus}, the whole program: 8 cases', 360, 26, k0, 'center', fc, 21)
        cell, gap = 21, 12
        w = 8 * 3 * cell + 7 * gap
        rule_icons(c, focus, 360 - w / 2, 46, cell, k0, t, 0.3, fc, show_bits=False, gap=gap)
        gh = self.N * 212 / self.W
        for i, (r, desc, ti) in enumerate(self.RULES):
            x = 18 + i * 236
            colr = FIG3_COLORS[str(r)]
            lit = ramp(t, ti, 0.5)
            draw_eca(c, self.grids[r], x, 136, 212, t, 0.6 + i * 0.15, 36, color=colr, a=k0, bg_a=0.08, frame=False)
            rrect(c, x - 6, 130, 224, gh + 12, 8, stroke=colr if lit > 0 else 'line', sw=1.2 + 2.0 * lit, a=k0,
                  glow=8 * lit)
            text(c, f'rule {r}', x + 106, 594, 38, 400, colr, k0, 'center', kind='italic')
            text(c, desc, x + 106, 640, 30, 700, 'ink', lit, 'center')
        lab(c, EXACT + '  ·  time runs down', 360, 690, ramp(t, 1.0, 0.6), 'center')


class RulesFig3(Scene):
    """Fig. 3: epiplexity S_T along the best-two-part-code frontier vs compute (fig3_eca.json), rules 15/30/54; then each
    rule's bits at the largest budget split into structure and randomness (as shares; the totals are printed)."""
    vertical = True
    dur = 26.0
    cues = [(0.3, 'draw'), (5.6, 'draw'), (9.2, 'draw'), (13.2, 'draw'), (19.4, 'pop')]
    T0 = {'15': 5.6, '30': 9.2, '54': 13.2}
    WORD = {'15': 'learned fast, holds little', '30': 'stays random', '54': 'keeps paying off'}
    SPLIT = 19.4

    def __init__(self):
        self.d = tdata('fig3_eca.json')['panels']

    def draw(self, c, t):
        ka = ramp(t, 0.3, 0.7)
        ax = LogAxes(80, 74, 500, 300, (11.8, 17.4), (0, 6.6))
        ax.draw(c, ka, (12, 14, 16), (0, 2, 4, 6), yfmt=lambda v: f'{v:g}', fs=21)
        text(c, 'structure learned, Sₜ (millions of bits)', 14, 36, 23, 500, 'ink', ka)
        lab(c, 'compute (FLOPs)', 580, 440, ka, 'right')
        ep = self.d['epiplexity']['frontier']
        for r in ('15', '30', '54'):
            f = ep[r]
            colr = FIG3_COLORS[r]
            ys = np.array(f['y']) / 1e6
            curve_reveal(c, ax, f['x'], ys, colr, t, self.T0[r], 2.0 if r == '54' else 1.2, w=4, dots=True, r=6)
            X, Y = ax.px(f['x'][-1], ys[-1])
            dy = {'15': -2, '30': 22, '54': 10}[r]
            text(c, r, float(X) + 16, float(Y) + dy, 30, 700, colr, ramp(t, self.T0[r] + 0.8, 0.5))
        ks = ramp(t, self.SPLIT, 0.6)
        # what each rule does, in words, under the chart
        for i, r in enumerate(('15', '30', '54')):
            k = ramp(t, self.T0[r] + 0.4, 0.5) * (1 - ks)
            if k > 0:
                text(c, f'rule {r}', 30, 514 + i * 52, 30, 400, FIG3_COLORS[r], k, kind='italic')
                text(c, self.WORD[r], 180, 514 + i * 52, 30, 600, 'ink', k)
        # each rule's bits at the largest budget: structure | randomness, as shares, with the total
        if ks > 0:
            lab(c, 'at the largest budget, each rule’s bits:', 14, 482, ks, color='ink', size=21)
            tot = self.d['two_part']['frontier']
            for i, r in enumerate(('15', '30', '54')):
                s = ep[r]['y'][-1]
                h = self.d['entropy']['frontier'][r]['y'][-1]
                yy = 502 + i * 56
                kk = ramp(t, self.SPLIT + 0.2 + i * 0.3, 0.6)
                text(c, r, 14, yy + 32, 30, 700, FIG3_COLORS[r], kk)
                frac = s / (s + h)
                info_bar(c, 66, yy + 6, 380 * frac, 380 * (1 - frac), 36, kk, labels=False,
                         prog=ramp(t, self.SPLIT + 0.2 + i * 0.3, 1.0, e_expo), min_w=4)
                text(c, f'{sci(tot[r]["y"][-1])} bits', 706, yy + 33, 26, 600, 'ink', kk, 'right')
            info_bar(c, 14, 662, 30, 0, 18, ks, labels=False)
            lab(c, 'structure', 52, 678, ks, color=S_COL, size=20)
            info_bar(c, 186, 662, 0, 30, 18, ks, labels=False)
            lab(c, 'randomness', 224, 678, ks, color=H_COL, size=20)
        lab(c, 'data: Fig. 3 · arXiv:2601.03220', 706, 686, ka * (1 - ks), 'right')
        lab(c, 'data: Fig. 3', 706, 678, ks, 'right')


# =============================================================== mystery

class MysteryLanes(Scene):
    """Sutskever's murder mystery (§5.3, quoted in the paper): the author can go culprit -> clues; the reader has to go
    clues -> culprit. The suspect, name and clues are an illustration."""
    vertical = True
    dur = 14.0
    cues = [(0.3, 'pop'), (4.0, 'draw'), (8.0, 'draw')]
    CLUES = ['muddy boots', 'a torn letter', 'a stopped clock']

    def draw(self, c, t):
        k0 = ramp(t, 0.2, 0.6)
        ka = ramp(t, 4.0, 0.6)          # the author's arrow
        kr = ramp(t, 8.0, 0.6)          # the reader's arrow
        lab(c, 'the culprit', 150, 28, k0, 'center', 'ink', 22)
        lab(c, 'the clues', 572, 28, k0, 'center', 'ink', 22)
        # the culprit card: a silhouette and a name (known to the author, a question for the reader)
        if k0 > 0:
            panel(c, 40, 48, 220, 300, k0, stroke='line')
            circle(c, 150, 140, 46, fill='pencil', a=k0 * 0.85)
            pth = skia.Path()
            pth.moveTo(70, 300); pth.quadTo(70, 200, 150, 196); pth.quadTo(230, 200, 230, 300); pth.close()
            c.drawPath(pth, paint('pencil', k0 * 0.85))
            kq = kr * (0.75 + 0.25 * math.sin(max(t - 8.0, 0) * 4))
            name_a = k0 * (1 - kr)
            text(c, 'the gardener', 150, 334, 26, 700, 'f', name_a * ka, 'center')
            text(c, '?', 150, 168, 92, 700, 'y', kq, 'center', glow=10)
            text(c, '? ? ?', 150, 334, 28, 700, 'y', kr, 'center')
        for i, s in enumerate(self.CLUES):
            k = ramp(t, 0.5 + i * 0.25, 0.5)
            if k <= 0:
                continue
            y = 48 + i * 104
            panel(c, 446, y, 252, 88, k, r=12, stroke='line')
            text(c, s, 572, y + 54, 25, 500, 'ink', k, 'center')
        # the two directions
        if ka > 0:
            arrow(c, 272, 128, 432, 128, 'f', ka, 4, 16, prog=ramp(t, 4.0, 0.6, e_io), glow=6)
            text(c, 'write', 352, 112, 24, 700, 'f', ka, 'center', kind='mono')
        if kr > 0:
            arrow(c, 432, 268, 272, 268, 'y', kr, 4, 16, prog=ramp(t, 8.0, 0.6, e_io), glow=6)
            text(c, 'deduce', 352, 304, 24, 700, 'y', kr, 'center', kind='mono')
        if ka > 0:
            text(c, 'the author', 30, 410, 34, 400, 'f', ka, kind='italic')
            text(c, 'picks the culprit first', 236, 410, 27, 500, 'ink', ka)
        if kr > 0:
            text(c, 'the reader', 30, 470, 34, 400, 'y', kr, kind='italic')
            text(c, 'must work it out', 236, 470, 27, 500, 'ink', kr)
        kq = ramp(t, 9.0, 0.7)
        text(c, '“If the model can predict [the name] then it', 360, 556, 22, 400, 'muted', kq, 'center', kind='italic')
        text(c, 'must have figured out [who did it]”', 360, 586, 22, 400, 'muted', kq, 'center', kind='italic')
        lab(c, 'Ilya Sutskever, 2019 · quoted in the paper', 360, 622, kq, 'center')
        lab(c, ILLUS, 360, 686, k0, 'center')


class MysteryBits(Scene):
    """§5.3.1, hard induction: Z = 32 random bits, f = 4 steps of rule 30, the first h bits hidden (computed from the
    rule, after Fig. 5a); 2^h candidate fills (the paper's reading of the compute cost); Fig. 5b's measured epiplexity
    for h = 0..5 (fig5_induction.json)."""
    vertical = True
    dur = 26.0
    cues = [(0.3, 'draw'), (6.5, 'tick'), (12.5, 'draw'), (18.5, 'chime')]

    def __init__(self):
        self.e = tdata('fig5_induction.json')['fig5b_hard']['epiplexity']
        z = np.random.default_rng(17).integers(0, 2, 32)
        self.rows = eca(30, 32, 5, init=z)

    def hidden(self, t):
        if t < 6.5:
            return 2
        return int(clamp(1 + (t - 6.5) / 1.0, 1, 5))

    def draw(self, c, t):
        k0 = ramp(t, 0.2, 0.6)
        h = self.hidden(t)
        cell, x0 = 21, 24
        lab(c, 'Z: 32 random bits', x0, 28, k0, color='ink', size=21)
        lab(c, EXACT, 696, 28, k0, 'right')
        z = self.rows[0]
        for j in range(32):
            hid = j < h
            rrect(c, x0 + j * cell, 42, cell * 0.84, cell * 0.84, 4, fill='faint' if hid else ('y' if z[j] else 'faint'),
                  fa=k0 * (0.9 if hid else (1 if z[j] else 0.45)))
            if hid:
                text(c, '?', x0 + j * cell + cell * 0.42, 42 + cell * 0.74, 18, 700, 'r', k0, 'center', kind='mono')
        kf = ramp(t, 1.4, 0.6)
        draw_eca(c, self.rows[1:], x0, 76, 32 * cell, t, 1.4, 6, color=FIG3_COLORS['30'], a=kf, bg_a=0.08, frame=False)
        lab(c, 'rule 30, 4 steps → predict the last row', x0, 196, kf, color=FIG3_COLORS['30'], size=21)
        # the hidden bits and the guesses they cost
        kh = ramp(t, 3.5, 0.6)
        if kh > 0:
            panel(c, 14, 218, 692, 72, kh, r=14, stroke='r')
            text(c, f'{h} hidden', 40, 266, 34, 700, 'r', kh)
            text(c, f'→  {2 ** h} possible fills', 682, 266, 34, 700, 'ink', kh, 'right')
        # every fill of the hidden bits, as chips (all 2^h of them; computed, not data)
        kg = kh * (1 - ramp(t, 12.0, 0.5))
        if kg > 0:
            n = 2 ** h
            cw, gap_ = 15, 3
            for i in range(n):
                q, r = divmod(i, 8)
                x, y = 30 + q * 172, 330 + r * 36
                kk = kg * ramp(t, 3.6 + 0.02 * i if i < 4 else 6.6 + 0.02 * i, 0.3)
                if kk <= 0:
                    continue
                w = h * (cw + gap_) + 18
                rrect(c, x, y, w, 28, 8, fill='panel2', stroke='r', sw=1.2, a=kk)
                for j in range(h):
                    on = (i >> (h - 1 - j)) & 1
                    rrect(c, x + 9 + j * (cw + gap_), y + 6, cw, cw + 1, 3, fill='y' if on else 'faint',
                          fa=kk * (1 if on else 0.6))
            lab(c, 'each must be tried against the output', 360, 640, kg, 'center', 'ink', 21)
        # Fig. 5b: measured epiplexity vs h, from zero
        ke = ramp(t, 12.5, 0.7)
        if ke > 0:
            text(c, 'structure learned (millions of bits)', 14, 340, 23, 500, 'ink', ke)
            col_chart(c, t, 12.5, [v / 1e6 for v in self.e['value']], 30, 600, 210, 6.0, 110, 76, INFERNO,
                      [str(hh) for hh in self.e['h']], lambda v: f'{v:.1f}', fs=30, stagger=0.2)
            lab(c, 'hidden bits', 360, 660, ke, 'center', 'ink', 20)
        lab(c, 'data: Fig. 5b · arXiv:2601.03220', 360, 690, ke, 'center')


# =============================================================== order

BOARD = {'e1': 'w:♚', 'g1': 'w:♜', 'd4': 'w:♟', 'e5': '♟', 'c6': '♞', 'f3': 'w:♞', 'e8': '♚', 'a8': '♜',
         'b5': 'w:♝', 'd8': '♛', 'd1': 'w:♛', 'h7': '♟', 'a2': 'w:♟'}          # the long video's illustration board
MOVES = '1. e4 e5  2. Nf3 Nc6 …'


class OrderTwoWays(Scene):
    """Fig. 4b: the same Lichess games written moves-then-board (forward) or board-then-moves (reverse); Shannon's chain
    rule says the total is the same either way (§5.2). The board is an illustration."""
    vertical = True
    dur = 16.0
    cues = [(0.3, 'pop'), (4.0, 'draw'), (8.0, 'draw'), (11.5, 'pop')]

    def lane(self, c, y, colr, name, first_board, k):
        text(c, name, 14, y + 42, 23, 700, colr, k, kind='mono')
        boxes = [('board', 120), ('moves', 330)] if first_board else [('moves', 330), ('board', 120)]
        x = 150
        for j, (kind, w) in enumerate(boxes):
            rrect(c, x, y, w, 66, 12, fill='panel2', stroke=colr, sw=1.8, a=k)
            if kind == 'board':
                chessboard(c, x + 33, y + 6, 54, k, None)
            else:
                text(c, MOVES, x + 18, y + 42, 22, 500, 'ink', k, kind='mono')
            if j == 0:
                arrow(c, x + w + 8, y + 33, x + w + 50, y + 33, colr, k, 3, 12)
            x += w + 58

    def draw(self, c, t):
        k0 = ramp(t, 0.2, 0.7)
        mv = ramp(t, 1.0, 0.8, e_io)
        chessboard(c, 220, 20, 280, k0, BOARD, arrows=[('f3', 'e5', 'y', mv)])
        lab(c, ILLUS, 500, 324, k0, 'right')
        self.lane(c, 352, ORDER_COLORS['forward'], 'forward', False, ramp(t, 4.0, 0.7))
        self.lane(c, 446, ORDER_COLORS['reverse'], 'reverse', True, ramp(t, 8.0, 0.7))
        ks = ramp(t, 11.5, 0.7)
        if ks > 0:
            panel(c, 14, 546, 692, 112, ks, r=14, stroke='v')
            text(c, 'H(X) + H(Y|X) = H(Y) + H(X|Y)', 360, 594, 30, 600, 'ink', ks, 'center', kind='mono')
            lab(c, 'shannon: the same total, in either order', 360, 634, ks, 'center', 'v', 21)


class OrderData(Scene):
    """Fig. 4c: epiplexity S_T vs compute, forward vs reverse (fig4_owf_chess.json); §6.1 / Fig. 7: after fine-tuning,
    puzzle accuracy 25.8% vs 25.9%, centipawn accuracy 21.0% vs 28.2% (fig7_chess_ood.json), bars from zero."""
    vertical = True
    dur = 27.0
    cues = [(0.4, 'draw'), (12.5, 'pop'), (17.0, 'pop'), (22.0, 'chime')]

    def __init__(self):
        self.c4 = tdata('fig4_owf_chess.json')['fig4c_chess']['panels']['epiplexity']
        self.f7 = tdata('fig7_chess_ood.json')['bars']

    def draw(self, c, t):
        F, R = ORDER_COLORS['forward'], ORDER_COLORS['reverse']
        ka = ramp(t, 0.3, 0.7)
        ax = LogAxes(80, 70, 470, 220, (14.9, 18.9), (0, 3.0))
        ax.draw(c, ka, (15, 16, 17, 18), (0, 1, 2, 3), yfmt=lambda v: f'{v:g}', fs=21)
        text(c, 'structure learned, Sₜ (×10⁸ bits)', 14, 34, 23, 500, 'ink', ka)
        lab(c, 'compute (FLOPs)', 550, 352, ka, 'right')
        for name, colr, t0 in (('forward', F, 0.6), ('reverse', R, 1.8)):
            d = self.c4[name]
            ys = np.array(d['y']) / 1e8
            curve_reveal(c, ax, d['x'], ys, colr, t, t0, 1.8, w=4, dots=True, r=5)
            X, Y = ax.px(d['x'][-1], ys[-1])
            text(c, name, float(X) + 14, float(Y) + (16 if name == 'forward' else 2), 24, 700, colr,
                 ramp(t, t0 + 1.6, 0.5), kind='mono')
        # while the bars wait: the gap at the largest budget (Fig. 4c), and why (illustration)
        kq = ramp(t, 3.5, 0.6) * (1 - ramp(t, 12.0, 0.5))
        if kq > 0:
            gain = self.c4['reverse']['y'][-1] / self.c4['forward']['y'][-1] - 1
            text(c, f'+{gain * 100:.0f}%', 30, 452, 60, 700, R, kq)
            text(c, 'more structure in reverse', 230, 422, 26, 600, 'ink', kq)
            lab(c, 'final points of Fig. 4c', 230, 452, kq)
        ki = ramp(t, 7.5, 0.6) * (1 - ramp(t, 12.0, 0.5))
        if ki > 0:
            chessboard(c, 40, 498, 120, ki, BOARD)
            arrow(c, 180, 558, 300, 558, R, ki, 3.5, 14, prog=ramp(t, 7.8, 0.6, e_io))
            text(c, 'infer', 240, 540, 22, 700, R, ki, 'center', kind='mono')
            rrect(c, 316, 526, 380, 64, 12, fill='panel2', stroke=R, sw=1.8, a=ki)
            text(c, '1. ?  ?   2. ?  ?   …', 336, 568, 24, 500, 'ink', ki, kind='mono')
            lab(c, ILLUS, 696, 640, ki, 'right')
        # Fig. 7, from zero
        groups = [('cp_acc', 'judging a position', 'centipawn accuracy', 17.0), ('puzzle_acc', 'puzzles', 'accuracy', 12.5)]
        for j, (key, title, sub, ti) in enumerate(sorted(groups, key=lambda g: g[3])):
            kg = ramp(t, ti, 0.6)
            if kg <= 0:
                continue
            y = 400 + j * 130
            text(c, title, 14, y, 26, 700, 'ink', kg)
            lab(c, sub, 706, y, kg, 'right')
            for q, (name, colr) in enumerate((('forward', F), ('reverse', R))):
                v = self.f7[key][name]
                kk = ramp(t, ti + 0.2 + q * 0.3, 0.9, e_expo)
                lab(c, {'forward': 'fwd', 'reverse': 'rev'}[name], 14, y + 38 + q * 44, kg, color=colr, size=21)
                bw = 480 / 0.35 * v * kk
                rrect(c, 70, y + 16 + q * 44, max(bw, 2), 32, 6, fill=colr, fa=0.9 * kg)
                text(c, f'{v * 100:.1f}%', 70 + bw + 12, y + 42 + q * 44, 28, 700, colr, kk)
        lab(c, 'after fine-tuning  ·  bars start at zero', 360, 662, ramp(t, 12.5, 0.6), 'center')
        lab(c, 'data: Fig. 4c, Fig. 7 · arXiv:2601.03220', 360, 690, ka, 'center')


# =============================================================== pixels

PIX_NAMES = ['OWText', 'Chess (R)', 'Chess', 'CIFAR-5M']
PIX_LABELS = ['web text', 'chess\nreversed', 'chess', 'images\nCIFAR-5M']
PIX_COLORS = ['#2fbf95', '#4f9fe0', '#8cc63f', '#9a97a6']     # Fig. 8a's hues, lifted for the dark ground


class PixelsTotal(Scene):
    """Fig. 8a: total information S_T + H_T per 5B tokens (§6.2; the caption's 1B is a typo, see the topic AGENTS.md)."""
    vertical = True
    dur = 12.0
    cues = [(0.4, 'draw'), (5.2, 'pop')]

    def __init__(self):
        self.b = tdata('fig8_natural.json')['fig8a_requential']['bars']

    def draw(self, c, t):
        k0 = ramp(t, 0.3, 0.6)
        text(c, 'total information (billions of bits)', 14, 34, 23, 500, 'ink', k0)
        lab(c, '5 billion tokens of each', 14, 66, k0)
        vals = [self.b[n]['S_T_plus_H_T'] / 1e9 for n in PIX_NAMES]
        col_chart(c, t, 0.4, vals, 20, 590, 450, 25.0, 170, 112, PIX_COLORS, PIX_LABELS, lambda v: f'{v:.1f}')
        kc = ramp(t, 5.2, 0.7, e_back)
        if kc > 0:
            r = vals[3] / vals[0]
            with layer(c, clamp(kc)):
                text(c, f'{r:.1f}× the bits', 260, 250, 40, 700, PIX_COLORS[3], 1, 'center')
                text(c, 'of web text', 260, 292, 28, 500, 'ink', 1, 'center')
                arrow(c, 410, 262, 520, 210, PIX_COLORS[3], 1, 3, 13, prog=ramp(t, 5.4, 0.5, e_io))
        lab(c, 'data: Fig. 8a · arXiv:2601.03220', 360, 690, k0, 'center')


class PixelsStructure(Scene):
    """Fig. 8a: epiplexity S_T alone (requential, 6e18 FLOPs, models up to 160M parameters); the ranking flips. Then the
    share of each that is structure: web text 4.1%, CIFAR-5M 0.4% (over 99% random, as §6.2 says)."""
    vertical = True
    dur = 25.0
    cues = [(0.4, 'draw'), (6.0, 'pop'), (13.0, 'draw'), (19.0, 'chime')]

    def __init__(self):
        self.b = tdata('fig8_natural.json')['fig8a_requential']['bars']

    def draw(self, c, t):
        k0 = ramp(t, 0.3, 0.6)
        text(c, 'structure a model can learn (×10⁸ bits)', 14, 34, 23, 500, 'ink', k0)
        vals = [self.b[n]['S_T'] / 1e8 for n in PIX_NAMES]
        col_chart(c, t, 0.4, vals, 20, 400, 300, 3.3, 170, 112, PIX_COLORS, PIX_LABELS, lambda v: f'{v:.1f}', stagger=0.3)
        kr = ramp(t, 6.0, 0.6, e_back)
        if kr > 0:
            stamp(c, 'ranking flips', 560, 120, 'y', 1, kr, rot=-4, size=28)
        ksh = ramp(t, 13.0, 0.6)
        if ksh > 0:
            for i, n in enumerate(('OWText', 'CIFAR-5M')):
                b = self.b[n]
                frac = b['S_T'] / b['S_T_plus_H_T']
                y = 528 + i * 76
                kk = ramp(t, 13.0 + i * 0.5, 0.6)
                nm = 'web text' if i == 0 else 'images'
                text(c, nm, 14, y, 24, 700, PIX_COLORS[PIX_NAMES.index(n)], kk, kind='mono')
                text(c, f'{frac * 100:.1f}% structure', 706, y, 28, 700, S_COL, kk, 'right')
                info_bar(c, 14, y + 12, 692 * frac, 692 * (1 - frac), 34, kk, labels=False,
                         prog=ramp(t, 13.0 + i * 0.5, 1.0, e_expo), min_w=4)
        lab(c, 'data: Fig. 8a · requential, 6 × 10¹⁸ FLOPs', 360, 690, k0, 'center')
