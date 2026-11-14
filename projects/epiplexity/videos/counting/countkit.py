"""Drawing pieces for "Who's Counting?" (projects/epiplexity/videos/counting): the four files and the scorecard.

The four files are computed here, not drawn by hand: all zeros; a million fair coin flips (numpy, seed 1, as in
projects/epiplexity/lab/compress_lab.py); SHA-256 in counter mode from the 7-byte (56-bit) seed b'seed:42' (the same
generator our compression check used); and pairs (X, rule 54 applied 48 times to X) on 64 periodic cells (as
lab/check_pairs.py). Shorts can reuse them with SOURCES = ['epiplexity/videos/counting'] and `from countkit import *`.

Scorecard: COLS holds every judge's verdict on the four files. Numeric entries are typed from the source they name
(Shannon and Kolmogorov: arithmetic on the files' construction; the compressor: data/ours_compress*.json, OUR check);
sophistication, the cryptographer's test and epiplexity are qualitative, following the paper (Thm 9, Fig. 3).
"""
import hashlib, math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import swash, hand_arrow

CITE = 'Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson (2026).  From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence.'
ARXIV = 'arxiv.org/abs/2601.03220'
OUR_CHECK, OUR_RUN, ILLUS, FRAMING = 'our check', 'our run', 'illustration', 'our framing'

# the paper's figure colours (Fig. 3: rules 15, 30, 54; Fig. 4a: forward, reverse, entropy)
RULE_COL = {15: '#2ca02c', 30: '#d62728', 54: '#9467bd'}
FIG4_COL = dict(forward='#9a9a2a', reverse='#b061b0', entropy='#9a9a9a')
SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

def sci(v, nd=1):
    e = int(math.floor(math.log10(abs(v))))
    return f'{v / 10 ** e:.{nd}f} × 10{str(e).translate(SUP)}'

def decade(e):
    return f'10{str(e).translate(SUP)}'

# ---------------------------------------------------------------- the four files
N_BITS = 1 << 20
_bits = {}

def eca(x, rule, k, keep=False):
    """k steps of an elementary cellular automaton on rows x (..., n), periodic boundary; keep=True returns all rows."""
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    rows = [x]
    for _ in range(k):
        x = table[(np.roll(x, 1, -1) << 2) | (x << 1) | np.roll(x, -1, -1)]
        rows.append(x)
    return np.stack(rows) if keep else x

def file_bits(key):
    """The first rows of each file as a 2-D 0/1 array (bits laid out row by row)."""
    if key in _bits:
        return _bits[key]
    if key == 'zeros':
        b = np.zeros((128, 128), np.uint8)
    elif key == 'coins':
        b = np.random.default_rng(1).integers(0, 2, 128 * 128, dtype=np.uint8).reshape(128, 128)
    elif key == 'prng':
        out, ctr = bytearray(), 0
        while len(out) * 8 < 128 * 128:
            out += hashlib.sha256(b'seed:42' + ctr.to_bytes(8, 'big')).digest(); ctr += 1
        b = np.unpackbits(np.frombuffer(bytes(out), np.uint8))[:128 * 128].reshape(128, 128)
    elif key == 'ca':           # one pair's full history: 49 rows of 64 cells; the file keeps only rows 0 and 48
        x = np.random.default_rng(3).integers(0, 2, 64, dtype=np.uint8)
        b = eca(x, 54, 48, keep=True)
    elif key == 'ca_pairs':     # the file itself: X | Y per line
        x = np.random.default_rng(3).integers(0, 2, (64, 64), dtype=np.uint8)
        b = np.concatenate([x, eca(x, 54, 48)], 1)
    else:
        raise KeyError(key)
    _bits[key] = b
    return b

_imgs = {}

def bit_image(key, bits, cell=6, gap=1, on='ink', off='panel2', dim_rows=None, dim=0.16, on2=None):
    """A grid image of bits: each bit a `cell`-pixel square with a `gap`; rows in dim_rows are faded."""
    k = (key, cell, gap, on, off, dim, on2, None if dim_rows is None else tuple(dim_rows))
    if k in _imgs:
        return _imgs[k]
    h, w = bits.shape
    on_c, off_c = np.array(hexrgb(PAL.get(on, on)), float), np.array(hexrgb(PAL.get(off, off)), float)
    rgb = np.where(bits[..., None] > 0, on_c, off_c)
    alpha = np.full((h, w), 255.0)
    if dim_rows is not None:
        alpha[list(dim_rows)] = 255 * dim
    big = np.zeros((h * cell, w * cell, 4), np.uint8)
    core = cell - gap
    for dy in range(core):
        for dx in range(core):
            big[dy::cell, dx::cell, :3] = rgb
            big[dy::cell, dx::cell, 3] = alpha
    im = skia.Image.fromarray(np.ascontiguousarray(big), colorType=skia.kRGBA_8888_ColorType)
    _imgs[k] = im
    return im

