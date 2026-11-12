"""Scenes of the jazz edition. Each lasts whole bars of the 96 bpm grid (beat.py) and narration.py keeps its clock
unwarped, so scene changes fall on the music's phrase boundaries. No cuts: each scene opens its ground over the last
one's colour with a slow iris, or crossfades on the same paper. Drawn with sleeve.py. Everything that looks like data is
abstract art and is labelled `illustration`. Nothing flashes.
"""
import math
from aiglainer.core import *
from aiglainer.timeline import Scene
from beat import BEAT, BAR, b, breathe
from event import WHEN, MORE
from sleeve import *

SPIN = 0.045            # turns a second: the record turns slowly, whatever the scene


class Jazz(Scene):
    fade_in = 0.0
    fade_out = 0.0
    chapter = None
    T0 = 0.0            # the scene's start in the video, to keep the record's spin continuous


def sticker(c, t, t0, cx, cy, r=78):
    """The 'jazz edition' badge, turning softly into place."""
    a, _ = soft(t, t0, 1.0)
    if a <= 0.003:
        return
    with at(c, cx, cy, 0.9 + 0.1 * e_out(clamp((t - t0) / 1.0)), -12 + 6 * (1 - e_out(clamp((t - t0) / 1.2)))):
        circle(c, cx + 4, cy + 6, r, fill='shadow', a=0.3 * a)
        circle(c, cx, cy, r, fill='mustard', a=a)
        circle(c, cx, cy, r - 9, stroke='night', sw=2, a=0.6 * a)
        say(c, 'jazz', cx, cy - 4, 46, 'night', a, 'center', 600, 'ital')
        say(c, 'EDITION', cx, cy + 30, 17, 'night', a, 'center', 700, 'body', track=0.18)


def title_card(c, t, t0, top='THE AIGS POD JOURNAL CLUB PRESENTS', top_kind='label', when_t=5.0, more_t=5.6, out=None):
    """THE AIGS HACKATHON, the date and 'details soon', centred above the record. Used by Title and End."""
    a, dy = soft(t, t0, 1.0, out)
    if top_kind == 'label':
        label(c, top, W / 2, 128 + dy, 20, 'paper', a * 0.75, 'center', track=0.2)
    else:
        say(c, top, W / 2, 140 + dy, 52, 'mustard', a, 'center', 560, 'ital')
    rise(c, t, t0 + 0.3, 'the aigs', W / 2, 272, 112, 'mustard', 'center', 560, 'ital', out=out, d=1.1)
    a2, dy2 = soft(t, t0 + 0.9, 1.3, out)
    size = fit('HACKATHON', 236, W - 2 * PAD - 60, 640)
    with at(c, W / 2, 400, 0.94 + 0.06 * e_out(clamp((t - t0 - 0.9) / 1.6))):
        say(c, 'HACKATHON', W / 2, 482 + dy2 * 0.6, size, 'paper', a2, 'center', 640, shadow=0.5)
    rise(c, t, when_t, WHEN, W / 2, 588, 70, 'paper', 'center', 500, 'ital', out=out)
    a3, dy3 = soft(t, more_t, 0.9, out)
    label(c, MORE.upper(), W / 2, 640 + dy3, 22, 'mustard', a3, 'center', bold=True, track=0.3)


