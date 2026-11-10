"""A Mechanistic Analysis of Transformers for Dynamical Systems: the whole paper in ~6 minutes, voiced by Michael,
scored in 'daylight'. Scenes are reused from the three part videos (see distilled.py)."""
SOURCES = ['dynamics/videos/sign', 'dynamics/videos/hidden', 'dynamics/videos/unfold']
HUD = 'the aigs pod  ·  /mull/  ·  dynamics'
OUTPUT_NAME = 'dynamics_in_six_minutes.mp4'
CHAPTERS = ['The sign problem', 'History as a sensor', 'Room and parameters', 'Our extrapolation', 'Questions']
SCENE_MODULES = ['distilled']
MUSIC = dict(style='daylight', duck_db=16, intro_until='Title')

# hidden's margin note (the part keeps its own in hidden/margin_notes.py; module names clash, so it is repeated here)
NOTES = {
    'Takens': [dict(t=14.5, text='no velocity sensor needed', x=1420, y=905, rot=-3)],
}

CHAPTER_TITLES = {'ColdOpen': 'Cold open: good forecasts, different insides', 'Title': 'Inside a forecasting transformer',
                  'Recipe': 'A spring is a two-step recipe (AR(2), §3.1)', 'OneHead': 'One head can only average (§2.3)',
                  'Springs': 'One spring rings, one goes flat (simulated)', 'TwoHeads': 'A second head brings the minus (App. A.1)',
                  'TwoMasses': 'Two masses: time stands in for a sensor (§3.2)', 'Hide': 'Van der Pol: hide the velocity (§4.1)',
                  'Takens': "Takens' theorem: the past stands in", 'Table1': 'History wins (Table 1)',
                  'Room': 'Chafee-Infante: two latent numbers collapse, three unfold (§4.2)',
                  'Loops': 'Cylinder flow: without Re the loops overlap (§4.3)', 'Recon': 'Rebuilding the whole field: ~70x worse without Re',
                  'Lesson': 'One-step accuracy is not latent identifiability', 'Emulators': 'Our extrapolation: climate emulators',
                  'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """A Mechanistic Analysis of Transformers for Dynamical Systems: the whole paper in about six minutes, for the aigs pod journal club.

What does a small transformer learn when it forecasts a dynamical system? A single attention-only head mixes past
samples with softmax weights that are positive and add up to one, so it can only average: it oversmooths a spring
that needs a plus and a minus, and a second head with an opposite-sign output weight fixes it. The paper stresses
this is a boundary case (§3.1, App. A.1); residual paths, feed-forward layers and more heads can supply the minus.
When a sensor is missing, a window of past samples stands in for it, as Takens' theorem says: on the Van der Pol
oscillator with velocity hidden, the best transformer's error is about 1,200 times lower than an MLP's (Table 1).
But history is not always enough: on the Chafee-Infante equation a latent of two numbers collapses the state's
surface while three unfold it, and on flow past a cylinder a model not told the Reynolds number rebuilds the full
v_x field about 70x worse (66.5x over the field, 53.6x in the wake). One-step accuracy is not latent identifiability.

Paper: Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi (2025). A Mechanistic Analysis
of Transformers for Dynamical Systems. arXiv preprint, v2. arXiv:2512.21113  https://arxiv.org/abs/2512.21113

Chapters
{chapters}

Notes
• Typed from the paper: m, c, k, the 25 Hz sampling and 7.12 / 3.56 Hz (§3.1); Case 1's coefficients (§3.1); the
  two-head output weights W_O = [1.087, −1.244] (App. A.1); which 2-DOF settings work (§3.2); the Van der Pol errors
  (Table 1, App. A.2.1: mean one-step test MSE over 10 seeds; NARX one deterministic fit); the cylinder Reynolds
  numbers and reconstruction errors (§4.3, App. A.5: 1.12e-4 vs 7.45e-3 whole field, 2.48e-4 vs 1.33e-2 wake).
• Our calculation: the soft spring's coefficients (+1.24, −0.98); the paper gives only their signs.
• Simulated from the paper's equations (our code, not the paper's trained models): the spring responses and spectra,
  our best one-head fit (one fixed weight, no positional encoding), the two-head construction, the two-mass motion,
  and the Van der Pol phase portraits, windows and delay-coordinate loop (µ = 0.5, Δt = 0.1).
• Illustrations, not data: the attention-weight sliders, the latent pictures for two and three numbers, the latent
  loops with and without Re, the error shapes across Re, and the cold open's vortex wakes.
• The paper's text and its table disagree on positional encoding: §4.1 says it reshapes attention "without
  systematically improving prediction accuracy", but Table 1 shows about 86× lower error with it in the 2-D model,
  and §5.2 calls it "a measurable improvement" for Van der Pol. We follow the table.
• Takens' bound n ≥ 2d + 1 is a sufficient condition; the paper takes d = 2 for Van der Pol, giving n = 5.
• App. A.5 says the fold-to-fold spread is "two orders of magnitude" smaller than the gap; from its own numbers it is
  about 13x smaller.
• The climate-emulator scene (ACE, SamudrACE) and the third question are our extrapolation, not claims of the paper.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'daylight'.
"""

def THUMBNAIL(c):
    from aiglainer.core import text
    from aiglainer.notes import lamp, swash, sticky
    lamp(c, 1500, 260, 2.4, 1, on=1)
    text(c, 'Good forecasts,', 120, 430, 140, 300, 'ink', kind='display')
    text(c, 'different', 120, 600, 150, 300, 'ink', kind='display')
    w = text(c, 'insides', 120, 790, 170, 400, 'y', kind='italic')
    swash(c, 120, 120 + w, 830, 'y', 1, 1, w=7)
    sticky(c, 1380, 640, ['the whole paper', 'in 6 minutes'], 1, rot=5.0, w=320, h=220)
