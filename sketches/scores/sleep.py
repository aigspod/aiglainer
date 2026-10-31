"""Score sketches after Max Richter, *nor earth, nor boundless sea* (from *Sleep*, 2015). Original material.
The title is the first line of Shakespeare's Sonnet 65, and all three follow it: fourteen phrases, one per line,
each a 'ta.. ta.. taaah' (two short, separate notes, then one held: the line coming to rest on its last word).
Lines 1-8 (brass, stone, the siege of days) sigh downwards in D minor, coloured by major sevenths and ninths;
lines 9-12 ("O fearful meditation!", four questions) repeat notes and climb, and line 12 hangs on Am7; the
couplet ("in black ink my love may still shine bright") turns to F major, then the loop falls back to D minor.
The strings thin to near-silence at the end of each quatrain, and the room is close rather than a hall.
  boundless  the main bed: string sections, the phrases on cellos then violins; a few far-back piano notes
  sonnet     the phrases sung by one wordless soprano over hushed strings and a soft organ
  brass      the stillest: longer lines, the phrases low on cellos, one solo-violin A held across everything
Usage: python sleep.py boundless|sonnet|brass out.wav [seconds]"""
import sys, wave
import numpy as np
import aiglainer.scores as S
from aiglainer.audio import SR, mtof, env_adsr, lp, hp
from aiglainer.scores import grand, choir, place, hall, soft
import samples                                      # VSCO 2 CE strings (CC0), fetched on first use

Dm, Dm_C, Bbma7, Am7 = [38, 50, 57, 62, 65], [36, 48, 57, 62, 65], [34, 46, 57, 62, 65], [33, 45, 55, 60, 64]
Gm9, Fma7, Bbma9, F = [43, 50, 57, 58, 62], [41, 48, 57, 60, 64], [46, 50, 57, 60, 65], [41, 53, 60, 64, 69]
SONNET = [                                          # (chord, ta, ta, taaah), one per line of the poem
    (Dm, 77, 76, 74), (Dm_C, 74, 76, 77), (Bbma7, 77, 76, 74), (Am7, 74, 72, 69),         # brass, nor stone ...
    (Gm9, 74, 70, 69), (Fma7, 72, 74, 77), (Bbma9, 74, 77, 81), (Am7, 81, 79, 76),        # summer's honey breath ...
    (Dm, 77, 77, 76), (Dm_C, 76, 76, 77), (Bbma7, 77, 77, 81), (Am7, 81, 81, 79),         # O fearful meditation ...
    (Bbma7, 77, 76, 74), (F, 72, 77, 81)]                                                 # O, none, unless ...
TA = (0.6, 1.8, 3.0)                                # onsets within a line: two shorter notes leading into a long one
BREATH = (3, 7, 11)                                 # quatrain ends: the strings thin to near-silence before the next

def organ(freq, n, att=2.5, rel=3.0):
    """A soft flue stop: a few octave partials, no vibrato, a slow wind-up."""
    t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * freq * h * t + S.rng.uniform(0, 6)) for h, a in ((1, 1.0), (2, 0.35), (3, 0.12), (4, 0.08)))
    return lp(x * env_adsr(n, att, 0.5, 0.9, rel), 1800)

def section(m):
    """Which section plays a note: basses, cellos, violas or violins, by register."""
    return 'bass' if m < 40 else 'cellos' if m < 53 else 'violas' if m < 67 else 'violins'

def bow(m, L, cutoff, inst=None, still=False):
    """A sampled string note, L samples long, stereo, darkened above `cutoff`. `still` blends the two nearest
    samples: their vibratos don't line up, so together they waver less (the samples all have vibrato)."""
    inst = inst or section(m)
    x = samples.note(inst, m, L / SR)
    if still:
        x = (x + samples.note(inst, m, L / SR, rank=1)) * 0.6
    return lp(x, cutoff) * 0.5

def pan2(x, pan):
    """Balance a stereo sample left or right (constant power), keeping its own width."""
    return x * [np.cos((pan + 1) * np.pi / 4) * 1.414, np.sin((pan + 1) * np.pi / 4) * 1.414]

