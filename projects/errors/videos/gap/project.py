"""Do circuits explain model errors? Video 1 of 3: the gap. (arXiv:2609.35686; journal club Nov 4.)
Shared pieces live in errkit.py; errors/videos/excuses and errors/videos/wrongname use them through SOURCES."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  circuits & errors · 1/3'
OUTPUT_NAME = 'circuit_errors_1_the_gap.mp4'
CHAPTERS = ['Circuits', 'Two piles', 'Results', 'Questions']
SCENE_MODULES = ['scenes']
MUSIC = dict(style='encore', intro_until='Title')

CHAPTER_TITLES = {'ColdOpen': 'Cold open: right where the model is wrong', 'Title': 'Do circuits explain model errors?',
                  'Circuit': 'What is a circuit? (the IOI circuit, Table 8)', 'Knockout': 'Knock out the rest: ablation and faithfulness',
                  'TwoPiles': 'Two piles: correct agreement and error agreement', 'Table1': 'The gap (Table 1, IOI)',
                  'Docstring': 'A messier picture (Table 1, Docstring)', 'Discussion': 'Questions to bring', 'End': 'Takeaway'}

DESCRIPTION = """Do circuits explain model errors? Part 1 of 3: the gap. A motion-graphics explainer for the aigs pod journal club.

A circuit is a small part of a network that is supposed to explain how the whole network does a task. This paper
scores circuits against the model's own answers, separately where the model is right and where it is wrong. On
indirect object identification in GPT-2 small, the classic circuit agrees on 99.5% of the model's correct answers
and only 15.2% of its mistakes (mean ablation, Table 1).

Paper: Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si (2026). Rethinking Circuit
Evaluation: Do Circuits Explain Model Errors? Preprint. arXiv:2609.35686

Chapters
{chapters}

Notes
• Bars are typed from Table 1; circuit head groups from Table 8. The dot field of 1,000 sentences is an illustration of
  the IOI error rate (Table 2: 884 errors in 100,000).
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'encore'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
