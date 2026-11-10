"""Shared drawing pieces for the dynamics topic (videos and shorts): "A Mechanistic Analysis of Transformers for
Dynamical Systems" (arXiv:2512.21113v2). Other pieces list SOURCES = ['dynamics/videos/sign'] and `from dynkit import *`;
load_json('sdof.json') etc. then finds this folder's data/ (written by simulate.py, OUR simulations: label them).

Every plot helper takes a rectangle (x, y, w, h) and a label size `fs`, so it works on the 1920x1080 canvas and in a
short's 720x700 BOX (use fs >= 19 there). Animations run from (t, t0): pass the scene time and when the piece starts.
Section headers: call hdr(self, c, t, '02', 'kicker', 'Title with one *word*') so subclasses can renumber with NUM.

Numbers typed below come from projects/dynamics/AGENTS.md (which cites the paper's sections and tables).
"""
import math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash, hand_arrow

CITE = 'Duthé, Evangelou, Liu, Kevrekidis & Chatzi.  A Mechanistic Analysis of Transformers for Dynamical Systems.  arXiv preprint, v2 2026.'
ARXIV = 'arxiv.org/abs/2512.21113'
AUTHORS = 'Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi'
AFFIL = 'eth zürich · johns hopkins · singapore-eth centre  ·  arxiv:2512.21113'
PAPER_TITLE = 'A Mechanistic Analysis of Transformers for Dynamical Systems'

SIM = 'simulated from the paper’s equations'          # put this on every chart drawn from simulate.py output
CALC = 'our calculation'
EXTRAP = 'our extrapolation'

# ---- numbers from the paper (see projects/dynamics/AGENTS.md for each source and the accuracy notes)
SDOF = dict(m=1.0, c=0.5, fs=25.0, x0_mm=10.0,
            k2000=dict(fn=7.12, a1=-0.4352, a2=-0.9802),      # §3.1 Case 1 (paper's a1; ours from Eq. 20 is -0.428)
            k500=dict(fn=3.56, a1=1.24, a2=-0.98))            # §3.1 Case 2: paper gives signs only; values are OUR calculation
TWO_HEAD_WO = (1.087, -1.244)                                 # App. A.1, learned output weights of the two-head model
TWODOF = dict(k=(1000, 1500), c=0.5, m=1.0, f_ours=(3.26, 9.52), f_paper=(4.1, 9.5))   # §3.2 (see accuracy note)
# Table 1 (§4.1, Van der Pol, partial observation: only x), test MSE, mean over 10 seeds
TABLE1 = [('MLP only', 2.485e-2, 'c'), ('polynomial NARX', 2.192e-3, 'v'), ('attention, 1D latent, no PE', 1.789e-3, 'g'),
          ('attention, 2D latent, no PE', 1.770e-3, 'g'), ('attention, 1D latent, PE', 5.848e-4, 'f'),
          ('attention, 2D latent, PE', 2.065e-5, 'y')]
# §4.3 / App. A.5: full-field reconstruction error from the one-sensor latent (Geometric Harmonics, 5-fold CV)
CYL_RECON = [('whole field', 1.12e-4, 7.45e-3), ('wake', 2.48e-4, 1.33e-2)]   # (label, with Re, without Re)

SUP = str.maketrans('-0123456789', '⁻⁰¹²³⁴⁵⁶⁷⁸⁹')

def sci(v, nd=1):
    """1.79e-3 -> '1.8 × 10⁻³' (for labels)."""
    e = int(math.floor(math.log10(abs(v))))
    m = v / 10 ** e
    return f'{m:.{nd}f} × 10{str(e).translate(SUP)}'

def decade(e):
    return f'10{str(e).translate(SUP)}'

# ---------------------------------------------------------------- labels and headers
def hdr(scene, c, t, num, kick, title, sub=None, **kw):
    """Section header whose number a subclass can override with NUM (like the errors topic)."""
    header(c, t, getattr(scene, 'NUM', num), kick, title, sub=sub, **kw)

def illustration(c, x, y, a=1.0, s='illustration', size=16, align='left'):
    note(c, s, x, y, a * 0.9, size, 'muted', align)

def sim_label(c, x, y, a=1.0, size=16, align='left', extra=''):
    """'simulated from the paper's equations' (+ optional ' · k = 500 N/m')."""
    note(c, SIM + (f'  ·  {extra}' if extra else ''), x, y, a * 0.9, size, 'muted', align)

def extrap_label(c, x, y, a=1.0, size=18, align='left'):
    """The amber 'our extrapolation' pill-less tag for the climate-emulator link."""
    note(c, EXTRAP, x, y, a, size, 'y', align)

def question_cards(c, t, qs, t0=0.6, y0=330, dy=250, h=210, size=40):
    """Numbered discussion cards. qs: [(rich text, start time)]."""
    for i, (q, ti) in enumerate(qs):
        k = ramp(t, ti, 0.9, e_expo)
        if k <= 0:
            continue
        yy = y0 + i * dy
        with layer(c, k):
            with xform(c, 0, (1 - k) * 30):
                panel(c, MX, yy, W - 2 * MX, h)
                line(c, MX + 36, yy + 1, MX + 156, yy + 1, 'y', 1, 4, cap='butt')
                text(c, f'{i + 1}', MX + 50, yy + h * 0.6, 72, 300, 'y', 1, kind='italic')
                rich(c, q, MX + 150, yy + h * 0.44, size, W - 2 * MX - 220, t, ti + 0.3, 0.025, 0.45)

