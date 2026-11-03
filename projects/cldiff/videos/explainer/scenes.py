"""Scenes for the conditional latent diffusion explainer (Scheinker & Williams, arXiv:2502.18684).

Paper figures are shown as crops (figcard, data/*.png from extract_paper.py) and labelled "Fig. N". The error bars in
Errors are redrawn from the numbers printed in the legends of the paper's Fig. 8. Everything else (beamlines, monitor
readouts, latent grids, the extremum-seeking path, square/circle shadows) is an illustration, labelled so on screen.
"""
import itertools, math
import numpy as np
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash
from cldkit import *

COORDS = ['x', 'y', 'φ', 'x′', 'y′', 'E']
PAIRS = list(itertools.combinations(range(6), 2))      # paper's ρ1..ρ15 order: (x,y), (x,φ), ... (y′,E)

# ======================================================================= TITLE
class Title(Scene):
    dur = 10.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, 'the aigs pod  ·  /mull/  ·  journal club', x0, 290, ramp(t, 0.2, 0.8), 'muted', 18)
        k = ramp(t, 0.1, 1.0, e_expo)
        with layer(c, k, (1 - k) * 16):
            text(c, 'Adaptive conditional', x0, 450 + (1 - k) * 40, 104, 800, 'ink')
            w2 = text(c, 'latent diffusion', x0, 566 + (1 - k) * 40, 104, 800, 'ink')
        swash(c, x0, x0 + w2, 600, 'y', 1, ramp(t, 0.7, 0.9, e_io), w=4)
        text(c, 'from beam-loss and current monitors to 2D phase-space pictures', x0, 670, 36, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'A. Scheinker  ·  A. Williams   (Los Alamos National Laboratory)', x0, 750, 30, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, 'arxiv:2502.18684  ·  2025', x0, 810, ramp(t, 2.6, 0.8), 'muted', 17)
        figcard(c, 'fig1_D', 1290, 360, 500, ramp(t, 1.0, 1.0), 'Fig. 1D', k=ramp(t, 1.0, 1.0, e_expo))
        sticky(c, 1560, 820, ['watch before', 'journal club'], ramp(t, 3.2, 0.5, e_back), rot=5.0)

# ======================================================================= QUESTION
class Question(Scene):
    dur = 41.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (6.0, 'tick'), (16.0, 'pop'), (22.0, 'pop'), (31.5, 'chime')]

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'Cheap monitors, *full* beam?')
        Y = 400
        k = ramp(t, 0.6, 2.0, e_io)
        xs = machine(c, 150, 1770, Y, 1, n=8, prog=k, labels=False)
        u = ((t - 1.0) * 0.1) % 1.0 if t > 1.0 else 0
        bunch(c, 150 + 1620 * u, Y, u * 6, ramp(t, 1.0, 0.6))
        km = ramp(t, 2.5, 1.0, e_expo)
        for i, xm in enumerate(xs):          # one monitor + one number per module (illustration)
            kk = clamp(km * 8 - i)
            if kk <= 0:
                continue
            rrect(c, xm - 30, Y + 52, 60, 30, 8, stroke='f', sw=1.6, a=kk, fill='panel', fa=0.8 * kk)
            text(c, 'BCM' if i % 2 else 'BLM', xm, Y + 73, 13, 500, 'f', kk, 'center', kind='mono')
            kn = ramp(t, 6.0 + i * 0.25, 0.5)
            v = 1.0 - 0.012 * i - 0.004 * math.sin(i * 2.1 + 0.3 * t)
            text(c, f'{v:.3f}', xm, Y + 118, 22, 500, 'ink', kn, 'center', kind='mono')
        note(c, 'each monitor: a single number', W / 2, Y + 160, ramp(t, 8.0, 0.6), 18, 'f', 'center')
        illus(c, W - MX, Y + 160, ramp(t, 3.0, 0.6), 'right')
        kw = ramp(t, 16.0, 1.0, e_expo)
        figcard(c, 'fig1_D', 1180, 640, 560, kw, 'Fig. 1D: 2D projections of the beam', k=kw)
        text(c, 'what we want →', 1150, 760, 30, 500, 'y', kw, 'right', kind='italic')
        ks = ramp(t, 22.0, 0.9, e_expo)
        if ks > 0:
            stat(c, MX, 720, '32 h', 'first full 6D measurement (SNS)', 'c', ks, size=78)
            note(c, '5,675,740 measurements · now 18 h   [paper ref. 12]', MX, 840, ks, 17, 'muted')
        caption(c, t, 'Can a {y:generative model} read the full beam from {f:simple monitor signals}?', 31.5, None, y=985, size=31)

