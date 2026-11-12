"""The aigs hackathon, jazz edition: the same invitation as hackathon/videos/invite, calmer and closer. A late-night
record-sleeve look (soft Fraunces on cream paper and deep navy, mustard, terracotta and sage) and an original small-combo
jazz tune generated in code (music.py). The date is WHEN in the invite's event.py, shared through SOURCES, so one edit
updates both videos. Build with: make P=hackathon/videos/invite-jazz NPROC=6"""
import os, sys

# The engine runs this file before it adds SOURCES to the path, and narration.py and music.py need the invite's
# event.py as soon as they load: add it here (the engine then finds it already there).
_INVITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'invite'))
if _INVITE not in sys.path:
    sys.path.append(_INVITE)

import music
from event import EVENT, WHEN, MORE

SOURCES = ['hackathon/videos/invite']
HUD = ''                              # no HUD, no progress bar: every scene has chapter = None
OUTPUT_NAME = 'aigs-hackathon_invite-jazz.mp4'
CHAPTERS = []
SCENE_MODULES = ['scenes']
SOUND_EFFECTS = False                 # the band is the only sound under the voice

# An original tune written for this piece (music.py), rendered to cache/ on first use and exactly the timeline's length.
# Under the narrator it eases down about 7.5 dB on slow ramps and stays down through short pauses, so it never steps.
MUSIC = dict(style=music.ensure(), duck_db=7.5, duck_ramp=1.4, duck_bridge=2.0, level=1.15)

CHAPTER_TITLES = {'Hook': 'The aigs hackathon', 'Models': 'The models', 'Tools': 'The tools', 'Questions': 'Open questions',
                  'Tracks': 'Six tracks', 'Welcome': 'Everyone welcome', 'End': WHEN}
DESCRIPTION = f"""{EVENT[0].upper() + EVENT[1:]}, the jazz edition: {WHEN}. {MORE[0].upper() + MORE[1:]}.

A hackathon from the aigs pod journal club's community: we open up machine-learned climate emulators, SamudrACE (a coupled ocean-atmosphere emulator from Ai2 and E3SM) and ACE, with exege, our toolkit for latent diagnostics, and ideas from four journal club papers: circuits in vision transformers (Seeing Through Circuits), checking models against physical laws (LAWFUL), whether circuits explain model errors, and transformers as dynamical systems.

Six tracks: ocean shortcut, ocean routing, atmosphere CO₂, errors and strata, dynamics, and exege integration. Beginners, and climate scientists new to interpretability, are very welcome.

The same invitation as our first video, slower and warmer.

Notes
• The five questions in the video are open questions, not results: nobody knows the answers yet.
• Everything that looks like data (oceans, flows, globes, networks, lines) is procedurally drawn art, not model output.
• Music: an original jazz tune (brushes, upright-style bass, electric piano, vibraphone), composed and generated in code for this video.
{{voice}}"""

THEME = dict(ground='#1b2540', night='#1b2540', teal='#1d4b50', paper='#f4ead7', cream='#f4ead7', ink='#2b2420',
             mustard='#e2a93b', terra='#c8643f', sage='#9fb59a', rose='#e9b8a0', muted='#7a6e60', faint='#d8ccb6',
             line='#d8ccb6', panel='#fbf4e6', panel2='#ece0c8', pencil='#3a322c', y='#e2a93b', g='#1d4b50',
             c='#c8643f', f='#9fb59a', fade='#121a2e', shadow='#0b1020')
BACKGROUND = dict(glow=0, vignette=0, grain=1.5, frame=False)


def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