class TitleCard(Scene):
    """Title card for every dynamics video. Subclasses set TITLE ('*word*' is amber italic), SUBTITLE, STICKY,
    KICKER; TITLE_SIZE shrinks automatically to fit. Ends of the animation: ~3.7 s."""
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]
    TITLE = 'Attention as a *dynamical* system'
    SUBTITLE = PAPER_TITLE
    KICKER = 'the aigs pod  ·  /mull/  ·  journal club, nov 11'
    STICKY = ['transformers', '& dynamics']
    TITLE_SIZE = 104
    AUTHORS, AFFIL = AUTHORS, AFFIL

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, self.KICKER, x0, 300, ramp(t, 0.2, 0.8), 'muted', 18)
        lamp(c, 1650, 190, 1.35, ramp(t, 0.0, 0.8), on=ramp(t, 0.15, 1.2, e_out))
        k = ramp(t, 0.1, 1.0, e_expo)
        parts = self.TITLE.split('*')
        size = self.TITLE_SIZE
        tot = sum(text_width(p, size, 400, 'italic') if i % 2 else text_width(p, size, 700, tracking=-0.01)
                  for i, p in enumerate(parts) if p)
        size = size * min(1.0, 1600 / max(tot, 1))
        with layer(c, k):
            xx, yy = x0, 500 + (1 - k) * 40
            for i, p in enumerate(parts):
                if not p:
                    continue
                if i % 2:
                    wd = text(c, p, xx, yy, size, 400, 'y', 1, kind='italic')
                    swash(c, xx - 4, xx + wd + 6, yy + size * 0.25, 'y', 1, ramp(t, 0.8, 0.9, e_io), w=4)
                else:
                    wd = text(c, p, xx, yy, size, 700, 'ink', 1, tracking=-0.01)
                xx += wd
        text(c, self.SUBTITLE, x0, 610, 42, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, self.AUTHORS, x0, 690, 28, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, self.AFFIL, x0, 750, ramp(t, 2.6, 0.8), 'muted', 17)
        sticky(c, 1500, 800, self.STICKY, ramp(t, 3.2, 0.5, e_back), rot=5.0)

class EndCard(Scene):
    """Takeaway + citation. Subclasses set TAKE (rich text), STATS [(big, small, colour)], NEXT (a kicker line, e.g.
    'journal club · nov 11'), HAND. Keep hold >= 2.0 on the scene's last narration line (house rule)."""
    dur = 14.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (13.0, 'outro')]
    TAKE, STATS, NEXT, HAND = '', [], '', 'see you at the desk'

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 210, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, self.TAKE, W / 2, 290, 48, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        n = max(1, len(self.STATS))
        step = min(560, (W - 2 * MX - 80) / n)
        for i, (big, small, colr) in enumerate(self.STATS):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * step, 545, big, small, colr, k, 60)
        k2 = ramp(t, 4.5, 0.9)
        with layer(c, k2):
            line(c, MX, 680, W - MX, 680, 'line', 1, 1.5)
            text(c, CITE, MX, 735, 24, 600, 'ink')
            text(c, ARXIV, MX, 780, 22, 500, 'g', 1, kind='mono')
            if self.NEXT:
                kicker(c, self.NEXT, MX, 840, 1, 'y', 18)
        k3 = ramp(t, 6.0, 0.8)
        lamp(c, 1660, 790, 1.1, k3, on=k3)
        if self.HAND:
            hand(c, self.HAND, 1390, 975, 36, 'pencil', k3, -3.0, ramp(t, 6.4, 1.0, e_lin))

# ---------------------------------------------------------------- small pieces
def token_row(c, values, x, y, t, t0, a=1.0, bw=96, bh=56, gap=12, fs=22, fmt='{:+.2f}', colors=None, labels=None,
              stagger=0.08, lab_fs=None, fill='panel'):
    """A row of token boxes holding numbers (or strings). labels under each box (e.g. 'x(t−4)'). Returns box centres."""
    xs = []
    lab_fs = lab_fs or max(14, fs * 0.72)
    for i, v in enumerate(values):
        k = ramp(t, t0 + i * stagger, 0.45, e_out) * a
        bx = x + i * (bw + gap)
        xs.append(bx + bw / 2)
        if k <= 0:
            continue
        colr = (colors or {}).get(i, 'line') if isinstance(colors, dict) else (colors[i] if colors else 'line')
        rrect(c, bx, y, bw, bh, 10, fill=fill, a=k, fa=k * 0.85)
        rrect(c, bx, y, bw, bh, 10, stroke=colr, sw=1.6, a=k)
        s = v if isinstance(v, str) else fmt.format(v).replace('-', '−')
        text(c, s, bx + bw / 2, y + bh / 2 + fs * 0.36, fs, 600, 'ink' if colr == 'line' else colr, k, 'center', kind='mono')
        if labels:
            text(c, labels[i], bx + bw / 2, y + bh + lab_fs + 10, lab_fs, 400, 'muted', k, 'center', kind='mono')
    return xs

def convex_mix(c, x, y, w, alpha, t, t0, a=1.0, left='x(t−1)', right='x(t)', color='y', fs=22, show_rule=True):
    """The one-head rule as a slider: a segment between two past samples, a dot at weight alpha toward `right`.
    Weights shown as 'alpha' and '1 − alpha' bars under each end; 'weights > 0 and add up to 1' beneath."""
    k = ramp(t, t0, 0.6) * a
    if k <= 0:
        return
    line(c, x, y, x + w, y, 'muted', k, 3)
    for xx, lab in ((x, left), (x + w, right)):
        circle(c, xx, y, 9, fill='panel2', stroke='ink', sw=2, a=k)
        text(c, lab, xx, y - 26, fs, 600, 'ink', k, 'center', kind='mono')
    px = x + w * clamp(alpha)
    circle(c, px, y, 13, fill=color, a=k, glow=8)
    bh = 70
    for xx, wt in ((x, 1 - alpha), (x + w, alpha)):
        rrect(c, xx - 22, y + 30 + bh * (1 - wt), 44, max(2, bh * wt), 5, fill=color, a=k, fa=k * 0.8)
        text(c, f'{wt:.2f}', xx, y + 30 + bh + fs + 8, fs * 0.85, 500, color, k, 'center', kind='mono')
    if show_rule:
        text(c, 'weights > 0 and add up to 1', x + w / 2, y + 30 + bh + fs * 2.4 + 8, fs * 0.85, 400, 'muted', k,
             'center', kind='mono')

