"""Crop the paper's figures into data/ as PNGs (the build reads only data/, never the PDF).

  python projects/cldiff/videos/explainer/extract_paper.py [paper.pdf]

Scheinker & Williams, "Adaptive conditional latent diffusion maps beam loss to 2D phase space projections",
arXiv:2502.18684. Most figures are raster images in the PDF, so they are shown as crops, never redrawn.
Clip rectangles are PDF points (x0, y0, x1, y1) on the given 1-based page, captions excluded, and are specific
to this arXiv version. Also writes out/crops_sheet.png, a contact sheet for checking the crops by eye.
"""
import os, sys
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data')
DPI = 300

CROPS = {
    'fig1':       (2, (54, 56, 558, 301)),     # overview: BCM readings -> latent diffusion -> VAE decoder -> projections
    'fig1_top':   (2, (54, 56, 558, 194)),     # LANSCE layout + panel A (signal along the accelerator)
    'fig1_D':     (2, (308, 196, 558, 301)),   # panel D: example (z,E) and (x,y) projections
    'fig2':       (2, (54, 403, 302, 468)),    # inductive beam current monitor
    'fig3':       (4, (55, 54, 559, 258)),     # VAE + latent diffusion pipeline
    'fig4':       (4, (61, 330, 565, 531)),    # 8 projections, their 8x8x3 latents and RGB channels
    'fig5':       (5, (54, 102, 302, 509)),    # VAE architecture stack
    'fig6_true':  (6, (54, 56, 558, 346)),     # 15 true projections at module 48
    'fig6_gen':   (6, (54, 358, 558, 645)),    # 15 generated projections
    'fig7':       (7, (54, 54, 558, 263)),     # (phi,E) true / pred / difference / latent along LANSCE
    'fig8':       (7, (54, 300, 558, 505)),    # error histograms: VAE, latent diffusion, end to end
    'fig9':       (8, (54, 54, 558, 300)),     # sigma fits, train vs test
    'fig10':      (9, (54, 54, 558, 336)),     # error vs module and projection
    'fig11':      (11, (54, 56, 558, 238)),    # adaptive tuning loop
    'fig12':      (12, (54, 78, 558, 420)),    # tracking results at modules 28, 38, 48
}

def main():
    doc = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'paper', 'paper.pdf'))
    os.makedirs(DATA, exist_ok=True)
    thumbs = []
    for name, (page, rect) in CROPS.items():
        pix = doc[page - 1].get_pixmap(dpi=DPI, clip=pymupdf.Rect(*rect))
        out = os.path.join(DATA, name + '.png')
        pix.save(out)
        im = Image.open(out).convert('RGB')
        im.thumbnail((620, 420))
        thumbs.append((name, im))
        print(f'{name:10s} p{page}  {pix.width}x{pix.height}')
    cols, cw, ch = 3, 640, 450
    sheet = Image.new('RGB', (cols * cw, ((len(thumbs) + cols - 1) // cols) * ch), (40, 40, 40))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(thumbs):
        x, y = (i % cols) * cw + 10, (i // cols) * ch + 24
        sheet.paste(im, (x, y))
        d.text((x, y - 18), name, fill=(255, 220, 120))
    os.makedirs(os.path.join(ROOT, 'out'), exist_ok=True)
    sheet.save(os.path.join(ROOT, 'out', 'crops_sheet.png'))

if __name__ == '__main__':
    main()
