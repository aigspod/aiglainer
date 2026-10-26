"""Reusable motion-graphics building blocks."""
import math
import numpy as np
import skia
from .core import *

MX = 120  # side margin

def header(c, t, num, kick, title, t0=0.15, out=None, y=168, size=64, sub=None):
    """Section header in the site's style: '01 / the question' label, light Fraunces title.
    Wrap one word of the title in *asterisks* for the amber italic word with a hand-drawn swash."""
    from .notes import swash
    a = window(t, t0, out, 0.7, 0.5)
    if a <= 0:
        return
    k = ramp(t, t0, 0.9, e_expo)
    w = text(c, f'{num} / ', MX, y, 18, 400, 'y', a * k, kind='mono', tracking=0.14)
    text(c, kick.lower(), MX + w, y, 18, 400, 'muted', a * k, kind='mono', tracking=0.14)
    kt = ramp(t, t0 + 0.15, 0.9, e_expo)
    yy = y + 76 + (1 - kt) * 24
    x = MX
    parts = title.split('*')
    for i, part in enumerate(parts):
        if not part:
            continue
        if i % 2:      # emphasised word
            wd = text(c, part, x, yy, size, 400, 'y', a * kt, kind='italic')
            swash(c, x - 4, x + wd + 6, yy + 16, 'y', a * kt, ramp(t, t0 + 0.6, 0.7, e_io))
        else:
            wd = text(c, part, x, yy, size, 700, 'ink', a * kt, tracking=-0.005)
        x += wd
    if sub:
        ks = ramp(t, t0 + 0.45, 0.8)
        text(c, sub, MX, y + 124 + (1 - ks) * 12, 27, 400, 'muted', a * ks)

def caption(c, t, s, t0, t1, y=985, size=31, maxw=1500, x=W / 2, align='center', base='ink'):
    a = window(t, t0, t1, 0.5, 0.45)
    if a <= 0:
        return
    rich(c, s, x, y, size, maxw, t, t0, 0.03, 0.5, a, align, base=base)

def note(c, s, x, y, a=1.0, size=18, color='muted', align='left'):
    text(c, s, x, y, size, 500, color, a, align, kind='mono', tracking=0.04)

def pill(c, x, y, s, color, a=1.0, scale=1.0, filled=True, size=18, cx=False):
    if a <= 0:
        return
    w = text_width(s.lower(), size, 400, 'mono', 0.12) + 30
    h = size + 18
    with xform(c, x if not cx else x - w / 2, y, scale, 0, w / 2, h / 2):
        if filled:
            rrect(c, 0, 0, w, h, h / 2, fill=color, a=a, fa=a * 0.18)
        rrect(c, 0, 0, w, h, h / 2, stroke=color, sw=1.6, a=a)
        text(c, s.lower(), 15, h / 2 + size * 0.36, size, 400, color, a, kind='mono', tracking=0.12)
    return w

def panel(c, x, y, w, h, a=1.0, r=18, stroke='line', fill='panel', fa=0.72):
    rrect(c, x, y, w, h, r, fill=fill, a=a, fa=a * fa)
    rrect(c, x, y, w, h, r, stroke=stroke, sw=1.4, a=a)

def radar_icon(c, x, y, s=1.0, a=1.0, t=0.0, ping=True, direction=0.0, color='g'):
    """A small radar: base + dish, emitting arcs toward `direction` (radians, 0 = +x)."""
    if a <= 0:
        return
    with xform(c, x, y, s):
        # stand
        line(c, 0, 0, 0, 34, 'muted', a, 3)
        line(c, -16, 38, 16, 38, 'muted', a, 3)
        c.save()
        c.rotate(math.degrees(direction))
        pth = skia.Path()
        pth.addArc(skia.Rect.MakeXYWH(-26, -26, 52, 52), 120, 120)
        c.drawPath(pth, paint(color, a, stroke=4))
        circle(c, 0, 0, 5, fill=color, a=a, glow=6)
        if ping:
            for k in range(3):
                ph = ((t * 0.8 + k / 3) % 1.0)
                r = 30 + ph * 120
                aa = a * (1 - ph) ** 1.5 * 0.9
                arc = skia.Path()
                arc.addArc(skia.Rect.MakeXYWH(-r, -r, 2 * r, 2 * r), -32, 64)
                c.drawPath(arc, paint(color, aa, stroke=2.5))
        c.restore()