def signed_bars(c, x, y, w, h, vals, t, t0, a=1.0, labels=None, colors=None, vmax=None, fmt='{:+.2f}', fs=22,
                morph=None, bw=None, zero_label=True):
    """Vertical bars about a zero line at y + h/2 (positive up, negative down), value printed at the bar's end.
    For AR coefficients (a1, a2), one head's effective weights, or W_O. morph=(t1, vals2) eases to other values."""
    k0 = ramp(t, t0, 0.6) * a
    if k0 <= 0:
        return
    n = len(vals)
    vmax = vmax or max(abs(v) for v in vals) * 1.15
    y0 = y + h / 2
    slot = w / n
    bw = bw or slot * 0.42
    line(c, x, y0, x + w, y0, 'muted', k0, 1.6)
    if zero_label:
        text(c, '0', x - 12, y0 + fs * 0.35, fs * 0.85, 500, 'muted', k0, 'right', kind='mono')
    for i, v in enumerate(vals):
        if morph and t >= morph[0]:
            v = lerp(v, morph[1][i], ramp(t, morph[0], 1.0, e_io))
        k = ramp(t, t0 + 0.2 + i * 0.25, 0.7, e_out) * a
        if k <= 0:
            continue
        colr = (colors[i] if colors else ('f' if v >= 0 else 'c'))
        cx = x + slot * (i + 0.5)
        hh = (h / 2) * abs(v) / vmax * ramp(t, t0 + 0.2 + i * 0.25, 0.9, e_expo)
        top = y0 - hh if v >= 0 else y0
        rrect(c, cx - bw / 2, top, bw, max(hh, 2), 6, fill=colr, a=k, fa=k * 0.85)
        ty = y0 - hh - 12 if v >= 0 else y0 + hh + fs + 6
        text(c, fmt.format(v).replace('-', '−'), cx, ty, fs, 700, colr, k, 'center', kind='mono')
        if labels:
            ly = y0 + fs + 10 if v >= 0 else y0 - 14
            text(c, labels[i], cx, ly, fs, 500, 'ink', k, 'center')

def log_bars(c, x, y, w, rows, t, t0, a=1.0, lo=1e-5, hi=1e-1, label_w=430, bh=30, dy=62, fs=22, stagger=0.35,
             value_fmt=sci, note_s='lower is better'):
    """Horizontal bars on a log axis (error: shorter is better). rows: [(label, value, colour)] e.g. TABLE1.
    Decade gridlines from lo to hi labelled 10⁻⁵ ... ; value printed at each bar's end."""
    bx = x + label_w
    sc = w / (math.log10(hi) - math.log10(lo))
    k0 = ramp(t, t0, 0.6) * a
    if k0 <= 0:
        return
    for e in range(int(round(math.log10(lo))), int(round(math.log10(hi))) + 1):
        X = bx + (e - math.log10(lo)) * sc
        line(c, X, y - 30, X, y + dy * len(rows) - 20, 'line', k0 * 0.8, 1)
        text(c, decade(e), X, y - 40, fs * 0.85, 500, 'muted', k0, 'center')
    if note_s:
        text(c, note_s, bx + w, y + dy * len(rows) + 8, fs * 0.75, 400, 'muted', k0, 'right', kind='mono')
    for i, (lab, v, colr) in enumerate(rows):
        ti = t0 + 0.3 + i * stagger
        k = ramp(t, ti, 0.6) * a
        if k <= 0:
            continue
        yy = y + i * dy
        text(c, lab, bx - 20, yy + bh * 0.75, fs, 600, 'ink', k, 'right')
        ww = max(3, (math.log10(v) - math.log10(lo)) * sc * ramp(t, ti, 1.0, e_expo))
        rrect(c, bx, yy, ww, bh, 5, fill=colr, a=k, fa=k * 0.85)
        text(c, value_fmt(v), bx + ww + 12, yy + bh * 0.75, fs * 0.9, 600, colr, k)

def pair_bars(c, rows, x, y, w, t, t0, a=1.0, names=('with Re', 'without Re'), colors=('f', 'c'), log=True,
              lo=1e-5, hi=1e-1, label_w=260, bh=28, dy=120, fs=22, value_fmt=sci, legend=True):
    """Two bars per row (e.g. CYL_RECON: with vs without the Reynolds number), log axis by default.
    rows: [(label, v1, v2)]."""
    k0 = ramp(t, t0, 0.6) * a
    if k0 <= 0:
        return
    bx = x + label_w
    L = (lambda v: (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo))) if log else (lambda v: v / hi)
    if log:
        for e in range(int(round(math.log10(lo))), int(round(math.log10(hi))) + 1):
            X = bx + L(10 ** e) * w
            line(c, X, y - 30, X, y + dy * len(rows) - 40, 'line', k0 * 0.8, 1)
            text(c, decade(e), X, y - 40, fs * 0.85, 500, 'muted', k0, 'center')
    for i, (lab, v1, v2) in enumerate(rows):
        ti = t0 + 0.3 + i * 0.5
        k = ramp(t, ti, 0.6) * a
        if k <= 0:
            continue
        yy = y + i * dy
        text(c, lab, bx - 20, yy + bh + 6, fs, 600, 'ink', k, 'right')
        g = ramp(t, ti, 1.0, e_expo)
        for j, (v, colr) in enumerate(((v1, colors[0]), (v2, colors[1]))):
            yb = yy + j * (bh + 6)
            ww = max(3, L(v) * w * g)
            rrect(c, bx, yb, ww, bh, 5, fill=colr, a=k, fa=k * 0.85)
            text(c, value_fmt(v), bx + ww + 12, yb + bh - 6, fs * 0.85, 600, colr, k)
    if legend:
        yl = y + dy * len(rows) - 10
        xx = bx
        for nm, colr in zip(names, colors):
            rrect(c, xx, yl - 14, 24, 15, 4, fill=colr, a=k0, fa=k0 * 0.85)
            xx += 36 + text(c, nm, xx + 34, yl, fs * 0.85, 500, 'ink', k0) + 40