ARC = (0.8, 0.9, 1.0, 0.85)                         # each quatrain builds to its third line, then eases into the breath

def swell(L, line, k):
    """The strings breathing: each line grows towards its middle and eases off at its end (the next line's swell
    overlaps it), riding a larger arc across the quatrain. Returns (loudness, brightness 0..1) per sample."""
    t = np.arange(L) / SR
    s = 0.5 - 0.5 * np.cos(2 * np.pi * np.clip(t / (line + 1.5), 0, 1))
    return (0.45 + 0.55 * s) * ARC[min(k % 14, 12) % 4], s

def strings(dry, send, chord, t0, line, att, lvl, parts):
    """The chord on the string sections, swelling: (slice of the chord, gain, cutoff, pans). `line` is (k, LN).
    Brightness follows the swell (a dark and a brighter copy crossfaded), so it sounds bowed, not turned up."""
    (k, LN), L = line, bed(*line)
    e = env_adsr(L, att, 0.8, 0.88, att * 0.9)
    amp, s = swell(L, LN, k)
    for sl, g, cut, pans in parts:
        for j, m in enumerate(chord[sl]):
            x = bow(m, L, 9000, still=True)
            x = lp(x, cut * 1.6) * (1 - s)[:, None] + lp(x, cut * 3.5) * s[:, None]
            x = pan2(x * (e * amp)[:, None] * lvl * g, pans[j % len(pans)])
            place(dry, x * 0.75, t0); place(send, x * 0.6, t0)

def bed(k, LN, tail=4):
    """How long line k's strings sound: past the next downbeat, except at a quatrain's end, where they let go early."""
    return int((LN - 0.6 if k % 14 in BREATH else LN + tail) * SR)

def room(dry, send):
    """Close and intimate: a short, dark room, little of it."""
    return hall(dry, send * 0.55, 4.0, 1.4)

def phrase(dry, send, notes, t0, line, voice, lvl, pan, wet=0.8):
    """One line, legato: two shorter notes leading into a long one, each bowed in softly and overlapping the next,
    the long one running on under the next line's first note. The line's shape stays (short, short, long) without
    gaps or accents, so it flows inside the strings rather than speaking over them."""
    for i, (m, on) in enumerate(zip(notes, TA)):
        last = i == 2
        L = int(((line - on + 0.8) if last else (TA[i + 1] - on + 0.45)) * SR)
        e = env_adsr(L, 0.9 if last else 0.3, 0.6, 0.9 if last else 0.85, 1.8 if last else 0.5)
        x = voice(m, L)
        x = (x * e[:, None] if x.ndim == 2 else x * e) * lvl * (0.75 if last else 0.6)
        x = pan2(x, pan) if x.ndim == 2 else x
        place(dry, x * 0.6, t0 + on, pan); place(send, x * wet, t0 + on, pan)

def violin(m, L):
    return bow(m, L, 3500, 'violins')

def cello(m, L):
    return bow(m, L, 3500, 'cellos')

def soprano(m, L):
    return choir(mtof(m), L, 0.3, voices=1, att=0.01, rel=0.01)  # synthesized (no free soprano samples); phrase() shapes it

