"""Scenes of the hackathon invitation. Each lasts whole bars of the 120 bpm grid (beat.py) and narration.py keeps its
clock unwarped, so a hit authored at b(bar, beat) lands on that beat of music.py's track. Hard cuts: no fades.
Drawn with poster.py. Everything that looks like data is abstract art and is labelled `illustration`.
"""
import math
from aiglainer.core import *
from aiglainer.timeline import Scene
from beat import BEAT, BAR, b, kick
from event import WHEN, MORE
from poster import *


class Poster(Scene):
    fade_in = 0.0
    fade_out = 0.0
    chapter = None


def wrap(s, size, maxw):
    lines, cur = [], ''
    for w in s.split():
        trial = (cur + ' ' + w).strip()
        if cur and tw(trial, size) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + [cur]


def when_lines():
    s = WHEN.upper()
    return ['WEEK OF', s[8:]] if s.startswith('WEEK OF ') else [s]


def out_glitch(t, t1, d=0.35):
    return ramp(t, t1 - d, d, e_in)


# ---------------------------------------------------------------- 1. hook, build, title drop
class Hook(Poster):
    dur = 20.0
    cues = [(b(6), 'impact'), (b(6, 2), 'stamp_soft'), (b(8), 'whoosh')]
    CX, CY, R = 1450, 560, 330

    def draw(self, c, t):
        if t < b(5, 3.5):
            amt = max(0.5 * window(t, 3.85, 4.05, 0.05, 0.05), 0.5 * window(t, 6.8, 7.05, 0.05, 0.05), 0.85 * ramp(t, b(5), BAR - BEAT / 2, e_in))
            glitch(c, lambda: self.open(c, t), amt, t, seed=1)
            if t >= b(5, 2):          # the snare roll's last beat: flicker on sixteenths
                if int((t - b(5, 2)) * 8) % 2 == 0:
                    slab(c, 'night', 0.85)
        elif t < b(6):
            slab(c, 'night')          # the breath before the drop
        else:
            amt = 0.6 * window(t, b(6), b(6) + 0.12, 0.01, 0.1) + 0.6 * window(t, b(8), b(8) + 0.12, 0.01, 0.1) + out_glitch(t, self.dur)
            glitch(c, lambda: self.drop(c, t), amt, t, seed=2)

    def open(self, c, t):
        spin = 0.2 * t + 3.2 * e_io(clamp((t - 4.6) / 3.0))
        hollow = 0.82 * ramp(t, 7.0, 1.0, e_io)
        globe(c, self.CX, self.CY, self.R, t, spin, reveal=ramp(t, 0.0, 1.6, e_out), hollow=hollow, air_amt=0.5 + 0.5 * ramp(t, 4.5, 2))
        if hollow > 0:
            circle(c, self.CX, self.CY, self.R + 6, stroke='cobalt', sw=4, a=ramp(t, 7.0, 0.5))
            network(c, self.CX - 210, self.CY - 150, 420, 300, t, 'ink', 'orange', ramp(t, 7.3, 0.6), speed=1 + 2 * ramp(t, b(4), BAR * 2, e_in))
        illustration(c, self.CX, self.CY + self.R + 60, 'muted', ramp(t, 1.0, 0.6), 'center')
        tag(c, 'THE AIGS POD  ·  JOURNAL CLUB', PAD, 140, 20, 'paper', 'ink', ramp(t, 0.3, 0.3))
        # line 1, in two waves of words on the beat
        o1 = 3.85
        slam_word(c, t, 1.0, 'MACHINE-LEARNED', PAD, 330, 64, 'ink', out=o1)
        slam_word(c, t, 1.5, 'CLIMATE', PAD, 490, 150, 'ink', out=o1)
        slam_word(c, t, 2.0, 'EMULATORS', PAD, 640, 150, 'orange', out=o1)
        o2 = 6.8
        for k, (s, colr) in enumerate([('A WHOLE', 'ink'), ('PLANET', 'cobalt'), ('FORWARD', 'ink'), ('IN TIME.', 'orange')]):
            slam_word(c, t, 4.0 + k * BEAT, s, PAD, 360 + k * 135, 130, colr, out=o2)
        # line 2: the question, misregistering as the build rises
        px = 10 * ramp(t, b(4, 1), BAR * 1.6, e_in)
        for k, (s, colr) in enumerate([("WHAT’S", 'ink'), ('GOING ON', 'ink'), ('INSIDE?', 'orange')]):
            slam_word(c, t, 7.5 + k * BEAT, s, PAD, 420 + k * 160, 150, colr, riso=('cobalt', 'lime', px))
        scanlines(c, t, 0.10 * ramp(t, b(4), BAR * 2, e_in))

    def drop(self, c, t):
        if t < b(8):
            slab(c, 'cobalt')
            stripes(c, t, 'lime', 0.10, speed=180)
            px = 5 * kick(t, b(6))
            s1 = fit('THE AIGS', 250, W - 2 * PAD)
            s2 = fit('HACKATHON', 250, W - 2 * PAD)
            slam_word(c, t, b(6), 'THE AIGS', PAD, 470, s1, 'paper', riso=('orange', 'lime', px), pump=0.015)
            slam_word(c, t, b(6, 2), 'HACKATHON', PAD, 720, s2, 'lime', riso=('orange', 'night', px), pump=0.015)
            tag(c, 'FROM THE AIGS POD JOURNAL CLUB COMMUNITY', PAD + 4, 860, 24, 'cobalt', 'paper', ramp(t, b(7), 0.15))
        else:
            slab(c, 'orange')
            stripes(c, t, 'night', 0.07, speed=-160)
            lines = when_lines()
            y = 420 if len(lines) == 2 else 560
            for k, s in enumerate(lines):
                size = fit(s, 130 if (k == 0 and len(lines) == 2) else 240, W - 2 * PAD)
                slam_word(c, t, b(8, 2 * k), s, PAD, y + k * 240, size, 'ink', riso=('paper', 'cobalt', 4 * kick(t, b(8))), pump=0.012)
            tag(c, MORE.upper(), PAD + 4, 830, 30, 'lime', 'night', ramp(t, b(9), 0.12))


