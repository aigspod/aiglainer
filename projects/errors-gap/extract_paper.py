"""Extract Fig. 1 of "Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?" (arXiv:2609.35686v1) into
data/fig1.json:  make data P=errors-gap   (needs the PDF in paper/).

Fig. 1 (page 5) is six panels of agreement (%) against retained edges (%), A_ok solid blue (#315b7d) and A_err dashed
red (#a64b43), nine points each. Calibration from the figure's own tick marks (drawing indices for v1):
  y: gridlines at 0 / 50 / 100 -> 159.20 / 129.97 / 100.75 pt (top row), 244.51 / 215.28 / 186.05 pt (bottom row)
  x: symmetric-log axis, ticks 0 / 0.1 / 1 / 10 / 50 -> 142.81 / 157.16 / 189.46 / 221.75 / 244.32 pt in the left
     column; the middle and right columns are offset by 125.76 and 251.51 pt. Linear between 0 and 0.1, log above.
The points sit at each circuit's retained-edge fraction as plotted, which need not equal the nominal budgets.
"""
import glob, json, math, os
import pymupdf

ROOT = os.path.dirname(os.path.abspath(__file__))
PANELS = [  # (key, title, Aok drawing, Aerr drawing, column, row)
    ('a', 'Llama: ARC-Challenge', 18, 28, 0, 0), ('b', 'Gemma: ARC-Challenge', 54, 64, 1, 0),
    ('c', 'Qwen: ARC-Challenge', 90, 100, 2, 0), ('d', 'Llama: ARC-Easy', 126, 136, 0, 1),
    ('e', 'Gemma: ARC-Easy', 162, 172, 1, 1), ('f', 'Llama: Subtraction', 198, 208, 2, 1)]
X0, X01, X1, DEC = 142.81, 157.16, 189.46, 32.29
COL = [0.0, 125.76, 251.51]
ROW = [(159.20, 100.75), (244.51, 186.05)]

def pts(dr):
    out = []
    for it in dr['items']:
        if it[0] == 'l':
            if not out:
                out.append((it[1].x, it[1].y))
            out.append((it[2].x, it[2].y))
    return out

def xval(px):
    if px <= X01:
        return 0.1 * (px - X0) / (X01 - X0)
    return 10 ** ((px - X1) / DEC)

def main():
    pdf = glob.glob(os.path.join(ROOT, 'paper', '*.pdf'))[0]
    drs = pymupdf.open(pdf)[4].get_drawings()
    out = {}
    for key, title, iok, ierr, cx, ry in PANELS:
        y0, y100 = ROW[ry]
        def conv(dr):
            return [(round(xval(x - COL[cx]), 4), round((y0 - y) / (y0 - y100) * 100, 2)) for x, y in pts(dr)]
        out[key] = dict(title=title, ok=conv(drs[iok]), err=conv(drs[ierr]))
        assert len(out[key]['ok']) == len(out[key]['err']) == 9, key
    json.dump(out, open(os.path.join(ROOT, 'data', 'fig1.json'), 'w'), indent=1)
    for k, v in out.items():
        print(k, v['title'], 'ok', [p[1] for p in v['ok']], 'err', [p[1] for p in v['err']], 'x', [p[0] for p in v['ok']])

if __name__ == '__main__':
    main()
