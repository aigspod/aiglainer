"""epiplexity short: pixels (9:16). Build with: make P=epiplexity/shorts/pixels
Scenes are native vertical ones in ../epishorts.py (built on epikit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py

KIND = 'short'
SOURCES = ['epiplexity/videos/epiplexity']
SCENE_MODULES = ['epishorts']
HUD = 'epiplexity'
CITE = 'finzi, qiu, jiang et al. · arxiv 2601.03220'
OUTPUT_NAME = 'epiplexity_short_pixels.mp4'
MUSIC = dict(style='dawn', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Tiny images hold three times the raw bits of web text, yet a model can learn far more structure from the text. Over 99% of the image bits are random detail.

From "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence" (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, 2026), arXiv:2601.03220v2. https://arxiv.org/abs/2601.03220
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: all bars are the paper's Fig. 8a (requential estimates at 6 × 10^18 FLOPs, models up to 160M parameters; OpenWebText, Lichess chess in both orders, CIFAR-5M), redrawn from data extracted from the figure. Totals are the stacked bar tops (epiplexity + time-bounded entropy). The caption says 1B tokens; §6.2 says 5B, and the bars only make sense at 5B, so we follow the text. The striped/noise bar is the video's way of drawing structure vs randomness.

#data #machinelearning #information #LLM #AI #shorts
"""
