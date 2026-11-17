"""trustkit: drawing pieces for "What Did It Learn to Trust?" (weatherdreamer/videos/trust), an explainer of
Duffy, Penn, Ballard, Posch & Vandal, "WeatherDreamer", arXiv:2611.18393v1. Independent of videos/loop.

Paper figures
  fig(name)                        the paper's own figure as a skia image, from projects/weatherdreamer/data/figs/
                                   (made by projects/weatherdreamer/extract_paper.py; not in git)
  figcard(c, name, x, y, w, a, label, src=(x0, y0, x1, y1), k)   a crop on a light card, labelled 'Fig. N · Duffy et al. 2026'
  crop_rect(name, src, x, y, w)    where a sub-rectangle of a crop lands on screen (for highlight boxes)

Labels (house rule: every chart or drawing says what it is)
  tag(c, ILLUS | OURS | text, x, y, a, align)      lowercase mono; OURS ('our reading', 'our arithmetic') is amber
  src(c, 'Table 2', x, y, a, align)                'data: Table 2 · arXiv:2611.18393'
  hdr(c, t, num, kicker, title, sub)               section header

Charts typed from the paper's text and tables (each call site names the section or table)
  hbar(c, x, y, w, v, vmax, color, a, prog, h)     one horizontal bar
  exhibit(c, x, y, s, a, k)                        a detective's evidence tag ('exhibit a')

Scenes: TitleCard, EndCard, question_cards(c, t, qs).
Every helper animates from (t, t0) so narrated time-warps work.
"""
import functools, math, os
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash, hand_arrow

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.normpath(os.path.join(HERE, '..', '..', 'data', 'figs'))

PAPER = 'Duffy et al. 2026'
TITLE = 'WeatherDreamer: Learning a World Model from Multimodal Earth Observations'
AUTHORS = 'Kate Duffy  ·  Elise Penn  ·  Tristan Ballard  ·  August Posch  ·  Thomas J. Vandal'
AFFIL = 'zeus ai, inc.  ·  arxiv:2611.18393  ·  13 nov 2026'
CITE = 'Duffy, Penn, Ballard, Posch & Vandal.  WeatherDreamer: Learning a World Model from Multimodal Earth Observations.  arXiv:2611.18393v1, 2026.'
ARXIV = 'arxiv.org/abs/2611.18393'
CARD = '#f6f1e7'

ILLUS, OURS = 'illustration', 'our'
# colours: WeatherDreamer amber, the operational systems blue, the optimum / reference green, trouble coral
WD, OPS, REF, BAD = 'y', 'g', 'f', 'c'

# ---------------------------------------------------------------- paper figures
@functools.lru_cache(maxsize=32)
def fig(name):
    path = os.path.join(FIGS, name + '.png')
    if not os.path.exists(path):
        raise SystemExit(f'missing {path}: the paper\'s figures are not in git. Put the paper (arXiv:2611.18393v1) at '
                         'projects/weatherdreamer/paper/paper.pdf and run '
                         '`python projects/weatherdreamer/extract_paper.py`.')
    return skia.Image.open(path)

def crop_size(name, src, w=None, h=None):
    im = fig(name)
    sx0, sy0, sx1, sy1 = src or (0, 0, 1, 1)
    asp = (im.height() * (sy1 - sy0)) / (im.width() * (sx1 - sx0))
    if w is None:
        w = h / asp
    return w, w * asp

def crop_rect(name, src, x, y, w, sub):
    """Screen rectangle (x, y, w, h) of `sub` (fractions of the whole figure) inside a crop `src` drawn at (x, y, w)."""
    cw, ch = crop_size(name, src, w)
    sx0, sy0, sx1, sy1 = src or (0, 0, 1, 1)
    fx = lambda v: x + (v - sx0) / (sx1 - sx0) * cw
    fy = lambda v: y + (v - sy0) / (sy1 - sy0) * ch
    return fx(sub[0]), fy(sub[1]), fx(sub[2]) - fx(sub[0]), fy(sub[3]) - fy(sub[1])

def figcard(c, name, x, y, w=None, a=1.0, label=None, h=None, pad=10, k=1.0, src=None, card=True):
    """A crop of the paper's own figure on a light card, top-left at (x, y). Returns (w, h) of the image."""
    im = fig(name)
    w, h = crop_size(name, src, w, h)
    if a <= 0:
        return w, h
    sx0, sy0, sx1, sy1 = src or (0, 0, 1, 1)
    with layer(c, a * k):
        with xform(c, 0, 0, 0.95 + 0.05 * k, 0, x + w / 2, y + h / 2):
            if card:
                rrect(c, x - pad, y - pad, w + 2 * pad, h + 2 * pad, 10, fill=CARD)
            r = skia.Rect.MakeLTRB(sx0 * im.width(), sy0 * im.height(), sx1 * im.width(), sy1 * im.height())
            c.drawImageRect(im, r, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.FilterMode.kLinear),
                            skia.Paint(AntiAlias=True))
    if label:
        note(c, f'{label} · {PAPER}', x - pad, y + h + pad + 24, a, 15, 'muted')
    return w, h