# ---------------------------------------------------------------- doodles
def _zigzag(x0, x1, y, n=7, amp=14):
    """Spring polyline from (x0, y) to (x1, y): short straight ends, n zigzag peaks."""
    L = x1 - x0
    e = min(18, L * 0.12)
    pts = [(x0, y), (x0 + e, y)]
    for i in range(2 * n):
        pts.append((x0 + e + (L - 2 * e) * (i + 0.5) / (2 * n), y + (amp if i % 2 else -amp)))
    pts += [(x1 - e, y), (x1, y)]
    return np.array(pts)

def spring_mass(c, x, y, disps=(0.0,), a=1.0, s=1.0, masses=None, springs=None, colors=None, damper=True,
                rest=False, arrow_on=None, rest_len=170, box=92, fs=24):
    """A wall-spring-mass chain doodle: wall at x, len(disps) masses joined by springs (and dashpots), on a floor.
    y is the masses' vertical centre. disps: each mass's displacement from rest in px (animate it from t, e.g.
    18 * sin(2 pi f t)). masses/springs: labels (default 'm', 'k' or 'm₁', 'k₁', ...). rest: dashed rest lines.
    arrow_on: index of a mass to draw a displacement arrow under. Returns the masses' centre x (unscaled coords)."""
    if a <= 0:
        return []
    n = len(disps)
    masses = masses or (['m'] if n == 1 else [f'm{chr(0x2081 + i)}' for i in range(n)])
    springs = springs or (['k'] if n == 1 else [f'k{chr(0x2081 + i)}' for i in range(n)])
    colors = colors or ['y'] * n
    cxs = []
    with xform(c, x, y, s):
        hb = box / 2
        line(c, 0, -hb - 40, 0, hb + 10, 'pencil', a, 3)                 # wall
        for j in range(7):
            yy = -hb - 34 + j * 20
            line(c, 0, yy, -16, yy + 14, 'pencil', a * 0.6, 1.6)
        line(c, -16, hb + 12, (rest_len + box) * n + 120, hb + 12, 'pencil', a * 0.7, 2)   # floor
        left = 0.0
        for i in range(n):
            x_rest = (rest_len + box) * i + rest_len
            xl = x_rest + disps[i]
            sy, dy_ = -hb * 0.4, hb * 0.45
            if not damper:
                sy = 0
            draw_poly(c, _zigzag(left, xl, sy, 7, 12), 'pencil', a, 2.4)
            text(c, springs[i], (left + xl) / 2, sy - 22, fs, 500, 'muted', a, 'center', kind='italic')
            if damper:
                mid = (left + xl) / 2
                line(c, left, dy_, mid - 18, dy_, 'pencil', a, 2.2)
                line(c, mid - 18, dy_ - 13, mid - 18, dy_ + 13, 'pencil', a, 2.2)
                line(c, mid - 26, dy_ - 13, mid + 16, dy_ - 13, 'pencil', a * 0.8, 2)
                line(c, mid - 26, dy_ + 13, mid + 16, dy_ + 13, 'pencil', a * 0.8, 2)
                line(c, mid + 16, dy_ - 13, mid + 16, dy_ + 13, 'pencil', a * 0.8, 2)
                line(c, mid - 8, dy_, xl, dy_, 'pencil', a, 2.2)
                line(c, mid - 8, dy_ - 9, mid - 8, dy_ + 9, 'pencil', a, 2.2)
            if rest:
                X = x_rest + hb
                line(c, X, -hb - 30, X, hb + 30, 'muted', a * 0.6, 1.4, dash=[6, 6])
            rrect(c, xl, -hb, box, box, 10, fill=colors[i], a=a, fa=a * 0.22)
            rrect(c, xl, -hb, box, box, 10, stroke=colors[i], sw=2.4, a=a)
            text(c, masses[i], xl + hb, fs * 0.38, fs * 1.2, 500, colors[i], a, 'center', kind='italic')
            if arrow_on == i and abs(disps[i]) > 3:
                X = x_rest + hb
                arrow(c, X, hb + 36, X + disps[i], hb + 36, colors[i], a, 2.4, 10)
            cxs.append(xl + hb)
            left = xl + box
    return cxs

# ---------------------------------------------------------------- plots
def _rng(vals, pad=0.08):
    lo, hi = float(np.min(vals)), float(np.max(vals))
    d = (hi - lo) or 1.0
    return lo - d * pad, hi + d * pad

