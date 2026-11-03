"""Scenes for the LEM explainer (Rautela & Scheinker, NAPAC2025, arXiv:2602.22618).

The paper is a three-page summary with no figures or tables, so nothing here is data: every beam image, latent
vector, trajectory and landscape is an illustration (labelled so on screen). Equations are the paper's own.
"""
import math
import numpy as np
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash
from lemkit import *

# ======================================================================= TITLE
class Title(Scene):
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, 'the aigs pod  ·  /mull/  ·  journal club', x0, 300, ramp(t, 0.2, 0.8), 'muted', 18)
        lamp(c, 1560, 300, 1.5, ramp(t, 0.0, 0.8), on=ramp(t, 0.15, 1.2, e_out))
        k = ramp(t, 0.1, 1.0, e_expo)
        with layer(c, k, (1 - k) * 16):
            text(c, 'Latent Evolution', x0, 470 + (1 - k) * 40, 128, 800, 'ink')
            w2 = text(c, 'Models', x0, 600 + (1 - k) * 40, 128, 800, 'ink')
        swash(c, x0, x0 + w2, 636, 'y', 1, ramp(t, 0.7, 0.9, e_io), w=4)
        text(c, 'one model for forward, inverse, tuning and UQ in accelerators', x0, 706, 40, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'M. Rautela  ·  A. Scheinker   (Los Alamos National Laboratory)', x0, 786, 30, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, 'NAPAC 2025  ·  arxiv:2602.22618', x0, 846, ramp(t, 2.6, 0.8), 'muted', 17)
        ka = ramp(t, 1.0, 1.4, e_io)
        machine(c, 1290, 1830, 520, ramp(t, 0.8, 0.8), n=4, prog=ka, labels=False)
        bunch(c, 1290 + 540 * ((t * 0.18) % 1.0), 520, t * 0.6, ka, 0.8)
        sticky(c, 1520, 760, ['watch before', 'journal club'], ramp(t, 3.2, 0.5, e_back), rot=5.0)

# ======================================================================= QUESTION
class Question(Scene):
    dur = 25.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (9.0, 'pop'), (13.5, 'tick'), (17.5, 'chime')]

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'Seeing the beam where we *can’t* look')
        Y = 560
        k = ramp(t, 0.6, 2.5, e_io)
        xs = machine(c, 150, 1770, Y, 1, n=8, prog=k)
        kb = ramp(t, 4.5, 0.8)
        u = ((t - 4.5) * 0.11) % 1.0 if t > 4.5 else 0
        bunch(c, 150 + 1620 * u, Y, u * 6, kb)
        if kb > 0:
            for i, xm in enumerate(xs):     # the beam's shape at each module
                kk = ramp(t, 5.0 + i * 0.25, 0.5) * (1 - ramp(t, 8.6, 0.4) * (0 if i in (0, 7) else 1))
                draw_image(c, phase_img(3, i / 7), xm - 36, Y - 170, 72, 72, kk)
                rrect(c, xm - 36, Y - 170, 72, 72, 4, stroke='line', sw=1.2, a=kk)
        km = ramp(t, 9.0, 0.7, e_expo)
        for i, xm in enumerate(xs):
            if i in (0, 7):
                pill(c, xm, Y + 110, 'screen', 'f', km, cx=True)
            else:
                text(c, '?', xm, Y - 112, 64, 400, 'c', km * (1 - ramp(t, 17.5, 0.5)), 'center', kind='italic')
        ks = window(t, 13.5, 17.6, 0.6, 0.5)
        if ks > 0:
            with layer(c, ks):
                panel(c, 660, 760, 600, 110)
                text(c, 'full beam-physics simulation', 690, 806, 26, 600, 'ink')
                rrect(c, 690, 830, 540, 14, 7, fill='faint')
                rrect(c, 690, 830, max(1, 540 * 0.08 * ramp(t, 13.8, 4.0, e_lin)), 14, 7, fill='g')
                text(c, 'slow', 1230, 806, 22, 500, 'c', 1, 'right', kind='mono')
        kv = ramp(t, 17.5, 0.8, e_expo)
        if kv > 0:
            for i, xm in enumerate(xs):
                if i in (0, 7):
                    continue
                kk = ramp(t, 17.8 + i * 0.12, 0.5)
                draw_image(c, phase_img(3, i / 7), xm - 36, Y - 170, 72, 72, kk * 0.9)
                rrect(c, xm - 36, Y - 170, 72, 72, 4, stroke='y', sw=1.6, a=kk)
            pill(c, W / 2, 790, 'virtual diagnostics: a fast learned model', 'y', kv, cx=True, size=22)
            illus(c, W - MX, 905, kv, 'right')
        caption(c, t, 'Measure in a {y:few} places; {y:predict} the rest.', 19.5, None, y=960, size=30)

