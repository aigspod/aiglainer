"""Time for a missing sensor: a 9:16 short (sensor). Build with: make P=dynamics/shorts/sensor"""
KIND = 'short'
SOURCES = ['dynamics/videos/sign']
SCENE_MODULES = ['dynshorts']
HUD = 'the aigs pod  ·  dynamics'
CITE = 'duthé et al. · arxiv 2512.21113'
OUTPUT_NAME = 'dynamics_short_sensor.mp4'
MUSIC = dict(style='encore', duck_db=16)
DESCRIPTION = """Can time stand in for a missing sensor? Two coupled masses, one sensor: with three past steps a transformer loses both modes, with four it finds them again. ⏱️

From "A Mechanistic Analysis of Transformers for Dynamical Systems" (Duthé, Evangelou, Liu, Kevrekidis & Chatzi, 2025), arXiv:2512.21113, §3.2. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Bella"). Which settings work (both positions with 3 steps; first mass only with 3 steps fails, with 4 works) is from §3.2. The masses' motion is simulated from the paper's equations and slowed 12×. The "four numbers" count (two positions, two velocities; one number per sensor per step) is our own rough reasoning.

#machinelearning #transformers #physics #AI #science #shorts
"""
