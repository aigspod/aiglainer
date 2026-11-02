"""Do circuits explain model errors? Video 2 of 3: can the gap be explained away? (arXiv:2609.35686; journal club Nov 4.)
Shared pieces (errkit.py) and Fig. 1 data (data/fig1.json) come from errors-gap."""
SOURCES = ['errors-gap']
HUD = 'the aigs pod  ·  /mull/  ·  circuits & errors · 2/3'
OUTPUT_NAME = 'circuit_errors_2_explained_away.mp4'
CHAPTERS = ['The gap', 'Rare errors?', 'Close calls?', 'A nudge?', 'Verdict', 'Questions']
SCENE_MODULES = ['scenes2', 'scenes']   # scenes2 first: its Title/Discussion/End win over part 1's
MUSIC = dict(style='analog')

CHAPTER_TITLES = {'Title': 'Can the gap be explained away?', 'Piles': 'Two piles: where the model is right, and where it is wrong', 'Gap': 'The gap (Table 1)', 'Fig1': 'Excuse one: errors are rare (Fig. 1)',
                  'Reweight': 'Weight the mistakes (Table 4)', 'CloseCalls': 'Excuse two: close calls (Table 7)',
                  'Nudge': 'Excuse three: just nudge it?', 'Verdicts': 'Three excuses, one gap',
                  'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """Can the gap be explained away? Part 2 of 3 on "Do circuits explain model errors?", for the aigs pod journal club.

A circuit is a small part of a network that is supposed to explain how the whole network does a task. Circuits that
keep nearly all of a model's correct answers miss most of its mistakes. Is that just because mistakes
are rare, or because they're close calls, or because the circuit is a little too sure of the right answer? The paper
tests all three, and the gap survives on the name task.

Paper: Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si (2026). Rethinking Circuit
Evaluation: Do Circuits Explain Model Errors? Preprint. arXiv:2609.35686

Chapters
{chapters}

Notes
• Fig. 1 is redrawn from the PDF's vector paths. Its Gemma ARC-Challenge points sit at the plotted edge fractions; the
  text's 80.3% / 54.4% at a 1% budget doesn't match the plotted points, so it isn't quoted here.
• For Llama ARC-Challenge at 2%, the numbers (80.0 overall, 46.7 matched, 54.9 errors) imply a reversed gap; the paper
  calls it "narrowed".
• The score bars in "Barely wrong" and the tiles in "Just nudge it?" are illustrations.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'analog'.
"""

def THUMBNAIL(c):
    from aiglainer.core import text, kicker
    from aiglainer.notes import lamp, swash, sticky
    lamp(c, 1500, 260, 2.4, 1, on=1)
    text(c, 'Three', 120, 430, 170, 300, 'ink', kind='display')
    w = text(c, 'excuses', 120, 620, 190, 400, 'y', kind='italic')
    swash(c, 120, 120 + w, 660, 'y', 1, 1, w=7)
    text(c, 'one gap', 120, 820, 120, 700, 'c')
    sticky(c, 1380, 640, ['circuits &', 'errors · 2/3'], 1, rot=5.0, w=320, h=220)
