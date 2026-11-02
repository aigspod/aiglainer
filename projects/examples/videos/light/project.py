"""A reference for restyling: the template video with a light look, another typeface, another voice and a deeper duck.
See docs/STYLES.md. Build with: make P=examples/videos/light"""
from margin_notes import NOTES

HUD = 'aiglainer  ·  an example'      # top-left label on every chapter scene
OUTPUT_NAME = 'examples-light_journal_club.mp4'

# Chapter names; a scene sets `chapter = i` to show "0i / name" top right and a tick on the progress bar.
CHAPTERS = ['The settings', 'The method', 'Takeaways']

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
MUSIC = dict(style='encore', duck_db=16, intro_until='Question', arp_from='Method', arp_until='Takeaway')   # quieter under the host

# YouTube chapter titles (default: the scene class name) and description; {chapters}/{voice} are filled in.
CHAPTER_TITLES = {'Title': 'A different look', 'Question': 'What you can change', 'Method': 'How it works', 'Takeaway': 'Takeaways'}
DESCRIPTION = """A different look: what the settings in docs/STYLES.md can do, on the template video.

Chapters
{chapters}

Notes
• The curve is the template's example data, not from any paper.
{voice}• This is an unofficial explainer, not produced by the authors.
"""

# The point of this project: a look that isn't the house one, from settings alone (docs/STYLES.md).
THEME = dict(ground='#f5efe3', ink='#231f1a', muted='#6f6a62', faint='#cfc6b4', line='#ddd4c2', panel='#fffaf0',
             panel2='#f0e8d8', pencil='#5b5a55', y='#b5701f', g='#2a6fb5', f='#1f8f6a', c='#c8552a', r='#bc3a55',
             v='#7d7a85', x='#8a5fa8', fade='#f5efe3', shadow='#8a7f6a')
BACKGROUND = dict(glow=0.5, vignette=0, grain=0.5, frame=False)
FONTS = dict(display='Inter.ttf', italic='Inter.ttf')       # sans headings instead of Fraunces

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