# ---------------------------------------------------------------- 1. the hook: a planet on a record, at night
class Hook(Jazz):
    dur = 20.0
    P0, P1 = (1380, 560, 380), (960, 1340, 540)

    def draw(self, c, t):
        slab(c, 'night')
        glow(c, 1380, 560, 700, 'teal', 0.5 * ramp(t, 0, 3))
        stars(c, t, ramp(t, 0.2, 2.5))
        k = ramp(t, 17.3, 2.7, e_io)                         # glide down to become the title's rising record
        x = lerp(self.P0[0], self.P1[0], k)
        y = lerp(self.P0[1], self.P1[1], k) + 60 * (1 - ramp(t, 0.3, 2.4, e_out))
        R = lerp(self.P0[2], self.P1[2], k)
        spin = SPIN * (self.T0 + t)
        planet_a = 1 - ramp(t, 12.0, 1.6, e_io)
        net_a = ramp(t, 12.0, 1.6, e_io) * (1 - ramp(t, 17.6, 1.8, e_io))
        lab_a = ramp(t, 17.6, 1.8, e_io)

        def inner(c, cx, cy, r):
            circle(c, cx, cy, r, fill='night', a=1)
            planet(c, cx, cy, r, t, spin * 3, a=planet_a)
            network(c, cx, cy, r, t, 'paper', 'mustard', net_a)
            if lab_a > 0:
                with layer(c, lab_a):
                    label_art(c, cx, cy, r, spin)
        record(c, x, y, R, t, spin, a=ramp(t, 0.3, 2.0), inner=inner, lab=lerp(0.5, 0.36, k))
        illustration(c, x, y + R + 44, 'paper', ramp(t, 1.5, 1.0) * (1 - ramp(t, 16.8, 0.6)), 'center')
        # line 1
        o1 = 10.2
        rise(c, t, 3.4, 'machine-learned', PAD, 330, 62, 'mustard', kind='ital', weight=520, out=o1)
        rise(c, t, 3.9, 'climate', PAD, 480, 144, 'paper', out=o1, shadow=0.4)
        rise(c, t, 4.4, 'emulators', PAD, 628, 144, 'paper', out=o1, shadow=0.4)
        rise(c, t, 6.2, 'can carry a whole planet', PAD + 4, 712, 40, 'paper', kind='body', weight=400, out=o1)
        rise(c, t, 6.9, 'forward in time.', PAD + 4, 764, 40, 'paper', kind='body', weight=400, out=o1)
        # line 2
        o2 = 16.9
        rise(c, t, 11.3, 'but what is really', PAD, 360, 62, 'mustard', kind='ital', weight=520, out=o2)
        rise(c, t, 12.0, 'going on,', PAD, 520, 144, 'paper', out=o2, shadow=0.4)
        rise(c, t, 12.7, 'inside them?', PAD, 676, 144, 'paper', out=o2, shadow=0.4)
        vignette(c, 0.4)


# ---------------------------------------------------------------- 2. the title: the record rises like a sun
class Title(Jazz):
    dur = 15.0
    T0 = 20.0

    def draw(self, c, t):
        slab(c, 'night')
        stars(c, t + 20, 0.8, y1=700)
        sink = ramp(t, 13.4, 1.6, e_in)
        cx, cy, R = 960, 1340 + 520 * sink, 540
        glow(c, cx, cy - 200, 900, 'mustard', 0.16 * ramp(t, 0, 2.0) * (1 - sink))
        arcs(c, cx, cy, R + 20, t, ('mustard', 'terra', 'sage'), a=1 - ramp(t, 13.2, 1.0), width=10, gap=22,
             grow=ramp(t, 0.0, 2.6, e_out))
        record(c, cx, cy, R, t, SPIN * (self.T0 + t))
        title_card(c, t, 0.2, out=13.9)
        a = 1 - ramp(t, 13.9, 0.6)
        if a > 0.003:
            with layer(c, a):
                sticker(c, t, 3.75, 1700, 182)
        vignette(c, 0.4)


