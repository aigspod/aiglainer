# epiplexity/videos

An aigs pod extra, not a journal-club piece: read [../AGENTS.md](../AGENTS.md) first (HUD, endings, no journal-club wording, accuracy notes).

| name | what | length | voice, score |
|---|---|---|---|
| `epiplexity` | the paper end to end: Shannon and Kolmogorov, the crack (pseudorandomness), the definition (S_T, H_T), measuring it, the three paradoxes (Figs. 3-7, our laptop run), real data (Fig. 8), the measures side by side, limits, questions | 10:29 | `bella-nicole`, `mysterium` |
| `counting` | "Who's Counting?": the lineage of information measures as a scorecard. Four files (all zeros, coin flips, a SHA-256 generator, rule 54 pairs) scored judge by judge: Shannon, Kolmogorov, a real compressor (our check), sophistication, the cryptographer, then epiplexity / time-bounded entropy; Fig. 3, our laptop run, the three rules revisited (Fig. 4a), a map of the measures | ~10:18 | `am_michael`, `encore` |

Lengths are the timeline (`make plan`), which the final MP4 matches. Music: `duck_db` 9, `duck_ramp` 1.2, last scene
`hold` 2.4. Each piece stands alone: don't write "last time" or "in the other video".

## The topic kit: `epiplexity/epikit.py`

Other pieces (the second video, the shorts) use it with `SOURCES = ['epiplexity/videos/epiplexity']` and
`from epikit import *`. Its docstring is the API reference. In short:

- **Data:** `tdata('fig3_eca.json')` reads the TOPIC's `data/` (`projects/epiplexity/data/`: extracted figure data and
  `ours_*.json`), falling back to the project's own `data/`. No copies needed. `FIG3_COLORS`, `RULE_COLORS`,
  `ORDER_COLORS`, `LOOP_COLORS` follow the paper's figure hues (lightened for the dark ground).
- **Labels:** `tag(c, OURS | ILLUS | EXACT | CHECK | text, x, y, a, align)` (OURS and CHECK are amber), `src(c, 'Fig. 3', ...)`
  ("data: Fig. 3 · arXiv:2601.03220"), `hdr(scene, c, t, num, kicker, title, sub)` (renumber with `NUM`), `stamp(...)`.
- **Cellular automata, exact:** `eca(rule, width, steps, init, seed)`, `draw_eca(c, grid, x, y, w, t, t0, rows_per_s, color, ...)`
  (cached image, grows row by row; also draws any 0/1 grid, e.g. a Game of Life window), `rule_icons(...)` (the 8
  neighbourhoods), `bits_row(...)`.
- **The motif:** `info_bar(c, x, y, s_w, h_w, ...)`: structure S_T (amber, striped) | randomness H_T (blue static);
  `bar_legend(c, x, y, a)`.
- **Charts:** `LogAxes` (log-x, optional log-y), `LinAxes` (= kit.Axes), `curve_reveal(...)` (draw a data polyline on,
  with dots), `loss_curve(...)` (curve + shaded area above its final value: the prequential picture).
