"""epiplexity short: mystery (9:16). Build with: make P=epiplexity/shorts/mystery
Scenes are native vertical ones in ../epishorts.py (built on epikit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py

KIND = 'short'
SOURCES = ['epiplexity/videos/epiplexity']
SCENE_MODULES = ['epishorts']
HUD = 'epiplexity'
CITE = 'finzi, qiu, jiang et al. · arxiv 2601.03220'
OUTPUT_NAME = 'epiplexity_short_mystery.mp4'
MUSIC = dict(style='silencia', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """In a murder mystery the author can pick the culprit first; the reader has to deduce it. A model predicting the text has the reader's job, so it can learn more than the process that made its data.

From "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence" (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, 2026), arXiv:2601.03220v2. https://arxiv.org/abs/2601.03220
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the culprit, name and clues are an illustration of Ilya Sutskever's murder-mystery remark, which the paper quotes. The bit rows are computed exactly (32 random bits, 4 steps of rule 30, the first bits hidden, after the paper's Fig. 5a). "Each hidden bit doubles the possibilities" is the paper's reading (2^h candidate fills; the compute it needs grows exponentially with h). The columns are the paper's Fig. 5b measured epiplexity for 0-5 hidden bits, redrawn from data extracted from the figure.

#induction #machinelearning #information #LLM #AI #shorts
"""
