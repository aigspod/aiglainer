"""Native 9:16 scene for the 'readable isn't used' short. Drawn in aiglainer.short.BOX (720 x 700), origin top-left.
Linear-probe R^2 for per-marker radial velocity, from LAWFUL Table 2 / Table 5 (circuit heads; T.MLP; T.MLP with the
attention output replaced by its mean)."""
from aiglainer.core import *
from aiglainer.timeline import Scene

BARS = [  # value, two-line label, colour, appears at (authored time)
    (0.019, ('before', 'attention'), 'v', 5.5),
    (0.213, ('best single', 'head'), 'c', 6.8),
    (0.761, ('all circuit', 'heads'), 'y', 9.0),
    (0.556, ('next layer', '(MLP)'), 'f', 12.5),
    (0.0004, ('MLP, attention', 'blanked'), 'r', 14.6),
]

class ProbeBars(Scene):
    vertical = True
    dur = 20.0
    cues = [(5.5, 'pop'), (6.8, 'pop'), (9.0, 'chime'), (12.5, 'pop'), (14.6, 'drop')]

    def draw(self, c, t):
        top, zero = 150, 520                       # y of R^2 = 1 and of 0
        ka = ramp(t, 0.3, 0.7)
        text(c, 'how well a probe reads velocity', 0, 30, 21, 400, 'muted', ka, kind='mono', tracking=0.06)
        text(c, 'R² = 1 is a perfect read-out', 0, 62, 21, 400, 'muted', ka * 0.8, kind='mono', tracking=0.06)
        line(c, 0, top, 720, top, 'faint', ka, 1.6, dash=[8, 7])
        text(c, '1.0', 720, top - 12, 19, 400, 'muted', ka, 'right', kind='mono')
        line(c, 0, zero, 720, zero, 'line', ka, 2)
        n, bw, gap = len(BARS), 100, 36
        x = (720 - (n * bw + (n - 1) * gap)) / 2
        for val, (l1, l2), colr, t0 in BARS:
            k = ramp(t, t0, 0.9, e_out)
            if k > 0:
                h = max(3, (zero - top) * val * k)
                rrect(c, x, zero - h, bw, h, 8, fill=colr, fa=0.88 * k, glow=8 if colr == 'y' else 4)
                text(c, f'{val:.2f}' if val >= 0.01 else '≈ 0', x + bw / 2, zero - h - 16, 30, 700, colr, k, 'center', kind='heavy')
                text(c, l1, x + bw / 2, zero + 40, 19, 600, 'ink', k, 'center')
                text(c, l2, x + bw / 2, zero + 65, 19, 600, 'ink', k, 'center')
            x += bw + gap
        kh = ramp(t, 17.0, 0.9)
        if kh > 0:
            hand(c, 'readable ≠ used', 360, 660, 40, 'y', kh, reveal=kh, align='center')