def boundless(total, arp_on):
    """8 s a line: cellos and basses, violas and violins from the second line; the phrases on cellos an octave down
    for the first quatrain, then on violins; while arp_on, a piano note in the gap of every other line."""
    LN = 8.0
    n = int((total + 12) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    for k in range(int(total / LN) + 1):
        ch, *notes = SONNET[k % 14]
        t0 = k * LN
        upper = [(slice(2, 5), min(1, k / 2), 2200, (-0.5, 0.1, 0.5))] if k >= 1 else []
        strings(dry, send, ch, t0, (k, LN), 3.0, 0.065, [(slice(0, 2), 1.0, 1500, (-0.35, 0.3))] + upper)
        if k < 4:
            phrase(dry, send, [m - 12 for m in notes], t0, LN, cello, 0.085, -0.2)
        else:
            phrase(dry, send, notes, t0, LN, violin, 0.065, 0.25)
        g = arp_on(t0)
        if k % 2 == 1 and g > 0.01:
            x = grand(mtof(ch[3] + 12), 0.2, 3.5) * g * 0.5
            place(dry, x * 0.25, t0 + 5.5, 0.35); place(send, x * 0.7, t0 + 5.5, 0.35)
    return soft(room(dry, send), 0.9)[:int(total * SR)]

def sonnet(total, arp_on):
    """8 s a line: hushed low strings and an organ; one wordless soprano sings the phrases. It rests through
    alternate sonnets while arp_on is low (the quiet edges of a video), and the violins carry them instead."""
    LN = 8.0
    n = int((total + 12) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    for k in range(int(total / LN) + 1):
        ch, *notes = SONNET[k % 14]
        t0 = k * LN
        L = bed(k, LN)
        strings(dry, send, ch, t0, (k, LN), 3.5, 0.08, [(slice(0, 2), 1.0, 1300, (-0.35, 0.3)),
                                                  (slice(2, 4), 0.7, 1800, (-0.5, 0.5))])
        for j, m in enumerate(ch[1:4]):
            x = organ(mtof(m), L) * 0.022
            place(dry, x * 0.4, t0, (-0.2, 0.0, 0.2)[j]); place(send, x, t0, (-0.2, 0.0, 0.2)[j])
        if (k // 14) % 2 == 0 or arp_on(t0) > 0.5:
            phrase(dry, send, notes, t0, LN, soprano, 0.045, 0.05, 1.0)
        else:
            phrase(dry, send, notes, t0, LN, violin, 0.04, 0.2)
    return soft(room(dry, send), 0.9)[:int(total * SR)]

def brass(total, arp_on):
    """11 s a line, the stillest: low strings crossfading slowly, the phrases low and soft on cellos, one solo-violin
    A held high across everything (it sits in every chord: root, fifth, third, seventh or ninth)."""
    LN = 11.0
    n = int((total + 14) * SR)
    dry = np.zeros((n, 2)); send = np.zeros((n, 2))
    for k in range(int(total / LN) + 1):
        ch, *notes = SONNET[k % 14]
        t0 = k * LN
        strings(dry, send, ch, t0, (k, LN), 5.0, 0.10, [(slice(0, 2), 1.0, 1200, (-0.3, 0.3)),
                                                              (slice(2, 4), 0.6, 1500, (-0.45, 0.45))])
        phrase(dry, send, [m - 12 for m in notes], t0 + 1.0, LN - 1.0, cello, 0.075 * (0.6 + 0.4 * arp_on(t0)), -0.15)
    L = int((total - LN + 8) * SR)
    if L > 0:
        e = env_adsr(L, 8.0, 1.0, 0.9, 7.0) * (1 + 0.12 * np.sin(2 * np.pi * np.arange(L) / SR / 23))   # a slow breath
        x = pan2(bow(81, L, 4500, 'violin') * e[:, None] * 0.016, 0.2)
        place(dry, x * 0.4, LN); place(send, x, LN)
    return soft(room(dry, send), 0.9)[:int(total * SR)]

STYLES = dict(boundless=boundless, sonnet=sonnet, brass=brass)
SEEDS = dict(boundless=106, sonnet=107, brass=108)

if __name__ == '__main__':
    name, path = sys.argv[1], sys.argv[2]
    total = float(sys.argv[3]) if len(sys.argv) > 3 else 14 * dict(brass=11.0).get(name, 8.0) + 4    # one sonnet
    S.rng = np.random.default_rng(SEEDS[name])
    arp_on = lambda t: float(np.clip((t - 15) / 10, 0, 1))      # a video's busy middle, from 15-25 s on
    x = hp(STYLES[name](total, arp_on), 40)
    x *= S.LEVEL / np.sqrt((x ** 2).mean())                     # the engine's loudness, so styles compare fairly
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())
    print('wrote', path, total, 's  peak', round(float(np.abs(x).max()), 3))
