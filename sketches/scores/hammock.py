"""Score sketches after Hammock's trilogy (Mysterium 2017, Universalis 2018, Silencia 2019). Original material.
  silencia   serene: swelling processed-guitar pads with an octave shimmer, a cello line, a few soft piano notes
  mysterium  solemn: a wordless choir and strings over guitar haze, swelling once, ending in a major chord (hope)
Usage: python hammock.py silencia|mysterium out.wav"""
import sys
import numpy as np
from scipy.signal import fftconvolve
from aiglainer.audio import SR, mtof, env_adsr, lp, hp, bp, stereo, reverb_ir, rng
from daylight import bowed
from tracks import grand, place, write

def guitar_swell(freq, n, att=1.4, rel=3.0):
    """An electric guitar note with the pick hidden by a volume swell (an e-bow / volume-pedal sound):
    a plucked-string spectrum, three chorused voices, a slow tape drift."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    drift = 1 + 0.0012 * np.sin(2 * np.pi * 0.23 * t + rng.uniform(0, 6))
    for det in (-0.06, 0.0, 0.06):
        f = freq * 2 ** (det / 12)
        ph0 = 2 * np.pi * np.cumsum(f * drift) / SR
        for h in range(1, 30):
            if h * f > 5000:
                break
            a = abs(np.sin(np.pi * h * 0.21)) / h ** 1.3
            x += a * np.sin(h * ph0 + rng.uniform(0, 6))
    x *= env_adsr(n, att, 0.8, 0.8, rel)
    return lp(x / 3, 3200)

FORMANTS = dict(ah=[(700, 1.0, 110), (1220, 0.5, 120), (2600, 0.22, 160)],
                oo=[(320, 1.0, 80), (800, 0.45, 100), (2240, 0.08, 140)])

def choir(freq, n, vowel=0.5, voices=4, att=2.0, rel=3.5):
    """Wordless voices on one note: a section of singers with their own pitch and vibrato, shaped by vowel formants.
    `vowel` blends 'oo' (0, hushed) to 'ah' (1, open)."""
    t = np.arange(n) / SR
    x = np.zeros(n)
    for v in range(voices):
        f = freq * 2 ** (rng.uniform(-0.09, 0.09) / 12)
        vib = 1 + 0.004 * np.clip((t - 0.6) / 1.2, 0, 1) * np.sin(2 * np.pi * rng.uniform(4.8, 5.6) * t + rng.uniform(0, 6))
        ph0 = 2 * np.pi * np.cumsum(f * vib) / SR
        for h in range(1, 40):
            fh = h * f
            if fh > 4000:
                break
            g = 0.0
            for name, w in (('oo', 1 - vowel), ('ah', vowel)):
                g += w * sum(a / (1 + ((fh - F) / bw) ** 2) for F, a, bw in FORMANTS[name])
            x += g / h ** 0.5 * np.sin(h * ph0 + rng.uniform(0, 6))
    breath = bp(rng.normal(0, 1, n), 900, 3000) * 0.004
    return (x / voices + breath) * env_adsr(n, att, 0.5, 0.9, rel)

def hall(dry, send, sec=6.5, decay=1.1):
    """Hammock's space: a long, dark hall, fed by a send so some parts sit deeper in it than others."""
    n = len(dry)
    ir = lp(reverb_ir(sec, decay), 4500)
    wet = np.stack([fftconvolve(send[:, i], ir[:, i])[:n] for i in range(2)], 1)
    return dry + hp(wet, 140)      # a hall without the boom: the low end stays dry and clear

def master(mix, total):
    mix = hp(mix[:int(total * SR)], 40)
    t = np.arange(len(mix)) / SR
    mix *= (np.clip(t / 2.5, 0, 1) * np.clip((total - t) / 6, 0, 1))[:, None]
    return np.tanh(mix / np.abs(mix).max() * 1.1) / 1.1