# ---------------------------------------------------------------- 2. the models
class Models(Poster):
    dur = 10.0
    cues = [(0.0, 'whoosh'), (b(3), 'stamp')]

    def draw(self, c, t):
        glitch(c, lambda: self.body(c, t), out_glitch(t, self.dur), t, seed=3)

    def body(self, c, t):
        tag(c, '01 / THE MODELS', PAD, 140, 20, 'paper', 'ink', ramp(t, 0.1, 0.2))
        # SamudrACE: an atmosphere over an ocean, coupled
        k = ramp(t, 0.0, 0.4, e_out)
        x, y, w, h = PAD - (1 - k) * 1000, 200, 830, 700
        slab(c, 'cobalt', 1, x, y, w, h)
        big(c, 'SAMUDRACE', x + 40, y + 120, fit('SAMUDRACE', 112, w - 80), 'paper')
        mono(c, 'coupled ocean + atmosphere emulator', x + 44, y + 170, 22, 'paper')
        mono(c, 'Ai2  ·  E3SM', x + 44, y + 205, 22, 'lime')
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(x + 30, y + 240, w - 60, 420))
        flow(c, x + 30, y + 240, w - 60, 170, t, 'orange', 0.95, step=34)
        waves(c, x + 30, y + 500, w - 60, 160, t, 'paper', 0.9, rows=6)
        for i in range(5):            # the coupling: fluxes up and down between the two, on the beat
            ax = x + 110 + i * 150
            up = i % 2 == 0
            pk = kick(t, 0.0, decay=5)
            y0, y1 = (y + 485, y + 420) if up else (y + 420, y + 485)
            arrow(c, ax, y0, ax, y1, 'lime', 0.6 + 0.4 * pk, 5, 16)
        c.restore()
        illustration(c, x + 44, y + h - 20, 'paper', 1)
        # ACE
        k2 = ramp(t, 1.0, 0.4, e_out)
        x2 = 990 + (1 - k2) * 1000
        slab(c, 'paper', 1, x2, y, 810, h)
        c.drawRect(skia.Rect.MakeXYWH(x2 + 4, y + 4, 802, h - 8), paint('ink', 1, stroke=8, cap='butt'))
        big(c, 'ACE', x2 + 40, y + 150, 170, 'ink')
        mono(c, 'climate emulator', x2 + 44, y + 205, 22, 'ink')
        globe(c, x2 + 405, y + 470, 190, t, 0.25 * t, sea='ink', air='orange', step=11, a=k2)
        illustration(c, x2 + 44, y + h - 20, 'ink', k2)
        # the banner
        a, sc = slam(t, b(3))
        if a > 0:
            with at(c, W / 2, 560, sc * (1 + 0.012 * kick(t, b(3))), -4):
                slab(c, 'night', a, -200, 460, W + 400, 200)
                big(c, 'OPEN THEM UP.', W / 2, 615, 150, 'paper', a, 'center', riso=('orange', 'lime', 4 * kick(t, b(3))))


