"""Getting real data out of a paper's figures, so charts are redrawn from numbers rather than eyeballed.

  python -m explainer inspect paper.pdf 8      # list page 8's vector paths and images (1-based page)

Most arXiv figures made with matplotlib keep their curves as vector paths: read the points with
`path_points`, then map them to data units with two known tick positions (`axis_map`). Heatmaps and
spectrograms are usually embedded rasters: pull them out by xref with `image` and turn the colours back into
values with `invert_colormap`. projects/lawful/extract_paper.py is a worked example.
"""
import numpy as np

def open_pdf(path):
    import pymupdf
    return pymupdf.open(path)

def inspect(path, page, min_items=5):
    """Print the page's coloured multi-segment paths (likely data curves) and embedded images."""
    doc = open_pdf(path)
    p = doc[int(page) - 1]
    print(f'page {page}: {p.rect}')
    print('\nvector paths (index, stroke colour, width, dashes, segments, bbox):')
    for i, d in enumerate(p.get_drawings()):
        if d.get('color') and len(d['items']) >= int(min_items):
            colr = '#%02x%02x%02x' % tuple(int(255 * v) for v in d['color'][:3])
            print(f'  {i:4d}  {colr}  w={d.get("width") or 0:.2f}  dashes={d.get("dashes")}  n={len(d["items"])}  {d["rect"]}')
    print('\nimages (xref, size, placement):')
    for im in p.get_images(full=True):
        xref = im[0]
        print(f'  xref {xref}  {im[2]}x{im[3]}  {p.get_image_rects(xref)}')
    print('\nshort numeric labels (likely axis ticks: use two of them with axis_map):')
    import re
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for sp in l['spans']:
                t = sp['text'].strip().replace('\u2212', '-')
                if t and len(t) <= 6 and re.fullmatch(r'-?[\d.]+', t):
                    x0, y0, x1, y1 = sp['bbox']
                    print(f'  {t:>6s}  centre x={(x0 + x1) / 2:7.1f}  y={(y0 + y1) / 2:7.1f}')

def path_points(drawing):
    """Polyline vertices of a pymupdf drawing (line and curve end points), in PDF points."""
    out = []
    for it in drawing['items']:
        if it[0] == 'l':
            if not out:
                out.append((it[1].x, it[1].y))
            out.append((it[2].x, it[2].y))
        elif it[0] == 'c':
            if not out:
                out.append((it[1].x, it[1].y))
            out.append((it[4].x, it[4].y))
    return np.array(out)

def axis_map(p0, v0, p1, v1):
    """Linear map from page coordinate to data value, given two (position, value) pairs, e.g. two ticks."""
    return lambda p: v0 + (np.asarray(p, float) - p0) * (v1 - v0) / (p1 - p0)

def image(doc, xref):
    """An embedded image as an (h, w, 3) uint8 array."""
    import pymupdf
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n > 3 or pix.alpha:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]

def invert_colormap(rgb, cmap='viridis', vmin=0.0, vmax=1.0):
    """Recover values from a colormapped image by nearest colour. Returns (values, mean colour error);
    an error under ~2/255 means the colormap guess is right."""
    from matplotlib import colormaps
    from scipy.spatial import cKDTree
    lut = colormaps[cmap](np.linspace(0, 1, 256))[:, :3] * 255
    d, i = cKDTree(lut).query(np.asarray(rgb, float).reshape(-1, 3))
    vals = (i / 255.0).reshape(np.asarray(rgb).shape[:2])
    return vmin + vals * (vmax - vmin), float(d.mean())
