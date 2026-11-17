"""weatherdreamer short: walls (9:16). Build with: make P=weatherdreamer/shorts/walls
Native vertical scenes in ../wdshorts.py (built on loopkit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: wdshorts.py

KIND = 'short'
SOURCES = ['weatherdreamer/videos/loop']
SCENE_MODULES = ['wdshorts']
HUD = 'weatherdreamer'
CITE = 'duffy, penn, ballard, posch & vandal · arxiv 2611.18393'
OUTPUT_NAME = 'weatherdreamer_short_walls.mp4'
MUSIC = dict(style='dawn', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """A weather model learned only from observations is within about ten percent of NOAA's own system at surface stations. Higher up, it falls well behind. Why?

From "WeatherDreamer: Learning a World Model from Multimodal Earth Observations" (Duffy, Penn, Ballard, Posch & Vandal, Zeus AI, 2026), arXiv:2611.18393v1. https://arxiv.org/abs/2611.18393
An unofficial explainer, not produced by the authors.
{voice}• Numbers from Table 2 (standard deviation of observation-minus-forecast, WeatherDreamer over NOAA's GSI first guess, 3-9 hours ahead, 30 cycles in 2024): surface stations 1.02-1.08 (temperature 1.04 shown), satellite ocean winds 1.65, balloon temperature 1.79, balloon wind 2.62 averaged over all levels (3.2-3.5 near the jet stream). The paper's two causes (§5): the dynamics run on patches of about 1,600 km, which limits the large, slowly evolving circulation; and the update draws little from upper-air observations (balloon gains 0.10-0.26 at 100-300 hPa, §4.3.3). The jet crossing a patch in about 9 hours at 50 m/s is our own arithmetic. The patch map is an illustration.

#weather #forecasting #machinelearning #AI #shorts
"""