def trace_plot(c, x, y, w, h, series, t, t0, a=1.0, xr=None, yr=None, xticks=(), yticks=(), xlabel=None, ylabel=None,
               dur=1.6, fs=20, fmt='{:g}', xfmt='{:g}', grid=True, axes=True, stagger=0.5, label_room=200):
    """Time-series plot. series: list of dicts {x, y, color, w=3, dash=None, dots=False, r=4, label=None, t0=None,
    dur=None, glow=0, a=1, line=True, label_xy=None}. Each draws left to right from its own t0 (default
    t0 + 0.6 + i * stagger). A label sits at its line's right end, or above the end (right-aligned) when it would run
    more than label_room px past the plot, or at label_xy (data coordinates). Returns the kit.Axes so a scene can annotate in data coordinates (ax.px(x, y))."""
    allx = np.concatenate([np.asarray(s['x'], float) for s in series])
    ally = np.concatenate([np.asarray(s['y'], float) for s in series])
    xr = xr or (float(allx.min()), float(allx.max()))
    yr = yr or _rng(ally)
    ax = Axes(x, y, w, h, xr, yr)
    k = ramp(t, t0, 0.7) * a
    if k <= 0:
        return ax
    if axes:
        _axes_draw(ax, c, k, xticks, yticks, fs, fmt, xfmt, grid, ramp(t, t0, 0.9, e_io))
        if xlabel:
            text(c, xlabel, x + w, y + h + fs * 1.6 + 22, fs * 0.9, 400, 'muted', k, 'right', kind='mono')
        if ylabel:
            text(c, ylabel, x, y - 18, fs * 0.9, 400, 'muted', k, 'left', kind='mono')
    for i, s in enumerate(series):
        st = s.get('t0', t0 + 0.6 + i * stagger)
        pr = ramp(t, st, s.get('dur', dur), e_io)
        if pr <= 0:
            continue
        xs, ys = np.asarray(s['x'], float), np.asarray(s['y'], float)
        m = (xs >= xr[0]) & (xs <= xr[1])
        P = ax.pts(xs[m], np.clip(ys[m], yr[0], yr[1]))
        colr, aa = s.get('color', 'y'), a * s.get('a', 1.0)
        if s.get('line', True):
            draw_poly(c, P, colr, aa, s.get('w', 3), pr, s.get('dash'), s.get('glow', 0))
        if s.get('dots'):
            nshow = int(len(P) * pr + 1e-9)
            for p in P[:nshow]:
                circle(c, p[0], p[1], s.get('r', 4), fill=colr, a=aa)
        if s.get('label') and pr > 0.95:
            ka = aa * ramp(t, st + s.get('dur', dur) * 0.95, 0.4)
            if s.get('label_xy') is not None:                       # data coordinates, left-aligned
                X, Y = ax.px(*s['label_xy'])
                text(c, s['label'], float(X), float(Y), fs, 600, colr, ka)
            elif P[-1][0] + 12 + text_width(s['label'], fs, 600) > x + w + label_room:
                p = P[-1]                                           # no room on the right: above the end, right-aligned
                text(c, s['label'], p[0], p[1] - fs * 0.8, fs, 600, colr, ka, 'right')
            else:
                p = P[-1]
                text(c, s['label'], p[0] + 12, p[1] + fs * 0.35, fs, 600, colr, ka)
    return ax

def _axes_draw(ax, c, k, xticks, yticks, fs, fmt, xfmt, grid, prog):
    """kit.Axes.draw with a label size (kit's is fixed at 22 px)."""
    if grid:
        for yv in yticks:
            _, Y = ax.px(0, yv)
            line(c, ax.x, Y, ax.x + ax.w * prog, Y, 'line', k * 0.7, 1)
        for xv in xticks:
            X, _ = ax.px(xv, 0)
            line(c, X, ax.y + ax.h, X, ax.y + ax.h * (1 - prog), 'line', k * 0.7, 1)
    if ax.yr[0] < 0 < ax.yr[1]:
        _, Y0 = ax.px(0, 0)
        line(c, ax.x, Y0, ax.x + ax.w * prog, Y0, 'muted', k * 0.6, 1.4)
    line(c, ax.x, ax.y + ax.h, ax.x + ax.w * prog, ax.y + ax.h, 'muted', k, 1.6)
    line(c, ax.x, ax.y + ax.h, ax.x, ax.y + ax.h * (1 - prog), 'muted', k, 1.6)
    for xv in xticks:
        X, _ = ax.px(xv, 0)
        text(c, xfmt.format(xv).replace('-', '−'), X, ax.y + ax.h + fs + 12, fs, 500, 'muted', k * prog, 'center', kind='mono')
    for yv in yticks:
        _, Y = ax.px(0, yv)
        text(c, fmt.format(yv).replace('-', '−'), ax.x - 12, Y + fs * 0.33, fs, 500, 'muted', k * prog, 'right', kind='mono')

def spectrum_plot(c, x, y, w, h, f, curves, t, t0, a=1.0, fmax=None, marks=(), norm='peak', fs=20, xticks=None,
                  xlabel='frequency (Hz)', ylabel='gain', fill=True, dur=1.4, stagger=0.6, db=False, db_floor=-40, yticks=None):
    """A small spectrum: curves [{mag, color, label=None, t0=None, w=3}] over frequencies f (Hz).
    norm: 'peak' scales each curve to its own maximum, 'first' scales all by the first curve's maximum, None = raw.
    db=True plots 20 log10 (floored at db_floor; ticks 0/−20/−40 unless yticks given). marks: [(f, label, colour)] dashed verticals labelled at the top
    (e.g. the natural frequency). Returns the Axes."""
    f = np.asarray(f, float)
    fmax = fmax or float(f.max())
    m = f <= fmax + 1e-9
    mags = [np.asarray(cv['mag'], float) for cv in curves]
    ref = mags[0].max()
    ys = []
    for mg in mags:
        v = mg / (mg.max() if norm == 'peak' else ref if norm == 'first' else 1.0)
        if db:
            v = np.maximum(20 * np.log10(np.maximum(v, 1e-12)), db_floor)
        ys.append(v)
    yr = (db_floor, 3) if db else (0, max(float(np.max(v[m])) for v in ys) * 1.1)
    ax = Axes(x, y, w, h, (0, fmax), yr)
    k = ramp(t, t0, 0.7) * a
    if k <= 0:
        return ax
    xticks = xticks if xticks is not None else [v for v in (0, 2, 4, 6, 8, 10, 12) if v <= fmax]
    yticks = yticks if yticks is not None else ((0, -20, -40) if db else ())
    _axes_draw(ax, c, k, xticks, yticks, fs, '{:g}', '{:g}', True, ramp(t, t0, 0.9, e_io))
    text(c, xlabel, x + w, y + h + fs * 1.6 + 22, fs * 0.9, 400, 'muted', k, 'right', kind='mono')
    if ylabel:
        text(c, ylabel, x, y - 18, fs * 0.9, 400, 'muted', k, 'left', kind='mono')
    for fm, lab, colr in marks:
        X, _ = ax.px(fm, 0)
        kk = ramp(t, t0 + 0.4, 0.6) * a
        line(c, X, y + h, X, y + 6, colr, kk * 0.8, 1.6, dash=[7, 7])
        if lab:
            text(c, lab, X, y - 6 + (0 if ylabel is None else -fs * 1.3), fs * 0.9, 600, colr, kk, 'center', kind='mono')
    for i, (cv, v) in enumerate(zip(curves, ys)):
        st = cv.get('t0', t0 + 0.6 + i * stagger)
        pr = ramp(t, st, dur, e_io)
        if pr <= 0:
            continue
        P = ax.pts(f[m], v[m])
        colr = cv.get('color', 'g')
        if fill and pr > 0:
            nn = max(2, int(len(P) * pr))
            pth = skia.Path()
            pth.moveTo(P[0][0], y + h)
            for p in P[:nn]:
                pth.lineTo(*p)
            pth.lineTo(P[nn - 1][0], y + h)
            pth.close()
            c.drawPath(pth, paint(colr, a * cv.get('a', 1.0) * 0.14))
        draw_poly(c, P, colr, a * cv.get('a', 1.0), cv.get('w', 3), pr, cv.get('dash'))
        if cv.get('label') and pr > 0.95:
            j = int(np.argmax(v[m]))
            text(c, cv['label'], P[j][0] + 14, P[j][1] - 10, fs, 600, colr, a * ramp(t, st + dur, 0.4))
    return ax

