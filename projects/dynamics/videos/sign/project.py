"""Attention can only average: the sign problem (arXiv:2512.21113v2, §2.3, §3.1, App. A.1, §3.2; journal club Nov 11).
This folder also hosts the topic's shared kit: dynkit.py (drawing helpers) and simulate.py (writes data/*.json).
Other pieces use them with SOURCES = ['dynamics/videos/sign'] and `from dynkit import *`."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  dynamics'
OUTPUT_NAME = 'dynamics_attention_can_only_average.mp4'
CHAPTERS = ['The recipe', 'One head', 'Two springs, two heads', 'Time for a sensor', 'Questions']
SCENE_MODULES = ['scenes']
MUSIC = dict(style='encore', duck_db=16, intro_until='Title')

CHAPTER_TITLES = {'ColdOpen': 'Cold open: a spring and a minus sign', 'Title': 'Attention can only average',
                  'Recipe': 'A spring is a two-step recipe (AR(2), §3.1)', 'OneHead': 'One head can only average (§2.3)',
                  'Plane': 'Half the plane is out of reach', 'Springs': 'One spring rings, one goes flat (Fig. 2, simulated)',
                  'TwoHeads': 'A second head brings the minus (App. A.1)', 'TwoMasses': 'Two masses: time stands in for a sensor (§3.2)',
                  'Delay': 'Why four steps? A linear check', 'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """Attention can only average: the sign problem. A motion-graphics explainer for the aigs pod journal club.

Predicting a spring's next position from its last two is a two-term recipe. A single attention-only head (no residual
path) mixes past samples with softmax weights that are positive and add up to one, then scales the mix by one shared
output number, so both of its effective coefficients always share a sign. A stiff spring (two negative coefficients) is
within reach; a softer spring needs a plus and a minus, and one head oversmooths it. Two heads with opposite-sign output
weights fix it. The paper stresses that this is a boundary case: the limitation "is specific to the single-head
attention-only setting ... and should not be interpreted as a general limitation of practical Transformer
architectures" (§3.1, App. A.1); residual paths, feed-forward layers and more heads can supply the minus. With two
coupled masses and one sensor, three past steps fail and four work: time stands in for the missing sensor.

Paper: Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi (2025). A Mechanistic Analysis
of Transformers for Dynamical Systems. arXiv preprint, v2. arXiv:2512.21113

Chapters
{chapters}

Notes
• Typed from the paper: m, c, k, the 25 Hz sampling and 7.12 / 3.56 Hz (§3.1); Case 1's coefficients a1 = −0.4352,
  a2 = −0.9802 (§3.1; Eq. 20 gives −0.428 for a1, a minor difference); the two-head output weights W_O = [1.087, −1.244]
  (App. A.1); which 2-DOF settings work (§3.2).
• Our calculation: Case 2's coefficients (+1.24, −0.98). The paper gives only their signs.
• Simulated from the paper's equations (our code): the spring responses and spectra, the best one-head fit (one fixed
  weight, no positional encoding; ours, not the paper's trained model, whose weights adapt to the input), the two-head construction (ours; the paper's
  trained model is a different solution), and the AR(3) / AR(4) fits on the first mass (a linear analogue of the
  paper's 3-vs-4-step result, not its transformer). The 2-DOF sampling rate and record length are our assumptions.
• Text vs. numbers: the paper reports 2-DOF modes at 4.1 and 9.5 Hz; its stated parameters give 3.26 and 9.52 Hz.
• The spring doodle's motion is an illustration. The climate-emulator question is our extrapolation.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'encore'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
