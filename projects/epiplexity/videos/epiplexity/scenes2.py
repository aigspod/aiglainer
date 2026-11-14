"""Paradox 1 (computation creates information: ECA rules, Fig. 3, our laptop run) and Paradox 2 (order matters: one-way
functions, Fig. 4a; chess, Fig. 4c and Fig. 7) of arXiv:2601.03220v2. Paper data come from the topic's data/ via
epikit.tdata; our run (ours_rules_n32_k8.json) is labelled 'our run'."""
from epikit import *

# ======================================================================= AUTOMATA
class Automata(Scene):
    """§5.1: what an elementary cellular automaton is, and rollouts of rules 15, 30 and 54 (computed from the rules)."""
    dur = 25.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (5.5, 'draw'), (14.0, 'pop'), (15.6, 'pop'), (17.2, 'pop')]

    def __init__(self):
        self.demo = eca(54, 33, 2, seed=21)
        self.grids = {r: eca(r, 64, 52, seed=7) for r in (15, 30, 54)}

    def draw(self, c, t):
        hdr(self, c, t, '03', 'paradox one', 'Can computation *create* information?',
            sub='§5.1: Shannon and Kolmogorov both say no: H(f(X)) ≤ H(X),  K(f(x)) ≤ K(x) + K(f) + c')
        # the three paradoxes (§5), the first one lit
        kr = window(t, 0.6, 5.0, 0.6, 0.5)
        if kr > 0:
            P = [('1', 'computation cannot create information', 'data processing: H(f(X)) ≤ H(X)'),
                 ('2', 'information does not depend on order', 'H(X) + H(Y|X) = H(Y) + H(X|Y)'),
                 ('3', 'a model can only match its generator', 'arg min E[−log P] = the true distribution')]
            for i, (n, claim, why) in enumerate(P):
                k = ramp(t, 0.6 + i * 0.35, 0.7, e_expo) * kr
                if k <= 0:
                    continue
                x = MX + i * 570
                lit = ramp(t, 2.4, 0.6) if i == 0 else 0
                with layer(c, k * (1 - 0.45 * ramp(t, 2.4, 0.6) * (i > 0))):
                    panel(c, x, 420, 540, 260, stroke='y' if lit > 0.5 else 'line')
                    line(c, x + 30, 421, x + 150, 421, 'y', 1, 4, cap='butt')
                    text(c, f'paradox {n}', x + 30, 480, 20, 500, 'y', 1, kind='mono')
                    rich(c, claim, x + 30, 540, 32, 480, 1e9, 0, base_w=500)
                    text(c, why, x + 30, 650, 17, 500, 'muted', 1, kind='mono')
            text(c, '“And yet…”: each looks different to a learner with limited compute', W / 2, 760, 24, 400, 'muted',
                 ramp(t, 2.8, 0.6) * kr, 'center', kind='italic')
        # the rule, as a table, and one row being updated (rule 54)
        kd = window(t, 5.5, 13.6, 0.7, 0.6)
        if kd > 0:
            w = 8 * 3 * 30 + 7 * 14
            rule_icons(c, 54, W / 2 - w / 2, 410, 30, kd, t, 5.8, 'y')
            kicker(c, 'rule 54: each cell’s next state from itself and its two neighbours', W / 2, 385, kd, 'muted', 16, 'center')
            cell = 34
            x0 = W / 2 - 33 * cell / 2
            y0 = 640
            bits_row(c, self.demo[0], x0, y0, cell, kd, 'y')
            j = int(clamp((t - 7.5) / 0.14, 0, 33))
            nxt = self.demo[1].copy()
            nxt[j:] = 0
            bits_row(c, nxt[:j], x0, y0 + cell + 10, cell, kd, 'y')
            for q in range(j, 33):
                rrect(c, x0 + q * cell, y0 + cell + 10, cell * 0.8, cell * 0.8, 6, fill='faint', fa=kd * 0.35)
            if 0 < j < 33:
                rrect(c, x0 + (j - 1) * cell - 4, y0 - 4, cell * 3 + 2, cell + 2, 6, stroke='ink', sw=2, a=kd)
                arrow(c, x0 + (j + 0.4) * cell, y0 + cell, x0 + (j + 0.4) * cell, y0 + cell + 10, 'ink', kd, 2, 6)
            text(c, 'time ↓', x0 - 24, y0 + cell + 4, 18, 500, 'muted', kd, 'right', kind='mono')
            note(c, 'one of 256 possible rules', W / 2, 800, kd, 17, 'muted', 'center')
        # three rules
        for i, (r, cls, desc) in enumerate(((15, 'class II', 'simple, periodic'), (30, 'class III', 'looks like noise'),
                                            (54, 'class IV', 'gliders that travel and collide'))):
            ti = 14.0 + i * 1.6
            k = ramp(t, ti, 0.6)
            if k <= 0:
                continue
            x = 150 + i * 560
            colr = FIG3_COLORS[str(r)]
            draw_eca(c, self.grids[r], x, 380, 500, t, ti, 26, color=colr, a=k, bg_a=0.08)
            text(c, f'rule {r}', x, 850, 34, 400, colr, k, kind='italic')
            text(c, cls, x + 140, 848, 20, 500, 'muted', k, kind='mono')
            text(c, desc, x, 886, 21, 500, 'ink', k, kind='mono')
        tag(c, EXACT + ' · random first row · time flows down', W - MX, 925, ramp(t, 14.5, 0.6), 'right')

