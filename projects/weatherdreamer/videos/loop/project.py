"""The Forecaster With No Answer Key: WeatherDreamer (Duffy, Penn, Ballard, Posch & Vandal, arXiv:2611.18393v1) told as
the story of the forecast loop, predict then correct, learned from observations alone. Also hosts the topic's kit,
loopkit.py. An aigs pod extra, not journal club: see projects/weatherdreamer/AGENTS.md."""
from margin_notes import NOTES

HUD = 'weatherdreamer  ·  an explainer'
OUTPUT_NAME = 'the_forecaster_with_no_answer_key.mp4'

CHAPTERS = ['The problem', 'The old loop', 'The learned loop', 'Down here', 'Up there', 'The scoreboard', 'Questions']
STEPS = ['the problem', 'the idea', 'the evidence', 'the limits']
CHAPTER_STEPS = {0: (0,), 1: (0,), 2: (1,), 3: (2,), 4: (2,), 5: (3,), 6: (3,)}

SCENE_MODULES = ['scenes1', 'scenes2']

MUSIC = dict(style='daylight', duck_db=9, duck_ramp=1.2, duck_bridge=2.0,
             intro_until='Title', arp_from='Dreamer', arp_until='Scoreboard')

CHAPTER_TITLES = {
    'ColdOpen': 'Cold open: nobody can see right now', 'Title': 'WeatherDreamer',
    'Clues': 'The clues: stations, balloons, satellites', 'Analysis': 'Data assimilation and the analysis',
    'Kalman': 'Predict, then correct', 'Dreamer': 'The learned loop', 'NoKey': 'No answer key (Fig. 1)',
    'Lessons': 'Three lessons', 'Surface': 'Near the ground (Fig. 4)', 'Unseen': 'Rain and cloud tops it never sees',
    'Aloft': 'The turn: higher up (Table 2)', 'Walls': 'Cause one: the walls', 'Listening': 'Cause two: not listening (Fig. 8)',
    'Scoreboard': 'Reading the scoreboard', 'Speed': 'Fast, and not yet continuous',
    'Questions': 'Questions to think about', 'End': 'Takeaway',
}

DESCRIPTION = """The Forecaster With No Answer Key: a motion-graphics explainer of WeatherDreamer.

Every weather forecast starts from a picture of the atmosphere right now, built by data assimilation: a slow, expensive, hand-engineered loop of predicting and correcting that even the celebrated AI forecasters still rely on. This paper trains one model to learn that whole loop, end to end, from raw observations of 18 observing systems, with no reanalysis as an answer key. The video follows the loop from the classic Kalman-style cycle to the learned one (memory, background, analysis, decoders), how it is taught, where it already competes near the ground, why it falls short higher up, how to read its scoreboard fairly, and what it costs to run.

Paper: Kate Duffy, Elise Penn, Tristan Ballard, August Posch, Thomas J. Vandal (Zeus AI, Inc.), 2026. WeatherDreamer: Learning a World Model from Multimodal Earth Observations. arXiv:2611.18393v1
https://arxiv.org/abs/2611.18393

Chapters
{chapters}

Notes
• Figures marked "Fig. N" are crops of the paper's own figures. Bar charts are redrawn from numbers in the paper's text and Table 2. Anything marked "illustration" (the globe of clues, the loop diagrams, the patch map) is not data.
• "The American and European ensembles" are NOAA's GEFS and ECMWF's IFS ENS; "NOAA's own assimilation" is the GSI first guess (3D-Var reanalysis scout run, 30 cycles in 2024). Surface scores are at 534 held-out stations.
• Table 2 vs abstract: the abstract says temperature-sounding departures are up to five times GSI's; the largest per-channel ratio in the text and table is about 4.6, so the video says "about four and a half". Radiosonde winds are 2.6 times worse averaged over 1000-100 hPa (1.6 near the ground, 3.2-3.5 at 300-200 hPa).
• "Our arithmetic": a 50 m/s jet crosses a 1,600 km patch in about 9 hours. The paper names the patch size and the weak use of upper-air observations as the two causes.
• Fair-comparison caveats (most from the paper): operational ensembles are compared with their real delivery delay (5-7 h old); much of the probabilistic edge comes from ensemble spread; many held-out stations have assimilated neighbours; the baselines are not elevation-adjusted at stations (our reading of the supplement); rain is verified against a product built partly from instruments the model reads. All authors work at Zeus AI, which develops the model.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'daylight'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
