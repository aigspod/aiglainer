"""The look of the jazz edition: a late-night record sleeve. Soft, chunky Fraunces (its SOFT and WONK axes turned up)
for display, Fraunces italic for the warm words, Inter for body text, Space Mono for tiny labels; cream paper, deep
navy and teal, mustard, terracotta, sage and rose (THEME tokens in project.py); slow eases, soft rises and fades, a
spinning record. Everything that looks like data here is abstract art, and the scenes label it `illustration`.
"""
import functools, math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.core import _var, FONT_DIR

PAD = 140          # side margin


# ---------------------------------------------------------------- type
def _face(kind, weight, size):
    path = FONT_DIR + ('/Fraunces-Italic.ttf' if kind == 'ital' else '/Fraunces.ttf')
    return _var(path, wght=clamp(weight, 100, 900), opsz=clamp(size, 9, 144), SOFT=100, WONK=1)


@functools.lru_cache(maxsize=512)
def _font(kind, weight, size):
    if kind in ('disp', 'ital'):
        f = skia.Font(_face(kind, weight, size), size)
    else:
        f = skia.Font(_var(FONT_DIR + '/Inter.ttf', wght=clamp(weight, 100, 900), opsz=clamp(size, 14, 32)), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setHinting(skia.FontHinting.kNone)
    return f


@functools.lru_cache(maxsize=4096)
def _runs(s, kind, weight, size):
    """Per-character fallback: Fraunces lacks a few glyphs (₂), which come from Inter."""
    chain = [_font(kind, weight, size), _font('body', min(weight, 700), size)]
    out = []
    for ch in s:
        f = next((f for f in chain if ch.isspace() or f.textToGlyphs(ch)[0]), chain[-1])
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return tuple((t, f) for t, f in out)


def tw(s, size, weight=620, kind='disp', track=-0.01):
    return sum(f.measureText(t) for t, f in _runs(s, kind, weight, size)) + track * size * max(0, len(s) - 1)


def fit(s, size, maxw, weight=620, kind='disp', track=-0.01):
    w = tw(s, size, weight, kind, track)
    return size if w <= maxw else size * maxw / w


def say(c, s, x, y, size, color='paper', a=1.0, align='left', weight=620, kind='disp', track=-0.01, shadow=0.0):
    """One line of type; y is the baseline. kind: 'disp' (soft Fraunces), 'ital' (its italic) or 'body' (Inter)."""
    if a <= 0.003 or not s:
        return 0
    w = tw(s, size, weight, kind, track)
    x0 = x - w / 2 if align == 'center' else x - w if align == 'right' else x
    if shadow:
        _draw(c, s, x0 + size * 0.03, y + size * 0.04, size, kind, weight, track, paint('shadow', a * shadow, blur=size * 0.05))
    _draw(c, s, x0, y, size, kind, weight, track, paint(color, a))
    return w


def _draw(c, s, x, y, size, kind, weight, track, p):
    for t, f in _runs(s, kind, weight, size):
        if track == 0:
            c.drawString(t, x, y, f, p)
            x += f.measureText(t)
            continue
        xs = []
        for wd in f.getWidths(f.textToGlyphs(t)):
            xs.append(x)
            x += wd + track * size
        c.drawTextBlob(skia.TextBlob.MakeFromPosTextH(t, xs, 0, f), 0, y, p)


def label(c, s, x, y, size=20, color='paper', a=1.0, align='left', bold=False, track=0.16):
    return text(c, s, x, y, size, 700 if bold else 400, color, a, align, 'mono', track)


def illustration(c, x, y, color='paper', a=1.0, align='left'):
    label(c, 'illustration', x, y, 17, color, a * 0.75, align, track=0.12)


def wrap(s, size, maxw, weight=620, kind='disp'):
    lines, cur = [], ''
    for w in s.split():
        trial = (cur + ' ' + w).strip()
        if cur and tw(trial, size, weight, kind) > maxw:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + [cur]


# ---------------------------------------------------------------- gentle motion
def soft(t, t0, d=0.9, out=None, d_out=0.6):
    """(alpha, rise) for something that drifts up into place at t0 and, optionally, fades away at `out`."""
    k = ramp(t, t0, d, e_out)
    a = k
    if out is not None:
        a *= 1 - ramp(t, out, d_out, e_io)
    return a, (1 - k) * 26


def rise(c, t, t0, s, x, y, size, color='paper', align='left', weight=620, kind='disp', out=None, d=0.9, shadow=0.0):
    """A line of type that rises softly into place."""
    a, dy = soft(t, t0, d, out)
    return say(c, s, x, y + dy, size, color, a, align, weight, kind, shadow=shadow)


def words(c, t, t0, s, x, y, size, color='paper', weight=620, kind='disp', stagger=0.14, out=None, align='left'):
    """A line whose words rise in one after another (left-aligned, or centred as a whole)."""
    ws = s.split(' ')
    space = tw(' ', size, weight, kind)
    total = sum(tw(w, size, weight, kind) for w in ws) + space * (len(ws) - 1)
    xx = x - total / 2 if align == 'center' else x
    for k, w in enumerate(ws):
        a, dy = soft(t, t0 + k * stagger, 0.8, out)
        say(c, w, xx, y + dy, size, color, a, 'left', weight, kind)
        xx += tw(w, size, weight, kind) + space
    return total


class at:
    """with at(c, x, y, s): scale (and rotate, degrees) about (x, y)."""
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


# ---------------------------------------------------------------- grounds and transitions
def slab(c, color, a=1.0, x=0, y=0, w=W, h=H):
    if a > 0.003:
        c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(color, a))


