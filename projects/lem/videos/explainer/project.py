"""LEM (Rautela & Scheinker, NAPAC2025, arXiv:2602.22618): settings for this video. See aiglainer/template/project.py."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  latent evolution'
OUTPUT_NAME = 'LEM_journal_club.mp4'

CHAPTERS = ['The question', 'Background', 'The model', 'Forward', 'Inverse', 'Tuning', 'Limits & discussion']
STEPS = ['forward', 'inverse', 'tuning']
CHAPTER_STEPS = {3: (0,), 4: (1,), 5: (2,)}

SCENE_MODULES = ['scenes']

def FULL_CUT():
    import scenes
    return [getattr(scenes, n)() for n in ('Title', 'Question', 'PhaseSpace', 'Roadmap', 'Compress', 'Evolve', 'Forward',
                                           'InverseBeam', 'InverseSettings', 'Tuning', 'Limits', 'Discussion', 'End')]

MUSIC = dict(duck_db=16, intro_until='Question', arp_from='Compress', arp_until='Limits')

CHAPTER_TITLES = {
    'Title': 'Latent Evolution Models', 'Question': 'The question: seeing the beam where we can’t look',
    'PhaseSpace': 'Background: 6D phase space and its 15 projections', 'Roadmap': 'One model, four jobs',
    'Compress': 'Step 1: compress the beam (VAE)', 'Evolve': 'Step 2: evolve it in latent space (transformer)',
    'Forward': 'Forward: predict downstream', 'InverseBeam': 'Inverse I: run time backwards, with error bars',
    'InverseSettings': 'Inverse II: recover the RF settings', 'Tuning': 'Tuning: Bayesian optimization in latent space',
    'Limits': 'Limits', 'Discussion': 'Questions to think about before we meet', 'End': 'Takeaway',
}
DESCRIPTION = """Latent Evolution Models, a motion-graphics explainer for journal club.

Paper: M. Rautela & A. Scheinker (2026). Advancing Accelerator Virtual Beam Diagnostics through Latent Evolution Modeling: An Integrated Solution to Forward, Inverse, Tuning, and UQ Problems. NAPAC2025, Sacramento. arXiv:2602.22618

Chapters
{chapters}

Notes
• The paper is a short summary with no figures or tables: every visual here is an illustration, not data. Equations are the paper's own.
• Results the paper mentions come from the authors' earlier work (its refs. 32–37).
{voice}• This is an unofficial explainer, not produced by the authors.
"""

THEME = {}

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