# ======================================================================= PHASE SPACE
class PhaseSpace(Scene):
    dur = 24.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (2.5, 'pop'), (7.5, 'draw'), (11.5, 'pop'), (17.0, 'chime')]

    def __init__(self):
        rng = np.random.default_rng(4)
        L = np.array([[1, 0, 0], [0.6, 0.6, 0], [0.2, -0.4, 0.5]])
        self.cloud = rng.normal(size=(700, 3)) @ L.T

    def draw(self, c, t):
        header(c, t, '02', 'background', 'What is *phase space*?')
        k1 = ramp(t, 2.5, 0.8, e_expo)
        if k1 > 0:
            circle(c, 260, 470, 14, fill='y', a=k1, glow=10)
            for i, (lab, colr) in enumerate([('x', 'g'), ('y', 'g'), ('z', 'g'), ('px', 'c'), ('py', 'c'), ('pz', 'c')]):
                kk = ramp(t, 2.8 + i * 0.35, 0.5)
                xx = 180 + (i % 3) * 80
                yy = 560 + (i // 3) * 64
                rrect(c, xx - 32, yy - 32, 64, 46, 10, stroke=colr, sw=1.6, a=kk, fill='panel', fa=0.8 * kk)
                text(c, lab, xx, yy, 26, 500, colr, kk, 'center', kind='italic')
            note(c, 'position', 150, 712, ramp(t, 3.4, 0.5), 15, 'g')
            note(c, 'momentum', 150, 736, ramp(t, 4.5, 0.5), 15, 'c')
            text(c, '6 numbers per particle', 260, 800, 24, 500, 'ink', ramp(t, 5.0, 0.6), 'center')
        k2 = ramp(t, 7.5, 1.0, e_expo)
        if k2 > 0:
            cx, cy, s = 700, 590, 78
            th = 0.25 * t
            R = np.array([[math.cos(th), 0, math.sin(th)], [0, 1, 0], [-math.sin(th), 0, math.cos(th)]])
            P = self.cloud @ R.T
            for p in P[: int(700 * k2)]:
                circle(c, cx + p[0] * s, cy + p[1] * s, 2.4, fill='y', a=0.55 * k2 * (0.6 + 0.4 * math.tanh(p[2])))
            text(c, 'all particles: a cloud in 6D', cx, 860, 24, 500, 'ink', k2, 'center')
            illus(c, cx, 892, k2, 'center', 'illustration · a 3D shadow of it')
        k3 = ramp(t, 11.5, 3.5, e_io)
        if k3 > 0:
            tiles(c, 1060, 360, 0.3, 1, cell=118, gap=26, reveal=k3, labels=True, cols=5)
            text(c, '6 choose 2  =  15 pairs', 1060 + 330, 336, 24, 600, 'ink', ramp(t, 12.0, 0.6), 'center', kind='mono')
        k4 = ramp(t, 17.0, 0.8, e_expo)
        if k4 > 0:
            line(c, 1060, 880, 1060 + 5 * 144 - 26, 880, 'y', k4, 3)
            text(c, 'X', 1060 + 330 - 110, 934, 44, 500, 'y', k4, 'center', kind='italic')
            text(c, '= the beam state', 1060 + 330 + 30, 930, 26, 500, 'ink', k4, 'center')
            illus(c, W - MX, 970, k4, 'right')

# ======================================================================= ROADMAP
class Roadmap(Scene):
    dur = 18.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (4.5, 'pop'), (7.5, 'pop'), (10.5, 'pop'), (13.5, 'pop')]
    CARDS = [('Forward', 'upstream beam  →  {y:downstream} beam', 'f', 4.5),
             ('Inverse: beam', 'downstream beam  →  {y:upstream} beam, with error bars', 'c', 7.5),
             ('Inverse: settings', 'beam  →  the {y:machine settings} that made it', 'x', 10.5),
             ('Tuning', 'find the settings with the {y:least beam loss}', 'y', 13.5)]

    def draw(self, c, t):
        header(c, t, '03', 'this paper', 'One model, *four* jobs')
        k0 = ramp(t, 0.6, 0.8)
        text(c, 'Can a single learned model of the beam serve all of these?', MX, 350, 34, 400, 'ink', k0, kind='italic')
        cw, gap, y0, ch = 395, 30, 420, 330
        for i, (lab, body, colr, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 32, y0 + 1, x + 140, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, f'0{i + 1}', x + 32, y0 + 60, 20, 400, colr, 1, kind='mono')
                    text(c, lab, x + 32, y0 + 120, 38, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 32, y0 + 190, 28, cw - 64, t, t0 + 0.3, 0.03, 0.45)
        caption(c, t, 'Problems usually solved by {y:separate} models, here under {y:one} umbrella.', 15.5, None, y=900, size=30)

