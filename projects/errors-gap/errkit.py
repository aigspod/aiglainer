"""Shared drawing pieces for the three "Do circuits explain model errors?" videos (errors-gap, errors-excuses,
errors-wrongname). The other two list SOURCES = ['errors-gap'] and `from errkit import *`.

Sources: arXiv:2609.35686v1. Table 8 (the IOI reference circuit's heads), Table 1, Table 4, Table 7, §4.2, §4.3, Fig. 2.
"""
import math
import numpy as np
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash

CITE = 'Zhang, Geng, Zhang, Yang, Zhang, Ye & Si (2026).  Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?  Preprint.'
ARXIV = 'arxiv.org/abs/2609.35686'

# Table 8: the IOI reference circuit in GPT-2 small (layer.head), by group. 26 heads.
GROUPS = [
    ('name movers', 'y', [(9, 9), (10, 0), (9, 6)]),
    ('backup name movers', 'v', [(10, 10), (10, 6), (10, 2), (10, 1), (11, 2), (9, 7), (9, 0), (11, 9)]),
    ('negative name movers', 'r', [(10, 7), (11, 10)]),
    ('inhibition', 'c', [(7, 3), (7, 9), (8, 6), (8, 10)]),
    ('induction', 'g', [(5, 5), (5, 8), (5, 9), (6, 9)]),
    ('duplicate token', 'f', [(0, 1), (0, 10), (3, 0)]),
    ('previous token', 'x', [(2, 2), (4, 11)]),
]
HEAD_COLOR = {h: colr for _, colr, hs in GROUPS for h in hs}

def head_grid(c, x, y, cell, t, t_lit=None, a=1.0, dim_rest=0.0, extra=None, labels=True, only=None):
    """GPT-2 small's 12 layers x 12 heads as a grid (layer 0 at the top). Circuit heads light up in their group
    colour from t_lit, one group at a time; dim_rest fades every other head (knocked out). extra: {(l, h): colour}."""
    if a <= 0:
        return
    r = cell * 0.34
    for l in range(12):
        for h in range(12):
            cx, cy = x + h * cell + cell / 2, y + l * cell + cell / 2
            colr = HEAD_COLOR.get((l, h))
            lit = 0.0
            if colr and t_lit is not None and (only is None or colr in only):
                gi = next(i for i, (_, cc, hs) in enumerate(GROUPS) if (l, h) in hs)
                lit = ramp(t, t_lit + gi * 0.45, 0.5, e_out)
            if extra and (l, h) in extra:
                colr, lit = extra[(l, h)]
            if lit > 0:
                circle(c, cx, cy, r * (1 + 0.15 * lit), fill=colr, a=a * lit, glow=6 * lit)
                circle(c, cx, cy, r, stroke='faint', sw=1.2, a=a * (1 - lit) * (1 - dim_rest))
            else:
                circle(c, cx, cy, r, stroke='faint', sw=1.4, a=a * (1 - 0.8 * dim_rest))
                circle(c, cx, cy, r * 0.35, fill='muted', a=a * 0.35 * (1 - dim_rest))
    if labels:
        for l in (0, 11):
            text(c, f'layer {l}', x - 14, y + l * cell + cell / 2 + 6, 16, 400, 'muted', a, 'right', kind='mono')
        text(c, '12 heads per layer', x + 6 * cell, y - 14, 16, 400, 'muted', a, 'center', kind='mono')

def legend_groups(c, x, y, t, t0, a=1.0, size=20, dy=34, groups=None):
    for i, (name, colr, hs) in enumerate(GROUPS):
        if groups is not None and name not in groups:
            continue
        k = ramp(t, t0 + i * 0.45, 0.5) * a
        circle(c, x + 8, y + i * dy - 7, 8, fill=colr, a=k)
        text(c, f'{name}  ({len(hs)})', x + 28, y + i * dy, size, 500, 'ink', k)

def tokens(c, words, x, y, size, t, t0, a=1.0, colors=None, stagger=0.06, gap=None):
    """A sentence laid out as words; colors {index: colour}. Returns the x-centres of the words."""
    gap = gap if gap is not None else size * 0.32
    xs, cx = [], x
    for i, w in enumerate(words):
        wd = text_width(w, size, 500)
        k = ramp(t, t0 + i * stagger, 0.4) * a
        colr = (colors or {}).get(i, 'ink')
        if colr != 'ink' and k > 0:
            rrect(c, cx - 8, y - size * 0.95, wd + 16, size * 1.35, 8, fill=colr, a=k, fa=k * 0.16)
        text(c, w, cx, y, size, 500, colr, k)
        xs.append(cx + wd / 2)
        cx += wd + gap
    return xs