# ---------------------------------------------------------------- 3. the tools
PAPERS = [('SEEING THROUGH CIRCUITS', 'circuits in vision transformers', 'orange', 'ink'),
          ('LAWFUL', 'checking models against physical laws', 'cobalt', 'paper'),
          ('ERRORS', 'do circuits explain model errors?', 'lime', 'ink'),
          ('DYNAMICS', 'transformers as dynamical systems', 'night', 'paper')]


class Tools(Poster):
    dur = 10.0
    cues = [(0.0, 'whoosh')] + [(b(1, 2 + k), 'tick') for k in range(4)]

    def draw(self, c, t):
        glitch(c, lambda: self.body(c, t), out_glitch(t, self.dur), t, seed=4)

    def body(self, c, t):
        slam_word(c, t, 0.0, 'EXEGE', PAD, 380, 280, 'ink', riso=('orange', 'cobalt', 7 * kick(t, 0.0, decay=4)))
        mono(c, 'our toolkit for latent diagnostics', PAD + 8, 450, 28, 'ink', ramp(t, 0.5, 0.3))
        # a grid of latent cells flickering on sixteenths (art)
        a = ramp(t, 0.5, 0.4)
        step = math.floor(t * 8)
        for i in range(12):
            for j in range(6):
                v = 0.5 + 0.5 * math.sin(i * 0.9 + j * 1.7 + step * 0.35) * math.cos(j * 0.6 - i * 0.3 + step * 0.21)
                colr = 'orange' if v > 0.93 else 'cobalt'
                c.drawRect(skia.Rect.MakeXYWH(1180 + i * 52, 150 + j * 52, 44, 44), paint(colr, a * (0.12 + 0.88 * v)))
        illustration(c, 1180, 490, 'muted', a)
        mono(c, '+ IDEAS FROM FOUR JOURNAL CLUB PAPERS', PAD, 545, 24, 'ink', ramp(t, b(1, 1), 0.2), bold=True)
        for k, (title, desc, bg, fg) in enumerate(PAPERS):
            t0 = b(1, 2 + k)
            a, sc = slam(t, t0, over=0.18)
            if a <= 0:
                continue
            x, y, w, h = PAD + k * 427, 580, 400, 370
            sc *= 1 + 0.02 * kick(t, b(3))
            with at(c, x + w / 2, y + h / 2, sc):
                slab(c, bg, a, x, y, w, h)
                mono(c, f'PAPER 0{k + 1}', x + 26, y + 46, 20, fg, a, bold=True)
                size = 50
                for i, ln in enumerate(wrap(title, size, w - 52)):
                    big(c, ln, x + 24, y + 120 + i * 54, size, fg, a)
                for i, ln in enumerate(wrap_mono(desc, 19, w - 52)):
                    mono(c, ln, x + 26, y + h - 62 + i * 28, 19, fg, a, track=0.04)