def phase_portrait(c, x, y, w, h, t, t0, a=1.0, cycle=None, transients=(), points=(), lim=3.3, fs=20,
                   xlabel='position x', ylabel='velocity', cycle_color='y', trans_color='g', dur=2.0, stagger=0.35,
                   mover=None, xline=None, ticks=(-3, -2, -1, 0, 1, 2, 3)):
    """Phase plane (x across, velocity up), both axes [-lim, lim]. cycle: (xs, vs) drawn from t0 + 0.4;
    transients: [(xs, vs)] drawn one after another after the cycle, each with a start dot; points:
    [(x, v, colour, label)] popping in at t0 + 0.6; mover: a phase in [0, 1) for a dot travelling on the cycle;
    xline: (X, colour) a vertical line 'same x' through the plane. Returns the Axes."""
    ax = Axes(x, y, w, h, (-lim, lim), (-lim, lim))
    k = ramp(t, t0, 0.7) * a
    if k <= 0:
        return ax
    _axes_draw(ax, c, k, ticks, ticks, fs, '{:g}', '{:g}', True, ramp(t, t0, 0.9, e_io))
    X0, Y0 = ax.px(0, 0)
    line(c, X0, y, X0, y + h, 'muted', k * 0.6, 1.4)
    text(c, xlabel, x + w, y + h + fs * 1.6 + 22, fs * 0.9, 400, 'muted', k, 'right', kind='mono')
    text(c, ylabel, x, y - 18, fs * 0.9, 400, 'muted', k, 'left', kind='mono')
    tc = t0 + 0.4
    if cycle is not None:
        P = ax.pts(*cycle)
        pr = ramp(t, tc, dur, e_io)
        draw_poly(c, P, cycle_color, a, 3.5, pr, glow=6)
        if mover is not None and pr >= 1:
            p = end_point(P, mover % 1.0)
            circle(c, p[0], p[1], 9, fill=cycle_color, a=a, glow=10)
    for i, (xs, vs) in enumerate(transients):
        st = tc + dur * 0.6 + i * stagger
        pr = ramp(t, st, dur, e_io)
        if pr <= 0:
            continue
        P = ax.pts(np.clip(xs, -lim, lim), np.clip(vs, -lim, lim))
        circle(c, P[0][0], P[0][1], 5, fill=trans_color, a=a * 0.9)
        draw_poly(c, P, trans_color, a * 0.75, 2, pr)
    if xline is not None:
        Xl, _ = ax.px(xline[0], 0)
        kk = ramp(t, t0 + 0.6, 0.6) * a
        line(c, Xl, y, Xl, y + h, xline[1], kk * 0.8, 1.8, dash=[8, 7])
        text(c, f'x = {xline[0]:g}', Xl + 10, y + fs + 6, fs * 0.9, 600, xline[1], kk, kind='mono')
    for i, (px, pv, colr, lab) in enumerate(points):
        kk = ramp(t, t0 + 0.6 + i * 0.3, 0.5, e_back) * a
        if kk <= 0:
            continue
        X, Y = ax.px(px, pv)
        circle(c, X, Y, 11 * min(kk, 1.2), fill=colr, a=min(kk, 1), glow=8)
        if lab:
            text(c, lab, X + 18, Y + fs * 0.35, fs, 600, colr, min(kk, 1))
    return ax

def attention_bars(c, x, y, w, h, weights, t, t0, a=1.0, labels=None, color='g', fs=18, vmax=None, show_values=True,
                   highlight=None, morph=None, title=None, stagger=0.08):
    """Attention weights over a token window as vertical bars (oldest left, newest right). Default labels
    't−n+1' ... 't'. vmax: the weight that fills h (default 1.0 if any weight > 0.5 else 0.5). highlight: {i: colour}.
    morph=(t1, weights2[, t2, weights3 ...]) eases between weight sets (e.g. a head flipping between lags).
    A 'weights add up to 1' note sits under the axis unless title says otherwise."""
    k0 = ramp(t, t0, 0.6) * a
    if k0 <= 0:
        return
    wts = np.asarray(weights, float)
    if morph:
        for j in range(0, len(morph), 2):
            if t >= morph[j]:
                wts = wts + (np.asarray(morph[j + 1], float) - wts) * ramp(t, morph[j], 0.8, e_io)
    n = len(wts)
    labels = labels or [('t' if i == n - 1 else f't−{n - 1 - i}') for i in range(n)]
    vmax = vmax or (1.0 if np.max(weights) > 0.5 else 0.5)
    slot = w / n
    bw = slot * 0.62
    line(c, x, y + h, x + w, y + h, 'muted', k0, 1.6)
    for i, v in enumerate(wts):
        k = ramp(t, t0 + 0.2 + i * stagger, 0.5) * a
        if k <= 0:
            continue
        cx = x + slot * (i + 0.5)
        hh = h * min(v / vmax, 1.0) * ramp(t, t0 + 0.2 + i * stagger, 0.8, e_expo)
        colr = (highlight or {}).get(i, color)
        rrect(c, cx - bw / 2, y + h - hh, bw, max(hh, 2), 5, fill=colr, a=k, fa=k * 0.85)
        if show_values:
            text(c, f'{v:.2f}', cx, y + h - hh - 10, fs, 600, colr, k, 'center', kind='mono')
        text(c, labels[i], cx, y + h + fs + 10, fs * 0.9, 400, 'muted', k, 'center', kind='mono')
    text(c, title if title is not None else 'weights add up to 1', x + w / 2, y + h + fs * 2.6 + 16, fs * 0.85, 400,
         'muted', k0, 'center', kind='mono')