# ======================================================================= PHASE SPACE
class PhaseSpace(Scene):
    dur = 36.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (3.5, 'pop'), (8.5, 'draw'), (17.5, 'pop'), (29.0, 'chime')]

    def __init__(self):
        rng = np.random.default_rng(4)
        L = np.array([[1, 0, 0], [0.6, 0.6, 0], [0.2, -0.4, 0.5]])
        self.cloud = rng.normal(size=(600, 3)) @ L.T

    def draw(self, c, t):
        header(c, t, '02', 'background', 'What is *phase space*?')
        k1 = ramp(t, 3.5, 0.8, e_expo)
        if k1 > 0:
            circle(c, 250, 360, 13, fill='y', a=k1, glow=10)
            for i, (lab, colr) in enumerate([('x', 'g'), ('y', 'g'), ('z', 'g'), ('px', 'c'), ('py', 'c'), ('pz', 'c')]):
                kk = ramp(t, 3.8 + i * 0.3, 0.5)
                xx, yy = 170 + (i % 3) * 80, 440 + (i // 3) * 62
                rrect(c, xx - 32, yy - 32, 64, 46, 10, stroke=colr, sw=1.6, a=kk, fill='panel', fa=0.8 * kk)
                text(c, lab, xx, yy, 26, 500, colr, kk, 'center', kind='italic')
            note(c, 'position  ·  momentum', 138, 570, ramp(t, 4.5, 0.5), 15, 'muted')
        kc = ramp(t, 8.5, 1.0, e_expo) * (1 - ramp(t, 28.5, 0.6))
        if kc > 0:
            cx, cy, s = 1250, 600, 85
            th = 0.25 * t
            R = np.array([[math.cos(th), 0, math.sin(th)], [0, 1, 0], [-math.sin(th), 0, math.cos(th)]])
            for p in (self.cloud @ R.T)[: int(600 * kc)]:
                circle(c, cx + p[0] * s, cy + p[1] * s, 2.4, fill='y', a=0.55 * kc * (0.6 + 0.4 * math.tanh(p[2])))
            text(c, 'six choose two  =  15 projections', cx, 360, 28, 600, 'ink', ramp(t, 11.0, 0.6) * kc, 'center', kind='mono')
            illus(c, cx, 900, kc, 'center', 'illustration · a 3D shadow of a 6D cloud')
        k3 = ramp(t, 17.5, 0.8, e_expo)
        if k3 > 0:
            text(c, 'at LANSCE the six become:', MX, 660, 24, 600, 'ink', k3)
            rows = [('px', "x′ = px / pz", 'angle'), ('py', "y′ = py / pz", 'angle'),
                    ('z', 'φ', 'rf phase, rel. to design'), ('pz', 'E', 'kinetic energy')]
            for i, (a0, b0, why) in enumerate(rows):
                kk = ramp(t, 18.0 + i * 1.6, 0.6)
                yy = 715 + i * 56
                text(c, a0, MX + 10, yy, 26, 500, 'c', kk, kind='italic')
                text(c, '→', MX + 80, yy, 26, 400, 'muted', kk)
                text(c, b0, MX + 130, yy, 26, 500, 'y', kk, kind='italic')
                note(c, why, MX + 330, yy - 4, kk, 16, 'muted')
        kf = ramp(t, 29.0, 1.0, e_expo)
        figcard(c, 'fig6_true', 900, 330, 880, kf, 'Fig. 6 (top): true projections at module 48', k=kf)

# ======================================================================= DATA
class Data(Scene):
    dur = 53.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (9.0, 'pop'), (14.0, 'draw'), (24.0, 'tick'), (31.0, 'pop'), (42.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '03', 'the data', 'One kilometre, *48* modules')
        Y, x0, x1 = 360, 150, 1770
        k0 = ramp(t, 0.6, 2.2, e_io)
        line(c, x0, Y, x0 + (x1 - x0) * k0, Y, 'faint', 1, 3)
        for i in range(48):
            kk = clamp(k0 * 48 - i)
            if kk <= 0:
                continue
            xm = x0 + (x1 - x0) * (i + 0.5) / 48
            hi = i < 4
            rrect(c, xm - 9, Y - 16, 18, 32, 4, fill='g' if hi else 'panel2', stroke='g', sw=1.2, a=kk, fa=(0.9 if hi else 0.8) * kk)
        note(c, 'LANSCE linac  ·  ~1 km  ·  48 rf modules', x1, Y + 50, ramp(t, 2.0, 0.6), 17, 'muted', 'right')
        note(c, 'first 4: the 201.25 MHz drift-tube linac', x0, Y + 50, ramp(t, 14.0, 0.6), 17, 'g')
        pill(c, W / 2, Y + 100, 'HPSim · GPU · 3D space charge · 1 million macro-particles per run', 'x', ramp(t, 9.0, 0.6), cx=True, size=18)
        # knob ranges
        kr = ramp(t, 14.0, 0.9, e_expo)
        if kr > 0:
            px, py = MX, 560
            panel(c, px, py, 700, 250, kr)
            text(c, 'each run: random shifts, first 4 cavities', px + 30, py + 50, 24, 600, 'ink', kr)
            for j, (lab, unit) in enumerate([('phase', '°'), ('amplitude', '%')]):
                yy = py + 115 + j * 80
                text(c, lab, px + 30, yy + 8, 20, 500, 'muted', kr, kind='mono')
                bx, bw = px + 200, 440
                line(c, bx, yy, bx + bw, yy, 'faint', kr, 2)
                rrect(c, bx, yy - 9, bw * ramp(t, 14.5 + j * 0.4, 1.0), 18, 6, fill='g', fa=0.55 * kr)
                text(c, f'±3{unit}', bx + bw + 14, yy + 8, 20, 600, 'g', kr, kind='mono')
                ko = ramp(t, 24.0, 0.8, e_expo)
                if ko > 0:
                    rrect(c, bx + bw / 3, yy - 13, bw / 3, 26, 6, stroke='y', sw=2.2, a=ko)
                    if j == 1:
                        note(c, 'operators: about ±1', bx + bw / 2, yy + 46, ko, 16, 'y', 'center')
        # counting
        kn = ramp(t, 31.0, 0.8, e_expo)
        if kn > 0:
            items = [('4', 'starting beams'), ('500', 'runs each'), ('48', 'modules'), ('15', 'projections')]
            xx = 900
            for i, (n, lab) in enumerate(items):
                kk = ramp(t, 31.0 + i * 1.4, 0.6, e_expo)
                text(c, n, xx, 620, 54, 700, 'y', kk)
                note(c, lab, xx, 655, kk, 15, 'muted')
                xx += max(text_width(n, 54, 700), 120) + 20
                if i < 3:
                    text(c, '×', xx, 615, 36, 400, 'muted', kk)
                    xx += 46
            ke = ramp(t, 37.0, 0.8, e_expo)
            text(c, '= 1.44 million images, 256 × 256 px', 900, 720, 32, 600, 'ink', ke)
        # split
        ks = ramp(t, 42.0, 1.0, e_expo)
        if ks > 0:
            bx, by, uw = 900, 790, 1.5
            for r in range(4):
                yy = by + r * 42
                kk = ramp(t, 42.0 + r * 0.4, 0.6)
                text(c, f'beam {r + 1}', bx, yy + 20, 18, 500, 'muted', kk, kind='mono')
                if r < 3:
                    rrect(c, bx + 110, yy, 400 * uw * kk, 26, 5, fill='g', fa=0.7)
                    rrect(c, bx + 110 + 400 * uw, yy, 100 * uw * kk, 26, 5, fill='y', fa=0.85)
                else:
                    rrect(c, bx + 110, yy, 500 * uw * kk, 26, 5, fill='c', fa=0.85)
            kl = ramp(t, 44.0, 0.6)
            note(c, 'train 400', bx + 110 + 200 * uw, by - 12, kl, 15, 'g', 'center')
            note(c, 'test 100', bx + 110 + 450 * uw, by - 12, kl, 15, 'y', 'center')
            note(c, 'beam 4: never seen in training, all 500 runs are test', bx + 110 + 500 * uw, by + 4 * 42 + 14, ramp(t, 46.0, 0.6), 16, 'c', 'right')

# ======================================================================= SIGNALS
class Signals(Scene):
    dur = 36.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (9.0, 'draw'), (18.5, 'pop'), (23.5, 'tick'), (31.0, 'chime')]
    SEGS = [('p', 8, 'f', 'rf settings: A₁ θ₁ … A₄ θ₄'), ('b', 48, 'g', 'beam current at each module'),
            ('d', 6, 'y', 'which projection'), ('m', 1, 'c', 'module')]

    def draw(self, c, t):
        header(c, t, '04', 'the input', 'Currents along the *machine*')
        k0 = ramp(t, 0.6, 1.0, e_expo)
        figcard(c, 'fig1_top', MX + 10, 320, 1030, k0, 'Fig. 1A: monitor readings along the accelerator', k=k0)
        k1 = ramp(t, 9.0, 0.9, e_expo)
        tex(c, 'bm', 1480, 400, 40, k1, reveal=k1)
        if k1 > 0:
            note(c, 'surviving current at module m: add up', 1480, 470, k1, 16, 'ink', 'center')
            note(c, 'the (z, pz) projection: computed from', 1480, 494, k1, 16, 'ink', 'center')
            note(c, 'the simulation, not a real monitor', 1480, 518, k1, 16, 'c', 'center')
            text(c, '48 numbers', 1480, 590, 30, 600, 'g', ramp(t, 13.0, 0.6), 'center')
        k2 = ramp(t, 18.5, 0.8, e_expo)
        if k2 > 0:
            text(c, 'c', MX, 770, 52, 500, 'ink', k2, kind='italic')
            text(c, '=', MX + 50, 768, 40, 400, 'muted', k2)
            x = MX + 110
            for i, (nm, n, colr, lab) in enumerate(self.SEGS):
                ks = ramp(t, 23.5 + i * 2.2, 0.8, e_expo)
                w = n * 17 - 3
                chips(c, x, 740, n, colr, max(0.25, ks) * k2, prog=k2)
                text(c, nm, x + w / 2, 720, 26, 600, colr, k2, 'center', kind='italic')
                if ks > 0:
                    note(c, f'{n} · {lab}' if n > 1 else lab, x + (w / 2 if n > 6 else 0), 812 + (i % 2) * 26, ks, 16, colr, 'center' if n > 6 else 'left')
                x += w + 34
        km = ramp(t, 31.0, 0.8, e_expo)
        tex(c, 'map', W / 2, 920, 40, km, reveal=km)

