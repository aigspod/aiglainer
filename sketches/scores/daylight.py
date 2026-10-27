"""Prototype 'daylight' score style, v3: sad but warm. A descending lament bass under strings,
a soft piano figure moving through the chords, and a singable line that rises and comes home."""
import sys, wave
import numpy as np
from scipy.signal import fftconvolve
from aiglainer.audio import SR, mtof, env_adsr, lp, hp, stereo, reverb_ir, rng

CH = 6.6   # seconds per chord
# E minor, the bass walking down by step (a lament bass), the dominant major so it pulls home, ending on Em.
# (bass, then voices low to high; no semitone clusters)
CHORDS = [
    [40, 52, 55, 59, 64],   # Em
    [38, 50, 54, 57, 62],   # D
    [36, 48, 55, 59, 64],   # Cmaj7
    [35, 47, 54, 59, 63],   # B
    [45, 52, 55, 60, 64],   # Am7
    [43, 52, 55, 59, 64],   # Em/G
    [36, 48, 55, 59, 64],   # Cmaj7
    [35, 47, 54, 59, 63],   # B
    [40, 52, 55, 59, 64],   # Em, held to the end
]
TOTAL = CH * len(CHORDS)
# The top line from the fifth chord: two notes per chord, rising to the high E, settling on G over the last Em
MELODY = {4: [72, 71], 5: [67, 71], 6: [76, 74], 7: [75, 71], 8: [67]}
FIGURE = [0, 2, 3, 2, 1, 2, 3, 2]   # the piano's broken-chord pattern over chord[1:]

def bowed(freq, n, voices=3, bright=0.6, cutoff=2600):
    """A small string section on one note: gently detuned saw-like voices, delayed vibrato, a little bow noise."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    vib_in = np.clip((t - 0.8) / 1.5, 0, 1)
    for v in range(voices):
        det = (v - (voices - 1) / 2) * 0.035
        f0 = freq * 2 ** (det / 12)
        vib = 1 + 0.0028 * vib_in * np.sin(2 * np.pi * (5.2 + 0.3 * v) * t + rng.uniform(0, 6))
        ph = 2 * np.pi * np.cumsum(f0 * vib) / SR + rng.uniform(0, 6)
        for h in range(1, 12):
            out += bright ** (h - 1) / h * np.sin(h * ph)
    out /= voices * 2
    noise = hp(lp(rng.normal(0, 1, n), freq * 3), freq) * 0.012
    return hp(lp(out + noise, cutoff), 45)

def piano(freq, dur=2.4):
    """A soft felt-piano note: slightly stretched partials, the upper ones dying faster."""
    L = int(dur * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    for h, a in enumerate([1.0, 0.45, 0.22, 0.1, 0.05], 1):
        f = freq * h * (1 + 0.0004 * h * h)
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * (1.6 + 1.3 * h))
    return lp(x * np.minimum(1, t / 0.006), 3000)

def layer_gain(t, start, ramp=8.0):
    return float(np.clip((t - start) / ramp, 0, 1))

def render():
    n = int((TOTAL + 6) * SR)
    out = np.zeros((n, 2))
    for k, chord in enumerate(CHORDS):
        last = k == len(CHORDS) - 1
        seg = int((CH + (6.0 if last else 3.0)) * SR)
        t0 = k * CH
        i0 = int(t0 * SR)
        e = env_adsr(seg, 0.9, 0.5, 0.85, 5.0 if last else 2.2)
        parts = [  # (notes, layer entry time, level, voices, cutoff)
            (chord[:2], 0.0, 0.12, 3, 2200),     # basses and cellos from the start
            (chord[2:4], CH, 0.10, 3, 3400),     # violas join on the second chord
            (chord[4:], 3 * CH, 0.07, 3, 5200),  # violins join on the fourth
        ]
        for p, (notes, start, lvl, voices, cut) in enumerate(parts):
            g = layer_gain(t0 + 1.5, start)
            if g <= 0:
                continue
            for j, m in enumerate(notes):
                x = bowed(mtof(m), seg, voices, cutoff=cut) * e * lvl * g
                pan = [(-0.45, 0.4), (-0.6, 0.6), (0.5, 0.5)][p][min(j, 1)]
                out[i0:i0 + seg] += stereo(x, pan)[:n - i0]
        # the piano figure, from the second chord, eighth notes at 72 bpm
        if k >= 1:
            step = 60 / 72 / 2
            for s in range(int(CH / step) if not last else 4):
                m = chord[1:][FIGURE[s % len(FIGURE)]] + 12
                x = piano(mtof(m)) * 0.05 * layer_gain(t0, CH, 2 * CH) * (1.0 if s % 4 == 0 else 0.75)
                a = int((t0 + s * step) * SR)
                out[a:a + len(x)] += stereo(x, 0.25 * np.sin(s * 1.1))[:n - a]
        for h, m in enumerate(MELODY.get(k, [])):      # the singing line on top
            L = int(((CH + 4) if last else (CH / 2 + 2.0)) * SR)
            a = int((t0 + h * CH / 2) * SR)
            x = bowed(mtof(m), L, 2, bright=0.62, cutoff=5600) * env_adsr(L, 0.5, 0.4, 0.9, 2.5 if last else 1.6) * 0.07
            out[a:a + L] += stereo(x, 0.1)[:n - a]
    T = np.arange(n) / SR
    out *= (np.clip(T / 3, 0, 1) * np.clip((TOTAL + 4 - T) / 6, 0, 1))[:, None]
    ir = reverb_ir(sec=2.4, decay=3.2)
    wet = np.stack([fftconvolve(out[:, i], ir[:, i])[:n] for i in range(2)], 1)
    mix = out * 0.85 + wet * 0.28
    mix = np.tanh(mix * 1.1) / 1.1
    mix = mix[:int((TOTAL + 4) * SR)]
    mix = mix / np.abs(mix).max() * 0.89
    with wave.open(sys.argv[1], 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print('wrote', sys.argv[1], TOTAL)

if __name__ == '__main__':
    render()
