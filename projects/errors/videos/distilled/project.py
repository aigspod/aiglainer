"""Do circuits explain model errors? The whole paper in ~6 minutes, voiced by Michael, scored in 'silencia'.
Scenes are reused from the three part videos (see distilled.py)."""
SOURCES = ['errors/videos/gap', 'errors/videos/excuses', 'errors/videos/wrongname']
HUD = 'the aigs pod  ·  /mull/  ·  circuits & errors'
OUTPUT_NAME = 'circuit_errors_in_six_minutes.mp4'
CHAPTERS = ['The test', 'The gap', 'Explained away?', 'What was missing', 'Questions']
SCENE_MODULES = ['distilled']
MUSIC = dict(style='silencia', intro_until='Title')

CHAPTER_TITLES = {'ColdOpen': 'Cold open: right where the model is wrong', 'Title': 'Do circuits explain model errors?',
                  'Circuit': 'What is a circuit?', 'Knockout': 'Knock out the rest: faithfulness', 'CloseCalls': 'Are mistakes just close calls? (Table 7)', 'PathTwo': 'A second path (Fig. 2B)', 'TwoPiles': 'Two piles', 'Table1': 'The gap (Table 1)',
                  'Fig1': 'Are mistakes just rare? (Fig. 1)', 'Nudge': 'Rate vs identity of errors',
                  'Result': '63 extra pieces: 14% → 75% (§4.2)', 'PathOne': 'How the wrong name wins (Fig. 2A)',
                  'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """Do circuits explain model errors? The whole paper in about six minutes, for the aigs pod journal club.

A circuit is supposed to explain how a network does a task. Scored separately where the model is right and where it
is wrong, the classic indirect-object circuit in GPT-2 small agrees on 99.5% of the model's correct answers and only
15.2% of its mistakes. The gap survives the obvious excuses, and 63 extra head-positions recover most of it.

Paper: Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si (2026). Rethinking Circuit
Evaluation: Do Circuits Explain Model Errors? Preprint. arXiv:2609.35686

Chapters
{chapters}

Notes
• Charts are typed from Tables 1 and 8 or redrawn from Fig. 1's vector data; the dot field, the sentence tiles and the
  positions of the 63 additions are illustrations. Fig. 2's attention percentages are for its two example sentences.
• The climate-emulator question is ours, not the paper's.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'silencia'.
"""

def THUMBNAIL(c):
    from aiglainer.core import text
    from aiglainer.notes import lamp, swash, sticky
    lamp(c, 1500, 260, 2.4, 1, on=1)
    text(c, 'Right where', 120, 430, 150, 300, 'ink', kind='display')
    w = text(c, 'the model', 120, 600, 150, 300, 'ink', kind='display')
    w = text(c, 'is wrong', 120, 790, 170, 400, 'r', kind='italic')
    swash(c, 120, 120 + w, 830, 'y', 1, 1, w=7)
    sticky(c, 1380, 640, ['the whole paper', 'in 6 minutes'], 1, rot=5.0, w=320, h=220)
