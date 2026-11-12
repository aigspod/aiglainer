"""An original small-combo jazz tune for the jazz edition of the hackathon invitation: 96 bpm, swung eighths, in F,
lifting a whole step to G for the open questions and staying there to the end.

The band, all synthesized here (nothing is sampled):
  brushes   a soft stirred swish on every beat, a brush tap on 2 and 4, a feathered kick
  ride      the ride pattern (ding, ding-a-ding) with the hi-hat foot on 2 and 4, in the fuller sections
  bass      an upright-style plucked bass, walking quarter notes, or a calmer two-feel of half notes
  rhodes    an FM electric piano comping on rootless 9th and 13th voicings (ii-V-I movement), with a gentle tremolo
  vibes     the lead: a vibraphone with motor tremolo, playing the tune's motif (5-6-1 up to the major 7th, "da-da-DAA,
            daaa"); on the very last bar the motif finally resolves up to the tonic, over a held chord
  horns     a soft muted-brass pad under the choruses, for warmth

The arrangement is read from narration.py: every scene lists its sections bar by bar (`mus`), so the track has exactly
the timeline's bars and scene changes fall on phrase boundaries. Sections:

  intro   rhodes and the motif on vibes, brushes, a little vinyl warmth     two     brushes, two-feel bass, sparse comping
  walk    walking bass, ride, brighter comping                               turn    one bar of ii-V with a soft fill
  chorus  the full band and the tune (the title; the open questions)        lift    three bars climbing into G, crescendo
  break   hushed: rhodes, bass, a whisper of brushes                         coda    the tune's first four bars, last time
  outro   the tonic chord, held, while the motif resolves

The lead lays out under the narrator and the drummer plays lighter (it reads the line times from narration.py), as a band would for a singer.
The render is cached by a hash of this file, the arrangement and those times: project.py asks `ensure()` for the path.
Listen with: make listen F=projects/hackathon/videos/invite-jazz/<path> Q="..."
"""
import hashlib, os, sys, wave
import numpy as np
from scipy.signal import fftconvolve, lfilter
from scipy.ndimage import maximum_filter1d