# ======================================================================= FIG 3
class Fig3(Scene):
    """Fig. 3 right: best two-part code, S_T and H_T vs compute, rules 15/30/54 (fig3_eca.json)."""
    dur = 31.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (7.0, 'draw'), (15.5, 'draw'), (23.0, 'tick')]
    PANELS = [('two_part', 'two-part code  (×10⁸ bits)', 1e8, (0, 1.12), (0, 0.5, 1.0)),
              ('epiplexity', 'epiplexity Sₜ  (×10⁶ bits)', 1e6, (0, 6.6), (0, 2, 4, 6)),
              ('entropy', 'time-bounded entropy Hₜ  (×10⁸ bits)', 1e8, (0, 1.12), (0, 0.5, 1.0))]

    def __init__(self):
        self.d = tdata('fig3_eca.json')
        self.mini = {r: eca(int(r), 40, 28, seed=3) for r in ('15', '30', '54')}

    def draw(self, c, t):
        hdr(self, c, t, '03', 'paradox one', 'Three rules, three *fates*',
            sub='Fig. 3: predict the row 48 steps on (64 cells) from a random row; best two-part code at each compute budget')
        ka = ramp(t, 0.6, 0.8)
        axes = []
        for i, (key, lab, scale, yr, yt) in enumerate(self.PANELS):
            ax = LogAxes(210 + i * 570, 400, 440, 360, (11.8, 17.4), yr)
            axes.append(ax)
            ax.draw(c, ka, (12, 14, 16), yt, yfmt=lambda v: f'{v:g}', fs=18)
            text(c, lab, ax.x, ax.y - 22, 21, 500, 'ink', ka)
            text(c, 'compute (FLOPs)', ax.x + ax.w, ax.y + ax.h + 64, 17, 500, 'muted', ka, 'right', kind='mono')
        for r, t0 in (('15', 7.0), ('30', 8.5), ('54', 15.5)):
            colr = FIG3_COLORS[r]
            for (key, lab, scale, yr, yt), ax in zip(self.PANELS, axes):
                f = self.d['panels'][key]['frontier'][r]
                ys = np.array(f['y']) / scale
                curve_reveal(c, ax, f['x'], ys, colr, t, t0, 2.2 if r == '54' else 1.4, w=3.2, dots=True, r=5)
            # label at the right end of the S_T curve
        kl = ramp(t, 2.0, 0.6)
        for i, r in enumerate(('15', '30', '54')):
            x = 300 + i * 520
            k = ramp(t, (7.0, 8.5, 15.5)[i], 0.6)
            draw_eca(c, self.mini[r], x, 852, 100, color=FIG3_COLORS[r], a=k, bg_a=0.06, frame=False)
            text(c, f'rule {r}', x + 122, 890, 28, 400, FIG3_COLORS[r], k, kind='italic')
            text(c, ('little of either', 'all randomness', 'structure that keeps growing')[i], x + 122, 926, 19, 500, 'ink',
                 ramp(t, (7.5, 10.0, 17.0)[i], 0.6), kind='mono')
        # annotations
        k5 = ramp(t, 18.0, 0.7)
        if k5 > 0:
            X, Y = axes[1].px(1.731e17, 5.411)
            text(c, '≈ 5.4 × 10⁶ bits', X - 6, Y - 18, 20, 600, FIG3_COLORS['54'], k5, 'right')
        src(c, 'Fig. 3', W - MX, 975, ka, 'right')

