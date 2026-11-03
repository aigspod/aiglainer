"""The YouTube thumbnail: one focal image, a few big words, nothing important bottom-right."""
from aiglainer.core import *
from aiglainer.notes import swash
from cldkit import figcard

def draw(c):
    text(c, 'Beam loss', 120, 330, 160, 600, 'ink', kind='display')
    text(c, '→', 120, 510, 160, 500, 'muted', kind='display')
    w = text(c, 'phase space', 300, 510, 160, 500, 'y', kind='italic')
    swash(c, 300, 300 + w, 552, 'y', 1, 1, w=8)
    kicker(c, 'latent diffusion  ·  journal club', 128, 650, 1, 'muted', 34)
    figcard(c, 'fig1_D', 1090, 600, 720, 1, None, credit=False)