HERE = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':          # run on its own: make the engine and the invite (for event.py) importable
    sys.path[:0] = [os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')), HERE, os.path.join(HERE, '..', 'invite')]
from aiglainer.audio import SR, mtof, lp, hp, bp
from beat import BPM, BEAT, BAR, SWING

# ---------------------------------------------------------------- harmony
# chords in F (tonic F): bass root, rootless voicing for the rhodes, chord tones (semitones over the root) for the bass
CHORDS = {
    'Imaj9':    (41, [57, 60, 64, 67], [0, 4, 7, 11]),     # Fmaj9:  A C E G
    'VI7b9':    (38, [54, 60, 63, 69], [0, 4, 7, 10]),     # D7b9:   F# C Eb A
    'ii9':      (43, [58, 62, 65, 69], [0, 3, 7, 10]),     # Gm9:    Bb D F A
    'V13':      (36, [58, 62, 64, 69], [0, 4, 7, 10]),     # C13:    Bb D E A
    'iii7':     (45, [55, 60, 64, 67], [0, 3, 7, 10]),     # Am7:    G C E G
    'IVmaj9':   (46, [57, 60, 62, 65], [0, 4, 7, 11]),     # Bbmaj9: A C D F
    'bVIImaj9': (39, [55, 58, 62, 65], [0, 4, 7, 11]),     # Ebmaj9: G Bb D F
}
# one entry per bar; a bar with two chords changes on beat 3. 'x+2' is chord x a whole step up (the pivot into G).
CHARTS = dict(
    intro=[['Imaj9'], ['IVmaj9']],
    two=[['ii9'], ['V13'], ['Imaj9'], ['VI7b9']],
    walk=[['Imaj9'], ['VI7b9'], ['ii9'], ['V13']],
    turn=[['ii9', 'V13']],
    chorus=[['Imaj9'], ['VI7b9'], ['ii9'], ['V13'], ['iii7', 'VI7b9'], ['ii9', 'V13'], ['Imaj9'], ['ii9', 'V13']],
    lift=[['IVmaj9'], ['bVIImaj9'], ['ii9+2', 'V13+2']],
    break_=[['IVmaj9'], ['iii7', 'VI7b9'], ['ii9']],
    coda=[['Imaj9'], ['VI7b9'], ['ii9'], ['V13']],
    outro=[['Imaj9']],
)
KEY_AFTER = dict(lift=2)      # the key (semitones over F) from the end of this section on

# the tune, in semitones over the tonic (F4 = 65, or G4 = 67 after the lift): (bar, beat, beats long, degree)
TUNE = [(0, 0, .5, 7), (0, .5, .5, 9), (0, 1, 1, 12), (0, 2, 2, 11),                         # the motif: 5 6 1 . 7
        (1, 0, .5, 10), (1, .5, .5, 9), (1, 1, 1, 7), (1, 2, 1.5, 4), (1, 3.5, .5, 1),
        (2, 0, .5, 9), (2, .5, .5, 11), (2, 1, 1, 14), (2, 2, 2, 12),                         # the motif on ii
        (3, 0, 1.5, 11), (3, 1.5, .5, 9), (3, 2, 1, 7), (3, 3, 1, 5),
        (4, 0, 1, 4), (4, 1, .5, 7), (4, 1.5, .5, 11), (4, 2, 1.5, 13), (4, 3.5, .5, 10),
        (5, 0, 1.5, 9), (5, 1.5, .5, 12), (5, 2, 1.5, 11), (5, 3.5, .5, 7),
        (6, 0, .5, 7), (6, .5, .5, 9), (6, 1, 1, 12), (6, 2, 2, 11),                          # the motif, home
        (7, 0, 1, 9), (7, 1, 1, 7), (7, 2, 2, 4)]
LEADS = dict(
    intro=[(0, 0, .5, 7), (0, .5, .5, 9), (0, 1, 1, 12), (0, 2, 2, 11), (1, 0, 1, 9), (1, 1, 1, 7), (1, 2, 2, 4)],
    chorus=TUNE,
    coda=TUNE[:17],
    lift=[(0, 1, .5, 0), (0, 1.5, .5, 4), (0, 2, 2, 9), (1, 1, .5, 2), (1, 1.5, .5, 5), (1, 2, 2, 12),
          (2, 0, .5, 11), (2, .5, .5, 14), (2, 1, 1, 16), (2, 2, .5, 13), (2, 2.5, .5, 11), (2, 3, 1, 7)],
    outro=[(0, 0, .5, 7), (0, .5, .5, 9), (0, 1, 1, 11), (0, 2, 6, 12)],      # the motif, resolving up to the tonic
)
# (the lift's lead is written in F, its last bar too: E G A over Am7, F# E C over D7, the ii-V into G)

# how present each part is per section (0 or missing = silent), and how the bass and comping play
MIXES = dict(
    intro=dict(rhodes=.8, vibes=.65, swish=.55, kick=0, vinyl=1, comp='whole', bass=None),
    two=dict(rhodes=.75, swish=.8, tap=.7, kick=.35, comp='sparse', bass='two'),
    walk=dict(rhodes=.8, ride=.65, foot=.6, swish=.35, tap=.4, kick=.45, comp='charleston', bass='walk'),
    turn=dict(rhodes=.8, swish=.8, tap=.7, kick=.4, comp='halves', bass='walk', fill=True),
    chorus=dict(rhodes=.9, vibes=1, horns=.8, ride=.85, foot=.7, swish=.3, tap=.45, kick=.55, comp='charleston', bass='walk', crash=.5),
    lift=dict(rhodes=.9, vibes=.8, horns=.6, swish=.9, tap=.6, ride=.5, kick=.45, comp='halves', bass='walk', fill=True),
    break_=dict(rhodes=.7, swish=.45, kick=0, comp='whole', bass='two'),
    coda=dict(rhodes=.9, vibes=1, horns=.8, ride=.85, foot=.7, swish=.3, tap=.45, kick=.55, comp='charleston', bass='walk', crash=.5),
    outro=dict(rhodes=1, vibes=1, horns=.7, ride=.35, comp='roll', bass='hold', vinyl=1),
)
GAIN = dict(swish=.14, tap=.34, kick=.38, ride=.16, foot=.24, crash=.075, fill=.34, bass=.36, rhodes=.15, vibes=.18,
            horns=.045, vinyl=.03)
# loudness of each kind of section (at its start, at its end), applied smoothly after the limiter
LEVELS = dict(intro=(.66, .70), two=(.78, .78), walk=(.80, .80), turn=(.76, .86), chorus=(.92, .92), lift=(.76, .92),
              break_=(.70, .70), coda=(.92, .92), outro=(.92, .92))


def sections():
    """[(kind, bars)] for the whole piece, from narration.py."""
    import narration
    return [('break_' if k == 'break' else k, n) for sd in narration.SCENES for n, k in sd['mus']]


def voiced():
    """[(t0, t1)] when the narrator speaks, from narration.py's laid-out lines and the cached clips (or a guess)."""
    import narration
    out, T = [], 0.0
    for sd in narration.SCENES:
        for v, text in sd['beats']:
            d = narration._clip_seconds(text) or (0.9 + 0.4 * len(text.split()))
            out.append((round(T + v + 0.35, 2), round(T + v + d, 2)))      # clips open with ~0.4 s of silence
        T += sd['bars'] * BAR
    return out


def ensure():
    """Path (relative to the project) of the rendered track for the current arrangement; renders it if missing."""
    secs, vo = sections(), voiced()
    key = hashlib.sha1(open(__file__, 'rb').read() + repr((secs, vo, BPM, SWING)).encode()).hexdigest()[:12]
    rel = os.path.join('cache', f'music_{key}.wav')
    path = os.path.join(HERE, rel)
    if not os.path.exists(path):
        print(f'music.py: rendering {rel}', file=sys.stderr, flush=True)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        x = render(secs, vo)
        tmp = path + f'.{os.getpid()}.tmp'
        with wave.open(tmp, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((x * 32767).astype(np.int16).tobytes())
        os.replace(tmp, path)
    return rel


# ---------------------------------------------------------------- instruments (mono)
rng = np.random.default_rng(1959)


def sw(beat):
    """Swing a position in beats: an off-beat eighth falls late, at SWING of the beat."""
    q, f = divmod(beat, 1.0)
    return q + (SWING if abs(f - 0.5) < 1e-6 else f)


def fade_edges(x, a=0.003, r=0.03):
    n = len(x)
    A, R = min(int(a * SR), n), min(int(r * SR), n)
    x[:A] *= np.linspace(0, 1, A, False)
    if R:
        x[n - R:] *= np.linspace(1, 0, R)
    return x


def rhodes(f, sec, vel=0.8):
    """FM electric piano: a 1:1 pair whose brightness dies away, plus a quiet bell-like tine at the 14th partial."""
    n = int(sec * SR)
    t = np.arange(n) / SR
    idx = (0.8 + 2.2 * vel) * np.exp(-t * 4.0) + 0.3
    body = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    tine = np.sin(2 * np.pi * f * 14.0 * t + 0.4 * np.sin(2 * np.pi * f * t)) * np.exp(-t * 22) * 0.2 * vel
    decay = np.exp(-t * (0.55 + f / 900))
    x = (body * decay + tine) * vel
    x = np.tanh(x * (0.8 + 0.6 * vel)) / (0.8 + 0.6 * vel)                # a little bark when played harder
    return fade_edges(x, 0.002, 0.12)


def vibes(f, sec, vel=0.9):
    """Vibraphone: partials at 1, 4 and 10 times the pitch, the upper ones shorter, a soft mallet, motor tremolo."""
    n = int((sec + 1.6) * SR)            # bars ring on after the note (pedal), then the damper
    t = np.arange(n) / SR
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t * 0.9)
         + 0.32 * np.sin(2 * np.pi * f * 3.98 * t) * np.exp(-t * 3.5)
         + 0.06 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 11))
    trem = 1 - 0.22 * (0.5 - 0.5 * np.cos(2 * np.pi * 5.2 * t))
    damp = np.clip(1 - (t - sec - 0.35) / 1.2, 0, 1)
    mallet = lp(rng.normal(0, 1, n), 2500) * np.exp(-t * 300) * 0.25
    return fade_edges((x * trem + mallet) * damp * vel, 0.0015, 0.05)


