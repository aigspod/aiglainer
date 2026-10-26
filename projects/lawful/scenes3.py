"""Circuits, results, mechanism, limits, discussion, end."""
import math
import numpy as np
import skia
from explainer.core import *
from explainer.kit import *
from explainer.timeline import Scene
from scenes2 import fig4
from scenes1 import rasters

S_HEADS = [f'S.h{i}' for i in range(8)]
T_HEADS = [f'T.h{i}' for i in range(8)]
COMPS = S_HEADS + ['S.MLP'] + T_HEADS + ['T.MLP']
CDAG = {'T.MLP', 'T.h0', 'T.h1', 'T.h2', 'T.h4', 'T.h6', 'T.h7', 'S.MLP', 'S.h4'}
TABLE1 = [  # tau label, tau, circuit, dsuf, dnec, rsuf, rnec
    ('0.3–0.5', 0.5, ['T.MLP', 'T.h6', 'T.h7'], 0.49, 1.89, 1.82, 1.11),
    ('0.6', 0.6, ['T.MLP', 'T.h1', 'T.h6', 'T.h7'], 0.35, 2.43, 2.11, 1.29),
    ('0.7', 0.7, ['T.MLP', 'T.h1', 'T.h6', 'T.h7', 'S.MLP'], 0.24, 3.08, 2.39, 2.17),
    ('0.8', 0.8, ['T.MLP', 'T.h1', 'T.h4', 'T.h6', 'T.h7', 'S.MLP'], 0.18, 3.19, 2.52, 2.03),
    ('0.9', 0.9, ['T.MLP', 'T.h0', 'T.h1', 'T.h2', 'T.h4', 'T.h6', 'T.h7', 'S.MLP', 'S.h4'], 0.09, 3.50, 3.05, 3.23),
]
M0 = 0.988

def chip(c, x, y, w, h, label, on, a=1.0, glow_k=0.0, base='panel2', size=17):
    if a <= 0:
        return
    if on > 0:
        rrect(c, x, y, w, h, 7, fill=mix(base, PAL['c'], on), a=a, fa=a, glow=10 * glow_k)
    else:
        rrect(c, x, y, w, h, 7, fill=base, a=a)
    rrect(c, x, y, w, h, 7, stroke=mix('faint', PAL['c'], on), sw=1.4, a=a)
    text(c, label, x + w / 2, y + h / 2 + size * 0.36, size, 650 if on > 0.5 else 500, mix('muted', '#1A0E05', on), a, 'center', kind='mono')

def arch(c, x0, y0, a, on, t=0.0, flow=0.0):
    """Fig. 2 re-drawn. on: dict comp -> highlight 0..1. Draws in a 1180x470 box at (x0,y0)."""
    if a <= 0:
        return
    Y = y0 + 430
    with layer(c, a):
        line(c, x0 + 70, Y, x0 + 1140, Y, 'muted', 0.8, 2.5)
        text(c, 'MoCap', x0, Y + 7, 20, 600, 'ink', 1, kind='mono')
        text(c, 'Radar', x0 + 1150, Y + 7, 20, 600, 'ink', 1, kind='mono')
        chip(c, x0 + 90, Y - 15, 90, 30, 'S.Proj', 0, size=15)
        chip(c, x0 + 600, Y - 15, 90, 30, 'T.Proj', 0, size=15)
        chip(c, x0 + 1010, Y - 15, 110, 30, 'MLP head', 0, size=15)
        for bx, heads, mlp, title in ((x0 + 200, S_HEADS, 'S.MLP', 'Spatial transformer'), (x0 + 710, T_HEADS, 'T.MLP', 'Temporal transformer')):
            rrect(c, bx, y0, 380, 470, 22, stroke='line', sw=1.5, a=1)
            text(c, title, bx + 190, y0 - 14, 20, 600, 'muted', 1, 'center')
            hx, hy = bx + 34, y0 + 26
            rrect(c, hx - 12, hy - 12, 134, 8 * 38 + 18, 12, fill='panel', a=0.8)
            for i, hname in enumerate(heads):
                chip(c, hx, hy + i * 38, 110, 30, hname, on.get(hname, 0), 1, on.get(hname, 0))
            # attn -> residual
            ax = hx + 128
            line(c, ax, hy + 4 * 38, ax + 30, hy + 4 * 38, 'muted', 0.6, 1.5)
            line(c, ax + 30, hy + 4 * 38, ax + 30, Y - 12, 'muted', 0.6, 1.5)
            circle(c, ax + 30, Y, 11, stroke='muted', sw=1.6, a=0.9)
            text(c, '+', ax + 30, Y + 6, 18, 600, 'muted', 1, 'center')
            mx_ = bx + 236
            chip(c, mx_, y0 + 230, 120, 36, mlp, on.get(mlp, 0), 1, on.get(mlp, 0), size=17)
            line(c, mx_ + 60, y0 + 266, mx_ + 60, Y - 12, 'muted', 0.6, 1.5)
            circle(c, mx_ + 60, Y, 11, stroke='muted', sw=1.6, a=0.9)
            text(c, '+', mx_ + 60, Y + 6, 18, 600, 'muted', 1, 'center')
        if flow > 0:
            flow_dots(c, np.array([[x0 + 70, Y], [x0 + 1140, Y]]), t, 'y', flow, 4, 0.25, 4)

