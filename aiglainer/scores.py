"""Score styles after music the pod loves, chosen like the others by a project's MUSIC['style'] (see audio.STYLES):

  daylight   strings over a descending lament bass, a soft piano figure, a singing line (after Max Richter)
  encore     soft solo piano: variations over a descending ground, time loosening at the end (after Keith Jarrett)
  analog     mellow piano house at 106 bpm (after Martin Roth)
  silencia   swelling processed-guitar pads, a cello line, a few soft piano notes (after Hammock's Silencia)
  mysterium  low strings and a wordless choir that swell, guitar haze above (after Hammock's Mysterium)

All original material, prototyped in sketches/scores/ (its README has what each is after and why). Each renders a
bed of any length in its own room, at the loudness of the 'night' score after its reverb, so swapping styles keeps
the voice/music balance. Each seeds its own generator, so a style always renders the same bed for the same inputs.
`arp_on(t)` (0..1) marks the busy middle of a video; each style uses it for its moving part.
"""
import numpy as np
from scipy.signal import fftconvolve
from .audio import SR, mtof, env_adsr, lp, hp, bp, stereo

LEVEL = 0.085     # RMS of the 'night' score after build()'s reverb (night 0.089, dawn 0.079)
rng = np.random.default_rng(0)      # reseeded by render() for every bed

def render(name, total, arp_on):
    global rng
    rng = np.random.default_rng(SEEDS[name])
    n = int(total * SR)
    x = hp(STYLES[name](total, arp_on), 40)
    x = np.pad(x, ((0, max(0, n - len(x))), (0, 0)))[:n]
    r = np.sqrt((x ** 2).mean())
    return x * (LEVEL / r) if r > 0 else x

# ---------------------------------------------------------------- mixing helpers
def place(out, x, t, pan=0.0):
    a = max(0, int(t * SR))     # humanized timing can nudge a first note just before zero
    if a >= len(out):
        return
    s = stereo(x, pan) if x.ndim == 1 else x
    m = min(len(s), len(out) - a)
    out[a:a + m] += s[:m]