def bass_note(f, sec, vel=0.85):
    """Upright-style plucked bass: decaying partials plucked near the end of the string, a thump, a woody body."""
    n = int((sec + 0.12) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for h in range(1, 14):
        if f * h > 3200:
            break
        a = abs(np.sin(np.pi * h * 0.16)) / h ** 0.8
        x += a * np.sin(2 * np.pi * f * h * (1 + 0.0004 * h * h) * t + rng.uniform(0, 0.3)) * np.exp(-t * (2.2 + 2.6 * h))
    x += 0.15 * np.sin(2 * np.pi * f * t) * np.exp(-t * 2.5)              # the round fundamental
    x += bp(rng.normal(0, 1, n), 300, 1800) * np.exp(-t * 45) * 0.35      # finger on the string
    off = np.clip(1 - (t - sec) / 0.09, 0, 1)                             # damped when the next note comes
    return fade_edges(x * off * vel, 0.004, 0.02)


def horn(f, sec, vel=0.7):
    """A soft muted-brass pad: two detuned saws, darkly filtered, slow to speak."""
    n = int((sec + 0.4) * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for det in (-0.07, 0.07):
        ph = (np.cumsum(np.full(n, f * 2 ** (det / 12) / SR)) + rng.uniform()) % 1.0
        x += 2 * ph - 1
    e = np.clip(t / 0.18, 0, 1) * np.clip(1 - (t - sec) / 0.4, 0, 1)
    return lp(lp(x, 1100), 1600) * e * vel


def swish(sec):
    """A brush stirred on the snare for one beat: band-passed noise that swells and fades."""
    n = int(sec * SR)
    t = np.arange(n) / SR
    e = np.sin(np.pi * np.clip(t / sec, 0, 1)) ** 1.5
    return bp(rng.normal(0, 1, n), 1800, 6500) * e


def tap():
    n = int(0.35 * SR); t = np.arange(n) / SR
    x = bp(rng.normal(0, 1, n), 1200, 6000) * np.exp(-t * 22) + 0.35 * np.sin(2 * np.pi * 185 * t) * np.exp(-t * 32)
    return fade_edges(x, 0.002, 0.02)


def kick():
    n = int(0.4 * SR); t = np.arange(n) / SR
    f = 52 + 30 * np.exp(-t * 25)
    return fade_edges(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9), 0.004, 0.03)


def ride(vel=1.0, sec=2.2):
    """A dark ride cymbal: a cluster of inharmonic partials and a hiss, a soft stick."""
    n = int(sec * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for f, a in ((420, .5), (1130, .35), (1790, .3), (2510, .3), (3320, .22), (4310, .16), (5470, .1)):
        x += a * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * (2.2 + f / 2200))
    x += hp(rng.normal(0, 1, n), 4500) * np.exp(-t * 3.0) * 0.5
    x += hp(rng.normal(0, 1, n), 2000) * np.exp(-t * 90) * 0.6          # the stick
    return fade_edges(lp(x, 8500) * vel, 0.001, 0.2)


def foot():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return fade_edges(bp(rng.normal(0, 1, n), 3000, 9000) * np.exp(-t * 60), 0.002, 0.02)


def crash(sec=4.0):
    n = int(sec * SR); t = np.arange(n) / SR
    x = hp(rng.normal(0, 1, n), 2500) * np.exp(-t * 1.1)
    for f in (610, 1480, 2290, 3170):
        x += 0.15 * np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * 1.6)
    return fade_edges(lp(x, 7000) * np.clip(t / 0.02, 0, 1), 0.001, 0.3)


