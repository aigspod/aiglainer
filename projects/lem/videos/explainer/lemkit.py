"""Shared drawing pieces for the LEM explainer: boxes, curved arrows, the 15 phase-space tiles, latent vectors,
the accelerator strip. Everything here is an ILLUSTRATION: arXiv:2602.22618 has no figures or data of its own,
so every image of a beam is a synthetic Gaussian-ish density, labelled `illustration` on screen."""
import functools, itertools, math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *

COORDS = ['x', 'y', 'z', 'px', 'py', 'pz']
PAIRS = list(itertools.combinations(range(6), 2))          # 15 = 6 choose 2
PAIR_LABELS = [f'{COORDS[i]}–{COORDS[j]}' for i, j in PAIRS]
NZ = 8          # latent size drawn on screen: the paper's own example ("e.g. an 8-dimensional latent", p. 3)

def illus(c, x, y, a=1.0, align='left', s='illustration'):
    note(c, s, x, y, a * 0.85, 15, 'muted', align)

def box(c, x, y, w, h, title, colr, a, k=1.0, sub=None, size=28):
    if a <= 0:
        return
    with layer(c, a * k):
        with xform(c, 0, 0, 0.92 + 0.08 * k, 0, x + w / 2, y + h / 2):
            rrect(c, x, y, w, h, 16, fill='panel', fa=0.85)
            rrect(c, x, y, w, h, 16, stroke=colr, sw=2.2, a=1)
            text(c, title, x + w / 2, y + h / 2 + (0 if sub is None else -8) + size * 0.36, size, 650, 'ink', 1, 'center')
            if sub:
                text(c, sub, x + w / 2, y + h / 2 + 34, 20, 500, 'muted', 1, 'center')

def curve_arrow(c, p0, p1, bend, color, a, prog=1.0, w=2.5, dash=None, head=12):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    mid = (p0 + p1) / 2 + np.array([-(p1 - p0)[1], (p1 - p0)[0]]) * bend
    ts = np.linspace(0, 1, 40)[:, None]
    pts = (1 - ts) ** 2 * p0 + 2 * (1 - ts) * ts * mid + ts ** 2 * p1
    if a <= 0 or prog <= 0:
        return pts
    draw_poly(c, pts, color, a, w, prog, dash=dash)
    e = end_point(pts, prog)
    e0 = end_point(pts, max(0, prog - 0.03))
    ang = math.atan2(e[1] - e0[1], e[0] - e0[0])
    pth = skia.Path()
    pth.moveTo(*e)
    pth.lineTo(e[0] - head * math.cos(ang - 0.42), e[1] - head * math.sin(ang - 0.42))
    pth.lineTo(e[0] - head * math.cos(ang + 0.42), e[1] - head * math.sin(ang + 0.42))
    pth.close()
    c.drawPath(pth, paint(color, a))
    return pts

# ---------------------------------------------------------------- phase-space tiles (illustration)
@functools.lru_cache(maxsize=4096)
def _density(p, q, seed=0):
    """A synthetic 2D density for projection pair p at evolution stage q (0..20): a correlated, slightly bent
    Gaussian whose tilt, width and bend drift along the machine. Not data."""
    s = q / 20.0
    u, v = np.meshgrid(np.linspace(-3, 3, 48), np.linspace(-3, 3, 48))
    rho = 0.75 * math.sin(p * 1.31 + s * 2.6 + seed * 0.9)
    sx = 0.85 + 0.35 * math.cos(p * 0.77 + s * 2.1 + seed)
    sy = 0.85 + 0.35 * math.sin(p * 1.13 - s * 1.7 + seed * 0.5)
    bend = 0.22 * math.sin(p * 0.6 + 1.0 + seed) * (0.3 + s)
    vv = v - bend * (u ** 2 - 1)
    a, b = u / sx, vv / sy
    d = np.exp(-(a * a - 2 * rho * a * b + b * b) / (2 * (1 - rho * rho)))
    if p % 4 == 1:          # a faint halo on some pairs, so they don't all look alike
        d += 0.18 * np.exp(-((u - 1.6 * math.cos(s * 3 + p)) ** 2 + (vv - 1.2) ** 2) / 0.5)
    return array_image(d / d.max() * 0.95)

def phase_img(p, s, seed=0):
    return _density(p, int(round(clamp(s) * 20)), seed)

def tiles(c, x, y, s, a=1.0, cell=58, gap=8, reveal=1.0, labels=False, seed=0, frame='line', cols=5):
    """The 15 projections in a cols x (15/cols) grid; `reveal` 0..1 pops them in one by one. Returns (w, h)."""
    rows = math.ceil(15 / cols)
    for n in range(15):
        k = clamp(reveal * 15 - n)
        if k <= 0 or a <= 0:
            continue
        i, j = n % cols, n // cols
        xx, yy = x + i * (cell + gap), y + j * (cell + gap + (18 if labels else 0))
        with layer(c, a * k):
            draw_image(c, phase_img(n, s, seed), xx, yy, cell, cell)
            rrect(c, xx, yy, cell, cell, 4, stroke=frame, sw=1.2)
            if labels:
                text(c, PAIR_LABELS[n], xx + cell / 2, yy + cell + 16, 13, 400, 'muted', 1, 'center', kind='mono')
    return cols * (cell + gap) - gap, rows * (cell + gap + (18 if labels else 0)) - gap

