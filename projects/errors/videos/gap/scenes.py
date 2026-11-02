"""Video 1 of 3: the gap. Circuits, the IOI circuit (Table 8), knock-outs, the two piles (Eq. 4), Table 1."""
from errkit import *

SENT = ['Sara', 'and', 'Courtney', 'went', 'to', 'the', 'hospital.', 'Courtney', 'gave', 'a', 'bone', 'to', '…']

class ColdOpen(Scene):
    dur = 22.0
    fade_in = 0.3
    cues = [(0.4, 'whoosh_soft'), (5.2, 'pop'), (10.2, 'pop')]

    def draw(self, c, t):
        cols = {}
        if t > 3.5:
            cols = {0: 'f', 2: 'v', 7: 'v'}
        xs = tokens(c, SENT, 170, 400, 50, t, 0.5, 1, cols, 0.12)
        # the answer slot
        ka = ramp(t, 5.0, 0.7, e_expo)
        if ka > 0:
            with layer(c, ka):
                panel(c, 170, 520, 700, 170)
                kicker(c, 'gpt-2 says', 206, 568, 1, 'muted', 18)
                text(c, 'Courtney', 206, 645, 64, 700, 'r', 1)
                text(c, '✗  one of its rare mistakes', 530, 640, 26, 500, 'r', 1)
        kb = ramp(t, 10.0, 0.7, e_expo)
        if kb > 0:
            with layer(c, kb):
                panel(c, 1000, 520, 680, 170, stroke='y')
                kicker(c, 'the circuit that should explain it says', 1036, 568, 1, 'muted', 18)
                text(c, 'Sara', 1036, 645, 64, 700, 'y', 1)
                text(c, '✓  the right answer', 1230, 640, 26, 500, 'y', 1)
        caption(c, t, 'The circuit is {y:right} where the model is {r:wrong}. Is that a good {y:explanation}?', 15.0, None, y=840, size=44)

class Title(TitleCard):
    pass

class Circuit(Scene):
    dur = 32.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (11.0, 'draw')]
    STORY = [('notice the repeat', 'duplicate-token, induction and previous-token heads see that {f:Courtney} appears twice', 'f', 17.0),
             ('inhibit it', '{c:inhibition heads} tell later heads: don’t copy the repeated name', 'c', 21.0),
             ('copy the other name', '{y:name movers} look back and copy {y:Sara} into the answer', 'y', 25.5)]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '01'), 'circuits', 'What is a *circuit*?')
        k = ramp(t, 4.0, 0.9)
        head_grid(c, 230, 330, 46, t, t_lit=11.0, a=k)
        kicker(c, 'gpt-2 small: 144 attention heads', 230, 905, k, 'muted', 17)
        k2 = ramp(t, 11.0, 0.8)
        if k2 > 0:
            text(c, '26 heads, mapped by hand (Wang et al., 2023)', 230, 950, 22, 600, 'y', k2)
        for i, (lab, body, colr, t0) in enumerate(self.STORY):
            kk = ramp(t, t0, 0.8, e_expo)
            if kk <= 0:
                continue
            yy = 330 + i * 190
            with layer(c, kk):
                with xform(c, (1 - kk) * 30, 0):
                    panel(c, 880, yy, 920, 160)
                    line(c, 916, yy + 1, 1036, yy + 1, colr, 1, 4, cap='butt')
                    text(c, f'{i + 1}.  {lab}', 916, yy + 62, 34, 400, 'ink', 1, kind='italic')
                    rich(c, body, 916, yy + 112, 26, 850, t, t0 + 0.3, 0.02, 0.4)

