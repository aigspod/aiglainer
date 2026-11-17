"""What Did It Learn to Trust?: a detective-story explainer of WeatherDreamer (Duffy, Penn, Ballard, Posch & Vandal,
arXiv:2611.18393v1): what the learned assimilation cycle trusts, what it ignores, what it learned about geometry, how
to read its scoreboard, and why its memory holds the satellites' footprints. An aigs pod extra, not journal club: see
projects/weatherdreamer/AGENTS.md. Kit: trustkit.py (independent of videos/loop). Paper figures are read from
projects/weatherdreamer/data/figs (run projects/weatherdreamer/extract_paper.py first; not in git)."""
from margin_notes import NOTES

HUD = 'weatherdreamer  ·  an explainer'
OUTPUT_NAME = 'weatherdreamer_what_did_it_learn_to_trust.mp4'

CHAPTERS = ['The case', 'Clue one: trust', 'Clue two: geometry', 'Clue three: the unseen', 'The scoreboard',
            'The reveal', 'To think about']
STEPS = ['the mystery', 'the clues', 'the scoreboard', 'the reveal']
CHAPTER_STEPS = {0: (0,), 1: (1,), 2: (1,), 3: (1,), 4: (2,), 5: (3,), 6: (3,)}

SCENE_MODULES = ['scenes1', 'scenes2']

MUSIC = dict(style='mysterium', duck_db=9, duck_ramp=1.2, duck_bridge=2.0,
             intro_until='Title', arp_from='Limb', arp_until='Reveal')

CHAPTER_TITLES = {
    'ColdOpen': 'Cold open: a memory full of satellite stripes', 'Title': 'What Did It Learn to Trust?',
    'CaseFile': 'The case file: predict, then correct', 'Gain': 'The gain: a question of trust',
    'Diagnostics': 'Clue one: reading trust out of a black box (Fig. 8)', 'Reversal': 'Not quite optimal: timid, trusting, deaf aloft',
    'Departures': 'Strong low, weak high (Table 2)', 'Suspects': 'Two suspects: upper-air data and 1,600 km patches',
    'Limb': 'Clue two: the view from an angle', 'LimbResult': 'It learned the geometry (Figs. 9b, S7)',
    'Stripes': 'The stripes vanish (Fig. S7)', 'Unseen': 'Clue three: cloud tops and rain it never sees (Fig. 6)',
    'Twist': 'The twist: learned retrieval, not clairvoyance', 'Clocks': 'The scoreboard: check the clocks (Fig. 4)',
    'FinePrint': 'The fine print', 'Reveal': 'The reveal: why it remembers the satellites (Fig. S3)',
    'RealTest': 'The real test', 'Questions': 'Questions to think about', 'End': 'The verdict',
}

DESCRIPTION = """What Did It Learn to Trust? A detective story inside WeatherDreamer.

Inside the memory of a new weather model are round footprints and diagonal stripes: the places its satellites were looking. WeatherDreamer learns the whole data assimilation cycle (predict the atmosphere an hour ahead, then correct it with new observations) directly from 18 observing systems, with no reanalysis and no prescribed instrument errors. This explainer works out, clue by clue, what it learned to trust: the instrument noise it discovered on its own, where its weighting is too timid, too trusting or nearly absent, how it learned satellite viewing geometry, what it can read out about clouds and rain it never sees while forecasting, how to read its scoreboard with care, and why remembering the satellites is part of how a filter knows how sure to be.

Paper: Kate Duffy, Elise Penn, Tristan Ballard, August Posch, Thomas J. Vandal (Zeus AI, Inc.). WeatherDreamer: Learning a World Model from Multimodal Earth Observations. arXiv:2611.18393v1 (13 Nov 2026). https://arxiv.org/abs/2611.18393

Chapters
{chapters}

Notes
• Figures marked "Fig. N" are crops of the paper's own figures (Figs. 4a, 8, S3, S7). Bar charts and tables are redrawn from numbers in the text and tables (§4.1-4.4, Table 2, Fig. 9b and Fig. S7 values quoted in §4.4); the crossover lines are drawn from the fitted slopes. Anything marked "illustration" (the predict-correct loop, the thermometer, the slanted views, the patch grid, the network-swap test) is not data.
• Upper air: radiosonde winds are 2.62 times NOAA's background averaged over 1000-100 hPa (1.6-1.7 low down, 3.2-3.5 at 300-200 hPa); the largest temperature-channel ratio is about 4.6 (the abstract rounds to "up to five"). NOAA's system uses far more instruments and decades of tuning; WeatherDreamer is scored as its ensemble mean.
• "Our arithmetic": a 50 m/s jet-level wind crosses a 1,600 km patch in about nine hours. "Our reading": the operational ensembles were matched to stations without an elevation adjustment (Text S6.4), which favours the model at mountain stations. The paper's own causes for the upper-air gap are the weak use of upper-air observations and the patch size (§5).
• Rain is verified against IMERG, which is built partly from instruments the model reads; cloud tops are learned mainly from geostationary infrared, as is the operational ACHA product. NSRDB irradiance being derived from GOES imagery is background, not from the paper. EarthCARE (radar and lidar, never seen in training) and the USCRN/SOLRAD ground stations are independent.
• The paper runs one data-denial experiment (all surface stations withheld). Whether the latent state stays the same when the observing network changes is not tested; that test and the closing questions are ours.
• All five authors are employees of Zeus AI, which develops WeatherDreamer (the paper's conflict-of-interest statement).
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'mysterium'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
