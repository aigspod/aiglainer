"""The musical grid of the jazz edition: 96 bpm, swung, so a beat is 0.625 s and a bar is 2.5 s.
narration.py snaps every scene to whole bars and music.py writes the track on the same grid, so scene changes
fall on phrase boundaries and the title, the lift and the final cadence land where the music turns."""
import math

BPM = 96
BEAT = 60 / BPM          # 0.625 s
BAR = 4 * BEAT           # 2.5 s
SWING = 0.62             # where the off-beat eighth falls within a beat (0.5 straight, 0.667 a hard triplet swing)


def b(bar, beat=0.0):
    """Authored time of a bar (and beat within it), from the start of the scene."""
    return bar * BAR + beat * BEAT


def breathe(t, t0=0.0, period=BAR):
    """0..1, a slow sine that rises and falls once a bar: for things that sway with the music rather than pump."""
    return 0.5 - 0.5 * math.cos(2 * math.pi * (t - t0) / period)