class Knockout(Scene):
    dur = 32.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (5.0, 'pop'), (14.0, 'tick'), (21.0, 'pop')]
    CARDS = [('average', 'its mean output over many other sentences', 'mean ablation'),
             ('another sentence', 'its output on a sentence with three unrelated names', 'resample ablation'),
             ('a learned constant', 'fitted to keep the circuit close to the model', 'optimal ablation')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '01'), 'how circuits are tested', 'Knock out the *rest*')
        k = ramp(t, 0.6, 0.8)
        head_grid(c, 180, 330, 34, t, t_lit=0.0, a=k, dim_rest=ramp(t, 2.0, 1.5), labels=False)
        note(c, 'circuit heads kept · the other 118 replaced', 180, 760, k, 16)
        for i, (big, small, tag) in enumerate(self.CARDS):
            kk = ramp(t, 5.0 + i * 0.6, 0.7, e_expo)
            if kk <= 0:
                continue
            x = 680 + i * 380
            with layer(c, kk):
                panel(c, x, 330, 350, 230)
                kicker(c, tag, x + 28, 372, 1, 'muted', 15)
                text(c, big, x + 28, 430, 34, 400, 'ink', 1, kind='italic')
                rich(c, small, x + 28, 476, 22, 300, t, 5.3 + i * 0.6, 0.02, 0.4, base='muted')
        # faithfulness: average preference for the right name, circuit vs model
        kf = ramp(t, 14.0, 0.8)
        if kf > 0:
            with layer(c, kf):
                panel(c, 680, 600, 1110, 300)
                kicker(c, 'faithfulness: average preference for the right name', 712, 645, 1, 'muted', 16)
                g = ramp(t, 15.0, 1.4, e_expo)
                for j, (lab, v, colr) in enumerate((('full model', 1.0, 'ink'), ('classic circuit', 0.956, 'y'))):
                    yy = 690 + j * 70
                    text(c, lab, 900, yy + 26, 24, 600, colr, 1, 'right')
                    rrect(c, 930, yy, 760 * v * g, 34, 6, fill=colr, a=1, fa=0.8)
                kv = ramp(t, 21.0, 0.7)
                text(c, '0.956', 1700, 866, 44, 700, 'y', kv, 'right', kind='mono')
                text(c, 'Table 1 · mean ablation', 712, 866, 17, 500, 'muted', kv, kind='mono')
        caption(c, t, 'But the model is right on {f:more than 99%} of these sentences: the average is mostly an average over {f:successes}.', 26.0, None, y=985, size=31)

