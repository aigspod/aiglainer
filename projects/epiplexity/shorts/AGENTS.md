# epiplexity/shorts

Five 9:16 shorts for arXiv:2601.03220v2. Facts, accuracy notes and the naming rule: [../AGENTS.md](../AGENTS.md)
(an aigs pod extra, not journal club: no "/mull/" or "journal club" in the HUD, captions or descriptions).

| name | upload title / headline | hook (first line) | scenes (native, `epishorts.py`) | length | voice, score |
|---|---|---|---|---|---|
| `seed` | A million bits, one seed / Random to whom? | a million random-looking bits from a seven-byte seed | `SeedStretch` (SHA-256 bits, computed), `SeedJudges` (Shannon 56 bits; our xz check 1.000 bits per bit, like coin flips; Thm 9 bar, illustration) | 0:44.6 | `bella-nicole`, `night` |
| `rules` | Three rules, three fates | three tiny rules, each fits on one line | `RulesGrow` (rules 15/30/54, computed), `RulesFig3` (Fig. 3 S_T frontier, then each rule's bits split at the largest budget) | 0:45.1 | `michael`, `analog` |
| `mystery` | The reader works harder | you work harder than the mystery's author | `MysteryLanes` (author vs reader, illustration; Sutskever quote), `MysteryBits` (Fig. 5a setup computed, 2^h fills, Fig. 5b bars) | 0:44.4 | `bella-nicole`, `silencia` |
| `order` | Same games, different lesson | can reading order change what you learn? | `OrderTwoWays` (Fig. 4b orderings, board illustration, Shannon's chain rule), `OrderData` (Fig. 4c S_T, Fig. 7 bars from zero) | 0:44.8 | `michael`, `daylight` |
| `pixels` | Why text beats pixels | web text or tiny images: which holds more? | `PixelsTotal` (Fig. 8a totals), `PixelsStructure` (Fig. 8a S_T, ranking flips; 4.1% vs 0.4% structure) | 0:43.2 | `bella-nicole`, `dawn` |

Lengths are the final MP4s. Every short: `KIND = 'short'`, `SOURCES = ['epiplexity/videos/epiplexity']`, HUD
`epiplexity`, CITE `finzi, qiu, jiang et al. · arxiv 2601.03220`, `MUSIC` `duck_db = 9`, `duck_ramp = 1.2`; the
first scene holds 0.5 s, the last 2.4 s (the 1-2 s fade tail). Headlines are 3-5 words, one amber word each. Each
`DESCRIPTION` has the hook, the citation, "An unofficial explainer, not produced by the authors.", the synthetic-voice
line (`{voice}`), what is paper data vs illustration vs our check, and hashtags.

## Shared code: `epishorts.py` (this folder)

All ten scenes live in `shorts/epishorts.py` (its docstring lists them by short). It imports the topic kit
(`from epikit import *`, from `SOURCES`) and `INFERNO` from the long video's `scenes3.py`; it subclasses nothing and
edits nothing in `videos/`. A short finds it because its `project.py` puts `shorts/` on `sys.path`:

```python
import os, sys
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))     # shorts/: epishorts.py
```

A change to `epishorts.py` (or to `epikit.py`, which every piece uses) changes these shorts: rebuild them and check
`out/narrated/qa/safe_*.png`. Helpers there: `lab` (19 px mono label), `sha_bits` (our compressor check's generator),
`col_chart` (zero-based columns with values and labels).

## Accuracy

- Data via `epikit.tdata`: `fig3_eca.json` (rules), `fig5_induction.json` (mystery), `fig4_owf_chess.json` and
  `fig7_chess_ood.json` (order), `fig8_natural.json` (pixels), `ours_compress.json` (seed, labelled "our check").
- `seed`: our check's generator is SHA-256 in counter mode on a **7-byte (56-bit)** seed, so the short says seven
  bytes / fifty-six bits (the long video's Crack scene draws a 64-bit seed). "The paper's theorem" is Thm 9 (a secure
  generator looks random to a polynomial-time observer); the bar is labelled an illustration.
- `rules`: the split bars are shares of each rule's bits at the largest budget (S_T vs H_T from Fig. 3), with each
  total printed, so rule 15's "almost all structure" reads as a share of only 2.2 × 10⁵ bits.
- `mystery`: "each hidden bit doubles the possibilities" is the paper's own reading (2^h candidate fills; compute
  grows exponentially with h). Fig. 5b's epiplexity goes 2.4 → 5.6 million bits for h = 0 → 5 ("more than doubles").
- `order`: Fig. 7 values print as 25.8% / 25.9% (puzzles) and 21.0% / 28.2% (centipawn); bars start at zero.
  "Centipawn" stays off air ("judging who has the advantage").
- `pixels`: Fig. 8a at 5 billion tokens (the caption's 1B is a typo; see ../AGENTS.md), said in the description; the
  on-screen line says "5 billion tokens of each". CIFAR-5M has 3.2× web text's total bits; 0.4% of its bits are
  structure, 4.1% of web text's.

## Status

Built Nov 13, 2026 with `make P=epiplexity/shorts/<name>`: every short ends with 0 flagged; mix WER seed 0.010 (Whisper
writes "bytes" as "bites"; the captions use the script), rules, mystery, order and pixels 0.000. Frames and
`out/narrated/qa/safe_*.png` checked: nothing that matters in the red, no overlaps. Nobody has listened with sound
(voice, music bed, duck depth and the fade tail are unheard), and nobody has watched on a phone.

- `MysteryBits` fills the gap before the Fig. 5b bars with every fill of the hidden bits (2^h chips, computed).
  `OrderData` fills it with Fig. 4c's final-point gap (+17%, reverse vs forward S_T) and an "infer the moves" sketch
  labelled illustration.
- `RulesGrow` uses 48 cells, seed 1, rows 16-108: at 64 cells rule 54's gliders (diagonal tracks of dark triangles in
  its periodic background) were too small to see. Rule 15 from a random row is a shifting, flipping copy of it ("repeats").