# ======================================================================= PATCHING
class Patching(Scene):
    dur = 35.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (2.4, 'pop'), (6.0, 'sweep'), (14.5, 'sweep'), (23.0, 'pop'), (27.5, 'pop')]

    def node_xy(self, i, y):
        x0 = 520
        gx = 0 if i < 9 else 70
        return x0 + i * 52 + gx, y

    def draw(self, c, t):
        header(c, t, '05', 'Circuits', 'Step 2: which parts *cause* it?')
        rows_a = 1 - ramp(t, 22.4, 0.7, e_io)
        rows = [(370, 'clean run on x', 'ink', 1.0), (520, 'counterfactual run on x′', 'x', 2.4), (720, 'patched run', 'y', 6.0)]
        mode = 'suf' if t < 14.5 else 'nec'
        swap = ramp(t, 14.5, 0.6, e_io)
        with layer(c, rows_a):
            for ri, (y, lab, colr, t0) in enumerate(rows):
                k = ramp(t, t0, 0.8, e_expo)
                if k <= 0:
                    continue
                text(c, lab, 480, y + 8, 24, 600, colr if ri else 'ink', k, 'right')
                for i, comp in enumerate(COMPS):
                    x, yy = self.node_xy(i, y)
                    kk = ramp(t, t0 + i * 0.03, 0.5, e_back)
                    if ri == 0:
                        circle(c, x, yy, 15 * kk, fill='faint', a=k)
                    elif ri == 1:
                        circle(c, x, yy, 15 * kk, fill='x', a=k * 0.9)
                    else:
                        inC = comp in CDAG
                        patched = inC if mode == 'suf' else (not inC)
                        if t < 14.5:
                            p = ramp(t, 7.5 + i * 0.05, 0.6) if patched else 0
                        else:
                            p_old = 1 if inC else 0
                            p_new = ramp(t, 15.4 + i * 0.05, 0.6) if patched else 0
                            p = max(p_old * (1 - swap), p_new)
                        circle(c, x, yy, 15 * kk, fill=mix('faint', PAL['x'], p), a=k)
                        if inC:
                            circle(c, x, yy, 21, stroke='c', sw=2.2, a=k * ramp(t, 6.6, 0.6))
                    if ri == 0 and i in (0, 9):
                        text(c, 'spatial  ·  9' if i == 0 else 'temporal  ·  9', x - 15, y - 34, 17, 500, 'muted', k, kind='mono')
            # drops from source row
            kd = ramp(t, 7.0, 0.6) if t < 14.5 else ramp(t, 15.0, 0.6)
            if kd > 0:
                for i, comp in enumerate(COMPS):
                    inC = comp in CDAG
                    patched = inC if mode == 'suf' else (not inC)
                    if not patched:
                        continue
                    x, _ = self.node_xy(i, 0)
                    tt0 = (7.2 if mode == 'suf' else 15.2) + i * 0.05
                    u = clamp((t - tt0) / 0.7)
                    if 0 < u < 1:
                        yy = lerp(540, 700, e_io(u))
                        circle(c, x, yy, 6, fill='x', a=(1 - u) * 0.9 + 0.1, glow=8)
                    line(c, x, 540, x, 700, 'x', 0.18 * kd, 1.5, dash=[3, 5])
            kc = ramp(t, 6.6, 0.6)
            text(c, 'C', 1520, 728, 30, 700, 'c', kc, kind='italic')
            text(c, '= an example circuit', 1546, 728, 22, 500, 'c', kc)
        # right-side explanations
        ks = window(t, 7.0, 14.2, 0.6, 0.4)
        if ks > 0:
            kicker(c, 'sufficiency', MX, 860, ks, 'y', 20)
            tex(c, 'suf', MX + 270, 852, 40, ks)
            rich(c, 'Route the perturbation through {c:C alone}. Does f still respond the way it does to the full perturbation?', 560, 862, 30, 1250, t, 7.4, 0.03, 0.45, ks)
        kn = window(t, 15.0, 22.2, 0.6, 0.4)
        if kn > 0:
            kicker(c, 'necessity', MX, 860, kn, 'y', 20)
            tex(c, 'nec', MX + 285, 852, 40, kn)
            rich(c, 'Route it through {w:everything except C}. Does the response survive without C?', 560, 862, 30, 1250, t, 15.4, 0.03, 0.45, kn)
        # tau definition
        k1 = ramp(t, 23.0, 0.9, e_expo)
        if k1 > 0:
            with layer(c, k1):
                tex(c, 'dsuf', 560, 420, 40, 1)
                tex(c, 'dnec', 1360, 420, 40, 1)
                rich(c, 'Each Δ is the drop in consistency from the unpatched M₀ when that configuration is used.', W / 2, 520, 28, 1500, t, 23.6, 0.02, 0.4, 1, 'center', base='muted')
        k2 = ramp(t, 27.5, 0.9, e_expo)
        if k2 > 0:
            with layer(c, k2):
                rrect(c, MX, 600, 1680, 300, 18, fill='y', fa=0.06)
                rrect(c, MX, 600, 1680, 300, 18, stroke='y', sw=1.4, a=0.5)
                kicker(c, 'τ-consistent circuit', MX + 40, 650, 1, 'y', 20)
                tex(c, 'tau', W / 2, 715, 46, 1)
                rich(c, '{w:C alone recovers at least τ·M₀,}   and   {w:without C, at most (1−τ)·M₀ remains.}', W / 2, 800, 30, 1600, t, 28.4, 0.03, 0.4, 1, 'center', base='muted')
                rich(c, 'A τ-physically consistent circuit is a minimal one: no single component can be dropped.', W / 2, 860, 26, 1600, t, 30.0, 0.02, 0.4, 1, 'center', base='muted')

