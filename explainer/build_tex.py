"""Typeset the project's equations (eqs.py: EQS key -> LaTeX, COLORS name -> hex) into tex/<key>.png.

Each equation is rendered at 1600 dpi with a transparent background, in the Fourier (Utopia) math font, and
drawn later with core.tex(c, key, ...). Skips the work when eqs.py hasn't changed since the last build.
Needs `tectonic` on PATH.
"""
import hashlib, importlib, json, os, subprocess
import pymupdf
from . import project

PREAMBLE = r'''\documentclass[border=1pt,multi=preview]{standalone}
\usepackage{amsmath,amssymb}
\usepackage{xcolor}
\usepackage{fourier}
%s
\begin{document}
\color{W}
%s
\end{document}'''

def main(force=False):
    P = project.get()
    src_path = P.path('eqs.py')
    if not os.path.exists(src_path):
        print('no eqs.py; nothing to typeset')
        return
    digest = hashlib.sha1(open(src_path, 'rb').read()).hexdigest()
    D = P.tex
    os.makedirs(D, exist_ok=True)
    meta_path = os.path.join(D, 'meta.json')
    eqs = importlib.import_module('eqs')
    EQS, COLORS = eqs.EQS, eqs.COLORS
    keys = list(EQS)
    if not force and os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        have = all(os.path.exists(os.path.join(D, k + '.png')) for k in keys) and set(keys) <= set(meta)
        if meta.get('_source') == digest or (have and '_source' not in meta):
            if '_source' not in meta:            # first run under this tool: record the source it matches
                meta['_source'] = digest
                json.dump(meta, open(meta_path, 'w'))
            print('equations up to date')
            return
    body = '\n'.join(r'\begin{preview}$\displaystyle ' + EQS[k] + r'$\end{preview}' for k in keys)
    cols = '\n'.join(r'\definecolor{%s}{HTML}{%s}' % kv for kv in COLORS.items())
    open(os.path.join(D, 'eqs.tex'), 'w').write(PREAMBLE % (cols, body))
    r = subprocess.run(['tectonic', 'eqs.tex'], cwd=D, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-3000:])
    doc = pymupdf.open(os.path.join(D, 'eqs.pdf'))
    assert doc.page_count == len(keys), (doc.page_count, len(keys))
    meta = {}
    for k, p in zip(keys, doc):
        pix = p.get_pixmap(dpi=1600, alpha=True)
        pix.save(os.path.join(D, k + '.png'))
        meta[k] = (pix.width, pix.height)
    meta['_source'] = digest
    json.dump(meta, open(meta_path, 'w'))
    print(f'typeset {len(keys)} equations')
