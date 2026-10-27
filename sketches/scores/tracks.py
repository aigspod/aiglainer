"""Prototype score styles 'encore' (solo piano, after a Jarrett encore) and 'analog' (mellow piano house, after
Martin Roth). Original material; written to sit beside 'daylight'. Usage: python tracks.py encore|analog out.wav"""
import sys, wave
import numpy as np
from scipy.signal import fftconvolve
from aiglainer.audio import SR, mtof, env_adsr, lp, hp, bp, stereo, reverb_ir, rng

def place(out, x, t, pan=0.0):
    a = max(0, int(t * SR))     # humanized timing can nudge a first note just before zero
    if a >= len(out):
        return
    s = stereo(x, pan) if x.ndim == 1 else x
    m = min(len(s), len(out) - a)
    out[a:a + m] += s[:m]

def write(mix, path):
    mix = mix / np.abs(mix).max() * 0.89
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print('wrote', path, len(mix) / SR)

def room(out, sec, decay, dry, wet):
    n = len(out)
    ir = reverb_ir(sec, decay)
    w = np.stack([fftconvolve(out[:, i], ir[:, i])[:n] for i in range(2)], 1)
    return out * dry + w * wet

# ---------------------------------------------------------------- instruments
def piano(freq, vel=0.6, hold=2.0, release=0.18, bright=1.0):
    """An acoustic piano note: two slightly detuned strings, stretched partials, a fast-then-slow decay,
    brighter when struck harder, a soft hammer knock, the damper falling after `hold` seconds.
    `bright` above 1 keeps more and longer-ringing upper partials and a harder hammer: a piercing tone."""
    L = int((hold + release + 0.05) * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    base = 0.45 * (freq / 220) ** 0.6
    for h in range(1, int(16 * bright)):
        fh = h * freq * np.sqrt(1 + 0.00025 * h * h)
        if fh > 9000 * bright:
            break
        amp = vel ** ((0.4 + 0.3 * h) / bright) / h ** (1.15 / bright)
        dh = base * (1 + 0.45 * (h - 1) / bright)
        env = 0.6 * np.exp(-t * dh * 4) + 0.4 * np.exp(-t * dh)
        ph = rng.uniform(0, 6)
        x += amp * env * (np.sin(2 * np.pi * fh * 1.0003 * t + ph) + np.sin(2 * np.pi * fh * 0.9997 * t + ph)) / 2
    x *= np.minimum(1, t / 0.002)
    k = int(0.03 * SR)
    x[:k] += lp(rng.normal(0, 1, k), 1200 * bright) * np.exp(-np.arange(k) / SR * 120) * 0.04 * vel * bright
    x *= np.where(t > hold, np.exp(-(t - hold) * 25), 1.0)
    return lp(x, min(18000, (2500 + 5000 * vel) * bright)) * vel

def rhodes(freq, vel=0.6, hold=2.0):
    """An electric piano: a sine bell with a decaying FM bark, a little tine, stereo tremolo."""
    L = int((hold + 0.4) * SR)
    t = np.arange(L) / SR
    idx = vel * 2.2 * np.exp(-t * 5) + 0.25
    x = np.sin(2 * np.pi * freq * t + idx * np.sin(2 * np.pi * freq * t)) * np.exp(-t * 0.9)
    x += 0.12 * np.sin(2 * np.pi * freq * 7.1 * t) * np.exp(-t * 14)
    x *= np.minimum(1, t / 0.003) * np.where(t > hold, np.exp(-(t - hold) * 10), 1.0)
    trem = 0.22 * np.sin(2 * np.pi * 4.2 * t)
    return np.stack([x * (1 + trem), x * (1 - trem)], 1) * vel

def saw_pad(freq, n):
    """Two detuned analog-style saws, warm and filtered."""
    t = np.arange(n) / SR
    x = sum(2 * ((f * t + rng.uniform()) % 1) - 1 for f in (freq * 2 ** (-0.08 / 12), freq * 2 ** (0.08 / 12)))
    return lp(x, 900, 4) * 0.5

def kick(gain=0.5):
    L = int(0.45 * SR); t = np.arange(L) / SR
    f = 46 + 90 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5) * np.minimum(1, t / 0.002)
    return lp(x, 2500) * gain

