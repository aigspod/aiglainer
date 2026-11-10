"""Transformers for dynamical systems, a 9:16 short (unfold). Build with: make P=dynamics/shorts/unfold"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign', 'dynamics/videos/unfold']
SCENE_MODULES = ['dynshorts2']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_unfold.mp4'
MUSIC = dict(style='silencia', duck_db=16)
DESCRIPTION = """A model can have all the information it needs, and still not have room to use it. 🧩

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113. Full explainers and a podcast: the aigs pod. An unofficial explainer, not produced by the authors.
Synthetic narration (Kokoro, "Bella"). The two mirror halves and the folded one-sensor view are our own three-mode simulation of the paper's Chafee-Infante equation (§4.2: ν = 0.16, sensor at the 10th of 256 grid points), drawn in two readings for display; the paper's models get five. The latent pictures are illustrations of §4.2 (Fig. 8-9): with a latent of two numbers the surface collapses to a thick curve and training is unstable across seeds; with three it unfolds.

#dynamicalsystems #transformers #machinelearning #AI #science #shorts
"""