# ======================================================================= SEARCH
class Search(Scene):
    dur = 35.0
    chapter = 4
    STEPS = [5.0, 9.0, 12.0, 15.0, 18.0]
    cues = [(0.2, 'whoosh'), (1.0, 'pop')] + [(s, 'blip') for s in [5.0, 9.0, 12.0, 15.0, 18.0]] + [(22.5, 'impact_soft'), (29.0, 'tick')]

    def state(self, t):
        idx = -1
        for i, s in enumerate(self.STEPS):
            if t >= s:
                idx = i
        return idx

    def draw(self, c, t):
        header(c, t, '05', 'Circuits', 'Growing a *circuit*', sub='Add the component that helps sufficiency most, until the τ test passes; then prune.')
        idx = self.state(t)
        on = {}
        for i in range(idx + 1):
            for comp in TABLE1[i][2]:
                if comp not in on:
                    on[comp] = ramp(t, self.STEPS[i], 0.6, e_back)
        ka = ramp(t, 1.0, 1.0, e_expo)
        arch_a = ka * (1 - 0.0 * ramp(t, 22.0, 0.6))
        with xform(c, 0, 0, 0.86, 0, 120, 350):
            arch(c, 120, 350, arch_a, on, t, flow=ramp(t, 2.0, 1.0) * 0.6)
        # readouts
        rx = 1210
        kr = ramp(t, 4.0, 0.8)
        if kr > 0 and idx >= 0:
            row = TABLE1[idx]
            tau = row[1]
            with layer(c, kr):
                text(c, 'τ', rx, 395, 46, 600, 'y', 1, kind='italic')
                text(c, row[0], rx + 40, 395, 46, 760, 'y', 1)
                text(c, f'|C| = {len(row[2])}', W - MX, 395, 34, 700, 'c', 1, 'right')
                text(c, 'of 18', W - MX, 425, 18, 500, 'muted', 1, 'right', kind='mono')
                # bars
                scale = 100.0  # px per unit
                bx = rx + 120
                def bar(y, lab, val, rval, thr, thr_lab, colr, good_low):
                    text(c, lab, rx, y + 8, 22, 600, 'ink', 1, kind='italic')
                    line(c, bx, y, bx + 4 * scale, y, 'line', 1, 14, cap='butt')
                    vv = val * ramp(t, self.STEPS[idx], 0.7)
                    line(c, bx, y, bx + vv * scale, y, colr, 1, 14, cap='butt')
                    line(c, bx, y + 16, bx + rval * scale, y + 16, 'muted', 0.55, 5, cap='butt')
                    X = bx + thr * scale
                    line(c, X, y - 16, X, y + 22, 'y', 1, 2.5)
                    text(c, f'{val:.2f}', W - MX, y + 8, 22, 600, colr, 1, 'right', kind='mono')
                    text(c, thr_lab, X, y - 24, 18, 600, 'y', 1, 'center')
                bar(500, 'Δsuf', row[3], row[5], (1 - tau) * M0, '(1−τ)M₀', 'c', True)
                bar(600, 'Δnec', row[4], row[6], tau * M0, 'τM₀', 'f', False)
                line(c, rx, 680, rx + 40, 680, 'muted', 0.55, 5, cap='butt')
                text(c, 'random-source control', rx + 52, 686, 18, 500, 'muted', 1, kind='mono')
                if t < 29:
                    text(c, 'pass:  Δsuf left of its line,  Δnec right of its line', rx, 730, 19, 500, 'ink', 0.9 * (1 - ramp(t, 28.4, 0.5)))
        # final stats
        kf = ramp(t, 22.5, 0.9, e_expo)
        if kf > 0:
            with layer(c, kf):
                rrect(c, MX, 840, 1680, 150, 18, fill='c', fa=0.08)
                rrect(c, MX, 840, 1680, 150, 18, stroke='c', sw=1.4, a=0.6)
                stat(c, MX + 40, 925, '9 / 18', 'components in C†', 'c', 1, 64, k=kf)
                stat(c, MX + 400, 925, '91%', 'of M₀ recovered (Δsuf = 0.09)', 'y', 1, 64, k=kf)
                stat(c, MX + 860, 925, '7 of 9', 'in the temporal block', 'c', 1, 64, k=kf)
                tex(c, 'cdag', MX + 1450, 890, 22, 1)
                note(c, 'core at τ ≤ 0.5:  T.{MLP, h6, h7}', MX + 1450, 955, 0.9, 17, 'muted', 'center')
        kc = ramp(t, 29.0, 0.8)
        if kc > 0:
            rich(c, 'Random-source controls do worse at every size: the effect depends on the {y:matched counterfactual}, not just on which components are patched.',
                 rx, 762, 21, 590, t, 29.0, 0.02, 0.4, kc, base='muted')

# ======================================================================= SPECTROGRAMS
class Spectrograms(Scene):
    dur = 21.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (1.4, 'pop'), (3.0, 'pop'), (3.4, 'pop'), (3.8, 'pop'), (5.5, 'sweep'), (11.0, 'tick'), (14.5, 'tick')]
    PANELS = [('gt', 'Radar GT', None), ('model', 'Model  f(x)', 'model'),
              ('cf_model', 'Model  f(x′)', 'cf_model'), ('cf_circuit', 'Circuit C†', 'cf_circuit'), ('cf_complement', 'Complement', 'cf_complement')]

    def __init__(self):
        r = rasters()
        self.ims = {k: array_image(np.array(v, float) / 255.0) for k, v in r['spec'].items()}
        self.cent = {k: np.array(v) for k, v in r['cent'].items()}

    def draw(self, c, t):
        header(c, t, '06', 'Results', 'The circuit *reproduces* the what-if')
        size, y0 = 300, 410
        xs = [MX, MX + 330, MX + 720, MX + 1050, MX + 1380]
        for j, (key, title, ck) in enumerate(self.PANELS):
            t0 = 1.0 + j * 0.4 + (1.2 if j >= 2 else 0)
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            x = xs[j]
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    draw_image(c, self.ims[key], x, y0, size, size, 1)
                    border = 'line'
                    if key == 'cf_circuit': border = 'c'
                    rrect(c, x, y0, size, size, 4, stroke=border, sw=2 if border != 'line' else 1.2)
                    text(c, title, x + size / 2, y0 - 18, 26, 650, 'c' if key == 'cf_circuit' else 'ink', 1, 'center')
                    if ck:
                        pts = self.cent[ck].copy()
                        P = np.stack([x + pts[:, 0] * size, y0 + pts[:, 1] * size], 1)
                        draw_poly(c, P, 'y', 1, 3, prog=ramp(t, 5.5, 2.5, e_io), dash=[9, 6])
                    for tk, lab in ((0, '0'), (0.5, '15'), (1, '30 s')):
                        text(c, lab, x + tk * size, y0 + size + 28, 16, 500, 'muted', 0.9, 'center' if tk != 1 else 'right', kind='mono')
        kg = ramp(t, 0.8, 0.8)
        text(c, 'unperturbed', xs[0], y0 - 70, 18, 400, 'muted', kg, kind='mono', tracking=0.16)
        line(c, xs[0], y0 - 58, xs[1] + size, y0 - 58, 'line', kg, 1.5)
        kg2 = ramp(t, 2.8, 0.8)
        text(c, 'counterfactual  α = 0.3  ·  patching', xs[2], y0 - 70, 18, 400, 'x', kg2, kind='mono', tracking=0.16)
        line(c, xs[2], y0 - 58, xs[4] + size, y0 - 58, 'x', kg2 * 0.6, 1.5)
        text(c, '±128 Hz', xs[0] - 12, y0 + 18, 15, 500, 'muted', kg, 'right', kind='mono')
        kl = ramp(t, 6.0, 0.6)
        legend_item(c, xs[0], y0 + size + 76, 'y', 'Doppler centroid (output bridge Df)', kl, dash=True, size=21)
        note(c, 'data from Fig. 3 · 30 s RandomWalk clip', xs[4] + size, y0 + size + 76, kl * 0.8, 16, align='right')
        # callouts
        k1 = ramp(t, 11.0, 0.7)
        if k1 > 0:
            pill(c, xs[3] + size / 2, y0 + size + 110, 'compressed, like f(x′)  ✓', 'f', k1, cx=True, size=17)
        k2 = ramp(t, 14.5, 0.7)
        if k2 > 0:
            pill(c, xs[4] + size / 2, y0 + size + 110, 'original amplitude  ✗', 'r', k2, cx=True, size=17)
        caption(c, t, 'Scaling radial velocity to 30% shrinks the centroid swings. Patching only {c:C†} reproduces that compression; patching the complement does not.',
                8.0, None, y=975, size=29, maxw=1650)