def hat(gain=0.03, dec=45):
    L = int(0.18 * SR); t = np.arange(L) / SR
    return hp(rng.normal(0, 1, L), 7000) * np.exp(-t * dec) * gain

def shaker(gain=0.012):
    L = int(0.09 * SR); t = np.arange(L) / SR
    return bp(rng.normal(0, 1, L), 4500, 9500) * np.exp(-t * 55) * np.minimum(1, t / 0.01) * gain

def bass(freq, dur, gain=0.22):
    L = int((dur + 0.1) * SR); t = np.arange(L) / SR
    x = (np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(4 * np.pi * freq * t)) * env_adsr(L, 0.008, 0.15, 0.7, 0.08)
    return lp(x, 400) * gain

def grand(freq, vel=0.4, hold=2.0, release=0.3):
    """A soft grand-piano note. Unlike `piano`, the tone dulls quickly after the strike (upper partials die
    much faster than the fundamental), the two strings beat unevenly, and a felt hammer rounds off the top,
    so a held note blooms and fades instead of sustaining like an organ."""
    L = int((hold + release + 0.05) * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    k = freq / 261.6
    t1 = 0.28 / k ** 0.5          # the prompt sound
    t2 = 2.6 / k ** 0.7           # the aftersound
    cut = 900 + 3200 * vel        # a soft felt hammer: struck gently, the top rolls off early
    for h in range(1, 24):
        fh = h * freq * np.sqrt(1 + 0.0003 * h * h)
        if fh > min(cut * 3, 11000):
            break
        amp = np.exp(-fh / cut) / h ** 1.2
        d = 1 + 0.9 * (h - 1)
        env = 0.7 * np.exp(-t * d / t1) + 0.3 * np.exp(-t * d ** 0.8 / t2)
        db = 0.06 + 0.05 * h * rng.uniform(0.6, 1.4)
        ph = rng.uniform(0, 6)
        x += amp * env * (np.sin(2 * np.pi * (fh + db) * t + ph) + 0.85 * np.sin(2 * np.pi * (fh - db) * t + ph * 1.7))
    x *= np.minimum(1, t / 0.0015)
    m = int(0.05 * SR)
    x[:m] += bp(rng.normal(0, 1, m), 60, 1500) * np.exp(-t[:m] * 80) * 0.05 * vel
    x *= np.where(t > hold, np.exp(-(t - hold) * 14), 1.0)
    return x * vel ** 1.3

def soundboard(out):
    """A wooden body: a short, dark, diffuse response that makes separate notes sound like one instrument."""
    n = int(0.08 * SR)
    ir = lp(rng.normal(0, 1, (n, 2)), 2500) * np.exp(-np.arange(n) / SR * 45)[:, None]
    ir /= np.sqrt((ir ** 2).sum(0))
    body = np.stack([fftconvolve(out[:, i], ir[:, i])[:len(out)] for i in range(2)], 1)
    return out + body * 0.35

# ---------------------------------------------------------------- encore: soft solo piano, E minor, a ground bass
def encore():
    """Inward and songful: a four-bar descending ground (E-D-C-B) played three times as variations, the left hand
    gently pulsing in eighth notes, a singing line in the middle of the keyboard, time loosening into a quiet coda."""
    beat = 60 / 60
    Em, EmD, Cma7, B7 = [40, 47, 55, 52], [38, 47, 55, 52], [36, 43, 52, 47], [35, 42, 51, 45]
    Csh = [37, 43, 52, 47]          # C#m7b5: the third time round, one note lifts the ground
    Am7 = [33, 40, 48, 43]
    PULSE = [0, 1, 2, 1, 3, 1, 2, 1]
    bars = [   # (left hand, melody [(beat, note, beats)], dynamic)
        (Em,   [], 0.8),
        (EmD,  [(0, 71, 2), (2, 72, 1), (3, 71, 1)], 0.85),
        (Cma7, [(0, 67, 2), (2, 64, 2)], 0.85),
        (B7,   [(0, 66, 2), (2, 63, 1), (3, 66, 1)], 0.8),
        (Em,   [(0, 67, 1), (1, 71, 1), (2, 76, 2)], 0.95),
        (EmD,  [(0, 74, 1.5), (1.5, 72, 0.5), (2, 71, 2)], 0.95),
        (Cma7, [(0, 72, 1), (1, 71, 1), (2, 69, 1), (3, 67, 1)], 0.9),
        (B7,   [(0, 66, 2), (2, 69, 1), (3, 71, 1)], 0.9),
        (Em,   [(0, 76, 2), (2, 74, 1), (3, 71, 1)], 1.0),
        (EmD,  [(0, 72, 2), (2, 71, 2)], 1.0),
        (Csh,  [(0, 76, 1), (1, 73, 1), (2, 71, 2)], 0.95),
        (B7,   [(0, 75, 1.5), (1.5, 73, 0.5), (2, 71, 2)], 0.9),
        (Cma7, [(0, 76, 2), (2, 71, 2)], 0.75),
        (Am7,  [(0, 72, 2), (2, 69, 2)], 0.7),
        (Em,   [(0, 67, 4)], 0.65),
    ]
    # loosened time: a breath at each phrase end, slowing through the coda
    nb = len(bars) * 4 + 8
    d = np.array([beat * (1 + 0.12 * (b % 16 == 15) + 0.05 * (b % 4 == 3) + 0.45 * np.clip((b - 48) / 12, 0, 1))
                  for b in range(nb)])
    tb = np.concatenate([[0], np.cumsum(d)])
    T = lambda b: float(np.interp(b, np.arange(len(tb)), tb))
    total = T(len(bars) * 4) + 5
    out = np.zeros((int((total + 2) * SR), 2))
    for i, (lh, mel, dyn) in enumerate(bars):
        b0 = i * 4
        last = i == len(bars) - 1
        coda = i >= 12
        end = T(b0 + 4) + (4.5 if last else 0.05)       # the pedal changes on the next downbeat
        if last:                                         # the final chord, rolled softly
            for j, m in enumerate([40, 47, 54, 55, 59]):
                t0 = T(b0) + 0.07 * j
                place(out, grand(mtof(m), 0.3 * dyn, end - t0), t0, (m - 60) / 50)
        else:
            steps = range(0, 8, 2) if coda else range(8)  # the coda pulses in quarter notes
            for s in steps:
                m = lh[PULSE[s]]
                t0 = T(b0 + s / 2) + rng.normal(0, 0.008)
                vel = (0.36 if s == 0 else 0.26 if s == 4 else 0.21) * dyn * rng.uniform(0.92, 1.06)
                place(out, grand(mtof(m), vel, end - t0), t0, (m - 60) / 50)
        for (bt, m, dur) in mel:
            t0 = T(b0 + bt) + 0.015 + rng.normal(0, 0.008)  # the melody just behind the beat
            hold = max(T(b0 + bt + dur) - t0, end - t0)
            vel = (0.46 if bt == 0 else 0.4) * dyn * rng.uniform(0.95, 1.04)
            place(out, grand(mtof(m), vel, hold), t0, (m - 60) / 50)
    out = soundboard(out)
    out = room(out, 2.2, 3.0, 0.88, 0.2)
    out = np.tanh(out / np.abs(out).max() * 0.95) / 0.95
    return out[:int(total * SR)]

# ---------------------------------------------------------------- analog: mellow piano house, A minor, 106 bpm
def analog():
    bpm = 106
    beat = 60 / bpm
    bar = 4 * beat
    nbars = 27
    total = nbars * bar + 3
    n = int((total + 2) * SR)
    keys = np.zeros((n, 2)); drums = np.zeros((n, 2)); low = np.zeros((n, 2))
    # a two-bar chord each: Am9 - Fmaj9 - Dm9 - Em7 (root, then the voicing)
    CH = [(45, [57, 60, 64, 67, 71]), (41, [57, 60, 64, 67]), (38, [57, 60, 62, 65, 69]), (40, [55, 59, 62, 64, 67])]
    # the piano hook, over each chord: (beat, note, beats)
    HOOK = [
        [(0, 76, .75), (.75, 72, .75), (1.5, 71, .5), (2, 72, 1.5), (4, 69, 2.5)],
        [(0, 76, .75), (.75, 72, .75), (1.5, 71, .5), (2, 72, 1), (3, 74, 1), (4, 72, 2.5)],
        [(0, 77, .75), (.75, 74, .75), (1.5, 72, .5), (2, 74, 1.5), (4, 69, 2.5)],
        [(0, 76, .75), (.75, 74, .75), (1.5, 71, .5), (2, 67, 1.5), (4, 71, 2.5)],
    ]
    beats_on = lambda b0, b1: [k for k in range(b0 * 4, b1 * 4)]
    for c in range(0, nbars, 2):
        root, voicing = CH[(c // 2) % 4]
        t0 = c * bar
        # the pad: warm saws under everything
        L = int((2 * bar + 1.5) * SR)
        pad = sum(saw_pad(mtof(m - 12), L) for m in voicing[:3]) * env_adsr(L, 0.6, 0.4, 0.8, 1.2) * 0.05
        place(keys, pad, t0, 0)
        # electric piano: a held chord on the one, soft off-beat stabs from bar 4
        for m in voicing:
            place(keys, rhodes(mtof(m), 0.42, bar * 1.6) * 0.18, t0 + rng.normal(0, 0.004), 0)
        if c >= 4:
            for bt in (2.5, 6.5):
                for m in voicing[1:4]:
                    place(keys, rhodes(mtof(m), 0.3, beat * 0.5) * 0.14, t0 + bt * beat, 0)
        # sub bass from bar 8: the root on the one, a syncopated push, the fifth
        if 8 <= c < nbars - 3:
            for bt, dm, du in [(0, 0, 1.2), (1.5, 0, .4), (3, 7, .8), (4, 0, 1.2), (5.5, 12, .4), (6.5, 7, .5), (7, 0, .8)]:
                place(low, bass(mtof(root - 12 + dm), du * beat), t0 + bt * beat, 0)
        # the piano hook from bar 12 to bar 24
        if 12 <= c < 24:
            for (bt, m, du) in HOOK[(c // 2) % 4]:
                v = (0.58 if bt in (0, 4) else 0.48) * rng.uniform(0.95, 1.05)
                place(keys, piano(mtof(m), v, du * beat + 0.25) * 0.55, t0 + bt * beat + rng.normal(0, 0.005), 0.15)
    # drums: kick from bar 4 until three bars before the end, hats and shaker from bar 8
    for k in beats_on(4, nbars - 3):
        place(drums, kick(0.42), k * beat, 0)
    for k in beats_on(8, nbars - 3):
        place(drums, hat(0.028), (k + 0.5) * beat, 0.25)
        for s in range(4):
            place(drums, shaker(0.012 * (1.0 if s == 2 else 0.6)), (k + s / 4) * beat + rng.normal(0, 0.004), -0.3)
    # the house pump: keys and pad duck gently on each kick
    t = np.arange(n) / SR
    ph = (t / beat) % 1
    on = (t >= 4 * bar) & (t < (nbars - 3) * bar)
    pump = 1 - on * 0.3 * np.exp(-ph * 7)
    keys *= pump[:, None]
    mix = room(keys, 2.0, 3.4, 0.9, 0.22) + drums * 0.9 + low
    # tape: a whisper of hiss, soft saturation
    mix += stereo(lp(hp(rng.normal(0, 1, n), 2500), 9000) * 0.0015)
    mix = np.tanh(mix / np.abs(mix).max() * 1.2) / 1.2
    mix *= (np.clip(t / 1.5, 0, 1) * np.clip((total - t) / 5, 0, 1))[:, None]
    return mix[:int(total * SR)]

if __name__ == '__main__':
    write(dict(encore=encore, analog=analog)[sys.argv[1]](), sys.argv[2])
