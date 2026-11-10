"""Thumbnail: one focal image (tangled vs ordered latent loops, illustrative), few big words."""
from dynkit import *

def draw(c):
    lamp(c, 1720, 170, 1.6, 1, on=1)
    text(c, 'Room to', 110, 330, 150, 700, 'ink', tracking=-0.01)
    w = text(c, 'unfold', 110, 520, 190, 400, 'y', kind='italic')
    swash(c, 106, 116 + w, 566, 'y', 1, 1, w=8)
    text(c, '≈ 70× worse', 110, 760, 96, 760, 'c', tracking=-0.02)
    text(c, 'without the hidden parameter', 116, 840, 42, 500, 'muted')
    res = range(7)
    cols = [mix('g', 'y', i / 6) for i in res]
    latent_loop(c, 1010, 330, 400, 300, illus_loops(res, separated=False, seed=3), 99, 0, colors=cols, frame=False,
                dot_speed=0, widths=[4] * 7)
    latent_loop(c, 1430, 330, 400, 300, illus_loops(res, separated=True), 99, 0, colors=cols, frame=False,
                dot_speed=0, widths=[4] * 7)
    text(c, 'tangled', 1210, 690, 40, 600, 'c', 1, 'center')
    text(c, 'separated', 1630, 690, 40, 600, 'f', 1, 'center')
    illustration(c, 1010, 745, 1, size=24)
    sticky(c, 1430, 760, ['latent room', '& parameters'], 1, rot=5.0, w=320, h=220)