def pair_bars(c, rows, x, y, w, t, t0, a=1.0, bh=26, dy=110, label_w=330, show_f=True, swap=None):
    """Paired horizontal bars, correct agreement (green) over error agreement (coral), 0..100 %.
    rows: [(label, ok, err, F)] ; swap: optional (t1, rows2) to morph to other values from t1."""
    sc = w / 100.0
    bx = x + label_w
    k0 = ramp(t, t0, 0.6) * a
    for v in (0, 25, 50, 75, 100):
        X = bx + v * sc
        line(c, X, y - 40, X, y + dy * len(rows) - 30, 'line', k0 * 0.8, 1)
        text(c, f'{v}%', X, y - 50, 17, 500, 'muted', k0, 'center', kind='mono')
    for i, row in enumerate(rows):
        lab, ok, err, F = row
        if swap and t >= swap[0]:
            m = ramp(t, swap[0], 1.2, e_io)
            _, ok2, err2, F2 = swap[1][i]
            ok, err, F = lerp(ok, ok2, m), lerp(err, err2, m), (F2 if m > 0.5 else F)
        ti = t0 + 0.4 + i * 0.5
        k = ramp(t, ti, 0.6) * a
        if k <= 0:
            continue
        yy = y + i * dy
        text(c, lab, bx - 24, yy + 22, 25, 600, 'ink', k, 'right')
        if show_f and F is not None:
            text(c, f'faithfulness {F:.2f}', bx - 24, yy + 52, 17, 500, 'muted', k, 'right', kind='mono')
        g = ramp(t, ti, 1.0, e_expo)
        for j, (v, colr) in enumerate(((ok, 'f'), (err, 'c'))):
            yb = yy + j * (bh + 6)
            ww = max(3, v * sc * g)
            rrect(c, bx, yb, ww, bh, 5, fill=colr, a=k, fa=k * 0.85)
            text(c, f'{v:.1f}%', bx + ww + 12, yb + bh - 6, 20, 600, colr, k, kind='mono')

def bars_legend(c, x, y, a=1.0, size=21):
    rrect(c, x, y - 15, 26, 16, 4, fill='f', a=a, fa=a * 0.85)
    w = text(c, 'agrees where the model is right', x + 38, y, size, 500, 'ink', a)
    rrect(c, x + w + 80, y - 15, 26, 16, 4, fill='c', a=a, fa=a * 0.85)
    text(c, 'same mistake where the model is wrong', x + w + 118, y, size, 500, 'ink', a)

def illustration(c, x, y, a=1.0):
    note(c, 'illustration', x, y, a * 0.9, 16, 'muted')

def question_cards(c, t, qs, t0=0.6, y0=330, dy=250, h=210, size=40):
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
    """Title card shared by the three videos; subclasses set TITLE ('*word*' for amber), PART, STICKY."""
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]
    TITLE, PART, STICKY = 'Do circuits explain model *errors*?', '', ['circuits & errors', 'the gap']

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, 'the aigs pod  ·  /mull/  ·  journal club, nov 4', x0, 300, ramp(t, 0.2, 0.8), 'muted', 18)
        lamp(c, 1650, 190, 1.35, ramp(t, 0.0, 0.8), on=ramp(t, 0.15, 1.2, e_out))
        k = ramp(t, 0.1, 1.0, e_expo)
        parts = self.TITLE.split('*')
        with layer(c, k):
            xx, yy = x0, 500 + (1 - k) * 40
            for i, p in enumerate(parts):
                if not p:
                    continue
                if i % 2:
                    wd = text(c, p, xx, yy, 104, 400, 'y', 1, kind='italic')
                    swash(c, xx - 4, xx + wd + 6, yy + 26, 'y', 1, ramp(t, 0.8, 0.9, e_io), w=4)
                else:
                    wd = text(c, p, xx, yy, 104, 700, 'ink', 1, tracking=-0.01)
                xx += wd
        text(c, 'Rethinking Circuit Evaluation', x0, 610, 44, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si', x0, 690, 28, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, 'toronto · mcgill · tsinghua  ·  preprint 2026  ·  arxiv:2609.35686', x0, 750, ramp(t, 2.6, 0.8), 'muted', 17)
        sticky(c, 1500, 640, self.STICKY, ramp(t, 3.2, 0.5, e_back), rot=5.0)

class EndCard(Scene):
    """Takeaway + citation. Subclasses set TAKE (rich text), STATS [(big, small, colour)], NEXT."""
    dur = 14.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (13.0, 'outro')]
    TAKE, STATS, NEXT = '', [], ''

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 210, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, self.TAKE, W / 2, 290, 48, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        for i, (big, small, colr) in enumerate(self.STATS):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * 560, 545, big, small, colr, k, 60)
        k2 = ramp(t, 4.5, 0.9)
        with layer(c, k2):
            line(c, MX, 680, W - MX, 680, 'line', 1, 1.5)
            text(c, CITE, MX, 735, 24, 600, 'ink')
            text(c, ARXIV, MX, 780, 22, 500, 'g', 1, kind='mono')
            if self.NEXT:
                kicker(c, self.NEXT, MX, 840, 1, 'y', 18)
        k3 = ramp(t, 6.0, 0.8)
        lamp(c, 1660, 790, 1.1, k3, on=k3)
        hand(c, 'see you at the desk', 1390, 975, 36, 'pencil', k3, -3.0, ramp(t, 6.4, 1.0, e_lin))