# ======================================================================= FIG 4a
class Fig4a(Scene):
    dur = 33.5
    chapter = 5
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (2.4, 'sweep'), (4.2, 'draw'), (8.0, 'draw'), (12.5, 'draw'), (17.0, 'draw'), (21.5, 'tick'), (27.0, 'tick')]
    CALL = [
        (4.2, '{g:g}, the physics model: the response the Doppler law demands at each α.'),
        (8.0, '{f:f} tracks g across the radar-resolvable range, which is why M₀ = 0.988.'),
        (12.5, '{c:C†} also tracks g, and is tightest for 0 ≤ α ≤ 1.'),
        (17.0, 'The {v:complement} V \\ C† stays nearly flat: it barely responds to scaling.'),
        (21.5, 'Beyond the band, f and C† stop following g: physical extrapolation, distributional extrapolation, or both.'),
        (27.0, 'For α < 0, C† loses tracking earlier. The sign flip may be carried by components outside the circuit.'),
    ]

    def draw(self, c, t):
        header(c, t, '06', 'Results', 'Behavior and cause, across the *range*')
        F = fig4()
        ax = Axes(230, 310, 760, 600, (-2, 2), (-1.6, 1.7))
        k0 = ramp(t, 1.0, 1.0, e_expo)
        ax.draw(c, k0, [-2, -1, 0, 1, 2], [-1.5, -0.75, 0, 0.75, 1.5], prog=k0)
        text(c, 'α', ax.x + ax.w / 2, ax.y + ax.h + 74, 30, 600, 'y', k0, 'center', kind='italic')
        tex(c, 'mhat', ax.x - 110, ax.y + ax.h / 2, 34, k0)
        kb = ramp(t, 2.4, 1.2, e_io)
        if kb > 0:
            X0, _ = ax.px(-1.16 * kb, 0); X1, _ = ax.px(1.16 * kb, 0)
            rrect(c, X0, ax.y, X1 - X0, ax.h, 0, fill='f', fa=0.09)
            line(c, X0, ax.y, X0, ax.y + ax.h, 'f', 0.8, 1.8, dash=[7, 6])
            line(c, X1, ax.y, X1, ax.y + ax.h, 'f', 0.8, 1.8, dash=[7, 6])
            text(c, 'radar-resolvable', (X0 + X1) / 2, ax.y + 34, 20, 600, 'f', kb, 'center')
        # outside-band emphasis
        ko = window(t, 21.5, 27.0, 0.8, 0.6)
        if ko > 0:
            for (a0, a1) in ((-2, -1.16), (1.16, 2)):
                X0, _ = ax.px(a0, 0); X1, _ = ax.px(a1, 0)
                rrect(c, X0, ax.y, X1 - X0, ax.h, 0, fill='r', fa=0.10 * ko)
        kn = window(t, 27.0, None, 0.8)
        if kn > 0:
            X0, _ = ax.px(-2, 0); X1, _ = ax.px(-0.3, 0)
            _, Y0 = ax.px(0, 0.1); _, Y1 = ax.px(0, -1.05)
            rrect(c, X0 + 4, Y0, X1 - X0, Y1 - Y0, 14, stroke='c', sw=2, a=kn * (0.6 + 0.4 * math.sin(t * 4)))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(ax.x, ax.y - 20, ax.w + 20, ax.h + 40))
        for key, colr, t0, dash in (('a_g', 'g', 4.2, None), ('a_f', 'f', 8.0, None), ('a_C', 'c', 12.5, None), ('a_V', 'v', 17.0, [10, 7])):
            p = ramp(t, t0, 2.2, e_io)
            if p > 0:
                P = ax.pts(F[key][:, 0], F[key][:, 1])
                draw_poly(c, P, colr, 1, 4, prog=p, dash=dash, glow=5)
                if p < 1:
                    e = end_point(P, p)
                    circle(c, *e, 7, fill=colr, glow=10)
        c.restore()
        # legend
        kl = ramp(t, 4.2, 0.6)
        lx, ly = ax.x + ax.w - 230, ax.y + ax.h - 150
        for i, (colr, lab, t0, dash) in enumerate((('g', 'g  physics', 4.2, False), ('f', 'f  model', 8.0, False), ('c', 'C†  circuit', 12.5, False), ('v', 'V \\ C†  complement', 17.0, True))):
            legend_item(c, lx, ly + i * 34, colr, lab, ramp(t, t0, 0.6), dash=dash, size=20)
        note(c, 'data extracted from Fig. 4a', ax.x, ax.y - 16, k0 * 0.8, 15)
        # callouts
        yy = 330
        for i, (t0, s) in enumerate(self.CALL):
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            hl = 1.0 if (i + 1 == len(self.CALL) or t < self.CALL[i + 1][0]) else 0.55
            h = rich(c, s, 1100, yy, 27, 700, t, t0, 0.02, 0.45, k * hl, lh=1.3)
            yy += h + 26

