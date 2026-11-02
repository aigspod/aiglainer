"""Native 9:16 scenes for the errors-short-* projects. Each draws in aiglainer.short.BOX (720 x 700), origin top-left.
Big type: labels >= 19 px, numbers >= 28 px. Numbers: Table 1 (IOI, mean ablation), §3 and Table 4, §4.2 of arXiv:2609.35686v1."""
from aiglainer.core import *
from aiglainer.timeline import Scene

def vbar(c, x, floor, w, hgt, colr, a, label, value, sub=None, glow=0):
    rrect(c, x - w / 2, floor - hgt, w, max(hgt, 3), 10, fill=colr, a=a, fa=a * 0.88, glow=glow)
    text(c, value, x, floor - hgt - 18, 40, 760, colr, a, 'center')
    text(c, label, x, floor + 42, 24, 600, 'ink', a, 'center')
    if sub:
        text(c, sub, x, floor + 74, 20, 500, 'muted', a, 'center')

class Sentence(Scene):
    vertical = True
    dur = 19.0
    cues = [(0.3, 'pop'), (4.5, 'pop'), (9.5, 'pop'), (14.0, 'chime')]

    def draw(self, c, t):
        for i, ln in enumerate(['Sara and Courtney', 'went to the hospital.', 'Courtney gave a bone to …']):
            text(c, ln, 360, 70 + i * 62, 46, 600, 'ink', ramp(t, 0.3 + i * 0.6, 0.5), 'center')
        for j, (lab, name, mark, colr, t0) in enumerate((('gpt-2 says', 'Courtney', '✗', 'r', 4.5), ('its circuit says', 'Sara', '✓', 'y', 9.5))):
            k = ramp(t, t0, 0.6, e_expo)
            if k <= 0:
                continue
            y = 270 + j * 180
            with layer(c, k):
                rrect(c, 60, y, 600, 150, 16, fill='panel', fa=0.8, stroke=colr, sw=2)
                text(c, lab, 100, y + 46, 22, 400, 'muted', 1, kind='mono', tracking=0.12)
                text(c, name, 100, y + 118, 64, 700, colr, 1)
                text(c, mark, 610, y + 112, 60, 700, colr, 1, 'right')
        k = ramp(t, 14.0, 0.7)
        text(c, 'right where the model is wrong', 360, 660, 32, 400, 'y', k, 'center', kind='italic')

class GapBars(Scene):
    vertical = True
    dur = 20.0
    cues = [(3.0, 'pop'), (8.0, 'pop'), (13.0, 'chime')]

    def draw(self, c, t):
        text(c, 'a famous circuit in gpt-2 small', 360, 30, 21, 400, 'muted', ramp(t, 0.3, 0.6), 'center', kind='mono', tracking=0.08)
        floor, hmax = 520, 400
        for i, (lab, sub, v, colr, t0) in enumerate((('model right', 'agrees with it', 99.5, 'f', 3.0),
                                                     ('model wrong', 'same mistake', 15.2, 'c', 8.0))):
            k = ramp(t, t0, 0.6)
            if k > 0:
                vbar(c, 200 + i * 320, floor, 190, hmax * v / 100 * ramp(t, t0, 1.2, e_expo), colr, k, lab, f'{v:.1f}%', sub)
        line(c, 60, floor, 660, floor, 'line', ramp(t, 3.0, 0.5), 2)
        text(c, 'Table 1 · mean ablation', 360, 680, 19, 400, 'muted', ramp(t, 3.0, 0.5), 'center', kind='mono')

