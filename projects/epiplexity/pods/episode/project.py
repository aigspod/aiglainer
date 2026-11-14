"""From Entropy to Epiplexity: a single-host audio episode (the owner's personal set; see the topic's naming rule). Script in episode.py;
build with: make P=epiplexity/pods/episode"""
KIND = 'podcast'
TITLE = 'From Entropy to Epiplexity'
OUTPUT_NAME = 'Epiplexity_pod.mp3'
SHOW = 'epiplexity · an explainer'      # ID3 album; the engine's default is the pod's show name, which this topic must not use
ARTIST = 'mahf708'                       # ID3 artist; likewise
SUMMARY = ('From Entropy to Epiplexity (Finzi, Qiu, Jiang, Izmailov, Kolter, Wilson): information for observers with '
           'limited compute. An unofficial explainer.')
BED = 0                     # talk on silence (the podcast norm); music only in the theme, stings and outro
# Soft solo piano. Podcasts honour duck_db (shallower than the template's 16) but always follow the voice's waveform:
# duck_ramp is kept for the house rule and takes effect only in videos (docs/STYLES.md).
MUSIC = dict(style='encore', duck_db=9, duck_ramp=1.2)

DESCRIPTION = """From Entropy to Epiplexity. An unofficial explainer, for anyone curious about information and learning.

AlphaZero learns superhuman chess from nothing but the rules, yet by the accounts of Shannon and Kolmogorov it seems
to have learned almost nothing: a short program can't create information. This episode follows that puzzle through a
2026 paper that puts the observer's computing budget into the definition of information. We start with Shannon
entropy (information as surprise) and Kolmogorov complexity (the shortest program), find the crack in both with
pseudorandom generators, and then meet epiplexity: the size of the best model a time-limited observer can find, set
against time-bounded entropy, what still looks random to it. We cover how to estimate it from a training run (the
area under the loss curve, and a stricter teacher-student code), three puzzles it untangles (computation creating
information, order mattering, models learning more than the process that made their data, with cellular automata,
chess, induction and emergence), what it says about text versus images and data selection, and where it is still
on shaky ground.

Paper: Marc Finzi, Shikai Qiu, Yiding Jiang (equal contribution), Pavel Izmailov, J. Zico Kolter, Andrew Gordon
Wilson (Carnegie Mellon University, New York University). From Entropy to Epiplexity: Rethinking Information for
Computationally Bounded Intelligence. arXiv:2601.03220v2 (2026). https://arxiv.org/abs/2601.03220
Code: https://github.com/shikaiqiu/epiplexity

Chapters
{chapters}

Questions to think about
{questions}

Notes
• The "Swedish mathematician" is Per Martin-Löf (1966). Algorithmic complexity: Solomonoff (1964), Kolmogorov
  (1965), Chaitin (1966). Pseudorandomness: Blum and Micali (1982), Yao (1982). The minimum description length
  principle: Rissanen (1978). The murder-mystery line is Ilya Sutskever's (2019), quoted in the paper.
• The area-under-the-curve (prequential) estimate is a heuristic; the teacher-student (requential) estimate is the
  rigorous one, typically 2-10x slower. They usually rank datasets alike, but that is not guaranteed.
• The theorems assume cryptographic primitives (pseudorandom generators, one-way functions or permutations) exist.
  Rule 30 is believed, not proven, to be one-way. The paper has not proven that the Game of Life meets its
  definition of emergence.
• Epiplexity measures how much structure a model extracts, not whether it is relevant to a given task; the chess and
  data-selection results are correlations, not guarantees.
• Text, chess and images (Fig. 8a): the caption says 1B tokens, the text 5B; the figure's totals fit 5B, so we say 5B.
  The trillion-token comparison (Fig. 8b) is said without a compute figure: the text gives 10^25 FLOPs, but the bars
  match the infinite-compute limit in Fig. 9. The ordering is the same either way.
• The data-selection (ADO) results are adapted from Jiang et al. (2025), which shares an author with this paper; the
  gains in that figure are small (for example, downstream accuracy 0.590 against 0.585).
• The closing questions are ours, not the paper's.
{voice}• An unofficial summary, not produced by the authors.
"""
