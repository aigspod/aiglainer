"""Scenes for this video. Each is a class with `dur` (authored seconds) and `draw(c, t)`, drawing on a 1920x1080
skia canvas at authored time t. Build every animation from ramp()/window() of t, so the narrated cut can
time-warp it. Iterate with `make preview SCENE=Method T="2 6 10"`.

The toolkit (aiglainer/core.py, kit.py, notes.py):
  text, rich (word-by-word reveal; {y:amber} {g:blue} {f:green} {c:coral} {x:lilac} {r:red} {m:muted}), tex (equations),
  header (section title, one *amber italic* word), caption, panel, pill, kicker, stat, Axes, draw_poly,
  legend_item, arrow, flow_dots, hand (handwriting), sticky, lamp, swash; easing ramp/window/e_out/e_io/e_expo.
"""
import math
import numpy as np
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash

class Title(Scene):
    dur = 7.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, 'the aigs pod  ·  /mull/  ·  journal club', x0, 330, ramp(t, 0.2, 0.8), 'muted', 18)
        lamp(c, 1480, 330, 1.7, ramp(t, 0.0, 0.8), on=ramp(t, 0.15, 1.2, e_out))
        k = ramp(t, 0.1, 1.0, e_expo)
        with layer(c, k, (1 - k) * 16):
            w = text(c, '__TITLE__', x0, 520 + (1 - k) * 40, 150, 800, 'ink')
        swash(c, x0, x0 + w, 556, 'y', 1, ramp(t, 0.7, 0.9, e_io), w=4)
        text(c, 'A subtitle in the paper’s own words', x0, 632, 44, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'Author One  ·  Author Two', x0, 720, 30, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, 'venue · year  ·  arxiv:xxxx.xxxxx', x0, 790, ramp(t, 2.6, 0.8), 'muted', 17)
        sticky(c, 1500, 640, ['watch before', 'journal club'], ramp(t, 3.2, 0.5, e_back), rot=5.0)

class Question(Scene):
    dur = 14.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (4.0, 'pop'), (6.0, 'pop')]
    CARDS = [('Why', 'It matters because {y:something real} depends on it.', 'g', 2.0),
             ('Hard', 'It is hard because the {y:obvious approach} fails.', 'c', 4.0),
             ('This paper', 'It proposes {y:one idea} and tests it.', 'f', 6.0)]

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'The *question*')
        cw, gap, y0, ch = 532, 42, 360, 360
        for i, (lab, body, colr, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, lab, x + 36, y0 + 96, 44, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 36, y0 + 180, 32, cw - 72, t, t0 + 0.3, 0.03, 0.45)
        caption(c, t, 'Captions carry {y:one idea} each, in plain words.', 9.0, None, y=900, size=32)

class Method(Scene):
    dur = 14.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (0.8, 'chime'), (4.0, 'draw')]

    def __init__(self):
        d = load_json('curve.json')
        self.curve = np.stack([d['x'], d['y']], 1)

    def draw(self, c, t):
        header(c, t, '02', 'the method', 'How it *works*')
        tex(c, 'main', 480, 560, 80, ramp(t, 0.8, 0.8), reveal=ramp(t, 0.8, 1.2, e_io), glow=6)
        text(c, 'the key equation', 480, 680, 22, 400, 'muted', ramp(t, 1.6, 0.6), 'center', kind='mono')
        ax = Axes(1000, 360, 760, 420, (-3, 3), (0, 1))
        k = ramp(t, 3.0, 0.9, e_expo)
        ax.draw(c, k, [-3, 0, 3], [0, 0.5, 1], prog=k, fmt='{:g}')
        p = ramp(t, 4.0, 2.5, e_io)
        if p > 0:
            draw_poly(c, ax.pts(self.curve[:, 0], self.curve[:, 1]), 'g', 1, 4, prog=p, glow=5)
        legend_item(c, ax.x + 30, ax.y + 40, 'g', 'from data/curve.json', ramp(t, 4.0, 0.6), size=20)
        note(c, 'data extracted from Fig. N', ax.x, ax.y - 16, k * 0.8, 15)

class Takeaway(Scene):
    dur = 12.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (11.0, 'outro')]

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 220, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, 'One sentence that says what the paper {y:showed}, and why it {y:matters}.',
             W / 2, 300, 50, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        for i, (big, small, colr) in enumerate([('0.00', 'the headline number', 'f'), ('N / M', 'a second result', 'c'), ('x → y', 'a third', 'y')]):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * 520, 545, big, small, colr, k, 56)
        k2 = ramp(t, 4.5, 0.9)
        with layer(c, k2):
            line(c, MX, 680, W - MX, 680, 'line', 1, 1.5)
            text(c, 'Authors (Year).  Paper title.  Venue.', MX, 740, 27, 600, 'ink')
            text(c, 'code  github.com/owner/repo', MX, 790, 22, 500, 'g', 1, kind='mono')
        k3 = ramp(t, 6.0, 0.8)
        lamp(c, 1640, 760, 1.15, k3, on=k3)
        hand(c, 'see you at the desk', 1390, 960, 36, 'pencil', k3, -3.0, ramp(t, 6.4, 1.0, e_lin))