# ======================================================================= COMPRESS (VAE)
class Compress(Scene):
    dur = 27.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (3.0, 'draw'), (8.5, 'draw'), (13.5, 'pop'), (19.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '04', 'the model · space', 'Step 1: *compress* the beam')
        cy = 560
        k0 = ramp(t, 0.6, 1.2, e_io)
        tiles(c, 130, 410, 0.2, 1, cell=50, gap=8, reveal=k0)
        text(c, 'X  (15 images)', 130 + 141, 620, 22, 500, 'ink', k0, 'center', kind='mono')
        k1 = ramp(t, 3.0, 0.9, e_expo)
        trapezoid(c, 450, cy, 260, 300, 90, 'g', k1, 'encoder', 'q(z | X)')
        arrow(c, 420, cy, 446, cy, 'g', k1, 2.5)
        kz = ramp(t, 4.2, 1.0)
        zx, zy = 800, cy - latent_h() / 2
        spread = ramp(t, 13.5, 1.2)
        latent(c, zx, zy, zvals(0), kz, cw=46, prog=kz, spread=spread)
        text(c, 'z', zx + 23, zy - 22, 40, 500, 'y', kz, 'center', kind='italic')
        arrow(c, 720, cy, 790, cy, 'y', kz, 2.5, prog=kz)
        note(c, f'{NZ} numbers', zx + 23, zy + latent_h() + 30, kz, 16, 'y', 'center')
        k2 = ramp(t, 8.5, 0.9, e_expo)
        arrow(c, 856, cy, 920, cy, 'y', k2, 2.5, prog=k2)
        trapezoid(c, 930, cy, 260, 90, 300, 'f', k2, 'decoder', 'p(X | z)')
        k3 = ramp(t, 9.4, 1.2, e_io)
        arrow(c, 1200, cy, 1232, cy, 'f', k3, 2.5)
        tiles(c, 1250, 410, 0.2, 1, cell=50, gap=8, reveal=k3, frame='f')
        text(c, 'rebuilt X', 1250 + 141, 620, 22, 500, 'ink', k3, 'center', kind='mono')
        kb = ramp(t, 11.0, 0.6)
        if kb > 0:
            text(c, '≈', 1680, 540, 64, 400, 'f', kb, 'center')
            text(c, 'good rebuild: z kept', 1680, 600, 18, 500, 'muted', kb, 'center', kind='mono')
            text(c, 'what matters', 1680, 626, 18, 500, 'muted', kb, 'center', kind='mono')
        kv = ramp(t, 13.5, 0.8, e_expo)
        pill(c, zx + 23, zy + latent_h() + 60, 'a mean + a spread', 'y', kv, cx=True, size=18)
        ke = ramp(t, 19.0, 0.9, e_expo)
        tex(c, 'bayes', 560, 820, 40, ke, reveal=ke)
        if ke > 0:
            text(c, 'trained by maximizing the ELBO', 1080, 806, 26, 600, 'ink', ke)
            text(c, '= rebuild well  −  keep z tidy', 1080, 846, 24, 400, 'muted', ke, kind='mono')
        illus(c, MX, 930, ramp(t, 1.0, 0.6), s=f'illustration · the paper uses a conditional VAE (CVAE); {NZ} dims is its own example size')