def wrap_mono(s, size, maxw):
    lines, cur = [], ''
    for w in s.split():
        trial = (cur + ' ' + w).strip()
        if cur and text_width(trial, size, 400, 'mono', 0.04) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + [cur]


# ---------------------------------------------------------------- 4. open questions
class Questions(Poster):
    dur = 26.0
    Q0 = b(3)          # the drop
    cues = [(b(3), 'impact'), (b(5), 'stamp_soft'), (b(6), 'whoosh'), (b(8), 'whoosh'), (b(9), 'whoosh'), (b(11), 'whoosh')]

    def draw(self, c, t):
        if t < b(2, 3.5):
            amt = 0.8 * ramp(t, b(2, 1), BAR * 0.6, e_in)
            glitch(c, lambda: self.intro(c, t), amt, t, seed=5)
            strobe(c, t, b(2, 2.5), b(2, 3.5), ['cobalt', 'orange', 'lime'], rate=3)
        elif t < b(3):
            slab(c, 'night')
        else:
            q = 0 if t < b(6) else 1 if t < b(8) else 2 if t < b(9) else 3 if t < b(11) else 4
            starts = [b(3), b(6), b(8), b(9), b(11)]
            amt = 0.55 * window(t, starts[q], starts[q] + 0.12, 0.01, 0.1) + out_glitch(t, self.dur)
            glitch(c, lambda: self.question(c, t, q, starts[q]), amt, t, seed=6 + q)

    def intro(self, c, t):
        slab(c, 'night')
        mono(c, 'AND THE BEST PART?', PAD, 260, 30, 'paper', ramp(t, 1.0, 0.3), bold=True)
        slam_word(c, t, 2.2, 'NOBODY KNOWS', PAD, 470, 170, 'paper', over=0.15)
        slam_word(c, t, 3.0, 'THE ANSWERS', PAD, 640, 170, 'paper', over=0.15)
        w = slam_word(c, t, 3.8, 'YET.', PAD, 810, 170, 'lime', over=0.15)
        if t >= 3.8 and int(t * 4) % 2 == 0:
            slab(c, 'lime', 1, PAD + w + 30, 810 - 128, 60, 140)
        if t >= b(2):
            tag(c, '05 OPEN QUESTIONS', PAD, 950, 30, 'night', 'lime', 1.0 if int((t - b(2)) * 4) % 2 == 0 else 0.0)
        scanlines(c, t, 0.12 * ramp(t, b(2), BAR, e_in))

    def question(self, c, t, q, t0):
        BG = ['orange', 'cobalt', 'paper', 'lime', 'night'][q]
        FG = ['ink', 'paper', 'ink', 'ink', 'paper'][q]
        slab(c, BG)
        big(c, '?', W - 80, 980, 900, 'paper', 0.13 if BG != 'paper' else 0.0, 'right')
        if BG == 'paper':
            big(c, '?', W - 80, 980, 900, 'cobalt', 0.07, 'right')
        tag(c, f'OPEN QUESTION 0{q + 1} / 05', PAD, 150, 22, BG, FG)
        getattr(self, f'q{q + 1}')(c, t, t0, FG)

    def q1(self, c, t, t0, FG):
        # arrows of heat flux into an ocean (art); then the thermometer
        a = 1 - ramp(t, t0 + b(2), 0.25)
        for i in range(5):
            ax = 1180 + i * 135
            pk = kick(t, t0, decay=6)
            arrow(c, ax, 540, ax, 700 + 14 * pk, 'ink', a * (0.55 + 0.45 * pk), 7, 22)
        waves(c, 1100, 740, 720, 170, t, 'ink', 0.9 * a, rows=5, width=5)
        illustration(c, 1100, 950, 'ink', 0.9 * a)
        size = fit('DOES THE OCEAN READ', 118, 1640)
        slam_word(c, t, t0, 'DOES THE OCEAN READ', PAD, 330, size, FG, over=0.12)
        slam_word(c, t, t0 + b(0, 2), 'A HEAT FLUX AS HEAT…', PAD, 460, size, FG, over=0.12)
        slam_word(c, t, t0 + b(2), '…OR AS A', PAD, 640, 118, 'paper', over=0.12)
        slam_word(c, t, t0 + b(2, 1), 'THERMOMETER?', PAD, 830, fit('THERMOMETER?', 190, 1380), FG, riso=('paper', 'cobalt', 5 * kick(t, t0 + b(2))), over=0.2)
        a2, sc = slam(t, t0 + b(2))
        if a2 > 0:
            with at(c, 1700, 760, sc):
                thermometer(c, 1700, 560, 320, 0.45 + 0.35 * kick(t, t0 + b(2), decay=4), 'paper', 'ink', a2 * (1 - 0 * a))

    def q2(self, c, t, t0, FG):
        slam_word(c, t, t0, 'WHICH PATH CARRIES', PAD, 330, 118, FG, over=0.12)
        a, sc = slam(t, t0 + BEAT * 2, over=0.12)
        if a > 0:
            w = tw('THE ', 118)
            with at(c, PAD + 500, 430, sc):
                big(c, 'THE ', PAD, 470, 118, FG, a)
                big(c, 'CO₂ SIGNAL?', PAD + w, 470, 118, 'lime', a)
        # two paths from one input to one output (art); a pulse takes both
        A = [(200, 760), (1740, 760)]
        B = [(200, 760), (520, 860), (900, 920), (1280, 860), (1740, 760)]
        k = ramp(t, t0 + 0.3, 0.6, e_io)
        draw_poly(c, A, 'paper', 0.55, 5, prog=k)
        draw_poly(c, B, 'paper', 0.55, 5, prog=k)
        for p in B[1:-1]:
            circle(c, *p, 12, fill='cobalt', stroke='paper', sw=4, a=k)
        circle(c, *A[0], 22, fill='paper', a=k)
        circle(c, *A[1], 22, fill='paper', a=k)
        mono(c, 'path a', 940, 735, 20, 'paper', k * 0.9)
        mono(c, 'path b', 860, 975, 20, 'paper', k * 0.9)
        illustration(c, 200, 975, 'paper', k)
        ph = ((t - t0) % BAR) / BAR
        if t > t0 + 0.6:
            circle(c, *end_point(A, ph), 13, fill='lime', a=1, glow=8)
            circle(c, *end_point(B, ph), 13, fill='orange', a=1, glow=8)
            big(c, '?', 1740, 700, 70, 'lime', 1, 'center')

    def q3(self, c, t, t0, FG):
        cx, cy = 1560, 330
        circle(c, cx, cy, 10, fill='cobalt', a=1)
        for k in range(3):
            r = 20 + (900 * ramp(t, t0 + BEAT * 2 + k * 0.12, 1.2, e_out))
            if t > t0 + BEAT * 2:
                circle(c, cx, cy, r, stroke='cobalt', sw=4, a=0.5 * (1 - k * 0.25))
        circle(c, cx, cy, 34 + 6 * kick(t, t0), stroke='cobalt', sw=4, a=0.9)
        slam_word(c, t, t0, 'LOCAL,', PAD, 470, 230, FG, over=0.15)
        slam_word(c, t, t0 + BEAT * 2, 'OR BASIN-SCALE?', PAD, 690, fit('OR BASIN-SCALE?', 170, 1680), 'cobalt', over=0.15)

    def q4(self, c, t, t0, FG):
        slam_word(c, t, t0, 'GOOD FORECASTS,', PAD, 330, 130, FG, over=0.12)
        slam_word(c, t, t0 + BAR / 2, 'BUT A SOUND', PAD, 480, 130, FG, over=0.12)
        slam_word(c, t, t0 + BAR * 0.75, 'INNER STATE?', PAD, 630, 130, 'cobalt', riso=('paper', 'orange', 3 * kick(t, t0)), over=0.12)
        # a forecast-like line drawn across (art), and a box for an inner state with a question in it
        x0, y0, w, h = 1050, 760, 700, 170
        pts = [(x0 + w * i / 80, y0 + h / 2 + h * 0.38 * (math.sin(i / 7.0) * 0.7 + 0.3 * math.sin(i / 2.3 + 1))) for i in range(81)]
        k = ramp(t, t0 + 0.2, 2.6, e_io)
        draw_poly(c, pts, 'ink', 1, 5, prog=k)
        line(c, x0, y0 + h, x0 + w, y0 + h, 'ink', 0.5, 2)
        illustration(c, x0, y0 + h + 40, 'ink', 0.9)
        a = ramp(t, t0 + BAR, 0.2)
        c.drawRect(skia.Rect.MakeXYWH(1500, 420, 250, 250), paint('ink', a, stroke=8, cap='butt'))
        big(c, '?', 1625, 610, 190, 'ink', a * (0.6 + 0.4 * kick(t, t0 + BAR)), 'center')
        mono(c, 'inner state', 1500, 400, 20, 'ink', a)

    def q5(self, c, t, t0, FG):
        # a field of points, a few marked wrong, some of those ringed (art)
        for i in range(9):
            for j in range(7):
                x, y = 1340 + i * 54, 640 + j * 50
                h = math.sin(i * 12.9898 + j * 78.233) * 43758.5453 % 1.0
                if h > 0.86:
                    pk = kick(t, t0, decay=5)
                    s = 13 + 4 * pk
                    line(c, x - s, y - s, x + s, y + s, 'orange', 1, 5)
                    line(c, x - s, y + s, x + s, y - s, 'orange', 1, 5)
                    if h > 0.93 and t > t0 + BAR:
                        circle(c, x, y, 26, stroke='lime', sw=4, a=1)
                else:
                    circle(c, x, y, 5, fill='paper', a=0.45)
        illustration(c, 1340, 1010, 'paper', 0.9)
        size = fit('DO OUR EXPLANATIONS', 118, 1640)
        slam_word(c, t, t0, 'DO OUR EXPLANATIONS', PAD, 330, size, FG, over=0.12)
        slam_word(c, t, t0 + BEAT, 'KEEP THE MODEL’S', PAD, 460, size, FG, over=0.12)
        slam_word(c, t, t0 + BEAT * 2, 'MISTAKES?', PAD, 670, 200, 'orange', riso=('cobalt', 'lime', 5 * kick(t, t0 + BEAT * 2)), over=0.2)


