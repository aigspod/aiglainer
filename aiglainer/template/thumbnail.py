"""The YouTube thumbnail (make thumbnail): drawn on the 1920x1080 canvas, saved at 1280x720.
One focal image, three to five big words, and nothing important bottom-right (the duration badge sits there)."""
from aiglainer.core import *
from aiglainer.notes import lamp, swash, sticky

def draw(c):
    lamp(c, 1450, 300, 2.6, 1, on=1)
    text(c, 'A big', 120, 470, 170, 300, 'ink', kind='display')
    w = text(c, 'question?', 120, 660, 170, 400, 'y', kind='italic')
    swash(c, 120, 120 + w, 700, 'y', 1, 1, w=7)
    kicker(c, '__NAME__  ·  journal club', 128, 840, 1, 'muted', 34)
    sticky(c, 1380, 700, ['mech interp', 'explainer'], 1, rot=5.0, w=300, h=220)
