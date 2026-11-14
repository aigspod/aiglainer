"""From Entropy to Epiplexity (Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson, arXiv:2601.03220v2): the paper end to end,
in about ten minutes. This folder also hosts the topic's kit, epikit.py (ECA diagrams, the S_T | H_T bar, loss-area
curves, the observer, Game of Life, chart helpers, title/end cards); other pieces use it with
SOURCES = ['epiplexity/videos/epiplexity'] and `from epikit import *`. Figure data is read from the TOPIC's data/
(projects/epiplexity/data) by epikit.tdata(). An aigs pod extra, not journal club: see projects/epiplexity/AGENTS.md."""
from margin_notes import NOTES

HUD = 'epiplexity  ·  an explainer'
OUTPUT_NAME = 'from_entropy_to_epiplexity.mp4'

CHAPTERS = ['The puzzle', 'The idea', 'Computation creates', 'Order matters', 'More than the source', 'Real data',
            'Limits & questions']
STEPS = ['the puzzle', 'the idea', 'the evidence', 'the stakes']
CHAPTER_STEPS = {0: (0,), 1: (1,), 2: (2,), 3: (2,), 4: (2,), 5: (3,), 6: (3,)}

SCENE_MODULES = ['scenes1', 'scenes2', 'scenes3']

MUSIC = dict(style='mysterium', duck_db=9, duck_ramp=1.2, duck_bridge=2.0,
             intro_until='Title', arp_from='Automata', arp_until='Family')

CHAPTER_TITLES = {
    'ColdOpen': 'Cold open: where did AlphaZero’s knowledge come from?', 'Title': 'From Entropy to Epiplexity',
    'Shannon': 'Shannon: information as surprise', 'Kolmogorov': 'Kolmogorov: the shortest program',
    'Crack': 'The crack: pseudorandom numbers', 'Observer': 'Putting the observer in: S_T and H_T',
    'Spectrum': 'Structure vs randomness, object by object', 'Measuring': 'Measuring it from loss curves',
    'Automata': 'Paradox 1: can computation create information?', 'Fig3': 'Rules 15, 30, 54 (Fig. 3)',
    'OurRun': 'Our laptop run (not the paper’s)', 'OneWay': 'Paradox 2: one-way functions (Fig. 4a)',
    'Chess': 'Chess in reverse order (Fig. 4c, Fig. 7)', 'Induction': 'Paradox 3: induction (Fig. 5b)',
    'Emergence': 'Emergence: Life and rule 54 (Fig. 6)', 'Natural': 'Text, chess, images (Fig. 8a, 8b)',
    'Selection': 'Choosing data (Fig. 8c)', 'Family': 'Shannon, Kolmogorov, epiplexity side by side',
    'Limits': 'Limits', 'Questions': 'Questions to think about', 'End': 'Takeaway',
}

DESCRIPTION = """From Entropy to Epiplexity: a motion-graphics explainer.

Shannon entropy and Kolmogorov complexity assume an observer with unlimited computation, so they say a pseudorandom stream holds almost no information and that computation can't create any. This paper puts a time budget into the definition: the shortest two-part code a time-bounded observer can find splits information into epiplexity (structure the observer can learn, the length of its best model) and time-bounded entropy (what still looks random to it). The video walks through the classic theories, the definition, how to measure it from neural-network loss curves, the paper's three paradoxes (computation creating information, order mattering, models learning more than their data's generator) and what it says about real data.

Paper: Marc Finzi, Shikai Qiu, Yiding Jiang, Pavel Izmailov, J. Zico Kolter, Andrew Gordon Wilson (2026). From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence. arXiv:2601.03220v2
https://arxiv.org/abs/2601.03220   Code: https://github.com/shikaiqiu/epiplexity

Chapters
{chapters}

Notes
• Charts of Figs. 2c, 3, 4a, 4c, 5b, 6, 7, 8a, 8b and 8c are redrawn from data extracted from the paper's figures.
• Cellular-automaton and Game of Life pictures are computed exactly from their rules. The chessboard, the loss-curve sketches, the information bars and the observer icon are illustrations.
• "Our run" and "our check" are our own laptop experiments, a miniature cousin of Fig. 3, not the paper's results: a ~0.8M-parameter transformer predicting 32-cell rows of rules 15/30/54/110 (and coin flips) 8 steps ahead for 4,000 training steps, plus a 20,000-step run 16 steps ahead (rule 54's loss-curve area grows past rule 15's); and gzip/xz on 2^20-bit sources.
• Text vs figure: Fig. 8a's caption says 1B tokens; §6.2 says 5B, and the bars only make sense at 5B. The video follows the text. Fig. 8b's bars equal Fig. 9's infinite-compute limit, so they are shown as that limit. Fig. 8c's axes are truncated; the differences are small.
• The comparison table (Shannon, Kolmogorov, sophistication, usable information, epiplexity) is our framing of the paper's §2 and §7.
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'mysterium'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
