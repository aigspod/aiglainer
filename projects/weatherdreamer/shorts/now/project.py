"""weatherdreamer short: now (9:16). Build with: make P=weatherdreamer/shorts/now
Native vertical scenes in ../wdshorts.py (built on loopkit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: wdshorts.py

KIND = 'short'
SOURCES = ['weatherdreamer/videos/loop']
SCENE_MODULES = ['wdshorts']
HUD = 'weatherdreamer'
CITE = 'duffy, penn, ballard, posch & vandal · arxiv 2611.18393'
OUTPUT_NAME = 'weatherdreamer_short_now.mp4'
MUSIC = dict(style='daylight', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Every weather forecast starts from a picture of the atmosphere right now, and nobody can see right now. A new model learns to build that picture from the scattered clues alone, every hour.

From "WeatherDreamer: Learning a World Model from Multimodal Earth Observations" (Duffy, Penn, Ballard, Posch & Vandal, Zeus AI, 2026), arXiv:2611.18393v1. https://arxiv.org/abs/2611.18393
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the globe of stations, balloons and satellite stripes and the two clocks are illustrations. Numbers from the paper: about 11,000 surface stations, about 650 balloon soundings at each of 00 and 12 UTC (§2.1); global analyses usually every 6 h and hours late (§1); one global hourly update in about 1.5 minutes on one H100 GPU, half of it reading data (§5). Near the ground it beats NOAA's global ensemble out to 12 hours at held-out stations (§4.1).

#weather #forecasting #machinelearning #AI #shorts
"""
