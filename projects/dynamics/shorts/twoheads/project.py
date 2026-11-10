"""Two heads, one subtraction: a 9:16 short (twoheads). Build with: make P=dynamics/shorts/twoheads"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign']
SCENE_MODULES = ['dynshorts']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_twoheads.mp4'
MUSIC = dict(style='analog', duck_db=16)
DESCRIPTION = """One attention head can't model a soft spring. Two heads can: the paper's trained model gives them output weights of 1.087 and −1.244, so one head's average is subtracted from the other's. ➖

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113, App. A.1. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Michael"). The output weights are typed from App. A.1; the sliding head weights are an illustration. The spectra are simulated from the paper's equations: the one-head curve is our best fixed-weight fit, and the two-head curve is our own simple version (one head on the newest sample, one on the older), not the paper's trained model.

#machinelearning #transformers #physics #AI #science #shorts
"""
