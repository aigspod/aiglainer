"""The poster look of the hackathon invitation: heavy Inter capitals on paper and on full-bleed slabs of cobalt,
signal orange, acid lime and near-black, riso-style misregistered type, slice glitches and scanlines, and
procedurally drawn halftone fields. Everything that looks like data here is abstract art, and labelled so.

Colours are THEME tokens (project.py): paper, ink, cobalt, orange, lime, night.
"""
import math
import numpy as np
import skia
from aiglainer.core import *
from beat import BEAT, kick

PAD = 120          # side margin


# ---------------------------------------------------------------- type
def tw(s, size, weight=900, track=-0.035):
    return text_width(s, size, weight, 'heavy', track)


def fit(s, size, maxw, weight=900, track=-0.035):
    """The largest size up to `size` at which s fits in maxw."""
    w = tw(s, size, weight, track)
    return size if w <= maxw else size * maxw / w


def big(c, s, x, y, size, color='ink', a=1.0, align='left', weight=900, track=-0.035, riso=None):
    """Heavy capitals. riso=(colour, colour, px) prints two misregistered copies underneath, like a riso poster."""
    if a <= 0.003:
        return 0
    if riso:
        c1, c2, px = riso
        if px > 0.3:
            text(c, s, x - px, y - px * 0.4, size, weight, c1, a * 0.9, align, 'heavy', track)
            text(c, s, x + px, y + px * 0.4, size, weight, c2, a * 0.9, align, 'heavy', track)
    return text(c, s, x, y, size, weight, color, a, align, 'heavy', track)


def mono(c, s, x, y, size=22, color='ink', a=1.0, align='left', track=0.14, bold=False):
    return text(c, s, x, y, size, 700 if bold else 400, color, a, align, 'mono', track)


def tag(c, s, x, y, size=22, fg='paper', bg='ink', a=1.0, align='left', padx=14, pady=10):
    """A mono label printed in a solid block: y is the text baseline."""
    if a <= 0.003:
        return 0
    w = text_width(s, size, 700, 'mono', 0.14)
    x0 = x - w / 2 if align == 'center' else x - w if align == 'right' else x
    c.drawRect(skia.Rect.MakeXYWH(x0 - padx, y - size * 0.95 - pady + size * 0.12, w + 2 * padx, size * 0.95 + 2 * pady), paint(bg, a))
    text(c, s, x0, y, size, 700, fg, a, 'left', 'mono', 0.14)
    return w + 2 * padx


def illustration(c, x, y, color='ink', a=1.0, align='left'):
    mono(c, 'illustration', x, y, 17, color, a * 0.8, align, 0.12)


def slam(t, t0, d=0.2, over=0.3):
    """(alpha, scale) for a word that slams in on a beat at t0."""
    if t < t0:
        return 0.0, 1.0
    k = ramp(t, t0, d, e_out)
    return min(1.0, (t - t0) / 0.05), 1 + over * (1 - k)


class at:
    """with at(c, x, y, s): scale about (x, y)."""
    def __init__(self, c, x, y, s=1.0, rot=0.0):
        self.c, self.x, self.y, self.s, self.rot = c, x, y, s, rot
    def __enter__(self):
        self.c.save()
        self.c.translate(self.x, self.y)
        if self.rot:
            self.c.rotate(self.rot)
        if self.s != 1:
            self.c.scale(self.s, self.s)
        self.c.translate(-self.x, -self.y)
        return self.c
    def __exit__(self, *a):
        self.c.restore()


def slam_word(c, t, t0, s, x, y, size, color='ink', align='left', riso=None, out=None, pump=0.0, over=0.3):
    """A heavy word slammed in at t0 (scaled about its own centre), optionally leaving at `out`, pumping on the kick."""
    a, sc = slam(t, t0, over=over)
    if out is not None:
        a *= 1 - ramp(t, out, 0.15, e_io)
    if a <= 0.003:
        return 0
    w = tw(s, size)
    cx = x + w / 2 if align == 'left' else x - w / 2 if align == 'right' else x
    sc *= 1 + pump * kick(t, t0)
    with at(c, cx, y - size * 0.36, sc):
        return big(c, s, x, y, size, color, a, align, riso=riso)


# ---------------------------------------------------------------- ground and texture
def slab(c, color, a=1.0, x=0, y=0, w=W, h=H):
    if a > 0.003:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(color, a))


def stripes(c, t, color, a=0.15, gap=46, width=10, speed=120, angle=-28):
    if a <= 0.003:
        return
    c.save()
    c.translate(W / 2, H / 2)
    c.rotate(angle)
    off = (t * speed) % gap
    p = paint(color, a)
    for k in range(-40, 41):
        x = k * gap + off
        c.drawRect(skia.Rect.MakeXYWH(x, -1400, width, 2800), p)
    c.restore()