# ---------------------------------------------------------------- latent vectors
def zvals(k, seed=0):
    return [0.5 + 0.42 * math.sin(i * 1.7 + k * 0.55 + seed * 1.3) * math.cos(i * 0.4 - k * 0.3) for i in range(NZ)]

def latent(c, x, y, vals, a=1.0, cw=34, ch=22, color='y', spread=None, label=None, prog=1.0):
    """A latent vector as a column of NZ cells; brightness = value. `spread` (0..1) draws each cell as a
    small bell (mean and width) instead: the VAE's distribution over z."""
    if a <= 0:
        return
    with layer(c, a):
        for i, v in enumerate(vals):
            k = clamp(prog * NZ - i)
            if k <= 0:
                continue
            yy = y + i * (ch + 4)
            rrect(c, x, yy, cw, ch, 4, fill=color, fa=0.12 + 0.75 * v * k)
            rrect(c, x, yy, cw, ch, 4, stroke=color, sw=1.3, a=0.8 * k)
            if spread:
                xs = np.linspace(x + 3, x + cw - 3, 24)
                mu, sd = x + 4 + v * (cw - 8), 2.0 + 5.0 * spread
                ys = yy + ch - 3 - (ch - 6) * np.exp(-((xs - mu) ** 2) / (2 * sd ** 2))
                draw_poly(c, np.stack([xs, ys], 1), 'ink', k * spread, 1.6)
        if label:
            text(c, label, x + cw / 2, y + NZ * (ch + 4) + 24, 24, 500, color, 1, 'center', kind='italic')

def latent_h(ch=22):
    return NZ * (ch + 4) - 4

# ---------------------------------------------------------------- the machine
def machine(c, x0, x1, y, a=1.0, n=8, prog=1.0, labels=True, hi=None):
    """A beamline: a pipe with n modules, alternating RF cavities (blue) and magnets (coral).
    Returns the modules' centre x positions."""
    xs = [x0 + (x1 - x0) * (i + 0.5) / n for i in range(n)]
    if a <= 0:
        return xs
    line(c, x0, y, x0 + (x1 - x0) * prog, y, 'faint', a, 3)
    for i, xm in enumerate(xs):
        k = clamp(prog * n - i)
        if k <= 0:
            continue
        hl = 1.0 if hi is None or hi == i else 0.45
        with layer(c, a * k * hl):
            if i % 2 == 0:       # RF cavity: a row of cells
                for j in range(3):
                    circle(c, xm - 26 + j * 26, y, 15, fill='panel2', stroke='g', sw=2)
            else:                # magnet: a quadrupole block
                rrect(c, xm - 22, y - 34, 44, 24, 5, fill='c', fa=0.25)
                rrect(c, xm - 22, y + 10, 44, 24, 5, fill='c', fa=0.25)
                rrect(c, xm - 22, y - 34, 44, 24, 5, stroke='c', sw=1.8)
                rrect(c, xm - 22, y + 10, 44, 24, 5, stroke='c', sw=1.8)
            if labels:
                text(c, ('rf cavity' if i % 2 == 0 else 'magnet'), xm, y + 64, 15, 400, 'muted', 1, 'center', kind='mono')
    return xs

def bunch(c, x, y, s, a=1.0, scale=1.0):
    """The particle bunch as a soft ellipse whose shape drifts with s (illustration)."""
    if a <= 0:
        return
    rx = (26 + 10 * math.sin(s * 5.0)) * scale
    ry = (14 + 7 * math.cos(s * 3.7)) * scale
    rot = 25 * math.sin(s * 2.3)
    with xform(c, x, y, 1, rot):
        for r, al in ((1.6, 0.10), (1.25, 0.2), (1.0, 0.5), (0.6, 0.8)):
            p = paint('y', a * al)
            c.drawOval(skia.Rect.MakeXYWH(-rx * r, -ry * r, 2 * rx * r, 2 * ry * r), p)

def trapezoid(c, x, y, w, h0, h1, color, a=1.0, label=None, sub=None):
    """Encoder (h0 > h1) or decoder (h0 < h1) as a funnel, centred on y."""
    if a <= 0:
        return
    pth = skia.Path()
    pth.moveTo(x, y - h0 / 2); pth.lineTo(x + w, y - h1 / 2); pth.lineTo(x + w, y + h1 / 2); pth.lineTo(x, y + h0 / 2); pth.close()
    c.drawPath(pth, paint(color, a * 0.13))
    c.drawPath(pth, paint(color, a, stroke=2.2))
    if label:
        text(c, label, x + w / 2, y + 8, 24, 650, 'ink', a, 'center')
    if sub:
        text(c, sub, x + w / 2, y + max(h0, h1) / 2 + 30, 17, 400, 'muted', a, 'center', kind='mono')

def lock(c, x, y, a=1.0, color='muted'):
    if a <= 0:
        return
    pth = skia.Path()
    pth.addArc(skia.Rect.MakeXYWH(x - 8, y - 18, 16, 18), 180, 180)
    c.drawPath(pth, paint(color, a, stroke=2.4))
    rrect(c, x - 12, y - 9, 24, 18, 3, fill=color, a=a)