# ======================================================================= COMPRESS (VAE)
class Compress(Scene):
    dur = 48.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (6.5, 'draw'), (17.0, 'pop'), (25.5, 'draw'), (36.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '05', 'the model · step 1', 'First, *compress*')
        k0 = ramp(t, 0.6, 1.0, e_expo)
        figcard(c, 'fig5', MX + 10, 310, None, k0, 'Fig. 5A', h=620, k=k0, src=(0, 0, 0.62, 1))
        out = 1 - ramp(t, 35.5, 0.6)
        cy = 520
        k1 = ramp(t, 6.5, 0.9, e_expo) * out
        if k1 > 0:
            figcard(c, 'fig1_D', 560, cy - 120, None, k1, None, h=240, src=(0.0, 0.0, 0.2, 0.5), pad=4, credit=False)
            text(c, '256 × 256', 560 + 120, cy + 160, 26, 600, 'ink', k1, 'center', kind='mono')
            note(c, '65,536 pixels', 560 + 120, cy + 190, k1, 16, 'muted', 'center')
        k2 = ramp(t, 8.0, 0.9, e_expo) * out
        trapezoid(c, 840, cy, 200, 240, 100, 'g', k2, 'encoder')
        kz = ramp(t, 9.5, 0.8, e_expo) * out
        latent_grid(c, 1080, cy - 50, 100, 0, kz)
        text(c, '8 × 8 × 3', 1130, cy + 100, 26, 600, 'y', kz, 'center', kind='mono')
        illus(c, 1130, cy - 70, kz, 'center')
        kc = ramp(t, 17.0, 0.8, e_expo) * out
        if kc > 0:
            note(c, '192 numbers', 1130, cy + 130, kc, 18, 'y', 'center')
        kh = window(t, 18.0, 35.5, 0.6, 0.5)
        if kh > 0:
            hand(c, '÷ 341', 1060, cy + 200, 40, 'pencil', kh, -3.0, ramp(t, 18.0, 0.8, e_lin))
        kd = ramp(t, 25.5, 0.9, e_expo) * out
        trapezoid(c, 1220, cy, 200, 100, 240, 'f', kd, 'decoder')
        if kd > 0:
            figcard(c, 'fig1_D', 1460, cy - 120, None, kd, None, h=240, src=(0.0, 0.0, 0.2, 0.5), pad=4, credit=False)
            text(c, 'rebuilt', 1580, cy + 160, 22, 500, 'f', kd, 'center', kind='mono')
            tex(c, 'vae', 1130, 800, 36, ramp(t, 28.0, 0.8) * out, reveal=ramp(t, 28.0, 1.0))
            note(c, 'R: rebuild error   ·   KL: keep the latent space smooth', 1130, 850, ramp(t, 28.5, 0.6) * out, 16, 'muted', 'center')
        k4 = ramp(t, 36.0, 1.0, e_expo)
        if k4 > 0:
            w, h = figcard(c, 'fig4', 640, 340, 1000, k4, 'Fig. 4: projections, their latents, and the R, G, B channels', k=k4)
            rows = ['image', 'latent', 'R: brightest', 'G: edges', 'B: mini copy']
            for i, lab in enumerate(rows):
                kk = ramp(t, 37.0 + max(0, i - 1) * 1.5, 0.6) if i >= 2 else k4
                note(c, lab, 640 + w + 24, 340 + (i + 0.5) * h / 5 + 5, kk, 17, ['ink', 'y', 'r', 'f', 'g'][i])

