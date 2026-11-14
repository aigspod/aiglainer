"""epiplexity short: rules (9:16). Build with: make P=epiplexity/shorts/rules
Scenes are native vertical ones in ../epishorts.py (built on epikit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py

KIND = 'short'
SOURCES = ['epiplexity/videos/epiplexity']
SCENE_MODULES = ['epishorts']
HUD = 'epiplexity'
CITE = 'finzi, qiu, jiang et al. · arxiv 2601.03220'
OUTPUT_NAME = 'epiplexity_short_rules.mp4'
MUSIC = dict(style='analog', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Three one-line rules, three fates: one repeats, one looks like static, one keeps teaching a model more as it gets more compute.

From "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence" (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, 2026), arXiv:2601.03220v2. https://arxiv.org/abs/2601.03220
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the cellular-automaton pictures are computed exactly from rules 15, 30 and 54 (random first rows). The curve is the paper's Fig. 3 (epiplexity along the best two-part code vs training compute, predicting 64 cells 48 steps ahead), redrawn from data extracted from the figure; the split bars use Fig. 3's values at the largest compute budget, as shares, with each rule's total printed.

#cellularautomata #complexity #machinelearning #information #AI #shorts
"""