# ---------------------------------------------------------------- 5. six tracks
TRACKS = [('A', 'OCEAN SHORTCUT', 'cobalt', 'paper'), ('B', 'OCEAN ROUTING', 'orange', 'ink'),
          ('C', 'ATMOSPHERE CO₂', 'night', 'paper'), ('D', 'ERRORS & STRATA', 'lime', 'ink'),
          ('E', 'DYNAMICS', 'cobalt', 'paper'), ('F', 'EXEGE INTEGRATION', 'orange', 'ink')]


class Tracks(Poster):
    dur = 8.0
    cues = [(0.0, 'whoosh')] + [(b(0, 2 + k), 'tick') for k in range(6)]

    def draw(self, c, t):
        glitch(c, lambda: self.body(c, t), out_glitch(t, self.dur), t, seed=12)

    def body(self, c, t):
        slam_word(c, t, 0.0, 'SIX TRACKS', PAD, 250, 150, 'ink', riso=('orange', 'cobalt', 5 * kick(t, 0.0, decay=4)), over=0.15)
        gw, gh, gap = (W - 2 * PAD - 48) / 3, (650 - 24) / 2, 24
        for k, (letter, name, bg, fg) in enumerate(TRACKS):
            t0 = b(0, 2 + k)
            a, sc = slam(t, t0, over=0.2)
            if a <= 0:
                continue
            i, j = k % 3, k // 3
            x, y = PAD + i * (gw + gap), 310 + j * (gh + gap)
            sc *= 1 + 0.02 * kick(t, b(2))
            with at(c, x + gw / 2, y + gh / 2, sc):
                slab(c, bg, a, x, y, gw, gh)
                big(c, letter, x + 26, y + 140, 140, fg, a)
                lines = wrap(name, 52, gw - 52)
                for n, ln in enumerate(lines):
                    big(c, ln, x + 28, y + gh - 34 - (len(lines) - 1 - n) * 56, 52, fg, a)


