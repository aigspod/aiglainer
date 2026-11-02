"""Video 3 of 3: how the wrong name wins. §4.2 and App. D (the 63-addition extension), Table 4 (fresh check),
§4.3 and Fig. 2 (the two omitted computations, with Fig. 2's attention percentages for its two example prompts), §5."""
from errkit import *
import scenes as part1
from scenes import ColdOpen, Circuit

class Gap(part1.Table1):
    chapter, NUM = 0, '01'

class Title(TitleCard):
    TITLE = 'How the wrong name *wins*'
    STICKY = ['circuits & errors', 'what was missing']

class Search(Scene):
    dur = 30.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (6.0, 'draw'), (12.0, 'pop'), (22.0, 'sweep')]
    NH, NP = 144, 25

    def __init__(self):
        rng = np.random.default_rng(11)
        allc = [(h, p) for h in range(self.NH) for p in range(self.NP)]
        idx = rng.permutation(len(allc))
        self.orig = set(allc[i] for i in idx[:26])
        self.added = [allc[i] for i in idx[26:89]]           # 63, positions illustrative

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '02'), 'the search', 'Looking for what’s *missing*')
        k = ramp(t, 4.0, 0.8)
        x0, y0, dx, dy = 150, 330, 11.2, 13
        add_k = ramp(t, 22.0, 2.5, e_io)
        n_add = int(round(add_k * len(self.added)))
        added = set(self.added[:n_add])
        if k > 0:
            for h in range(self.NH):
                for p in range(self.NP):
                    X, Y = x0 + h * dx, y0 + p * dy
                    if (h, p) in self.orig:
                        circle(c, X, Y, 4.2, fill='y', a=k)
                    elif (h, p) in added:
                        circle(c, X, Y, 4.6, fill='f', a=k, glow=5)
                    else:
                        circle(c, X, Y, 1.7, fill='muted', a=k * 0.45)
            kicker(c, '144 heads →', x0, y0 + self.NP * dy + 22, k, 'muted', 16)
            kicker(c, '↓ 25 positions in the sentence', x0, y0 - 26, k, 'muted', 16)
            illustration(c, x0 + self.NH * dx - 110, y0 + self.NP * dy + 22, k)
        kk = ramp(t, 6.0, 0.6)
        stat(c, 150, 790, '3,574', 'candidate additions (App. D)', 'ink', kk, 52)
        legend_item(c, 520, 770, 'y', 'the classic circuit (26)', kk, size=21)
        legend_item(c, 520, 810, 'f', f'added by the search ({n_add})' if t >= 22 else 'added by the search', ramp(t, 22.0, 0.6), size=21)
        for i, (sgn, s, colr) in enumerate((('+', 'reproduce the model’s mistakes', 'f'), ('−', 'lose ≤ 0.5 pt on the right pile', 'c'),
                                            ('−', 'add as little as possible', 'c'))):
            ki = ramp(t, 12.0 + i * 1.2, 0.6)
            text(c, sgn, 1180, 780 + i * 46, 34, 700, colr, ki)
            text(c, s, 1220, 780 + i * 46, 26, 500, 'ink', ki)
        kicker(c, 'the search’s objective (Eq. 5)', 1180, 735, ramp(t, 12.0, 0.6), 'muted', 16)

BARS = [('classic circuit', 14.22, 'c'), ('blanket nudge, same cost', 20.44, 'v'), ('random extensions (median)', 29.33, 'v'),
        ('the 63-addition extension', 75.11, 'y')]   # §4.2, 26,000-sentence test set, 225 model errors

class Result(Scene):
    dur = 34.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (6.0, 'pop'), (8.0, 'pop'), (13.0, 'tick'), (19.0, 'pop'), (26.0, 'tick')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '03'), 'the result', 'Three in *four*', sub='Error agreement on 26,000 fresh sentences (225 model mistakes) · §4.2')
        bx, sc, y0 = 620, 11.5, 400
        k0 = ramp(t, 4.0, 0.6)
        for v in (0, 25, 50, 75, 100):
            X = bx + v * sc
            line(c, X, y0 - 30, X, y0 + 4 * 95 - 20, 'line', k0 * 0.8, 1)
            text(c, f'{v}%', X, y0 - 40, 17, 500, 'muted', k0, 'center', kind='mono')
        order = [(0, 6.0), (3, 8.0), (1, 19.0), (2, 19.6)]
        for i, (j, t0) in enumerate(order):
            lab, v, colr = BARS[j]
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            yy = y0 + j * 95
            text(c, lab, bx - 24, yy + 30, 26, 600, colr if j in (0, 3) else 'ink', k, 'right')
            ww = v * sc * ramp(t, t0, 1.1, e_expo)
            if j == 2:
                rrect(c, bx + 17.33 * sc, yy + 4, (41.33 - 17.33) * sc * ramp(t, t0, 1.1, e_expo), 36, 6, fill='v', a=k, fa=k * 0.25)
                text(c, 'median 29.3% · range 17.3–41.3%', bx + 41.33 * sc + 14, yy + 30, 19, 500, 'v', k, kind='mono')
            rrect(c, bx, yy + 10, ww, 24, 5, fill=colr, a=k, fa=k * 0.9)
            if j != 2:
                text(c, f'{v:.1f}%', bx + ww + 12, yy + 30, 21, 600, colr, k, kind='mono')
        ks = ramp(t, 13.0, 0.7)
        stat(c, 150, 860, '99.34 → 98.93%', 'agreement on the right pile', 'f', ks, 46)
        stat(c, 760, 860, '+137', 'mistakes now reproduced', 'y', ramp(t, 14.0, 0.7), 46)
        stat(c, 1080, 860, '−106', 'correct sentences lost', 'c', ramp(t, 14.6, 0.7), 46)
        kc = ramp(t, 26.0, 0.7)
        if kc > 0:
            hand(c, 'a fresh 5,200-sentence check: −0.85 pt on the right pile, past the 0.5 limit', 150, 985, 28, 'pencil', kc, -2.0, ramp(t, 26.0, 1.2, e_lin))

