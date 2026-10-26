"""Beginner primer scenes: what mechanistic interpretability is, reading vs. writing, and the paper's roadmap."""
import math
import numpy as np
import skia
from explainer.core import *
from explainer.kit import *
from explainer.timeline import Scene
from scenes1 import rasters, draw_body
import walker as WK

def _graph(x0, y0, w, h):
    """Node positions for a small cartoon network: embed -> attention heads -> MLP -> heads -> MLP -> out."""
    cols = [4, 8, 3, 8, 3, 1]
    nodes = []
    for ci, n in enumerate(cols):
        x = x0 + w * (0.06 + 0.88 * ci / (len(cols) - 1))
        for j in range(n):
            y = y0 + h * (0.5 if n == 1 else 0.1 + 0.8 * j / (n - 1))
            nodes.append((ci, j, x, y))
    edges = []
    for a in nodes:
        for b in nodes:
            if b[0] == a[0] + 1 and (a[1] * 7 + b[1] * 3 + a[0]) % 3 == 0:
                edges.append((a, b))
    return nodes, edges

# ======================================================================= WHAT IS MECH INTERP
class MechInterp(Scene):
    dur = 30.0
    chapter = 0
    tracker = False
    cues = [(0.2, 'whoosh'), (1.0, 'pop'), (6.0, 'sweep'), (12.0, 'chime'), (20.0, 'pop')]
    CIRCUIT = {(1, 2), (1, 5), (2, 1), (3, 6), (4, 1), (5, 0)}

    def __init__(self):
        r = rasters()
        self.spec = array_image(np.array(r['spec']['model'], float) / 255.0)

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'Mechanistic interpretability, *briefly*')
        bx, by, bw, bh = 470, 360, 700, 400
        k0 = ramp(t, 0.8, 0.9, e_expo)
        # input
        with layer(c, k0):
            panel(c, 130, 450, 230, 230)
            cam = WK.Camera(yaw=-0.5, pitch=0.12, dist=5.0, focal=420, cx=245, cy=575, target=(0, 0, 0.9))
            J = WK.skeleton(t * 2 * math.pi * 0.9)
            M, _ = WK.markers(J)
            draw_body(c, cam, M, J, 1.0, color='g', r=3, glow=4)
            text(c, 'motion in', 245, 715, 22, 500, 'muted', 1, 'center', kind='mono')
            arrow(c, 372, 565, bx - 14, 565, 'muted', 1, 2.5)
            arrow(c, bx + bw + 14, 565, 1250, 565, 'muted', 1, 2.5)
            draw_image(c, self.spec, 1262, 465, 200, 200)
            rrect(c, 1262, 465, 200, 200, 4, stroke='line', sw=1.2)
            text(c, 'radar out', 1362, 715, 22, 500, 'muted', 1, 'center', kind='mono')
        # the network: opaque box, then opened
        nodes, edges = _graph(bx + 40, by + 50, bw - 80, bh - 100)
        reveal = ramp(t, 6.0, 1.6, e_io)
        circ = ramp(t, 12.0, 1.0)
        with layer(c, k0):
            for (a, b) in edges:
                inC = (a[0], a[1]) in self.CIRCUIT and (b[0], b[1]) in self.CIRCUIT
                colr = mix('faint', PAL['c'], circ if inC else 0)
                line(c, a[2], a[3], b[2], b[3], colr, reveal * (0.9 if inC and circ > 0 else 0.55), 1.5 + 2 * (circ if inC else 0))
            for (ci, j, x, y) in nodes:
                inC = (ci, j) in self.CIRCUIT
                kind = 'mlp' if ci in (2, 4) else 'node'
                fill = mix('panel2', PAL['c'], circ if inC else 0)
                if kind == 'mlp':
                    rrect(c, x - 22, y - 14, 44, 28, 6, fill=fill, a=reveal, glow=8 * circ if inC else 0)
                    rrect(c, x - 22, y - 14, 44, 28, 6, stroke=mix('faint', PAL['c'], circ if inC else 0), sw=1.4, a=reveal)
                else:
                    circle(c, x, y, 9, fill=fill, a=reveal, glow=8 * circ if inC else 0)
                    circle(c, x, y, 9, stroke=mix('faint', PAL['c'], circ if inC else 0), sw=1.4, a=reveal)
            if reveal > 0.95:
                for e_i, (a, b) in enumerate(edges[::5]):
                    flow_dots(c, np.array([[a[2], a[3]], [b[2], b[3]]]), t + e_i * 0.37, 'y', 0.7, 1, 0.5, 3, 5)
            # the lid
            lid = 1 - reveal
            if lid > 0:
                rrect(c, bx, by, bw, bh, 18, fill='#0c0d15', a=lid)
                text(c, '?', bx + bw / 2, by + bh / 2 + 40, 120, 300, 'muted', lid * 0.7, 'center', kind='display')
            rrect(c, bx, by, bw, bh, 18, stroke=mix('faint', PAL['y'], reveal), sw=1.6, a=1)
            lab_a = 1 - ramp(t, 5.6, 0.5)
            text(c, 'behavioral evaluation: only inputs and outputs', bx + bw / 2, by - 22, 21, 400, 'muted', k0 * lab_a, 'center', kind='mono')
            text(c, 'mechanistic interpretability: look inside', bx + bw / 2, by - 22, 21, 400, 'y', ramp(t, 6.4, 0.6), 'center', kind='mono')
            if circ > 0:
                text(c, 'a circuit: a few components that do one job together', bx + bw / 2, by + bh + 42, 24, 500, 'c', circ, 'center')
            # accuracy check
            kc = ramp(t, 2.6, 0.6) * (1 - ramp(t, 11.5, 0.6))
            text(c, 'accurate ✓', 1560, 575, 30, 600, 'f', kc)
            for (ci, j, x, y) in nodes:
                if ci == 1 and reveal > 0.5:
                    text(c, 'attention heads', x, by + 34, 17, 400, 'muted', ramp(t, 8.0, 0.6) * (1 - circ * 0.5), 'center', kind='mono')
                    break
            for (ci, j, x, y) in nodes:
                if ci == 2 and reveal > 0.5:
                    text(c, 'MLP', x, by + bh - 14, 17, 400, 'muted', ramp(t, 8.4, 0.6) * (1 - circ * 0.5), 'center', kind='mono')
                    break
        # why physics
        kp = ramp(t, 20.0, 0.9, e_expo)
        if kp > 0:
            with layer(c, kp):
                rrect(c, MX, 850, 820, 120, 14, fill='panel', fa=0.85)
                rrect(c, MX, 850, 820, 120, 14, stroke='line', sw=1.2)
                text(c, 'language models', MX + 30, 896, 26, 600, 'ink')
                text(c, 'the “right” algorithm is usually unknown', MX + 30, 936, 24, 400, 'muted')
                text(c, '?', MX + 770, 930, 64, 300, 'muted', 1, 'center', kind='display')
            kq = ramp(t, 21.5, 0.9, e_expo)
            with layer(c, kq):
                rrect(c, 980, 850, 820, 120, 14, fill='y', fa=0.08)
                rrect(c, 980, 850, 820, 120, 14, stroke='y', sw=1.4, a=0.7)
                text(c, 'physics', 1010, 896, 26, 600, 'y')
                text(c, 'the true law is written down', 1010, 936, 24, 400, 'ink')
                tex(c, 'doppler', 1680, 910, 40, 1)

