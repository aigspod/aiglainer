"""Save the paper's figures into data/figs/ as PNGs (the build reads only data/figs, never the PDF).

  python projects/weatherdreamer/extract_paper.py [paper.pdf]      (default: projects/weatherdreamer/paper/paper.pdf)

Duffy, Penn, Ballard, Posch & Vandal, "WeatherDreamer: Learning a World Model from Multimodal Earth Observations",
arXiv:2611.18393v1. Every figure in this PDF is one embedded raster image (no vector data), so scenes show them as
labelled crops ("Fig. N") and never redraw them; charts are drawn from numbers typed from the text and tables. The
images are written at their embedded resolution, captions excluded. Kept out of
git like the PDF (data/.gitignore). The page -> figure map below is specific to v1.
"""
import os, sys
import pymupdf

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'data', 'figs')

# 1-based page -> name (each of these pages carries exactly one large raster image)
FIGS = {4: 'fig1', 7: 'fig2', 8: 'fig3', 12: 'fig4', 14: 'fig5', 16: 'fig6', 17: 'fig7', 20: 'fig8', 21: 'fig9',
        33: 'figS1', 34: 'figS2', 40: 'figS3', 41: 'figS4', 42: 'figS5', 43: 'figS6', 44: 'figS7'}

def main():
    doc = pymupdf.open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'paper', 'paper.pdf'))
    os.makedirs(OUT, exist_ok=True)
    for page, name in FIGS.items():
        ims = [im for im in doc[page - 1].get_images(full=True)]
        big = max(ims, key=lambda im: im[2] * im[3])
        pix = pymupdf.Pixmap(doc, big[0])
        if pix.n - pix.alpha > 3:
            pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
        if pix.alpha:
            pix = pymupdf.Pixmap(pix, 0)
        path = os.path.join(OUT, name + '.png')
        pix.save(path)
        print(f'{name:6s} p{page:<3d} {pix.width}x{pix.height}')

if __name__ == '__main__':
    main()
