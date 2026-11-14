"""epikit: shared drawing pieces for the epiplexity topic ("From Entropy to Epiplexity", Finzi, Qiu, Jiang, Izmailov,
Kolter & Wilson, arXiv:2601.03220v2). Hosted by projects/epiplexity/videos/epiplexity; other pieces list
SOURCES = ['epiplexity/videos/epiplexity'] and `from epikit import *`.

Data
  tdata('fig3_eca.json')          the TOPIC's data/ (projects/epiplexity/data/: the paper's figures, extracted by
                                  extract_paper.py, and our lab runs ours_*.json); falls back to the project's own data/.
  FIG3_COLORS, RULE_COLORS        rule 15 / 30 / 54 in Fig. 3's hues (lightened for the dark ground), 110 and coin ours.

Labels (always put one on a chart or a drawing; house rule)
  tag(c, OURS | ILLUS | EXACT | CHECK | 'any text', x, y, a, align)   lowercase mono; OURS is amber, the rest muted
  src(c, 'Fig. 3', x, y, a, align)                                     'data: Fig. 3 · arXiv:2601.03220'
  hdr(scene, c, t, '02', 'kicker', 'Title with one *word*', sub=None)  section header; subclasses renumber with NUM

Cellular automata (exact, computed from the rule; label EXACT)
  eca(rule, width, steps, init='random'|'single'|array, seed)  -> (steps, width) uint8, periodic boundary
  eca_image(grid, color, cell, gap, bg_a)                      -> cached skia image (one pixel block per cell)
  draw_eca(c, grid, x, y, w, t=1e9, t0=0, rows_per_s=None, color='y', a=1, gap=0.18)
                                                               grows row by row from t0 (all rows if rows_per_s is None)
  rule_icons(c, rule, x, y, cell, a, t, t0, color, show_bits)  Wolfram's 8 neighbourhoods -> new cell (the rule as a table)
  bits_row(c, bits, x, y, cell, a, color, t, t0, stagger)      a row of 0/1 cells (strings, seeds, outputs)

The information bar (the topic's motif): structure S_T (amber, solid) | randomness H_T (blue, static noise)
  info_bar(c, x, y, s_w, h_w, h=44, a=1, labels=True, fs=18, prog=1, s_lab=..., h_lab=...)
  S_COL, H_COL                                                 'y' and 'g'

Learning curves
  LogAxes(x, y, w, h, xr=(lo_exp, hi_exp), yr=(lo, hi), ylog=False)   .px(xv, yv), .pts(xs, ys), .draw(c, a, ...)
  LinAxes = kit.Axes
  loss_curve(c, ax, xs, ys, color, t, t0, dur, final=None, area=True, fa=0.22, w=3, a=1)
                                                               draws a curve and shades the area above its final value
  curve_reveal(c, ax, xs, ys, color, t, t0, dur, w=3, a=1, dots=False, r=5)   a polyline drawn on left to right

The observer
  observer(c, x, y, s=1, a=1, dial=0.5, t=0, label='compute  T')    an eye with a compute dial beneath it

Other pictures
  life_step(g), life_run(g, n), rle(s), GOSPER, GLIDER        Conway's Game of Life, exact (wrap-around board)
  draw_cells(c, g, x, y, cell, color, a, gap)                 any 0/1 grid as rounded cells
  chessboard(c, x, y, size, a, t, t0, pieces, arrows)          an illustration board (Apple Symbols glyphs if present)
  code_card(c, x, y, w, lines, a, fs, title)                    a monospace snippet card (Fig. 1's examples)
  stamp(c, s, x, y, color, a, k, rot)                          a verdict stamped onto the frame
  sci(v, nd) -> '5.4 × 10⁶';  decade(e) -> '10¹⁴'

Scenes
  TitleCard, EndCard, question_cards(c, t, qs, ...): same contract as the other topics' kits (see their docstrings).

Every helper animates from (t, t0) so narrated time-warps work. Numbers typed here cite the paper's section or figure.
"""
import functools, json, math, os
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash, hand_arrow

HERE = os.path.dirname(os.path.abspath(__file__))
TOPIC_DATA = os.path.normpath(os.path.join(HERE, '..', '..', 'data'))