def iris(c, t, prev, cx, cy, d=1.3, t0=0.0):
    """Open this scene's ground over the previous scene's colour as a growing circle from (cx, cy).
    Draw the scene's ground first; this paints the previous colour outside the circle while it grows."""
    k = ramp(t, t0, d, e_io)
    if k >= 1:
        return
    r = 2300 * k
    pth = skia.Path()
    pth.addRect(skia.Rect.MakeWH(W, H))
    pth.addCircle(cx, cy, r)
    pth.setFillType(skia.PathFillType.kEvenOdd)
    c.drawPath(pth, paint(prev))


def glow(c, cx, cy, r, color='mustard', a=0.25):
    """A soft pool of warm light."""
    if a <= 0.003:
        return
    p = skia.Paint(AntiAlias=True)
    p.setShader(skia.GradientShader.MakeRadial((cx, cy), r, [col(color, a), col(color, a * 0.35), col(color, 0)], [0, 0.45, 1]))
    c.drawCircle(cx, cy, r, p)


def vignette(c, a=0.35):
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.72, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), col('shadow', a)], [0, 0.55, 1]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)


def _hash(*k):
    v = math.sin(sum((i + 1) * 12.9898 * x for i, x in enumerate(k)) + 78.233) * 43758.5453
    return v - math.floor(v)


def stars(c, t, a=1.0, n=70, color='paper', seed=3, y1=H):
    """A sparse night sky. Each star breathes slowly (a period of seconds), never flashes."""
    if a <= 0.003:
        return
    for i in range(n):
        x, y = _hash(seed, i, 1) * W, _hash(seed, i, 2) * y1
        r = 1.2 + 2.2 * _hash(seed, i, 3) ** 3
        b = 0.35 + 0.35 * math.sin(t * (0.5 + 0.7 * _hash(seed, i, 4)) + 6.28 * _hash(seed, i, 5))
        circle(c, x, y, r, fill=color, a=a * b * 0.8)


# ---------------------------------------------------------------- the record
def record(c, cx, cy, R, t, spin=0.0, label_col='terra', a=1.0, inner=None, sheen=0.6, label_text='THE AIGS POD  ·  JAZZ EDITION  ·  ', lab=0.36):
    """A vinyl record: grooves, a sheen that stays put while it turns, a label (or `inner(c, cx, cy, r)`, drawn in the
    label's place and clipped to it). spin is in turns."""
    if a <= 0.003:
        return
    with layer(c, a):
        c.drawCircle(cx, cy, R + 3, paint('shadow', 0.35, blur=18))
        c.drawCircle(cx, cy, R, paint('#141824'))
        p = paint('#2a3044', 0.9, stroke=1.4)
        r = R * 0.95
        k = 0
        while r > R * (lab + 0.02):
            p.setColor(col('#323a52' if k % 7 else '#3b4460', 0.9))
            c.drawCircle(cx, cy, r, p)
            r -= 5.5 + 2.5 * _hash(7, k)
            k += 1
        for ang, w in ((-35, 26), (145, 26)):         # the light catching the grooves
            sh = skia.Paint(AntiAlias=True)
            sh.setShader(skia.GradientShader.MakeSweep(cx, cy, [col('paper', 0), col('paper', 0.13 * sheen), col('paper', 0)],
                                                      [0, 0.5, 1], skia.TileMode.kClamp, ang - w, ang + w))
            c.drawCircle(cx, cy, R * 0.97, sh)
        rl = R * lab
        if inner:
            c.save()
            pth = skia.Path()
            pth.addCircle(cx, cy, rl)
            c.clipPath(pth, doAntiAlias=True)
            inner(c, cx, cy, rl)
            c.restore()
        else:
            label_art(c, cx, cy, rl, spin, label_col, label_text)
        circle(c, cx, cy, max(4, R * 0.018), fill='#141824', a=1)