def delay_window(c, x, y, w, h, ts, xs, i_end, n, t, t0, a=1.0, color='y', line_color='g', slide=None, fs=18,
                 vector=True, vec_xy=None, vec_bw=None, show_dots=True, yr=None):
    """Delay embedding: a sampled series across (x, y, w, h) with the n most recent samples ending at index i_end
    boxed and lit; vector=True stacks them as tokens [x(t), x(t−1), ...] in a column at vec_xy (default: right of the
    strip). slide=(t1, dur, i_end2) slides the window along the series. Returns the window's sample positions."""
    ts, xs = np.asarray(ts, float), np.asarray(xs, float)
    ax = Axes(x, y, w, h, (ts[0], ts[-1]), yr or _rng(xs, 0.12))
    k = ramp(t, t0, 0.6) * a
    if k <= 0:
        return []
    P = ax.pts(ts, xs)
    draw_poly(c, P, line_color, k * 0.8, 2.4, ramp(t, t0, 1.2, e_io))
    if show_dots:
        for p in P:
            circle(c, p[0], p[1], 3.2, fill=line_color, a=k * 0.6)
    ie = float(i_end)
    if slide and t >= slide[0]:
        ie = lerp(i_end, slide[2], ramp(t, slide[0], slide[1], e_io))
    ie = int(round(ie))
    idx = list(range(max(0, ie - n + 1), ie + 1))
    kw = ramp(t, t0 + 0.8, 0.6, e_expo) * a
    if kw <= 0:
        return []
    pw = P[idx]
    x0b, x1b = pw[0][0] - 16, pw[-1][0] + 16
    rrect(c, x0b, y - 8, x1b - x0b, h + 16, 12, fill=color, a=kw, fa=kw * 0.08)
    rrect(c, x0b, y - 8, x1b - x0b, h + 16, 12, stroke=color, sw=1.8, a=kw)
    text(c, f'last {n} samples', (x0b + x1b) / 2, y - 18, fs, 500, color, kw, 'center', kind='mono')
    for p in pw:
        circle(c, p[0], p[1], 7, fill=color, a=kw, glow=6)
    if vector:
        vx, vy = vec_xy or (x + w + 70, y)
        bw = vec_bw or 120
        bh = min(52, (h + 16) / n - 8)
        for j, i in enumerate(reversed(idx)):
            kk = ramp(t, t0 + 1.0 + j * 0.08, 0.4) * a
            yy = vy + j * (bh + 8)
            rrect(c, vx, yy, bw, bh, 9, fill='panel', a=kk, fa=kk * 0.85)
            rrect(c, vx, yy, bw, bh, 9, stroke=color, sw=1.5, a=kk)
            text(c, f'{xs[i]:+.2f}'.replace('-', '−'), vx + bw / 2, yy + bh / 2 + fs * 0.38, fs, 600, 'ink', kk,
                 'center', kind='mono')
            lab = 'x(t)' if j == 0 else f'x(t−{j})'
            text(c, lab, vx + bw + 12, yy + bh / 2 + fs * 0.35, fs * 0.9, 400, 'muted', kk, kind='mono')
    return pw

def latent_loop(c, x, y, w, h, loops, t, t0, a=1.0, colors=None, labels=None, square=False, dot_speed=0.25,
                dur=2.0, stagger=0.4, fs=18, axis_labels=('h₁', 'h₂'), frame=True, closed=True, widths=None):
    """Closed loops in a 2-D plane (a latent space, delay coordinates, or illustrative loops). loops: list of Nx2
    arrays (any units): all are fitted together into the rectangle (square=True keeps one scale for both axes;
    False stretches each axis, fine for flat loops like vdp.json's pca_loop). Each loop draws on from
    t0 + 0.4 + i * stagger, then a dot travels around it. labels sit at each loop's rightmost point."""
    k = ramp(t, t0, 0.6) * a
    if k <= 0:
        return
    allp = np.concatenate([np.asarray(L, float) for L in loops])
    lo, hi = allp.min(0), allp.max(0)
    span = np.maximum(hi - lo, 1e-9)
    if square:
        span[:] = span.max()
    pad = 0.1
    def M(L):
        L = np.asarray(L, float)
        u = (L - (lo + hi) / 2) / span
        return np.stack([x + w / 2 + u[:, 0] * w * (1 - 2 * pad), y + h / 2 - u[:, 1] * h * (1 - 2 * pad)], 1)
    if frame:
        line(c, x, y + h, x + w, y + h, 'muted', k, 1.4)
        line(c, x, y, x, y + h, 'muted', k, 1.4)
        if axis_labels:
            text(c, axis_labels[0], x + w, y + h + fs + 10, fs, 500, 'muted', k, 'right', kind='mono')
            text(c, axis_labels[1], x - 12, y + fs * 0.4, fs, 500, 'muted', k, 'right', kind='mono')
    for i, L in enumerate(loops):
        P = M(L)
        if closed:
            P = np.vstack([P, P[:1]])
        colr = (colors[i] if colors else 'y')
        st = t0 + 0.4 + i * stagger
        pr = ramp(t, st, dur, e_io)
        if pr <= 0:
            continue
        draw_poly(c, P, colr, a * 0.9, (widths[i] if widths else 3), pr, glow=4)
        if pr >= 1 and dot_speed:
            p = end_point(P, ((t - st - dur) * dot_speed) % 1.0)
            circle(c, p[0], p[1], 7, fill=colr, a=a, glow=8)
        if labels and labels[i] and pr > 0.9:
            j = int(np.argmax(P[:, 0]))
            text(c, labels[i], P[j][0] + 12, P[j][1] + fs * 0.35, fs, 600, colr, a * ramp(t, st + dur * 0.9, 0.4))

