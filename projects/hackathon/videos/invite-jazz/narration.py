"""Narration for the jazz edition of the hackathon invitation: the same story as the invite, said warmly to one
listener, with room to breathe and long music-only stretches (the title chorus, the five open questions, the cadence).

Each scene is a whole number of bars of the 96 bpm grid (`bars`, see beat.py), and `mus` says which section of
music.py's tune plays under it, bar by bar. `_snap()` below lays each scene's lines where they fall (never earlier
than written, never overlapping) and sets `hold` and `vend` so the scene lasts exactly its bars with an unwarped
clock: authored time is real time, so scene changes land on the music's phrase boundaries.
Beats are (earliest time, text). The last scene keeps several seconds after its line for the cadence and the fade.
After editing a line, run `make narration` twice: the first run synthesizes it, the second lays it out with its
real length (the build says so when it had to guess).

The date comes from the invite's event.py (SOURCES in project.py), so one edit there updates both videos.
"""
import hashlib, os, sys, wave

from beat import BAR
from event import WHEN, spoken

VOICE = 'bella-nicole'  # Bella blended 70/30 with Nicole (aiglainer/hosts.py): softer and closer
SPEED = 0.94            # a touch slower than the invite: unhurried
LANG = 'a'
SAY = {}

SCENES = [
    dict(scene='Hook', bars=8, mus=[(2, 'intro'), (5, 'two'), (1, 'turn')], beats=[
        (3.0, 'Machine-learned climate emulators can carry a whole planet forward in time.'),
        (11.0, 'But what is really going on, inside them?'),
    ]),
    dict(scene='Title', bars=6, mus=[(3, 'chorus'), (3, 'walk')], beats=[
        (7.0, "So here's an invitation."),
        (10.0, 'The aigs pod journal club is throwing a hackathon.'),
    ]),
    dict(scene='Models', bars=4, mus=[(4, 'walk')], beats=[
        (0.9, "Together, let's open up emulators of the ocean and the atmosphere."),
    ]),
    dict(scene='Tools', bars=4, mus=[(4, 'two')], beats=[
        (0.9, "We'll bring our own toolkit, and ideas from four journal club papers."),
    ]),
    dict(scene='Questions', bars=13, mus=[(3, 'lift'), (8, 'chorus'), (2, 'two')], beats=[
        (0.7, "And here's the best part. Nobody knows the answers yet."),
    ]),
    dict(scene='Tracks', bars=4, mus=[(4, 'two')], beats=[
        (0.9, 'There are six tracks, from the ocean, to the atmosphere, to the code.'),
    ]),
    dict(scene='Welcome', bars=4, mus=[(3, 'break'), (1, 'turn')], beats=[
        (0.7, 'New to interpretability? A climate scientist? A total beginner?'),
        (5.9, 'You are so welcome here.'),
    ]),
    dict(scene='End', bars=6, mus=[(4, 'coda'), (2, 'outro')], beats=[
        (1.0, f'So come and join us. {spoken(WHEN)}. Details soon.'),
    ]),
]

# ------------------------------------------------------------------ fit every scene to its bars
GAP, LEAD, MIN_HOLD = 0.3, 0.45, 0.5         # GAP and LEAD as in aiglainer/narrated.py
HERE = os.path.dirname(os.path.abspath(__file__))


def _clip_seconds(text):
    """Length of the synthesized clip for a line, from the cache (named as aiglainer/tts.py names it), or None."""
    from aiglainer import hosts, tts
    voice = hosts.get(VOICE)['voice'] if VOICE in hosts.HOSTS else VOICE
    key = hashlib.sha1(f'{voice}|{SPEED}|{tts.spoken(text, SAY)}'.encode()).hexdigest()[:16]
    path = os.path.join(HERE, 'cache', key + '.wav')
    if not os.path.exists(path):
        return None
    with wave.open(path) as w:
        return round(w.getnframes() / w.getframerate(), 3)      # as lines.json rounds it


def _snap(scenes):
    guessed = []
    for sd in scenes:
        assert sum(n for n, _ in sd['mus']) == sd['bars'], sd['scene']
        t_free, beats = LEAD, []
        for v, text in sd['beats']:
            d = _clip_seconds(text)
            if d is None:
                d = 0.9 + 0.4 * len(text.split())
                guessed.append(text)
            v = max(v, t_free)
            beats.append((round(v, 3), text))
            t_free = round(v, 3) + d + GAP
        length = sd['bars'] * BAR
        hold = length - (t_free - GAP)
        if hold < MIN_HOLD:
            print(f"narration.py: {sd['scene']} needs more than {sd['bars']} bars (short by {MIN_HOLD - hold:.2f}s)", file=sys.stderr)
        sd.update(beats=beats, hold=hold, vend=length, smax=1.0)
    if guessed:
        print(f'narration.py: guessed the length of {len(guessed)} new line(s); run `make narration` again to lay them out', file=sys.stderr)


_snap(SCENES)