def vinyl(n):
    """A little record warmth: faint hiss and sparse soft crackle."""
    x = lp(rng.normal(0, 1, n), 3500) * 0.08
    k = rng.random(n) < 7 / SR
    pops = np.zeros(n)
    pops[k] = rng.normal(0, 1, k.sum())
    return x + bp(np.convolve(pops, np.exp(-np.arange(int(0.002 * SR)) / 20), 'same'), 900, 5000) * 1.2


def place(buf, x, t, pan=0.0, gain=1.0):
    i = int(round(t * SR))
    if i >= len(buf) or i + len(x) <= 0:
        return
    if i < 0:
        x, i = x[-i:], 0
    m = min(len(x), len(buf) - i)
    l, r = np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414
    buf[i:i + m, 0] += x[:m] * l * gain
    buf[i:i + m, 1] += x[:m] * r * gain


def jit(s=0.006):
    return float(rng.normal(0, s))


# ---------------------------------------------------------------- arrangement
def chord(name, key):
    """(bass root, voicing, tones) for a chart entry in the current key; 'x+2' shifts a chord a whole step."""
    sh = key
    if '+' in name:
        name, extra = name.split('+')
        sh = int(extra)
    root, voicing, tones = CHORDS[name]
    return root + sh, [m + sh for m in voicing], tones