# ======================================================================= DIFFUSE
class Diffuse(Scene):
    dur = 49.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (5.0, 'draw'), (11.5, 'draw'), (21.0, 'pop'), (28.5, 'pop'), (40.0, 'chime')]
    N = 5

    def draw(self, c, t):
        header(c, t, '06', 'the model · step 2', 'Then *generate*, in latent space')
        out = 1 - ramp(t, 39.5, 0.6)
        s, y, x0, dx = 140, 400, 200, 330
        xs = [x0 + i * dx for i in range(self.N)]
        k0 = ramp(t, 0.6, 0.8, e_expo) * out
        latent_grid(c, xs[0], y, s, 0, k0)
        note(c, 'z: a latent grid', xs[0] + s / 2, y + s + 30, k0, 16, 'y', 'center')
        kf = ramp(t, 5.0, 4.0, e_lin)
        for i in range(1, self.N):
            kk = clamp(kf * (self.N - 1) - (i - 1)) * out
            latent_grid(c, xs[i], y, s, i / (self.N - 1), kk)
            curve_arrow(c, (xs[i - 1] + s / 2 + 10, y - 12), (xs[i] + s / 2 - 10, y - 12), 0.25, 'c', kk, kk, w=2, head=9)
        note(c, 'add noise, step by step  →', xs[2] + s / 2, y - 62, ramp(t, 5.5, 0.6) * out, 17, 'c', 'center')
        note(c, 'pure noise', xs[-1] + s / 2, y + s + 30, ramp(t, 8.5, 0.6) * out, 16, 'c', 'center')
        illus(c, W - MX, y - 62, k0, 'right')
        tex(c, 'noise', 560, 800, 30, ramp(t, 7.0, 0.8) * out, reveal=ramp(t, 7.0, 1.0))
        kr = ramp(t, 11.5, 4.0, e_lin)
        yb = y + s + 60
        for i in range(self.N - 1, 0, -1):
            kk = clamp(kr * (self.N - 1) - (self.N - 1 - i)) * out
            curve_arrow(c, (xs[i] + s / 2 - 10, yb), (xs[i - 1] + s / 2 + 10, yb), 0.25, 'f', kk, kk, w=2.5, head=10)
        note(c, '←  a U-Net removes one step of noise', xs[2] + s / 2, yb + 106, ramp(t, 11.8, 0.6) * out, 18, 'f', 'center')
        kt = ramp(t, 21.0, 0.8, e_expo) * out
        if kt > 0:
            stat(c, 1180, 810, '100', 'steps, not ~1000: the grid is tiny', 'f', kt, size=64)
        kc = ramp(t, 28.5, 0.8, e_expo) * out
        if kc > 0:
            yc = 630
            chips(c, 290, yc, 8, 'f', kc, w=16, h=26, gap=3)
            chips(c, 455, yc, 48, 'g', kc, w=16, h=26, gap=3)
            chips(c, 1380, yc, 6, 'y', kc, w=16, h=26, gap=3)
            chips(c, 1506, yc, 1, 'c', kc, w=16, h=26, gap=3)
            text(c, 'c', 262, yc + 22, 34, 500, 'ink', kc, 'right', kind='italic')
            for i in range(1, self.N):
                xm = (xs[i] + xs[i - 1]) / 2 + s / 2
                arrow(c, xm, yc - 6, xm, yb - 22, 'ink', kc * 0.7, 1.6, head=7)
            note(c, 'guides every step', 1550, yc + 20, kc, 16, 'ink')
        k4 = ramp(t, 40.0, 1.0, e_expo)
        figcard(c, 'fig3', 310, 330, 1300, k4, 'Fig. 3: D, E: diffusion makes a latent  ·  F: the VAE decoder makes the image', k=k4)

