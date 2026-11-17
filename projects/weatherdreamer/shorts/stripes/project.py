"""weatherdreamer short: stripes (9:16). Build with: make P=weatherdreamer/shorts/stripes
Native vertical scenes in ../wdshorts.py (built on loopkit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: wdshorts.py

KIND = 'short'
SOURCES = ['weatherdreamer/videos/loop']
SCENE_MODULES = ['wdshorts']
HUD = 'weatherdreamer'
CITE = 'duffy, penn, ballard, posch & vandal · arxiv 2611.18393'
OUTPUT_NAME = 'weatherdreamer_short_stripes.mp4'
MUSIC = dict(style='mysterium', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Open up a weather model's memory and some channels show weather. Others show the round footprints and diagonal stripes of the satellites that were watching. Why would it remember that?

From "WeatherDreamer: Learning a World Model from Multimodal Earth Observations" (Duffy, Penn, Ballard, Posch & Vandal, Zeus AI, 2026), arXiv:2611.18393v1. https://arxiv.org/abs/2611.18393
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the maps are crops of the paper's Fig. S3 (channels of the 512-number memory h and the 64-number latent state z at 00 UTC on 20 August 2024). The comparison with a classical filter's error estimates is the paper's own (Fig. S3 caption). The paper removes all surface stations in one test, but does not check whether z stays the same when the satellite network changes; that question is ours.

#weather #forecasting #machinelearning #AI #shorts
"""
