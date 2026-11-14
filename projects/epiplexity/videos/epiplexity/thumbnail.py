"""Thumbnail: one focal image (the same tiny kind of rule giving noise or structure, watched by the observer) and three
big words. Both diagrams are computed from their rules (30 left, 54 right). Nothing important in the bottom-right."""
from epikit import *

def draw(c):
    g30 = eca(30, 46, 64, seed=2)
    g54 = eca(54, 46, 64, seed=9)
    x0, y0, w = 1010, 70, 400
    with layer(c, 0.95):
        draw_eca(c, g30, x0, y0, w, color='g', bg_a=0.06, frame=False, gap=0.2)
        draw_eca(c, g54, x0 + w + 30, y0, w, color='y', bg_a=0.06, frame=False, gap=0.2, glow=6)
        # fade both diagrams out towards the bottom so the words and the duration badge stay clean
        p = skia.Paint()
        p.setBlendMode(skia.BlendMode.kDstIn)
        p.setShader(skia.GradientShader.MakeLinear([(0, 560), (0, 900)], [skia.Color(0, 0, 0, 255), skia.Color(0, 0, 0, 0)]))
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), p)
    observer(c, x0 + w + 15, 600, 1.6, 1, 0.55, label=None)
    text(c, 'noise', x0 + 20, 860, 44, 600, 'g', 1, kind='mono')
    text(c, 'structure', x0 + 2 * w + 10, 860, 44, 600, 'y', 1, 'right', kind='mono')
    text(c, 'Random', 100, 430, 190, 1000, 'ink', kind='display')
    w2 = text(c, 'to whom?', 100, 640, 176, 1100, 'y', kind='italic')
    swash(c, 110, 100 + w2, 690, 'y', 1, 1, w=10)
    kicker(c, 'epiplexity', 112, 820, 1, 'muted', 46)
