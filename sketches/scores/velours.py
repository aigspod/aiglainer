"""Score sketch 'velours', after ROUGGE's piano-and-voice lullabies (*L'heure du soir - Berceuses pour piano et voix*,
2025): "inside music", intimate and nocturnal, the voice a texture rather than words. Original material: the key,
chords, figures and lines are ours, written to the character Music Flamingo heard in the EP (minor-mode loops that
rock like a lullaby with no dominant pulling home; soft, heavily pedalled piano in free time, a low foundation under
slow upper arpeggios; a wordless voice that murmurs and sometimes keens high and strained, close, with reverb and
delay; long swells and real silences). The recordings are never used or kept here.

C# minor, free time, ~4.5 s a chord, a breath every four:
  A  C#m - F#m(add9) - Amaj7 - G#m7, twice (the second time the murmur enters)
  B  E - B/D# - C#m(add9) - A(add9), then E - B/D# - A(add9), and a rolled C#m (the keen rises over B)

Usage: python velours.py velours|velours2|berceuse|cascade|nuit out.wav"""
import sys
import numpy as np
from aiglainer.audio import SR, mtof, env_adsr, lp, hp, bp, stereo, rng
from tracks import grand, place, write, room

# ---------------------------------------------------------------- the voice, as texture
HUM = [(260, 1.0, 70), (1050, 0.10, 140), (2500, 0.05, 200)]        # a closed-mouth 'mm', nasal and dark
OO = [(330, 1.0, 80), (820, 0.40, 110), (2300, 0.06, 160)]
EE = [(300, 0.7, 80), (2350, 0.65, 170), (3100, 0.45, 220)]         # a thin, bright 'ee' for the keen

def _gain(fh, formants):
    return sum(a / (1 + ((fh - F) / bw) ** 2) for F, a, bw in formants)

def _wobble(n, rate, depth):
    """A slow random drift (lowpassed noise), +-depth, for pitch or loudness that never sits still."""
    w = lp(rng.normal(0, 1, n + SR), rate)[SR:]
    return 1 + depth * w / (np.abs(w).max() + 1e-9)

def voice(path, amps, formants, tilt=1.6, breath=0.25, jitter=0.0012, rough=0.0, cut=3000):
    """One wordless voice. `path` is the pitch in Hz per sample (glides included), `amps` the loudness per sample.
    A soft glottal source (harmonics falling as 1/h^tilt) and breath noise, both shaped by the vowel's formants."""
    n = len(path)
    t = np.arange(n) / SR
    f = path * _wobble(n, 6, jitter)
    vib = 1 + 0.0035 * np.clip(amps / (amps.max() + 1e-9) - 0.5, 0, 1) * np.sin(2 * np.pi * 4.6 * t + rng.uniform(0, 6))
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    f0 = float(np.median(path))
    x = np.zeros(n)
    for h in range(1, 60):
        if h * f0 > cut * 1.6:
            break
        x += _gain(h * f0, formants) / h ** tilt * np.sin(h * ph + rng.uniform(0, 6))
    noise = rng.normal(0, 1, n)
    air = sum(a * bp(noise, max(80, F - bw), F + bw) for F, a, bw in formants) * breath
    x = (x + air) * amps * _wobble(n, 0.7, 0.18)
    if rough:                                   # the strain: a little grit when the keen pushes
        loud = amps / (amps.max() + 1e-9)
        x *= 1 + rough * loud ** 2 * np.sin(2 * np.pi * 31 * t) * _wobble(n, 3, 0.5)
    return lp(hp(x, 70), cut)

def line(notes, total, glide=0.18, scoop=0.0):
    """Pitch and loudness paths for a phrase: notes are (start, dur, midi, level). The pitch glides between notes
    (portamento `glide` s) and, with `scoop`, slides up into each one from that many semitones below."""
    n = int(total * SR)
    midi = np.full(n, float(notes[0][2]))
    amp = np.zeros(n)
    for (t0, d, m, lv) in notes:
        a, b = int(t0 * SR), min(n, int((t0 + d) * SR))
        seg = np.full(b - a, float(m))
        if scoop:
            k = np.arange(b - a) / SR
            seg -= scoop * np.exp(-k / 0.22)
        midi[a:b] = seg
        amp[a:b] = np.maximum(amp[a:b], lv * env_adsr(b - a, min(0.9, d * 0.35), 0.3, 0.85, min(1.4, d * 0.4)))
    midi = smooth(midi, int(glide * SR))         # portamento: smooth the pitch steps
    return 440 * 2 ** ((midi - 69) / 12), amp

