"""The YouTube thumbnail of the jazz edition (make thumbnail): drawn on the 1920x1080 canvas, saved at 1280x720.
Night navy, a big record with a terracotta label half off the right edge, rainbow arcs, and few big words:
the aigs HACKATHON, 'jazz edition', the date. Nothing important bottom-right (the timestamp covers it)."""
from aiglainer.core import *
from event import WHEN
from sleeve import PAD, slab, say, fit, record, arcs, glow, stars, vignette


def draw(c):
    slab(c, 'night')
    stars(c, 3.0, 0.7, n=50)
    cx, cy, R = 1640, 600, 470
    glow(c, cx, cy, 900, 'mustard', 0.14)
    arcs(c, cx, cy + 40, R + 26, 0, ('mustard', 'terra', 'sage'), width=16, gap=30)
    record(c, cx, cy, R, 0, 0.08, 'terra', lab=0.38)
    x = PAD - 30
    say(c, 'the aigs', x + 6, 250, 130, 'mustard', 1, 'left', 600, 'ital')
    say(c, 'HACKATHON', x, 470, fit('HACKATHON', 230, 1500, 700), 'paper', 1, 'left', 700, shadow=0.7)
    say(c, 'jazz edition', x + 4, 690, 168, 'mustard', 1, 'left', 640, 'ital', shadow=0.6)
    say(c, WHEN, x + 8, 860, 80, 'paper', 1, 'left', 560, 'ital', shadow=0.6)
    vignette(c, 0.35)