# ---------------------------------------------------------------- 6. welcome
class Welcome(Poster):
    dur = 12.0
    cues = [(0.0, 'whoosh_soft')]

    def draw(self, c, t):
        if t < b(5, 3.5):
            amt = 0.8 * ramp(t, b(5), BAR - BEAT / 2, e_in) + 0.4 * window(t, 6.55, 6.8, 0.05, 0.05)
            glitch(c, lambda: self.body(c, t), amt, t, seed=13)
            strobe(c, t, b(5, 2), b(5, 3.5), ['cobalt', 'orange', 'lime'], rate=3)
        else:
            slab(c, 'night')

    def body(self, c, t):
        globe(c, 1500, 800, 520, t, 0.12 * t, sea='cobalt', air='orange', a=0.22, step=16, reveal=ramp(t, 0, 1.5))
        o = 6.6
        mono(c, 'NEW TO', PAD, 370, 34, 'ink', window(t, 1.0, o, 0.15, 0.15), bold=True)
        slam_word(c, t, 1.3, 'INTERPRETABILITY?', PAD, 510, fit('INTERPRETABILITY?', 140, 1680), 'ink', out=o, over=0.12)
        slam_word(c, t, 3.2, 'A CLIMATE SCIENTIST?', PAD, 670, fit('A CLIMATE SCIENTIST?', 110, 1680), 'cobalt', out=o, over=0.12)
        slam_word(c, t, 5.0, 'A TOTAL BEGINNER?', PAD, 820, 110, 'orange', out=o, over=0.12)
        slam_word(c, t, 6.85, 'YOU ARE', PAD, 470, 200, 'ink', over=0.12)
        size = fit('WELCOME HERE.', 200, 1680)
        w = slam_word(c, t, 7.35, 'WELCOME HERE.', PAD, 690, size, 'orange', riso=('cobalt', 'lime', 4 * ramp(t, b(5), BAR, e_in)), over=0.12)
        k = ramp(t, 8.0, 0.5, e_out)
        if k > 0:
            slab(c, 'ink', 1, PAD, 730, tw('WELCOME HERE.', size) * k, 16)
        scanlines(c, t, 0.12 * ramp(t, b(5), BAR, e_in))