# ======================================================================= EVOLVE (transformer)
class Evolve(Scene):
    dur = 29.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (3.5, 'draw'), (8.0, 'pop'), (11.5, 'chime'), (16.0, 'pop'), (24.5, 'chime')]
    N = 8

    def draw(self, c, t):
        header(c, t, '05', 'the model · time', 'Step 2: *evolve* it, in latent space')
        k0 = ramp(t, 0.6, 1.2, e_io)
        xs = machine(c, 150, 1770, 350, k0, n=self.N, prog=k0, labels=False)
        Yt, Yz = 400, 480
        hi = 5          # the step whose look-back we highlight
        for i, xm in enumerate(xs):
            kt = ramp(t, 3.5 + i * 0.18, 0.5)
            draw_image(c, phase_img(2, i / 7), xm - 28, Yt, 56, 56, kt)
            arrow(c, xm, Yt + 62, xm, Yz - 6, 'g', kt, 1.8, head=8, prog=kt)
            latent(c, xm - 15, Yz, zvals(i), kt, cw=30, ch=14, prog=kt)
            text(c, f'z{i}' if i < self.N - 1 else 'zT', xm, Yz + latent_h(14) + 30, 22, 500, 'y', kt, 'center', kind='italic')
        k1 = ramp(t, 8.0, 3.0, e_lin)
        yb = Yz + latent_h(14) + 52
        for i in range(self.N - 1):
            kk = clamp(k1 * (self.N - 1) - i)
            if kk > 0:
                curve_arrow(c, (xs[i] + 14, yb), (xs[i + 1] - 14, yb), 0.35, 'y', 1, kk, w=2.2, head=9)
        pill(c, W / 2, yb + 40, 'a transformer predicts the next z', 'y', ramp(t, 8.3, 0.6), cx=True)
        k2 = ramp(t, 11.5, 0.9, e_expo)
        tex(c, 'eq1', 520, 860, 38, k2, reveal=k2)
        note(c, 'eq. (1), as printed: each step looks one step back', 520, 925, k2, 16, 'muted', 'center')
        k3 = ramp(t, 16.0, 0.9, e_expo)
        if k3 > 0:
            for j in range(hi):
                curve_arrow(c, (xs[j], Yz - 10), (xs[hi] - 6, Yz - 12), -0.22 - 0.02 * (hi - j), 'g', k3 * 0.75, k3, w=1.6, head=8)
            tex(c, 'chain', 1370, 860, 38, k3, reveal=k3)
            note(c, 'the text: AR(1:T), every earlier step', 1370, 925, k3, 16, 'g', 'center')
        kn = ramp(t, 21.0, 0.6)
        pill(c, 1370, 770, 'trained from one past state and from many', 'g', kn, cx=True, size=16)
        caption(c, t, '{g:Space} (the VAE) and {y:time} (the transformer) are learned {y:separately}, then joined.', 24.5, None, y=1000, size=28)
        illus(c, W - MX, 300, k0, 'right')

# ======================================================================= FORWARD
class Forward(Scene):
    dur = 17.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (3.0, 'draw'), (9.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '06', 'problem 1 · forward', 'Predict the beam *downstream*')
        cy = 560
        k0 = ramp(t, 0.8, 1.0, e_io)
        tiles(c, 130, 420, 0.0, 1, cell=50, gap=8, reveal=k0)
        text(c, 'upstream X0', 130 + 141, 630, 22, 500, 'ink', k0, 'center', kind='mono')
        k1 = ramp(t, 3.0, 0.8, e_expo)
        trapezoid(c, 450, cy, 160, 240, 80, 'g', k1, 'enc')
        n = 6
        xs = [700 + i * 110 for i in range(n)]
        kh = ramp(t, 4.0, 4.5, e_lin)
        for i, xz in enumerate(xs):
            kk = clamp(kh * n - i + 0.6)
            latent(c, xz, cy - latent_h(14) / 2, zvals(i), kk, cw=30, ch=14)
            if i:
                curve_arrow(c, (xs[i - 1] + 34, cy - 70), (xz - 4, cy - 70), 0.4, 'y', 1, clamp(kh * n - i + 1), w=2.2, head=9)
        text(c, 'transformer steps z through the machine', 975, cy + 100, 20, 500, 'y', ramp(t, 4.5, 0.6), 'center', kind='mono')
        k2 = ramp(t, 8.0, 0.8, e_expo)
        trapezoid(c, 1350, cy, 160, 80, 240, 'f', k2, 'dec')
        k3 = ramp(t, 9.0, 1.4, e_io)
        tiles(c, 1530, 420, 1.0, 1, cell=50, gap=8, reveal=k3, frame='f')
        text(c, 'downstream XT', 1530 + 141, 630, 22, 500, 'ink', k3, 'center', kind='mono')
        kx = ramp(t, 11.0, 0.7)
        if kx > 0:
            panel(c, 660, 760, 600, 90, kx)
            text(c, 'full simulation', 700, 815, 26, 500, 'muted', kx)
            line(c, 690, 806, 900, 806, 'c', kx, 2.5)
            text(c, 'not needed at run time', 940, 815, 24, 500, 'f', kx)
        illus(c, W - MX, 930, k0, 'right')

