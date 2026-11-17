"""Thumbnail: one focal image (a globe of scattered clues: stations, balloons, satellite stripes; an illustration) and
three big words. Nothing important in the bottom-right (the duration badge)."""
from loopkit import *

def draw(c):
    g = Globe(1400, 470, 400, -62, 24)
    g.draw(c, 1)
    g.dots(c, STATIONS, 'ink', 3.4, 0.85)
    g.dots(c, BALLOONS, 'f', 7, 1)
    for i in range(5):
        lo, la = polar_track(i, lon_start=-30)
        g.track(c, lo, la, 'g', 22, 0.25)
        g.track(c, lo, la, 'g', 3, 0.8)
    text(c, 'No answer', 100, 420, 170, 1000, 'ink', kind='display')
    w2 = text(c, 'key.', 100, 620, 190, 1100, 'y', kind='italic')
    swash(c, 110, 100 + w2, 670, 'y', 1, 1, w=10)
    kicker(c, 'weatherdreamer', 112, 800, 1, 'muted', 46)
