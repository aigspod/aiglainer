"""Thumbnail: one focal image (the simulated Van der Pol loop, same x, two phases), few big words."""
import numpy as np
from aiglainer.core import *
from aiglainer.kit import Axes
from aiglainer.notes import lamp, swash, sticky

def draw(c):
    d = load_json('vdp.json')                      # our simulation of the paper's equations (dynamics/videos/sign)
    lamp(c, 1760, 110, 1.1, 1, on=1)
    text(c, 'Rebuild the', 110, 400, 132, 760, 'ink', tracking=-0.02)
    w = text(c, 'hidden', 110, 590, 170, 400, 'y', kind='italic')
    swash(c, 110, 110 + w, 630, 'y', 1, 1, w=8)
    text(c, 'state', 110 + w + 40, 590, 170, 760, 'ink', tracking=-0.02)
    kicker(c, 'attention as delay embedding', 118, 760, 1, 'muted', 44)
    ax = Axes(1140, 400, 560, 560, (-3.0, 3.0), (-3.0, 3.0))
    draw_poly(c, ax.pts(np.array(d['cycle_x']), np.array(d['cycle_v'])), 'y', 1, 9, glow=10)
    X, _ = ax.px(1.0, 0)
    line(c, X, 400, X, 960, 'ink', 0.6, 4, dash=[16, 12])
    for p, colr in zip(d['same_x']['points'], ('f', 'c')):
        PX, PY = ax.px(p['x'], p['v'])
        circle(c, PX, PY, 26, fill=colr, a=1, glow=14)
    text(c, 'up?', 1590, 470, 72, 400, 'f', kind='italic')
    text(c, 'down?', 1580, 880, 72, 400, 'c', kind='italic')
