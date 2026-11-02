"""Native 9:16 scene for the 'twice wrong' short. Drawn in aiglainer.short.BOX (720 x 700), origin top-left.
A thought experiment about the consistency score (LAWFUL Eq. 9-10), not data: labelled 'illustration'."""
from aiglainer.core import *
from aiglainer.timeline import Scene

def alpha_at(t):
    """The speed dial: 1 -> 0.5 -> 1.15 -> 1, eased."""
    a = 1.0
    a -= 0.5 * ramp(t, 5.2, 1.6, e_io)
    a += 0.65 * ramp(t, 8.2, 1.8, e_io)
    a -= 0.15 * ramp(t, 11.0, 1.0, e_io)
    return a

class TwiceWrong(Scene):
    vertical = True
    dur = 20.0
    cues = [(0.4, 'pop'), (2.4, 'pop'), (5.2, 'sweep'), (8.2, 'sweep'), (12.0, 'chime')]

    def draw(self, c, t):
        al = alpha_at(t)
        base, floor_y = 100, 430                    # px for the true Doppler centroid at alpha = 1; bars stand on floor_y
        text(c, 'illustration', 720, 18, 18, 400, 'muted', 0.8, 'right', kind='mono', tracking=0.1)
        cols = (('model A', 'right frequency', 'f', 1.0, 0.4), ('model B', 'twice the frequency', 'c', 2.0, 2.4))
        for i, (name, sub, colr, k, t0) in enumerate(cols):
            x = 180 + i * 360
            a = ramp(t, t0, 0.6)
            if a <= 0:
                continue
            text(c, name, x, 66, 40, 700, colr, a, 'center', kind='heavy')
            text(c, sub, x, 104, 25, 400, 'muted', a, 'center')
            hgt = base * k * al * ramp(t, t0 + 0.2, 0.9, e_out)
            rrect(c, x - 70, floor_y - hgt, 140, hgt, 10, fill=colr, fa=0.85 * a, glow=8)
            yt = floor_y - base * al                # what physics says: the same height for both
            line(c, x - 110, yt, x + 110, yt, 'g', a, 3, dash=[10, 7])
            line(c, x - 120, floor_y, x + 120, floor_y, 'line', a, 2)
        kp = ramp(t, 0.8, 0.6)
        if kp > 0:
            text(c, '- - -  what physics says', 360, 152, 24, 400, 'g', kp, 'center')
        ks = ramp(t, 12.0, 0.7, e_out)
        if ks > 0:
            for i in range(2):
                x = 180 + i * 360
                rrect(c, x - 104, floor_y + 22, 208, 58, 29, stroke='f', sw=2, a=ks, fill='f', fa=0.12 * ks)
                text(c, 'score 1.00 ✓', x, floor_y + 61, 27, 700, 'f', ks, 'center', kind='heavy')
        kd = ramp(t, 4.6, 0.6)
        if kd > 0:
            text(c, 'speed toward the radar', 360, 580, 22, 400, 'muted', kd, 'center', kind='mono', tracking=0.08)
            text(c, f'× {al:.2f}', 360, 650, 56, 700, 'y', kd, 'center', kind='heavy')
        kh = ramp(t, 15.0, 0.8)
        if kh > 0:
            hand(c, 'still twice wrong', 448, 220, 34, 'c', kh, reveal=kh, align='right')
