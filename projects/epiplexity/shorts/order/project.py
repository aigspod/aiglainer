"""epiplexity short: order (9:16). Build with: make P=epiplexity/shorts/order
Scenes are native vertical ones in ../epishorts.py (built on epikit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py

KIND = 'short'
SOURCES = ['epiplexity/videos/epiplexity']
SCENE_MODULES = ['epishorts']
HUD = 'epiplexity'
CITE = 'finzi, qiu, jiang et al. · arxiv 2601.03220'
OUTPUT_NAME = 'epiplexity_short_order.mp4'
MUSIC = dict(style='daylight', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Chess games written as moves-then-board or board-then-moves hold the same information for Shannon. For a model with limited compute, the reverse order holds more learnable structure, and it transfers better.

From "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence" (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, 2026), arXiv:2601.03220v2. https://arxiv.org/abs/2601.03220
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the chessboard is an illustration. The curves are the paper's Fig. 4c (epiplexity vs compute for Lichess games, forward vs reverse) and the bars are Fig. 7 (after fine-tuning: puzzle accuracy 25.8% vs 25.9%, centipawn evaluation accuracy 21.0% vs 28.2%), redrawn from data extracted from the figures; bars start at zero. The paper stresses that epiplexity measures how much structure there is, not whether it helps a given task.

#chess #machinelearning #information #data #AI #shorts
"""