PAPER_TITLE = 'From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence'
AUTHORS = 'Marc Finzi*  ·  Shikai Qiu*  ·  Yiding Jiang*  ·  Pavel Izmailov  ·  J. Zico Kolter  ·  Andrew Gordon Wilson'
AFFIL = 'carnegie mellon  ·  nyu  ·  *equal contribution  ·  arxiv:2601.03220'
CITE = 'Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson.  From Entropy to Epiplexity.  arXiv:2601.03220v2, 2026.'
ARXIV = 'arxiv.org/abs/2601.03220'
CODE = 'github.com/shikaiqiu/epiplexity'
HUD = 'epiplexity  ·  an explainer'

OURS, ILLUS, EXACT, CHECK = 'our run', 'illustration', 'computed from the rule', 'our check'
S_COL, H_COL = 'y', 'g'
# Fig. 3's rule colours (matplotlib green / red / purple), lightened a little to read on the dark ground.
FIG3_COLORS = {'15': '#4fc25e', '30': '#e5534b', '54': '#b08ee0'}
RULE_COLORS = dict(FIG3_COLORS, **{'110': '#f0a35a', 'coin': '#9a97a6'})
# Fig. 4c / Fig. 7 (forward green, reverse purple) and Fig. 6 (non-looped purple, looped orange), lightened likewise.
ORDER_COLORS = {'forward': '#4fc25e', 'reverse': '#b08ee0'}
LOOP_COLORS = {'non-looped': '#b06fd8', 'looped': '#f89540'}

SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

def sci(v, nd=1):
    """5.41e6 -> '5.4 × 10⁶'."""
    if v == 0:
        return '0'
    e = int(math.floor(math.log10(abs(v))))
    m = v / 10 ** e
    return f'{m:.{nd}f} × 10{str(e).translate(SUP)}'

def decade(e):
    return f'10{str(int(e)).translate(SUP)}'

# ---------------------------------------------------------------- data
@functools.lru_cache(maxsize=64)
def _read(path):
    return json.load(open(path))

def tdata(name):
    """A JSON file from the topic's data/ folder (projects/epiplexity/data), else from the project's own data/."""
    p = os.path.join(TOPIC_DATA, name)
    if os.path.exists(p):
        return _read(p)
    return load_json(name)

# ---------------------------------------------------------------- labels and headers
def tag(c, s, x, y, a=1.0, align='left', size=16):
    """A source/kind label. OURS ('our run') is amber so our own experiments are never mistaken for the paper's."""
    colr = 'y' if s.startswith(OURS) or s.startswith(CHECK) else 'muted'
    note(c, s, x, y, a * (1.0 if colr == 'y' else 0.9), size, colr, align)

def src(c, fig, x, y, a=1.0, align='left', size=16, extra=''):
    """'data: Fig. 3 · arXiv:2601.03220' (+ extra)."""
    s = f'data: {fig}  ·  arXiv:2601.03220' + (f'  ·  {extra}' if extra else '')
    note(c, s, x, y, a * 0.9, size, 'muted', align)

def hdr(scene, c, t, num, kick, title, sub=None, **kw):
    header(c, t, getattr(scene, 'NUM', num), kick, title, sub=sub, **kw)

def stamp(c, s, x, y, color='r', a=1.0, k=1.0, rot=-6, size=34, align='center'):
    """A verdict stamped on: a rounded box that lands with a little overshoot (k: 0..1 from ramp(.., e_back))."""
    if a <= 0 or k <= 0:
        return
    w = text_width(s, size, 600, 'mono', 0.06) + 44
    h = size + 30
    sc = 1.0 + 0.6 * (1 - k)
    with xform(c, x, y, sc, rot):
        x0 = -w / 2 if align == 'center' else 0
        with layer(c, a * clamp(k * 1.4)):
            rrect(c, x0, -h / 2, w, h, 10, fill='panel', fa=0.94)
            rrect(c, x0, -h / 2, w, h, 10, fill=color, fa=0.12)
            rrect(c, x0, -h / 2, w, h, 10, stroke=color, sw=3)
            text(c, s, x0 + 22, size * 0.36, size, 600, color, 1, kind='mono', tracking=0.06)