def highlight(c, x, y, w, h, color='y', a=1.0, prog=1.0, pad=6):
    """A glowing frame drawn around a region (prog draws it on)."""
    if a <= 0 or prog <= 0:
        return
    pts = [(x - pad, y - pad), (x + w + pad, y - pad), (x + w + pad, y + h + pad), (x - pad, y + h + pad), (x - pad, y - pad)]
    draw_poly(c, np.array(pts, float), color, a, 4, prog=prog, glow=8)

# ---------------------------------------------------------------- labels
def tag(c, s, x, y, a=1.0, align='left', size=16):
    colr = 'y' if s.startswith(OURS) else 'muted'
    note(c, s, x, y, a * (1.0 if colr == 'y' else 0.9), size, colr, align)

def src(c, where, x, y, a=1.0, align='left', size=16):
    note(c, f'data: {where}  ·  arXiv:2611.18393', x, y, a * 0.9, size, 'muted', align)

def hdr(c, t, num, kick, title, sub=None, **kw):
    header(c, t, num, kick, title, sub=sub, **kw)

def exhibit(c, x, y, s, a=1.0, k=1.0, color='y', rot=-4):
    """A manila evidence tag with a string hole: the detective motif. (x, y) is its left-centre."""
    if a <= 0 or k <= 0:
        return
    w = text_width(s, 20, 600, 'mono', 0.1) + 58
    h = 44
    with xform(c, x, y, 0.85 + 0.15 * k, rot):
        with layer(c, a * clamp(k * 1.5)):
            pth = skia.Path()
            pth.moveTo(14, -h / 2)
            pth.lineTo(w, -h / 2)
            pth.lineTo(w, h / 2)
            pth.lineTo(14, h / 2)
            pth.lineTo(0, h / 2 - 12)
            pth.lineTo(0, -h / 2 + 12)
            pth.close()
            c.drawPath(pth, paint('#d9c08a', 0.95))
            circle(c, 16, 0, 5, fill='bg0')
            text(c, s, 32, 7, 20, 600, '#2a1f0c', 1, kind='mono', tracking=0.1)

def hbar(c, x, y, w, v, vmax, color, a=1.0, prog=1.0, h=30, v0=0.0):
    """A horizontal bar from v0 to v on a 0..vmax scale of width w. Returns the end x."""
    x0 = x + v0 / vmax * w
    x1 = x + (v0 + (v - v0) * prog) / vmax * w
    if a > 0 and prog > 0:
        rrect(c, x0, y - h / 2, max(x1 - x0, 3), h, 5, fill=color, fa=a * 0.85)
    return x1

def marker(c, x, y, h, color, a=1.0, label=None, size=17):
    """A vertical tick (an optimum, a reference) with a label above."""
    if a <= 0:
        return
    line(c, x, y - h / 2 - 6, x, y + h / 2 + 6, color, a, 4, cap='butt', glow=4)
    if label:
        text(c, label, x, y - h / 2 - 14, size, 600, color, a, 'center', kind='mono')

# ---------------------------------------------------------------- small pictures
def satellite(c, x, y, s=1.0, a=1.0, rot=0, color='ink'):
    """A satellite icon: body and two panels (illustration)."""
    if a <= 0:
        return
    with xform(c, x, y, s, rot):
        rrect(c, -14, -11, 28, 22, 4, fill='panel2', stroke=color, sw=2, a=a)
        for sx in (-1, 1):
            x0 = 18 if sx > 0 else -58
            rrect(c, x0, -8, 40, 16, 2, fill='g', fa=a * 0.55, stroke='g', sw=1.4, a=a)
            line(c, sx * 14, 0, sx * 18, 0, color, a, 2)

def thermometer(c, x, y, s=1.0, a=1.0, fill=0.6, color='c'):
    if a <= 0:
        return
    with xform(c, x, y, s):
        rrect(c, -9, -70, 18, 80, 9, fill='panel2', stroke='ink', sw=2, a=a)
        circle(c, 0, 22, 16, fill=color, stroke='ink', sw=2, a=a)
        rrect(c, -4, -62 + 70 * (1 - fill), 8, 70 * fill + 8, 4, fill=color, a=a)