# ---------------------------------------------------------------- silencia: serene, D major, chords of 7.5 s
def silencia():
    CH = 7.5
    chords = [            # Dadd9 - A/C# - Bm7(add11) - Gmaj9, twice
        [38, 50, 57, 64, 66], [37, 49, 57, 64, 69], [35, 47, 54, 57, 64], [31, 43, 50, 54, 57],
    ] * 2
    total = CH * len(chords) + 4
    n = int((total + 8) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    CELLO = {2: [(0, 54, 7.5)], 3: [(0, 55, 4), (4, 54, 3.5)], 4: [(0, 57, 4), (4, 54, 3.5)],
             5: [(0, 52, 7.5)], 6: [(0, 50, 4), (4, 52, 3.5)], 7: [(0, 50, 9)]}
    PIANO = {4: [(0.5, 69), (2.5, 66), (4.5, 64)], 5: [(0.5, 69), (3, 64)], 6: [(0.5, 66), (2.5, 62), (4.5, 61)],
             7: [(0.5, 62), (3.5, 57)]}
    for k, ch in enumerate(chords):
        t0 = k * CH
        L = int((CH + 4) * SR)
        # a soft pad under everything: the guitar's lowest notes, hidden in the hall
        for m in ch[:2]:
            x = guitar_swell(mtof(m), L, att=2.5, rel=4.0) * 0.10
            place(dry, x * 0.4, t0, 0); place(send, x, t0, 0)
        # swelling guitars, each note of the chord blooming a little after the last, with an octave shimmer
        for j, m in enumerate(ch[2:]):
            ts = t0 + 0.6 * j + rng.uniform(0, 0.3)
            x = guitar_swell(mtof(m), L, att=1.6) * 0.09
            pan = (-0.6, 0.0, 0.6)[j]
            place(dry, x * 0.5, ts, pan); place(send, x, ts, pan)
            place(send, guitar_swell(mtof(m + 12), L, att=3.0) * 0.025, ts + 0.8, -pan)
        # the cello comes forward from the third chord
        for (bt, m, du) in CELLO.get(k, []):
            Lc = int((du + 2.5) * SR)
            x = bowed(mtof(m), Lc, 3, bright=0.55, cutoff=2400) * env_adsr(Lc, 1.0, 0.4, 0.9, 2.2) * 0.13
            place(dry, x * 0.8, t0 + bt, -0.15); place(send, x * 0.5, t0 + bt, -0.15)
        # a few soft piano notes, far back in the room
        for (bt, m) in PIANO.get(k, []):
            x = grand(mtof(m), 0.32, 2.5)
            place(dry, x * 0.35, t0 + bt, 0.3); place(send, x * 0.7, t0 + bt, 0.3)
    return master(hall(dry, send), total)

# ---------------------------------------------------------------- mysterium: solemn, B minor to D major, 8 s chords
def mysterium():
    CH = 8.0
    chords = [            # Bm - Gmaj7 - D/F# - Em9 - Bm - Gmaj7 - Asus2 - D
        [35, 47, 54, 59, 62], [31, 43, 54, 59, 62], [42, 50, 57, 62, 66], [40, 52, 55, 59, 66],
        [35, 47, 54, 59, 62], [31, 43, 54, 59, 62], [33, 45, 52, 59, 64], [38, 50, 57, 62, 66],
    ]
    total = CH * len(chords) - 4
    n = int((total + 10) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    # the swell: hushed 'oo' at first, opening to 'ah' at the fifth and sixth chords, settling on the last
    shape = [0.35, 0.45, 0.6, 0.75, 1.0, 1.0, 0.8, 0.7]
    vowel = [0.0, 0.1, 0.3, 0.5, 0.85, 0.9, 0.6, 0.4]
    for k, ch in enumerate(chords):
        t0 = k * CH
        last = k == len(chords) - 1
        L = int((CH + (8 if last else 3.5)) * SR)
        g = shape[k]
        # low strings throughout
        for j, m in enumerate(ch[:2]):
            x = bowed(mtof(m), L, 3, cutoff=1800) * env_adsr(L, 1.6, 0.5, 0.9, 5 if last else 3) * 0.11 * (0.8 + 0.4 * g)
            place(dry, x * 0.7, t0, (-0.4, 0.4)[j]); place(send, x * 0.5, t0, (-0.4, 0.4)[j])
        # the choir on the upper three notes, from the second chord
        if k >= 1:
            for j, m in enumerate(ch[2:]):
                x = choir(mtof(m), L, vowel[k], att=2.2, rel=5 if last else 3.5) * 0.07 * g
                pan = (-0.5, 0.0, 0.5)[j]
                place(dry, x * 0.45, t0 + 0.2 * j, pan); place(send, x, t0 + 0.2 * j, pan)
        # guitar haze above, mostly reverb
        for j, m in enumerate(ch[3:]):
            x = guitar_swell(mtof(m + 12), L, att=3.0) * 0.03 * g
            place(send, x, t0 + 1.0, (0.6, -0.6)[j])
        # violins join the swell (chords 4-7) with a slow line
        if 3 <= k:
            m = {3: 71, 4: 74, 5: 74, 6: 76, 7: 78}[k]     # B, D, D, E, F#: rising into the last chord
            x = bowed(mtof(m), L, 4, bright=0.6, cutoff=4200) * env_adsr(L, 1.8, 0.5, 0.9, 5 if last else 3) * 0.045 * g
            place(dry, x * 0.6, t0, 0.2); place(send, x * 0.7, t0, 0.2)
    return master(hall(dry, send, 6.0, 1.2), total)

if __name__ == '__main__':
    write(dict(silencia=silencia, mysterium=mysterium)[sys.argv[1]](), sys.argv[2])
