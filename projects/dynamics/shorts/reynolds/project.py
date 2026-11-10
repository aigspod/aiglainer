"""Transformers for dynamical systems, a 9:16 short (reynolds). Build with: make P=dynamics/shorts/reynolds"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign', 'dynamics/videos/unfold']
SCENE_MODULES = ['dynshorts2']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_reynolds.mp4'
MUSIC = dict(style='daylight', duck_db=16)
DESCRIPTION = """Two transformers forecast a flow equally well. One was never told the Reynolds number, and inside, it mixes regimes together. 🌀

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113. Full explainers and a podcast: the aigs pod. An unofficial explainer, not produced by the authors.
Synthetic narration (Kokoro, "Michael"). Typed from §4.3 and App. A.5: rebuilding the full v_x field from the one-sensor latent (geometric harmonics, 5-fold cross-validation) gives a mean absolute error of 1.12e-4 with Re and 7.45e-3 without (66.5×; in the wake 2.48e-4 vs 1.33e-2, 53.6×); the largest one-step error across both models is about 2.3e-2. The wake and the latent loops are illustrations of what §4.3 describes, not the paper's data.
Our extrapolation, not the paper's claim: in climate emulators such as ACE and SamudrACE, forcing (CO₂, sea surface temperatures) plays the Reynolds number's role.

#dynamicalsystems #transformers #machinelearning #AI #science #shorts
"""