def gauss(c, x0, x1, y, mu, sd, color, a=1.0, hpx=110, xmin=18.0, xmax=24.0, fa=0.25, prog=1.0):
    """A bell curve on a number line from xmin..xmax mapped to x0..x1 (illustration)."""
    if a <= 0 or prog <= 0:
        return
    xs = np.linspace(xmin, xmax, 240)
    ys = np.exp(-0.5 * ((xs - mu) / sd) ** 2)
    X = x0 + (xs - xmin) / (xmax - xmin) * (x1 - x0)
    Y = y - ys * hpx * prog
    pth = skia.Path()
    pth.moveTo(X[0], y)
    for xx, yy in zip(X, Y):
        pth.lineTo(xx, yy)
    pth.lineTo(X[-1], y)
    pth.close()
    c.drawPath(pth, paint(color, a * fa))
    draw_poly(c, np.stack([X, Y], 1), color, a, 3)

def question_cards(c, t, qs, y0=300, dy=176, h=148, size=33):
    """Numbered questions. qs: [(rich text, start time)]."""
    for i, (q, ti) in enumerate(qs):
        k = ramp(t, ti, 0.9, e_expo)
        if k <= 0:
            continue
        yy = y0 + i * dy
        with layer(c, k):
            with xform(c, 0, (1 - k) * 30):
                panel(c, MX, yy, W - 2 * MX, h)
                line(c, MX + 36, yy + 1, MX + 156, yy + 1, 'y', 1, 4, cap='butt')
                text(c, f'{i + 1}', MX + 50, yy + h * 0.66, 64, 300, 'y', 1, kind='italic')
                rich(c, q, MX + 140, yy + h * 0.44, size, W - 2 * MX - 200, t, ti + 0.3, 0.025, 0.45)

# ---------------------------------------------------------------- title and end cards
class TitleCard(Scene):
    """Title over a faint crop of the memory channels (Fig. S3a), with the case-file kicker."""
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        x0 = MX + 40
        with layer(c, 0.3 * ramp(t, 0.0, 1.2)):
            figcard(c, 'figS3', 1240, 80, 600, 1, src=(0.0, 0.02, 1.0, 0.50), card=False)
        kicker(c, 'a case file  ·  an explainer of arxiv:2611.18393', x0, 330, ramp(t, 0.2, 0.8), 'muted', 18)
        k = ramp(t, 0.1, 1.0, e_expo)
        with layer(c, k):
            yy = 500 + (1 - k) * 40
            w1 = text(c, 'What did it learn to ', x0, yy, 104, 700, 'ink', 1, tracking=-0.01)
            w2 = text(c, 'trust?', x0 + w1, yy, 104, 400, 'y', 1, kind='italic')
            swash(c, x0 + w1 - 4, x0 + w1 + w2 + 6, yy + 24, 'y', 1, ramp(t, 0.8, 0.9, e_io), w=4)
        text(c, 'Inside WeatherDreamer, a weather model learned from raw observations', x0, 600, 34, 400, 'ink',
             ramp(t, 1.2, 0.7), kind='italic')
        text(c, AUTHORS, x0, 690, 25, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, AFFIL, x0, 740, ramp(t, 2.6, 0.8), 'muted', 17)
        exhibit(c, x0 + 4, 830, 'case: the striped memory', ramp(t, 3.0, 0.6), ramp(t, 3.0, 0.6, e_back))

class EndCard(Scene):
    """Takeaway + citation. Subclasses set TAKE (rich text), STATS [(big, small, colour)].
    Keep hold >= 2.0 on the last narration line (house rule: picture and music fade out)."""
    dur = 14.0
    fade_out = 1.8
    cues = [(0.2, 'chime'), (12.5, 'outro')]
    TAKE, STATS, NEXT = '', [], 'an unofficial explainer, not made by the authors'

    def draw(self, c, t):
        kicker(c, 'the verdict', W / 2, 210, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, self.TAKE, W / 2, 290, 46, 1560, t, 0.6, 0.05, 0.6, 1, 'center', base_w=600, lh=1.25)
        n = max(1, len(self.STATS))
        step = min(560, (W - 2 * MX - 80) / n)
        for i, (big, small, colr) in enumerate(self.STATS):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * step, 560, big, small, colr, k, 60)
        k2 = ramp(t, 4.0, 0.9)
        with layer(c, k2):
            line(c, MX, 690, W - MX, 690, 'line', 1, 1.5)
            rich(c, CITE, MX, 745, 23, W - 2 * MX, base_w=600)
            text(c, ARXIV, MX, 830, 22, 500, 'g', 1, kind='mono')
            if self.NEXT:
                kicker(c, self.NEXT, MX, 880, 1, 'muted', 17)