# ======================================================================= INVERSE I
class InverseBeam(Scene):
    dur = 30.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (5.0, 'pop'), (9.0, 'draw'), (13.5, 'tick'), (18.0, 'draw'), (25.0, 'chime')]

    def path(self, j, n=60):
        """A latent trajectory from z_T (right) back to z_0 (left); j > 0 are sampled variants (illustration)."""
        u = np.linspace(0, 1, n)
        rng = np.random.default_rng(j)
        a1, a2 = rng.normal(0, 1, 2) * (0 if j == 0 else 1)
        x = 1460 - u * 700
        y = 560 + 70 * np.sin(u * 3.4 + 0.5) + u ** 1.4 * (a1 * 46 + a2 * 18 * np.sin(u * 6))
        return np.stack([x, y], 1)

    def draw(self, c, t):
        header(c, t, '07', 'problem 2 · inverse', 'Run time *backwards*')
        k0 = ramp(t, 0.6, 1.0, e_io)
        tiles(c, 1560, 440, 1.0, 1, cell=40, gap=6, reveal=k0, cols=3)
        text(c, 'measured downstream', 1560 + 63, 420, 18, 500, 'ink', k0, 'center', kind='mono')
        kp = window(t, 5.0, 13.0, 0.7, 0.6)
        if kp > 0:
            for j, yy in enumerate((400, 650)):
                tiles(c, 180, yy, 0.05, kp, cell=40, gap=6, cols=3, seed=j * 2 + 1)
                curve_arrow(c, (330, yy + 90), (1540, 580), 0.06 * (1 if j == 0 else -1), 'muted', kp * 0.7, kp, w=1.8, dash=[8, 6])
            text(c, 'different upstream beams can look alike downstream', W / 2, 900, 24, 500, 'c', kp, 'center', kind='mono')
        kr = ramp(t, 9.0, 0.8, e_expo)
        tex(c, 'fwd', 520, 340, 30, kr * (1 - 0.5 * ramp(t, 10.5, 0.6)))
        note(c, 'forward training', 520, 384, kr * 0.8, 15, 'y', 'center')
        tex(c, 'rev', 1200, 340, 30, ramp(t, 10.0, 0.8))
        note(c, 'reverse training', 1200, 384, ramp(t, 10.0, 0.8) * 0.8, 15, 'c', 'center')
        kt = ramp(t, 10.5, 2.5, e_io)
        if kt > 0:
            P = self.path(0)
            draw_poly(c, P, 'c', 1, 3, prog=kt, glow=4)
            for q in np.linspace(0, 1, 7):
                if q <= kt:
                    pt = end_point(P, q)
                    circle(c, pt[0], pt[1], 6, fill='c', a=1)
            circle(c, P[0, 0], P[0, 1], 9, fill='y', a=1)
            text(c, 'zT', P[0, 0] + 22, P[0, 1] - 14, 26, 500, 'y', 1, kind='italic')
            if kt >= 1:
                text(c, 'z0', P[-1, 0] - 50, P[-1, 1] - 14, 26, 500, 'c', 1, kind='italic')
        kf = ramp(t, 13.5, 0.8, e_expo)
        if kf > 0:
            for x, lab in ((380, 'encoder'), (540, 'decoder')):
                rrect(c, x - 60, 780, 120, 46, 10, stroke='muted', sw=1.6, a=kf)
                text(c, lab, x, 810, 18, 500, 'muted', kf, 'center', kind='mono')
                lock(c, x + 76, 814, kf)
            rrect(c, 660, 780, 260, 46, 10, stroke='c', sw=2, a=kf, fill='c', fa=0.15 * kf)
            text(c, 'transformer: retrained', 790, 810, 18, 500, 'c', kf, 'center', kind='mono')
        ku = ramp(t, 18.0, 4.0, e_io)
        if ku > 0:
            rng = np.random.default_rng(7)
            for j in range(1, 16):
                P = self.path(j)
                draw_poly(c, P, 'c', 0.32, 1.6, prog=ku)
                e = end_point(P, ku)
                circle(c, e[0], e[1], 3.4, fill='c', a=0.8)
            for j in range(18):
                dx, dy = rng.normal(0, 1, 2)
                circle(c, 1460 + dx * 8, 595 + dy * 12, 3, fill='y', a=0.8 * ramp(t, 18.0, 0.6))
            note(c, 'samples of zT from the encoder', 1460, 690, ramp(t, 18.2, 0.6), 15, 'y', 'center')
        ke = ramp(t, 25.0, 0.8, e_expo)
        if ke > 0:
            xb = 720
            line(c, xb, 470, xb, 720, 'ink', ke, 2.5)
            line(c, xb - 14, 470, xb + 14, 470, 'ink', ke, 2.5)
            line(c, xb - 14, 720, xb + 14, 720, 'ink', ke, 2.5)
            text(c, 'spread  =  error bar', xb - 24, 600, 24, 600, 'ink', ke, 'right')
            text(c, '(aleatoric uncertainty)', xb - 24, 634, 18, 400, 'muted', ke, 'right', kind='mono')
        illus(c, W - MX, 960, k0, 'right')

