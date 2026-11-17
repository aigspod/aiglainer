"""weatherdreamer short: trust (9:16). Build with: make P=weatherdreamer/shorts/trust
Native vertical scenes in ../wdshorts.py (built on loopkit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: wdshorts.py

KIND = 'short'
SOURCES = ['weatherdreamer/videos/loop']
SCENE_MODULES = ['wdshorts']
HUD = 'weatherdreamer'
CITE = 'duffy, penn, ballard, posch & vandal · arxiv 2611.18393'
OUTPUT_NAME = 'weatherdreamer_short_trust.mp4'
MUSIC = dict(style='silencia', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """A forecast says 20 degrees, a thermometer says 22. How far should you move? Weather systems usually set that trust by hand. This model learned it from the data.

From "WeatherDreamer: Learning a World Model from Multimodal Earth Observations" (Duffy, Penn, Ballard, Posch & Vandal, Zeus AI, 2026), arXiv:2611.18393v1. https://arxiv.org/abs/2611.18393
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the number line (20 vs 22 degrees, errors 1 and 0.5, a gain of 0.8) is an illustration of the textbook one-variable gain. Numbers from the paper (§4.3.3, Fig. 8): the error the update assumes for clear-sky microwave temperature channels is 0.2-0.4 K, at the instruments' on-orbit noise; its gain there is about 0.64 where about 0.82 would be optimal; for satellite ocean winds about 0.9 vs 0.8; for weather balloons at 100-300 hPa only 0.10-0.26.

#weather #forecasting #machinelearning #AI #shorts
"""