# ======================================================================= OUR RUN
class OurRun(Scene):
    """Our laptop run (lab/eca_lab.py; ours_rules_n32_k8.json): loss curves and prequential areas. Not the paper's.
    If ours_rules_n32_k16_s20000.json has rules 15 and 54, a longer run replaces the area bars at LONG."""
    dur = 38.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (8.0, 'draw'), (12.5, 'draw'), (19.5, 'draw'), (24.5, 'pop')]
    ORDER = [('15', 8.0), ('30', 12.5), ('coin', 13.2), ('54', 19.5), ('110', 20.2)]

    LONG = 30.5          # when the longer run (if its file has rules 15 and 54) replaces the area bars

    def __init__(self):
        self.d = tdata('ours_rules_n32_k8.json')
        try:
            lr = tdata('ours_rules_n32_k16_s20000.json')['runs']
            self.long = lr if '15' in lr and '54' in lr else None
        except (OSError, KeyError, ValueError):
            self.long = None

    def draw(self, c, t):
        hdr(self, c, t, '03', 'our run', 'A *miniature* on a laptop', sub=None)
        tag(c, OURS + ' (not the paper’s):  a 4-layer transformer, 0.8M parameters  ·  32 cells, 8 steps  ·  '
            '4,000 steps of 128 fresh rows', MX, 300, ramp(t, 0.6, 0.7), size=18)
        ax = LinAxes(200, 380, 880, 470, (0, 4000), (0, 42))
        ka = ramp(t, 0.8, 0.8)
        ax.draw(c, ka, (0, 1000, 2000, 3000, 4000), (0, 8, 16, 24, 32, 40), fmt='{:g}', xfmt='{:g}')
        text(c, 'loss: bits per 32-cell row  (lower is better)', 200, 362, 18, 500, 'muted', ka, kind='mono')
        text(c, 'training step', 1080, 918, 18, 500, 'muted', ka, 'right', kind='mono')
        runs = self.d['runs']
        for name, t0 in self.ORDER:
            r = runs[name]
            y = np.array(r['curve'])
            x = np.arange(len(y)) * r['every']
            colr = RULE_COLORS[name]
            fin = loss_curve(c, ax, x, y, colr, t, t0, 2.6, final=r['final_bits'], area=name in ('15', '54'),
                             fa=0.16 * ramp(t, 24.5, 0.8), w=2.6 if name != 'coin' else 2.0)
            k = ramp(t, t0 + 2.4, 0.5)
            lab = f'rule {name}' if name != 'coin' else 'coin flips'
            X, Y = ax.px(4000, fin)
            dy = {'30': -16, 'coin': 18, '54': 6, '110': 6, '15': -12}[name]
            text(c, f'{lab}  {fin:.1f}', X + 14, Y + dy + 6, 19, 600, colr, k, kind='mono')
        k15 = ramp(t, 10.0, 0.6)
        if k15 > 0:
            X, Y = ax.px(1690, 0.4)
            _, Y2 = ax.px(1690, 13)
            line(c, float(X), float(Y) - 8, float(X), float(Y2) + 8, RULE_COLORS['15'], k15 * 0.8, 1.5)
            circle(c, float(X), float(Y), 6, stroke=RULE_COLORS['15'], sw=2.5, a=k15)
            note(c, '≈ 0 bits by step ~1,700', float(X) + 10, float(Y2), k15, 17, RULE_COLORS['15'])
        # areas above the final loss (the prequential heuristic), bits summed over every training row
        kb = ramp(t, 24.5, 0.8) * (1 - ramp(t, self.LONG - 0.6, 0.6) if self.long else 1)
        if kb > 0:
            x0, y0 = 1420, 420
            kicker(c, 'area above final loss', x0, y0 - 22, kb, 'muted', 16)
            note(c, 'bits, summed over training (a heuristic)', x0, y0 + 4, kb * 0.9, 14)
            amax = max(runs[n]['area_bits'] for n in runs)
            for i, n in enumerate(('15', '54', '110', '30', 'coin')):
                a = runs[n]['area_bits']
                yy = y0 + 46 + i * 74
                kk = ramp(t, 24.7 + i * 0.25, 0.6) * kb
                text(c, f'rule {n}' if n != 'coin' else 'coin', x0, yy + 20, 20, 500, RULE_COLORS[n], kk, kind='mono')
                bw = 200 * a / amax * ramp(t, 24.7 + i * 0.25, 0.9, e_expo)
                rrect(c, x0 + 104, yy, max(bw, 2), 28, 5, fill=RULE_COLORS[n], fa=kk * 0.85)
                text(c, sci(a), x0 + 114 + bw, yy + 21, 18, 500, 'ink', kk)
            note(c, 'one run each, not a compute sweep', x0, y0 + 430, kb * 0.9, 15)
        # a longer run (our run): 16 steps, 20,000 training steps, rules 15 and 54 with their areas
        kl = ramp(t, self.LONG, 0.8) if self.long else 0
        if kl > 0:
            x0, y0 = 1400, 400
            kicker(c, 'a longer run', x0, y0 - 22, kl, 'y', 16)
            note(c, '16 steps · 20,000 training steps', x0, y0 + 4, kl * 0.9, 14)
            ax2 = LinAxes(x0 + 30, y0 + 40, 360, 250, (0, 20000), (0, 42))
            ax2.draw(c, kl, (0, 10000, 20000), (0, 16, 32), fmt='{:g}', xfmt='{:g}', grid=False)
            for i, n in enumerate(('15', '54')):
                r = self.long[n]
                y = np.array(r['curve'])
                x = np.arange(len(y)) * r['every']
                loss_curve(c, ax2, x, y, RULE_COLORS[n], t, self.LONG + 0.3 + i * 0.8, 2.0, final=r['final_bits'],
                           fa=0.22, w=2.0, a=kl)
            for i, n in enumerate(('15', '54')):
                r = self.long[n]
                yy = y0 + 360 + i * 50
                kk = ramp(t, self.LONG + 2.6 + i * 0.4, 0.6) * kl
                text(c, f'rule {n}', x0, yy, 20, 500, RULE_COLORS[n], kk, kind='mono')
                text(c, f'final {r["final_bits"]:.1f} bits  ·  area {sci(r["area_bits"])}', x0 + 110, yy, 18, 500, 'ink', kk)