def illus_loops(params, separated=True, n=240, seed=2):
    """ILLUSTRATIVE loops for a parameter sweep (e.g. Reynolds numbers), NOT data: separated=True gives nested,
    ordered loops; False gives loops that overlap and cross (the 'without Re' picture). Label 'illustration'."""
    rng = np.random.default_rng(seed)
    th = np.linspace(0, 2 * np.pi, n, endpoint=False)
    out = []
    m = len(params)
    for i, _ in enumerate(params):
        u = i / max(m - 1, 1)
        if separated:
            rx, ry, sk = 1.0 + 0.9 * u, 0.55 + 0.45 * u, 0.25 * u
            L = np.stack([rx * np.cos(th) + sk * np.cos(2 * th), ry * np.sin(th) + 0.4 * u], 1)
        else:
            ph = rng.uniform(0, np.pi)
            rx, ry = 1.4 + 0.25 * rng.standard_normal(), 0.8 + 0.15 * rng.standard_normal()
            L = np.stack([rx * np.cos(th + ph) + 0.35 * np.cos(2 * th), ry * np.sin(th) + 0.3 * np.sin(3 * th + ph)], 1)
        out.append(L)
    return out

def coef_plane(c, cx, cy, size, t, t0, a=1.0, targets=(), lim=1.5, reach=True, best=None, fs=18, ticks=(-1, 1),
               xlabel='a₁  (weight on x(t))', ylabel='a₂  (weight on x(t−1))'):
    """The AR(2) coefficient plane: a1 across, a2 up, square of side `size` centred at (cx, cy), axes [-lim, lim].
    reach=True shades the two same-sign quadrants: everything one softmax head can reach (positive weights summing
    to one, times one output weight). targets: [(a1, a2, colour, label)] pop in from t0 + 0.8 + 0.5 i.
    best: (from_i, b1, b2, colour, label) draws an arrow from target from_i to the best one-head point."""
    ax = Axes(cx - size / 2, cy - size / 2, size, size, (-lim, lim), (-lim, lim))
    k = ramp(t, t0, 0.7) * a
    if k <= 0:
        return ax
    x0, y0 = cx - size / 2, cy - size / 2
    if reach:
        qf = min(fs, size / 2 * 0.9 / (0.62 * 18 * 1.1))       # quadrant labels fit their quadrant
        kr = ramp(t, t0 + 0.3, 0.8) * a
        rrect(c, cx, y0, size / 2, size / 2, 0, fill='f', a=kr, fa=kr * 0.13)
        rrect(c, x0, cy, size / 2, size / 2, 0, fill='f', a=kr, fa=kr * 0.13)
        text(c, 'one head can reach', cx + size / 4, y0 + fs + 12, qf, 600, 'f', kr, 'center', kind='mono')
        text(c, 'one head can reach', cx - size / 4, cy + size / 2 - 14, qf, 600, 'f', kr, 'center', kind='mono')
        text(c, 'out of reach', cx + size / 4, cy + size / 2 - 14, qf, 600, 'c', kr, 'center', kind='mono')
        text(c, 'out of reach', cx - size / 4, y0 + fs + 12, qf, 600, 'c', kr, 'center', kind='mono')
    rrect(c, x0, y0, size, size, 6, stroke='line', sw=1.4, a=k)
    line(c, x0, cy, x0 + size, cy, 'muted', k, 1.6)
    line(c, cx, y0, cx, y0 + size, 'muted', k, 1.6)
    for v in ticks:
        X, Y = ax.px(v, v)
        line(c, X, cy - 6, X, cy + 6, 'muted', k, 1.4)
        line(c, cx - 6, Y, cx + 6, Y, 'muted', k, 1.4)
        text(c, f'{v:+g}'.replace('-', '−'), X, cy + fs + 10, fs * 0.85, 500, 'muted', k, 'center', kind='mono')
        text(c, f'{v:+g}'.replace('-', '−'), cx - 12, Y + fs * 0.33, fs * 0.85, 500, 'muted', k, 'right', kind='mono')
    text(c, xlabel, x0 + size, y0 + size + fs * 1.4 + 14, fs, 500, 'ink', k, 'right')
    text(c, ylabel, x0, y0 - 16, fs, 500, 'ink', k, 'left')
    for i, (a1, a2, colr, lab) in enumerate(targets):
        kk = ramp(t, t0 + 0.8 + i * 0.5, 0.5, e_back) * a
        if kk <= 0:
            continue
        X, Y = ax.px(a1, a2)
        circle(c, X, Y, 12 * min(kk, 1.2), fill=colr, a=min(kk, 1), glow=10)
        if lab:
            text(c, lab, X, Y + 12 + fs * 1.1, fs, 700, colr, min(kk, 1), 'center')
    if best:
        i, b1, b2, colr, lab = best
        kk = ramp(t, t0 + 0.8 + len(targets) * 0.5 + 0.3, 0.8) * a
        if kk > 0:
            X0_, Y0_ = ax.px(targets[i][0], targets[i][1])
            X1_, Y1_ = ax.px(b1, b2)
            arrow(c, X0_, Y0_, X1_, Y1_, colr, kk, 2.4, 12, prog=ramp(t, t0 + 0.8 + len(targets) * 0.5 + 0.3, 0.9, e_io), dash=[8, 6])
            circle(c, X1_, Y1_, 9, stroke=colr, sw=2.4, a=kk)
            if lab:
                text(c, lab, X1_ + 14, Y1_ - 14, fs, 600, colr, kk)
    return ax