# ======================================================================= READ vs WRITE
class ProbeVsPatch(Scene):
    dur = 28.0
    chapter = 0
    tracker = False
    cues = [(0.2, 'whoosh'), (1.5, 'pop'), (9.0, 'tick'), (13.0, 'pop'), (17.0, 'sweep'), (23.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'Two tools: *read*, or write')
        # ---- left: probe
        kl = ramp(t, 1.5, 0.9, e_expo)
        px, py, pw, ph = MX, 320, 820, 500
        if kl > 0:
            with layer(c, kl):
                panel(c, px, py, pw, ph)
                kicker(c, 'read · a linear probe', px + 30, py + 44, 1, 'y', 19)
                n = 10
                vals = [0.5 + 0.45 * math.sin(t * 1.3 + i * 0.9) * math.cos(i * 0.4) for i in range(n)]
                cx, cy0 = px + 110, py + 90
                text(c, 'activations', cx + 16, py + ph - 28, 18, 400, 'muted', 1, 'center', kind='mono')
                for i, v in enumerate(vals):
                    r, g, b = CMAP[int(clamp(v) * 255)]
                    rrect(c, cx, cy0 + i * 34, 34, 28, 4, fill='#%02x%02x%02x' % (r, g, b))
                # probe lines
                bx_, by_ = px + 330, py + 230
                for i in range(n):
                    line(c, cx + 36, cy0 + 14 + i * 34, bx_ - 6, by_ + 40, 'y', 0.18 + 0.3 * vals[i], 1.3)
                rrect(c, bx_, by_, 190, 80, 12, fill='panel2')
                rrect(c, bx_, by_, 190, 80, 12, stroke='y', sw=1.6)
                text(c, 'w · a + b', bx_ + 95, by_ + 50, 28, 400, 'ink', 1, 'center', kind='italic')
                arrow(c, bx_ + 196, by_ + 40, bx_ + 270, by_ + 40, 'muted', 1, 2.5)
                v = 1.3 + 0.25 * math.sin(t * 1.3)
                text(c, f'v ≈ {v:.1f} m/s', bx_ + 285, by_ + 50, 32, 600, 'g')
                text(c, 'velocity, read out', bx_ + 285, by_ + 86, 20, 400, 'muted', 1, kind='mono')
                kd = ramp(t, 9.0, 0.7)
                text(c, 'readable ≠ used', px + pw / 2 + 120, py + ph - 70, 34, 400, 'y', kd, 'center', kind='italic')
        # ---- right: patching
        kr = ramp(t, 13.0, 0.9, e_expo)
        rx, ry, rw, rh = 980, 320, 820, 500
        if kr > 0:
            with layer(c, kr):
                panel(c, rx, ry, rw, rh)
                kicker(c, 'write · activation patching', rx + 30, ry + 44, 1, 'y', 19)
                rows = [(ry + 170, 'original input', 'faint'), (ry + 320, 'what-if input', 'x')]
                xs = [rx + 250 + i * 88 for i in range(5)]
                copy = ramp(t, 16.5, 1.2, e_io)
                for ri, (yy, lab, colr) in enumerate(rows):
                    text(c, lab, rx + 30, yy + 7, 20, 500, 'ink' if ri == 0 else 'x', 1, kind='mono')
                    for i, x in enumerate(xs):
                        if i:
                            line(c, xs[i - 1] + 18, yy, x - 18, yy, 'muted', 0.6, 1.5)
                        fill = colr
                        if ri == 0 and i == 2:
                            fill = mix('faint', PAL['x'], 1.0 if copy >= 1 else 0)
                        circle(c, x, yy, 17, fill=fill, a=1, glow=6 if (ri == 0 and i == 2 and copy >= 1) else 0)
                    line(c, xs[-1] + 18, yy, xs[-1] + 60, yy, 'muted', 0.6, 1.5)
                # the copied activation travelling up
                if 0 < copy < 1:
                    yy = lerp(rows[1][0], rows[0][0], copy)
                    circle(c, xs[2], yy, 10, fill='x', glow=10)
                # output gauges
                for ri, (yy, _, colr) in enumerate(rows):
                    gx = xs[-1] + 70
                    base = 0.25 if ri == 0 else 0.8
                    if ri == 0:
                        base = lerp(0.25, 0.72, ramp(t, 17.8, 1.0, e_out))
                    line(c, gx, yy, gx + 130, yy, 'line', 1, 10, cap='butt')
                    line(c, gx, yy, gx + 130 * base, yy, 'g' if ri == 0 else 'x', 1, 10, cap='butt')
                    text(c, 'output', gx + 65, yy - 22, 17, 400, 'muted', 1, 'center', kind='mono')
                kk = ramp(t, 19.0, 0.7)
                text(c, 'the output moved, so that component matters', rx + rw / 2, ry + rh - 60, 26, 500, 'g', kk, 'center')
        caption(c, t, 'Reading shows what’s {y:there}. Patching shows what’s {y:used}.', 23.0, None, y=930, size=36)

# ======================================================================= ROADMAP
class Roadmap(Scene):
    dur = 27.0
    chapter = 0
    steps = (0, 1, 2)
    tracker = True
    cues = [(0.2, 'whoosh'), (2.5, 'pop'), (9.0, 'pop'), (15.0, 'pop'), (21.0, 'chime')]
    CARDS = [
        ('behavior', 'Does the model follow the law when we change its input in physically meaningful, what-if ways?',
         'consistency over what-if inputs', 'g', 2.5),
        ('cause', 'Which components inside the model produce that law-following behavior?',
         'activation patching finds a circuit', 'c', 9.0),
        ('mechanism', 'How do those components actually compute velocity?',
         'probes and attention patterns', 'x', 15.0),
    ]

    def draw(self, c, t):
        header(c, t, '01', 'the question', 'The plan: *three* steps')
        cw, gap, y0, ch = 532, 42, 350, 470
        for i, (name, q, how, colr, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, f'{i + 1}', x + 36, y0 + 112, 92, 300, colr, 1, kind='display')
                    text(c, name, x + 100, y0 + 98, 44, 400, 'ink', 1, kind='italic')
                    rich(c, q, x + 36, y0 + 190, 31, cw - 72, t, t0 + 0.3, 0.03, 0.45, 1.0, lh=1.34)
                    kh = ramp(t, t0 + 2.4, 0.6)
                    line(c, x + 36, y0 + ch - 104, x + cw - 36, y0 + ch - 104, 'line', kh, 1.2)
                    text(c, 'how the paper tests it', x + 36, y0 + ch - 66, 17, 400, 'muted', kh, kind='mono', tracking=0.08)
                    text(c, how, x + 36, y0 + ch - 30, 24, 500, colr, kh)
            if i < 2 and k > 0.5:
                hx = x + cw + 6
                line(c, hx, y0 + ch / 2, hx + gap - 12, y0 + ch / 2, 'muted', ramp(t, t0 + 1, 0.5), 2)
        k4 = ramp(t, 21.0, 0.8)
        if k4 > 0:
            hand(c, 'the tracker up top follows along', W / 2 + 120, 150, 34, 'pencil', k4, -2.0, ramp(t, 21.0, 1.4, e_lin))
            from explainer.notes import hand_arrow
            hand_arrow(c, W / 2 + 110, 135, W / 2 + 30, 92, 'pencil', k4, ramp(t, 22.2, 0.6), bend=-0.3)
