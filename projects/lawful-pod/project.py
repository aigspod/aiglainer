"""LAWFUL, the full audio episode for journal club. Script in episode.py; build with: make P=lawful-pod"""
KIND = 'podcast'
TITLE = 'LAWFUL: When a network follows the law, has it learned the physics?'
OUTPUT_NAME = 'LAWFUL_pod.mp3'
SUMMARY = 'LAWFUL (Chen, Parker & Arora, ICML 2026 MI workshop), explained for the aigs pod journal club.'
BED = 0                     # faint music under the talk, 0..1 (0: talk on silence, the podcast norm)

DESCRIPTION = """LAWFUL: When a network follows the law, has it learned the physics? An audio episode for the aigs pod journal club.

A small transformer predicts radar from motion capture, and it responds to physically controlled changes the way the
Doppler law says it should. What does that show, and what doesn't it? We walk through the paper's counterfactual test,
what its 0.988 consistency score does and doesn't constrain, the circuit found by activation patching (and its weak
necessity control), the probes, and the attention-pattern hypothesis, then ask what evidence would justify saying a
model has learned the physics.

Paper: Kevin Chen, Kenneth W. Parker, Anish Arora (2026). LAWFUL: Law-Aligned Witness for Faithful Use of Latents.
Mechanistic Interpretability Workshop, ICML 2026. arXiv:2607.28672 · Code: https://github.com/aciculachen/LAWFUL

Chapters
{chapters}

Questions to discuss
1. Can a model satisfy a scaling law while getting the absolute physical quantities wrong? What would you test next?
2. Which input counterfactuals remain physically meaningful, and how should we validate their construction?
3. Does the necessity result survive controls for off-manifold activation mixing? What would strengthen it?
4. What experiment would distinguish fixed-lag comparison from genuinely adaptive differentiation?
5. What would a similarly rigorous analysis require for coupled, multivariable systems such as climate emulators?

Notes
• The "doubled frequency" network is a hypothetical counterexample to the consistency metric (Eq. 9–10), not a
  claim about the paper's trained model.
• The alpha range (±1.16) is an empirical sweep within the radar-resolvable range, not a certificate over the continuum.
• The paper's text says "six of the seven temporal heads" in the circuit favour the attention pattern; Table 2 lists
  six temporal heads, five of which do (T.h4 is the exception).
• The climate-emulator passage is our extrapolation, not a result of the paper.
{voice}• An unofficial summary, not produced by the authors.
"""
