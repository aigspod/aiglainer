"""Rebuilding a hidden state: attention as a delay embedding (§2.3, §4.1, Table 1, Fig. 6 of arXiv:2512.21113v2;
journal club Nov 11). Shared drawing code and simulated data come from dynamics/videos/sign (dynkit.py, data/vdp.json)."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  dynamics'
OUTPUT_NAME = 'dynamics_rebuilding_a_hidden_state.mp4'
SOURCES = ['dynamics/videos/sign']
CHAPTERS = ['The oscillator', 'Hide the velocity', 'Results', 'Inside the model', 'Questions']
SCENE_MODULES = ['scenes']
MUSIC = dict(style='analog', duck_db=16, intro_until='Title')

CHAPTER_TITLES = {'ColdOpen': 'Cold open: up or down?', 'Title': 'Rebuilding a hidden state',
                  'VdP': 'The Van der Pol oscillator', 'FullState': 'Full state: MLP and transformer tie (Table 1)',
                  'Hide': 'Hide the velocity: same x, two phases', 'Takens': "Takens' theorem: the past stands in",
                  'Table1': 'History wins (Table 1, partial observation)', 'Latent': 'Inside: two corrections for one x (Fig. 6b-d)',
                  'Attention': 'Attention weights, and a text-table disagreement (Fig. 6e-g)', 'Discussion': 'Questions to bring',
                  'End': 'Takeaway'}

DESCRIPTION = """Rebuilding a hidden state: how attention acts as a delay embedding. A motion-graphics explainer for the aigs pod journal club.

A Van der Pol oscillator has a position and a velocity. Give a model both, and a plain MLP predicts the next step as
well as a transformer (test error about 10^-7). Hide the velocity, and the MLP can't tell whether the oscillator is
rising or falling. A single-head transformer reading the last five samples recovers it: with positional encoding and
a two-dimensional latent, its error is about 1,200 times lower than the MLP's and about 100 times lower than a
polynomial NARX baseline (Table 1). Takens' theorem explains why the history is enough.

Paper: Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi (2025). A Mechanistic Analysis
of Transformers for Dynamical Systems. arXiv preprint, v2. arXiv:2512.21113  https://arxiv.org/abs/2512.21113

Chapters
{chapters}

Notes
• Bar lengths are typed from Table 1 (App. A.2.1): mean one-step test MSE on the limit cycle over 10
  seeds (NARX: one deterministic fit, no seeds). The table's standard deviations are not plotted.
• The phase portraits, the sliding window, the delay-coordinate loop and the window-average loop are our own
  simulation of the paper's equations (µ = 0.5, Δt = 0.1; transients with the paper's BDF settings, the limit cycle at tighter tolerance), not the paper's trained
  models. The paper's figures are images; we describe Fig. 6 rather than redraw it.
• The attention-weight bars illustrate the patterns §4.1 describes (nearly uniform without positional encoding,
  lag-specific with it); the weights are not the paper's.
• The paper's text and its table disagree on positional encoding: §4.1 says it reshapes attention "without
  systematically improving prediction accuracy", but Table 1 shows about 86× lower error with it in the 2-D model,
  and §5.2 calls it "a measurable improvement" for Van der Pol. We follow the table.
• Takens' bound n ≥ 2d + 1 is a sufficient condition; the paper takes d = 2 for this oscillator, giving n = 5.
• The climate-emulator question is our extrapolation, not a claim of the paper.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'analog'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