# ======================================================================= LABEL (d)
class Label(Scene):
    dur = 44.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (9.5, 'pop'), (17.5, 'pop'), (24.0, 'pop'), (32.5, 'chime')]
    COLX = [MX, 700, 1280]

    def d(self, j):
        v = [0] * 6
        for a in PAIRS[j]:
            v[a] = 1
        return v

    def draw(self, c, t):
        header(c, t, '07', 'the model · conditioning', 'Which projection? Ask *physically*')
        k0 = ramp(t, 0.6, 1.5, e_io)
        for j, (a, b) in enumerate(PAIRS):
            kk = clamp(k0 * 15 - j)
            note(c, f'ρ{j + 1}', MX + j * 112, 320, kk, 15, 'muted')
            note(c, f'{COORDS[a]},{COORDS[b]}', MX + j * 112, 344, kk, 17, 'ink')
        tops = [('a number', 'ρⱼ → j / 15', 'c', 9.5), ('one-hot', '15 slots, one lit', 'x', 17.5), ('6 slots: the axes', 'a 1 on each shown axis', 'f', 24.0)]
        for i, (ttl, sub, colr, t0) in enumerate(tops):
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            x = self.COLX[i]
            panel(c, x, 400, 540, 560, k)
            line(c, x + 28, 401, x + 128, 401, colr, k, 4, cap='butt')
            text(c, ttl, x + 28, 460, 32, 400, 'ink', k, kind='italic')
            note(c, sub, x + 28, 494, k, 16, colr)
        # A: scalar
        ka = ramp(t, 10.5, 0.8)
        if ka > 0:
            x = self.COLX[0] + 40
            line(c, x, 640, x + 460, 640, 'faint', ka, 2)
            for j in range(15):
                xx = x + 460 * (j + 1) / 15
                hi = j in (0, 1, 2)
                circle(c, xx, 640, 7 if hi else 4, fill='c' if hi else 'muted', a=ka)
                if hi:
                    note(c, f'ρ{j + 1}', xx, 620 - (j % 2) * 22, ka, 14, 'c', 'center')
            rich(c, '{c:ρ2} (x,φ) sits {y:twice as close} to {c:ρ1} (x,y) as {c:ρ3} (x,x′) does, though both share only x.',
                 x, 720, 21, 470, t, 12.0, 0.02, 0.4)
        # B: one-hot
        kb = ramp(t, 18.5, 0.8)
        if kb > 0:
            x, y, cs = self.COLX[1] + 40, 540, 14
            for i in range(15):
                for j in range(15):
                    rrect(c, x + j * cs, y + i * cs, cs - 2, cs - 2, 2, fill='x' if i == j else 'faint', a=kb, fa=0.9 if i == j else 0.5)
            rich(c, 'Every pair is equally far apart: {y:shared axes are ignored}.', x + 240, 560, 21, 230, t, 19.0, 0.02, 0.4)
        # C: 6 slots
        kc = ramp(t, 25.0, 0.8)
        if kc > 0:
            x = self.COLX[2] + 40
            for i, a in enumerate(COORDS):
                note(c, a, x + 120 + i * 40 + 13, 540, kc, 16, 'muted', 'center')
            for r, j in enumerate([0, 1, 2, 11, 12]):
                kk = ramp(t, 25.5 + r * 0.6, 0.5)
                yy = 560 + r * 48
                note(c, f'd{j + 1}  ({COORDS[PAIRS[j][0]]},{COORDS[PAIRS[j][1]]})', x, yy + 24, kk, 15, 'ink')
                for i, v in enumerate(self.d(j)):
                    rrect(c, x + 120 + i * 40, yy, 30, 32, 4, fill='f' if v else 'faint', fa=0.9 if v else 0.4, a=kk)
        kd = ramp(t, 32.5, 0.8, e_expo)
        if kd > 0:
            x = self.COLX[2] + 40
            text(c, 'd1·d2 = d1·d3 = 1', x, 860, 22, 600, 'f', kd, kind='mono')
            text(c, 'd12·d13 = 0', x, 896, 22, 600, 'ink', ramp(t, 34.5, 0.6), kind='mono')
            pill(c, x + 300, 896 - 26, 'worked best', 'f', ramp(t, 37.5, 0.6), size=16)