class Axes:
    def __init__(self, x, y, w, h, xr, yr):
        self.x, self.y, self.w, self.h, self.xr, self.yr = x, y, w, h, xr, yr

    def px(self, xv, yv):
        X = self.x + (np.asarray(xv, float) - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w
        Y = self.y + self.h - (np.asarray(yv, float) - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h
        return X, Y

    def pts(self, xs, ys):
        X, Y = self.px(xs, ys)
        return np.stack([X, Y], 1)

    def draw(self, c, a, xticks, yticks, xlabel=None, ylabel_key=None, prog=1.0, fmt='{:.2f}', xfmt='{:g}', zero=True, grid=True):
        if a <= 0:
            return
        k = prog
        if grid:
            for yv in yticks:
                _, Y = self.px(0, yv)
                line(c, self.x, Y, self.x + self.w * k, Y, 'line', a * 0.7, 1)
            for xv in xticks:
                X, _ = self.px(xv, 0)
                line(c, X, self.y + self.h, X, self.y + self.h - self.h * k, 'line', a * 0.7, 1)
        if zero and self.yr[0] < 0 < self.yr[1]:
            _, Y0 = self.px(0, 0)
            line(c, self.x, Y0, self.x + self.w * k, Y0, 'muted', a * 0.6, 1.4)
        if zero and self.xr[0] < 0 < self.xr[1]:
            X0, _ = self.px(0, 0)
            line(c, X0, self.y + self.h, X0, self.y + self.h * (1 - k), 'muted', a * 0.6, 1.4)
        line(c, self.x, self.y + self.h, self.x + self.w * k, self.y + self.h, 'muted', a, 1.6)
        line(c, self.x, self.y + self.h, self.x, self.y + self.h * (1 - k), 'muted', a, 1.6)
        for xv in xticks:
            X, _ = self.px(xv, 0)
            text(c, xfmt.format(xv).replace('-', '−'), X, self.y + self.h + 34, 22, 500, 'muted', a * k, 'center', kind='mono')
        for yv in yticks:
            _, Y = self.px(0, yv)
            text(c, fmt.format(yv).replace('-', '−'), self.x - 14, Y + 7, 22, 500, 'muted', a * k, 'right', kind='mono')

def stat(c, x, y, big, small, color='y', a=1.0, size=78, align='left', k=1.0):
    if a <= 0:
        return
    text(c, big, x, y + (1 - k) * 18, size, 760, color, a * k, align, tracking=-0.02)
    text(c, small, x, y + 44, 24, 500, 'muted', a * k, align)

def smooth_curve(pts, n=400):
    """Cubic (Catmull-Rom) resample of a polyline (x increasing)."""
    pts = np.asarray(pts, float)
    from scipy.interpolate import CubicSpline
    x, y = pts[:, 0], pts[:, 1]
    keep = np.concatenate([[True], np.diff(x) > 1e-6])
    cs = CubicSpline(x[keep], y[keep])
    xs = np.linspace(x[0], x[-1], n)
    return np.stack([xs, cs(xs)], 1)

def legend_item(c, x, y, color, label, a=1.0, dash=False, size=24):
    line(c, x, y - 8, x + 40, y - 8, color, a, 4, dash=[9, 6] if dash else None)
    text(c, label, x + 54, y, size, 500, 'ink', a)

def number(c, val, x, y, size=80, color='y', a=1.0, fmt='{:.3f}', align='left', weight=760, kind='sans'):
    return text(c, fmt.format(val).replace('-', '−'), x, y, size, weight, color, a, align, kind=kind, tracking=-0.01)

def flow_dots(c, pts, t, color, a=1.0, n=3, speed=0.35, r=4.5, glow=8):
    """Pulses travelling along a polyline."""
    if a <= 0:
        return
    for k in range(n):
        u = (t * speed + k / n) % 1.0
        p = end_point(pts, u)
        fade = math.sin(math.pi * u)
        circle(c, p[0], p[1], r, fill=color, a=a * fade, glow=glow)