# ======================================================================= ONE-WAY FUNCTIONS
class OneWay(Scene):
    """§5.2: symmetry of information; one-way functions (Thm 13); Fig. 4a: rule 30, 8 steps, forward vs reverse."""
    dur = 29.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (7.0, 'pop'), (14.5, 'draw'), (22.5, 'tick')]

    def __init__(self):
        a = tdata('fig4_owf_chess.json')['fig4a_owf']['series']
        self.s = a
        self.r30 = eca(30, 24, 9, seed=13)

    def draw(self, c, t):
        hdr(self, c, t, '04', 'paradox two', 'Does *order* matter?',
            sub='§5.2: for Shannon, the total is the same in either order (for Kolmogorov, up to a log term)')
        tex(c, 'sym', 480, 400, 40, ramp(t, 1.5, 0.8))
        # primes: easy one way, hard the other (illustration)
        kp = ramp(t, 7.0, 0.7)
        if kp > 0:
            panel(c, MX, 470, 760, 210, kp)
            text(c, '7919 × 6841', MX + 30, 535, 34, 500, 'ink', kp, kind='mono')
            arrow(c, MX + 300, 524, MX + 420, 524, 'f', kp, 3, 14, prog=ramp(t, 7.3, 0.5, e_io))
            text(c, '54,173,879', MX + 440, 535, 34, 500, 'ink', kp, kind='mono')
            text(c, 'multiply: instant', MX + 30, 568, 18, 500, 'f', kp, kind='mono')
            kr = ramp(t, 8.8, 0.6)
            text(c, '54,173,879', MX + 30, 635, 34, 500, 'ink', kr, kind='mono')
            arrow(c, MX + 300, 624, MX + 420, 624, 'r', kr, 3, 14, prog=ramp(t, 9.0, 0.5, e_io))
            text(c, '? × ?', MX + 440, 635, 34, 500, 'r', kr, kind='mono')
            text(c, 'factor: a search', MX + 30, 668, 18, 500, 'r', kr, kind='mono')
            tag(c, ILLUS, MX + 760, 700, kp, 'right')
        # rule 30 as the one-way function
        k3 = ramp(t, 14.5, 0.7)
        if k3 > 0:
            draw_eca(c, self.r30, MX + 120, 740, 216, color=FIG3_COLORS['30'], a=k3, bg_a=0.08)
            text(c, 'X', MX + 90, 756, 24, 400, 'ink', k3, kind='italic')
            text(c, 'Y', MX + 90, 740 + 216 / 24 * 9 - 4, 24, 400, 'ink', k3, kind='italic')
            text(c, 'rule 30, 8 steps', MX + 360, 790, 20, 500, FIG3_COLORS['30'], k3, kind='mono')
            text(c, 'forward: X then Y', MX + 360, 830, 20, 500, '#c9c94a', k3, kind='mono')
            text(c, 'reverse: Y then X', MX + 360, 862, 20, 500, '#c77ad6', k3, kind='mono')
            note(c, 'believed one-way (not proven)', MX + 360, 900, k3, 16)
        # Fig. 4a
        ax = LinAxes(1040, 400, 720, 470, (12, 68), (0, 135))
        kc = ramp(t, 14.5, 0.8)
        if kc > 0:
            ax.draw(c, kc, (16, 32, 48, 64), (0, 32, 64, 96, 128), fmt='{:g}', xfmt='{:g}')
            text(c, 'loss: bits per (X, Y) pair', 1040, 382, 18, 500, 'muted', kc, kind='mono')
            text(c, 'n, cells per row', 1760, 918, 18, 500, 'muted', kc, 'right', kind='mono')
            s = self.s
            curve_reveal(c, ax, s['random_guess']['x'], s['random_guess']['y'], '#c0504d', t, 14.8, 0.8, w=2, dash=[8, 6])
            curve_reveal(c, ax, s['entropy']['x'], s['entropy']['y'], 'v', t, 14.8, 0.8, w=6, a=0.5)
            text(c, 'random guess, 2n', 1600, ax.px(60, 128)[1] - 4, 17, 500, '#c0504d', ramp(t, 15.5, 0.5), 'right', kind='mono')
            text(c, 'entropy, n', 1756, ax.px(64, 64)[1] + 40, 17, 500, 'v', ramp(t, 15.5, 0.5), 'right', kind='mono')
            curve_reveal(c, ax, s['forward']['x'], s['forward']['y'], '#c9c94a', t, 16.0, 1.4, w=3, dots=True)
            curve_reveal(c, ax, s['reverse']['x'], s['reverse']['y'], '#c77ad6', t, 22.5, 1.4, w=3, dots=True)
            kg = ramp(t, 24.0, 0.6)
            if kg > 0:
                X, Y1 = ax.px(64, 78.01)
                _, Y0 = ax.px(64, 64)
                line(c, float(X) + 18, float(Y1), float(X) + 18, float(Y0), '#c77ad6', kg, 2.5)
                text(c, '≈ 14-bit gap', float(X) + 10, float(Y1) - 18, 18, 600, '#c77ad6', kg, 'right', kind='mono')
            src(c, 'Fig. 4a', 1760, 965, kc, 'right')