# ---------------------------------------------------------------- 3. the models, in two portholes
class Models(Jazz):
    dur = 10.0
    L, Rr, CY, R = 560, 1360, 520, 230

    def draw(self, c, t):
        slab(c, 'paper')
        iris(c, t, 'night', 960, 1100, 1.4)
        out = 9.2
        rise(c, t, 1.2, 'together, let’s open them up', W / 2, 170, 64, 'terra', 'center', 520, 'ital', out=out)
        self.samudrace(c, t, out)
        self.ace(c, t, out)

    def porthole(self, c, t, cx, t0, out):
        a, dy = soft(t, t0, 1.0, out)
        k = 0.92 + 0.08 * e_out(clamp((t - t0) / 1.2))
        return a, dy, k

    def samudrace(self, c, t, out):
        cx, cy, R = self.L, self.CY, self.R
        a, dy, k = self.porthole(c, t, cx, 1.0, out)
        if a <= 0.003:
            return
        reveal = ramp(t, 2.2, 1.6, e_io)
        with layer(c, a), at(c, cx, cy + dy, k):
            c.drawCircle(cx + 5, cy + 9, R, paint('shadow', 0.25, blur=14))
            circle(c, cx, cy, R, fill='night', a=1)
            c.save()
            pth = skia.Path()
            pth.addCircle(cx, cy, R * (0.15 + 0.85 * reveal) if reveal > 0 else 0.1)
            c.clipPath(pth, doAntiAlias=True)
            c.drawRect(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, R), paint('panel2'))
            breeze(c, cx - R, cy - R, 2 * R, R - 10, t, 'terra', 0.9, step=36, seg=24, width=4)
            c.drawRect(skia.Rect.MakeXYWH(cx - R, cy, 2 * R, R), paint('teal'))
            waves(c, cx - R, cy + 18, 2 * R, R - 30, t, 'paper', 0.8, rows=6, width=3.5)
            for i in range(5):            # the coupling: fluxes up and down between the two, breathing slowly
                ax = cx - 2 * R / 3 + i * R / 3
                up = i % 2 == 0
                bob = 6 * math.sin(t * 1.3 + i)
                y0, y1 = (cy + 34 + bob, cy - 34 + bob) if up else (cy - 34 + bob, cy + 34 + bob)
                arrow(c, ax, y0, ax, y1, 'mustard', 0.95, 5, 15)
            c.restore()
            circle(c, cx, cy, R, stroke='ink', sw=3, a=0.85)
        illustration(c, cx, cy + R + 40, 'muted', a, 'center')
        rise(c, t, 3.0, 'SamudrACE', cx, cy + R + 118, 70, 'ink', 'center', 640, out=out)
        rise(c, t, 3.5, 'coupled ocean + atmosphere emulator', cx, cy + R + 166, 28, 'muted', 'center', 450, 'body', out=out)
        a2, dy2 = soft(t, 3.9, 0.9, out)
        label(c, 'Ai2  ·  E3SM', cx, cy + R + 208 + dy2, 20, 'terra', a2, 'center', bold=True)

    def ace(self, c, t, out):
        cx, cy, R = self.Rr, self.CY, self.R
        a, dy, k = self.porthole(c, t, cx, 1.4, out)
        if a <= 0.003:
            return
        reveal = ramp(t, 2.6, 1.6, e_io)
        with layer(c, a), at(c, cx, cy + dy, k):
            c.drawCircle(cx + 5, cy + 9, R, paint('shadow', 0.25, blur=14))
            circle(c, cx, cy, R, fill='night', a=1)
            stars_in = 0.6 * reveal
            for i in range(26):
                ang = _star(i)
                circle(c, cx + R * 0.88 * math.cos(ang[0]), cy + R * 0.88 * math.sin(ang[0]), ang[1], fill='paper', a=stars_in)
            planet(c, cx, cy, R * 0.66 * (0.3 + 0.7 * reveal), t, 0.04 * t, a=reveal)
            c.drawArc(skia.Rect.MakeXYWH(cx - R * 0.8, cy - R * 0.25, R * 1.6, R * 0.5), 200, 140, False,
                      paint('mustard', 0.8 * reveal, stroke=3))
            circle(c, cx, cy, R, stroke='ink', sw=3, a=0.85)
        illustration(c, cx, cy + R + 40, 'muted', a, 'center')
        rise(c, t, 3.4, 'ACE', cx, cy + R + 118, 70, 'ink', 'center', 640, out=out)
        rise(c, t, 3.9, 'climate emulator', cx, cy + R + 166, 28, 'muted', 'center', 450, 'body', out=out)


def _star(i):
    h = math.sin(i * 91.7 + 3.1) * 43758.5453
    h -= math.floor(h)
    g = math.sin(i * 17.3 + 1.7) * 23421.631
    g -= math.floor(g)
    return h * 6.283, 1.5 + 2.0 * g


# ---------------------------------------------------------------- 4. the tools: exege and four papers, like LPs
PAPERS = [('Seeing Through Circuits', 'circuits in vision transformers', 'night', 'paper'),
          ('LAWFUL', 'checking models against physical laws', 'terra', 'paper'),
          ('Errors', 'do circuits explain model errors?', 'mustard', 'ink'),
          ('Dynamics', 'transformers as dynamical systems', 'teal', 'paper')]