# ======================================================================= RESULTS
class Results(Scene):
    dur = 30.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (6.5, 'pop'), (13.5, 'tick'), (19.5, 'chime')]

    def draw(self, c, t):
        header(c, t, '08', 'results', 'Generated vs *true*')
        out = 1 - ramp(t, 19.0, 0.6)
        k1 = ramp(t, 0.8, 1.0, e_expo) * out
        figcard(c, 'fig6_true', 140, 330, 780, k1, 'Fig. 6 (top)', k=k1)
        text(c, 'true', 140, 302, 22, 600, 'ink', ramp(t, 6.5, 0.6) * out, kind='mono')
        k2 = ramp(t, 6.5, 1.0, e_expo) * out
        figcard(c, 'fig6_gen', 1000, 330, 780, k2, 'Fig. 6 (bottom)', k=k2)
        text(c, 'generated', 1000, 302, 22, 600, 'x', k2, kind='mono')
        kp = ramp(t, 13.5, 0.7) * out
        if kp > 0:
            caption(c, t, 'White curves: true profiles  ·  {x:magenta}: generated', 13.5, 19.0, y=985, size=26)
        k3 = ramp(t, 19.5, 1.0, e_expo)
        figcard(c, 'fig7', 260, 320, 1400, k3, 'Fig. 7: true (row 1) vs predicted (row 2) (φ, E), modules 1 → 48', k=k3)

# ======================================================================= ERRORS
class Errors(Scene):
    dur = 41.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (8.0, 'pop'), (14.0, 'pop'), (24.0, 'draw'), (32.5, 'tick')]
    # mean absolute percent error, typed from the legends of the paper's Fig. 8 (A, B, C): (train, test)
    STAGES = [('VAE alone', 'image error', 15.67, 15.55), ('latent diffusion', 'latent error', 8.07, 14.05),
              ('full chain', 'image error', 16.53, 23.79)]

    def draw(self, c, t):
        header(c, t, '09', 'results', 'How big are the *errors*?')
        x0, y0, h, ymax = 190, 880, 460, 30.0
        k0 = ramp(t, 0.6, 0.9, e_expo)
        if k0 > 0:
            line(c, x0 - 20, y0, x0 + 760, y0, 'line', k0, 2)
            for v in (0, 10, 20, 30):
                yy = y0 - h * v / ymax
                line(c, x0 - 20, yy, x0 + 760, yy, 'line', k0 * 0.5, 1)
                note(c, f'{v}%', x0 - 30, yy + 5, k0, 14, 'muted', 'right')
            legend_item(c, x0 + 470, 360, 'g', 'train', k0, size=20)
            legend_item(c, x0 + 600, 360, 'y', 'test', k0, size=20)
        for i, (nm, kind, tr, te) in enumerate(self.STAGES):
            kk = ramp(t, 1.0 + i * 0.6, 1.0, e_expo)
            if kk <= 0:
                continue
            gx = x0 + i * 250
            hl = 1.0
            if t > 8.0:
                hl = 1.0 if (i == 0 and t < 14.0) or (i == 2 and t >= 14.0) else 0.4
                if t >= 24.0:
                    hl = 1.0
            with layer(c, hl):
                for j, (v, colr) in enumerate([(tr, 'g'), (te, 'y')]):
                    bh = h * v / ymax * kk
                    rrect(c, gx + j * 80, y0 - bh, 70, bh, 4, fill=colr, fa=0.85)
                    note(c, f'{v:.1f}', gx + j * 80 + 35, y0 - bh - 10, kk, 16, colr, 'center')
                note(c, nm, gx + 75, y0 + 30, kk, 17, 'ink', 'center')
                note(c, kind, gx + 75, y0 + 54, kk, 14, 'muted', 'center')
        note(c, 'mean absolute % error, from the legends of the paper’s Fig. 8  ·  the middle pair is on latents, not images', x0 - 30, 975, k0, 14, 'muted')
        k2 = ramp(t, 24.0, 1.0, e_expo) * (1 - ramp(t, 32.0, 0.6))
        figcard(c, 'fig9', 1060, 380, 740, k2, 'Fig. 9: fitted beam sizes σ, true vs predicted', k=k2)
        k3 = ramp(t, 32.5, 1.0, e_expo)
        figcard(c, 'fig10', 1060, 380, 740, k3, 'Fig. 10: error vs module & projection', k=k3)

