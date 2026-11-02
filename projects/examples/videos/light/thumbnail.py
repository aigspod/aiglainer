"""The thumbnail: the same drawing code, in this project's theme."""
from aiglainer.core import *
from aiglainer.notes import lamp, swash, sticky

def draw(c):
    lamp(c, 1450, 300, 2.6, 1, on=1)
    text(c, 'A different', 120, 470, 170, 700, 'ink')
    w = text(c, 'look', 120, 660, 170, 700, 'y')
    swash(c, 120, 120 + w, 700, 'y', 1, 1, w=7)
    kicker(c, 'aiglainer  ·  an example', 128, 840, 1, 'muted', 34)