class Tools(Jazz):
    dur = 10.0

    def draw(self, c, t):
        slab(c, 'paper')
        out = 9.2
        rise(c, t, 0.8, 'exege', PAD - 6, 330, 210, 'ink', weight=640, out=out)
        rise(c, t, 1.5, 'our toolkit for latent diagnostics', PAD + 4, 428, 32, 'muted', kind='body', weight=450, out=out)
        self.grid(c, t, out)
        rise(c, t, 3.3, '+ ideas from four journal club papers', PAD + 2, 520, 32, 'ink', kind='body', weight=600, out=out)
        s, gap, y = 380, 40, 572
        for k, (title, desc, bg, fg) in enumerate(PAPERS):
            a, dy = soft(t, 4.0 + 0.45 * k, 1.0, out)
            if a <= 0.003:
                continue
            x = PAD + k * (s + gap)
            yy = y + dy * 1.6
            with layer(c, a):
                sleeve(c, x, yy, s, bg)
                emblem(c, k, x + s - 92, yy + 92, 58, fg, t)
                label(c, f'PAPER 0{k + 1}', x + 28, yy + 48, 17, fg, 0.85, bold=True)
                dl = wrap(desc, 22, s - 60, 450, 'body')
                for i, ln in enumerate(dl):
                    say(c, ln, x + 28, yy + s - 38 - (len(dl) - 1 - i) * 30, 22, fg, 0.92, 'left', 450, 'body', 0)
                lines = wrap(title, 48, s - 60, 620)
                base = yy + s - 38 - (len(dl) - 1) * 30 - 62          # titles sit on the description, never in it
                for i, ln in enumerate(lines):
                    say(c, ln, x + 28, base - (len(lines) - 1 - i) * 54, 48, fg, 1, 'left', 620)

    def grid(self, c, t, out):
        x0, y0, n, m, s, g = 1210, 150, 10, 5, 46, 10
        for i in range(n):
            for j in range(m):
                a, _ = soft(t, 1.0 + 0.04 * (i + j), 0.8, out)
                if a <= 0.003:
                    continue
                v = 0.5 + 0.5 * math.sin(i * 0.9 + j * 1.7 + t * 0.5) * math.cos(j * 0.6 - i * 0.3 + t * 0.33)
                colr = 'mustard' if v > 0.9 else 'teal'
                c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0 + i * (s + g), y0 + j * (s + g), s, s), 8, 8),
                            paint(colr, a * (0.15 + 0.85 * v)))
        illustration(c, x0, y0 + m * (s + g) + 26, 'muted', soft(t, 1.4, 0.8, out)[0])


def emblem(c, k, cx, cy, r, colr, t):
    """A small mid-century mark per paper sleeve (decoration)."""
    if k == 0:                       # circuits: a node with three branches
        for ang in (-150, -30, 90):
            a = math.radians(ang)
            line(c, cx, cy, cx + r * math.cos(a), cy + r * math.sin(a), colr, 0.9, 4)
            circle(c, cx + r * math.cos(a), cy + r * math.sin(a), 9, fill=colr, a=0.9)
        circle(c, cx, cy, 14, fill='mustard', a=1)
    elif k == 1:                     # laws: a balance of arcs
        for i in range(3):
            c.drawArc(skia.Rect.MakeXYWH(cx - r + i * 14, cy - r + i * 14, 2 * (r - i * 14), 2 * (r - i * 14)), 180, 180, False,
                      paint(colr, 0.9 - 0.25 * i, stroke=6, cap='butt'))
        line(c, cx - r, cy + 4, cx + r, cy + 4, colr, 0.9, 4)
    elif k == 2:                     # errors: a cross in a ring
        circle(c, cx, cy, r * 0.8, stroke=colr, sw=5, a=0.9)
        s = r * 0.35
        line(c, cx - s, cy - s, cx + s, cy + s, 'terra', 1, 7)
        line(c, cx - s, cy + s, cx + s, cy - s, 'terra', 1, 7)
    else:                            # dynamics: a slow spiral
        pts = [(cx + r * (u / 6.3) ** 0.8 * math.cos(u + t * 0.3), cy + r * (u / 6.3) ** 0.8 * math.sin(u + t * 0.3))
               for u in [i * 0.15 for i in range(43)]]
        draw_poly(c, pts, colr, 0.9, 4)


# ---------------------------------------------------------------- 5. the open questions, after hours
QUESTIONS = [
    [('Does the ocean read', 'paper'), ('a heat flux as heat…', 'paper'), ('or as a thermometer?', 'mustard')],
    [('Which path carries', 'paper'), ('the CO₂ signal?', 'mustard')],
    [('Local,', 'paper'), ('or basin-scale?', 'mustard')],
    [('Good forecasts,', 'paper'), ('but a sound', 'paper'), ('inner state?', 'mustard')],
    [('Do our explanations', 'paper'), ('keep the model’s', 'paper'), ('mistakes?', 'mustard')],
]