def draw_grid(c, im, x, y, w, h, a=1.0, reveal=1.0):
    """Draw a bit-grid image into (x, y, w, h), revealed top to bottom."""
    if a <= 0 or reveal <= 0:
        return
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(x - 2, y - 2, w + 4, h * reveal + 2))
    draw_image(c, im, x, y, w, h, a, smooth=False)
    c.restore()

FILES = [('zeros', 'all zeros', '000000…'), ('coins', 'coin flips', 'a fair coin'),
         ('prng', 'pseudorandom', 'SHA-256 · 56-bit seed'), ('ca', 'rule 54 pairs', '64 cells · 48 steps')]

def file_thumb(c, key, x, y, s, a=1.0, reveal=1.0, cell=None):
    """A square-ish picture of one file, s pixels wide. 'ca' shows one pair's history with the 47 unwritten rows faded."""
    if a <= 0:
        return
    if key == 'ca':
        bits = file_bits('ca')
        im = bit_image('ca', bits, cell=cell or 6, gap=1, on='ink', off='panel2', dim_rows=range(1, 48))
        h = s * 49 / 64
        rrect(c, x - 6, y - 6, s + 12, h + 12, 8, fill='panel', a=a, fa=a * 0.9)
        draw_grid(c, im, x, y, s, h, a, reveal)
        return h
    n = 64 if s > 160 else 24
    bits = file_bits(key)[:n, :n]
    im = bit_image(f'{key}{n}', bits, cell=cell or 6, gap=1, on='ink', off='panel2')
    rrect(c, x - 6, y - 6, s + 12, s + 12, 8, fill='panel', a=a, fa=a * 0.9)
    draw_grid(c, im, x, y, s, s, a, reveal)
    return s

# ---------------------------------------------------------------- the scorecard
_zip = {}
def zip_ratio(key, comp='xz'):
    """Compressed bits per bit from OUR checks (data/ours_compress.json, data/ours_compress_pairs.json)."""
    if not _zip:
        a = load_json('ours_compress.json')['results']
        b = load_json('ours_compress_pairs.json')['results']
        _zip.update(zeros=a['zeros'], coins=a['coin'], prng=a['prng'], ca=b['rule54'], ca30=b['rule30'], ca15=b['rule15'])
    return _zip[key][comp]

def _zip_cells():
    def m(v):
        return f'{v:.2f} M' if v > 0.01 else f'{v:.3f} M'
    return [(m(zip_ratio('zeros')), 'vanishes'), (m(zip_ratio('coins')), 'no shrink'),
            (m(zip_ratio('prng')), 'no shrink'), (m(zip_ratio('ca')), 'barely shrinks')]

# cells: (value, small note). best: rows the judge scores highest. tone: per-row colour override.
COLS = [
    dict(judge='Shannon', measure='entropy H', color='g', best=[1],
         cells=[('0', 'nothing to guess'), ('1 M', '1 bit per flip'), ('56', 'only the seed'), ('0.5 M', 'only the starts')]),
    dict(judge='Kolmogorov', measure='shortest program K', color='x', best=[1],
         cells=[('≈ 20', 'print 0, n times'), ('≈ 1 M', 'no shortcut'), ('small', 'seed + generator'), ('≈ 0.5 M', 'starts + rule')]),
    dict(judge='compressor', measure='xz · our check', color='v', best=[1, 2], cells=None),
    dict(judge='sophistication', measure='structure, unbounded', color='f', best=[],
         cells=[('≈ 0', ''), ('≈ 0', ''), ('≈ 0', ''), ('≈ 0', 'rule + random rows')]),
    dict(judge='cryptographer', measure='random to a fast test?', color='c', best=[], verdict=True,
         cells=[('no', ''), ('yes', ''), ('yes', 'without the seed'), ('no', 'partly predictable')]),
    dict(judge='epiplexity', measure='structure  S_T', color='y', best=[3], group='the paper, 2026',
         cells=[('≈ 0', 'tiny model'), ('≈ 0', '“flip a coin”'), ('≈ 0', 'Thm 9'), ('high', 'gliders, collisions')]),
    dict(judge='time-bounded H', measure='random  H_T', color='r', best=[1, 2], group='the paper, 2026',
         cells=[('≈ 0', 'nothing left'), ('1 M', 'all random'), ('≈ 1 M', 'Thm 9'), ('medium', 'starts + some')]),
]

def col_cells(j):
    return COLS[j]['cells'] or _zip_cells()

SC = dict(x=120, label_w=330, right=1800, y0=292, head_h=108, row_h=138)

def _col_x(j):
    cw = (SC['right'] - SC['x'] - SC['label_w']) / len(COLS)
    return SC['x'] + SC['label_w'] + j * cw, cw

