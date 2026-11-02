"""Do circuits explain model errors? Video 3 of 3: how the wrong name wins. (arXiv:2609.35686; journal club Nov 4.)
Shared pieces (errkit.py) come from errors-gap."""
SOURCES = ['errors-gap']
HUD = 'the aigs pod  ·  /mull/  ·  circuits & errors · 3/3'
OUTPUT_NAME = 'circuit_errors_3_how_the_wrong_name_wins.mp4'
CHAPTERS = ['The task', 'The search', 'The result', 'Path one', 'Path two', 'What it means']
SCENE_MODULES = ['scenes3', 'scenes']   # scenes3 first: its Title/Discussion/End win over part 1's
MUSIC = dict(style='mysterium')

CHAPTER_TITLES = {'ColdOpen': 'Cold open: right where the model is wrong', 'Title': 'How the wrong name wins', 'Circuit': 'The classic circuit (Table 8)', 'Gap': 'The gap (Table 1)', 'Search': 'Looking for what’s missing (App. D)',
                  'Result': 'Three in four: the 63-addition extension (§4.2)', 'PathOne': 'Path one: weaker inhibition (Fig. 2A)',
                  'PathTwo': 'Path two: a different label (Fig. 2B)', 'Meaning': 'A cheap check (§5)',
                  'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """How the wrong name wins. Part 3 of 3 on "Do circuits explain model errors?", for the aigs pod journal club.

The classic indirect-object circuit in GPT-2 small reproduces only 14% of the model's mistakes. A search adds 63
head-position pairs and reaches 75% on fresh sentences, while barely touching the correct ones. Tracing the additions
shows two omitted computations: context that weakens the inhibition of the repeated name, and first-layer heads that
change how the correct name looks to the name movers.

Paper: Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si (2026). Rethinking Circuit
Evaluation: Do Circuits Explain Model Errors? Preprint. arXiv:2609.35686

Chapters
{chapters}

Notes
• Which 63 head-positions were added isn't listed in the paper beyond the five first-layer heads; their positions in
  the search-space picture are an illustration.
• Attention percentages (78.5 → 28.3, 3.4 → 15.7, 59.3 → 53.4, 68.4 → 71.9) are for Fig. 2's two example prompts only.
• On a fresh 5,200-sentence check, correct agreement fell 0.85 points, beyond the search's 0.5-point tolerance (Table 4).
• The climate-emulator card is our extrapolation, not a result of the paper.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'mysterium'.
"""

def THUMBNAIL(c):
    from aiglainer.core import text
    from aiglainer.notes import lamp, swash, sticky
    lamp(c, 1500, 260, 2.4, 1, on=1)
    text(c, 'Sara?', 120, 430, 170, 700, 'f')
    w = text(c, 'Courtney.', 120, 640, 190, 400, 'r', kind='italic')
    swash(c, 120, 120 + w, 680, 'y', 1, 1, w=7)
    text(c, 'how the wrong name wins', 128, 820, 60, 500, 'ink')
    sticky(c, 1380, 640, ['circuits &', 'errors · 3/3'], 1, rot=5.0, w=320, h=220)