- **Pictures:** `observer(c, x, y, s, a, dial, t, label)` (eye + compute dial), `life_step/life_run/rle/GOSPER/GLIDER/place`
  (Game of Life, exact), `draw_cells`, `chessboard(...)` (Apple Symbols glyphs; discs elsewhere), `code_card(...)`,
  `fade_edge(...)` (alpha-fade a layer's left edge without touching the background), `sci()`, `decade()`.
- **Scenes:** `TitleCard` (rule 54 grows behind the title), `EndCard` (TAKE, STATS, citation + code link),
  `question_cards(...)`.

A change to `epikit.py` changes every piece that imports it. The scenes in `scenes1-3.py` can be subclassed too
(SCENE_MODULES order), e.g. a short cropping `Fig3` or `OurRun`.

## Caveats

- Figure data are read from the topic's `data/`; `extract_paper.py` there documents how. The scenes never trace a figure
  by eye; the loss-curve sketches in `Measuring`, the info bars, the chessboards and the observer are labelled
  "illustration"; ECA and Life pictures are labelled "computed from the rule".
- `OurRun` shows `ours_rules_n32_k8.json` (and the 20,000-step `ours_rules_n32_k16_s20000.json` if present), always
  labelled "our run (not the paper's)". `ours_order_k8_s4000.json` (rule 30 forward vs reverse) is NOT shown: the
  model never learned the forward direction beyond n = 8 (both directions sit at the 2n random-guess level), so it
  says nothing about the paper's Fig. 4a.
- Built Nov 13, 2026: 80 lines, 1,282 words, 0 flagged, mix WER 0.009. Nobody has listened to it yet.

## `counting/`: its own kit, `countkit.py`

Independent of `epikit.py` (built in parallel). `countkit.py`: the four files, computed (`file_bits`, `bit_image`,
`file_thumb`, `eca`), the scorecard (`COLS` holds every judge's verdict per file; `scorecard(c, t, cols_done,
cols_now, times, ...)`; `ScoreScene` subclasses fill one column), `quote_card`, `card`, `tag`, `brace`,
`question_cards`. Shorts can reuse it with `SOURCES = ['epiplexity/videos/counting']` and `from countkit import *`;
good short material: `ColdOpen` (four files, one question), any `Score*` scene, `Incomputable` (compressors vs
Kolmogorov), `Crypto` (next-bit predictor at 50%), `Laptop` (the ranking flips with budget), `End` (full scorecard).

- The fourth file is **pairs** (random 64-cell row X, then rule 54 applied 48 times), not a row-by-row history: a
  learner predicting row t+1 from row t learns the local rule in a few bits, so a history would have LOW epiplexity.
  Pairs match the paper's Fig. 3 setup (Y = F^48(X)) and its emergence argument (predicting far ahead). Its Shannon
  entropy is the random half (0.5 M bits); xz shrinks it only to 0.94 (`lab/check_pairs.py`, `data/ours_compress_pairs.json`).
- Scorecard numbers: Shannon/Kolmogorov by construction (seed 56 bits; zeros ~log2 n = 20); the compressor column is
  xz from our checks; sophistication, the cryptographer and epiplexity are qualitative (Thm 9, Fig. 3), said on screen.
- `Laptop` shows `ours_rules_n32_k16_s20000.json` (curves) and the prequential area at 4,000 steps (the separate
  `ours_rules_n32_k16.json` run) vs 20,000 steps: rule 15 3.9-4.0e6 both times; rule 54 0.99e6 then 9.1e6. Each
  area is against its own run's final loss. Labelled "our run"; the order run (rule 30 fwd/rev) is not used.
- The next-bit predictor (`scenes1.next_bit_check`) is an order-10 context counter run online over 20,000 bits of the
  generator: 49.6% right (our check, computed at render time).
- Data copied into `counting/data/` from the topic's `data/` (`fig3_eca.json`, `fig4_owf_chess.json`,
  `ours_compress.json`, `ours_rules_n32_k16*.json`); recopy if those are regenerated.
- Narration avoids the author names (Whisper fails Qiu, Izmailov, Kolter); they are on the title card and in the
  description. Built Nov 13, 2026; nobody has listened to it yet.


## Published (Nov 14, 2026, The AIGS Pod channel, public)

Videos: `epiplexity` https://youtu.be/JCLiEXVWQ7g ("From Entropy to Epiplexity: rethinking information for bounded
observers"), `counting` https://youtu.be/JWgsdWJptkA. Shorts: seed UjkjoPaTtRU, rules V1ooO2hSie0, mystery AsYt1Y73C_I,
order fEcivv_Za6E, pixels 7Gyu6Gnx0B0 (youtube.com/shorts/<id>). Each has its description, captions.srt as English
subtitles, and (videos) its thumbnail; audience not for kids, paid promotion No, AI use No. The owner watched them first.