def scorecard(c, t, cols_done=(), cols_now=(), times=(0.5, 1.0, 1.5, 2.0), head_t=0.2, win_t=None, a=1.0,
              dim_prev=True, ghosts=True, row_t=None, win_all=None, row_hi=None):
    """The scorecard. cols_done: columns drawn complete; cols_now: columns filling now (header at head_t, row i at
    times[i], the column's best cells light up at win_t). ghosts: later columns as faint empty slots.
    row_t: when the row labels appear (None = already there). win_all: light every column's winners (end card)."""
    if a <= 0:
        return
    x0, y0, hh, rh = SC['x'], SC['y0'], SC['head_h'], SC['row_h']
    kr = a if row_t is None else a * ramp(t, row_t, 0.6)
    # row labels: the file's picture, name and recipe
    for i, (key, name, sub) in enumerate(FILES):
        ky = y0 + hh + i * rh
        k = kr if row_t is None else a * ramp(t, row_t + i * 0.15, 0.6)
        hi = 1.0 if row_hi is None else (1.0 if i == row_hi else 0.45)
        with layer(c, k * hi):
            file_thumb(c, key, x0 + 6, ky + 24 if key != 'ca' else ky + 34, 90, 1, cell=6)
            text(c, name, x0 + 120, ky + 64, 27, 600, 'ink', 1)
            text(c, sub, x0 + 120, ky + 94, 15, 400, 'muted', 1, kind='mono')
    line(c, x0, y0 + hh - 6, SC['right'], y0 + hh - 6, 'line', a, 1.4)
    any_now = len(cols_now) > 0
    for j, col in enumerate(COLS):
        cx, cw = _col_x(j)
        done, now = j in cols_done, j in cols_now
        if not (done or now):
            if ghosts:
                ga = a * 0.55
                rrect(c, cx + 8, y0 + 8, cw - 16, hh - 22 + 4 * rh, 12, stroke='faint', sw=1.2, a=ga)
                text(c, '?', cx + cw / 2, y0 + hh / 2 + 14, 40, 400, 'faint', ga, 'center', kind='italic')
            continue
        ca = a * (0.5 if (done and any_now and dim_prev) else 1.0)
        kh = ca * (1.0 if done else ramp(t, head_t, 0.6, e_expo))
        colr = col['color']
        if col.get('group') and j == 5:
            gx = cx + 8
            gw = 2 * cw - 16
            line(c, gx, y0 - 2, gx + gw, y0 - 2, 'y', kh * 0.8, 2)
            text(c, col['group'], gx + gw / 2, y0 - 12, 15, 400, 'y', kh, 'center', kind='mono', tracking=0.08)
        if kh > 0:
            line(c, cx + 18, y0 + 6, cx + cw - 18, y0 + 6, colr, kh, 3, cap='butt')
            size = 27 if text_width(col['judge'], 27, 400, 'italic') < cw - 16 else 23
            text(c, col['judge'], cx + cw / 2, y0 + 46, size, 400, 'ink', kh, 'center', kind='italic')
            meas = col['measure']
            text(c, meas, cx + cw / 2, y0 + 76, 14, 400, colr, kh, 'center', kind='mono')
        for i, (val, sub) in enumerate(col_cells(j)):
            ky = y0 + hh + i * rh
            kc = ca * (1.0 if done else ramp(t, times[i], 0.55, e_expo))
            if kc <= 0:
                continue
            best = i in col['best']
            wk = 0.0
            if best:
                if win_all is not None:
                    wk = ramp(t, win_all + j * 0.18, 0.6)
                elif done:
                    wk = 1.0
                elif win_t is not None:
                    wk = ramp(t, win_t, 0.6)
            with layer(c, kc):
                with xform(c, 0, (1 - kc) * 14):
                    rrect(c, cx + 10, ky + 8, cw - 20, rh - 16, 12, fill='panel', a=1, fa=0.8)
                    if wk > 0:
                        rrect(c, cx + 10, ky + 8, cw - 20, rh - 16, 12, stroke=colr, sw=2.4, a=wk, glow=0)
                        rrect(c, cx + 10, ky + 8, cw - 20, rh - 16, 12, fill=colr, a=wk, fa=wk * 0.10)
                    vcol = colr if (best and wk > 0) else 'ink'
                    if col.get('verdict'):
                        vcol = 'c' if val == 'yes' else 'muted'
                    vsize = 34 if text_width(val, 34, 600) < cw - 30 else 27
                    text(c, val, cx + cw / 2, ky + 68, vsize, 600, mix('ink', PAL[colr], wk) if vcol == colr else vcol,
                         1, 'center')
                    if sub:
                        ssize = 15 if text_width(sub, 15, 400) < cw - 24 else 13
                        text(c, sub, cx + cw / 2, ky + 102, ssize, 400, 'muted', 1, 'center')

