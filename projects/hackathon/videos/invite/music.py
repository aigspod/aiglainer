"""An original, beat-driven track for the hackathon invitation: 120 bpm in C major, four-on-the-floor kick, offbeat
bass, a sidechained supersaw, a plucked arpeggio and a lead hook, with builds, drops, breaks and an outro.

The arrangement is read from narration.py: every scene lists its sections bar by bar (`mus`), so the track has
exactly the timeline's bars and every cut lands on a downbeat. Sections:

  intro   filtered kick and arpeggio over a pad            intro2  hats and bass come in, the filter opens
  build   snare roll, riser, reversed cymbal, a breath     drop    everything, with the lead hook (music-only stretches)
  verse   groove without the lead, under the narrator      break   pads and soft keys, no kick
  hit     one bar of drop with a crash (a title hit)       outro   the tonic chord rings out

All material here is written for this piece (the hook is `HOOK` below); nothing is sampled. The render is cached by a
hash of this file and the arrangement, so editing either makes a new file: project.py asks `ensure()` for the path,
and the engine (MUSIC['style'] = that path) loops nothing, because the track is exactly the timeline's length.
Listen with: make listen F=projects/hackathon/videos/invite/<path> Q="..."
"""
import hashlib, os, sys, wave
import numpy as np
from scipy.signal import butter, sosfilt, sosfilt_zi, fftconvolve

HERE = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':          # run on its own: make the engine importable
    sys.path[:0] = [os.path.normpath(os.path.join(HERE, '..', '..', '..', '..'))]
from aiglainer.audio import SR, mtof, lp, hp, bp
from beat import BPM, BEAT, BAR

S16 = BEAT / 4

# chords as (bass root, voicing); progressions per section kind, one chord a bar
F, G, AM, C = (41, [65, 69, 72, 76]), (43, [67, 71, 74, 79]), (45, [69, 72, 76, 81]), (36, [64, 67, 72, 76])
PROG = dict(drop=[F, G, AM, C], hit=[F], intro=[F, G, AM, C], intro2=[F, G, AM, C], build=[G], verse=[AM, F, C, G],
            break_=[F, G, AM, C], outro=[C])

# the lead hook over F G Am C: (bar, start in 16ths, length in 16ths, midi note)
HOOK = [(0, 0, 2, 81), (0, 2, 2, 79), (0, 4, 3, 81), (0, 7, 3, 84), (0, 10, 2, 81), (0, 12, 4, 79),
        (1, 0, 2, 79), (1, 2, 2, 77), (1, 4, 3, 79), (1, 7, 3, 83), (1, 10, 6, 86),
        (2, 0, 3, 88), (2, 3, 3, 86), (2, 6, 2, 84), (2, 8, 4, 81), (2, 12, 2, 84), (2, 14, 2, 86),
        (3, 0, 6, 88), (3, 6, 2, 86), (3, 8, 4, 84), (3, 12, 4, 79)]
HOOK_END = [(3, 0, 4, 88), (3, 4, 4, 86), (3, 8, 8, 84)]      # the answering phrase resolves home

# how loud each part is in each kind of section (0 = silent)
MIXES = dict(
    intro=dict(kick=.5, shaker=.3, pad=.8, arp=.55, sc=.2, lpf=(380, 1300)),
    intro2=dict(kick=.75, hat=.5, shaker=.4, bass=.6, pad=.75, arp=.7, sc=.3, lpf=(1300, 4200)),
    build=dict(kick=.85, hat=.55, shaker=.4, bass=.55, pad=.8, arp=.75, saw=.35, roll=1, riser=1, rev=1, sc=.35,
               lpf=(2500, 14000), breath=True),
    drop=dict(kick=1, clap=1, hat=.8, ohat=.75, shaker=.45, bass=1, saw=1, arp=.45, lead=1, crash=1, sc=.75),
    hit=dict(kick=1, clap=1, hat=.8, ohat=.75, shaker=.45, bass=1, saw=1, arp=.45, lead=1, crash=1, sc=.75),
    verse=dict(kick=.8, clap=.5, hat=.6, shaker=.4, bass=.75, pad=.55, arp=.8, sc=.45, fill=True),
    break_=dict(pad=1, keys=.8, arp=.4, sub=.5, lpf=(2200, 2200)),
    outro=dict(pad=1, saw=.45, keys=.6, ring=True),
)
GAIN = dict(kick=.95, clap=.32, hat=.11, ohat=.09, shaker=.05, crash=.16, bass=.32, saw=.05, pad=.07, arp=.085,
            lead=.12, keys=.10, sub=.25, roll=.16, riser=.11, rev=.12)


