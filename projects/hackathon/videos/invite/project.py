"""The aigs hackathon: a 98-second invitation, cut like an ad to an original beat-driven track, in a poster look
(heavy capitals on paper and on cobalt, orange, lime and black slabs) instead of the house /mull/ style.
The event's date is WHEN in event.py. Build with: make P=hackathon/videos/invite NPROC=6"""
import music
from event import EVENT, WHEN, MORE

HUD = ''                              # no HUD, no progress bar: every scene has chapter = None
OUTPUT_NAME = 'aigs-hackathon_invite.mp4'
CHAPTERS = []
SCENE_MODULES = ['scenes']

# An original track written for this piece (music.py), rendered to cache/ on first use and exactly the timeline's
# length. Under the narrator it drops a gentle 8 dB with smooth ramps; between lines it rides up, as an ad should.
MUSIC = dict(style=music.ensure(), duck_db=8, duck_ramp=1.2, duck_bridge=2.0, level=1.3)

CHAPTER_TITLES = {'Hook': 'The aigs hackathon', 'Models': 'The models', 'Tools': 'The tools', 'Questions': 'Open questions',
                  'Tracks': 'Six tracks', 'Welcome': 'Everyone welcome', 'End': WHEN}
DESCRIPTION = f"""{EVENT[0].upper() + EVENT[1:]}: {WHEN}. {MORE[0].upper() + MORE[1:]}.

A hackathon from the aigs pod journal club's community: we open up machine-learned climate emulators, SamudrACE (a coupled ocean-atmosphere emulator from Ai2 and E3SM) and ACE, with exege, our toolkit for latent diagnostics, and ideas from four journal club papers: circuits in vision transformers (Seeing Through Circuits), checking models against physical laws (LAWFUL), whether circuits explain model errors, and transformers as dynamical systems.

Six tracks: ocean shortcut, ocean routing, atmosphere CO₂, errors and strata, dynamics, and exege integration. Beginners, and climate scientists new to interpretability, are very welcome.

Notes
• The questions in the video are open questions, not results.
• Everything that looks like data (globes, flows, waves, networks, lines) is procedurally drawn art, not model output.
• Music: an original track generated in code for this video.
{{voice}}"""

THEME = dict(ground='#f2efe7', paper='#f2efe7', ink='#111114', night='#111114', cobalt='#1f3bff', orange='#ff4f1c',
             lime='#cffa45', muted='#5f5c56', faint='#cfcac0', line='#d9d4ca', panel='#ffffff', panel2='#e8e3d8',
             pencil='#333333', y='#ff4f1c', g='#1f3bff', c='#ff4f1c', f='#cffa45', fade='#08080a', shadow='#000000')
BACKGROUND = dict(glow=0, vignette=0, grain=0.7, frame=False)
FONTS = dict(display='Inter.ttf', italic='Inter.ttf')


def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
