"""Extract figure data from "From Entropy to Epiplexity" (Finzi et al., arXiv:2601.03220v2) into data/*.json.

  python projects/epiplexity/data/extract_paper.py [paper.pdf]     (default: projects/epiplexity/paper/paper.pdf)

Every number comes from the PDF's vector paths (matplotlib output), mapped to data units through the figure's own
gridlines: each axis is calibrated from the gridline positions and the tick values printed next to them, fitted in
log10 space for log axes, and the fit residual is checked so a wrong scale type (log vs linear) fails loudly.
Values are stored in the axis' real units (the "x10^k" offsets are applied).

fig2c_preq_req.json   Fig. 2c   prequential vs requential epiplexity (MB), four dataset groups
fig3_eca.json         Fig. 3    ECA rules 15/30/54: two-part code, epiplexity, entropy vs compute (frontiers + runs)
fig4_owf_chess.json   Fig. 4a/c one-way function loss vs state size; chess forward/reverse H_T, S_T vs compute
fig5_induction.json   Fig. 5b/c induction hard/easy: loss curves vs compute and measured epiplexity bars
fig6_emergence.json   Fig. 6    emergence ECA: non-looped vs looped frontier (+ runs)
fig7_chess_ood.json   Fig. 7    chess forward vs reverse: epiplexity, puzzle accuracy, centipawn accuracy bars
fig8_natural.json     Fig. 8a/b/c  S_T and H_T bars per dataset; ADO vs natural loss curves and bars
fig9_scaling.json     Fig. 9    S_T vs compute and optimal train tokens vs compute per dataset

Drawing selection (colours, widths, panel boxes) is specific to arXiv:2601.03220v2.
"""
import json, os, sys
import numpy as np
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # projects/epiplexity
DATA = os.path.join(ROOT, 'data')
SRC = 'arXiv:2601.03220v2'
GRID = '#cccccc'

# ---------------------------------------------------------------- helpers

def hexc(c):
    return '#%02x%02x%02x' % tuple(int(round(255 * v)) for v in c[:3]) if c else None

_cache = {}
def drawings(doc, page):
    """Drawings of a 1-based page, cached."""
    if page not in _cache:
        _cache[page] = doc[page - 1].get_drawings()
    return _cache[page]

def pts(d):
    """Polyline vertices of a drawing (line/curve end points), PDF points."""
    out = []
    for it in d['items']:
        if it[0] in ('l', 'c'):
            if not out:
                out.append((it[1].x, it[1].y))
            end = it[2] if it[0] == 'l' else it[4]
            out.append((end.x, end.y))
    return np.array(out)

