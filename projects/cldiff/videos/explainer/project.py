"""Conditional latent diffusion (Scheinker & Williams, arXiv:2502.18684): settings for this video."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  latent diffusion'
OUTPUT_NAME = 'CLD_journal_club.mp4'

CHAPTERS = ['The question', 'Background', 'Data & signals', 'The model', 'Results', 'Adaptive tracking', 'Limits & discussion']
STEPS = ['compress', 'generate', 'track']
CHAPTER_STEPS = {3: (0, 1), 4: (1,), 5: (2,)}

SCENE_MODULES = ['scenes']

ORDER = ('Title', 'Question', 'PhaseSpace', 'Data', 'Signals', 'Compress', 'Diffuse', 'Label', 'Results', 'Errors',
         'Adaptive', 'Tracking', 'Limits', 'Discussion', 'End')

def FULL_CUT():
    import scenes
    return [getattr(scenes, n)() for n in ORDER]

MUSIC = dict(duck_db=16, intro_until='Question', arp_from='Compress', arp_until='Limits')

CHAPTER_TITLES = {
    'Title': 'Adaptive conditional latent diffusion', 'Question': 'The question: cheap monitors, full beam?',
    'PhaseSpace': 'Background: 6D phase space and its 15 projections', 'Data': 'The data: 1.44 million simulated images',
    'Signals': 'The input: beam currents and the condition vector', 'Compress': 'Step 1: compress (VAE)',
    'Diffuse': 'Step 2: generate (latent diffusion)', 'Label': 'Which projection? A physics-informed label',
    'Results': 'Results: generated vs true', 'Errors': 'How big are the errors?',
    'Adaptive': 'Adaptive tuning with extremum seeking', 'Tracking': 'Tracking a drifting beam',
    'Limits': 'Limits', 'Discussion': 'Questions to think about before we meet', 'End': 'Takeaway',
}
DESCRIPTION = """Adaptive conditional latent diffusion, a motion-graphics explainer for journal club.

Paper: A. Scheinker & A. Williams (2025). Adaptive conditional latent diffusion maps beam loss to 2D phase space projections. arXiv:2502.18684

Chapters
{chapters}

Notes
• Figures marked "Fig. N" are crops of the paper's own figures. The error bars are redrawn from the numbers in the legends of the paper's Fig. 8. Anything marked "illustration" is not data.
• All results are from simulations of the LANSCE linac (HPSim).
{voice}• This is an unofficial explainer, not produced by the authors.
"""

THEME = {}

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
