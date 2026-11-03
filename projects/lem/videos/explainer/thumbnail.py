"""The YouTube thumbnail: one focal image, a few big words, nothing important bottom-right."""
from aiglainer.core import *
from aiglainer.notes import lamp, swash, sticky
from lemkit import tiles, latent, zvals, NZ

def draw(c):
    lamp(c, 1560, 260, 2.2, 1, on=1)
    text(c, 'Beams,', 120, 400, 170, 300, 'ink', kind='display')
    w = text(c, 'compressed', 120, 590, 170, 400, 'y', kind='italic')
    swash(c, 120, 120 + w, 630, 'y', 1, 1, w=7)
    kicker(c, 'latent evolution models  ·  journal club', 128, 760, 1, 'muted', 34)
    tiles(c, 1340, 650, 0.3, 1, cell=70, gap=10, cols=5)
    latent(c, 1250, 650, zvals(0), 1, cw=50, ch=26)
