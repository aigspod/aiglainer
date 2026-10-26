"""LAWFUL thumbnail: the glowing marker-body a radar is watching, and the question the paper asks."""
import math
import numpy as np
from aiglainer.core import *
from aiglainer.kit import radar_icon
from aiglainer.notes import swash, sticky
import walker as WK

def draw(c):
    # focal image: a 53-marker body mid-stride, lit like the lamp, with radar pings reaching it
    cam = WK.Camera(yaw=-0.62, pitch=0.10, dist=4.2, focal=1250, cx=470, cy=600, target=(0, 0, 0.92))
    J = WK.skeleton(2.1)
    M, Wt = WK.markers(J)
    c.drawCircle(470, 600, 420, paint('y', 0.10, blur=120))
    for a, b in WK.BONES:
        P, _ = cam.project(np.array([J[a], J[b]]))
        line(c, *P[0], *P[1], 'pencil', 0.35, 3)
    P, d = cam.project(M)
    dn = (d - d.min()) / (np.ptp(d) + 1e-6)
    for i in np.argsort(-d):
        k = 1 - 0.4 * dn[i]
        circle(c, P[i, 0], P[i, 1], 8.5 * (0.8 + 0.3 * k), fill='ink', a=k, glow=14)
    rx, ry = 930, 600
    for r, a in ((150, 0.85), (250, 0.55), (350, 0.3)):
        arc = skia.Path()
        arc.addArc(skia.Rect.MakeXYWH(rx - r, ry - r, 2 * r, 2 * r), 180 - 26, 52)
        c.drawPath(arc, paint('g', a, stroke=7))
    radar_icon(c, rx, ry, 2.4, 1, 0, ping=False, direction=math.pi, color='g')
    # the question: few words, heavy enough to survive a 168 px phone thumbnail
    x0 = 1030
    text(c, 'Did it learn', x0, 430, 142, 1000, 'ink', kind='display')
    w = text(c, 'the physics?', x0, 610, 158, 1100, 'y', kind='italic')
    swash(c, x0 + 10, x0 + w, 652, 'y', 1, 1, w=9)
    tex(c, 'doppler', x0 + 175, 800, 70, 0.95, glow=6)
    sticky(c, 120, 90, ['physics as', 'ground truth'], 1, rot=-5.0, w=330, h=210)