# ======================================================================= ADAPTIVE
class Adaptive(Scene):
    dur = 56.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (11.5, 'tick'), (16.0, 'pop'), (25.5, 'draw'), (33.0, 'draw'), (45.5, 'chime')]
    T0 = 33.0           # the extremum-seeking illustration starts here

    def __init__(self):
        # bounded extremum seeking (paper Eq. 22) on C = |c - c*(τ)|², c* drifting: an illustration, not data
        dt, alpha, k, w = 1e-3, 0.1, 4.0, np.array([40.0, 52.0])
        cc = np.array([-0.7, 0.55])
        self.path, self.star = [], []
        for i in range(int(24 / dt)):
            tau = i * dt
            cs = np.array([0.25 + 0.3 * math.cos(tau * 0.2), -0.15 + 0.3 * math.sin(tau * 0.2)])
            cc = cc + dt * np.sqrt(alpha * w) * np.cos(w * tau + k * ((cc - cs) ** 2).sum())
            if i % 10 == 0:
                self.path.append(cc.copy()); self.star.append(cs)
        self.path, self.star = np.array(self.path), np.array(self.star)

    def knob(self, c, x, y, v, a):
        circle(c, x, y, 30, fill='panel2', stroke='f', sw=2, a=a)
        ang = math.radians(-220 + 260 * v)
        line(c, x, y, x + 22 * math.cos(ang), y + 22 * math.sin(ang), 'f', a, 3)

    def draw(self, c, t):
        header(c, t, '10', 'adaptive', 'When the machine *drifts*')
        k0 = ramp(t, 0.6, 0.8, e_expo) * (1 - ramp(t, 32.5, 0.6))
        if k0 > 0:
            for i in range(4):
                v = 0.5 + 0.25 * math.sin(0.35 * t + i * 1.7)
                self.knob(c, MX + 60 + i * 120, 400, v, k0)
            note(c, 'rf settings drift: minutes to hours', MX + 20, 470, k0, 17, 'f')
            note(c, 'true values: not known exactly', MX + 20, 496, k0, 17, 'muted')
            ks = ramp(t, 11.5, 1.0)
            text(c, 'c', MX + 20, 590, 40, 500, 'ink', k0, kind='italic')
            chips(c, MX + 70, 562, 8, 'f', k0 * (1 - 0.7 * ks))
            chips(c, MX + 210, 562, 12, 'g', k0)
            note(c, '…', MX + 420, 590, k0, 20, 'muted')
            if ks > 0:
                note(c, 'stale', MX + 70, 630, ks * k0, 18, 'c')
            illus(c, MX + 20, 680, k0)
        k1 = ramp(t, 16.0, 1.0, e_expo)
        figcard(c, 'fig11', 700, 330, 1080, k1, 'Fig. 11: τ = machine time,  t = diffusion time', k=k1)
        kc = ramp(t, 25.5, 0.8, e_expo)
        tex(c, 'cost', 1240, 810, 32, kc, reveal=kc)
        ke = ramp(t, 33.0, 0.8, e_expo)
        tex(c, 'es', 1240, 885, 32, ke, reveal=ke)
        kg = ramp(t, 45.5, 0.8, e_expo)
        tex(c, 'grad', 1240, 960, 30, kg, reveal=kg)
        if kg > 0:
            note(c, '≈ gradient descent, without estimating a gradient', 1240, 1010, kg, 15, 'f', 'center')
        # extremum-seeking illustration
        ka = ramp(t, self.T0, 0.8, e_expo)
        if ka > 0:
            px, py, pw = MX + 10, 380, 500
            def P(q):
                return px + (q[0] + 1) / 2 * pw, py + (1 - (q[1] + 1) / 2) * pw
            n = int(clamp((t - self.T0) / 24) * (len(self.path) - 1))
            with layer(c, ka):
                rrect(c, px, py, pw, pw, 8, fill='panel', fa=0.8)
                st = self.star[n]
                for r in (0.15, 0.3, 0.45, 0.6, 0.75):
                    cx_, cy_ = P(st)
                    circle(c, cx_, cy_, r * pw / 2, stroke='faint', sw=1.4)
                cx_, cy_ = P(st)
                text(c, '×', cx_, cy_ + 9, 28, 600, 'y', 1, 'center')
                pts = np.array([P(q) for q in self.path[max(0, n - 1500):n + 1]])
                if len(pts) > 1:
                    draw_poly(c, pts, 'f', 0.75, 1.6)
                e = P(self.path[n])
                circle(c, e[0], e[1], 7, fill='f', a=1, glow=6)
                note(c, '× = cost minimum, drifting', px + 14, py + pw - 16, 1, 15, 'y')
            illus(c, px, py + pw + 26, ka, s='illustration · extremum seeking on a 2D toy cost')