def centre(d):
    r = d['rect']
    return ((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2)

def inside(d, box, tol=0.5):
    r = d['rect']
    return r.x0 >= box[0] - tol and r.x1 <= box[2] + tol and r.y0 >= box[1] - tol and r.y1 <= box[3] + tol

def overlaps(d, box):
    r = d['rect']
    return not (r.x1 < box[0] or r.x0 > box[2] or r.y1 < box[1] or r.y0 > box[3])

def select(doc, page, box, stroke=None, fill=None, width=None, kind=None, min_items=1, contained=True, wtol=0.03):
    """Drawings in a panel box matching stroke colour / fill colour / line width / type."""
    out = []
    for d in drawings(doc, page):
        if (inside(d, box) if contained else overlaps(d, box)) is False:
            continue
        if stroke is not None and hexc(d.get('color')) != stroke:
            continue
        if fill is not None and hexc(d.get('fill')) != fill:
            continue
        if width is not None and abs((d.get('width') or 0) - width) > wtol:
            continue
        if kind is not None and d['type'] != kind:
            continue
        if len(d['items']) < min_items:
            continue
        out.append(d)
    return out

class Axis:
    """Page coordinate <-> data value, calibrated from gridlines and their tick values."""
    def __init__(self, positions, values, log=False, name=''):
        p = np.asarray(positions, float)
        v = np.log10(values) if log else np.asarray(values, float)
        self.a, self.b = np.polyfit(p, v, 1)
        self.log = log
        resid = np.abs(self.a * p + self.b - v).max() / (np.ptp(v) or 1)
        assert resid < 2e-3, f'{name}: ticks do not fit a {"log" if log else "linear"} axis (resid {resid:.2e})'
        # linear axes: quantize to ~1/5000 of the tick span (the vector precision), so zero reads as 0, not 37.5
        self.step = None if log else 10 ** np.floor(np.log10(np.ptp(v) / 5000))
    def __call__(self, p):
        v = self.a * np.asarray(p, float) + self.b
        return 10 ** v if self.log else np.round(v / self.step) * self.step + 0.0

def gridlines(doc, page, box):
    """Sorted x positions of vertical and y positions of horizontal gridlines spanning a panel box. The panel frame
    is drawn in the same grey but thicker, so lines of the maximum width are dropped."""
    cand = []
    for d in drawings(doc, page):
        if hexc(d.get('color')) != GRID or d.get('fill') or len(d['items']) != 1 or d['items'][0][0] != 'l':
            continue
        a, b = d['items'][0][1], d['items'][0][2]
        if abs(a.x - b.x) < 0.01 and min(a.y, b.y) <= box[1] + 1 and max(a.y, b.y) >= box[3] - 1 \
                and box[0] - 1 <= a.x <= box[2] + 1:
            cand.append(('x', a.x, d['width']))
        elif abs(a.y - b.y) < 0.01 and min(a.x, b.x) <= box[0] + 1 and max(a.x, b.x) >= box[2] - 1 \
                and box[1] - 1 <= a.y <= box[3] + 1:
            cand.append(('y', a.y, d['width']))
    wmax = max(c[2] for c in cand)
    xs = sorted({round(c[1], 3) for c in cand if c[0] == 'x' and c[2] < wmax - 1e-3})
    ys = sorted({round(c[1], 3) for c in cand if c[0] == 'y' and c[2] < wmax - 1e-3})
    return xs, ys

def axes(doc, page, box, xticks=None, yticks=None, xlog=False, ylog=False, name=''):
    """(xaxis, yaxis) for a panel; tick values are listed in increasing order, matched to gridlines left->right
    and bottom->top. Pass None for a categorical axis."""
    xs, ys = gridlines(doc, page, box)
    ax = ay = None
    if xticks is not None:
        assert len(xs) == len(xticks), f'{name}: {len(xs)} x gridlines {xs} for ticks {xticks}'
        ax = Axis(xs, xticks, xlog, name + ' x')
    if yticks is not None:
        assert len(ys) == len(yticks), f'{name}: {len(ys)} y gridlines {ys} for ticks {yticks}'
        ay = Axis(ys[::-1], yticks, ylog, name + ' y')
    return ax, ay

def sig(v, n=4):
    """Round to n significant figures (lists, nested lists, scalars)."""
    if isinstance(v, (list, tuple, np.ndarray)):
        return [sig(x, n) for x in v]
    v = float(v)
    if v == 0 or not np.isfinite(v):
        return 0.0 if v == 0 else None
    return float(f'{v:.{n}g}')

def curve(d, ax, ay, box=None, n=None):
    """Data-unit (x, y) lists of a polyline, dropping vertices outside the panel box (matplotlib clips paths near the
    figure edge, so off-axes coordinates are not data) and downsampling to about n points."""
    p = pts(d)
    if box is not None:
        keep = (p[:, 0] >= box[0] - 0.3) & (p[:, 0] <= box[2] + 0.3) & (p[:, 1] >= box[1] - 0.3) & (p[:, 1] <= box[3] + 0.3)
        p = p[keep]
    if n and len(p) > n:
        p = p[np.unique(np.linspace(0, len(p) - 1, n).round().astype(int))]
    return {'x': sig(ax(p[:, 0])), 'y': sig(ay(p[:, 1]))}

def bar_top(d):
    """Top edge of a filled bar rect (the item rect, not the stroke-padded bbox)."""
    r = d['items'][0][1]
    return r.y0, (r.x0 + r.x1) / 2

def save(name, obj):
    path = os.path.join(DATA, name)
    with open(path, 'w') as f:
        json.dump(obj, f, separators=(',', ':'))
    print(f'wrote {path} ({os.path.getsize(path) / 1024:.1f} kB)')

# ---------------------------------------------------------------- Fig. 2c (p.13)

def fig2c(doc):
    pg = 13
    panels = {   # name: (box, fill colour, x ticks, y ticks)
        'ECA':          ((411.32, 102.23, 455.42, 123.22), '#2e86ab', [0, .5, 1], [0, 2.5, 5]),
        'Induct Easy':  ((470.90, 102.23, 514.99, 123.22), '#a23b72', [.1, .5, .9], [4, 5, 6]),
        'Induct Hard':  ((411.32, 143.83, 455.42, 164.81), '#f18f01', [.5, .75, 1], [4, 5, 6]),
        'Natural':      ((470.90, 143.83, 514.99, 164.81), '#6a994e', [10, 30, 50], [10, 50, 90]),
    }
    out = {'source': f'Fig. 2c, {SRC} p.13, extracted from vector paths (marker centres)',
           'x': 'S_req: requential-coding epiplexity estimate (MB)',
           'y': 'S_preq: prequential-coding epiplexity estimate (MB)',
           'note': 'each panel has its own linear axes; points are unlabelled datasets within each group',
           'groups': {}}
    for name, (box, col, xt, yt) in panels.items():
        ax, ay = axes(doc, pg, box, xt, yt, name=f'fig2c {name}')
        dots = select(doc, pg, box, fill=col, stroke='#191919')
        c = np.array([centre(d) for d in dots])
        order = np.argsort(c[:, 0])
        out['groups'][name] = {'color': col, 'S_req_MB': sig(ax(c[order, 0]), 3), 'S_preq_MB': sig(ay(c[order, 1]), 3)}
    return out

# ---------------------------------------------------------------- Fig. 3 (p.17)

RULES = {'15': '#2ca02c', '30': '#d62728', '54': '#9467bd'}

def fig3(doc):
    pg = 17
    panels = {   # key: (box, y ticks (real units), label)
        'two_part': ((333.26, 102.32, 378.29, 169.86), [0, .2e8, .4e8, .6e8, .8e8, 1e8],
                     '|P| + E log 1/P(Y|X): total two-part code length (bits)'),
        'epiplexity': ((406.95, 102.32, 451.98, 169.86), [0, 1e6, 2e6, 3e6, 4e6, 5e6],
                       'S_T(Y|X): epiplexity (bits)'),
        'entropy': ((454.02, 102.32, 499.05, 169.86), [0, .2e8, .4e8, .6e8, .8e8, 1e8],
                    'H_T(Y|X): time-bounded entropy (bits)'),
    }
    out = {'source': f'Fig. 3 right, {SRC} p.17, extracted from vector paths',
           'x': 'compute (FLOPs), log axis', 'colors': RULES,
           'note': 'frontier = thick line through the black-edged dots (best two-part code at each compute budget); '
                   'S_T and H_T panels are evaluated at the same frontier points. runs = thin per-run curves '
                   '(only drawn in the two-part panel), downsampled; values above the top of the axes are clipped.',
           'panels': {}}
    for key, (box, yt, label) in panels.items():
        ax, ay = axes(doc, pg, box, [1e14, 1e17], yt, xlog=True, name=f'fig3 {key}')
        P = {'y_label': label, 'frontier': {}, 'runs': {}}
        for rule, col in RULES.items():
            thick = select(doc, pg, box, stroke=col, width=1.02, min_items=3)   # legend handle has 2
            assert len(thick) == 1, (key, rule, len(thick))
            fr = curve(thick[0], ax, ay)
            dots = [d for d in select(doc, pg, box, fill=col, stroke='#191919') if d['rect'].width < 2.5]
            # the legend's marker sits inside panel 1 at x=353.3: exclude by matching to frontier vertices
            fx = pts(thick[0])[:, 0]
            dots = [d for d in dots if np.abs(fx - centre(d)[0]).min() < 0.2]
            assert len(dots) == len(fx), (key, rule, len(dots), len(fx))
            P['frontier'][rule] = fr
            if key == 'two_part':
                runs = select(doc, pg, box, stroke=col, width=0.32, min_items=10)
                P['runs'][rule] = [curve(r, ax, ay, box, n=30) for r in runs]
        if not any(P['runs'].values()):
            del P['runs']
        out['panels'][key] = P
    return out

# ---------------------------------------------------------------- Fig. 4 (p.19)

def fig4(doc):
    pg = 19
    box = (123.45, 110.74, 229.51, 177.60)
    ax, ay = axes(doc, pg, box, [20, 40, 60], [0, 25, 50, 75, 100], name='fig4a')
    a = {'source': f'Fig. 4a, {SRC} p.19, extracted from vector paths',
         'x': 'n, state size (bits)', 'y': 'H_T(A|B) + H_T(B): loss of the model (bits)',
         'note': 'ECA rule 30 one-way function, 8 steps. Entropy = Shannon entropy (grey band, = n), Random Guess '
                 '(red band lower edge, = 2n).',
         'series': {}}
    for name, col in (('forward', '#808000'), ('reverse', '#800080')):
        d = select(doc, pg, box, stroke=col, width=0.95, min_items=3)
        assert len(d) == 1
        a['series'][name] = curve(d[0], ax, ay) | {'color': col}
    grey = select(doc, pg, box, fill='#808080', contained=False)[0]
    p = pts(grey)
    p = p[p[:, 1] < box[3] - 0.01]                          # top edge of the band only
    p = p[np.unique(p[:, 0].round(2), return_index=True)[1]]
    a['series']['entropy'] = {'x': sig(ax(p[:, 0])), 'y': sig(ay(p[:, 1])), 'color': '#808080'}
    red = select(doc, pg, box, fill='#8b0000', contained=False)[0]
    p = pts(red)
    p = p[(p[:, 1] > box[1] - 20) & (p[:, 1] < box[3])]     # lower edge; its far top edge (y=-380) is not data
    p = p[np.unique(p[:, 0].round(2), return_index=True)[1]]
    a['series']['random_guess'] = {'x': sig(ax(p[:, 0])), 'y': sig(ay(p[:, 1])), 'color': '#8b0000'}

    c = {'source': f'Fig. 4c, {SRC} p.19, extracted from vector paths',
         'x': 'compute (FLOPs), log axis', 'colors': {'forward': '#2ca02c', 'reverse': '#9467bd'},
         'note': 'Forward = moves then final board (FEN); Reverse = board then moves. Lines through the dots.',
         'panels': {}}
    for key, box, yt, label in (
            ('entropy', (393.59, 111.15, 443.25, 183.44), [4e9, 5e9, 6e9, 7e9, 8e9], 'H_T(X): time-bounded entropy (bits)'),
            ('epiplexity', (448.22, 111.15, 497.88, 183.44), [.5e8, 1e8, 1.5e8, 2e8, 2.5e8], 'S_T(X): epiplexity (bits)')):
        ax, ay = axes(doc, pg, box, [1e16, 1e18], yt, xlog=True, name=f'fig4c {key}')
        P = {'y_label': label}
        for name, col in c['colors'].items():
            d = select(doc, pg, box, stroke=col, width=1.09, min_items=3)
            assert len(d) == 1
            P[name] = curve(d[0], ax, ay)
        c['panels'][key] = P
    return {'fig4a_owf': a, 'fig4c_chess': c}

# ---------------------------------------------------------------- Fig. 5 (p.20)

def fig5(doc):
    pg = 20
    # (b) hard induction
    box = (260.77, 100.96, 332.33, 160.46)
    ax, ay = axes(doc, pg, box, [1e14, 1e15, 1e16], [1, 10], xlog=True, ylog=True, name='fig5b loss')
    cols = ['#280b53', '#65156e', '#9f2a63', '#d44842', '#f57d15', '#fac228']   # h = 0..5 (legend order)
    b = {'source': f'Fig. 5b, {SRC} p.20, extracted from vector paths',
         'loss': {'x': 'compute (FLOPs), log axis', 'y': 'train loss (bits), log axis',
                  'note': 'curves clipped to the axes (h=0 falls below 10^-0.3 bits at the end); dashed level = '
                          'h bits, the loss the text says training converges to',
                  'curves': {}},
         'epiplexity': {'x': 'hidden bits h', 'y': 'measured epiplexity (bits)', 'h': [], 'value': []}}
    for h, col in enumerate(cols):
        d = select(doc, pg, box, stroke=col, width=0.36, min_items=10, contained=False)
        assert len(d) == 1
        cv = curve(d[0], ax, ay, box, n=120) | {'color': col}
        lvl = [x for x in select(doc, pg, box, stroke=col, width=0.36, contained=False) if x.get('dashes', '').startswith('[ 1.3')]
        if lvl:
            cv['dashed_level'] = sig(ay(pts(lvl[0])[0, 1]))
        b['loss']['curves'][f'h={h}'] = cv
    bbox = (337.00, 100.96, 354.89, 160.46)
    _, ay = axes(doc, pg, bbox, None, [0, 1e6, 2e6, 3e6, 4e6, 5e6], name='fig5b bars')   # "x10^6" is a glyph path
    for h, col in enumerate(cols):
        d = select(doc, pg, (bbox[0], 0, bbox[2], 1e9), fill=col, kind='fs', contained=False)
        d = [x for x in d if x['items'][0][0] == 're']
        assert len(d) == 1
        b['epiplexity']['h'].append(h)
        b['epiplexity']['value'].append(sig(ay(bar_top(d[0])[0])))
    # (c) easy induction
    box = (396.70, 101.18, 467.86, 162.88)
    ax, ay = axes(doc, pg, box, [1e13, 1e14, 1e15], [1300, 1400, 1500, 1600], xlog=True, ylog=True, name='fig5c loss')
    cols = {0: '#320a5e', 2: '#781c6d', 4: '#bc3754', 6: '#ed6925', 8: '#fbb61a'}
    c = {'source': f'Fig. 5c, {SRC} p.20, extracted from vector paths',
         'loss': {'x': 'compute (FLOPs), log axis', 'y': 'train loss (bits; ~1.3e3, so presumably per 512-token sequence, inferred), log axis (ticks 1.3-1.6 x10^3)',
                  'note': 'dashed = loss achievable with the provided rows plus a unigram strategy; dotted = '
                          'theoretical loss using both the provided rows and in-context induction (text, Sec. 5.3.1)',
                  'curves': {}},
         'epiplexity': {'x': 'hidden rows h', 'y': 'measured epiplexity (bits)', 'h': [], 'value': []}}
    for h, col in cols.items():
        d = select(doc, pg, box, stroke=col, width=0.37, min_items=10, contained=False)
        assert len(d) == 1
        cv = curve(d[0], ax, ay, box, n=120) | {'color': col}
        for x in select(doc, pg, box, stroke=col, width=0.37, contained=False):
            if len(x['items']) == 1:
                kind = 'dashed_level' if x['dashes'].startswith('[ 1.38') else 'dotted_level'
                cv[kind] = sig(ay(pts(x)[0, 1]))
        c['loss']['curves'][f'h={h}'] = cv
    bbox = (472.72, 101.18, 496.43, 162.88)
    _, ay = axes(doc, pg, bbox, None, [0, 1e6, 2e6, 3e6, 4e6], name='fig5c bars')
    for h, col in cols.items():
        d = [x for x in select(doc, pg, bbox, fill=col, kind='fs') if x['items'][0][0] == 're']
        assert len(d) == 1
        c['epiplexity']['h'].append(h)
        c['epiplexity']['value'].append(sig(ay(bar_top(d[0])[0])))
    return {'fig5b_hard': b, 'fig5c_easy': c}

# ---------------------------------------------------------------- Fig. 6 (p.23)

def fig6(doc):
    pg = 23
    cols = {'non-looped': '#7e03a8', 'looped': '#f89540'}
    out = {'source': f'Fig. 6, {SRC} p.23, extracted from vector paths',
           'x': 'compute (FLOPs), log axis', 'colors': cols,
           'note': 'frontier = best two-part code over both model families at each compute; "model" says which '
                   'family each frontier point comes from (dot colour). ECA rule 54, iterated dynamics. runs = thin '
                   'per-run curves (two-part panel only), downsampled; points above the axes top are dropped.',
           'panels': {}}
    for key, box, yt, label in (
            ('two_part', (401.01, 271.72, 446.25, 340.52), [0, .25e9, .5e9, .75e9, 1e9], '|P| + E log 1/P(X) (bits)'),
            ('epiplexity', (450.77, 271.72, 496.01, 340.52), [0, .5e7, 1e7, 1.5e7], 'S_T(X): epiplexity (bits)')):
        ax, ay = axes(doc, pg, box, [1e15, 1e17], yt, xlog=True, name=f'fig6 {key}')
        dots = []
        for model, col in cols.items():
            for d in select(doc, pg, box, fill=col, stroke='#191919', contained=False):
                cx, cy = centre(d)
                if box[0] <= cx <= box[2] and box[1] <= cy <= box[3]:     # markers poke out of the frame
                    dots.append((cx, cy, model))
        dots.sort()
        segs = [pts(d) for col in cols.values() for d in select(doc, pg, box, stroke=col, width=1.17)]
        verts = np.unique(np.round(np.vstack(segs), 2), axis=0)
        assert len(verts) == len(dots), (key, len(verts), len(dots))
        xy = np.array([d[:2] for d in dots])
        P = {'y_label': label, 'frontier': {'x': sig(ax(xy[:, 0])), 'y': sig(ay(xy[:, 1])), 'model': [d[2] for d in dots]}}
        if key == 'two_part':
            P['runs'] = {m: [curve(r, ax, ay, box, n=30) for r in select(doc, pg, box, stroke=col, width=0.37, min_items=10, contained=False)]
                         for m, col in cols.items()}
        out['panels'][key] = P
    return out

# ---------------------------------------------------------------- Fig. 7 (p.24)

def fig7(doc):
    pg = 24
    cols = {'forward': '#1b9e77', 'reverse': '#7570b3'}
    out = {'source': f'Fig. 7, {SRC} p.24, extracted from vector paths (filled bar rects)',
           'note': 'models pre-trained on forward (moves then board) or reverse (board then moves) chess ordering, '
                   'then fine-tuned; Puzzle Acc = chess puzzles, CP Acc = centipawn evaluation accuracy',
           'units': {'epiplexity': 'bits', 'puzzle_acc': 'fraction', 'cp_acc': 'fraction'}, 'bars': {}}
    for key, box, yt in (('epiplexity', (404.64, 398.65, 432.08, 464.07), [0, .5e8, 1e8, 1.5e8, 2e8, 2.5e8]),
                         ('puzzle_acc', (448.54, 398.65, 475.98, 464.07), [0, .1, .2, .3]),
                         ('cp_acc', (492.44, 398.65, 519.87, 464.07), [0, .1, .2, .3])):
        _, ay = axes(doc, pg, box, None, yt, name=f'fig7 {key}')
        out['bars'][key] = {}
        for name, col in cols.items():
            d = select(doc, pg, box, fill=col, stroke='#191919')
            assert len(d) == 1
            out['bars'][key][name] = sig(ay(bar_top(d[0])[0]))
    return out

# ---------------------------------------------------------------- Fig. 8 (p.25)

def stacked_bars(doc, pg, box, ay, names):
    """Solid S_T bars and the hatched H_T bars stacked on them (stroke-only outline rects whose bottom is an S_T top).
    On the log axis the hatched bar's top is S_T + H_T."""
    solid = sorted([d for d in drawings(doc, pg) if d['type'] == 'fs' and hexc(d.get('color')) == '#000000'
                    and d['items'][0][0] == 're' and box[0] <= d['items'][0][1].x0 <= box[2]
                    and d['items'][0][1].y1 > box[3] + 100], key=lambda d: d['items'][0][1].x0)
    outline = [d for d in drawings(doc, pg) if d['type'] == 's' and len(d['items']) == 1 and d['items'][0][0] == 're'
               and d.get('stroke_opacity', 1) < 0.5 and box[0] <= d['items'][0][1].x0 <= box[2]]
    assert len(solid) == len(names), (len(solid), names)
    out = {}
    for name, d in zip(names, solid):
        r = d['items'][0][1]
        h = [o for o in outline if abs(o['items'][0][1].x0 - r.x0) < .05 and abs(o['items'][0][1].y1 - r.y0) < .05]
        assert len(h) == 1, name
        S, tot = float(ay(r.y0)), float(ay(h[0]['items'][0][1].y0))
        out[name] = {'S_T': sig(S), 'S_T_plus_H_T': sig(tot), 'H_T': sig(tot - S), 'color': hexc(d['fill'])}
    return out

def fig8(doc):
    pg = 25
    box = (116.01, 102.14, 207.99, 152.79)
    _, ay = axes(doc, pg, box, None, [1e8, 1e9, 1e10], ylog=True, name='fig8a')
    a = {'source': f'Fig. 8a, {SRC} p.25, extracted from vector paths',
         'y': 'information (bits), log axis',
         'note': 'requential coding at 6e18 FLOPs. Solid bar = S_T; hatched bar is stacked on it, so its top is '
                 'S_T + H_T and H_T = top - S_T (assumes matplotlib bar(H, bottom=S)). Caption says 1B tokens; Sec. 6.2 '
                 'text says 5B. The bars favour 5B: CIFAR-5M (256 grey levels, max 8 bits/token) totals 2.33e10 bits '
                 '= 23 bits/token at 1B but 4.7 at 5B; OWText (96 chars, max 6.6 bits/char) 7.3 at 1B vs 1.5 at 5B.',
         'bars': stacked_bars(doc, pg, box, ay, ['OWText', 'Chess (R)', 'Chess', 'CIFAR-5M'])}
    box = (244.38, 100.73, 339.64, 147.23)
    _, ay = axes(doc, pg, box, None, [1e10, 1e12], ylog=True, name='fig8b')
    b = {'source': f'Fig. 8b, {SRC} p.25, extracted from vector paths',
         'y': 'information (bits), log axis',
         'note': 'estimated from scaling laws + prequential coding for 1T (1e12) tokens at 1e25 FLOPs. Solid = S_T, '
                 'hatched stacked on top (top = S_T + H_T). Colours differ from Fig. 9. Each S_T bar equals Fig. 9\'s dashed '
                 'S_inf x 1.443 (= 1/ln 2) to 0.1%, so these look like the S_inf limit in bits, not S_T at 1e25 FLOPs '
                 '(Fig. 9 curves at 1e25 sit 3-12% below S_inf), and Fig. 9 looks like it is in nats.',
         'bars': stacked_bars(doc, pg, box, ay, ['Language', 'Img VQ 32^2', 'Img VQ 16^2', 'Vid VQ 16^3',
                                                 'Img 32^2', 'Img 16^2', 'Img 8^2'])}
    cols = {'ADO': '#7f05a9', 'Natural': '#f89643'}
    c = {'source': f'Fig. 8c, {SRC} p.25, extracted from vector paths', 'colors': cols,
         'note': 'ADO = data selected by ADO (Jiang et al. 2025); Natural = standard sampling. Bars, not points. '
                 'Perplexity 1/2 are OOD perplexities on two text corpora (lower is better).',
         'loss': {'x': 'training step', 'y': 'training loss (units unlabelled)'},
         'bars': {}}
    box = (364.94, 95.18, 413.99, 150.14)
    ax, ay = axes(doc, pg, box, [0, 2.5e4, 5e4], [2.0, 2.2, 2.4, 2.6, 2.8], name='fig8c loss')
    for name, col in cols.items():
        d = select(doc, pg, box, stroke=col, width=0.62, min_items=10)
        assert len(d) == 1
        c['loss'][name] = curve(d[0], ax, ay, box)
    for key, box, yt in (('epiplexity_bits', (426.61, 95.18, 440.63, 150.14), [.5e10, 1e10, 1.5e10, 2e10, 2.5e10]),
                         ('accuracy', (453.24, 95.18, 467.26, 150.14), [.55, .56, .57, .58, .59, .60]),
                         ('perplexity_1', (479.87, 95.18, 493.89, 150.14), [12.0, 12.1, 12.2, 12.3]),
                         ('perplexity_2', (506.50, 95.18, 520.52, 150.14), [13, 13.5, 14, 14.5, 15, 15.5, 16])):
        _, ay = axes(doc, pg, box, None, yt, name=f'fig8c {key}')
        c['bars'][key] = {}
        for name, col in cols.items():
            d = [x for x in select(doc, pg, (box[0], 0, box[2], 1e5), fill=col, stroke='#191919', contained=False)
                 if box[0] <= x['items'][0][1].x0 <= box[2]]
            assert len(d) == 1, key
            c['bars'][key][name] = sig(ay(bar_top(d[0])[0]))
    return {'fig8a_requential': a, 'fig8b_scaling': b, 'fig8c_ado': c}

# ---------------------------------------------------------------- Fig. 9 (p.25)

def fig9(doc):
    pg = 25
    cols = {'Language': '#666666', 'Img VQ 32^2': '#66a61e', 'Img VQ 16^2': '#e7298a', 'Vid VQ 16^3': '#e6ab02',
            'Img 32^2': '#7570b3', 'Img 16^2': '#d95f02', 'Img 8^2': '#1b9e77'}     # from the legend handles
    out = {'source': f'Fig. 9, {SRC} p.25, extracted from vector paths', 'colors': cols,
           'x': 'compute (FLOPs), log axis',
           'units_warning': 'y units unlabelled; S_inf here x 1/ln 2 equals the Fig. 8b bits bars to 0.1%, so the '
                            'epiplexity axis is most likely nats (Table 1 scaling-law E is in nats)',
           'note': 'fixed dataset of D = 1e12 tokens; curves from fitted scaling laws. Dashed lines: S_inf(X) '
                   '(left, compute -> infinity limit of epiplexity) and D (right).',
           'panels': {}}
    for key, box, yt, label in (
            ('epiplexity', (376.82, 508.40, 431.60, 582.36), [1e9, 1e10, 1e11], 'S_T(X): epiplexity (unlabelled; likely nats, see units_warning), log axis'),
            ('optimal_tokens', (439.82, 508.40, 494.60, 582.36), [1e11, 1e12], 'optimal train tokens D*, log axis')):
        ax, ay = axes(doc, pg, box, [1e22, 1e28], yt, xlog=True, ylog=True, name=f'fig9 {key}')
        P = {'y_label': label, 'curves': {}}
        for name, col in cols.items():
            d = select(doc, pg, box, stroke=col, width=0.88, min_items=10)
            assert len(d) == 1, (key, name)
            cv = curve(d[0], ax, ay, box, n=60)
            lim = [x for x in select(doc, pg, box, stroke=col, width=0.53) if len(x['items']) == 1]
            assert len(lim) == 1
            cv['dashed_limit'] = sig(ay(pts(lim[0])[0, 1]))
            P['curves'][name] = cv
        out['panels'][key] = P
    return out

# ---------------------------------------------------------------- main

if __name__ == '__main__':
    doc = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'paper', 'paper.pdf'))
    os.makedirs(DATA, exist_ok=True)
    save('fig2c_preq_req.json', fig2c(doc))
    save('fig3_eca.json', fig3(doc))
    save('fig4_owf_chess.json', fig4(doc))
    save('fig5_induction.json', fig5(doc))
    save('fig6_emergence.json', fig6(doc))
    save('fig7_chess_ood.json', fig7(doc))
    save('fig8_natural.json', fig8(doc))
    save('fig9_scaling.json', fig9(doc))