S1 = ['Then,', 'Sara', 'and', 'Courtney', 'went', 'to', 'the', 'hospital.', 'Courtney', 'gave', 'a', 'bone', 'to']

class PathOne(Scene):
    dur = 40.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (10.0, 'draw'), (20.0, 'draw'), (25.0, 'pop'), (33.0, 'pop')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '04'), 'path one', 'Weaker *inhibition*', sub='Fig. 2A, one example prompt, redrawn')
        swap = ramp(t, 33.5, 0.8) if t >= 33 else 0
        words = list(S1)
        if swap > 0.5:
            words[11] = 'snack'
        xs = tokens(c, words, 150, 640, 40, t, 0.6, 1, {1: 'f', 3: 'v', 8: 'v', 11: 'g'}, 0.04)
        yb = 640 - 40
        k1 = ramp(t, 5.0, 0.7)
        if k1 > 0:
            # inhibition head 8.6, reading the second Courtney
            bxx, byy = 1080, 330
            with layer(c, k1):
                panel(c, bxx, byy, 330, 100, stroke='c')
                text(c, 'inhibition head 8.6', bxx + 24, byy + 42, 24, 600, 'c', 1)
                text(c, 'looks at the 2nd Courtney', bxx + 24, byy + 76, 19, 500, 'muted', 1)
            v = lerp(78.5, 28.3, ramp(t, 10.0, 2.5, e_io))
            arrow(c, bxx + 120, byy + 100, xs[8], yb, 'c', k1, 2 + 6 * v / 100)
            if getattr(self, 'PCT_RIGHT', False):      # shorts: keep the number inside a crop that starts at the box
                text(c, f'{v:.1f}%', bxx + 350, byy + 56, 30, 700, 'c', k1, kind='mono')
                note(c, 'circuit → extended', bxx + 350, byy + 84, k1 * ramp(t, 10.0, 0.6), 15)
            else:
                text(c, f'{v:.1f}%', bxx - 10, byy + 150, 30, 700, 'c', k1, 'right', kind='mono')
                note(c, 'circuit → extended', bxx - 10, byy + 178, k1 * ramp(t, 10.0, 0.6), 15, align='right')
        k2 = ramp(t, 10.0, 0.7)
        if k2 > 0:
            arrow(c, xs[11], 640 + 26, xs[11] + 40, 760, 'g', k2, 2.5)
            text(c, 'added heads read the object', xs[11] + 50, 790, 21, 600, 'g', k2)
        k3 = ramp(t, 20.0, 0.7)
        if k3 > 0:
            bxx, byy = 220, 330
            with layer(c, k3):
                panel(c, bxx, byy, 330, 100, stroke='y')
                text(c, 'name mover 9.9', bxx + 24, byy + 42, 24, 600, 'y', 1)
                text(c, 'looks at the 1st Courtney', bxx + 24, byy + 76, 19, 500, 'muted', 1)
            v = lerp(3.4, 15.7, ramp(t, 20.0, 2.0, e_io))
            arrow(c, bxx + 200, byy + 100, xs[3], yb, 'y', k3, 2 + 6 * v / 100)
            text(c, f'{v:.1f}%', bxx + 350, byy + 150, 30, 700, 'y', k3, kind='mono')
            text(c, '→ copies Courtney', bxx + 350, byy + 186, 21, 600, 'r', k3)
        for i, (big, small, colr, ti) in enumerate((('120 / 137', 'changed inhibition → classic circuit', 'c', 25.0),
                                                     ('107 / 137', 'bone → snack: right answer returns', 'g', 33.0),
                                                     ('68', 'of those vanish, inhibition held fixed', 'muted', 36.0))):
            stat(c, 150 + i * 570, 880, big, small, colr, ramp(t, ti, 0.7), 46)