# ======================================================================= TRACKING
class Tracking(Scene):
    dur = 40.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (6.5, 'pop'), (14.5, 'tick'), (20.5, 'draw'), (32.5, 'chime')]

    def draw(self, c, t):
        header(c, t, '11', 'adaptive', 'Tracking a *drifting* beam')
        x, y = 150, 320
        k0 = ramp(t, 0.6, 1.0, e_expo)
        w, h = figcard(c, 'fig12', x, y, None, k0, 'Fig. 12: (φ, E) at modules 28, 38, 48', h=640, k=k0)
        for j, (lab, colr, t0) in enumerate([('no tracking', 'c', 6.5), ('target', 'y', 9.0), ('with tracking', 'f', 11.5)]):
            kk = window(t, t0, 20.5, 0.5, 0.6) if j < 2 else ramp(t, t0, 0.5)
            if kk > 0:
                rrect(c, x + j * w / 3 - 2, y - 6, w / 3 + 2, h + 12, 6, stroke=colr, sw=3, a=kk)
        kr = ramp(t, 14.5, 0.8, e_expo)
        if kr > 0:
            rich(c, 'Recovers the target’s shape; {y:misses small interior details}.', 1160, 380, 28, 620, t, 14.6, 0.03, 0.45)
        ks = ramp(t, 20.5, 0.9, e_expo)
        if ks > 0:
            bx, by = 1200, 560
            # a square and a disc with the same 1D profile (illustration): both drawn above one shared profile
            rrect(c, bx, by, 160, 160, 2, fill='g', fa=0.35 * ks, stroke='g', sw=2, a=ks)
            circle(c, bx + 340, by + 80, 80, fill='x', stroke='x', sw=2, a=ks * 0.9)
            for xx in (bx + 80, bx + 340):
                arrow(c, xx, by + 175, xx, by + 225, 'muted', ks, 2, head=9)
            line(c, bx - 10, by + 300, bx + 440, by + 300, 'faint', ks, 2)
            for off in (0, 260):
                rrect(c, bx + off, by + 240, 160, 60, 2, fill='y', fa=0.6 * ks)
            note(c, 'same 1D profile, if the densities are chosen right', bx + 220, by + 334, ks, 16, 'y', 'center')
            illus(c, bx + 220, by + 360, ks, 'center')
        kp = ramp(t, 32.5, 0.8, e_expo)
        pill(c, 1420, 1000, 'the model only makes beams the machine can make', 'f', kp, cx=True, size=18)

# ======================================================================= LIMITS
class Limits(Scene):
    dur = 33.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.5, 'pop'), (12.5, 'pop'), (20.0, 'pop')]
    CARDS = [('Simulation only', 'The currents are {y:summed simulated particles}, not real monitors with noise, offsets and calibration drift.', 'c', 2.5),
             ('A narrow knob set', 'Only the {y:first 4 cavities} vary (8 numbers). The other 44 modules and all the magnets stay fixed.', 'g', 12.5),
             ('What isn’t broken out', 'No separate result for the {y:unseen starting beam}. Tracking: {y:3 examples}, no statistics.', 'y', 20.0)]

    def draw(self, c, t):
        header(c, t, '12', 'limits', 'A few *cautions*')
        cw, gap, y0, ch = 532, 42, 360, 470
        for i, (lab, body, colr, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, lab, x + 36, y0 + 90, 38, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 36, y0 + 160, 29, cw - 72, t, t0 + 0.3, 0.025, 0.45)

# ======================================================================= DISCUSSION
class Discussion(Scene):
    dur = 37.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (9.5, 'pop'), (16.5, 'pop'), (22.5, 'pop'), (29.5, 'pop')]
    QS = [
        'The title says {y:beam loss}, but the inputs are simulated currents. What changes with real, noisy monitors?',
        'If each stage adds error, is a {y:bigger autoencoder} the fix, or should the compression go?',
        'How far can the {y:starting beam} change before the model needs retraining?',
        'When tracking matches a {y:1D profile}, how do we know the rest of the image is right?',
        'Could these monitors and this model {y:tune} the machine, not just watch it?',
    ]
    T0 = [2.0, 9.5, 16.5, 22.5, 29.5]

    def draw(self, c, t):
        header(c, t, '13', 'discussion', 'Before we *meet*: questions to think about')
        y = 340
        for i, q in enumerate(self.QS):
            t0 = self.T0[i]
            k = ramp(t, t0, 0.7, e_expo)
            if k <= 0:
                y += 120
                continue
            text(c, f'Q{i + 1}', MX, y + 8 + (1 - k) * 10, 30, 750, 'y', k, kind='mono')
            h = rich(c, q, MX + 90, y + 8, 33, 1380, t, t0 + 0.1, 0.025, 0.45, k, lh=1.28)
            y += max(h, 44) + 46
        sticky(c, 1600, 900, ['bring one', 'to the desk'], ramp(t, 33.0, 0.5, e_back), rot=-4.0, w=230, h=170, tag='homework')

# ======================================================================= END
class End(Scene):
    dur = 16.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (15.0, 'outro')]

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 230, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, 'Cheap {f:monitors}, a compressed {y:latent space}, a guided {g:diffusion} model: single numbers in, detailed beam pictures out.',
             W / 2, 310, 50, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        for i, (lab, colr) in enumerate([('compress', 'y'), ('generate', 'g'), ('track', 'f')]):
            k = ramp(t, 3.0 + i * 0.3, 0.8, e_expo)
            pill(c, W / 2 + (i - 1) * 380, 520, lab, colr, k, size=22, cx=True)
        k2 = ramp(t, 5.0, 0.9)
        with layer(c, k2):
            line(c, MX, 640, W - MX, 640, 'line', 1, 1.5)
            text(c, 'A. Scheinker & A. Williams (2025).  Adaptive conditional latent diffusion maps beam loss', MX, 700, 27, 600, 'ink')
            text(c, 'to 2D phase space projections.', MX, 740, 27, 600, 'ink')
            text(c, 'arxiv.org/abs/2502.18684', MX, 790, 22, 500, 'g', 1, kind='mono')
            note(c, 'an unofficial explainer, not made by the authors  ·  “Fig. N” = crops of the paper’s figures', MX, 840, 0.9, 16)
        k3 = ramp(t, 6.0, 0.8)
        lamp(c, 1640, 790, 1.15, k3, on=k3)
        hand(c, 'see you at the desk', 1380, 990, 36, 'pencil', k3, -3.0, ramp(t, 6.4, 1.0, e_lin))