# ======================================================================= CHESS
class Chess(Scene):
    """Fig. 4b (the two orderings), Fig. 4c (H_T, S_T vs compute), §6.1 / Fig. 7 (downstream), all from fig4/fig7 json."""
    dur = 27.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (8.0, 'draw'), (15.5, 'pop')]

    def __init__(self):
        self.c4 = tdata('fig4_owf_chess.json')['fig4c_chess']['panels']
        self.f7 = tdata('fig7_chess_ood.json')['bars']
        self.board = {'e1': 'w:♚', 'g1': 'w:♜', 'd4': 'w:♟', 'e5': '♟', 'c6': '♞', 'f3': 'w:♞', 'e8': '♚', 'a8': '♜',
                      'b5': 'w:♝', 'd8': '♛', 'd1': 'w:♛', 'h7': '♟', 'a2': 'w:♟'}

    def draw(self, c, t):
        hdr(self, c, t, '04', 'paradox two', 'Chess, *backwards*',
            sub='Fig. 4b-c, §6.1, Fig. 7: Lichess games as moves then final board (forward) or board then moves (reverse)')
        F, R = ORDER_COLORS['forward'], ORDER_COLORS['reverse']
        for i, (lab, colr, first, second) in enumerate((('forward', F, '1. e4 e5  2. Nf3 Nc6  3. Bb5 …', 'final board'),
                                                       ('reverse', R, 'final board', '1. e4 e5  2. Nf3 Nc6  3. Bb5 …'))):
            k = ramp(t, 0.8 + i * 1.6, 0.7)
            if k <= 0:
                continue
            y = 350 + i * 78
            text(c, lab, MX, y + 40, 24, 600, colr, k, kind='mono')
            for j, s_ in enumerate((first, second)):
                x = MX + 170 + j * 520
                isb = s_ == 'final board'
                w = 150 if isb else 440
                rrect(c, x, y, w, 58, 10, fill='panel2', stroke=colr, sw=1.4, a=k)
                if isb:
                    chessboard(c, x + 49, y + 3, 52, k, None)
                else:
                    text(c, s_, x + 18, y + 37, 19, 500, 'ink', k, kind='mono')
                if j == 0:
                    arrow(c, x + w + 14, y + 29, MX + 170 + 520 - 14, y + 29, colr, k, 2.4, 11)
        kb = ramp(t, 2.5, 0.7)
        chessboard(c, 1420, 330, 230, kb, self.board)
        tag(c, ILLUS, 1650, 585, kb, 'right')
        # Fig. 4c
        kc = ramp(t, 8.0, 0.8)
        for i, (key, lab, scale, yr, yt) in enumerate((('entropy', 'time-bounded entropy Hₜ  (×10⁹ bits)', 1e9, (3, 8.2), (4, 6, 8)),
                                                       ('epiplexity', 'epiplexity Sₜ  (×10⁸ bits)', 1e8, (0, 3.0), (0, 1, 2)))):
            ax = LogAxes(200 + i * 520, 650, 400, 230, (14.9, 18.9), yr)
            ax.draw(c, kc, (15, 16, 17, 18), yt, yfmt=lambda v: f'{v:g}', fs=17)
            text(c, lab, ax.x, ax.y - 18, 19, 500, 'ink', kc)
            for name, colr, t0 in (('forward', F, 8.4), ('reverse', R, 9.4)):
                d = self.c4[key][name]
                curve_reveal(c, ax, d['x'], np.array(d['y']) / scale, colr, t, t0, 1.6, w=3, dots=True, r=4)
        text(c, 'compute (FLOPs)', 1120, 945, 16, 500, 'muted', kc, 'right', kind='mono')
        src(c, 'Fig. 4c', 200, 975, kc)
        # Fig. 7 (bars from zero)
        kf = ramp(t, 15.5, 0.8)
        if kf > 0:
            x0 = 1280
            for j, (key, lab, fmt) in enumerate((('puzzle_acc', 'puzzle accuracy', '{:.1%}'), ('cp_acc', 'centipawn accuracy', '{:.1%}'))):
                y = 680 + j * 130
                text(c, lab, x0, y - 12, 19, 500, 'ink', kf, kind='mono')
                for q, (name, colr) in enumerate((('forward', F), ('reverse', R))):
                    v = self.f7[key][name]
                    kk = ramp(t, 15.8 + j * 0.8 + q * 0.3, 0.8, e_expo) * kf
                    bw = 480 / 0.35 * v * kk
                    rrect(c, x0, y + q * 40, max(bw, 2), 30, 5, fill=colr, fa=kf * 0.85)
                    text(c, fmt.format(v), x0 + bw + 12, y + q * 40 + 23, 19, 600, colr, kf, kind='mono')
            note(c, 'after fine-tuning; bars start at zero', x0, 930, kf * 0.9, 15)
            src(c, 'Fig. 7', 1800, 975, kf, 'right')