def near(pc_note, prev, lo=31, hi=50):
    """The octave of a note (any octave) closest to prev, within the bass's range."""
    cands = [pc_note % 12 + 12 * o for o in range(1, 6)]
    cands = [c for c in cands if lo <= c <= hi] or cands
    return min(cands, key=lambda c: abs(c - prev))


def render(secs, vo):
    bars = []                     # (kind, index within section, section length, key)
    key = 0
    for kind, n in secs:
        for i in range(n):
            bars.append((kind, i, n, key))
        key = KEY_AFTER.get(kind, key)
    # chord per beat, for the whole piece (the bass looks ahead to the next chord)
    beats = []
    for kind, i, n, k in bars:
        ch = CHARTS[kind][i % len(CHARTS[kind])]
        for q in range(4):
            beats.append(chord(ch[0] if len(ch) == 1 or q < 2 else ch[1], k))
    total = len(bars) * BAR
    N = int((total + 4.0) * SR)
    parts = {k: np.zeros((N, 2)) for k in GAIN}
    voice_on = np.zeros(int(total * 20) + 1, bool)               # 50 ms blocks when the narrator speaks
    for a, z in vo:
        voice_on[max(0, int((a - 0.25) * 20)):int((z + 0.35) * 20)] = True

    def speaking(t0, t1):
        return voice_on[max(0, int(t0 * 20)):max(int(t0 * 20) + 1, int(t1 * 20))].any()

    T, KK, FT, CR = tap(), kick(), foot(), crash()
    prev_bass = 41
    for bi, (kind, i, n, k) in enumerate(bars):
        M = MIXES[kind]
        t0 = bi * BAR
        last = i == n - 1
        # -------------------------------------------------- drums
        for q in range(4):
            tb = t0 + q * BEAT
            soft_ = 0.6 if speaking(tb - 0.05, tb + BEAT) else 1.0                # the drummer plays lighter under the voice
            if M.get('swish'):
                place(parts['swish'], swish(BEAT * 1.05), tb + jit(0.01), 0.15 * (-1) ** q, soft_ * M['swish'] * (1.0 if q % 2 else 0.8))
            if M.get('tap') and q in (1, 3):
                place(parts['tap'], T, tb + jit(), 0.1, soft_ * M['tap'] * (0.9 + 0.2 * rng.random()))
            if M.get('kick') and (q in (0, 2) or kind in ('walk', 'chorus', 'coda')):
                place(parts['kick'], KK, tb + jit(0.004), 0, M['kick'] * (1.0 if q == 0 else 0.7))
            if M.get('foot') and q in (1, 3):
                place(parts['foot'], FT, tb + jit(0.004), -0.35, M['foot'])
            if M.get('ride'):
                v = soft_ * M['ride'] * (1.0 if q in (1, 3) else 0.82)
                place(parts['ride'], ride(v), tb + jit(0.004), 0.45)
                if q in (1, 3):                                  # the skip note: ding, ding-a-ding
                    place(parts['ride'], ride(0.55 * soft_ * M['ride'], 1.2), t0 + sw(q + 0.5) * BEAT + jit(0.004), 0.45)
        if M.get('crash') and i == 0:
            place(parts['crash'], CR, t0, -0.3, M['crash'] * (0.5 if speaking(t0, t0 + BAR) else 1.0))
        if M.get('fill') and last:     # a soft fill into the next downbeat: brush triplets on 3 and 4, rising
            for s in range(6):
                tt = t0 + (2 + s / 3) * BEAT
                place(parts['fill'], tap(), tt + jit(0.004), -0.2 + 0.08 * s, 0.35 + 0.13 * s)
        if M.get('vinyl') and i == 0:
            L = int(n * BAR * SR)
            v = vinyl(L)
            u = np.arange(L) / L
            env_ = np.clip(1.2 - u, 0, 1) if kind == 'intro' else np.clip(u * 3, 0, 1)
            place(parts['vinyl'], v * env_, t0, 0.0, M['vinyl'])
        # -------------------------------------------------- bass
        style = M.get('bass')
        bb = bi * 4
        if style == 'walk':
            for q in range(4):
                root, _, tones = beats[bb + q]
                nroot = beats[bb + q + 1][0] if bb + q + 1 < len(beats) else root
                starts = q == 0 or beats[bb + q - 1][0] != root
                changes = nroot != root or q == 3
                if starts:
                    note = near(root, prev_bass)
                elif changes and bb + q + 1 < len(beats):
                    tgt = near(nroot, prev_bass)
                    note = tgt + (1 if tgt < prev_bass else -1)                  # chromatic approach
                else:
                    opts = [near(root + iv, prev_bass) for iv in tones[1:]]
                    tgt = near(nroot, prev_bass)
                    note = min(opts, key=lambda m: abs(m - (prev_bass + tgt) / 2) + 0.3 * rng.random())
                    if note == prev_bass:
                        note = opts[(opts.index(note) + 1) % len(opts)]
                place(parts['bass'], bass_note(mtof(note), BEAT * 0.98, 0.85 + 0.15 * (q == 0)), t0 + q * BEAT + jit(0.004), 0)
                prev_bass = note
        elif style == 'two':
            for q in (0, 2):
                root = beats[bb + q][0]
                nroot = beats[bb + 4][0] if bb + 4 < len(beats) else root
                if q == 0 or root != beats[bb][0]:
                    note = near(root, prev_bass)                                 # a chord's first beat: its root
                elif nroot == root:
                    note = near(root + 7, prev_bass)                             # the fifth
                else:
                    tgt = near(nroot, prev_bass)
                    note = tgt + (1 if tgt < prev_bass else -1)                  # a half step into the next root
                place(parts['bass'], bass_note(mtof(note), BEAT * 1.96, 0.85), t0 + q * BEAT + jit(0.004), 0)
                prev_bass = note
                if q == 2 and rng.random() < 0.5:                                # a swung pickup now and then
                    place(parts['bass'], bass_note(mtof(note), BEAT * 0.3, 0.45), t0 + sw(3.5) * BEAT, 0)
        elif style == 'hold' and i == 0:
            root = beats[bb][0]
            note = near(root, prev_bass, 33, 45)
            place(parts['bass'], bass_note(mtof(note), BAR * n, 0.9), t0, 0)
            L = int(BAR * n * SR); tt = np.arange(L) / SR                        # and the low root ringing under it
            place(parts['bass'], np.sin(2 * np.pi * mtof(note) * tt) * np.exp(-tt * 0.5) * np.clip(tt / 0.05, 0, 1) * 0.35, t0, 0)
        # -------------------------------------------------- rhodes comping
        comp = M.get('comp')
        hits = dict(whole=[(0, 3.9, .75)], sparse=[(0, 1.4, .7), (2.5, 1.2, .62)] if i % 2 == 0 else [(1.5, 2.3, .66)],
                    charleston=[(0, 1.3, .8), (1.5, 1.6, .72)] if i % 2 == 0 else [(0.5, 1.0, .7), (2, 1.3, .75), (3.5, .5, .62)],
                    halves=[(0, 1.8, .8), (2, 1.6, .78), (3.5, .5, .6)], roll=[(0, 4 * n, .8)] if i == 0 else []).get(comp, [])
        for pos, ln, vel in hits:
            tpos = sw(pos)
            bidx = bb + min(int(tpos + 0.5), 4)                                  # an anticipation takes the next chord
            root, voicing, _ = beats[min(bidx, len(beats) - 1)]
            spread = 0.035 if comp == 'roll' else 0.012
            if comp == 'roll':
                voicing = [root + 12] + voicing + [voicing[1] + 12]               # the last chord, root and all
            for j, m in enumerate(voicing):
                x = rhodes(mtof(m), ln * BEAT + 0.25, vel * (0.92 + 0.1 * rng.random()))
                place(parts['rhodes'], x, t0 + tpos * BEAT + j * spread + jit(0.004), -0.35 + 0.23 * j, M['rhodes'])
        # -------------------------------------------------- horns under the choruses
        if M.get('horns'):
            for h in range(2 if len(CHARTS[kind][i % len(CHARTS[kind])]) == 2 else 1):
                _, voicing, _ = beats[bb + 2 * h]
                ln = (2 if h == 0 and len(CHARTS[kind][i % len(CHARTS[kind])]) == 2 else 4) * BEAT
                notes = voicing[1:]
                if kind == 'outro':
                    ln = BAR * n if i == 0 else 0
                    notes = [beats[bb][0] + 12] + voicing
                if ln:
                    for j, m in enumerate(notes):
                        place(parts['horns'], horn(mtof(m), ln, 0.8), t0 + 2 * h * BEAT, -0.5 + 0.5 * j, M['horns'])
        # -------------------------------------------------- the lead
        if M.get('vibes') and kind in LEADS:
            tonic = 65 + (k if kind != 'lift' else 0)
            ph = LEADS[kind]
            plen = max(p[0] for p in ph) + 1
            for (pb, pos, ln, deg) in ph:
                if pb != i % plen or (kind == 'outro' and i >= plen):
                    continue
                ts = t0 + sw(pos) * BEAT
                if speaking(ts - 0.1, ts + ln * BEAT):
                    continue                                                     # lay out for the narrator
                x = vibes(mtof(tonic + deg), ln * BEAT, (0.85 + 0.15 * (pos % 1 == 0)) * M['vibes'])
                place(parts['vibes'], x, ts + jit(0.004), 0.2)
    # -------------------------------------------------- mix
    parts['bass'] = lp(hp(parts['bass'], 38), 3000)
    parts['rhodes'] = hp(parts['rhodes'], 110)
    tt = np.arange(N) / SR
    trem = 0.18 * np.sin(2 * np.pi * 4.4 * tt)                                   # the suitcase's stereo tremolo
    parts['rhodes'][:, 0] *= 1 + trem
    parts['rhodes'][:, 1] *= 1 - trem
    parts['horns'] = hp(parts['horns'], 160)
    parts['ride'] = hp(parts['ride'], 300)
    dry = sum(parts[k] * GAIN[k] for k in parts)
    send = sum(parts[k] * GAIN[k] * w for k, w in (('rhodes', .4), ('vibes', .55), ('horns', .5), ('swish', .25),
                                                    ('tap', .2), ('fill', .25), ('ride', .15), ('crash', .3), ('bass', .05)))
    n_ir = int(2.2 * SR); ti = np.arange(n_ir) / SR
    ir = lp(rng.normal(0, 1, (n_ir, 2)) * np.exp(-3.2 * ti)[:, None], 5500)
    ir[:int(0.018 * SR)] = 0                                                     # a little pre-delay
    ir /= np.sqrt((ir ** 2).sum(0))
    wet = np.stack([fftconvolve(send[:, c], ir[:, c])[:N] for c in range(2)], 1)
    mix = dry + hp(wet, 180) * 0.5
    mix = hp(mix, 30)
    mix = mix - 0.25 * bp(mix, 180, 380)                                         # less mud in the low mids
    mix = limit(mix)
    mix *= section_gain(bars, N)[:, None]
    mix = mix / np.abs(mix).max() * 0.89
    return mix[:int((total + 3.0) * SR)]


