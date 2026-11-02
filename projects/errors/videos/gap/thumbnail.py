"""Thumbnail: one focal image, few big words."""
from aiglainer.core import *
from aiglainer.notes import lamp, swash, sticky

def draw(c):
    lamp(c, 1500, 260, 2.4, 1, on=1)
    text(c, '99.5%', 120, 420, 190, 760, 'f', tracking=-0.02)
    text(c, 'vs', 120, 560, 90, 300, 'muted', kind='italic')
    text(c, '15%', 300, 640, 190, 760, 'c', tracking=-0.02)
    w = text(c, 'the mistakes', 120, 820, 110, 400, 'y', kind='italic')
    swash(c, 120, 120 + w, 856, 'y', 1, 1, w=7)
    sticky(c, 1380, 640, ['circuits &', 'errors · 1/3'], 1, rot=5.0, w=320, h=220)