def smooth(x, k):
    """Centred moving average over k samples (a running sum: a direct convolution here took minutes)."""
    if k < 2:
        return x
    p = np.pad(x, (k, k), mode='edge')
    c = np.concatenate([[0.0], np.cumsum(p)])
    y = (c[k:] - c[:-k]) / k
    o = k // 2
    return y[k - o:k - o + len(x)]

def echo(x, d=0.39, fb=0.38, taps=4):
    """A soft tape-ish delay: each repeat darker and quieter."""
    y = x.copy()
    k = int(d * SR)
    rep = x
    for i in range(1, taps + 1):
        rep = lp(np.pad(rep, (k, 0))[:len(x)], 3200 - 500 * i) * fb
        y += rep
    return y

# ---------------------------------------------------------------- the piano
CH = {   # (bass and fifth, upper voicing)
    'C#m': ([37, 44], [56, 61, 64, 68]), 'F#m9': ([42, 49], [57, 61, 66, 68]), 'Amaj7': ([45, 52], [56, 61, 64, 69]),
    'G#m7': ([44, 51], [59, 63, 66, 68]), 'E': ([40, 47], [56, 59, 64, 68]), 'B/D#': ([39, 47], [54, 59, 63, 66]),
    'C#m9': ([37, 44], [56, 63, 64, 68]), 'Aadd9': ([45, 52], [57, 59, 64, 69]),
}
SEQ = ['C#m', 'F#m9', 'Amaj7', 'G#m7'] * 2 + ['E', 'B/D#', 'C#m9', 'Aadd9', 'E', 'B/D#', 'Aadd9', 'C#m']
ARP = [0, 1, 2, 3, 2, 1]

def velours(total=None):
    # free time: each chord 4.2-4.8 s, a breath after every fourth, the last two broadening
    durs = [4.5 + rng.uniform(-0.3, 0.3) + (1.4 if i % 4 == 3 else 0) + (1.2 if i >= len(SEQ) - 2 else 0)
            for i in range(len(SEQ))]
    starts = np.concatenate([[0.6], 0.6 + np.cumsum(durs)])
    end = starts[-1] + 6
    N = int(end * SR)
    pno = np.zeros((N, 2))
    for i, name in enumerate(SEQ):
        bass, up = CH[name]
        t0, d = starts[i], durs[i]
        last = i == len(SEQ) - 1
        breath = 1.4 if i % 4 == 3 else 0
        hold = d - breath * 0.6 + (4 if last else 0.15)          # the pedal lifts a little before a breath
        dyn = 0.8 + 0.2 * np.sin(np.pi * (i % 8) / 7)            # each eight-chord pass swells and eases
        for j, m in enumerate(bass):
            tb = t0 + 0.05 * j
            place(pno, grand(mtof(m), 0.30 * dyn, hold - 0.05 * j), tb, -0.25)
        if last:                                                 # a slow roll, then let it ring
            for j, m in enumerate(up + [up[0] + 12]):
                tt = t0 + 0.35 + 0.16 * j
                place(pno, grand(mtof(m), 0.20, hold - 0.35 - 0.16 * j), tt, (m - 60) / 45)
            continue
        play = d - breath - 0.4
        steps = ARP[:max(3, int(play / 0.68))]
        gaps = np.linspace(0.62, 0.78, len(steps)) * rng.uniform(0.95, 1.05, len(steps))   # easing into each chord
        tt = t0 + 0.55
        for k, s in enumerate(steps):
            m = up[s]
            vel = (0.19 + 0.05 * (k == 0)) * dyn * rng.uniform(0.9, 1.08)
            place(pno, grand(mtof(m), vel, max(0.6, t0 + hold - tt)), tt + rng.normal(0, 0.01), (m - 60) / 45)
            tt += gaps[k]
        if i >= 8 and i % 2 == 0:                                # in B, a single high note answers the voice
            m = up[-1] + 12
            place(pno, grand(mtof(m), 0.14 * dyn, max(0.6, t0 + hold - tt)), t0 + d * 0.62, 0.3)
    pno = room(pno, 2.4, 2.6, 0.85, 0.22)

    # the murmur: from the second pass, low and lazy, one held note across each pair of chords
    S = starts
    mur = [(S[4] + 0.8, 7.5, 56, 0.9), (S[6] + 0.4, 4.6, 57, 0.8), (S[7] + 0.3, 4.5, 56, 0.85),
           (S[8] + 0.6, 4.8, 56, 0.9), (S[9] + 0.2, 4.6, 54, 0.8), (S[10] + 0.3, 4.4, 56, 0.85), (S[11], 5.4, 57, 0.75),
           (S[12] + 0.5, 4.2, 59, 0.85), (S[13] + 0.2, 4.6, 58 + 0, 0.8), (S[14] + 0.3, 6.0, 57, 0.8), (S[15] + 0.4, 6.5, 56, 0.7)]
    p, a = line(mur, end, glide=0.35)
    v1 = voice(p, a, HUM, tilt=1.8, breath=0.35, cut=2200) * 0.55 + voice(p, a, OO, tilt=1.6, breath=0.2, cut=2600) * 0.35
    # the keen: over B, high and thin, sliding up into each note, pushing a little at the top
    kee = [(S[8] + 1.4, 3.2, 76, 0.8), (S[9] + 1.0, 2.6, 75, 0.7), (S[10] + 0.8, 3.6, 73, 0.75),
           (S[12] + 1.2, 2.8, 80, 0.85), (S[13] + 0.6, 3.0, 78, 0.75), (S[14] + 0.9, 4.2, 76, 0.7)]
    p2, a2 = line(kee, end, glide=0.12, scoop=1.6)
    v2 = voice(p2, a2, EE, tilt=1.1, breath=0.45, jitter=0.0025, rough=0.22, cut=6000) * 0.32
    vox = echo(v1 + v2)
    vox = room(stereo(vox, 0.05) + stereo(echo(v2, 0.53, 0.3), 0.35) * 0.4, 5.0, 1.3, 0.75, 0.45)

    mix = pno + vox * 0.55
    return mix[:int((total or end) * SR)]