class Questions(Jazz):
    dur = 32.5
    Q0 = b(3)            # the first question arrives with the chorus, after the three-bar lift
    QL = 2 * BAR         # each question holds for two bars
    CX, CY, R = 1440, 540, 270

    def draw(self, c, t):
        slab(c, 'night')
        iris(c, t, 'paper', 960, 540, 1.4)
        stars(c, t, 0.7 * ramp(t, 0.6, 2.0), seed=9)
        if t < self.Q0:
            self.intro(c, t)
        else:
            q = min(int((t - self.Q0) / self.QL), 4)
            self.card(c, t, q, self.Q0 + q * self.QL)
        vignette(c, 0.4)

    def intro(self, c, t):
        out = self.Q0 - 0.85
        rise(c, t, 1.1, 'and here’s the best part', W / 2, 380, 66, 'mustard', 'center', 520, 'ital', out=out)
        words(c, t, 2.9, 'Nobody knows the answers', W / 2, 560, 120, 'paper', align='center', out=out)
        rise(c, t, 4.4, 'yet.', W / 2, 726, 156, 'mustard', 'center', out=out, d=1.2)
        a, dy = soft(t, 5.2, 0.9, out)
        label(c, 'FIVE OPEN QUESTIONS', W / 2, 860 + dy, 22, 'paper', a * 0.85, 'center', track=0.3)
        for k in range(5):
            circle(c, W / 2 - 80 + k * 40, 905 + dy, 7, fill='mustard', a=soft(t, 5.5 + 0.12 * k, 0.6, out)[0])

    def card(self, c, t, q, t0):
        out = t0 + self.QL - 0.7 if q < 4 else self.dur - 0.8
        a, dy = soft(t, t0 + 0.15, 0.9, out, 0.55)
        glow(c, self.CX, self.CY, 520, 'teal', 0.55)
        label(c, f'OPEN QUESTION {q + 1} OF 5', PAD, 250 + dy, 20, 'mustard', a, bold=True, track=0.24)
        lines = QUESTIONS[q]
        size = 118 if q == 2 else 92
        size = min(fit(s, size, 1060, 620) for s, _ in lines)
        y = 440 if len(lines) == 3 else 500
        for i, (s, colr) in enumerate(lines):
            rise(c, t, t0 + 0.35 + 0.35 * i, s, PAD, y + i * size * 1.18, size, colr, out=out, shadow=0.4)
        art_a, _ = soft(t, t0 + 0.2, 1.1, out, 0.55)
        if art_a > 0.003:
            with layer(c, art_a):
                cx, cy, R = self.CX, self.CY, self.R
                circle(c, cx, cy, R, fill='#16203a', a=1)
                c.save()
                pth = skia.Path()
                pth.addCircle(cx, cy, R)
                c.clipPath(pth, doAntiAlias=True)
                getattr(self, f'q{q + 1}')(c, t, t0, cx, cy, R)
                c.restore()
                circle(c, cx, cy, R, stroke='paper', sw=3, a=0.35)
            illustration(c, self.CX, self.CY + self.R + 44, 'paper', art_a, 'center')

    def q1(self, c, t, t0, cx, cy, R):
        c.drawRect(skia.Rect.MakeXYWH(cx - R, cy + 20, 2 * R, R), paint('teal'))
        waves(c, cx - R, cy + 40, 2 * R, R - 40, t, 'paper', 0.75, rows=6)
        for i in range(4):
            ax = cx - 200 + i * 92
            bob = 10 * math.sin(t * 1.4 + i * 0.8)
            arrow(c, ax, cy - 160 + bob, ax, cy - 10 + bob, 'terra', 0.95, 6, 18)
        k = ramp(t, t0 + 2.2, 1.0, e_out)
        thermometer(c, cx + 175, cy - 170 + 20 * (1 - k), 210, 0.45 + 0.1 * math.sin(t * 0.8), 'paper', 'terra', k, sw=7)

    def q2(self, c, t, t0, cx, cy, R):
        A = [(cx - 200, cy), (cx + 200, cy)]
        B = [(cx - 200, cy), (cx - 110, cy + 110), (cx, cy + 140), (cx + 110, cy + 110), (cx + 200, cy)]
        k = ramp(t, t0 + 0.4, 1.2, e_io)
        draw_poly(c, A, 'paper', 0.6, 4, prog=k)
        draw_poly(c, B, 'paper', 0.6, 4, prog=k)
        for p in B[1:-1]:
            circle(c, *p, 10, fill='teal', stroke='paper', sw=3, a=k)
        circle(c, *A[0], 18, fill='paper', a=k)
        circle(c, *A[1], 18, fill='paper', a=k)
        label(c, 'path a', cx, cy - 22, 17, 'paper', 0.8 * k, 'center')
        label(c, 'path b', cx, cy + 186, 17, 'paper', 0.8 * k, 'center')
        if t > t0 + 1.4:
            ph = ((t - t0 - 1.4) / 3.0) % 1.0
            circle(c, *end_point(A, ph), 11, fill='mustard', a=1, glow=8)
            circle(c, *end_point(B, ph), 11, fill='rose', a=1, glow=8)
        say(c, '?', cx + 200, cy - 50, 64, 'mustard', k, 'center', 600, 'ital')

    def q3(self, c, t, t0, cx, cy, R):
        x, y = cx - 70, cy - 40
        for k in range(4):
            u = ((t - t0) / 3.2 + k / 4) % 1.0
            circle(c, x, y, 20 + 330 * u, stroke='mustard', sw=4, a=0.7 * (1 - u) * ramp(t, t0 + 0.4, 0.8))
        circle(c, x, y, 12, fill='mustard', a=1)
        circle(c, x, y, 32, stroke='paper', sw=3, a=0.8)

    def q4(self, c, t, t0, cx, cy, R):
        x0, y0, w, h = cx - 220, cy + 40, 440, 140
        pts = [(x0 + w * i / 80, y0 + h / 2 + h * 0.36 * (math.sin(i / 7.0) * 0.7 + 0.3 * math.sin(i / 2.3 + 1))) for i in range(81)]
        draw_poly(c, pts, 'mustard', 1, 5, prog=ramp(t, t0 + 0.3, 2.6, e_io))
        line(c, x0, y0 + h, x0 + w, y0 + h, 'paper', 0.4, 2)
        a = ramp(t, t0 + 1.6, 0.9)
        rrect(c, cx - 80, cy - 200, 160, 160, 14, stroke='paper', sw=5, a=a)
        say(c, '?', cx, cy - 72, 110, 'paper', a * (0.75 + 0.25 * breathe(t)), 'center', 600, 'ital')
        label(c, 'inner state', cx, cy - 218, 17, 'paper', a * 0.85, 'center')

    def q5(self, c, t, t0, cx, cy, R):
        for i in range(9):
            for j in range(8):
                x, y = cx - 200 + i * 50, cy - 175 + j * 50
                h = math.sin(i * 12.9898 + j * 78.233) * 43758.5453 % 1.0
                if h > 0.86:
                    s = 12
                    line(c, x - s, y - s, x + s, y + s, 'terra', 1, 5)
                    line(c, x - s, y + s, x + s, y - s, 'terra', 1, 5)
                    if h > 0.93:
                        circle(c, x, y, 25, stroke='mustard', sw=4, a=ramp(t, t0 + 1.4, 0.9))
                else:
                    circle(c, x, y, 5, fill='paper', a=0.4)


