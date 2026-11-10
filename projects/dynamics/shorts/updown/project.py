"""Transformers for dynamical systems, a 9:16 short (updown). Build with: make P=dynamics/shorts/updown"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign']
SCENE_MODULES = ['dynshorts2']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_updown.mp4'
MUSIC = dict(style='night', duck_db=16)
DESCRIPTION = """Same position, two directions: from one snapshot of its height you can't tell whether an oscillator is rising or falling. Five past samples can. ↕️

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113. Full explainers and a podcast: the aigs pod. An unofficial explainer, not produced by the authors.
Synthetic narration (Kokoro, "Michael"). The moving dot and the two five-sample windows are our own simulation of the paper's Van der Pol equations (µ = 0.5, Δt = 0.1), not its trained models. Column heights are typed from Table 1 (velocity hidden, one-step test MSE, mean of 10 seeds): MLP on x(t) alone 2.485e-2; single-head transformer on the last five samples, 2-D latent with positional encoding, 2.065e-5 (about 1200× lower).

#dynamicalsystems #transformers #machinelearning #AI #science #shorts
"""