# ---------------------------------------------------------------- elementary cellular automata (exact)
def eca(rule, width, steps, init='random', seed=0):
    """Rows of an elementary cellular automaton: cell' = bit (4*left + 2*cell + right) of `rule` (Wolfram's numbering),
    periodic boundary. init: 'random' (fair coin per cell, seeded), 'single' (one live cell in the middle) or an array."""
    if isinstance(init, str):
        if init == 'single':
            x = np.zeros(width, np.uint8); x[width // 2] = 1
        else:
            x = np.random.default_rng(seed).integers(0, 2, width, dtype=np.uint8)
    else:
        x = np.asarray(init, np.uint8)
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    rows = [x]
    for _ in range(steps - 1):
        x = table[(np.roll(x, 1) << 2) | (x << 1) | np.roll(x, -1)]
        rows.append(x)
    return np.array(rows)

_img_cache = {}

def eca_image(grid, color='y', cell=6, gap=0.18, bg_a=0.10):
    """A skia image of a 0/1 grid, `cell` pixels per cell with a dark gap: live cells in `color`, dead ones faintly."""
    key = (grid.tobytes(), grid.shape, color, cell, gap, bg_a)
    if key in _img_cache:
        return _img_cache[key]
    r, g_, b = hexrgb(PAL.get(color, color))
    br, bg, bb = hexrgb(PAL['faint'])
    rows, cols = grid.shape
    gp = max(0, int(round(cell * gap)))
    img = np.zeros((rows * cell, cols * cell, 4), np.uint8)
    block = np.zeros((cell, cell), bool)
    block[:cell - gp, :cell - gp] = True
    on = np.kron(grid.astype(bool), block)
    off = np.kron(~grid.astype(bool), block)
    img[on] = (r, g_, b, 255)
    img[off] = (br, bg, bb, int(255 * bg_a))
    im = skia.Image.fromarray(np.ascontiguousarray(img), colorType=skia.kRGBA_8888_ColorType)
    _img_cache[key] = im
    return im

def draw_eca(c, grid, x, y, w, t=1e9, t0=0.0, rows_per_s=None, color='y', a=1.0, gap=0.18, bg_a=0.10, glow=0, frame=True):
    """Draw a spacetime diagram (time flows down) w pixels wide. With rows_per_s, rows appear one by one from t0,
    the newest row flashing bright. Returns the drawn height."""
    if a <= 0:
        return 0
    rows, cols = grid.shape
    cpx = w / cols
    cell = max(2, int(round(cpx * 2)))            # supersample so cells stay crisp when scaled
    im = eca_image(grid, color, cell, gap, bg_a)
    hgt = rows * cpx
    shown = rows if rows_per_s is None else clamp((t - t0) * rows_per_s, 0, rows)
    if shown <= 0:
        return hgt
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x - 2, y - 2, w + 4, shown * cpx + 2))
    if glow:
        gp = skia.Paint(AntiAlias=True); gp.setAlphaf(a * 0.35); gp.setImageFilter(skia.ImageFilters.Blur(glow, glow))
        c.drawImageRect(im, skia.Rect.MakeXYWH(x, y, w, hgt), skia.SamplingOptions(skia.FilterMode.kLinear), gp)
    p = skia.Paint(AntiAlias=True); p.setAlphaf(a)
    c.drawImageRect(im, skia.Rect.MakeXYWH(x, y, w, hgt), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()
    if rows_per_s is not None and 0 < shown < rows:            # the row being computed, flashing
        i = int(shown)
        rr = grid[i]
        for j in np.nonzero(rr)[0]:
            rrect(c, x + j * cpx, y + i * cpx, cpx * (1 - gap), cpx * (1 - gap), cpx * 0.2, fill='ink', fa=a * 0.85)
    if frame:
        rrect(c, x - 6, y - 6, w + 12, min(hgt, shown * cpx) + 12, 6, stroke='line', sw=1.2, a=a * 0.8)
    return hgt

def rule_icons(c, rule, x, y, cell=22, a=1.0, t=1e9, t0=0.0, color='y', show_bits=True, gap=14, stagger=0.12):
    """Wolfram's picture of a rule: the 8 neighbourhoods (111 ... 000) with the new middle cell beneath each.
    Returns the total width."""
    total = 8 * 3 * cell + 7 * gap
    for k, idx in enumerate(range(7, -1, -1)):
        kk = ramp(t, t0 + k * stagger, 0.4) * a
        if kk <= 0:
            continue
        bits = [(idx >> 2) & 1, (idx >> 1) & 1, idx & 1]
        out = (rule >> idx) & 1
        bx = x + k * (3 * cell + gap)
        for j, b in enumerate(bits):
            rrect(c, bx + j * cell, y, cell - 2, cell - 2, 3, fill=color if b else 'faint', fa=kk * (1 if b else 0.5))
        rrect(c, bx + cell, y + cell + 6, cell - 2, cell - 2, 3, fill=color if out else 'faint', fa=kk * (1 if out else 0.5))
        rrect(c, bx + cell - 3, y + cell + 3, cell + 4, cell + 4, 4, stroke='ink', sw=1.3, a=kk * 0.6)
        if show_bits:
            text(c, str(out), bx + cell * 1.5 - 1, y + 2 * cell + 34, 18, 500, color if out else 'muted', kk, 'center', kind='mono')
    return total

def bits_row(c, bits, x, y, cell=18, a=1.0, color='y', t=1e9, t0=0.0, stagger=0.0, gap=0.2, off_a=0.45):
    """A row of 0/1 cells, optionally appearing one by one."""
    for j, b in enumerate(bits):
        k = ramp(t, t0 + j * stagger, 0.25) * a if stagger else a
        if k <= 0:
            continue
        rrect(c, x + j * cell, y, cell * (1 - gap), cell * (1 - gap), cell * 0.2,
              fill=color if b else 'faint', fa=k * (1 if b else off_a))

def fade_edge(c, x0, x1, y0, y1, top=None):
    """Inside a layer: fade what is already drawn to transparent on the left (alpha 0 at x0 -> 1 at x1); with
    top=(ya, yb) also fade it out at the top. Leaves the background untouched."""
    p = skia.Paint()
    p.setBlendMode(skia.BlendMode.kDstIn)
    p.setShader(skia.GradientShader.MakeLinear([(x0, 0), (x1, 0)], [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 255)]))
    c.drawRect(skia.Rect.MakeXYWH(x0 - 4000, y0, x1 - x0 + 8000, y1 - y0), p)