def label_art(c, cx, cy, rl, spin, label_col='terra', label_text='THE AIGS POD  ·  JAZZ EDITION  ·  '):
    """A record's paper label: a colour, its name turning around the edge, a fine ring."""
    circle(c, cx, cy, rl, fill=label_col, a=1)
    with at(c, cx, cy, 1, spin * 360):
        _ring_text(c, label_text, cx, cy, rl * 0.74, max(11, rl * 0.11), 'paper')
    circle(c, cx, cy, rl * 0.42, stroke='paper', sw=2, a=0.5)


def _ring_text(c, s, cx, cy, r, size, color):
    f = _font('body', 600, size)
    n = len(s)
    for i, ch in enumerate(s):
        ang = -math.pi / 2 + 2 * math.pi * i / n
        c.save()
        c.translate(cx + r * math.cos(ang), cy + r * math.sin(ang))
        c.rotate(math.degrees(ang) + 90)
        c.drawString(ch, -f.measureText(ch) / 2, 0, f, paint(color, 0.9))
        c.restore()


# ---------------------------------------------------------------- abstract art (never data)
def waves(c, x0, y0, w, h, t, color='paper', a=1.0, rows=7, width=3.5, amp=12, speed=0.6):
    """Stacked wavy lines (an ocean, as art), moving slowly."""
    if a <= 0.003:
        return
    p = paint(color, a, stroke=width)
    for k in range(rows):
        y = y0 + h * (k + 0.5) / rows
        pth = skia.Path()
        for i in range(0, int(w) + 1, 10):
            yy = y + amp * math.sin(i / 85 + t * speed + k * 0.9) * (0.6 + 0.4 * math.sin(i / 260 - t * 0.25 + k))
            (pth.moveTo if i == 0 else pth.lineTo)(x0 + i, yy)
        c.drawPath(pth, p)


def breeze(c, x0, y0, w, h, t, color='terra', a=1.0, step=40, seg=26, width=4, speed=0.35):
    """Short curved strokes along a slow swirling flow (an atmosphere, as art)."""
    if a <= 0.003:
        return
    p = paint(color, a, stroke=width, cap='round')
    pth = skia.Path()
    for j in range(int(h / step) + 1):
        for i in range(int(w / step) + 1):
            x = x0 + (i + 0.5) * step + 8 * math.sin(j * 1.3)
            y = y0 + (j + 0.5) * step
            u, v = x / 300.0, y / 300.0
            ang = math.sin(u * 2.0 + t * speed) * 1.4 + math.cos(v * 2.5 - t * speed * 0.7) * 1.1
            L = seg * (0.6 + 0.4 * math.sin(u * 3 + v * 2 + t * 0.8))
            dx, dy = math.cos(ang) * L / 2, math.sin(ang) * L / 2
            pth.moveTo(x - dx, y - dy)
            pth.quadTo(x + dy * 0.3, y - dx * 0.3, x + dx, y + dy)
    c.drawPath(pth, p)


