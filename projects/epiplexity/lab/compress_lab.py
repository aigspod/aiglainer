"""Our own compression check (not from the paper): what generic compressors (a computable stand-in for
Kolmogorov complexity) say about different sources. Each source gives N bits; we report compressed size / N.
Writes ../data/ours_compress.json."""
import bz2, hashlib, json, lzma, os, zlib
import numpy as np

N = 1 << 20            # bits per source
HERE = os.path.dirname(os.path.abspath(__file__))

def eca_rows(rule, width, steps, seed):
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, width, dtype=np.uint8)
    table = np.array([(rule >> i) & 1 for i in range(8)], np.uint8)
    rows = []
    for _ in range(steps):
        rows.append(x)
        x = table[(np.roll(x, 1) << 2) | (x << 1) | np.roll(x, -1)]
    return np.concatenate(rows)

def prng_bits(seed: bytes, n):
    out, ctr = bytearray(), 0                         # SHA-256 in counter mode: a short seed, deterministic
    while len(out) * 8 < n:
        out += hashlib.sha256(seed + ctr.to_bytes(8, 'big')).digest(); ctr += 1
    return np.unpackbits(np.frombuffer(bytes(out), np.uint8))[:n]

sources = {
    'zeros': np.zeros(N, np.uint8),
    'period': np.tile(np.array([0, 1, 1, 0, 1, 0, 0, 1], np.uint8), N // 8),
    'coin': np.random.default_rng(1).integers(0, 2, N, dtype=np.uint8),
    'prng': prng_bits(b'seed:42', N),
    'rule15': eca_rows(15, 1024, N // 1024, 2),
    'rule30': eca_rows(30, 1024, N // 1024, 2),
    'rule54': eca_rows(54, 1024, N // 1024, 2),
    'rule110': eca_rows(110, 1024, N // 1024, 2),
}
res = {}
for k, bits in sources.items():
    raw = np.packbits(bits).tobytes()
    res[k] = {name: round(len(f(raw)) * 8 / N, 4) for name, f in
              [('gzip', lambda b: zlib.compress(b, 9)), ('bz2', lambda b: bz2.compress(b, 9)),
               ('xz', lambda b: lzma.compress(b, preset=9 | lzma.PRESET_EXTREME))]}
    print(f'{k:8s}', res[k])
json.dump(dict(source='our run (not the paper): compressed bits per input bit, N = 2^20 bits per source; ECA rows of '
               'width 1024 from a random first row; prng = SHA-256 counter mode on a 7-byte seed', N=N, results=res),
          open(os.path.join(HERE, '..', 'data', 'ours_compress.json'), 'w'), indent=1)