def bar_legend(c, x, y, a=1.0, fs=17):
    """'structure (epiplexity)' and 'randomness (time-bounded entropy)' swatches for the info bar."""
    if a <= 0:
        return
    info_bar(c, x, y - 15, 44, 0, 18, a, labels=False)
    w = text(c, 'structure · epiplexity', x + 56, y, fs, 500, S_COL, a, kind='mono')
    info_bar(c, x + 56 + w + 40, y - 15, 0, 44, 18, a, labels=False)
    text(c, 'randomness · time-bounded entropy', x + 56 + w + 40 + 56, y, fs, 500, H_COL, a, kind='mono')

# ---------------------------------------------------------------- the information bar
_noise = {}

def _noise_img():
    if 'img' not in _noise:
        rng = np.random.default_rng(3)
        n = rng.random((60, 600)) < 0.5
        r, g_, b = hexrgb(PAL[H_COL])
        img = np.zeros((60, 600, 4), np.uint8)
        img[n] = (r, g_, b, 255)
        img[~n] = (int(r * 0.45), int(g_ * 0.45), int(b * 0.45), 255)
        _noise['img'] = skia.Image.fromarray(np.ascontiguousarray(img), colorType=skia.kRGBA_8888_ColorType)
    return _noise['img']

def info_bar(c, x, y, s_w, h_w, h=44, a=1.0, labels=True, fs=18, prog=1.0, s_lab='structure', h_lab='randomness',
             vals=None, min_w=3):
    """One object's information as a bar: structure (epiplexity, S_T: solid amber with fine stripes) then randomness
    (time-bounded entropy, H_T: blue static). s_w, h_w in pixels; prog grows the bar from the left.
    vals=(s_text, h_text) prints values inside/after the segments."""
    if a <= 0 or prog <= 0:
        return
    s_w, h_w = s_w * prog, h_w * prog
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, max(s_w + h_w, min_w), h), 8, 8)
    c.save()
    c.clipRRect(rr, skia.ClipOp.kIntersect, True)
    if s_w > 0:
        rrect(c, x, y, max(s_w, min_w), h, 0, fill=S_COL, fa=a * 0.95)
        for k in range(int(s_w // 14) + 2):                    # fine diagonal stripes: an orderly texture
            xx = x + k * 14
            line(c, xx, y + h, xx + h * 0.6, y, '#000000', a * 0.13, 3, cap='butt')
    if h_w > 0:
        p = skia.Paint(AntiAlias=False); p.setAlphaf(a)
        c.drawImageRect(_noise_img(), skia.Rect.MakeXYWH(0, 0, max(1, h_w / 4), h / 4),
                        skia.Rect.MakeXYWH(x + s_w, y, h_w, h), skia.SamplingOptions(skia.FilterMode.kNearest), p)
    c.restore()
    c.drawRRect(rr, paint('ink', a * 0.35, stroke=1.2))
    if labels:
        if s_lab:
            text(c, s_lab, x, y - 12, fs, 500, S_COL, a * clamp(prog * 2), kind='mono')
        if h_lab and h_w > 30:
            text(c, h_lab, x + s_w + h_w, y - 12, fs, 500, H_COL, a * clamp(prog * 2), 'right', kind='mono')
    if vals:
        sv, hv = vals
        if sv:
            text(c, sv, x + s_w + 10 if s_w < 120 else x + 12, y + h / 2 + fs * 0.36, fs, 600,
                 'ink' if s_w < 120 else '#1a1206', a, kind='mono')
        if hv:
            text(c, hv, x + s_w + h_w + 12, y + h / 2 + fs * 0.36, fs, 600, H_COL, a, kind='mono')

# ---------------------------------------------------------------- charts
class LogAxes:
    """Axes with a log10 x axis (exponents xr=(lo, hi)) and a linear or log10 y axis. px/pts take raw values."""
    def __init__(self, x, y, w, h, xr, yr, ylog=False):
        self.x, self.y, self.w, self.h, self.xr, self.yr, self.ylog = x, y, w, h, xr, yr, ylog

    def px(self, xv, yv):
        lx = np.log10(np.maximum(np.asarray(xv, float), 1e-300))
        X = self.x + (lx - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w
        yv = np.asarray(yv, float)
        ly = np.log10(np.maximum(yv, 1e-300)) if self.ylog else yv
        Y = self.y + self.h - (ly - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h
        return X, Y

    def pts(self, xs, ys):
        X, Y = self.px(xs, ys)
        return np.stack([X, Y], 1)

    def draw(self, c, a, xdecades=None, yticks=(), yfmt=None, xlabel=None, ylabel=None, fs=19, prog=1.0, grid=True):
        if a <= 0:
            return
        xdecades = xdecades if xdecades is not None else range(int(math.ceil(self.xr[0])), int(self.xr[1]) + 1)
        x0, y0, w, h = self.x, self.y, self.w, self.h
        for yv in yticks:
            _, Y = self.px(10 ** self.xr[0], yv)
            if grid:
                line(c, x0, Y, x0 + w * prog, Y, 'line', a * 0.7, 1)
            s = yfmt(yv) if yfmt else (decade(math.log10(yv)) if self.ylog else f'{yv:g}')
            text(c, s, x0 - 12, Y + fs * 0.35, fs, 500, 'muted', a * prog, 'right', kind='mono')
        for e in xdecades:
            X = x0 + (e - self.xr[0]) / (self.xr[1] - self.xr[0]) * w
            if grid:
                line(c, X, y0 + h, X, y0 + h - h * prog, 'line', a * 0.7, 1)
            text(c, decade(e), X, y0 + h + fs + 12, fs, 500, 'muted', a * prog, 'center')
        line(c, x0, y0 + h, x0 + w * prog, y0 + h, 'muted', a, 1.6)
        line(c, x0, y0 + h, x0, y0 + h * (1 - prog), 'muted', a, 1.6)
        if xlabel:
            text(c, xlabel, x0 + w, y0 + h + fs * 2 + 26, fs, 500, 'muted', a * prog, 'right', kind='mono')
        if ylabel:
            text(c, ylabel, x0, y0 - 18, fs, 500, 'muted', a * prog, kind='mono')

LinAxes = Axes

def curve_reveal(c, ax, xs, ys, color, t, t0, dur, w=3, a=1.0, dots=False, r=5, glow=0, dash=None):
    """A data polyline drawn on from left to right between t0 and t0 + dur; dots marks the data points."""
    k = ramp(t, t0, dur, e_io)
    if k <= 0 or a <= 0:
        return
    pts = ax.pts(xs, ys)
    draw_poly(c, pts, color, a, w, prog=k, glow=glow, dash=dash)
    if dots:
        n = len(pts)
        for i, p in enumerate(pts):
            if i / max(n - 1, 1) <= k + 1e-6:
                circle(c, p[0], p[1], r, fill=color, stroke='#111111', sw=1.4, a=a)

def loss_curve(c, ax, xs, ys, color, t, t0, dur, final=None, area=True, fa=0.22, w=3, a=1.0, area_color=None):
    """A loss curve drawn on over [t0, t0+dur], with the area above its final value shaded as it goes (the
    prequential picture: structure absorbed = area under the curve above the final loss). final defaults to the
    mean of the last 5% of ys. Returns final."""
    xs, ys = np.asarray(xs, float), np.asarray(ys, float)
    if final is None:
        k = max(3, len(ys) // 20)
        final = float(np.mean(ys[-k:]))
    pr = ramp(t, t0, dur, e_io)
    if pr <= 0 or a <= 0:
        return final
    n = max(2, int(len(xs) * pr))
    pts = ax.pts(xs[:n], ys[:n])
    if area:
        _, Yf = ax.px(xs[0], final)
        pth = skia.Path()
        pth.moveTo(pts[0][0], Yf)
        for p in pts:
            pth.lineTo(p[0], min(p[1], Yf))
        pth.lineTo(pts[-1][0], Yf)
        pth.close()
        c.drawPath(pth, paint(area_color or color, a * fa))
    draw_poly(c, pts, color, a, w)
    return final

# ---------------------------------------------------------------- the observer
def observer(c, x, y, s=1.0, a=1.0, dial=0.5, t=0.0, label='compute  T', color='y'):
    """An eye (the observer) above a gauge whose needle shows its compute budget T (dial 0..1)."""
    if a <= 0:
        return
    with xform(c, x, y, s):
        # eye
        pth = skia.Path()
        pth.moveTo(-70, 0)
        pth.quadTo(0, -62, 70, 0)
        pth.quadTo(0, 62, -70, 0)
        pth.close()
        c.drawPath(pth, paint('panel2', a * 0.9))
        c.drawPath(pth, paint('pencil', a * 0.9, stroke=3))
        blink = 1.0
        circle(c, 0, 0, 24, fill=color, a=a * 0.95, glow=10 + 8 * dial)
        circle(c, 0, 0, 10, fill='#120d06', a=a)
        circle(c, 7, -7, 4, fill='ink', a=a * 0.8)
        # gauge
        gy = 110
        arc = skia.Path()
        arc.addArc(skia.Rect.MakeXYWH(-62, gy - 62, 124, 124), 180, 180)
        c.drawPath(arc, paint('faint', a, stroke=8, cap='round'))
        prog = skia.Path()
        prog.addArc(skia.Rect.MakeXYWH(-62, gy - 62, 124, 124), 180, 180 * clamp(dial))
        c.drawPath(prog, paint(color, a, stroke=8, cap='round'))
        ang = math.pi * (1 - clamp(dial))
        line(c, 0, gy, 50 * math.cos(ang), gy - 50 * math.sin(ang), 'ink', a, 3)
        circle(c, 0, gy, 6, fill='ink', a=a)
        if label:
            text(c, label, 0, gy + 40, 18, 500, 'muted', a, 'center', kind='mono', tracking=0.08)

# ---------------------------------------------------------------- Game of Life (exact)
def life_step(g):
    """One step of Conway's Game of Life on a wrap-around board (born with 3 neighbours, survives with 2 or 3)."""
    n = sum(np.roll(np.roll(g, dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))
    return ((n == 3) | ((g == 1) & (n == 2))).astype(np.uint8)

def life_run(g, n):
    out = [g]
    for _ in range(n - 1):
        g = life_step(g)
        out.append(g)
    return out

def rle(s):
    """Decode a Life RLE pattern body ('bo$2bo$3o!') into a 0/1 array."""
    rows, row, num = [], [], ''
    for ch in s:
        if ch.isdigit():
            num += ch
            continue
        k = int(num) if num else 1
        num = ''
        if ch in 'bo':
            row += [1 if ch == 'o' else 0] * k
        elif ch == '$':
            rows.append(row); row = []
            rows += [[]] * (k - 1)
        elif ch == '!':
            break
    rows.append(row)
    w = max(len(r) for r in rows)
    return np.array([r + [0] * (w - len(r)) for r in rows], np.uint8)

GLIDER = rle('bo$2bo$3o!')
GOSPER = rle('24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!')

def place(board, pat, r, c_):
    b = board.copy()
    b[r:r + pat.shape[0], c_:c_ + pat.shape[1]] = pat
    return b

def draw_cells(c, g, x, y, cell, color='y', a=1.0, gap=0.16, off_a=0.0, glow=0):
    """A 0/1 grid as rounded cells (fine for boards up to a few thousand cells; use draw_eca's image for more)."""
    if a <= 0:
        return
    if off_a > 0:
        rrect(c, x, y, g.shape[1] * cell, g.shape[0] * cell, 4, fill='faint', fa=a * off_a)
    p = paint(color, a)
    if glow:
        gp = paint(color, a * 0.4, blur=glow)
    ys, xs = np.nonzero(g)
    s = cell * (1 - gap)
    for i, j in zip(ys, xs):
        r = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + j * cell, y + i * cell, s, s), s * 0.22, s * 0.22)
        if glow:
            c.drawRRect(r, gp)
        c.drawRRect(r, p)

# ---------------------------------------------------------------- chess (illustration)
_SYM = '/System/Library/Fonts/Apple Symbols.ttf'
_sym_font = {}

def _chess_font(size):
    if size not in _sym_font:
        tf = skia.Typeface.MakeFromFile(_SYM) if os.path.exists(_SYM) else None
        _sym_font[size] = skia.Font(tf, size) if tf else None
    return _sym_font[size]

START = {'a8': '♜', 'b8': '♞', 'c8': '♝', 'd8': '♛', 'e8': '♚', 'f8': '♝', 'g8': '♞', 'h8': '♜',
         'a1': '♜', 'b1': '♞', 'c1': '♝', 'd1': '♛', 'e1': '♚', 'f1': '♝', 'g1': '♞', 'h1': '♜'}
START.update({f'{f}7': '♟' for f in 'abcdefgh'})
START.update({f'{f}2': '♟' for f in 'abcdefgh'})

def sq(name, x, y, size):
    """Centre of a square ('e4') on a board drawn at (x, y) with side `size` (white at the bottom)."""
    f, r = ord(name[0]) - 97, int(name[1]) - 1
    s = size / 8
    return x + (f + 0.5) * s, y + (7 - r + 0.5) * s

def chessboard(c, x, y, size, a=1.0, pieces=None, arrows=(), light='#2b2c42', dark='#1f2033'):
    """An illustration board. pieces: {square: glyph} (the solid glyph set; white pieces are those on ranks given in
    `white`: by convention any square whose piece string starts with 'w:' is white, e.g. 'w:♚'). arrows: [(from, to,
    colour, progress)]."""
    if a <= 0:
        return
    s = size / 8
    for i in range(8):
        for j in range(8):
            rrect(c, x + j * s, y + i * s, s, s, 0, fill=light if (i + j) % 2 == 0 else dark, fa=a)
    rrect(c, x, y, size, size, 4, stroke='line', sw=2, a=a)
    f = _chess_font(int(s * 0.78))
    for name, g in (pieces or {}).items():
        white = g.startswith('w:')
        g = g[2:] if white else g
        cx, cy = sq(name, x, y, size)
        colr = 'ink' if white else '#0b0b12'
        if f is not None:
            w = f.measureText(g)
            if not white:      # dark pieces get a light rim so they read on dark squares
                c.drawString(g, cx - w / 2, cy + s * 0.28, f, paint('pencil', a * 0.9, stroke=2.2))
            c.drawString(g, cx - w / 2, cy + s * 0.28, f, paint(colr, a))
        else:
            circle(c, cx, cy, s * 0.3, fill=colr, stroke='pencil', sw=2, a=a)
    for (fr, to, colr, pr) in arrows:
        x0, y0 = sq(fr, x, y, size)
        x1, y1 = sq(to, x, y, size)
        arrow(c, x0, y0, x1, y1, colr, a * 0.9, 5, 16, prog=pr, glow=6)

# ---------------------------------------------------------------- cards
def code_card(c, x, y, w, lines, a=1.0, fs=19, title=None, h=None, lh=1.45, color='ink'):
    """A monospace snippet on a panel (Fig. 1's examples). Returns the card height."""
    if a <= 0:
        return 0
    hh = h or (len(lines) * fs * lh + 40 + (34 if title else 0))
    panel(c, x, y, w, hh, a, r=12, fill='#141522', fa=0.92)
    yy = y + 32
    if title:
        text(c, title, x + 20, yy, 15, 500, 'muted', a, kind='mono', tracking=0.08)
        yy += 34
    for ln in lines:
        text(c, ln, x + 20, yy + fs * 0.4, fs, 400, color, a, kind='mono')
        yy += fs * lh
    return hh

def question_cards(c, t, qs, y0=300, dy=168, h=140, size=34):
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
                rich(c, q, MX + 140, yy + h * 0.47, size, W - 2 * MX - 200, t, ti + 0.3, 0.025, 0.45)

# ---------------------------------------------------------------- title and end cards
class TitleCard(Scene):
    """The topic's title card: TITLE ('*word*' amber italic; shrinks to fit), SUBTITLE, AUTHORS, AFFIL, KICKER,
    and a rule 54 spacetime diagram growing behind on the right (computed from the rule). Animation done by ~3.5 s."""
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]
    TITLE = 'From Entropy to *Epiplexity*'
    SUBTITLE = 'Rethinking Information for Computationally Bounded Intelligence'
    KICKER = 'an explainer of arXiv:2601.03220'
    AUTHORS, AFFIL = AUTHORS, AFFIL
    TITLE_SIZE = 118
    RULE = 54

    def __init__(self):
        self.grid = eca(self.RULE, 120, 150, seed=5)

    def draw(self, c, t):
        x0 = MX + 40
        with layer(c, 0.55 * ramp(t, 0.0, 1.0)):
            draw_eca(c, self.grid, 1180, 60, 640, t, 0.0, 60, color='y', bg_a=0.0, frame=False, gap=0.2)
            fade_edge(c, 1180, 1560, 60, H)
        kicker(c, self.KICKER, x0, 330, ramp(t, 0.2, 0.8), 'muted', 18)
        k = ramp(t, 0.1, 1.0, e_expo)
        parts = self.TITLE.split('*')
        size = self.TITLE_SIZE
        tot = sum(text_width(p_, size, 400, 'italic') if i % 2 else text_width(p_, size, 700, tracking=-0.01)
                  for i, p_ in enumerate(parts) if p_)
        size = size * min(1.0, 1500 / max(tot, 1))
        with layer(c, k):
            xx, yy = x0, 500 + (1 - k) * 40
            for i, p_ in enumerate(parts):
                if not p_:
                    continue
                if i % 2:
                    wd = text(c, p_, xx, yy, size, 400, 'y', 1, kind='italic')
                    swash(c, xx - 4, xx + wd + 6, yy + size * 0.22, 'y', 1, ramp(t, 0.8, 0.9, e_io), w=4)
                else:
                    wd = text(c, p_, xx, yy, size, 700, 'ink', 1, tracking=-0.01)
                xx += wd
        text(c, self.SUBTITLE, x0, 600, 36, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, self.AUTHORS, x0, 690, 25, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, self.AFFIL, x0, 740, ramp(t, 2.6, 0.8), 'muted', 17)

class EndCard(Scene):
    """Takeaway + citation + code link. Subclasses set TAKE (rich text), STATS [(big, small, colour)], NEXT (kicker).
    Keep hold >= 2.0 on the last narration line (house rule: picture and music fade out)."""
    dur = 14.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (12.5, 'outro')]
    TAKE, STATS, NEXT = '', [], 'an unofficial explainer, not made by the authors'

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 210, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, self.TAKE, W / 2, 290, 46, 1560, t, 0.6, 0.05, 0.6, 1, 'center', base_w=600, lh=1.25)
        n = max(1, len(self.STATS))
        step = min(560, (W - 2 * MX - 80) / n)
        for i, (big, small, colr) in enumerate(self.STATS):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * step, 560, big, small, colr, k, 60)
        k2 = ramp(t, 4.0, 0.9)
        with layer(c, k2):
            line(c, MX, 690, W - MX, 690, 'line', 1, 1.5)
            text(c, CITE, MX, 745, 24, 600, 'ink')
            text(c, ARXIV + '   ·   code: ' + CODE, MX, 790, 22, 500, 'g', 1, kind='mono')
            if self.NEXT:
                kicker(c, self.NEXT, MX, 850, 1, 'muted', 17)