# ======================================================================= FIG 4b
class Fig4b(Scene):
    dur = 23.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (3.0, 'draw'), (9.0, 'tick'), (14.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '06', 'Results', 'What the law *forbids*')
        F = fig4()
        ax = Axes(230, 330, 760, 560, (-2, 2), (-0.1, 1.0))
        k0 = ramp(t, 1.0, 1.0, e_expo)
        ax.draw(c, k0, [-2, -1, 0, 1, 2], [0, 0.25, 0.5, 0.75, 1.0], prog=k0)
        text(c, 'α  (tangential scaling)', ax.x + ax.w / 2, ax.y + ax.h + 74, 26, 600, 'y', k0, 'center', kind='italic')
        tex(c, 'mhat', ax.x - 110, ax.y + ax.h / 2, 34, k0)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(ax.x, ax.y - 20, ax.w + 20, ax.h + 40))
        for key, colr, dash in (('b_g', 'g', None), ('b_f', 'f', None), ('b_C', 'c', None), ('b_V', 'v', [10, 7])):
            p = ramp(t, 3.0, 3.0, e_io)
            P = ax.pts(F[key][:, 0], F[key][:, 1])
            draw_poly(c, P, colr, 1, 4, prog=p, dash=dash, glow=5)
        c.restore()
        # alpha = 0 marker
        k1 = ramp(t, 14.0, 0.7)
        if k1 > 0:
            X, Y = ax.px(0, 0)
            pulse = 0.5 + 0.5 * math.sin(t * 5)
            circle(c, X, Y, 16 + 6 * pulse, stroke='y', sw=2.5, a=k1)
            for key, colr in (('b_C', 'c'), ('b_V', 'v')):
                v = float(np.interp(0, F[key][:, 0], F[key][:, 1]))
                Xv, Yv = ax.px(0, v)
                circle(c, Xv, Yv, 9, fill=colr, a=k1, glow=8)
                line(c, X, Y, Xv, Yv, colr, k1 * 0.6, 2, dash=[4, 5])
        lx, ly = ax.x + ax.w - 230, ax.y + 210
        for i, (colr, lab, dash) in enumerate((('g', 'g  physics', False), ('f', 'f  model', False), ('c', 'C†  circuit', False), ('v', 'V \\ C†  complement', True))):
            legend_item(c, lx, ly + i * 34, colr, lab, ramp(t, 3.0, 0.6), dash=dash, size=20)
        note(c, 'data extracted from Fig. 4b', ax.x, ax.y - 16, k0 * 0.8, 15)
        tex(c, 'ptan', 1440, 360, 36, ramp(t, 1.4, 0.8), reveal=ramp(t, 1.4, 1.0, e_io))
        rich(c, 'Zero the radial part and scale only the motion {v:perpendicular} to the line of sight.', 1100, 450, 26, 700, t, 1.8, 0.02, 0.4, ramp(t, 1.8, 0.5), base='muted')
        rich(c, 'Tangential motion produces no first-order Doppler. A lawful model should barely respond, whatever α is.', 1100, 560, 27, 700, t, 6.0, 0.02, 0.4, ramp(t, 6.0, 0.5))
        rich(c, '{f:f}, {c:C†} and {g:g} all stay small: {f:near-invariant} ✓', 1100, 680, 27, 700, t, 9.0, 0.02, 0.4, ramp(t, 9.0, 0.5))
        rich(c, '{y:α = 0 is a body at rest}, so the response must vanish exactly. f and g meet it; C† deviates slightly; the complement deviates a lot.',
             1100, 760, 27, 700, t, 14.0, 0.02, 0.4, ramp(t, 14.0, 0.5))

# ======================================================================= PROBES
class Probes(Scene):
    dur = 26.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (8.0, 'tick'), (12.5, 'chime'), (18.0, 'drop')]
    ROWS = [('T.Proj (input to temporal attention)', 0.019, 'v'),
            ('T.h0', 0.078, 'c'), ('T.h1', 0.042, 'c'), ('T.h2', 0.213, 'c'), ('T.h4', 0.057, 'c'),
            ('T.h6', 0.152, 'c'), ('T.h7', 0.066, 'c'), ('S.h4', 0.032, 'c'),
            ('All heads in C†, combined', 0.761, 'y'),
            ('T.MLP', 0.556, 'f'),
            ('T.MLP, attention output ablated', 0.0004, 'r')]

    def draw(self, c, t):
        header(c, t, '07', 'Mechanism', 'Step 3: where does velocity *appear*?', sub='Linear probes: how well can each marker’s radial velocity be read out? (R² = 1 is perfect)')
        x0, bx, y0, dy, sc = MX, 600, 380, 50, 960
        k0 = ramp(t, 1.0, 0.8)
        # axis
        for v in (0, 0.25, 0.5, 0.75, 1.0):
            X = bx + v * sc
            line(c, X, y0 - 30, X, y0 + dy * len(self.ROWS) - 10, 'line', k0 * 0.8, 1)
            text(c, f'{v:g}', X, y0 - 40, 18, 500, 'muted', k0, 'center', kind='mono')
        text(c, 'R²', bx - 30, y0 - 40, 20, 600, 'muted', k0, 'right', kind='italic')
        for i, (lab, val, colr) in enumerate(self.ROWS):
            t0 = 1.2 + i * 0.35
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            y = y0 + i * dy + (16 if i >= 8 else 0) + (16 if i >= 9 else 0)
            dim = 1.0
            if 8.0 <= t < 12.5 and not (1 <= i <= 7): dim = 0.35
            if 12.5 <= t < 18.0 and i != 8: dim = 0.35
            if t >= 18.0 and i < 9: dim = 0.35
            text(c, lab, bx - 24, y + 8, 22, 600 if i >= 8 else 500, 'ink', k * dim, 'right')
            v = val
            if i == 10:
                v = lerp(0.556, 0.0004, ramp(t, 18.5, 1.4, e_io)) if t >= 18.0 else 0.556
            w = v * sc * ramp(t, t0, 1.0, e_expo)
            rrect(c, bx, y - 13, max(w, 3), 26, 5, fill=colr, a=k * dim, fa=k * dim * (0.95 if i >= 8 else 0.75), glow=8 if i == 8 and t > 12.5 else 0)
            text(c, f'{v:.3f}' if v >= 0.001 else f'{v:.4f}', bx + max(w, 3) + 14, y + 8, 21, 600, colr, k * dim, kind='mono')
        caption(c, t, '{w:No single head} decodes it well: every head’s R² is at most 0.21.', 8.0, 12.2, y=985, size=30)
        caption(c, t, 'Together, the circuit’s heads reach {y:R² = 0.76}. Radial velocity emerges in their {y:combined} output.', 12.5, 17.7, y=985, size=30)
        caption(c, t, 'T.MLP also decodes it (0.556), but replace attention’s output with its mean and that collapses to {r:0.0004}. It inherits v from attention.', 18.0, None, y=985, size=28, maxw=1700)

