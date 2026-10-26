"""YouTube thumbnail: python -m aiglainer thumbnail  ->  <project>/out/thumbnail.png (1280x720) + a legibility sheet.

The project's THUMBNAIL(c) draws on the usual 1920x1080 canvas (same coordinates and helpers as scenes) over
the standard background; the result is downsampled to YouTube's 1280x720. Thumbnails are mostly seen small,
so a second image shows it at search-result (360 px) and phone (168 px) sizes; check that it still reads.
Rules of thumb: one focal image, three to five big words, high contrast, nothing important in the
bottom-right corner (YouTube puts the duration there).
"""
import os
import numpy as np
import skia
from .core import W, H, col
from .timeline import draw_background, draw_grain, _bg_image
from . import project

def render():
    P = project.get()
    if not P.THUMBNAIL:
        raise SystemExit(f'project {P.name} defines no THUMBNAIL(c)')
    s = skia.Surface(W, H)
    c = s.getCanvas()
    _bg_image()
    draw_background(c, 0.0)
    P.THUMBNAIL(c)
    draw_grain(c, 0)
    return s.makeImageSnapshot()

def _scaled(img, w, h):
    s = skia.Surface(w, h)
    s.getCanvas().drawImageRect(img, skia.Rect.MakeWH(w, h), skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    return s.makeImageSnapshot()

def main():
    P = project.get()
    os.makedirs(P.out(), exist_ok=True)
    img = render()
    thumb = _scaled(img, 1280, 720)
    path = P.path('out', 'thumbnail.png')
    thumb.save(path, skia.kPNG)
    if os.path.getsize(path) > 2_000_000:          # YouTube's limit is 2 MB
        thumb.save(path.replace('.png', '.jpg'), skia.kJPEG, 92)
    # legibility check: the thumbnail at the sizes people actually see it
    sizes = [(640, 360), (360, 203), (168, 95)]
    sheet = skia.Surface(sum(w for w, _ in sizes) + 40 * len(sizes), 400)
    c = sheet.getCanvas()
    c.clear(col('#0f0f0f'))
    x = 20
    for w, h in sizes:
        c.drawImage(_scaled(img, w, h), x, 20)
        x += w + 40
    sheet.makeImageSnapshot().save(P.path('out', 'thumbnail_sizes.png'), skia.kPNG)
    print(path)
