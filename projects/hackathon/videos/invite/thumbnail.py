"""The YouTube thumbnail (make thumbnail): drawn on the 1920x1080 canvas, saved at 1280x720.
Three big words on cobalt, the date in an orange block, a halftone planet; nothing important bottom-right."""
from aiglainer.core import *
from event import WHEN
from poster import PAD, slab, big, fit, globe, stripes


def draw(c):
    slab(c, 'cobalt')
    stripes(c, 0.0, 'lime', 0.08)
    globe(c, 1500, 470, 400, 1.3, 0.9, sea='paper', air='orange', a=1, step=15)
    big(c, 'THE AIGS', PAD - 10, 330, 190, 'paper', riso=('orange', 'night', 5))
    big(c, 'HACK-', PAD - 10, 560, 250, 'lime', riso=('orange', 'night', 6))
    big(c, 'ATHON', PAD - 10, 790, 250, 'lime', riso=('orange', 'night', 6))
    s = WHEN.upper()
    size = fit(s, 92, 1300)
    w = text_width(s, size, 900, 'heavy', -0.03)
    slab(c, 'orange', 1, PAD - 30, 850, w + 50, size * 1.25)
    big(c, s, PAD - 6, 850 + size * 0.98, size, 'night', track=-0.03)