S2 = ['Then,', 'Vanessa', 'and', 'Katie', 'were', 'thinking', 'about', 'going', 'to', 'the', 'garden.', 'Vanessa', 'wanted', 'to', 'give', 'a', 'ring', 'to']

class PathTwo(Scene):
    dur = 32.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (10.0, 'draw'), (24.0, 'pop')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '05'), 'path two', 'A different *label*', sub='Fig. 2B, one example prompt, redrawn')
        xs = tokens(c, S2, 150, 720, 34, t, 0.6, 1, {1: 'v', 3: 'f', 11: 'v'}, 0.03)
        k1 = ramp(t, 4.0, 0.7)
        if k1 > 0:
            for i, h in enumerate(['0.1', '0.3', '0.5', '0.6', '0.10']):
                X = xs[3] - 180 + i * 90
                rrect(c, X - 36, 800, 72, 44, 8, fill='f', stroke=None, a=k1, fa=k1 * 0.2)
                text(c, h, X, 830, 20, 600, 'f', k1, 'center', kind='mono')
                arrow(c, X, 800, xs[3], 732, 'f', k1 * 0.6, 1.6)
            text(c, 'first-layer heads at Katie, left out of the classic circuit', xs[3] - 216, 890, 21, 600, 'f', k1)
        for j, (lab, a0, a1, colr, ti) in enumerate((('name mover 9.9 (copies names)', 59.3, 53.4, 'y', 10.0),
                                                      ('negative name mover 10.7 (pushes names down)', 68.4, 71.9, 'r', 14.0))):
            k = ramp(t, ti, 0.7)
            if k <= 0:
                continue
            yy = 400 + j * 110
            v = lerp(a0, a1, ramp(t, ti + 0.8, 1.6, e_io))
            text(c, lab, 150, yy, 24, 600, colr, k)
            text(c, 'attention to Katie', 150, yy + 30, 18, 500, 'muted', k, kind='mono')
            rrect(c, 760, yy - 22, 8 * v, 34, 6, fill=colr, a=k, fa=k * 0.85)
            text(c, f'{a0:.1f}% → {v:.1f}%', 780 + 8 * 72, yy + 2, 24, 600, colr, k, kind='mono')
        kr = ramp(t, 20.0, 0.7)
        text(c, 'both favour Vanessa, the wrong name', 1420, 640, 26, 600, 'r', kr, 'center')
        kk = ramp(t, 24.0, 0.7)
        stat(c, 1260, 900, '35 / 137', 'patch the changed keys at Katie only', 'y', kk, 46)
        stat(c, 1260, 990 - 20, '', '', 'y', 0)
        note(c, 'anywhere else: 0', 1260, 990, kk, 18, 'muted')

class Meaning(Scene):
    dur = 32.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (4.5, 'pop'), (15.0, 'stamp_soft'), (22.0, 'pop')]
    CHECKS = ['split the sentences: model right / model wrong', 'report agreement on both piles, with their sizes',
              'on the wrong pile, count only the same wrong answer', 'check several circuit sizes, not just one']

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '06'), 'what it means', 'A cheap *check*', sub='The paper’s recommendations · §5')
        for i, s in enumerate(self.CHECKS):
            k = ramp(t, 4.5 + i * 1.8, 0.6)
            yy = 380 + i * 70
            rrect(c, MX, yy - 26, 34, 34, 6, stroke='f', sw=2, a=k)
            text(c, '✓', MX + 17, yy, 26, 700, 'f', k * ramp(t, 5.0 + i * 1.8, 0.4), 'center')
            text(c, s, MX + 60, yy, 28, 500, 'ink', k)
        pill(c, MX, 680, 'necessary, not sufficient', 'y', ramp(t, 15.0, 0.6), size=22)
        kc = ramp(t, 22.0, 0.8, e_expo)
        if kc > 0:
            with layer(c, kc):
                panel(c, 1050, 330, 750, 430, stroke='g')
                kicker(c, 'our extrapolation, not the paper’s', 1086, 376, 1, 'g', 16)
                text(c, 'a climate emulator', 1086, 440, 40, 400, 'ink', 1, kind='italic')
                rich(c, 'Does the explanation reproduce the emulator’s {f:skill}, or also its {r:known biases}, where it runs too warm or too wet?', 1086, 500, 28, 680, t, 22.3, 0.02, 0.4)

class Discussion(Scene):
    dur = 18.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (11.0, 'chime')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '06'), 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('The extension was found with the {y:mistakes in its objective}. What would convince you it found {y:mechanism}, not a fit?', 3.0),
                              ('What would this test look like for an {y:emulator} and its biases?', 11.0)])

class End(EndCard):
    TAKE = 'Explaining how a model {f:succeeds} isn’t explaining how it {r:fails}.'
    STATS = [('14 → 75%', 'mistakes reproduced, 63 additions', 'y'), ('120 / 137', 'path one: inhibition', 'c'), ('35 / 137', 'path two: the label on Katie', 'f')]
    NEXT = 'also in this series: the gap  ·  can the gap be explained away?'
