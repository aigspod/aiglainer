"""Our own compression check for this video's fourth file (not from the paper).

The file: 8192 pairs (X, Y), X a random row of 64 cells, Y = rule 54 applied 48 times to X (periodic boundary),
written X then Y, one pair after another: 8192 * 128 = 2^20 bits, the same size as the other three files and the
same row width and step count as the paper's Fig. 3 setup (much less data). Generic compressors (gzip, bz2, xz) are a
computable stand-in for Kolmogorov complexity; we report compressed bits per input bit, as
projects/epiplexity/lab/compress_lab.py does for zeros, coin flips and the SHA-256 generator. Rules 15 and 30 are
included for comparison. Writes ../data/ours_compress_pairs.json.
"""
import bz2, json, lzma, os, zlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS, WIDTH, STEPS = 8192, 64, 48

def eca(x, rule, k):
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    for _ in range(k):
        x = table[(np.roll(x, 1, 1) << 2) | (x << 1) | np.roll(x, -1, 1)]
    return x

def pairs(rule, seed=3):
    x = np.random.default_rng(seed).integers(0, 2, (PAIRS, WIDTH), dtype=np.uint8)
    return np.concatenate([x, eca(x, rule, STEPS)], 1).reshape(-1)

res = {}
for rule in (15, 30, 54):
    raw = np.packbits(pairs(rule)).tobytes()
    n = len(raw) * 8
    res[f'rule{rule}'] = {name: round(len(f(raw)) * 8 / n, 4) for name, f in
                          [('gzip', lambda b: zlib.compress(b, 9)), ('bz2', lambda b: bz2.compress(b, 9)),
                           ('xz', lambda b: lzma.compress(b, preset=9 | lzma.PRESET_EXTREME))]}
    print(rule, res[f'rule{rule}'])
json.dump(dict(source='our check (not the paper): compressed bits per input bit for 8192 pairs (random 64-cell row X, '
               'then rule^48(X)), 2^20 bits per file; lab/check_pairs.py', pairs=PAIRS, width=WIDTH, steps=STEPS,
               N=PAIRS * 2 * WIDTH, results=res),
          open(os.path.join(HERE, '..', 'data', 'ours_compress_pairs.json'), 'w'), indent=1)