def planet(c, cx, cy, r, t, spin=0.0, sea='teal', land='sage', air='paper', a=1.0):
    """A soft little planet: a teal sea, drifting sage patches and cream cloud strokes, all procedural."""
    if a <= 0.003:
        return
    with layer(c, a):
        c.save()
        pth = skia.Path()
        pth.addCircle(cx, cy, r)
        c.clipPath(pth, doAntiAlias=True)
        c.drawCircle(cx, cy, r, paint(sea))
        for k in range(7):                                    # patches drift east with the spin
            ph = (_hash(11, k) + spin * 0.5) % 1.0
            x = cx - r * 1.3 + ph * r * 2.6
            y = cy + (_hash(12, k) - 0.5) * r * 1.4
            rr = r * (0.18 + 0.22 * _hash(13, k))
            squash = math.sqrt(max(0.0, 1 - ((x - cx) / (r * 1.05)) ** 2))
            c.drawOval(skia.Rect.MakeXYWH(x - rr * max(squash, 0.15), y - rr * 0.7, 2 * rr * max(squash, 0.15), rr * 1.4), paint(land, 0.85))
        breeze(c, cx - r, cy - r, 2 * r, 2 * r, t, air, 0.55, step=max(18, r / 5), seg=max(10, r / 8), width=max(2, r / 70))
        sh = skia.Paint(AntiAlias=True)                       # the night side
        sh.setShader(skia.GradientShader.MakeRadial((cx - r * 0.35, cy - r * 0.4), r * 1.6,
                                                    [col('shadow', 0), col('shadow', 0.15), col('shadow', 0.6)], [0, 0.55, 1]))
        c.drawCircle(cx, cy, r, sh)
        c.restore()
        circle(c, cx, cy, r, stroke='paper', sw=2, a=0.25)


def network(c, cx, cy, r, t, color='paper', hot='mustard', a=1.0, cols=5, rows=4, seed=2):
    """A small layered network with soft pulses drifting through it (abstract, not any real model)."""
    if a <= 0.003:
        return
    w, h = r * 1.3, r * 0.95
    xs = [cx - w / 2 + w * i / (cols - 1) for i in range(cols)]
    ys = [cy - h / 2 + h * j / (rows - 1) for j in range(rows)]
    p = paint(color, a * 0.3, stroke=1.6)
    for i in range(cols - 1):
        for j in range(rows):
            for k in range(rows):
                if _hash(seed, i, j, k) < 0.45:
                    c.drawLine(xs[i], ys[j], xs[i + 1], ys[k], p)
    for q in range(6):
        ph = (t * 0.22 + q / 6) % 1.0
        i = min(int(ph * (cols - 1)), cols - 2)
        u = ph * (cols - 1) - i
        j = int(_hash(seed + 5, q, i) * rows)
        k = int(_hash(seed + 5, q, i + 1) * rows)
        circle(c, lerp(xs[i], xs[i + 1], u), lerp(ys[j], ys[k], u), max(4, r * 0.035), fill=hot, a=a, glow=6)
    for x in xs:
        for y in ys:
            circle(c, x, y, max(5, r * 0.045), fill='night', stroke=color, sw=2.5, a=a)


def arcs(c, cx, cy, r0, t, colors=('mustard', 'terra', 'sage', 'rose'), a=1.0, width=16, gap=30, grow=1.0):
    """Concentric half-rings over a horizon, mid-century style; `grow` (0..1) lets them bloom outward in turn."""
    if a <= 0.003:
        return
    for k, colr in enumerate(colors):
        g = clamp(grow * len(colors) - k)
        if g <= 0:
            continue
        r = r0 + (k + 1) * gap + k * width
        c.drawArc(skia.Rect.MakeXYWH(cx - r, cy - r, 2 * r, 2 * r), 180, 180 * e_io(g), False, paint(colr, a * 0.9, stroke=width, cap='butt'))


def sleeve(c, x, y, s, color, a=1.0, rot=0.0):
    """A square record sleeve with a soft shadow; draw its art after, inside (x, y, s, s)."""
    if a <= 0.003:
        return
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x + 6, y + 10, s, s), 6, 6), paint('shadow', 0.22 * a, blur=14))
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, s, s), 6, 6), paint(color, a))


def thermometer(c, x, y, h, level, color='paper', fill='terra', a=1.0, sw=8):
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
        c.drawLine(x + sw * 2.2, yy, x + sw * 3.6, yy, paint(color, a, stroke=3))


def swash(c, x0, y, w, prog, color='mustard', a=1.0, width=7):
    """A hand-drawn underline that draws itself in."""
    if a <= 0.003 or prog <= 0:
        return
    pts = [(x0 + w * u, y + 10 * math.sin(u * 3.0 + 0.4) - 14 * u * u) for u in np.linspace(0, 1, 60)]
    draw_poly(c, pts, color, a, width, prog=prog)