def scanlines(c, t, a=0.08, color='night', band=True):
    """Thin horizontal lines across the frame, and a soft bright band rolling down it."""
    if a <= 0.003:
        return
    p = paint(color, a, stroke=1.0, aa=False)
    for y in range(0, H, 4):
        c.drawLine(0, y + 0.5, W, y + 0.5, p)
    if band:
        yb = (t * 520) % (H + 300) - 150
        g = skia.Paint()
        g.setShader(skia.GradientShader.MakeLinear([(0, yb - 120), (0, yb + 120)], [col('paper', 0), col('paper', a * 1.6), col('paper', 0)]))
        c.drawRect(skia.Rect.MakeXYWH(0, yb - 120, W, 240), g)


def _hash(*k):
    v = math.sin(sum((i + 1) * 12.9898 * x for i, x in enumerate(k)) + 78.233) * 43758.5453
    return v - math.floor(v)


def glitch(c, fn, amt, t, seed=0, bands=14, rate=24):
    """Draw fn() cut into horizontal bands, some shifted sideways: a data glitch of strength amt (0..1)."""
    if amt <= 0.01:
        fn()
        return
    step = math.floor(t * rate)
    y = 0.0
    for k in range(bands):
        h = H / bands * (0.4 + 1.2 * _hash(seed, k, step))
        dx = 0.0
        if _hash(seed + 7, k, step) < 0.25 + 0.6 * amt:
            dx = (_hash(seed + 3, k, step) - 0.5) * 2 * 140 * amt
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0, y, W, h + 1))
        c.translate(dx, 0)
        fn()
        c.restore()
        y += h
        if y >= H:
            break
    if y < H:
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0, y, W, H - y))
        fn()
        c.restore()


def strobe(c, t, t0, t1, colors, rate=3):
    """Full-frame colour changes, one per 1/rate of a second, between t0 and t1. Keep rate <= 3 (WCAG 2.3.1: no more
    than three flashes a second) and avoid dark/light alternation."""
    if t0 <= t < t1:
        k = int((t - t0) * rate)
        slab(c, colors[k % len(colors)])


# ---------------------------------------------------------------- halftone fields (abstract)
_grid = {}


def _disc(R, step):
    key = (R, step)
    if key not in _grid:
        n = int(R / step) + 1
        xs = np.arange(-n, n + 1) * step
        X, Y = np.meshgrid(xs, xs)
        X = X + (np.arange(len(xs))[:, None] % 2) * step / 2          # hex-ish packing
        m = X ** 2 + Y ** 2 < R ** 2
        _grid[key] = (X[m], Y[m])
    return _grid[key]


def _points(c, xs, ys, rs, color, a):
    """Dots of varying radius, bucketed so each bucket is one drawPoints call."""
    if a <= 0.003 or len(xs) == 0:
        return
    edges = np.linspace(0, rs.max() + 1e-6, 9)
    idx = np.digitize(rs, edges)
    for b in range(1, len(edges)):
        sel = idx == b
        if not sel.any():
            continue
        r = (edges[b - 1] + edges[b]) / 2
        if r < 0.4:
            continue
        p = paint(color, a, stroke=2 * r, cap='round')
        c.drawPoints(skia.Canvas.kPoints_PointMode, [skia.Point(float(x), float(y)) for x, y in zip(xs[sel], ys[sel])], p)


def globe(c, cx, cy, R, t, spin=0.0, sea='cobalt', air='orange', a=1.0, step=13, reveal=1.0, air_amt=1.0, tilt=0.38, hollow=0.0):
    """A halftone planet: an abstract swirl field on an orthographic sphere (art, not data).
    spin turns it (radians); reveal grows it from the centre; hollow empties it from the centre (0..1)."""
    if a <= 0.003 or reveal <= 0:
        return
    X, Y = _disc(R, step)
    x, y = X / R, Y / R
    z = np.sqrt(np.clip(1 - x * x - y * y, 0, 1))
    # tilt about the x axis, then latitude / longitude
    yy = y * math.cos(tilt) + z * math.sin(tilt)
    zz = -y * math.sin(tilt) + z * math.cos(tilt)
    lat = np.arcsin(np.clip(-yy, -1, 1))
    lon = np.arctan2(x, zz) + spin
    f = 0.5 + 0.5 * (np.sin(3 * lon + 2.2 * np.sin(2 * lat) + 0.6 * t) * np.cos(lat) * 0.7
                     + 0.3 * np.sin(5 * lat - 2 * lon - 0.4 * t))
    g = np.sin(4 * lon - 3 * np.sin(3 * lat) - 1.1 * t) * np.cos(1.5 * lat) + 0.5 * np.sin(7 * lat + lon + 0.8 * t)
    shade = 0.35 + 0.65 * z
    r = step * 0.5 * (0.18 + 0.82 * f) * shade
    d = np.sqrt(x * x + y * y)
    vis = d < reveal * 1.08
    if hollow > 0:
        vis &= d > hollow * 1.1 - 0.1
    pop = np.clip((reveal * 1.08 - d) / 0.12, 0, 1)
    r = r * pop
    cloud = (g > 1.05 - 0.55 * air_amt) & vis
    oc = vis & ~cloud
    _points(c, cx + X[oc], cy + Y[oc], r[oc], sea, a)
    _points(c, cx + X[cloud], cy + Y[cloud], r[cloud] * 1.05, air, a)