def ir(sec, decay):
    n = int(sec * SR)
    t = np.arange(n) / SR
    h = lp(rng.normal(0, 1, (n, 2)) * np.exp(-decay * t)[:, None], 6000)
    h[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    return h / np.sqrt((h ** 2).sum(0))

def conv(x, h):
    return np.stack([fftconvolve(x[:, i], h[:, i])[:len(x)] for i in range(2)], 1)

def room(out, sec, decay, dry, wet):
    return out * dry + conv(out, ir(sec, decay)) * wet

def hall(dry, send, sec=6.5, decay=1.1):
    """Hammock's space: a long, dark hall fed by a send, without the boom (the low end stays dry and clear)."""
    return dry + hp(conv(send, lp(ir(sec, decay), 4500)), 140)

def soft(x, drive=1.1):
    return np.tanh(x / np.abs(x).max() * drive) / drive

def layer(t, start, ramp=8.0):
    return float(np.clip((t - start) / ramp, 0, 1))

# ---------------------------------------------------------------- instruments
def bowed(freq, n, voices=3, bright=0.6, cutoff=2600):
    """A small string section on one note: gently detuned saw-like voices, delayed vibrato, a little bow noise."""
    t = np.arange(n) / SR
    out = np.zeros(n)
    vib_in = np.clip((t - 0.8) / 1.5, 0, 1)
    for v in range(voices):
        f0 = freq * 2 ** ((v - (voices - 1) / 2) * 0.035 / 12)
        vib = 1 + 0.0028 * vib_in * np.sin(2 * np.pi * (5.2 + 0.3 * v) * t + rng.uniform(0, 6))
        ph = 2 * np.pi * np.cumsum(f0 * vib) / SR + rng.uniform(0, 6)
        for h in range(1, 12):
            out += bright ** (h - 1) / h * np.sin(h * ph)
    out /= voices * 2
    noise = hp(lp(rng.normal(0, 1, n), freq * 3), freq) * 0.012
    return hp(lp(out + noise, cutoff), 45)

def grand(freq, vel=0.4, hold=2.0, release=0.3):
    """A soft grand-piano note: the tone dulls quickly after the strike (upper partials die much faster than the
    fundamental), the two strings beat unevenly, a felt hammer rounds off the top. Blooms and fades, never an organ."""
    L = int((hold + release + 0.05) * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    k = freq / 261.6
    t1, t2 = 0.28 / k ** 0.5, 2.6 / k ** 0.7       # the prompt sound, the aftersound
    cut = 900 + 3200 * vel
    for h in range(1, 24):
        fh = h * freq * np.sqrt(1 + 0.0003 * h * h)
        if fh > min(cut * 3, 11000):
            break
        d = 1 + 0.9 * (h - 1)
        env = 0.7 * np.exp(-t * d / t1) + 0.3 * np.exp(-t * d ** 0.8 / t2)
        db = 0.06 + 0.05 * h * rng.uniform(0.6, 1.4)
        ph = rng.uniform(0, 6)
        x += np.exp(-fh / cut) / h ** 1.2 * env * (np.sin(2 * np.pi * (fh + db) * t + ph) + 0.85 * np.sin(2 * np.pi * (fh - db) * t + ph * 1.7))
    x *= np.minimum(1, t / 0.0015)
    m = int(0.05 * SR)
    x[:m] += bp(rng.normal(0, 1, m), 60, 1500) * np.exp(-t[:m] * 80) * 0.05 * vel
    x *= np.where(t > hold, np.exp(-(t - hold) * 14), 1.0)
    return x * vel ** 1.3

def soundboard(out):
    """A wooden body: a short, dark, diffuse response that makes separate notes sound like one instrument."""
    n = int(0.08 * SR)
    h = lp(rng.normal(0, 1, (n, 2)), 2500) * np.exp(-np.arange(n) / SR * 45)[:, None]
    return out + conv(out, h / np.sqrt((h ** 2).sum(0))) * 0.35

def house_piano(freq, vel=0.6, hold=2.0, release=0.18):
    """The brighter piano of the house track: two detuned strings, stretched partials, brighter when struck harder."""
    L = int((hold + release + 0.05) * SR)
    t = np.arange(L) / SR
    x = np.zeros(L)
    base = 0.45 * (freq / 220) ** 0.6
    for h in range(1, 16):
        fh = h * freq * np.sqrt(1 + 0.00025 * h * h)
        if fh > 9000:
            break
        dh = base * (1 + 0.45 * (h - 1))
        env = 0.6 * np.exp(-t * dh * 4) + 0.4 * np.exp(-t * dh)
        ph = rng.uniform(0, 6)
        x += vel ** (0.4 + 0.3 * h) / h ** 1.15 * env * (np.sin(2 * np.pi * fh * 1.0003 * t + ph) + np.sin(2 * np.pi * fh * 0.9997 * t + ph)) / 2
    x *= np.minimum(1, t / 0.002)
    k = int(0.03 * SR)
    x[:k] += lp(rng.normal(0, 1, k), 1200) * np.exp(-np.arange(k) / SR * 120) * 0.04 * vel
    x *= np.where(t > hold, np.exp(-(t - hold) * 25), 1.0)
    return lp(x, 2500 + 5000 * vel) * vel

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
    t = np.arange(n) / SR
    x = sum(2 * ((f * t + rng.uniform()) % 1) - 1 for f in (freq * 2 ** (-0.08 / 12), freq * 2 ** (0.08 / 12)))
    return lp(x, 900, 4) * 0.5

def kick(gain=0.5):
    L = int(0.45 * SR); t = np.arange(L) / SR
    f = 46 + 90 * np.exp(-t * 32)
    return lp(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5) * np.minimum(1, t / 0.002), 2500) * gain

def hat(gain=0.03):
    L = int(0.18 * SR); t = np.arange(L) / SR
    return hp(rng.normal(0, 1, L), 7000) * np.exp(-t * 45) * gain

def shaker(gain=0.012):
    L = int(0.09 * SR); t = np.arange(L) / SR
    return bp(rng.normal(0, 1, L), 4500, 9500) * np.exp(-t * 55) * np.minimum(1, t / 0.01) * gain

def bass(freq, dur, gain=0.22):
    L = int((dur + 0.1) * SR); t = np.arange(L) / SR
    return lp((np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(4 * np.pi * freq * t)) * env_adsr(L, 0.008, 0.15, 0.7, 0.08), 400) * gain

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
            x += abs(np.sin(np.pi * h * 0.21)) / h ** 1.3 * np.sin(h * ph0 + rng.uniform(0, 6))
    return lp(x / 3 * env_adsr(n, att, 0.8, 0.8, rel), 3200)

FORMANTS = dict(ah=[(700, 1.0, 110), (1220, 0.5, 120), (2600, 0.22, 160)],
                oo=[(320, 1.0, 80), (800, 0.45, 100), (2240, 0.08, 140)])

def choir(freq, n, vowel=0.5, voices=4, att=2.0, rel=3.5):
    """Wordless voices on one note, each singer with their own pitch and vibrato, shaped by vowel formants.
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
            g = sum(w * sum(a / (1 + ((fh - F) / bw) ** 2) for F, a, bw in FORMANTS[name])
                    for name, w in (('oo', 1 - vowel), ('ah', vowel)))
            x += g / h ** 0.5 * np.sin(h * ph0 + rng.uniform(0, 6))
    return (x / voices + bp(rng.normal(0, 1, n), 900, 3000) * 0.004) * env_adsr(n, att, 0.5, 0.9, rel)

# ---------------------------------------------------------------- daylight
def daylight(total, arp_on):
    """E minor, the bass walking down by step, 6.6 s a chord; violas then violins join; the piano figure plays
    while arp_on; a singing line on the second half of every pass after the first."""
    CH = 6.6
    chords = [[40, 52, 55, 59, 64], [38, 50, 54, 57, 62], [36, 48, 55, 59, 64], [35, 47, 54, 59, 63],   # Em D Cmaj7 B
              [45, 52, 55, 60, 64], [43, 52, 55, 59, 64], [36, 48, 55, 59, 64], [35, 47, 54, 59, 63]]   # Am7 Em/G Cmaj7 B
    melody = {4: [72, 71], 5: [67, 71], 6: [76, 74], 7: [75, 71]}
    figure = [0, 2, 3, 2, 1, 2, 3, 2]
    n = int((total + 6) * SR)
    out = np.zeros((n, 2))
    for k in range(int(total / CH) + 1):
        chord, t0 = chords[k % 8], k * CH
        i0 = int(t0 * SR)
        seg = int((CH + 3.0) * SR)
        e = env_adsr(seg, 0.9, 0.5, 0.85, 2.2)
        for p, (notes, start, lvl, cut) in enumerate([(chord[:2], 0.0, 0.12, 2200), (chord[2:4], CH, 0.10, 3400),
                                                      (chord[4:], 3 * CH, 0.07, 5200)]):
            g = layer(t0 + 1.5, start)
            if g <= 0:
                continue
            for j, m in enumerate(notes):
                x = bowed(mtof(m), seg, 3, cutoff=cut) * e * lvl * g
                out[i0:i0 + seg] += stereo(x, [(-0.45, 0.4), (-0.6, 0.6), (0.5, 0.5)][p][min(j, 1)])[:n - i0]
        g = layer(t0, CH, 2 * CH) * arp_on(t0)
        if k >= 1 and g > 0.01:
            step = 60 / 72 / 2
            for s in range(int(CH / step)):
                m = chord[1:][figure[s % 8]] + 12
                tt = t0 + s * step
                L = int(2.4 * SR); tl = np.arange(L) / SR
                x = np.zeros(L)
                for h, a in enumerate([1.0, 0.45, 0.22, 0.1, 0.05], 1):
                    x += a * np.sin(2 * np.pi * mtof(m) * h * (1 + 0.0004 * h * h) * tl) * np.exp(-tl * (1.6 + 1.3 * h))
                x = lp(x * np.minimum(1, tl / 0.006), 3000) * 0.05 * g * (1.0 if s % 4 == 0 else 0.75)
                place(out, x, tt, 0.25 * np.sin(s * 1.1))
        if k >= 4:
            for h, m in enumerate(melody.get(k % 8, [])):
                L = int((CH / 2 + 2.0) * SR)
                x = bowed(mtof(m), L, 2, bright=0.62, cutoff=5600) * env_adsr(L, 0.5, 0.4, 0.9, 1.6) * 0.07
                place(out, x, t0 + h * CH / 2, 0.1)
    return soft(room(out, 2.4, 3.2, 0.85, 0.28))[:int(total * SR)]

# ---------------------------------------------------------------- encore
def encore(total, arp_on):
    """Soft solo piano in E minor at 60 bpm: a four-bar descending ground (E-D-C-B) as variations, the left hand
    pulsing in quarters (eighths while arp_on), a mid-register melody just behind the beat; the last three bars a
    coda that slows into a rolled Em."""
    beat = 1.0
    Em, EmD, Cma7, B7 = [40, 47, 55, 52], [38, 47, 55, 52], [36, 43, 52, 47], [35, 42, 51, 45]
    Csh, Am7 = [37, 43, 52, 47], [33, 40, 48, 43]      # C#m7b5: one note lifts the ground the third time round
    pulse = [0, 1, 2, 1, 3, 1, 2, 1]
    body = [
        (Em, []), (EmD, [(0, 71, 2), (2, 72, 1), (3, 71, 1)]), (Cma7, [(0, 67, 2), (2, 64, 2)]), (B7, [(0, 66, 2), (2, 63, 1), (3, 66, 1)]),
        (Em, [(0, 67, 1), (1, 71, 1), (2, 76, 2)]), (EmD, [(0, 74, 1.5), (1.5, 72, 0.5), (2, 71, 2)]),
        (Cma7, [(0, 72, 1), (1, 71, 1), (2, 69, 1), (3, 67, 1)]), (B7, [(0, 66, 2), (2, 69, 1), (3, 71, 1)]),
        (Em, [(0, 76, 2), (2, 74, 1), (3, 71, 1)]), (EmD, [(0, 72, 2), (2, 71, 2)]),
        (Csh, [(0, 76, 1), (1, 73, 1), (2, 71, 2)]), (B7, [(0, 75, 1.5), (1.5, 73, 0.5), (2, 71, 2)]),
    ]
    coda = [(Cma7, [(0, 76, 2), (2, 71, 2)]), (Am7, [(0, 72, 2), (2, 69, 2)]), (Em, [(0, 67, 4)])]
    dyn_body = [0.8, 0.85, 0.85, 0.8, 0.95, 0.95, 0.9, 0.9, 1.0, 1.0, 0.95, 0.9]

    def times(N):           # loosened time: a breath at each phrase end, the coda slowing
        d = [beat * (1 + 0.12 * (b % 16 == 15) + 0.05 * (b % 4 == 3) + 0.45 * np.clip((b - (N - 3) * 4) / 12, 0, 1))
             for b in range(N * 4 + 8)]
        return np.concatenate([[0], np.cumsum(d)])
    N = 3
    while times(N + 1)[(N + 1) * 4] < total - 3:
        N += 1
    tb = times(N)
    T = lambda b: float(np.interp(b, np.arange(len(tb)), tb))
    seq = list(range(12)) + [4 + (i % 8) for i in range(max(0, N - 15))]      # then passes two and three, again
    bars = [body[j] + (dyn_body[j],) for j in seq[:max(0, N - 3)]] + [c + (d,) for c, d in zip(coda, (0.75, 0.7, 0.65))][-min(3, N):]
    out = np.zeros((int((total + 8) * SR), 2))
    for i, (lh, mel, dyn) in enumerate(bars):
        b0 = i * 4
        last = i == len(bars) - 1
        in_coda = i >= len(bars) - 3
        end = T(b0 + 4) + (4.5 if last else 0.05)          # the pedal changes on the next downbeat
        if last:
            for j, m in enumerate([40, 47, 54, 55, 59]):
                t0 = T(b0) + 0.07 * j
                place(out, grand(mtof(m), 0.3 * dyn, end - t0), t0, (m - 60) / 50)
        else:
            steps = range(0, 8, 2) if in_coda or arp_on(T(b0)) < 0.5 else range(8)
            for s in steps:
                m = lh[pulse[s]]
                t0 = T(b0 + s / 2) + rng.normal(0, 0.008)
                vel = (0.36 if s == 0 else 0.26 if s == 4 else 0.21) * dyn * rng.uniform(0.92, 1.06)
                place(out, grand(mtof(m), vel, end - t0), t0, (m - 60) / 50)
        for (bt, m, dur) in mel:
            t0 = T(b0 + bt) + 0.015 + rng.normal(0, 0.008)
            hold = max(T(b0 + bt + dur) - t0, end - t0)
            vel = (0.46 if bt == 0 else 0.4) * dyn * rng.uniform(0.95, 1.04)
            place(out, grand(mtof(m), vel, hold), t0, (m - 60) / 50)
    out = room(soundboard(out), 2.2, 3.0, 0.88, 0.2)
    return soft(out, 0.95)[:int(total * SR)]

# ---------------------------------------------------------------- analog
def analog(total, arp_on):
    """Mellow piano house, A minor, 106 bpm, Am9 - Fmaj9 - Dm9 - Em7 two bars each: pads and electric piano, then a
    soft kick with a gentle pump, then bass, hats and shaker; the acoustic piano hook while arp_on; the beat drops
    away for the last bars."""
    beat = 60 / 106
    bar = 4 * beat
    nb = int(total / bar) + 1
    intro = min(4, max(1, nb // 6)); full = min(8, 2 * intro); outro = min(3, max(1, nb // 8))
    n = int((total + 3) * SR)
    keys = np.zeros((n, 2)); drums = np.zeros((n, 2)); low = np.zeros((n, 2))
    chords = [(45, [57, 60, 64, 67, 71]), (41, [57, 60, 64, 67]), (38, [57, 60, 62, 65, 69]), (40, [55, 59, 62, 64, 67])]
    hook = [
        [(0, 76, .75), (.75, 72, .75), (1.5, 71, .5), (2, 72, 1.5), (4, 69, 2.5)],
        [(0, 76, .75), (.75, 72, .75), (1.5, 71, .5), (2, 72, 1), (3, 74, 1), (4, 72, 2.5)],
        [(0, 77, .75), (.75, 74, .75), (1.5, 72, .5), (2, 74, 1.5), (4, 69, 2.5)],
        [(0, 76, .75), (.75, 74, .75), (1.5, 71, .5), (2, 67, 1.5), (4, 71, 2.5)],
    ]
    for c in range(0, nb, 2):
        root, voicing = chords[(c // 2) % 4]
        t0 = c * bar
        L = int((2 * bar + 1.5) * SR)
        place(keys, sum(saw_pad(mtof(m - 12), L) for m in voicing[:3]) * env_adsr(L, 0.6, 0.4, 0.8, 1.2) * 0.05, t0, 0)
        for m in voicing:
            place(keys, rhodes(mtof(m), 0.42, bar * 1.6) * 0.18, t0 + rng.normal(0, 0.004), 0)
        if c >= intro:
            for bt in (2.5, 6.5):
                for m in voicing[1:4]:
                    place(keys, rhodes(mtof(m), 0.3, beat * 0.5) * 0.14, t0 + bt * beat, 0)
        if full <= c < nb - outro:
            for bt, dm, du in [(0, 0, 1.2), (1.5, 0, .4), (3, 7, .8), (4, 0, 1.2), (5.5, 12, .4), (6.5, 7, .5), (7, 0, .8)]:
                place(low, bass(mtof(root - 12 + dm), du * beat), t0 + bt * beat, 0)
        g = arp_on(t0)
        if c >= full and g > 0.01:
            for (bt, m, du) in hook[(c // 2) % 4]:
                v = (0.58 if bt in (0, 4) else 0.48) * rng.uniform(0.95, 1.05)
                place(keys, house_piano(mtof(m), v, du * beat + 0.25) * 0.55 * g, t0 + bt * beat + rng.normal(0, 0.005), 0.15)
    for k in range(intro * 4, (nb - outro) * 4):
        place(drums, kick(0.42), k * beat, 0)
    for k in range(full * 4, (nb - outro) * 4):
        place(drums, hat(0.028), (k + 0.5) * beat, 0.25)
        for s in range(4):
            place(drums, shaker(0.012 * (1.0 if s == 2 else 0.6)), (k + s / 4) * beat + rng.normal(0, 0.004), -0.3)
    t = np.arange(n) / SR
    on = (t >= intro * bar) & (t < (nb - outro) * bar)
    keys *= (1 - on * 0.3 * np.exp(-((t / beat) % 1) * 7))[:, None]       # the house pump: keys duck on each kick
    mix = room(keys, 2.0, 3.4, 0.9, 0.22) + drums * 0.9 + low
    mix += stereo(lp(hp(rng.normal(0, 1, n), 2500), 9000) * 0.0015)       # a whisper of tape hiss
    return soft(mix, 1.2)[:int(total * SR)]

# ---------------------------------------------------------------- silencia
def silencia(total, arp_on):
    """Serene, D major, Dadd9 - A/C# - Bm7(add11) - Gmaj9 at 7.5 s each: swelling guitars blooming note by note
    with an octave shimmer, a cello line from the third chord, a few soft piano notes far back while arp_on."""
    CH = 7.5
    chords = [[38, 50, 57, 64, 66], [37, 49, 57, 64, 69], [35, 47, 54, 57, 64], [31, 43, 50, 54, 57]]
    cello = {0: [(0, 50, 7.5)], 1: [(0, 49, 4), (4, 52, 3.5)], 2: [(0, 54, 7.5)], 3: [(0, 55, 4), (4, 54, 3.5)],
             4: [(0, 57, 4), (4, 54, 3.5)], 5: [(0, 52, 7.5)], 6: [(0, 50, 4), (4, 52, 3.5)], 7: [(0, 50, 7.5)]}
    piano = {4: [(0.5, 69), (2.5, 66), (4.5, 64)], 5: [(0.5, 69), (3, 64)], 6: [(0.5, 66), (2.5, 62), (4.5, 61)],
             7: [(0.5, 62), (3.5, 57)]}
    n = int((total + 8) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    for k in range(int(total / CH) + 1):
        ch, t0 = chords[k % 4], k * CH
        L = int((CH + 4) * SR)
        for m in ch[:2]:            # a soft pad under everything: the guitar's lowest notes, hidden in the hall
            x = guitar_swell(mtof(m), L, att=2.5, rel=4.0) * 0.10
            place(dry, x * 0.4, t0); place(send, x, t0)
        for j, m in enumerate(ch[2:]):
            ts = t0 + 0.6 * j + rng.uniform(0, 0.3)
            x = guitar_swell(mtof(m), L, att=1.6) * 0.09
            pan = (-0.6, 0.0, 0.6)[j]
            place(dry, x * 0.5, ts, pan); place(send, x, ts, pan)
            place(send, guitar_swell(mtof(m + 12), L, att=3.0) * 0.025, ts + 0.8, -pan)
        if k >= 2:
            for (bt, m, du) in cello[k % 8]:
                Lc = int((du + 2.5) * SR)
                x = bowed(mtof(m), Lc, 3, bright=0.55, cutoff=2400) * env_adsr(Lc, 1.0, 0.4, 0.9, 2.2) * 0.13
                place(dry, x * 0.8, t0 + bt, -0.15); place(send, x * 0.5, t0 + bt, -0.15)
        g = arp_on(t0)
        if k >= 4 and g > 0.01:
            for (bt, m) in piano.get(k % 8, []):
                x = grand(mtof(m), 0.32, 2.5) * g
                place(dry, x * 0.35, t0 + bt, 0.3); place(send, x * 0.7, t0 + bt, 0.3)
    return soft(hall(dry, send))[:int(total * SR)]

# ---------------------------------------------------------------- mysterium
def mysterium(total, arp_on):
    """Solemn, B minor to D major, 8 s chords: low strings; from the second chord a wordless choir opening from a
    hushed 'oo' to an 'ah' at the swell; guitar haze above; violins rising into the last chords while arp_on."""
    CH = 8.0
    chords = [[35, 47, 54, 59, 62], [31, 43, 54, 59, 62], [42, 50, 57, 62, 66], [40, 52, 55, 59, 66],   # Bm Gmaj7 D/F# Em9
              [35, 47, 54, 59, 62], [31, 43, 54, 59, 62], [33, 45, 52, 59, 64], [38, 50, 57, 62, 66]]   # Bm Gmaj7 Asus2 D
    shape = [0.35, 0.45, 0.6, 0.75, 1.0, 1.0, 0.8, 0.7]
    vowel = [0.0, 0.1, 0.3, 0.5, 0.85, 0.9, 0.6, 0.4]
    violin = {3: 71, 4: 74, 5: 74, 6: 76, 7: 78}
    K = int(total / CH) + 1
    n = int((total + 10) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    for k in range(K):
        j8, t0 = k % 8, k * CH
        ch, g = chords[j8], shape[j8]
        last = k == K - 1
        L = int((CH + (8 if last else 3.5)) * SR)
        rel = 5 if last else 3
        for j, m in enumerate(ch[:2]):
            x = bowed(mtof(m), L, 3, cutoff=1800) * env_adsr(L, 1.6, 0.5, 0.9, rel) * 0.11 * (0.8 + 0.4 * g)
            place(dry, x * 0.7, t0, (-0.4, 0.4)[j]); place(send, x * 0.5, t0, (-0.4, 0.4)[j])
        if k >= 1:
            for j, m in enumerate(ch[2:]):
                x = choir(mtof(m), L, vowel[j8], att=2.2, rel=rel + 0.5) * 0.07 * g
                pan = (-0.5, 0.0, 0.5)[j]
                place(dry, x * 0.45, t0 + 0.2 * j, pan); place(send, x, t0 + 0.2 * j, pan)
        for j, m in enumerate(ch[3:]):
            place(send, guitar_swell(mtof(m + 12), L, att=3.0) * 0.03 * g, t0 + 1.0, (0.6, -0.6)[j])
        a = arp_on(t0)
        if j8 in violin and a > 0.01:
            x = bowed(mtof(violin[j8]), L, 4, bright=0.6, cutoff=4200) * env_adsr(L, 1.8, 0.5, 0.9, rel) * 0.045 * g * a
            place(dry, x * 0.6, t0, 0.2); place(send, x * 0.7, t0, 0.2)
    return soft(hall(dry, send, 6.0, 1.2))[:int(total * SR)]

STYLES = dict(daylight=daylight, encore=encore, analog=analog, silencia=silencia, mysterium=mysterium)
SEEDS = dict(daylight=101, encore=102, analog=103, silencia=104, mysterium=105)
