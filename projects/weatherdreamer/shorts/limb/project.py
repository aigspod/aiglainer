"""weatherdreamer short: limb (9:16). Build with: make P=weatherdreamer/shorts/limb
Native vertical scenes in ../wdshorts.py (built on loopkit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: wdshorts.py

KIND = 'short'
SOURCES = ['weatherdreamer/videos/loop']
SCENE_MODULES = ['wdshorts']
HUD = 'weatherdreamer'
CITE = 'duffy, penn, ballard, posch & vandal · arxiv 2611.18393'
OUTPUT_NAME = 'weatherdreamer_short_limb.mp4'
MUSIC = dict(style='analog', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Satellite images go cold toward their edges, with seams where one satellite hands off to the next. A weather model learned to remove that, from instruments that disagree.

From "WeatherDreamer: Learning a World Model from Multimodal Earth Observations" (Duffy, Penn, Ballard, Posch & Vandal, Zeus AI, 2026), arXiv:2611.18393v1. https://arxiv.org/abs/2611.18393
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the slant-path sketch and the warm-and-cold disk are illustrations. The two maps are crops of the paper's Fig. S7 (ATMS channel 7: observed, and the analysis decoded straight down). Numbers from §4.4: decoding at nadir recovers 83-96% of the observed limb darkening; near 80 degrees the correction is about 6 K in the 11.2 µm window, 14 K at 6.9 µm (water vapour), 16 K at 13.3 µm (CO2) and 22 K at 9.6 µm (ozone). The correction is radiometric only; parallax of high clouds remains.

#weather #forecasting #machinelearning #AI #shorts
"""
