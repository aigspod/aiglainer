"""Extract figure data from the LAWFUL paper PDF into data/.

  make data P=lawful     (or: python projects/lawful/extract_paper.py)

fig4.json    curves of Fig. 4a/4b, read from the PDF's vector paths and mapped to data units
rasters.json Fig. 3 spectrograms and Fig. 5 attention maps (viridis inverted back to values),
             plus the Fig. 3 Doppler-centroid curves (vector paths, panel-normalized)

Page indices, drawing indices, image xrefs and axis calibrations are specific to arXiv:2607.28672v1.
"""
import json, os, sys
import numpy as np
import pymupdf
from PIL import Image
from matplotlib import colormaps
from scipy.spatial import cKDTree

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')

def path_points(dr):
    out = []
    for it in dr['items']:
        if it[0] == 'l':
            if not out:
                out.append((it[1].x, it[1].y))
            out.append((it[2].x, it[2].y))
        elif it[0] == 'c':
            if not out:
                out.append((it[1].x, it[1].y))
            out.append((it[4].x, it[4].y))
    return out

def fig4(doc):
    drs = doc[7].get_drawings()
    res = {}
    # panel (a): x from -2..2 spans the curve extent; y tick centres 0.00 -> 121.95pt, 0.75 per 23.2pt
    x0, x1 = 118.568115234375, 225.6711883544922
    for name, idx in (('g', 71), ('f', 72), ('C', 73), ('V', 74)):
        res['a_' + name] = [(round(-2 + 4 * (x - x0) / (x1 - x0), 4), round((121.95 - y) / 23.2 * 0.75, 4)) for x, y in path_points(drs[idx])]
    # panel (b): 0.00 -> 310.05pt, 1.00 per 84pt
    x0, x1 = 114.90704345703125, 227.5262908935547
    for name, idx in (('g', 183), ('f', 184), ('C', 185), ('V', 186)):
        res['b_' + name] = [(round(-2 + 4 * (x - x0) / (x1 - x0), 4), round((310.05 - y) / 84.0, 4)) for x, y in path_points(drs[idx])]
    return res

def rasters(doc):
    lut = colormaps['viridis'](np.linspace(0, 1, 256))[:, :3] * 255
    tree = cKDTree(lut)

    def inv(xref):
        pix = pymupdf.Pixmap(doc, xref)
        if pix.n > 3 or pix.alpha:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3].astype(float)
        d, i = tree.query(a.reshape(-1, 3))
        print(f'  xref {xref}: mean colour error {d.mean():.2f}')
        return (i / 255.0).reshape(a.shape[:2])

    spec = {}
    for k, x in zip(['gt', 'model', 'cf_model', 'cf_circuit', 'cf_complement'], [692, 693, 694, 695, 696]):
        v = inv(x)
        spec[k] = np.asarray(Image.fromarray((v * 255).astype(np.uint8)).resize((140, 140), Image.BILINEAR)).tolist()
    heads = {}
    for h, x in zip(range(8), [681, 683, 684, 685, 686, 687, 688, 689]):
        v = inv(x)
        idx = ((np.arange(32) + 0.5) * v.shape[0] / 32).astype(int)
        heads[f'h{h}'] = (v[np.ix_(idx, idx)] * 0.04).round(5).tolist()   # colourbar spans 0..0.04
    drs = doc[6].get_drawings()
    rects = {24: (179.9278, 242.5095), 38: (272.0702, 334.6518), 52: (348.6115, 411.1931), 66: (425.1528, 487.7345)}
    y0, y1 = 97.34442, 159.92604
    cent = {}
    for idx, name in zip([24, 38, 52, 66], ['model', 'cf_model', 'cf_circuit', 'cf_complement']):
        cent[name] = [((it[1].x - rects[idx][0]) / (rects[idx][1] - rects[idx][0]), (it[1].y - y0) / (y1 - y0))
                      for it in drs[idx]['items'] if it[0] == 'l']
    return {'spec': spec, 'cent': cent, 'heads': heads}

if __name__ == '__main__':
    doc = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'paper', '2607.28672v1.pdf'))
    os.makedirs(DATA, exist_ok=True)
    json.dump(fig4(doc), open(os.path.join(DATA, 'fig4.json'), 'w'))
    json.dump(rasters(doc), open(os.path.join(DATA, 'rasters.json'), 'w'))
    print('wrote', DATA)
