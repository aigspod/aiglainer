"""Room to unfold: latent room and parameters (§4.2, App. A.4, §4.3, App. A.5, §5.1 of arXiv:2512.21113v2).
A standalone 16:9 explainer. Shared drawing pieces come from dynamics/videos/sign (dynkit.py); our Chafee-Infante
simulation is simulate.py -> data/ci.json."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  dynamics'
OUTPUT_NAME = 'dynamics_room_to_unfold.mp4'
SOURCES = ['dynamics/videos/sign']
SCENE_MODULES = ['scenes']

CHAPTERS = ['The latent', 'Room', 'Parameters', 'Our extrapolation', 'Questions']

MUSIC = dict(style='mysterium', duck_db=16, intro_until='Title')

CHAPTER_TITLES = {
    'ColdOpen': 'Cold open: good forecasts, different insides',
    'Title': 'Room to unfold',
    'Latent': 'One sensor, five readings, a latent state',
    'Rod': 'Chafee-Infante: a rod on a two-dimensional surface',
    'Fold': 'Symmetry folds the single-sensor view (our simulation)',
    'Room': 'A latent of two collapses; three unfolds',
    'Cylinder': 'Flow past a cylinder: Reynolds number 100 to 750',
    'Loops': 'Without Re the loops overlap; with Re they separate',
    'Recon': 'Rebuilding the whole field: ~70x worse without Re',
    'Lesson': 'One-step accuracy is not latent identifiability',
    'Emulators': 'Our extrapolation: climate emulators',
    'Discussion': 'Questions to bring',
    'End': 'Takeaway',
}

DESCRIPTION = """Room to unfold: latent room and parameters. A motion-graphics explainer for the aigs pod journal club.

A one-layer transformer that watches a system through a single sensor has to build its own internal state (the
latent) from a few past readings. This video follows two of the paper's tests. On the Chafee-Infante equation, five
readings in principle hold enough information, yet a latent of two numbers collapses the two-dimensional surface while three
numbers unfold it: the surface's symmetry folds what one sensor sees. On flow past a cylinder, a model not told the
Reynolds number mixes regimes together in its latent; rebuilding the full v_x velocity field from that latent is about
70x worse (66.5x over the field, 53.6x in the wake). One-step accuracy is not latent identifiability.

Paper: Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi (2025). A Mechanistic Analysis
of Transformers for Dynamical Systems. arXiv preprint, v2. arXiv:2512.21113

Chapters
{chapters}

Notes
• Simulated: the rod and the folding picture are our own three-mode Galerkin simulation of the paper's
  Chafee-Infante equation (§4.2: nu = 0.16, sensor at the 10th of 256 grid points, two readings 4/9 apart), not the
  paper's data or figures. The fold is drawn in two readings for display; the paper's models get five.
• Typed from the paper: the cylinder reconstruction errors (§4.3 and App. A.5: 1.12e-4 vs 7.45e-3 whole field,
  2.48e-4 vs 1.33e-2 wake), the Reynolds number ranges, the largest one-step error across both models (about 2.3e-2).
• Illustrations, not data: the latent pictures for a latent of two and three numbers, the latent loops with and
  without Re, the error shapes across Re, the vortex wake, and the sensor signal in the model diagram.
• App. A.5 says the fold-to-fold spread is "two orders of magnitude" smaller than the gap; from its own numbers it is
  about 13x smaller.
• The climate-emulator scene (ACE, SamudrACE) is our extrapolation, not a claim of the paper.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'mysterium'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