# ======================================================================= INVERSE II
class InverseSettings(Scene):
    dur = 24.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (6.0, 'tick'), (8.5, 'draw'), (13.5, 'pop'), (19.0, 'chime')]

    def knob(self, c, x, y, v, lab, a, colr='f'):
        if a <= 0:
            return
        circle(c, x, y, 36, fill='panel2', stroke=colr, sw=2.2, a=a)
        ang = math.radians(-220 + 260 * v)
        line(c, x, y, x + 26 * math.cos(ang), y + 26 * math.sin(ang), colr, a, 3.5)
        text(c, lab, x, y + 64, 16, 500, 'muted', a, 'center', kind='mono')

    def draw(self, c, t):
        header(c, t, '08', 'problem 3 · inverse', 'Which *settings* made this beam?')
        cy = 590
        k0 = ramp(t, 0.6, 1.0, e_io)
        tiles(c, 130, 470, 0.6, 1, cell=50, gap=8, reveal=k0)
        text(c, 'X', 130 + 141, 450, 30, 500, 'ink', k0, 'center', kind='italic')
        for i, (v, lab) in enumerate([(0.3, 'phase 1'), (0.7, 'amplitude 1'), (0.55, 'phase 2'), (0.4, 'amplitude 2')]):
            self.knob(c, 1500 + (i % 2) * 170, 500 + (i // 2) * 170, v, lab, ramp(t, 1.0 + i * 0.25, 0.6))
        text(c, 'y', 1585, 440, 30, 500, 'f', k0, 'center', kind='italic')
        note(c, 'rf cavity set-points', 1585, 840, k0, 15, 'f', 'center')
        kd = window(t, 6.0, 8.6, 0.5, 0.5)
        if kd > 0:
            curve_arrow(c, (440, 540), (1440, 540), -0.12, 'c', kd, kd, w=2.5, dash=[10, 8])
            text(c, 'directly: hard', 940, 420, 26, 600, 'c', kd, 'center')
        k1 = ramp(t, 8.5, 0.8, e_expo)
        trapezoid(c, 450, cy, 200, 240, 80, 'g', k1, 'encoder', 'already trained')
        tex(c, 'dag', W / 2, 370, 44, k1, reveal=k1)
        kz = ramp(t, 9.2, 0.8)
        latent(c, 690, cy - latent_h() / 2, zvals(3), kz, cw=40, prog=kz)
        text(c, 'z', 710, cy - latent_h() / 2 - 20, 34, 500, 'y', kz, 'center', kind='italic')
        k2 = ramp(t, 13.5, 1.0, e_expo)
        if k2 > 0:
            layers = [6, 7, 5, 4]
            pos = [[(860 + li * 160, cy + (j - (n - 1) / 2) * 52) for j in range(n)] for li, n in enumerate(layers)]
            for li in range(len(pos) - 1):
                for p in pos[li]:
                    for q in pos[li + 1]:
                        line(c, *p, *q, 'f', 0.18 * k2, 1)
            for L in pos:
                for p in L:
                    circle(c, *p, 9, fill='panel2', stroke='f', sw=1.8, a=k2)
            arrow(c, 745, cy, 845, cy, 'y', k2, 2.2)
            arrow(c, 1360, cy, 1450, cy, 'f', k2, 2.2)
            text(c, 'small dense network  g', 1100, cy + 220, 20, 500, 'f', k2, 'center', kind='mono')
            tex(c, 'reg', 1100, 900, 36, ramp(t, 14.3, 0.8), reveal=ramp(t, 14.3, 1.0))
        illus(c, MX, 960, k0)

# ======================================================================= TUNING
class Tuning(Scene):
    dur = 34.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (9.5, 'draw'), (14.0, 'pop'), (19.0, 'tick'), (23.5, 'draw'), (28.0, 'chime')]
    PX, PY, PW, PH = 860, 330, 940, 600

    def __init__(self):
        n = 160
        u, v = np.meshgrid(np.linspace(-1, 1, n), np.linspace(1, -1, n))
        # objective J (lower = less beam loss): three basins, an illustration
        J = 1.0 - 0.9 * np.exp(-((u + 0.45) ** 2 + (v - 0.2) ** 2) / 0.05) \
                - 0.85 * np.exp(-((u - 0.35) ** 2 + (v + 0.35) ** 2) / 0.04) \
                - 0.6 * np.exp(-((u - 0.75) ** 2 + (v - 0.6) ** 2) / 0.03) + 0.15 * (u ** 2 + v ** 2)
        self.J = (J - J.min()) / (J.max() - J.min())
        rng = np.random.default_rng(11)
        self.samples = rng.uniform(-0.95, 0.95, (34, 2))
        self.samples[-6:] = [(-0.43, 0.18), (0.33, -0.33), (-0.47, 0.22), (0.37, -0.36), (0.74, 0.58), (0.77, 0.62)]

    def to_px(self, u, v):
        return self.PX + (u + 1) / 2 * self.PW, self.PY + (1 - (v + 1) / 2) * self.PH

    def inside(self, u, v):
        return ((u + 0.1) / 0.85) ** 2 + ((v + 0.05 - 0.25 * u) / 0.62) ** 2 < 1

    def draw(self, c, t):
        header(c, t, '09', 'problem 4 · tuning', 'Tune in the *latent* space')
        k0 = ramp(t, 0.6, 0.8, e_expo)
        tex(c, 'argy', 440, 380, 38, k0, reveal=k0)
        note(c, 'J(y): e.g. total fractional beam loss', 440, 444, k0, 16, 'muted', 'center')
        kk = ramp(t, 4.0, 1.5, e_io)
        for i in range(48):
            a = clamp(kk * 48 - i)
            if a <= 0:
                continue
            x, y = 165 + (i % 12) * 50, 510 + (i // 12) * 50
            circle(c, x, y, 16, fill='panel2', stroke='f', sw=1.4, a=a)
            ang = math.radians(-220 + 260 * ((i * 0.37) % 1))
            line(c, x, y, x + 11 * math.cos(ang), y + 11 * math.sin(ang), 'f', a, 2)
        note(c, 'p = tens to hundreds of knobs', 440, 730, kk, 16, 'c', 'center')
        note(c, 'each try = a slow simulation', 440, 756, kk, 16, 'c', 'center')
        kl = ramp(t, 9.5, 1.0, e_expo)
        if kl > 0:
            with layer(c, kl):
                draw_image(c, array_image(1 - self.J, vmin=0, vmax=1.25), self.PX, self.PY, self.PW, self.PH)
                rrect(c, self.PX, self.PY, self.PW, self.PH, 6, stroke='line', sw=1.4)
                text(c, 'a 2D slice of latent space  (dark = high loss, bright = low)', self.PX, self.PY - 16, 17, 400, 'muted', 1, kind='mono')
            tex(c, 'argz', 440, 850, 32, ramp(t, 10.0, 0.8), reveal=ramp(t, 10.0, 1.0))
        ks = ramp(t, 14.0, 9.0, e_lin)
        kprune = ramp(t, 23.5, 0.8)
        n = int(len(self.samples) * ks)
        for (u, v) in self.samples[:n]:
            x, y = self.to_px(u, v)
            if self.inside(u, v) or t < 19.0:
                circle(c, x, y, 7, fill='g', stroke='ink', sw=1.2, a=1)
            else:
                a = 1 - 0.6 * kprune
                line(c, x - 7, y - 7, x + 7, y + 7, 'r', a, 3)
                line(c, x - 7, y + 7, x + 7, y - 7, 'r', a, 3)
        if ks > 0:
            pill(c, self.PX + 20, self.PY + 20, 'bayesian optimization', 'g', ramp(t, 14.0, 0.6))
            note(c, 'z  →  g(z) = y  →  J(y)', self.PX + 20, self.PY + 90, ramp(t, 14.4, 0.6), 18, 'ink')
        ku = ramp(t, 19.0, 0.8)
        if ku > 0:
            outline = []
            for th in np.linspace(0, 2 * math.pi, 120):
                uu = -0.1 + 0.85 * math.cos(th)
                vv = -0.05 + 0.25 * uu + 0.62 * math.sin(th)
                outline.append(self.to_px(uu, vv))
            pts = np.array(outline + [outline[0]])
            draw_poly(c, pts, 'f', ku, 2.5, dash=[10, 6], prog=ku)
            note(c, 'realistic beams', pts[30][0] + 10, pts[30][1] - 14, ku, 18, 'f')
            note(c, 'outside: decodes to beams that can’t exist', self.PX + self.PW - 20, self.PY + self.PH - 20, ku, 16, 'r', 'right')
        if kprune > 0:
            pill(c, self.PX + 20, self.PY + self.PH - 56, 'classifier prunes the unrealistic', 'r', kprune, size=16)
        ko = ramp(t, 28.0, 0.8, e_back)
        if ko > 0:
            for (u, v) in [(-0.45, 0.2), (0.35, -0.35)]:
                x, y = self.to_px(u, v)
                text(c, '★', x, y + 14, max(1, 44 * ko), 400, 'y', clamp(ko), 'center', glow=8)
        note(c, 'several distinct optima (as reported in ref. 37)', self.PX + self.PW / 2, self.PY + self.PH + 34, clamp(ko), 16, 'y', 'center')
        illus(c, MX, 960, kl)

# ======================================================================= LIMITS
class Limits(Scene):
    dur = 24.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.5, 'pop'), (10.0, 'pop'), (16.5, 'pop')]
    CARDS = [('A summary paper', 'Every result it mentions lives in {y:earlier papers} (refs. 32–37). This video shows {y:no numbers}; every picture is an illustration.', 'c', 2.5),
             ('Simulation first', 'The tuning claims come from {y:simulation} studies. How they carry to a {y:real machine} is a question for those papers.', 'g', 10.0),
             ('Eq. 1 vs the text', 'Eq. 1 is printed in {y:first-order} (Markov) form; the text says the model conditions on {y:all past steps}.', 'y', 16.5)]

    def draw(self, c, t):
        header(c, t, '10', 'limits', 'A few *cautions*')
        cw, gap, y0, ch = 532, 42, 360, 440
        for i, (lab, body, colr, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, lab, x + 36, y0 + 90, 40, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 36, y0 + 160, 29, cw - 72, t, t0 + 0.3, 0.025, 0.45)

