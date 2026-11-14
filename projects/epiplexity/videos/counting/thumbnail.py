"""The thumbnail: the four files (computed, as in the video) and the question. Heaviest display weights only;
nothing important bottom-right (the duration badge sits there)."""
from countkit import *

def draw(c):
    x0 = 110
    text(c, 'Who’s', x0, 430, 230, 900, 'ink', kind='display')
    w = text(c, 'counting?', x0, 660, 220, 700, 'y', kind='italic')
    from aiglainer.notes import swash
    swash(c, x0, x0 + w - 60, 712, 'y', 1, 1, w=9)
    text(c, 'shannon vs epiplexity', x0 + 8, 860, 72, 700, 'ink', 1, kind='mono')
    s, gap = 270, 40
    for i, (key, _, _) in enumerate(FILES):
        x = 1230 + (i % 2) * (s + gap)
        y = 120 + (i // 2) * (s + gap + 20)
        if key == 'ca':
            y += 30
            h = s * 49 / 64
            rrect(c, x - 16, y - 16, s + 32, h + 32, 16, fill='y', fa=0.18, glow=24)
            rrect(c, x - 16, y - 16, s + 32, h + 32, 16, stroke='y', sw=5)
        if key == 'ca':
            rrect(c, x - 6, y - 6, s + 12, h + 12, 8, fill='panel', fa=0.9)
            draw_grid(c, bit_image('ca_amber', file_bits('ca'), 6, 1, 'y', 'panel2'), x, y, s, h, 1)
        else:
            file_thumb(c, key, x, y, s, 1, cell=6)