# ---------------------------------------------------------------- variations
# Each after one trait Music Flamingo heard in the EP, with the voice made more voice-like than in v1: the mouth opens
# from 'mm' towards 'ah' as a note swells, small breaths before phrases, the keen rawer and further forward.
AH = [(700, 1.0, 110), (1150, 0.45, 130), (2600, 0.18, 170)]

def voice_open(p, a, openness, **kw):
    """The murmur with a mouth: closed 'mm' when quiet, opening towards 'ah' as it swells."""
    o = openness * (a / (a.max() + 1e-9)) ** 1.5
    return voice(p, a * (1 - o), HUM, **kw) + voice(p, a * o, AH, **kw) * 0.8

def inhale(at, n, level=0.05):
    """A small breath before a phrase: 0.35 s of airy noise, rising, cut off where the voice starts."""
    x = np.zeros(n)
    L = int(0.35 * SR)
    a = int(at * SR)
    if a < 0 or a + L > n:
        return x
    e = np.linspace(0, 1, L) ** 2
    x[a:a + L] = bp(rng.normal(0, 1, L), 500, 3500) * e * level
    return x

def nearest(pcs, lo, hi, prev):
    """The chord tone (pitch classes pcs) in lo..hi closest to prev: lazy voice leading."""
    cands = [m for m in range(lo, hi + 1) if m % 12 in pcs]
    return min(cands, key=lambda m: (abs(m - prev), m))