# ======================================================================= QK vs VAL
class QKVal(Scene):
    dur = 26.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (8.5, 'pop'), (9.0, 'pop'), (16.0, 'tick')]
    HEADS = [('T.h0', 3.06, 3.48), ('T.h1', 2.68, 3.56), ('T.h2', 3.14, 3.54), ('T.h4', 3.45, 3.28), ('T.h6', 1.88, 3.47), ('T.h7', 2.34, 3.33), ('S.h4', 3.55, 2.92)]

    def draw(self, c, t):
        header(c, t, '07', 'Mechanism', 'Pattern, not *payload*')
        # concept panel
        k0 = ramp(t, 1.0, 0.9, e_expo)
        px, py, pw, ph = MX, 300, 760, 360
        if k0 > 0:
            with layer(c, k0):
                panel(c, px, py, pw, ph)
                kicker(c, 'inside one attention head', px + 28, py + 40, 1, 'muted', 16)
                n = 12
                xs = [px + 60 + i * 58 for i in range(n)]
                yk, yq = py + 260, py + 120
                q = int((t * 1.2) % n)
                for i in range(n):
                    circle(c, xs[i], yk, 10, fill='faint')
                    circle(c, xs[i], yq, 8, fill='faint', a=0.6)
                circle(c, xs[q], yq, 11, fill='y', glow=8)
                for i in range(n):
                    w_ = math.exp(-((i - (q - 4) % n) ** 2) / 2.0) + math.exp(-((i - (q + 3) % n) ** 2) / 2.0)
                    pth = skia.Path(); pth.moveTo(xs[q], yq + 10)
                    pth.cubicTo(xs[q], yq + 80, xs[i], yk - 80, xs[i], yk - 12)
                    c.drawPath(pth, paint('c', 0.1 + 0.8 * min(1, w_), stroke=1 + 3 * min(1, w_)))
                text(c, 'QK = the attention pattern: which frames to read', px + 28, py + ph - 52, 22, 600, 'c', 1)
                text(c, 'VAL = the values: what is carried from them', px + 28, py + ph - 20, 22, 500, 'muted', 1)
        # big bars
        k1 = ramp(t, 8.5, 0.9, e_expo)
        bx, by = 980, 330
        if k1 > 0:
            with layer(c, k1):
                kicker(c, 'sufficiency deviation, all circuit heads · lower = better', bx, by, 1, 'muted', 16)
                for j, (key, val, colr, lab) in enumerate((('qk', 0.35, 'c', 'patch only the pattern'), ('val', 1.31, 'v', 'patch only the values'))):
                    y = by + 70 + j * 130
                    tex(c, key, bx, y + 10, 30, 1, align='left')
                    w = val * 330 * ramp(t, 9.0 + j * 0.4, 1.0, e_expo)
                    rrect(c, bx + 250, y - 22, w, 44, 8, fill=colr, fa=0.9)
                    number(c, val, bx + 250 + w + 16, y + 14, 40, colr, 1, '{:.2f}')
                    text(c, lab, bx + 250, y + 52, 20, 500, 'muted', 1)
        # per-head small multiples
        k2 = ramp(t, 16.0, 0.9)
        if k2 > 0:
            with layer(c, k2):
                kicker(c, 'per head: Δsuf with QK patched vs. VAL patched', MX, 730, 1, 'muted', 16)
                for i, (h, qk, va) in enumerate(self.HEADS):
                    x = MX + i * 240
                    y = 770
                    kk = ramp(t, 16.2 + i * 0.12, 0.6)
                    text(c, h, x, y + 22, 22, 650, 'ink', kk, kind='mono')
                    for j, (v, colr) in enumerate(((qk, 'c'), (va, 'v'))):
                        line(c, x, y + 50 + j * 22, x + v * 44 * kk, y + 50 + j * 22, colr, kk, 12, cap='butt')
                        text(c, f'{v:.2f}', x + v * 44 * kk + 8, y + 56 + j * 22, 15, 600, colr, kk, kind='mono')
                    better = qk < va
                    pill(c, x, y + 100, 'QK wins' if better else 'VAL wins', 'f' if better else 'r', kk, size=14)
        caption(c, t, 'Swapping in the counterfactual {c:attention pattern} alone nearly restores consistency; swapping the values alone does not.', 11.5, 15.6, y=985, size=29)
        caption(c, t, 'In Table 2, 5 of the 6 temporal heads in C† are more QK-sufficient (T.h4 is the exception). The scaling response lives in {c:where attention looks}.', 16.4, None, y=985, size=28, maxw=1700)
        note(c, 'note: the paper’s text says “six of the seven”; its Table 2 values give 5 of 6 temporal heads (and S.h4 favors VAL)', MX, 930, ramp(t, 18.0, 0.8) * 0.85, 15)