# ---------------------------------------------------------------- 6. six tracks: the back of the sleeve
TRACKS = ['Ocean shortcut', 'Ocean routing', 'Atmosphere CO₂', 'Errors & strata', 'Dynamics', 'Exege integration']


class Tracks(Jazz):
    dur = 10.0
    T0 = 87.5

    def draw(self, c, t):
        slab(c, 'paper')
        iris(c, t, 'night', 1440, 540, 1.4)
        out = 9.2
        a, dy = soft(t, 0.6, 1.2, out)
        with layer(c, a):
            record(c, 1600, 250 + dy, 150, t, SPIN * (self.T0 + t), 'teal', label_text='SIX TRACKS  ·  SIX TRACKS  ·  ')
        rise(c, t, 1.0, 'Six tracks', PAD - 4, 300, 144, 'ink', weight=640, out=out)
        rise(c, t, 2.6, 'from the ocean, to the atmosphere, to the code', PAD, 378, 44, 'terra', weight=520, kind='ital', out=out)
        for k, name in enumerate(TRACKS):
            col_, row = k // 3, k % 3
            x, y = PAD + col_ * 840, 548 + row * 140
            a, dy = soft(t, 1.8 + 0.42 * k, 0.9, out)
            if a <= 0.003:
                continue
            say(c, f'{k + 1}', x, y + dy, 60, 'terra', a, 'left', 560, 'ital')
            say(c, name, x + 78, y + dy, 58, 'ink', a, 'left', 600)
            line(c, x, y + 38 + dy, x + 740, y + 38 + dy, 'faint', a, 2, dash=[2, 9])