def limit(x, ceiling=0.5):
    """A gentle limiter: a smoothed peak envelope (fast attack, slow release) sets the gain, then a soft clip."""
    x = x / np.abs(x).max()
    pk = maximum_filter1d(np.abs(x).max(1), int(0.01 * SR))
    a = np.exp(-1 / (0.25 * SR))
    env = lfilter([1 - a], [1, -a], pk)
    env = np.maximum(env, pk * 0.7)
    g = np.minimum(1.0, ceiling / np.maximum(env, 1e-6))
    g = lfilter([1 - np.exp(-1 / (0.02 * SR))], [1, -np.exp(-1 / (0.02 * SR))], g)
    y = x * g[:, None]
    return np.tanh(y * 1.4) / 1.4


def section_gain(bars, N):
    """Gain per sample from LEVELS, every change eased over a beat on either side of the bar line (no steps)."""
    per = np.empty(len(bars) + 1)
    g = np.empty(N)
    for k, (kind, i, n, _) in enumerate(bars):
        a, z = LEVELS[kind]
        j0, j1 = int(k * BAR * SR), int((k + 1) * BAR * SR)
        g[j0:j1] = a + (z - a) * (i + np.linspace(0, 1, j1 - j0, False)) / n
    end = int(len(bars) * BAR * SR)
    g[end:] = LEVELS[bars[-1][0]][1]
    L = int(BEAT * SR)
    for k in range(1, len(bars)):
        j = int(k * BAR * SR)
        before, after = g[j - L - 1], g[min(j + L, N - 1)]
        if abs(after - before) > 1e-3:
            g[j - L:j + L] = before + (after - before) * (0.5 - 0.5 * np.cos(np.linspace(0, np.pi, 2 * L)))
    return g


if __name__ == '__main__':
    print(os.path.join(HERE, ensure()))
