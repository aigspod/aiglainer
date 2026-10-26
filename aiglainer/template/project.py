"""Settings for this video. Every setting is optional; defaults are in aiglainer/project.py."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  __NAME__'      # top-left label on every chapter scene
OUTPUT_NAME = '__NAME___journal_club.mp4'

# Chapter names; a scene sets `chapter = i` to show "0i / name" top right and a tick on the progress bar.
CHAPTERS = ['The question', 'The method', 'Takeaways']

# Optional story spine, shown as a tracker at the top while a scene's chapter maps onto a step.
# Use it when the paper's argument has stages (e.g. ['behavior', 'cause', 'mechanism']); [] hides it.
STEPS = []
CHAPTER_STEPS = {}

SCENE_MODULES = ['scenes']           # where scene classes live (narration.py refers to them by name)

# Optional un-narrated cut (`make CUT=full`): the scenes played at their authored speed.
def FULL_CUT():
    import scenes
    return [scenes.Title(), scenes.Question(), scenes.Method(), scenes.Takeaway()]

# Shape the score with scene names: a quiet drone until `intro_until`, an arpeggio between the other two.
MUSIC = dict(intro_until='Question', arp_from='Method', arp_until='Takeaway')

# YouTube chapter titles (default: the scene class name) and description; {chapters}/{voice} are filled in.
CHAPTER_TITLES = {'Title': '__TITLE__', 'Question': 'The question', 'Method': 'How it works', 'Takeaway': 'Takeaways'}
DESCRIPTION = """__TITLE__, a motion-graphics explainer for journal club.

Paper: AUTHORS (YEAR). __TITLE__. VENUE. arXiv:XXXX.XXXXX

Chapters
{chapters}

Notes
• Charts are redrawn from data extracted from the paper's figures.
{voice}• This is an unofficial explainer, not produced by the authors.
"""

THEME = {}                           # override colour tokens from aiglainer/core.py PAL, e.g. {'y': '#e3a75a'}

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