def piece(sp):
    C, seq = sp['chords'], sp['seq']
    durs = [sp['dur'] * rng.uniform(1 - sp.get('jit', 0.07), 1 + sp.get('jit', 0.07)) for _ in seq]
    rest = [sp.get('breaths', {}).get(i, 0.0) for i in range(len(seq))]
    for k in range(1, sp.get('broaden', 2) + 1):
        durs[-k] *= 1.3
    starts = np.concatenate([[0.6], 0.6 + np.cumsum(np.add(durs, rest))])
    end = starts[-1] + sp.get('tail', 6)
    N = int(end * SR)
    pno = np.zeros((N, 2))
    g0, g1 = sp.get('gaps', (0.62, 0.78))
    for i, name in enumerate(seq):
        bass, up = C[name]
        t0, d = starts[i], durs[i]
        last = i == len(seq) - 1
        hold = d + (4 if last else 0.15) + (rest[i] * 0.3)
        dyn = sp.get('pv', 1.0) * (0.8 + 0.2 * np.sin(np.pi * (i % 8) / 7))
        for j, m in enumerate(bass):
            place(pno, grand(mtof(m), 0.30 * dyn, hold - 0.05 * j), t0 + 0.05 * j, -0.25)
        if last:
            for j, m in enumerate(up + [up[0] + 12]):
                place(pno, grand(mtof(m), 0.19 * dyn, hold - 0.4 - 0.17 * j), t0 + 0.4 + 0.17 * j, (m - 60) / 45)
            continue
        pat = sp.get('arp', [0, 1, 2, 3, 2, 1])
        nst = max(sp.get('min_steps', 3), int((d - 0.5) / ((g0 + g1) / 2)))
        if not sp.get('flow', False):
            nst = min(nst, len(pat))
        gaps = np.linspace(g0, g1, nst) * rng.uniform(0.95, 1.05, nst)
        tt = t0 + sp.get('arp_in', 0.55)
        for k in range(nst):
            m = up[pat[k % len(pat)]]
            vel = (0.19 + 0.05 * (k % len(pat) == 0)) * dyn * rng.uniform(0.9, 1.08)
            place(pno, grand(mtof(m), vel, max(0.6, t0 + hold - tt)), tt + rng.normal(0, 0.01), (m - 60) / 45)
            tt += gaps[k]
        if i in sp.get('answer', ()):
            m = up[-1] + 12
            place(pno, grand(mtof(m), 0.14 * dyn, max(0.6, t0 + hold - t0 - d * 0.62)), t0 + d * 0.62, 0.3)
    pno = room(pno, *sp.get('proom', (2.4, 2.6, 0.85, 0.22)))

    vox = np.zeros(N)
    mu = sp.get('mur')
    if mu:      # the murmur: lazy voice leading through chord tones, one note across `hold` chords
        lo, hi = mu['reg']
        prev, notes, last_end = (lo + hi) // 2, [], -9.0
        for i in range(mu['from'], mu.get('to', len(seq)), mu.get('hold', 1)):
            pcs = {m % 12 for m in C[seq[i]][0] + C[seq[i]][1]}
            prev = nearest(pcs, lo, hi, prev)
            j = min(len(seq) - 1, i + mu.get('hold', 1) - 1)
            t0 = starts[i] + rng.uniform(0.2, 0.7)
            dur = starts[j] + durs[j] - t0 - rng.uniform(0.2, 0.8)
            if rng.uniform() < mu.get('sigh', 0.3) and dur > 3:     # a sigh down to a neighbouring chord tone
                d1 = dur * rng.uniform(0.55, 0.7)
                notes.append((t0, d1 + 0.3, prev, mu['lv'] * rng.uniform(0.85, 1)))
                p2 = nearest(pcs, lo, hi, prev - 2)
                notes.append((t0 + d1, dur - d1, p2, mu['lv'] * 0.8))
                prev = p2
            else:
                notes.append((t0, dur, prev, mu['lv'] * rng.uniform(0.8, 1)))
            if t0 - last_end > 1.2 and mu.get('breath', True):
                vox += inhale(t0 - 0.42, N, 0.05 * mu['lv'])
            last_end = t0 + dur
        p, a = line(notes, end, glide=mu.get('glide', 0.3))
        vox += voice_open(p, a, mu.get('open', 0.5), tilt=1.7, breath=mu.get('air', 0.3), cut=2800) * mu.get('gain', 0.7)
    ke = sp.get('kee')
    if ke:      # the keen: high and thin, sliding up into each note, pushing (and cracking) at the top
        lo, hi = ke['reg']
        prev, notes = hi - 2, []
        for i in ke['at']:
            pcs = {m % 12 for m in C[seq[i]][1]}
            prev = nearest(pcs, lo, hi, prev + ke.get('lean', 1))
            t0 = starts[i] + rng.uniform(0.6, 1.3)
            notes.append((t0, min(durs[i] * 0.8, ke.get('max', 3.6)), prev, ke['lv'] * rng.uniform(0.85, 1)))
        p, a = line(notes, end, glide=0.1, scoop=ke.get('scoop', 2.0))
        if ke.get('crack'):        # a brief flip up near each note's peak, like a voice catching
            for (t0, d, m, lv) in notes:
                c0 = int((t0 + d * 0.45) * SR)
                L = int(0.11 * SR)
                if c0 + L < len(p):
                    p[c0:c0 + L] *= 2 ** (ke['crack'] / 12 * np.sin(np.linspace(0, np.pi, L)))
        vox += voice(p, a, EE, tilt=1.0, breath=ke.get('air', 0.5), jitter=0.003, rough=ke.get('rough', 0.4),
                     cut=7000) * ke.get('gain', 0.45)
    if mu or ke:
        e = sp.get('echo', (0.39, 0.38))
        vox = echo(vox, *e)
        vox = room(stereo(vox, 0.05), *sp.get('vroom', (4.5, 1.4, 0.8, 0.35)))
    return pno + vox * sp.get('vox', 0.75)

def pcs_of(*ms):
    return ms

V2 = dict(      # v1 with the edits: the voice forward and more voice-like, the keen rawer, a little sparser
    chords=CH, seq=SEQ, dur=4.6, breaths={3: 1.8, 7: 2.4, 11: 1.8}, answer=(8, 10, 12),
    mur=dict(reg=(52, 59), **{'from': 4}, hold=1, lv=0.9, open=0.6, sigh=0.35, gain=0.8),
    kee=dict(reg=(72, 81), at=[8, 9, 10, 12, 13, 14], lv=0.85, rough=0.5, crack=1.2, gain=0.5),
    vroom=(4.0, 1.6, 0.85, 0.28), vox=0.85)

