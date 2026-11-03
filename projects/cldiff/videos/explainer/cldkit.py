"""Shared drawing pieces for the conditional latent diffusion explainer.

`figcard` shows a crop of one of the paper's own figures (data/<name>.png, made by extract_paper.py) on a light card
with its figure number. Native drawings that are not data carry an `illustration` label on screen."""
import functools, math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer import project

PAPER = 'Scheinker & Williams (2025)'
CARD = '#f6f1e7'

def illus(c, x, y, a=1.0, align='left', s='illustration'):
    note(c, s, x, y, a * 0.85, 15, 'muted', align)

@functools.lru_cache(maxsize=32)
def fig(name):
    return skia.Image.open(project.get().find('data', name + '.png'))

def fig_aspect(name):
    im = fig(name)
    return im.height() / im.width()

def figcard(c, name, x, y, w=None, a=1.0, label=None, h=None, pad=10, k=1.0, credit=True, src=None):
    """A paper figure crop on a light card, top-left at (x, y), image width w (or height h). Returns (w, h) of the image.
    `src` = (x0, y0, x1, y1) in 0..1 picks a sub-rectangle of the crop."""
    im = fig(name)
    sx0, sy0, sx1, sy1 = src or (0, 0, 1, 1)
    asp = (im.height() * (sy1 - sy0)) / (im.width() * (sx1 - sx0))
    if w is None:
        w = h / asp
    h = w * asp
    if a <= 0:
        return w, h
    with layer(c, a * k):
        with xform(c, 0, 0, 0.94 + 0.06 * k, 0, x + w / 2, y + h / 2):
            rrect(c, x - pad, y - pad, w + 2 * pad, h + 2 * pad, 10, fill=CARD)
            p = skia.Paint(AntiAlias=True)
            r = skia.Rect.MakeLTRB(sx0 * im.width(), sy0 * im.height(), sx1 * im.width(), sy1 * im.height())
            c.drawImageRect(im, r, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if label and credit:
        note(c, f'{label} · {PAPER}', x - pad, y + h + pad + 22, a, 15, 'muted')
    return w, h

def box(c, x, y, w, h, title, colr, a, k=1.0, sub=None, size=28):
    if a <= 0:
        return
    with layer(c, a * k):
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

def machine(c, x0, x1, y, a=1.0, n=8, prog=1.0, labels=True):
    """A beamline: a pipe with n modules, alternating RF cavities (blue) and magnets (coral). Returns centre xs."""
    xs = [x0 + (x1 - x0) * (i + 0.5) / n for i in range(n)]
    if a <= 0:
        return xs
    line(c, x0, y, x0 + (x1 - x0) * prog, y, 'faint', a, 3)
    for i, xm in enumerate(xs):
        k = clamp(prog * n - i)
        if k <= 0:
            continue
        with layer(c, a * k):
            if i % 2 == 0:
                for j in range(3):
                    circle(c, xm - 26 + j * 26, y, 15, fill='panel2', stroke='g', sw=2)
            else:
                rrect(c, xm - 22, y - 34, 44, 24, 5, fill='c', fa=0.25)
                rrect(c, xm - 22, y + 10, 44, 24, 5, fill='c', fa=0.25)
                rrect(c, xm - 22, y - 34, 44, 24, 5, stroke='c', sw=1.8)
                rrect(c, xm - 22, y + 10, 44, 24, 5, stroke='c', sw=1.8)
            if labels:
                text(c, ('rf cavity' if i % 2 == 0 else 'magnet'), xm, y + 64, 15, 400, 'muted', 1, 'center', kind='mono')
    return xs

def bunch(c, x, y, s, a=1.0, scale=1.0):
    if a <= 0:
        return
    rx = (26 + 10 * math.sin(s * 5.0)) * scale
    ry = (14 + 7 * math.cos(s * 3.7)) * scale
    with xform(c, x, y, 1, 25 * math.sin(s * 2.3)):
        for r, al in ((1.6, 0.10), (1.25, 0.2), (1.0, 0.5), (0.6, 0.8)):
            c.drawOval(skia.Rect.MakeXYWH(-rx * r, -ry * r, 2 * rx * r, 2 * ry * r), paint('y', a * al))

def trapezoid(c, x, y, w, h0, h1, color, a=1.0, label=None, sub=None):
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

# ---------------------------------------------------------------- an 8x8x3 latent grid (illustration)
@functools.lru_cache(maxsize=1)
def _latent_base():
    """A smooth 8x8x3 pattern in the spirit of the paper's Fig. 4 latents (green field, magenta core). Not data."""
    u, v = np.meshgrid(np.linspace(-1, 1, 8), np.linspace(-1, 1, 8))
    core = np.exp(-(u ** 2 + (v * 1.2) ** 2) / 0.35)
    r = 0.15 + 0.8 * core
    g = 0.85 - 0.5 * core + 0.1 * np.sin(3 * u)
    b = 0.2 + 0.7 * core * (0.6 + 0.4 * np.cos(2 * v))
    return np.clip(np.stack([r, g, b], -1), 0, 1)

@functools.lru_cache(maxsize=1)
def _noise():
    return np.random.default_rng(5).uniform(0, 1, (8, 8, 3))

def latent_grid(c, x, y, s, noise=0.0, a=1.0, cell_gap=1.5):
    """Draw the 8x8x3 latent as an RGB pixel grid of side s, blended toward fixed noise by `noise` (0..1)."""
    if a <= 0:
        return
    al = 1 - noise
    z = math.sqrt(al) * _latent_base() + math.sqrt(1 - al) * _noise() if noise > 0 else _latent_base()
    z = np.clip(z / max(1e-6, math.sqrt(al) + math.sqrt(1 - al)) if noise > 0 else z, 0, 1)
    cs = s / 8
    for i in range(8):
        for j in range(8):
            rgb = tuple(int(255 * q) for q in z[i, j])
            rrect(c, x + j * cs, y + i * cs, cs - cell_gap, cs - cell_gap, 2, fill='#%02x%02x%02x' % rgb, a=a)
    rrect(c, x - 3, y - 3, s + 6 - cell_gap, s + 6 - cell_gap, 4, stroke='line', sw=1.2, a=a)

def chips(c, x, y, n, color, a=1.0, w=14, h=34, gap=3, prog=1.0, vals=None):
    """A row of n small cells (a vector). Returns total width."""
    for i in range(n):
        k = clamp(prog * n - i)
        if k > 0 and a > 0:
            v = 0.55 if vals is None else vals[i]
            rrect(c, x + i * (w + gap), y, w, h, 3, fill=color, fa=(0.15 + 0.7 * v) * k * a)
            rrect(c, x + i * (w + gap), y, w, h, 3, stroke=color, sw=1.1, a=0.8 * k * a)
    return n * (w + gap) - gap
