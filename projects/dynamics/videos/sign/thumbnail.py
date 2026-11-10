"""Thumbnail: one focal image (a plus bar and a minus bar), few big words; nothing important bottom-right."""
from dynkit import *

def draw(c):
    lamp(c, 1720, 150, 1.3, 1, on=1)
    text(c, 'Attention', 110, 340, 150, 800, 'ink', kind='sans', tracking=-0.02)
    text(c, 'can only', 110, 500, 120, 500, 'muted', kind='italic')
    w = text(c, 'average', 110, 690, 180, 500, 'y', kind='italic')
    swash(c, 110, 110 + w, 735, 'y', 1, 1, w=9)
    # the recipe a soft spring needs: one plus, one minus (our calculation: +1.24 and -0.98)
    x0, y0 = 1130, 560
    line(c, x0 - 40, y0, x0 + 560, y0, 'muted', 1, 5)
    rrect(c, x0 + 40, y0 - 300, 190, 300, 14, fill='f', fa=0.95)
    rrect(c, x0 + 320, y0, 190, 238, 14, fill='c', fa=0.95)
    for cx, cy, colr, plus in ((x0 + 135, y0 - 370, 'f', True), (x0 + 415, y0 + 310, 'c', False)):
        rrect(c, cx - 50, cy - 11, 100, 22, 8, fill=colr, fa=1)          # bold drawn signs (glyphs render thin)
        if plus:
            rrect(c, cx - 11, cy - 50, 22, 100, 8, fill=colr, fa=1)
    hand(c, 'needs a minus', 110, 900, 92, 'pencil', 1, -2.5)