class TwoPiles(Scene):
    dur = 34.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (6.0, 'draw'), (11.0, 'sweep'), (16.5, 'pop'), (22.0, 'pop')]
    NX, NY = 50, 20

    def __init__(self):
        rng = np.random.default_rng(4)
        n = self.NX * self.NY
        self.err = set(rng.choice(n, 9, replace=False).tolist())   # ~0.9%: IOI test census, 884 of 100,000 (Table 2)

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '02'), 'the new test', 'Two *piles*')
        k = ramp(t, 6.0, 0.8)
        split = ramp(t, 11.0, 2.0, e_io)
        cell = 15
        x0, y0 = 160, 340
        ei = 0
        for i in range(self.NX * self.NY):
            gx, gy = i % self.NX, i // self.NX
            px, py = x0 + gx * cell, y0 + gy * cell
            if i in self.err:
                tx, ty = 1300 + (ei % 3) * 60, 400 + (ei // 3) * 60
                ei += 1
                X, Y = lerp(px, tx, split), lerp(py, ty, split)
                circle(c, X, Y, lerp(4.5, 16, split), fill='r', a=k, glow=4)
            else:
                X = lerp(px, px * 0.85 + 10, split)
                circle(c, X, py, 4.2, fill='f', a=k * 0.75)
        kicker(c, '1,000 test sentences · fewer than 1% wrong (Table 2: 884 of 100,000)', 160, 690, k, 'muted', 16)
        ks = ramp(t, 13.0, 0.7)
        text(c, 'pile 1: the model is right', 160, 300, 26, 600, 'f', ks)
        text(c, 'pile 2: the model is wrong', 1300, 340, 26, 600, 'r', ks)
        for i, (lab, body, colr, ti) in enumerate((('correct agreement', 'on pile 1, the circuit is {f:also right}', 'f', 16.5),
                                                   ('error agreement', 'on pile 2, the circuit makes the {c:exact same mistake}', 'c', 22.0))):
            kk = ramp(t, ti, 0.8, e_expo)
            if kk <= 0:
                continue
            with layer(c, kk):
                panel(c, 160 + i * 820, 740, 780, 150)
                text(c, lab, 196 + i * 820, 800, 34, 400, colr, 1, kind='italic')
                rich(c, body, 196 + i * 820, 850, 26, 720, t, ti + 0.3, 0.02, 0.4)
        caption(c, t, 'Only two possible answers here: a circuit that misses the mistake gives the {y:right name} instead.', 28.0, None, y=985, size=30)

IOI_MEAN = [('classic circuit (26 heads)', 99.5, 15.2, 0.956), ('ACDC (402 edges)', 97.3, 11.8, 1.167),
            ('EAP-IG (6,498 edges)', 99.1, 41.7, 0.987), ('edge pruning (256–268 edges)', 98.3, 11.4, 1.486)]   # Table 1, IOI, mean
IOI_RES = [('classic circuit (26 heads)', 91.2, 40.6, 0.644), ('ACDC (402 edges)', 91.5, 24.8, 0.887),
           ('EAP-IG (6,498 edges)', 97.8, 51.4, 0.905), ('edge pruning (256–268 edges)', 93.7, 17.6, 1.002)]    # Table 1, IOI, resample

class Table1(Scene):
    dur = 36.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (9.0, 'pop'), (27.0, 'sweep')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '03'), 'results', 'The *gap*', sub='Indirect object identification, GPT-2 small · Table 1')
        tag = 'knock-out: average (mean ablation)' if t < 27.6 else 'knock-out: another sentence (resample ablation)'
        kicker(c, tag, W - MX, 336, ramp(t, 0.6, 0.6), 'y', 17, align='right')
        rows = IOI_MEAN
        vis = 1 if t < 14.0 else 4
        pair_bars(c, rows[:vis] if t < 14.0 else rows, 120, 430, 1180, t, 3.6 if t < 14.0 else 13.2, swap=(27.0, IOI_RES), label_w=420)
        bars_legend(c, MX, 960, ramp(t, 4.0, 0.6), 21)
        k = ramp(t, 21.0, 0.7) * (1 - ramp(t, 26.5, 0.5))
        if k > 0:
            hand(c, 'F > 1: more sure than the model itself', 1180, 905, 32, 'pencil', k, -2.5, ramp(t, 21.0, 1.0, e_lin))

DOC = [('classic circuit · mean', 77.1, 35.8, 1.017), ('EAP-IG · mean', 65.6, 69.4, 0.651),
       ('classic circuit · resample', 47.2, 38.9, 0.765)]   # Table 1, Docstring

class Docstring(Scene):
    dur = 26.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (7.0, 'pop'), (12.0, 'pop'), (19.0, 'pop')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '03'), 'a second task', 'A messier *picture*', sub='Docstring: a 4-layer model completes Python documentation · wrong on ~35% (Table 2)')
        n = 1 if t < 12 else (2 if t < 19 else 3)
        pair_bars(c, DOC[:n], 120, 470, 1180, t, 6.6, label_w=420)
        bars_legend(c, MX, 960, ramp(t, 7.0, 0.6), 21)
        caption(c, t, 'A {y:small gap} can mean errors are reproduced better, or that {c:successes} stopped being reproduced.', 19.5, None, y=900, size=29)

class Discussion(Scene):
    dur = 18.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (10.0, 'chime')]

    def draw(self, c, t):
        header(c, t, getattr(self, 'NUM', '04'), 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('If a circuit gets the {y:right answer} where the model got it {r:wrong}, what has it explained?', 3.0),
                              ('How much of the gap belongs to the {y:knock-out method}, rather than the circuit?', 10.0)])

class End(EndCard):
    TAKE = 'A circuit can look {y:faithful} on average, and still miss most of the model’s {r:mistakes}.'
    STATS = [('99.5%', 'classic circuit agrees where the model is right', 'f'), ('15.2%', '…and where it is wrong', 'c'),
             ('0.956', 'its faithfulness score', 'y')]
    NEXT = 'also in this series: can the gap be explained away?  ·  how the wrong name wins'