# ======================================================================= DISCUSSION
class Discussion(Scene):
    dur = 33.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (1.5, 'pop'), (7.5, 'pop'), (14.0, 'pop'), (20.0, 'pop'), (26.0, 'pop')]
    QS = [
        'What does the latent space {y:throw away}, and could that matter for beam loss?',
        'When is the encoder’s spread enough uncertainty, and when do we also need the {y:model’s own} uncertainty?',
        'If many settings give the same beam, what does a {y:settings estimate} even mean?',
        'Is the feasibility classifier just defining “physical” as {y:“looks like the training data”}?',
        'Could one shared latent space be a {y:single point of failure} for all four tasks at once?',
    ]
    T0 = [1.5, 7.5, 14.0, 20.0, 26.0]

    def draw(self, c, t):
        header(c, t, '11', 'discussion', 'Before we *meet*: questions to think about')
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
        sticky(c, 1600, 900, ['bring one', 'to the desk'], ramp(t, 29.0, 0.5, e_back), rot=-4.0, w=230, h=170, tag='homework')

# ======================================================================= END
class End(Scene):
    dur = 16.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (15.0, 'outro')]

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 230, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, 'One {g:encoder}, one {y:time model}, four jobs: compress the beam once, then {y:reuse} that latent space everywhere.',
             W / 2, 310, 50, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        for i, (lab, colr) in enumerate([('forward', 'f'), ('inverse: beam', 'c'), ('inverse: settings', 'x'), ('tuning', 'y')]):
            k = ramp(t, 2.5 + i * 0.3, 0.8, e_expo)
            pill(c, MX + 160 + i * 420, 500, lab, colr, k, size=22)
        k2 = ramp(t, 5.0, 0.9)
        with layer(c, k2):
            line(c, MX, 640, W - MX, 640, 'line', 1, 1.5)
            text(c, 'M. Rautela & A. Scheinker (2026).  Advancing accelerator virtual beam diagnostics', MX, 700, 27, 600, 'ink')
            text(c, 'through latent evolution modeling.  NAPAC 2025, Sacramento.', MX, 740, 27, 600, 'ink')
            text(c, 'arxiv.org/abs/2602.22618', MX, 790, 22, 500, 'g', 1, kind='mono')
            note(c, 'an unofficial explainer, not made by the authors  ·  all visuals are illustrations', MX, 840, 0.9, 16)
        k3 = ramp(t, 6.0, 0.8)
        lamp(c, 1640, 790, 1.15, k3, on=k3)
        hand(c, 'see you at the desk', 1380, 990, 36, 'pencil', k3, -3.0, ramp(t, 6.4, 1.0, e_lin))
