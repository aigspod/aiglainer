"""The musical grid the whole piece is cut to: 120 bpm, so a beat is half a second and a bar is two.
Scenes author their hits on this grid; narration.py snaps every scene to a whole number of bars, and music.py
writes the track on the same grid, so cuts, title hits and drops land on beats."""
import math

BPM = 120
BEAT = 60 / BPM          # 0.5 s
BAR = 4 * BEAT           # 2.0 s


def b(bar, beat=0.0):
    """Authored time of a bar (and beat within it), from the start of the scene."""
    return bar * BAR + beat * BEAT


def kick(t, t0=0.0, t1=1e9, decay=9.0):
    """1 on every beat between t0 and t1, decaying: a visual pump that follows the kick drum."""
    if t < t0 or t >= t1:
        return 0.0
    return math.exp(-decay * ((t - t0) % BEAT))