def flow(c, x0, y0, w, h, t, color='orange', a=1.0, step=34, seg=22, width=4, phase=0.0):
    """Short strokes along an abstract swirling flow, drifting with time (an atmosphere, as art)."""
    if a <= 0.003:
        return
    p = paint(color, a, stroke=width, cap='round')
    pth = skia.Path()
    for j in range(int(h / step)):
        for i in range(int(w / step)):
            x = x0 + (i + 0.5) * step + 6 * math.sin(j * 1.3)
            y = y0 + (j + 0.5) * step
            u, v = x / 260.0, y / 260.0
            ang = math.sin(u * 2.1 + t * 0.9 + phase) * 1.6 + math.cos(v * 2.7 - t * 0.6) * 1.2
            L = seg * (0.55 + 0.45 * math.sin(u * 3 + v * 2 + t * 2.0))
            pth.moveTo(x - math.cos(ang) * L / 2, y - math.sin(ang) * L / 2)
            pth.lineTo(x + math.cos(ang) * L / 2, y + math.sin(ang) * L / 2)
    c.drawPath(pth, p)


def waves(c, x0, y0, w, h, t, color='paper', a=1.0, rows=7, width=4, amp=14):
    """Stacked wavy lines (an ocean, as art)."""
    if a <= 0.003:
        return
    p = paint(color, a, stroke=width)
    for k in range(rows):
        y = y0 + h * (k + 0.5) / rows
        pth = skia.Path()
        for i in range(0, int(w) + 1, 12):
            xx = x0 + i
            yy = y + amp * math.sin(i / 70 + t * 1.6 + k * 0.9) * (0.6 + 0.4 * math.sin(i / 230 - t * 0.5 + k))
            (pth.moveTo if i == 0 else pth.lineTo)(xx, yy)
        c.drawPath(pth, p)


def network(c, x0, y0, w, h, t, color='ink', hot='orange', a=1.0, cols=6, rows=5, seed=1, speed=1.0):
    """A layered network of nodes and edges with pulses running along it (abstract, not any real model)."""
    if a <= 0.003:
        return
    xs = [x0 + w * i / (cols - 1) for i in range(cols)]
    ys = [y0 + h * j / (rows - 1) for j in range(rows)]
    p = paint(color, a * 0.35, stroke=1.6)
    for i in range(cols - 1):
        for j in range(rows):
            for k in range(rows):
                if _hash(seed, i, j, k) < 0.42:
                    c.drawLine(xs[i], ys[j], xs[i + 1], ys[k], p)
    # pulses
    for q in range(10):
        ph = (t * 0.55 * speed + q / 10) % 1.0
        i = int(ph * (cols - 1))
        u = ph * (cols - 1) - i
        j = int(_hash(seed + 5, q, i) * rows)
        k = int(_hash(seed + 5, q, i + 1) * rows)
        x = lerp(xs[i], xs[i + 1], u)
        y = lerp(ys[j], ys[k], u)
        c.drawLine(xs[i], ys[j], x, y, paint(hot, a * 0.9, stroke=3.5))
        circle(c, x, y, 7, fill=hot, a=a)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            circle(c, x, y, 11, fill='paper', stroke=color, sw=3, a=a)


def thermometer(c, x, y, h, level, color='paper', fill='ink', a=1.0, sw=8):
    """A thermometer glyph: tube from (x, y) down h px to a bulb; level 0..1."""
    if a <= 0.003:
        return
    r = sw * 2.4
    tube = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - sw * 1.4, y, sw * 2.8, h), sw * 1.4, sw * 1.4)
    c.drawRRect(tube, paint(color, a))
    circle(c, x, y + h + r * 0.6, r * 1.25, fill=color, a=a)
    c.drawRect(skia.Rect.MakeXYWH(x - sw * 0.6, y + h - (h - sw) * level, sw * 1.2, (h - sw) * level + sw), paint(fill, a))
    circle(c, x, y + h + r * 0.6, r * 0.8, fill=fill, a=a)
    for k in range(1, 6):
        yy = y + h * k / 6
        c.drawLine(x + sw * 2.2, yy, x + sw * 3.6, yy, paint(color, a, stroke=4))