def sections():
    """[(kind, bars)] for the whole piece, from narration.py."""
    import narration
    return [('break_' if k == 'break' else k, n) for sd in narration.SCENES for n, k in sd['mus']]


def ensure():
    """Path (relative to the project) of the rendered track for the current arrangement; renders it if missing."""
    secs = sections()
    key = hashlib.sha1(open(__file__, 'rb').read() + repr((secs, BPM)).encode()).hexdigest()[:12]
    rel = os.path.join('cache', f'music_{key}.wav')
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        print(f'music.py: rendering {rel}', file=sys.stderr, flush=True)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        x = render(secs)
        tmp = path + f'.{os.getpid()}.tmp'
        with wave.open(tmp, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
        os.replace(tmp, path)
    return rel


# ---------------------------------------------------------------- instruments (mono unless noted)
rng = np.random.default_rng(2026)


def env(n, a, d, s, r, hold=None):
    """ADSR over n samples; the note is held for `hold` seconds (default: until the release)."""
    A, D, R = int(a * SR), int(d * SR), int(r * SR)
    H = n - R if hold is None else int(hold * SR)
    e = np.full(n, float(s))
    e[:A] = np.linspace(0, 1, A, False)
    e[A:A + D] = np.linspace(1, s, len(e[A:A + D]), False)
    if H < n:
        e[H:H + R] = np.linspace(e[max(H - 1, 0)], 0, len(e[H:H + R]))
        e[H + R:] = 0
    return e


def saw(f, n, phase=0.0):
    ph = (phase + np.cumsum(np.full(n, f / SR))) % 1.0
    return 2 * ph - 1


def additive(f, n, harmonics, decay=None, amps=None):
    t = np.arange(n) / SR
    x = np.zeros(n)
    for h in range(1, harmonics + 1):
        if f * h > 15000:
            break
        a = (amps(h) if amps else 1 / h) * (np.exp(-t * decay(h)) if decay else 1)
        x += a * np.sin(2 * np.pi * f * h * t)
    return x


def kick():
    n = int(0.45 * SR); t = np.arange(n) / SR
    f = 46 + 120 * np.exp(-t * 32)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6.5)
    x += hp(rng.normal(0, 1, n), 2500) * np.exp(-t * 350) * 0.25
    return x * np.minimum(1, t / 0.0015)


def clap():
    n = int(0.5 * SR); t = np.arange(n) / SR
    noise = bp(rng.normal(0, 1, n), 900, 4200)
    e = sum(np.where(t >= o, np.exp(-(t - o) * 140), 0) for o in (0, 0.011, 0.022)) + np.where(t >= 0.03, np.exp(-(t - 0.03) * 16), 0) * 0.6
    return noise * e


def snare():
    n = int(0.3 * SR); t = np.arange(n) / SR
    return bp(rng.normal(0, 1, n), 1400, 7000) * np.exp(-t * 24) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * 0.6


def hat(open_=False):
    n = int((0.45 if open_ else 0.07) * SR); t = np.arange(n) / SR
    return hp(rng.normal(0, 1, n), 7500) * np.exp(-t * (8 if open_ else 70))


def shaker():
    n = int(0.09 * SR); t = np.arange(n) / SR
    return bp(rng.normal(0, 1, n), 5000, 12000) * np.minimum(1, t / 0.008) * np.exp(-t * 45)


def crash(sec=3.2):
    n = int(sec * SR); t = np.arange(n) / SR
    x = hp(rng.normal(0, 1, n), 3500) * np.exp(-t * 1.4)
    for f in (3215, 4410, 5873, 7120):
        x += 0.08 * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * 2.2)
    return x * np.minimum(1, t / 0.002)


def pluck(f, n, bright=1.0):
    return additive(f, n, 12, decay=lambda h: 7 + 3.2 * h / bright) * np.minimum(1, np.arange(n) / (0.002 * SR))


def keynote(f, n):
    """A soft electric-piano-like note: a few partials, the upper ones dying first."""
    x = additive(f, n, 6, decay=lambda h: 1.6 + 1.2 * h, amps=lambda h: [1, .45, .2, .12, .06, .04][h - 1])
    return x * np.minimum(1, np.arange(n) / (0.003 * SR))


