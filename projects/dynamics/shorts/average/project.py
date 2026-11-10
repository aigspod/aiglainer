"""Attention can only average: a 9:16 short (average). Build with: make P=dynamics/shorts/average"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign']
SCENE_MODULES = ['dynshorts']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_average.mp4'
MUSIC = dict(style='dawn', duck_db=16)
DESCRIPTION = """Why can't one attention head predict a soft spring? Its weights are positive and add up to one, so it can only average, and the spring needs a minus sign. 🌀

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113. The paper calls this a boundary case: one head, attention only, no residual path; more heads can supply the minus. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Bella"). The stiff spring's coefficients (−0.4352, −0.9802) are from §3.1; the soft spring's (+1.24, −0.98) are our calculation (the paper gives only their signs). The sliding weights are an illustration.

#machinelearning #transformers #physics #AI #science #shorts
"""