class ScoreScene(Scene):
    """One judge fills in the scorecard. Subclasses set COLS_DONE, COLS_NOW, TIMES (one per file), WIN, NUM, KICK,
    TITLE, and optionally NOTE (a mono line under the table)."""
    dur = 18.0
    cues = [(0.2, 'whoosh')]
    COLS_DONE, COLS_NOW, TIMES, WIN = (), (0,), (2.0, 5.0, 9.0, 13.0), 15.0
    NUM, KICK, TITLE, NOTE = '01', 'judge', 'The *scores*', 'bits  ·  each file is 1,048,576 bits (1 M)'
    HEAD_T = 0.4

    def draw(self, c, t):
        header(c, t, self.NUM, self.KICK, self.TITLE)
        scorecard(c, t, self.COLS_DONE, self.COLS_NOW, self.TIMES, self.HEAD_T, self.WIN)
        if self.NOTE:
            note(c, self.NOTE, SC['right'], 210, ramp(t, 0.8, 0.6) * 0.9, 16, 'muted', 'right')

# ---------------------------------------------------------------- small pieces
def quote_card(c, t, t0, q, who, x, y, w, size=36, a=1.0, maxw=None):
    """A pull quote: amber rule, italic text (rich markup allowed), attribution."""
    k = ramp(t, t0, 0.8, e_expo) * a
    if k <= 0:
        return 0
    items, nl, lh = layout_rich(q, size, maxw or w - 120)
    h = nl * lh + 110
    with layer(c, k):
        panel(c, x, y, w, h)
        line(c, x + 36, y + 1, x + 156, y + 1, 'y', 1, 4, cap='butt')
        text(c, '“', x + 34, y + 96, 96, 400, 'y', 0.8, kind='italic')
        rich(c, '{i:' + q + '}', x + 96, y + 66, size, maxw or w - 120, t, t0 + 0.25, 0.02, 0.5, lh=1.32)
        text(c, who, x + w - 40, y + h - 30, 18, 400, 'muted', ramp(t, t0 + 0.8, 0.6), 'right', kind='mono', tracking=0.06)
    return h

def card(c, x, y, w, h, k, colr='y', title=None, tsize=36):
    """A panel with a coloured top rule and an italic title; returns nothing (draw contents after)."""
    panel(c, x, y, w, h, k)
    line(c, x + 36, y + 1, x + 156, y + 1, colr, k, 4, cap='butt')
    if title:
        text(c, title, x + 36, y + 70, tsize, 400, 'ink', k, kind='italic')

def tag(c, s, x, y, a=1.0, color='muted', size=15, align='left'):
    """A lowercase mono source tag ('our check', 'illustration', 'Fig. 3, redrawn')."""
    text(c, s, x, y, size, 400, color, a * 0.95, align, kind='mono', tracking=0.06)

def question_cards(c, t, qs, y0=300, dy=162, h=138, size=34):
    for i, (q, ti) in enumerate(qs):
        k = ramp(t, ti, 0.9, e_expo)
        if k <= 0:
            continue
        yy = y0 + i * dy
        with layer(c, k):
            with xform(c, 0, (1 - k) * 30):
                panel(c, MX, yy, W - 2 * MX, h)
                line(c, MX + 36, yy + 1, MX + 156, yy + 1, 'y', 1, 4, cap='butt')
                text(c, f'{i + 1}', MX + 56, yy + h * 0.66, 64, 300, 'y', 1, kind='italic')
                rich(c, q, MX + 150, yy + h * 0.6, size, W - 2 * MX - 220, t, ti + 0.3, 0.025, 0.45)

def brace(c, x0, x1, y, color='y', a=1.0, prog=1.0, depth=16, up=False):
    """A curly brace under (or over) [x0, x1]."""
    if a <= 0 or prog <= 0:
        return
    s = -1 if up else 1
    xm = (x0 + x1) / 2
    p = skia.Path()
    p.moveTo(x0, y)
    p.cubicTo(x0, y + s * depth * 0.7, x0 + 10, y + s * depth * 0.5, xm - 14, y + s * depth * 0.55)
    p.cubicTo(xm - 4, y + s * depth * 0.6, xm, y + s * depth * 0.8, xm, y + s * depth)
    p.cubicTo(xm, y + s * depth * 0.8, xm + 4, y + s * depth * 0.6, xm + 14, y + s * depth * 0.55)
    p.cubicTo(x1 - 10, y + s * depth * 0.5, x1, y + s * depth * 0.7, x1, y)
    meas = skia.PathMeasure(p, False)
    seg = skia.Path()
    meas.getSegment(0, meas.getLength() * prog, seg, True)
    c.drawPath(seg, paint(color, a, stroke=2.6))
