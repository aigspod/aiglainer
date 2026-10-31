"""Real string samples for the score sketches: Versilian Studios Chamber Orchestra 2 Community Edition (VSCO 2 CE,
Sam Gossner / Versilian Studios, CC0 1.0: https://github.com/sgossner/VSCO-2-CE; the readme asks for a credit,
which the README here gives). Only the sustained-vibrato folders, ~300 MB, fetched once into ~/.cache/aiglainer/.

  note(inst, midi, dur, vel=0)   one note of any length: the nearest sample, repitched (and resampled to SR),
                                 its sustain looped with crossfades if the note outlasts it; stereo, starts on the bow
  python samples.py              fetch (if needed) and print the pitch index

The filenames' octave numbers don't follow one convention across instruments, so every sample's pitch is measured
(harmonic product spectrum on its sustain) and kept in an index next to the samples.
"""
import os, json, glob, urllib.parse, urllib.request
import numpy as np
import soundfile as sf
from aiglainer.audio import SR

ROOT = os.path.expanduser("~/.cache/aiglainer/vsco2ce")
REPO = "https://raw.githubusercontent.com/sgossner/VSCO-2-CE/master/"
API = "https://api.github.com/repos/sgossner/VSCO-2-CE/git/trees/master?recursive=1"
INST = dict(violins="Strings/Violin Section/susVib", violas="Strings/Viola Section/susvib",
            cellos="Strings/Cello Section/susvib", violin="Strings/Solo Violin/Arco Vib",
            bass="Strings/Solo Contrabass/SusVib")
SOFT = ("_v1", "_p.")                 # the softest layer of each instrument: mellow, the bow barely pressing

def fetch():
    """Download the folders in INST (skipping files already there)."""
    tree = json.load(urllib.request.urlopen(API))["tree"]
    paths = [t["path"] for t in tree if t["type"] == "blob" and t["path"].endswith(".wav")
             and any(t["path"].startswith(d + "/") for d in INST.values())]
    for p in paths:
        dst = os.path.join(ROOT, p)
        if not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            urllib.request.urlretrieve(REPO + urllib.parse.quote(p), dst + ".part")
            os.replace(dst + ".part", dst)
    print(f"{len(paths)} samples in {ROOT}")

def pitch(x, sr):
    """Fundamental of a sustained note, in fractional MIDI: harmonic product spectrum over the steady middle."""
    m = x.mean(1) if x.ndim > 1 else x
    a = int(len(m) * 0.25); seg = m[a:a + min(int(2.0 * sr), len(m) - a)] * np.hanning(min(int(2.0 * sr), len(m) - a))
    n = 1 << 19
    S = np.abs(np.fft.rfft(seg, n)); f = np.fft.rfftfreq(n, 1 / sr)
    lo, hi = np.searchsorted(f, 25), np.searchsorted(f, 2500)
    h = S[:hi * 4].copy()
    hps = np.log(h[:hi] + 1e-9)
    for k in (2, 3, 4):
        hps += np.log(h[::k][:hi] + 1e-9)
    f0 = f[lo + np.argmax(hps[lo:hi])]
    return 69 + 12 * np.log2(f0 / 440)

_index, _cache = None, {}

def index():
    global _index
    if _index is None:
        path = os.path.join(ROOT, "index.json")
        if not os.path.exists(path):
            if not all(os.path.isdir(os.path.join(ROOT, d)) for d in INST.values()):
                fetch()
            idx = {}
            for name, d in INST.items():
                files = [f for f in sorted(glob.glob(os.path.join(ROOT, d, "*.wav"))) if any(s in os.path.basename(f) for s in SOFT)]
                idx[name] = sorted([round(float(pitch(*sf.read(f))), 2), os.path.relpath(f, ROOT)] for f in files)
            json.dump(idx, open(path, "w"), indent=1)
        _index = json.load(open(path))
    return _index

def load(rel):
    """A sample at its own rate, trimmed to the start of the bow (5 ms before it reaches 2% of its peak)."""
    if rel not in _cache:
        x, sr = sf.read(os.path.join(ROOT, rel), always_2d=True)
        a = int(np.argmax(np.abs(x).max(1) > 0.02 * np.abs(x).max()))
        _cache[rel] = (x[max(0, a - int(0.005 * sr)):], sr)
    return _cache[rel]

def note(inst, midi, dur, rank=0):
    """`dur` seconds of `inst` playing `midi` (the caller shapes the envelope). Stereo, at SR, peak about 1.
    `rank` 1 takes the second-nearest sample instead (blend the two to smooth out their vibrato)."""
    p, rel = sorted(index()[inst], key=lambda e: abs(e[0] - midi))[rank]
    x, sr = load(rel)
    step = 2 ** ((midi - p) / 12) * sr / SR                 # source samples per output sample
    n = int(dur * SR)
    need = int(n * step) + 2
    b = len(x) - int(0.4 * sr)                              # leave out the release tail
    if need > b:                                            # loop the sustain (from 1.5 s), crossfading each seam
        a, xf = int(1.5 * sr), int(0.8 * sr)
        g = np.sin(np.linspace(0, np.pi / 2, xf))[:, None]  # equal power
        src = x[:b].copy()
        while len(src) < need:
            nxt = x[a:b]
            src = np.concatenate([src[:-xf], src[-xf:] * g[::-1] + nxt[:xf] * g, nxt[xf:]])
        x = src
    return _read(x, np.arange(n) * step) / (np.abs(x).max() + 1e-9)

def _read(x, pos):
    """Linear interpolation at fractional positions, per channel."""
    i = np.clip(pos.astype(int), 0, len(x) - 2); f = (pos - i)[:, None]
    return x[i] * (1 - f) + x[i + 1] * f

if __name__ == "__main__":
    for name, rows in index().items():
        print(f"{name:8s}", " ".join(f"{p:5.1f}" for p, _ in rows))