# ======================================================================= HEATMAPS
class Heatmaps(Scene):
    dur = 32.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (0.8, 'pop'), (4.5, 'sweep'), (12.0, 'pop'), (20.0, 'tick'), (25.0, 'chime')]

    def __init__(self):
        r = rasters()
        self.ims = {k: array_image(np.array(v), vmin=0, vmax=0.04) for k, v in r['heads'].items()}

    def draw(self, c, t):
        header(c, t, '07', 'Mechanism', 'Two heads, two *ends* of the window')
        zoom = ramp(t, 4.5, 1.4, e_io)
        # thumbnails -> big h6/h7
        for i in range(8):
            key = f'h{i}'
            ts = 140 + 0 * i
            x_t = MX + 40 + i * 205
            y_t = 360
            if i in (6, 7):
                j = i - 6
                x_b, y_b, s_b = MX + 20 + j * 470, 340, 420
                x = lerp(x_t, x_b, zoom); y = lerp(y_t, y_b, zoom); s = lerp(180, s_b, zoom)
                a = ramp(t, 0.8 + i * 0.08, 0.6)
            else:
                x, y, s = x_t, y_t, 180
                a = ramp(t, 0.8 + i * 0.08, 0.6) * (1 - ramp(t, 4.3, 0.45))
            if a <= 0:
                continue
            draw_image(c, self.ims[key], x, y, s, s, a, smooth=False)
            rrect(c, x, y, s, s, 3, stroke='line', sw=1.2, a=a)
            hl = 'c' if f'T.{key}' in CDAG else 'muted'
            text(c, f'T.{key}', x + s / 2, y - 14, 20 + 6 * (zoom if i in (6, 7) else 0), 650, hl, a, 'center', kind='mono')
        k0 = ramp(t, 1.4, 0.6) * (1 - zoom)
        text(c, 'mean attention, 200 evaluation windows · rows = query time, columns = key time', MX + 40, 600, 20, 500, 'muted', k0)
        note(c, 'data from Fig. 5', MX + 40, 640, k0 * 0.8, 16)
        # labels on big maps
        kz = ramp(t, 6.0, 0.6)
        if kz > 0:
            for j, (lab, colr, ky) in enumerate((('attends to the earliest frames', 'g', 0.04), ('attends to the latest frames', 'x', 0.96))):
                x_b = MX + 20 + j * 470
                text(c, lab, x_b + 210, 800, 22, 600, colr, kz, 'center')
                kx = x_b + ky * 420
                arrow(c, kx, 770, kx, 768 - 6, colr, kz, 3, 12)
            text(c, 'key time →', MX + 20, 850, 18, 500, 'muted', kz, kind='mono')
            text(c, 'query time ↓', MX + 20, 880, 18, 500, 'muted', kz, kind='mono')
        # interpretation panel
        ki = ramp(t, 12.0, 0.9, e_expo)
        if ki > 0:
            ix, iy, iw, ih = 1100, 320, 700, 480
            with layer(c, ki):
                panel(c, ix, iy, iw, ih)
                kicker(c, "authors' interpretation", ix + 26, iy + 40, 1, 'y', 16)
                fast = 0.5 + 0.5 * math.sin((t - 12) * 0.55)  # 0 slow .. 1 fast
                ax = Axes(ix + 50, iy + 80, iw - 100, 260, (0, 1), (-1, 1))
                xs = np.linspace(0, 1, 200)
                freq = lerp(0.8, 2.6, fast)
                r = 0.75 * np.sin(2 * np.pi * freq * xs + 0.6)
                line(c, ax.x, ax.y + ax.h, ax.x + ax.w, ax.y + ax.h, 'muted', 0.7, 1.5)
                text(c, 'range to radar  r(t)', ax.x, ax.y - 10, 18, 500, 'muted', 1, kind='mono')
                for fx in np.linspace(0, 1, 33):
                    X, _ = ax.px(fx, 0)
                    line(c, X, ax.y + ax.h, X, ax.y + ax.h - 8, 'faint', 1, 1.5)
                draw_poly(c, ax.pts(xs, r), 'ink', 0.9, 3)
                gap = lerp(0.42, 0.1, fast)
                tq = 0.5
                ta, tb = tq - gap / 2, tq + gap / 2
                ra = 0.75 * math.sin(2 * math.pi * freq * ta + 0.6); rb = 0.75 * math.sin(2 * math.pi * freq * tb + 0.6)
                Pa = ax.px(ta, ra); Pb = ax.px(tb, rb)
                line(c, *Pa, *Pb, 'y', 1, 3, glow=6)
                circle(c, *Pa, 9, fill='g', glow=8)
                circle(c, *Pb, 9, fill='x', glow=8)
                line(c, Pa[0], Pa[1], Pa[0], ax.y + ax.h, 'g', 0.5, 1.5, dash=[4, 4])
                line(c, Pb[0], Pb[1], Pb[0], ax.y + ax.h, 'x', 0.5, 1.5, dash=[4, 4])
                text(c, 'early frame', Pa[0], ax.y + ax.h + 28, 17, 600, 'g', 1, 'center', kind='mono')
                text(c, 'late frame', Pb[0], ax.y + ax.h + 50, 17, 600, 'x', 1, 'center', kind='mono')
                text(c, 'v ≈ Δr / Δt', ix + iw - 40, iy + ih - 40, 30, 650, 'y', 1, 'right', kind='italic')
                text(c, 'fast motion → short gap' if fast > 0.5 else 'slow motion → long gap', ix + 40, iy + ih - 40, 22, 600, 'ink', 1)
        caption(c, t, 'A velocity is a {y:temporal difference}: it needs an early and a late reference point. The two heads supply them, and neither alone carries the difference.', 15.0, 24.6, y=975, size=28, maxw=1700)
        caption(c, t, 'Because QK carries the scaling response, attention may {y:choose the frame gap} to suit the speed, like multi-scale temporal differentiation.', 25.0, None, y=975, size=28, maxw=1700)

