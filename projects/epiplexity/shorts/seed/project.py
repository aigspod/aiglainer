"""epiplexity short: seed (9:16). Build with: make P=epiplexity/shorts/seed
Scenes are native vertical ones in ../epishorts.py (built on epikit). An aigs pod extra, not journal club: see ../../AGENTS.md."""
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py

KIND = 'short'
SOURCES = ['epiplexity/videos/epiplexity']
SCENE_MODULES = ['epishorts']
HUD = 'epiplexity'
CITE = 'finzi, qiu, jiang et al. · arxiv 2601.03220'
OUTPUT_NAME = 'epiplexity_short_seed.mp4'
MUSIC = dict(style='night', duck_db=9, duck_ramp=1.2)
DESCRIPTION = """Seven bytes of seed, a million random-looking bits. How much information is that? Shannon, a compressor and a learner with limited compute give three different answers.

From "From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence" (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, 2026), arXiv:2601.03220v2. https://arxiv.org/abs/2601.03220
An unofficial explainer, not produced by the authors.
{voice}• Paper vs illustration: the million bits are real SHA-256 output (counter mode, 7-byte seed), computed for the video; a slice is drawn. "Our check" is our own run of xz on 1,048,576 bits of this generator and of coin flips (1.000 compressed bits per bit for both), not the paper's. The structure/noise bar is an illustration of the paper's Theorem 9 (a cryptographically secure generator looks random to any polynomial-time observer).

#information #entropy #machinelearning #cryptography #AI #shorts
"""