AM = {'Am9': ([33, 40], [60, 64, 67, 71]), 'Dm9': ([38, 45], [60, 64, 65, 69]),
      'Fmaj7': ([41, 48], [57, 60, 64, 69]), 'Em7': ([40, 47], [55, 59, 62, 67])}
BERCEUSE = dict(    # the rocking lullaby (the EP's i-iv swaying): A minor, Am9 <-> Dm9, ~3.4 s a chord, voice soaring
    chords=AM, seq=['Am9', 'Dm9'] * 2 + ['Am9', 'Dm9', 'Fmaj7', 'Em7'] + ['Am9', 'Dm9'] * 2 + ['Fmaj7', 'Em7', 'Dm9', 'Am9'],
    dur=3.4, breaths={3: 1.2, 7: 2.0, 11: 1.2}, arp=[0, 2, 1, 3, 1, 2], gaps=(0.5, 0.62), flow=True, answer=(9, 11),
    mur=dict(reg=(57, 64), **{'from': 2}, hold=2, lv=0.9, open=0.5, sigh=0.5, gain=0.75),
    kee=dict(reg=(74, 84), at=[8, 10, 12, 13], lv=0.9, rough=0.45, crack=1.5, scoop=2.5, max=4.0, gain=0.5))

FS = {'F#m': ([42, 49], [57, 61, 66, 69]), 'E': ([40, 47], [56, 59, 64, 68]), 'Dmaj7': ([38, 45], [57, 61, 66, 69]),
      'Bm9': ([35, 42], [57, 61, 62, 66]), 'D': ([38, 45], [57, 62, 66, 69]), 'Esus4': ([40, 47], [57, 59, 64, 69])}
CASCADE = dict(     # the falling loop (i - bVII - bVI, as in the EP's circling minor loops): F# minor, flowing
    chords=FS, seq=['F#m', 'E', 'Dmaj7'] * 4 + ['Bm9', 'D', 'Esus4', 'F#m', 'Bm9', 'D', 'Esus4'] + ['F#m', 'E', 'Dmaj7', 'F#m'],
    dur=2.4, jit=0.05, breaths={11: 3.0, 18: 1.5}, arp=[0, 1, 2, 3, 2, 1], gaps=(0.36, 0.42), flow=True, arp_in=0.3,
    mur=dict(reg=(49, 56), **{'from': 3, 'to': 12}, hold=3, lv=0.85, open=0.35, sigh=0.6, gain=0.8, glide=0.45),
    kee=dict(reg=(73, 81), at=[12, 13, 14, 16, 17, 18], lv=0.8, rough=0.35, crack=1.0, gain=0.42),
    proom=(2.0, 2.8, 0.85, 0.2))

EB = {'Ebm': ([39, 46], [58, 63, 66, 70]), 'Cbmaj7': ([35, 42], [59, 63, 66, 70]), 'Gbadd9': ([42, 49], [56, 61, 66, 70]),
      'Db/F': ([41, 49], [56, 61, 65, 68]), 'Abm9': ([44, 51], [59, 63, 66, 70])}
NUIT = dict(        # the sparsest: E-flat minor, long chords, wide silences, the voice far away in the echo
    chords=EB, seq=['Ebm', 'Cbmaj7', 'Gbadd9', 'Db/F', 'Ebm', 'Cbmaj7', 'Abm9', 'Ebm'],
    dur=6.4, breaths={1: 2.4, 3: 3.0, 5: 2.4}, arp=[1, 2, 3], gaps=(0.9, 1.2), min_steps=3, arp_in=1.0, pv=0.85,
    mur=dict(reg=(51, 58), **{'from': 1}, hold=1, lv=0.75, open=0.3, sigh=0.4, gain=0.65, air=0.45),
    kee=dict(reg=(75, 82), at=[6], lv=0.6, rough=0.25, crack=0.8, gain=0.35, max=4.5),
    echo=(0.62, 0.45), vroom=(6.0, 1.0, 0.6, 0.6), vox=0.65, tail=8)

VARIANTS = dict(velours2=V2, berceuse=BERCEUSE, cascade=CASCADE, nuit=NUIT)

if __name__ == '__main__':
    which = sys.argv[1]
    if which == 'velours':
        write(velours(), sys.argv[2])
    else:
        write(piece(VARIANTS[which]), sys.argv[2])