# ======================================================================= LIMITS
class Limits(Scene):
    dur = 23.0
    chapter = 7
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (5.0, 'pop'), (9.0, 'pop'), (13.0, 'pop')]
    CARDS = [
        ('One case study', 'A single {y:linear} law in one small spatio-temporal transformer. Nonlinear and multi-variable laws, and larger models, may need different bridges, perturbations and searches.'),
        ('The law is given', 'LAWFUL takes the grounding law as {y:supplied}. It does not say how to choose it, or how to discover it.'),
        ('Uniform perturbations', 'Perturbations rescale speed {y:uniformly} across the body. Changing the motion itself, or only part of the body, is untested.'),
        ('A scalar bridge', 'The Doppler centroid captures the {y:bulk shift} only. Spread, harmonics and micro-Doppler may run through other circuits.'),
    ]

    def draw(self, c, t):
        header(c, t, '08', 'Limits & discussion', 'What the paper does not (yet) *show*')
        cw, chh = 828, 260
        for i, (lab, body) in enumerate(self.CARDS):
            t0 = 1.0 + i * 4.0
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            x = MX + (i % 2) * (cw + 24)
            y = 330 + (i // 2) * (chh + 24)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 24):
                    panel(c, x, y, cw, chh)
                    text(c, f'{i + 1:02d}', x + 30, y + 58, 22, 600, 'y', 1, kind='mono')
                    text(c, lab, x + 90, y + 58, 32, 700, 'ink', 1)
                    rich(c, body, x + 30, y + 118, 27, cw - 60, t, t0 + 0.3, 0.02, 0.4)
        caption(c, t, 'Invariant enforcement and signal-flow quantification, gaps 3 and 4, are groundwork here rather than finished results.', 17.5, None, y=940, size=27, base='muted')

# ======================================================================= DISCUSSION
class Discussion(Scene):
    dur = 32.0
    chapter = 7
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (6.5, 'pop'), (12.5, 'pop'), (18.5, 'pop'), (24.5, 'pop')]
    QS = [
        'Is matching one number, the centroid slope, enough to say the model {y:uses} the Doppler law?',
        'The circuit search picks components by sufficiency alone, one at a time. {y:Would a different search find a different circuit?}',
        'Without the circuit, consistency falls far below zero (Δnec = 3.50 vs M₀ = 0.988). {y:How should we read effect sizes} on a score with no floor?',
        'Beyond |α| ≈ 1.16: radar physics or distribution shift? {y:What experiment would separate them?}',
        'What would LAWFUL need for {y:nonlinear, multi-variable} laws, or for a law nobody knows in advance?',
    ]

    def draw(self, c, t):
        header(c, t, '08', 'Limits & discussion', 'Before we *meet*: questions to think about')
        y = 330
        for i, q in enumerate(self.QS):
            t0 = 1.0 + i * 6.0
            k = ramp(t, t0, 0.7, e_expo)
            if k <= 0:
                y += 130
                continue
            text(c, f'Q{i + 1}', MX, y + 8 + (1 - k) * 10, 30, 750, 'y', k, kind='mono')
            h = rich(c, q, MX + 90, y + 8, 33, 1580, t, t0 + 0.1, 0.025, 0.45, k, lh=1.28)
            y += max(h, 44) + 48
        from explainer.notes import sticky
        sticky(c, 1560, 860, ['bring one', 'to the desk'], ramp(t, 27.0, 0.5, e_back), rot=-4.0, w=230, h=170, tag='homework')

# ======================================================================= END
class End(Scene):
    dur = 20.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (21.0, 'outro')]

    def draw(self, c, t):
        k0 = ramp(t, 0.3, 1.0, e_expo)
        kicker(c, 'the takeaway', W / 2, 220, k0, 'y', 20, align='center')
        rich(c, 'A known {y:physical law}, not task accuracy, as the ground truth for a model’s {y:internal computation}.',
             W / 2, 300, 50, 1500, t, 0.6, 0.05, 0.6, 1, 'center', base_w=650, lh=1.25)
        stats = [('0.988', 'M₀: the model obeys the law', 'f'), ('9 / 18', 'components recover 91% of M₀', 'c'),
                 ('0.02 → 0.76', 'R² for v, pre-attention → C† heads', 'y'), ('0.35 vs 1.31', 'Δsuf: QK-only vs VAL-only patch', 'x')]
        for i, (big, small, colr) in enumerate(stats):
            k = ramp(t, 3.0 + i * 0.35, 0.8, e_expo)
            x = MX + 40 + i * 420
            with layer(c, k):
                line(c, x, 470, x + 60 * k, 470, colr, 1, 3)
                text(c, big, x, 545, 50, 760, colr, 1, tracking=-0.02)
                text(c, small, x, 588, 21, 500, 'muted', 1)
        k2 = ramp(t, 5.5, 0.9)
        with layer(c, k2):
            line(c, MX, 680, W - MX, 680, 'line', 1, 1.5)
            text(c, 'Chen, Parker & Arora (2026).  LAWFUL: Law-Aligned Witness for Faithful Use of Latents.', MX, 740, 27, 600, 'ink', 1)
            text(c, 'Mechanistic Interpretability Workshop, ICML 2026, Seoul  ·  arXiv:2607.28672', MX, 782, 23, 500, 'muted', 1)
            text(c, 'code  github.com/aciculachen/LAWFUL', MX, 832, 22, 500, 'g', 1, kind='mono')
            note(c, 'Charts are redrawn from data extracted from the paper’s figures. Walker, radar and step diagrams are illustrations.', MX, 900, 0.85, 16)
        k3 = ramp(t, 7.0, 0.8)
        from explainer.notes import lamp
        lamp(c, 1640, 760, 1.15, k3, on=k3)
        hand(c, 'see you at the desk', 1390, 960, 36, 'pencil', k3, -3.0, ramp(t, 7.4, 1.0, e_lin))
