"""Handwritten margin notes (Caveat) and other doodles in the aigspod site style.

A project lists its notes per scene name in project.NOTES; the timeline draws them on top of the scene.

Each note: t (authored scene time it starts writing), text, x, y (baseline start), optional:
  rot (deg, default -2.5), size (34), color ('pencil'), until (authored time it fades), align,
  arrow=(x0, y0, x1, y1) a wobbly hand-drawn arrow, drawn after the words.
Keep them to asides; explanations belong in the narration and the clean type.
"""
import math
import skia
from .core import *

def hand_arrow(c, x0, y0, x1, y1, color='pencil', a=1.0, prog=1.0, bend=0.25, seed=3):
    if a <= 0 or prog <= 0:
        return
    mx, my = (x0 + x1) / 2 - (y1 - y0) * bend, (y0 + y1) / 2 + (x1 - x0) * bend
    pts = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1)
           for u in [i / 30 * prog for i in range(31)]]
    pth = skia.Path()
    pth.moveTo(*pts[0])
    for p in pts[1:]:
        pth.lineTo(*p)
    c.drawPath(pth, paint(color, a * 0.9, stroke=2.2, effect=skia.DiscretePathEffect.Make(7, 1.1, seed)))
    if prog >= 0.98:
        (ax, ay), (bx, by) = pts[-4], pts[-1]
        ang = math.atan2(by - ay, bx - ax)
        for d in (-0.55, 0.5):
            c.drawLine(bx, by, bx - 15 * math.cos(ang + d), by - 15 * math.sin(ang + d), paint(color, a * 0.9, stroke=2.2))

def swash(c, x0, x1, y, color='y', a=1.0, prog=1.0, w=3.0):
    """The hand-drawn underline the site puts under its italic title word."""
    if a <= 0 or prog <= 0:
        return
    pth = skia.Path()
    pth.moveTo(x0, y + 3)
    pth.cubicTo(x0 + (x1 - x0) * 0.3, y - 7, x0 + (x1 - x0) * 0.65, y + 9, x1, y - 3)
    meas = skia.PathMeasure(pth, False)
    seg = skia.Path()
    meas.getSegment(0, meas.getLength() * prog, seg, True)
    c.drawPath(seg, paint(color, a * 0.9, stroke=w))

def draw_notes(c, notes, t):
    for n in notes:
        t0 = n['t']
        k = window(t, t0, n.get('until'), 0.3, 0.5)
        if k <= 0:
            continue
        reveal = ramp(t, t0, max(0.6, len(n['text']) * 0.045), e_lin)
        colr = n.get('color', 'pencil')
        hand(c, n['text'], n['x'], n['y'], n.get('size', 34), colr, k, n.get('rot', -2.5), reveal, n.get('align', 'left'))
        if 'arrow' in n:
            ap = ramp(t, t0 + max(0.6, len(n['text']) * 0.045), 0.5, e_out)
            hand_arrow(c, *n['arrow'], color=colr, a=k, prog=ap, bend=n.get('bend', 0.25))

def sticky(c, x, y, lines, a=1.0, rot=4.0, w=250, h=200, tag='todo'):
    """The site's yellow sticky note with a red pin."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    rrect(c, 4, 8, w, h, 4, fill='#000000', fa=a * 0.35)
    pth = skia.Path()
    pth.moveTo(0, 0); pth.lineTo(w, 0); pth.lineTo(w, h - 26); pth.lineTo(w - 26, h); pth.lineTo(0, h); pth.close()
    c.drawPath(pth, paint('sticky', a))
    text(c, tag, 20, 34, 15, 400, '#5c4f12', a, kind='mono', tracking=0.16)
    for i, ln in enumerate(lines):
        text(c, ln, 20, 82 + i * 40, 34, 600, 'sticky_ink', a, kind='hand')
    circle(c, w * 0.72, 4, 9, fill='#d06a5a', a=a)
    c.restore()

def lamp(c, x, y, s=1.0, a=1.0, on=1.0):
    """A line-drawn desk lamp with a warm pool of light, after the /mull/ header doodle."""
    if a <= 0:
        return
    with xform(c, x, y, s):
        c.drawCircle(-40, 120, 170, paint('y', a * 0.10 * on, blur=60))
        c.drawCircle(-30, 30, 60, paint('y', a * 0.18 * on, blur=30))
        p = paint('pencil', a * 0.8, stroke=2)
        c.drawLine(-120, 140, 80, 140, p)                                      # desk edge
        c.drawLine(40, 136, 60, 70, p); c.drawLine(60, 70, 10, -20, p)       # arm
        c.drawLine(28, 140, 52, 140, paint('pencil', a * 0.8, stroke=4))     # base
        head = skia.Path(); head.moveTo(10, -20); head.lineTo(-40, -6); head.lineTo(-20, 28); head.close()
        c.drawPath(head, p)
        circle(c, 60, 70, 4, stroke='pencil', sw=2, a=a * 0.8)
        circle(c, -30, 14, 6, fill='y', a=a * on, glow=10 * on)
        for i, (dx, dy) in enumerate(((-90, 128), (-70, 124), (-50, 120))):  # a small stack of papers
            c.drawLine(-110 + i * 6, dy, -40 + i * 6, dy, paint('pencil', a * 0.55, stroke=1.6))

