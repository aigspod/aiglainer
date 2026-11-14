"""Who's Counting?: how Shannon entropy, Kolmogorov complexity, sophistication, cryptographic pseudorandomness and
epiplexity each count the information in the same four files. A companion to arXiv:2601.03220v2 (Finzi, Qiu, Jiang,
Izmailov, Kolter, Wilson). An aigs pod extra, not journal club: see projects/epiplexity/AGENTS.md. Drawing helpers live in
countkit.py (the four files, the scorecard); scenes in scenes1.py (judges) and scenes2.py (the paper and after)."""
from margin_notes import NOTES

HUD = 'epiplexity  ·  an explainer'
OUTPUT_NAME = 'epiplexity_whos_counting.mp4'

CHAPTERS = ['Shannon', 'Kolmogorov', 'Structure vs noise', 'Cryptographers', 'Epiplexity', 'Measuring it',
            'The rules, revisited', 'The family', 'To think about']

STEPS = []
CHAPTER_STEPS = {}

SCENE_MODULES = ['scenes1', 'scenes2']

# 'encore' (soft solo piano) keeps clear of the topic's other video; music stays well under the host.
MUSIC = dict(style='encore', duck_db=9, duck_ramp=1.2, intro_until='Title', arp_from='Kolmogorov', arp_until='Verdict')

CHAPTER_TITLES = {
    'ColdOpen': 'Four files, one question', 'Title': "Who's Counting?",
    'Shannon': 'Shannon (1948): information is surprise', 'ScoreShannon': "Shannon's scores",
    'Rules': "Three rules of Shannon's information", 'Kolmogorov': 'Kolmogorov complexity: the shortest program',
    'ScoreK': "Kolmogorov's scores", 'Incomputable': 'Incomputable; real compressors (our check)',
    'ScoreZip': "The compressor's scores", 'Structure': 'Structure vs noise: sophistication, effective complexity, logical depth',
    'ScoreSoph': "Sophistication's scores", 'Crypto': 'Cryptography: randomness depends on the observer',
    'ScoreCrypto': "The cryptographer's verdicts", 'Epiplexity': 'Epiplexity and time-bounded entropy',
    'ScoreEpi': 'The new scores', 'Measuring': 'Measuring it: the area under the loss curve (Fig. 3)',
    'Laptop': 'A laptop-sized check: the ranking flips with budget (our run)', 'Revisited': "Shannon's three rules, revisited (Figs. 3, 4a, 6)",
    'Map': 'The family of measures (our framing)', 'Verdict': 'Was Shannon wrong?',
    'Questions': 'Questions to think about', 'End': 'Same files, different winners',
}

DESCRIPTION = """Who's Counting? Shannon, Kolmogorov, and the bounded observer.

Four files of about a million bits each: all zeros, a million fair coin flips, the output of a pseudorandom generator from a 56-bit seed, and pairs of rows from the cellular automaton rule 54 (a random 64-cell row and the row 48 steps later). Which holds the most information? Shannon entropy, Kolmogorov complexity, a real compressor, sophistication, the cryptographer's pseudorandomness test, and the new epiplexity each give a different answer. A scorecard fills in judge by judge, and each judge's blind spot motivates the next. This is a companion to a 2026 paper that defines epiplexity: the structural information a computationally bounded observer can extract from data, as opposed to time-bounded entropy, what still looks random to it.

Paper: Marc Finzi, Shikai Qiu, Yiding Jiang, Pavel Izmailov, J. Zico Kolter, Andrew Gordon Wilson (2026). From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence. arXiv:2601.03220 (v2, March 2026). https://arxiv.org/abs/2601.03220
Code: https://github.com/shikaiqiu/epiplexity

Chapters
{chapters}

Notes
• Redrawn from data extracted from the paper's figures: Fig. 3 (epiplexity of ECA rules 15, 30, 54 against compute) and Fig. 4a (rule 30 forward vs reverse).
• Our own checks, not the paper's: the compression ratios (gzip, bz2, xz on 2^20 bits per file; the pseudorandom file is SHA-256 in counter mode), the next-bit predictor on the generator's output, and the laptop run (a ~0.8M-parameter transformer trained online to predict a 32-cell row 16 steps ahead; prequential area above each run's final loss). After 4,000 steps rule 15's area is larger than rule 54's (4.0 vs 1.0 million bits); after 20,000 steps rule 54's is larger (9.1 vs 3.9).
• The scorecard's entries for sophistication, the cryptographic test and epiplexity are qualitative, following the paper's theorems (Thm 9 for the pseudorandom file) and Fig. 3; the coffee cup, the loss-curve sketches and the map of measures are illustrations (our framing).
• Prequential epiplexity (the area under the loss curve) is a heuristic; the paper's requential code is the rigorous estimate. Rule 30 is believed, not proven, to be one-way.
• Historical notes are limited to: Shannon 1948; Solomonoff 1964, Kolmogorov 1965, Chaitin 1966; Martin-Löf 1966; Blum-Micali and Yao 1982; Koppel 1988; Bennett 1988; Gell-Mann and Lloyd 1996; excess entropy (Crutchfield and Packard 1983, Grassberger 1986); Rissanen 1978; Xu et al. 2020. Quotes are Shannon's (1948) and von Neumann's (1951, quoted in the paper).
{voice}• An unofficial explainer, not produced by the authors. Score: original, in the style 'encore'.
"""

def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