# ---------------------------------------------------------------- 7. welcome: there's a seat for you
class Welcome(Jazz):
    dur = 10.0
    CX, CY = 1490, 560

    def draw(self, c, t):
        slab(c, 'teal')
        iris(c, t, 'paper', 960, 540, 1.4)
        out = 9.4
        glow(c, self.CX, self.CY, 560, 'mustard', 0.22 * ramp(t, 0.6, 1.5) * (1 - ramp(t, out, 0.6)))
        self.table(c, t, out)
        o1 = 6.4
        size = fit('New to interpretability?', 86, 1000)
        rise(c, t, 1.1, 'New to interpretability?', PAD, 360, size, 'paper', out=o1, shadow=0.35)
        rise(c, t, 3.1, 'A climate scientist?', PAD, 500, size, 'mustard', out=o1, shadow=0.35)
        rise(c, t, 4.7, 'A total beginner?', PAD, 640, size, 'rose', out=o1, shadow=0.35)
        rise(c, t, 7.0, 'you are', PAD, 420, 84, 'paper', weight=520, kind='ital', out=out)
        rise(c, t, 7.4, 'so welcome', PAD - 4, 590, 156, 'mustard', out=out, shadow=0.35)
        rise(c, t, 7.9, 'here.', PAD - 4, 750, 156, 'mustard', out=out, shadow=0.35)
        sa = 1 - ramp(t, out, 0.6)
        swash(c, PAD, 790, 380, ramp(t, 8.3, 0.9, e_io), 'paper', sa * 0.9, 6)

    def table(self, c, t, out):
        cx, cy = self.CX, self.CY
        a, dy = soft(t, 0.9, 1.1, out)
        if a <= 0.003:
            return
        with layer(c, a):
            c.drawCircle(cx + 6, cy + 12 + dy, 150, paint('shadow', 0.3, blur=16))
            circle(c, cx, cy + dy, 150, fill='sage', a=1)
            circle(c, cx, cy + dy, 118, stroke='paper', sw=2, a=0.35)
            circle(c, cx - 30, cy - 20 + dy, 26, fill='paper', a=0.9)                  # two cups on the table
            circle(c, cx + 44, cy + 30 + dy, 22, fill='paper', a=0.9)
            circle(c, cx - 30, cy - 20 + dy, 16, fill='terra', a=0.8)
            circle(c, cx + 44, cy + 30 + dy, 13, fill='terra', a=0.8)
        for k in range(7):
            ang = math.radians(180 + k * 360 / 7)
            x, y = cx + 238 * math.cos(ang), cy + 238 * math.sin(ang)
            ak, dk = soft(t, 1.3 + 0.16 * k, 0.8, out)
            if k == 0:                   # the empty seat nearest the words, kept for you
                g = 0.6 + 0.4 * breathe(t, 0, 3.0)
                w = ramp(t, 7.3, 1.2)
                circle(c, x, y + dk, 46, fill='mustard', a=ak, glow=10 + 16 * w * g)
                circle(c, x, y + dk, 46, stroke='paper', sw=3, a=ak * (0.4 + 0.5 * w))
            else:
                circle(c, x, y + dk, 42, fill='paper', a=ak * 0.85)


# ---------------------------------------------------------------- 8. the end card
class End(Jazz):
    dur = 15.0
    T0 = 107.5

    def draw(self, c, t):
        slab(c, 'night')
        iris(c, t, 'teal', 960, 1100, 1.5)
        stars(c, t + 107.5, 0.8 * ramp(t, 0.5, 2.0), y1=700)
        up = ramp(t, 0.3, 2.4, e_out)
        cx, cy, R = 960, 1340 + 380 * (1 - up), 540
        glow(c, cx, cy - 200, 900, 'mustard', 0.16 * up)
        arcs(c, cx, cy, R + 20, t, ('mustard', 'terra', 'sage'), width=10, gap=22, grow=ramp(t, 1.2, 2.6, e_out))
        record(c, cx, cy, R, t, SPIN * (self.T0 + t))
        title_card(c, t, 0.8, 'come and join us', 'ital', when_t=2.9, more_t=4.8)
        sticker(c, t, 3.4, 1700, 182)
        vignette(c, 0.4)