class Faithful(Scene):
    vertical = True
    dur = 20.0
    cues = [(3.0, 'pop'), (9.0, 'pop'), (14.0, 'drop')]

    def draw(self, c, t):
        floor, unit = 470, 230           # px per 1.0 of faithfulness
        text(c, 'faithfulness · 1 means perfect', 360, 30, 21, 400, 'muted', ramp(t, 3.0, 0.6), 'center', kind='mono', tracking=0.08)
        for i, (lab, v, colr, t0) in enumerate((('full model', 1.0, 'ink', 3.0), ('edge pruning circuit', 1.486, 'y', 9.0))):
            k = ramp(t, t0, 0.6)
            if k > 0:
                vbar(c, 200 + i * 320, floor, 170, unit * v * ramp(t, t0, 1.2, e_expo), colr, k, lab, f'{v:.2f}', glow=6 if i else 0)
        kd = ramp(t, 3.0, 0.6)
        line(c, 60, floor - unit, 660, floor - unit, 'g', kd, 2.5, dash=[10, 7])
        line(c, 60, floor, 660, floor, 'line', kd, 2)
        ke = ramp(t, 14.0, 0.7, e_expo)
        if ke > 0:
            with layer(c, ke):
                rrect(c, 80, 570, 560, 110, 16, fill='panel', fa=0.85, stroke='c', sw=2)
                text(c, '11.4%', 120, 645, 56, 760, 'c', 1)
                text(c, 'of the model’s', 330, 618, 24, 500, 'ink', 1)
                text(c, 'mistakes reproduced', 330, 652, 24, 500, 'ink', 1)

class NudgeGrid(Scene):
    vertical = True
    dur = 24.0
    cues = [(5.0, 'pop'), (9.0, 'pop'), (14.0, 'chime')]
    MODEL, NUDGED = {3, 9, 14, 20}, {5, 9, 17, 22}       # illustration

    def draw(self, c, t):
        text(c, 'illustration', 700, 20, 19, 400, 'muted', 0.8, 'right', kind='mono', tracking=0.1)
        cell, cols = 92, 6
        for g, (lab, wrong, t0) in enumerate((('the model', self.MODEL, 5.0), ('the nudged circuit', self.NUDGED, 9.0))):
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            y0 = 70 + g * 330
            text(c, lab, 360, y0, 28, 700, 'ink', k, 'center')
            text(c, f'{len(wrong)} of 24 wrong', 360, y0 + 34, 22, 500, 'r', k, 'center')
            for i in range(24):
                x, y = 84 + (i % cols) * cell, y0 + 56 + (i // cols) * 58
                bad = i in wrong
                kk = ramp(t, t0 + 0.02 * i, 0.3) * k
                shared = bad and i in self.MODEL and i in self.NUDGED
                hl = ramp(t, 14.0, 0.5) if shared else 0
                rrect(c, x, y, cell - 14, 46, 8, fill='r' if bad else 'f', a=kk, fa=kk * (0.85 if bad else 0.22),
                      stroke='y' if hl > 0 else None, sw=4)
                if bad:
                    text(c, '✗', x + (cell - 14) / 2, y + 34, 28, 700, 'ink', kk, 'center')

class Extension(Scene):
    vertical = True
    dur = 21.0
    cues = [(3.0, 'pop'), (6.0, 'pop'), (12.0, 'pop'), (16.0, 'chime')]
    BARS = [('classic', 14.22, 'c', 3.0), ('nudge', 20.44, 'v', 12.0), ('random', 29.33, 'v', 12.4), ('+63', 75.11, 'y', 6.0)]

    def draw(self, c, t):
        text(c, 'mistakes reproduced · fresh sentences', 360, 30, 21, 400, 'muted', ramp(t, 3.0, 0.6), 'center', kind='mono', tracking=0.06)
        floor, hmax = 500, 400
        for i, (lab, v, colr, t0) in enumerate(self.BARS):
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            x = 105 + i * 170
            if lab == 'random':        # the range of random extensions of the same size, 17.3-41.3 %
                rrect(c, x - 60, floor - hmax * 0.4133, 120, hmax * (0.4133 - 0.1733), 8, fill='v', a=k, fa=k * 0.22)
            vbar(c, x, floor, 104, hmax * v / 100 * ramp(t, t0, 1.1, e_expo), colr, k, lab, f'{v:.0f}%', glow=8 if colr == 'y' else 0)
        line(c, 30, floor, 690, floor, 'line', ramp(t, 3.0, 0.5), 2)
        k = ramp(t, 16.0, 0.6)
        text(c, 'right pile: 99.3% → 98.9%', 360, 650, 30, 600, 'f', k, 'center')
        text(c, '§4.2 · random: median 29%, range 17–41%', 360, 688, 19, 400, 'muted', ramp(t, 12.4, 0.5), 'center', kind='mono')