# ---------------------------------------------------------------- 7. the card
class End(Poster):
    dur = 12.0
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        glitch(c, lambda: self.body(c, t), 0.6 * window(t, 0.0, 0.12, 0.01, 0.1), t, seed=14)

    def body(self, c, t):
        slab(c, 'cobalt')
        globe(c, 1580, 780, 430, t, 0.15 * t, sea='paper', air='lime', a=0.28, step=14)
        pump = kick(t, 0.0, b(3))
        s1 = fit('HACKATHON', 250, W - 2 * PAD)
        slam_word(c, t, 0.0, 'THE AIGS', PAD, 330, 200, 'paper', riso=('orange', 'lime', 4 * pump), over=0.2)
        slam_word(c, t, BEAT, 'HACKATHON', PAD, 545, s1, 'lime', riso=('orange', 'night', 4 * pump), over=0.2)
        s = WHEN.upper()
        slam_word(c, t, BEAT * 2, s, PAD, 690, fit(s, 104, W - 2 * PAD), 'paper', over=0.12)
        tag(c, MORE.upper(), PAD + 4, 800, 36, 'lime', 'night', ramp(t, BEAT * 3, 0.12))
        mono(c, 'from the aigs pod journal club community', PAD + 4, 950, 24, 'paper', ramp(t, b(1), 0.4) * 0.9)
        illustration(c, W - PAD, 1010, 'paper', 0.6, 'right')
