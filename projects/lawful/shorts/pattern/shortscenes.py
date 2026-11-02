"""Native 9:16 scene for the 'pattern, not payload' short. Drawn in aiglainer.short.BOX (720 x 700), origin top-left.
Numbers from LAWFUL Table 2: patching only the attention pattern (QK) of the circuit's heads leaves a score of
0.988 - 0.35 = 0.64; patching only the values leaves 0.988 - 1.31 = -0.32. The head diagram is an illustration."""
import math
from aiglainer.core import *
from aiglainer.timeline import Scene

M0, QK, VAL = 0.988, 0.988 - 0.35, 0.988 - 1.31

class WhereVsWhat(Scene):
    vertical = True
    dur = 16.0
    cues = [(0.4, 'pop'), (1.8, 'draw'), (8.0, 'pop'), (11.5, 'drop')]

    def draw(self, c, t):
        # a head: frames along time, one query below; arcs = where it looks, dots coming back = what it carries
        ka = ramp(t, 0.3, 0.7)
        text(c, 'one attention head', 0, 26, 21, 400, 'muted', ka, kind='mono', tracking=0.08)
        text(c, 'illustration', 720, 26, 18, 400, 'muted', 0.8 * ka, 'right', kind='mono', tracking=0.1)
        xs = [40 + i * 91 for i in range(8)]
        fy, qy, qx = 110, 270, 360
        for x in xs:
            circle(c, x, fy, 13, fill='v', a=ka * 0.9)
        text(c, 'frames over time →', 40, fy - 36, 20, 400, 'muted', ka, kind='mono', tracking=0.06)
        circle(c, qx, qy, 17, fill='y', a=ka, glow=8)
        kw = ramp(t, 1.8, 1.2, e_io)
        weights = [0.9, 0.35, 0.1, 0.05, 0.05, 0.1, 0.35, 0.9]
        for x, wgt in zip(xs, weights):
            if kw > 0:
                line(c, qx, qy - 17, qx + (x - qx) * kw, qy - 17 + (fy + 14 - qy + 17) * kw, 'y', kw * (0.25 + 0.75 * wgt), 1.5 + 5 * wgt)
        kv = window(t, 3.0, None, 0.6)
        if kv > 0:
            for x, wgt in zip(xs, weights):
                ph = ((t - 3.0) * 0.6 + x / 720) % 1.0
                px, py = x + (qx - x) * ph, fy + 14 + (qy - fy - 31) * ph
                circle(c, px, py, 3 + 5 * wgt, fill='g', a=kv * (0.3 + 0.7 * wgt))
        kl = ramp(t, 2.2, 0.6)
        if kl > 0:
            text(c, 'where it looks', 40, 330, 27, 700, 'y', kl, kind='heavy')
            text(c, 'what it carries', 680, 330, 27, 700, 'g', kl, 'right', kind='heavy')
        # the two swaps, as bars of the score that's left (full model = 0.988)
        x0, full = 200, 440                     # x of score 0, px for 0.988
        def bar(y, val, label, colr, k):
            text(c, label, 0, y - 18, 25, 600, 'ink', k)
            w = full * val / M0 * ramp(k, 0, 1, e_out)
            rrect(c, x0 + min(0, w), y, abs(w), 50, 8, fill=colr, fa=0.85 * k, glow=6)
            # the value sits just right of the bar's far end (of the zero line, for a negative bar)
            text(c, f'{val:.2f}'.replace('-', '−'), x0 + max(w, 0) + 14, y + 37, 32, 700, colr, k, kind='heavy')
        kb = ramp(t, 6.8, 0.6)
        if kb > 0:
            line(c, x0, 405, x0, 640, 'muted', kb, 2)
            line(c, x0 + full, 405, x0 + full, 640, 'f', kb, 2, dash=[7, 6])
            text(c, '0', x0, 664, 20, 400, 'muted', kb, 'center', kind='mono')
            text(c, 'full model 0.988', 720, 664, 20, 400, 'f', kb, 'right', kind='mono')
        k1 = ramp(t, 8.0, 1.0)
        if k1 > 0:
            bar(450, QK, 'swap only where it looks', 'y', k1)
        k2 = ramp(t, 11.5, 1.0)
        if k2 > 0:
            bar(570, VAL, 'swap only what it carries', 'r', k2)