def lead_note(f, n):
    t = np.arange(n) / SR
    vib = 1 + (2 ** (0.14 / 12) - 1) * np.sin(2 * np.pi * 5.6 * t) * np.clip((t - 0.12) / 0.15, 0, 1)
    ph = np.cumsum(f * vib) / SR
    x = np.zeros(n)
    for det in (-0.06, 0.06):
        p = ph * 2 ** (det / 12)
        for h in range(1, 15):
            if f * h > 14000:
                break
            x += np.sin(2 * np.pi * h * p) / h
    return x


def place(buf, x, t, pan=0.0, gain=1.0):
    i = int(round(t * SR))
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    m = min(len(x), len(buf) - i)
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    if x.ndim == 1:
        buf[i:i + m, 0] += x[:m] * l * gain
        buf[i:i + m, 1] += x[:m] * r * gain
    else:
        buf[i:i + m] += x[:m] * gain


# ---------------------------------------------------------------- arrangement
def render(secs):
    bars = []                     # (kind, index within section, section length)
    for kind, n in secs:
        bars += [(kind, i, n) for i in range(n)]
    total = len(bars) * BAR
    N = int((total + 3.0) * SR)
    parts = {k: np.zeros((N, 2)) for k in GAIN}
    sc = np.ones(N)               # sidechain gain (the pump), applied to bass, saw, pad and arp
    cut = np.full(N // 480 + 1, 18000.0)         # bus low-pass cutoff per 10 ms block
    breath = np.ones(N)
    K, CL, SN, HC, HO, SH, CR = kick(), clap(), snare(), hat(), hat(True), shaker(), crash()
    hook_bar = 0
    for b, (kind, i, n) in enumerate(bars):
        M = MIXES[kind]
        t0 = b * BAR
        root, chord = PROG[kind][i % len(PROG[kind])]
        nxt = bars[b + 1][0] if b + 1 < len(bars) else None
        last = i == n - 1
        if 'lpf' in M:            # filter sweep across the section, exponential in frequency
            c0, c1 = M['lpf']
            k0, k1 = int(t0 * 100), int((t0 + BAR) * 100)
            u = (i + np.linspace(0, 1, k1 - k0, False)) / n
            cut[k0:k1] = c0 * (c1 / c0) ** u
        # drums
        for q in range(4):
            tb = t0 + q * BEAT
            if M.get('kick'):
                place(parts['kick'], K, tb, 0, M['kick'])
                if M.get('sc'):
                    j = int(tb * SR); L = int(BEAT * SR); tt = np.arange(L) / SR
                    sc[j:j + L] = np.minimum(sc[j:j + L], 1 - M['sc'] * np.exp(-tt / 0.11) * np.minimum(1, tt / 0.004 + 0.6))
            if M.get('clap') and q in (1, 3):
                place(parts['clap'], CL, tb, 0.05, M['clap'])
            if M.get('hat'):
                place(parts['hat'], HC, tb + BEAT / 2, 0.25, M['hat'])
            if M.get('ohat') and q in (0, 1, 2, 3):
                place(parts['ohat'], HO, tb + BEAT / 2, -0.2, M['ohat'] * (0.6 if q % 2 == 0 else 1))
            if M.get('shaker'):
                for s in range(4):
                    place(parts['shaker'], SH, tb + s * S16, 0.4 * (-1) ** s, M['shaker'] * (1 if s == 2 else 0.55))
        if M.get('crash') and i == 0:
            place(parts['crash'], CR, t0, 0, M['crash'])
        if M.get('fill') and last and nxt is not None:
            for s in range(4):    # a sixteenth snare fill into the next scene
                place(parts['roll'], SN, t0 + 3 * BEAT + s * S16, 0, 0.35 + 0.15 * s)
        if M.get('roll'):         # snare roll across the build: eighths, then sixteenths, then thirty-seconds
            u0 = i / n
            steps = [(s, S16 * 2) for s in np.arange(0, BAR, S16 * 2)] if u0 < 0.5 and n > 1 else []
            if not steps:
                steps = [(s, S16) for s in np.arange(0, BAR * 0.5, S16)] + [(s, S16 / 2) for s in np.arange(BAR * 0.5, BAR - BEAT / 2, S16 / 2)]
            for s, _ in steps:
                u = (i + s / BAR) / n
                place(parts['roll'], SN, t0 + s, 0, 0.15 + 0.85 * u ** 1.6)
        if M.get('riser') and i == 0:
            L = int(n * BAR * SR); tt = np.arange(L) / SR; d = n * BAR
            noise = rng.normal(0, 1, L)
            lo, hi = hp(noise, 400), hp(noise, 5000)
            u = tt / d
            x = (lo * (1 - u) + hi * u) * u ** 2.0
            x += np.sin(2 * np.pi * np.cumsum(220 * 2 ** (2.5 * u)) / SR) * u ** 2.5 * 0.25
            place(parts['riser'], x, t0, 0, M['riser'])
        if M.get('rev') and last:  # reversed cymbal swelling into the next downbeat
            r = crash(1.6)[::-1]
            place(parts['rev'], r, t0 + BAR - len(r) / SR - BEAT / 2, 0, M['rev'])
        if M.get('breath') and last:   # half a beat of silence before the drop
            j = int((t0 + BAR - BEAT / 2) * SR); L = int(BEAT / 2 * SR)
            breath[j:j + L] = np.minimum(breath[j:j + L], np.r_[np.linspace(1, 0, 240), np.zeros(L - 240)])
        # bass
        if M.get('bass'):
            for q in range(4):
                for off, on in ((0, kind in ('verse', 'intro2', 'build')), (BEAT / 2, True)):
                    if not on:
                        continue
                    L = int(0.22 * SR)
                    f = mtof(root)
                    x = lp(saw(f, L) * 0.6 + np.sin(2 * np.pi * f * np.arange(L) / SR), 900) * env(L, 0.003, 0.08, 0.7, 0.05)
                    place(parts['bass'], x, t0 + q * BEAT + off, 0, M['bass'])
        if M.get('sub'):
            L = int((BAR + 0.3) * SR)
            x = np.sin(2 * np.pi * mtof(root) * np.arange(L) / SR) * env(L, 0.25, 0.1, 1, 0.3)
            place(parts['sub'], x, t0, 0, M['sub'])
        # chords
        ring = M.get('ring')
        if M.get('saw'):
            L = int((BAR * (n if ring else 1) + (2.5 if ring else 0.03)) * SR)
            if not ring or i == 0:
                e = env(L, 0.01, 0.2, 0.85, 2.4 if ring else 0.03)
                for m in chord:
                    for k, det in enumerate((-0.22, -0.1, 0, 0.1, 0.22)):
                        x = saw(mtof(m) * 2 ** (det / 12), L, rng.uniform()) * e
                        place(parts['saw'], x, t0, (-0.7, -0.35, 0, 0.35, 0.7)[k], M['saw'])
        if M.get('pad'):
            L = int((BAR * (n if ring else 1) + (3.0 if ring else 0.6)) * SR)
            if not ring or i == 0:
                e = env(L, 0.35 if not ring else 0.8, 0.3, 0.9, 3.0 if ring else 0.6)
                tt = np.arange(L) / SR
                for j, m in enumerate(chord + [root + 12]):
                    for det in (-0.08, 0.08):
                        f = mtof(m) * 2 ** (det / 12)
                        x = (np.sin(2 * np.pi * f * tt + rng.uniform(0, 6)) + 0.18 * np.sin(4 * np.pi * f * tt)) * e
                        place(parts['pad'], x, t0, (-0.6 + 1.2 * j / 4) * (1 if det > 0 else -1), M['pad'])
        if M.get('keys'):
            hits = [(0, 1.0), (1.5 * BEAT, 0.7), (2.5 * BEAT, 0.8)] if not ring else ([(0, 1.0)] if i == 0 else [])
            for off, g in hits:
                L = int(2.4 * SR)
                for m in chord:
                    place(parts['keys'], keynote(mtof(m - 12), L), t0 + off, rng.uniform(-0.3, 0.3), M['keys'] * g)
        if M.get('arp') and not (ring and i > 0):
            tones = chord + [chord[1] + 12, chord[2] + 12]
            pat = [0, 1, 2, 3, 4, 3, 2, 1]
            for s in range(16):
                m = tones[pat[(s + b) % 8]] - 12
                place(parts['arp'], pluck(mtof(m), int(0.35 * SR), 1.0), t0 + s * S16, 0.45 * (-1) ** s,
                      M['arp'] * (1.0 if s % 4 == 0 else 0.7))
        # lead: the hook over drops, answered on its second pass; a hit plays its first bar
        if M.get('lead'):
            pb = i % 4
            phrase = HOOK_END if (i // 4) % 2 == 1 and pb == 3 else HOOK
            for (bb, s, ln, m) in phrase:
                if bb != pb:
                    continue
                L = int((ln * S16 + 0.08) * SR)
                x = lead_note(mtof(m), L) * env(L, 0.006, 0.12, 0.75, 0.07)
                place(parts['lead'], x, t0 + s * S16, 0, M['lead'])
    # pump, mix, delay and room
    for k in ('bass', 'saw', 'pad', 'arp'):
        parts[k] *= sc[:, None]
    parts['saw'] = hp(lp(parts['saw'], 5200), 180)
    parts['lead'] = lp(parts['lead'], 7000)
    d = int(3 * S16 * SR)         # dotted-eighth ping-pong delay on the lead
    dl = np.zeros_like(parts['lead'])
    src = parts['lead'].copy()
    for k in range(1, 5):
        g = 0.38 ** k
        sh = src[:-d * k] if d * k < N else src[:0]
        left = k % 2 == 1
        dl[d * k:, 0] += sh[:, 0] * g * (1.0 if left else 0.4)
        dl[d * k:, 1] += sh[:, 1] * g * (0.4 if left else 1.0)
    parts['lead'] += lp(dl, 4000)
    dry = sum(parts[k] * GAIN[k] for k in parts)
    send = sum(parts[k] * GAIN[k] * w for k, w in (('pad', .5), ('arp', .45), ('lead', .4), ('clap', .25), ('keys', .5), ('saw', .2), ('roll', .2)))
    n_ir = int(2.8 * SR); tt = np.arange(n_ir) / SR
    ir = lp(rng.normal(0, 1, (n_ir, 2)) * np.exp(-2.6 * tt)[:, None], 7000)
    ir /= np.sqrt((ir ** 2).sum(0))
    wet = np.stack([fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], 1)
    mix = dry + hp(wet, 150) * 0.55
    mix *= breath[:, None]
    mix = sweep(mix, cut)
    mix = hp(mix, 28)
    mix = np.tanh(mix / np.abs(mix).max() * 1.6) / 1.6
    mix *= section_gain(bars, N)[:, None]         # after the limiter, so drops stand out from verses and breaks
    mix = mix / np.abs(mix).max() * 0.89
    return mix[:int((total + 2.5) * SR)]


# overall level of each kind of section, (at its start, at its end): drops loudest, breaks and intros well below
LEVELS = dict(intro=(.5, .62), intro2=(.66, .78), build=(.78, 1.0), drop=(1, 1), hit=(1, 1), verse=(.7, .7),
              break_=(.56, .56), outro=(.8, .8))


def section_gain(bars, N):
    """Gain per sample from LEVELS. A rise (into a drop or a hit) is instant, on the downbeat after the build's breath;
    a fall eases over the half second before the cut, so the music never steps down under a scene's first line."""
    g = np.empty(N)
    for k, (kind, i, n) in enumerate(bars):
        a, z = LEVELS[kind]
        j0, j1 = int(k * BAR * SR), int((k + 1) * BAR * SR)
        g[j0:j1] = a + (z - a) * (i + np.linspace(0, 1, j1 - j0, False)) / n
    g[int(len(bars) * BAR * SR):] = LEVELS[bars[-1][0]][1]
    for k in range(1, len(bars)):
        j = int(k * BAR * SR)
        before, after = g[j - 1], g[j]
        if after < before:
            L = int(0.5 * SR)
            g[j - L:j] = before + (after - before) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, L)))
    return g


def sweep(x, cut):
    """A low-pass whose cutoff follows `cut` (one value per 10 ms block), filter state carried across blocks."""
    out = np.empty_like(x)
    zi = None
    blk = SR // 100
    for k in range(0, len(x), blk):
        fc = min(float(cut[min(k // blk, len(cut) - 1)]), 20000.0)
        sos = butter(2, fc / (SR / 2), 'low', output='sos')
        if zi is None:
            zi = np.stack([sosfilt_zi(sos) * x[0, c] for c in range(2)], -1)
        y, zi = sosfilt(sos, x[k:k + blk], axis=0, zi=zi)
        out[k:k + blk] = y
    return out


if __name__ == '__main__':
    print(os.path.join(HERE, ensure()))
