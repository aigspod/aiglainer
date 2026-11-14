# epiplexity

*From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence*, Marc Finzi\*, Shikai
Qiu\*, Yiding Jiang\*, Pavel Izmailov, J. Zico Kolter, Andrew Gordon Wilson (CMU, NYU; \*equal contribution).
arXiv:2601.03220v2, 16 Mar 2026 (v1 Jan 2026). [arxiv.org/abs/2601.03220](https://arxiv.org/abs/2601.03220). Code:
[github.com/shikaiqiu/epiplexity](https://github.com/shikaiqiu/epiplexity). These pieces are unofficial and not made
by the authors. Layout and commit rules are in [../AGENTS.md](../AGENTS.md).

**This topic is an aigs pod extra, not a journal-club piece** (decided Nov 2026: published on the aigs pod channels,
but no meeting is behind it). Don't use "/mull/", "journal club", "before the meeting" or "see you at the desk":
not in the HUD, title cards, endings, descriptions or narration. Naming the aigs pod is fine but optional (the
shipped cuts don't). Use the HUD `epiplexity  ·  an explainer`. End on reflective questions "to
think about", not meeting prep. Keep the default dark look, scores and house rules for audio: `duck_db` 8-10,
`duck_ramp` about 1.2, and a 1.5-2.5 s fade at the end.

| kind | what |
|---|---|
| `videos/` | ~10-minute explainers (see videos/AGENTS.md when it exists) |
| `pods/` | a single-host episode |
| [shorts/](shorts/AGENTS.md) | five 9:16 shorts of about 45 s (`seed`, `rules`, `mystery`, `order`, `pixels`), native vertical scenes in `shorts/epishorts.py` built on `epikit.py` |
| `lab/` | **our own** laptop experiments (`eca_lab.py`), always labelled "our run" on screen |
| `data/` | figure data extracted from the paper (`extract_paper.py`), and `ours_*.json` from `lab/` |

## The paper in one breath

Shannon entropy and Kolmogorov complexity assume an observer with unlimited computation, so they can't tell
"random" from "structured" the way a real learner experiences it. The paper defines, for an observer limited to time
T, the program P\* minimizing the two-part code |P| + E[log 1/P(X)] over programs that sample and evaluate within T.
**Epiplexity** S_T(X) = |P\*| (structure, the bits in the model). **Time-bounded entropy** H_T(X) = E[log 1/P\*(X)]
(what is left unpredictable). "Epiplexity" = **epi**stemic com**plexity**. Measured with neural nets in two ways:
prequential (area under the loss curve above the final loss, a heuristic) and requential (cumulative KL between a
teacher and a student trained on the teacher's samples, an explicit code, 2-10x slower). MDL picks a model for given
data; epiplexity is its dual: it picks data for a given compute budget.

## Three apparent paradoxes (§1, §5)

1. **Deterministic transformations can't add information.** (Data processing inequality; H(f(X)) ≤ H(X);
   K(f(x)) ≤ K(x) + K(f) + c.) And yet PRNGs, synthetic data, maths from axioms, emergent dynamics, AlphaZero.
   - Thm 12: a PRG G stretching k bits to n raises polynomial-time entropy by more than n − k − nε(k) − c.
   - Asymmetry: with bounded compute, a short program for f does not give one for f⁻¹ (unbounded: K(f⁻¹) = K(f) + O(1)).
     Guidance for synthetic data: use transformations without simple, efficient inverses.
   - Fig. 3: ECA rules iterated 48 times on 64 cells, predict Y = F(X) from random X, D = 100M tokens.
     Rule 15 (class II): little of either (low H_T, low S_T). Rule 30 (class III): high H_T, ~no S_T (loss makes no
     progress). Rule 54 (class IV): medium H_T, high S_T, loss keeps falling with compute.
2. **Information doesn't depend on factorization order.** H(X) + H(Y|X) = H(Y) + H(X|Y); the same for K up to O(log).
   And yet LLMs compress left-to-right English better than reversed text (an "arrow of time", Papadopoulos et al.
   2024), and cryptography relies on functions easy one way and hard the other.
   - Thm 13: for a one-way permutation f, X uniform, Y = f(X): H_poly(X|Y) + H_poly(Y) > H_poly(Y|X) + H_poly(X) + ω(log n).
     Corollary (Thm 26): no poly-time model that fits a one-way function's forward direction can satisfy Bayes' theorem.
   - Fig. 4a: rule 30, 8 steps, state size n, as a stand-in one-way function (believed one-way, not proven;
     unlike crypto OWFs, its forward pass can be written as a RASP-L program, App. D). Forward reaches the Shannon
     entropy; reverse keeps a gap.
   - Fig. 4b/c: Lichess games as moves-then-final-board (forward) or board-then-moves (reverse). Reverse has higher
     H_T and higher S_T as compute grows; the gap vanishes at small compute. The paper notes there is no clean
     polynomial vs non-polynomial separation here.
3. **Likelihood modeling is merely distribution matching.** argmin_P E_Q[−log P] = Q, so (the view goes) a model
   can't learn more than the generator holds. And yet:
   - **Induction.** Sutskever's murder mystery: predicting the culprit's name needs the deduction the author never
     had to make (the author picked the murderer first). Setup Y = (m(Z), f(Z)), m masks h bits.
     *Hard*: f = 4 steps of rule 30 on n = 32, first h bits hidden; loss converges to h bits but the compute needed
     grows exponentially in h (consistent with trying all 2^h candidates); measured epiplexity grows with h.
     *Easy*: random Markov chain over V = 8 symbols with h of its rows hidden ("removes h columns" in the text),
     sequences of 512; for 0 < h < 8 the model must both read the given rows and induct the hidden ones in context
     (statistical induction heads); epiplexity is highest for 0 < h < 8, above h = 0 and h = 8.
   - **Emergence.** Game of Life: an unbounded observer just simulates; a bounded one must learn "species" (blocks,
     oscillators, gliders, guns) and their collisions, a longer program. Def. 14 (epiplexity-emergent). The paper has
     NOT proven Life satisfies it. Fig. 6: ECA rule 54, non-looped vs looped transformer: at low compute the
     non-looped model's epiplexity rises with compute; past a threshold the looped model (which can unroll the
     rule step by step, like chain-of-thought) wins and MDL and epiplexity drop abruptly (brute force found).
   - Conjectured: no "limited epiplexity increase property", i.e. the MDL-optimal model can be unboundedly larger than
     the generating program.

## Other results and numbers

- Thm 9: for a CSPRNG, n − 2 − nε < H_poly(G(U_k)) ≤ n + c and S_poly ≤ c + nε. Shannon H(G(U_k)) = k; time-bounded K ≤ k + c.
- Thm 10: assuming one-way functions, there exist X_n with S_poly(X_n) = Ω(log n) (nonconstructive; modest growth).
- Uniform random bits: S_T ≤ a constant, H_T ≥ n. 0101…/1010… with prob ½ each: S_T = O(1), H_T = O(1).
- Basic properties: H(X) ≤ S_T + H_T ≤ n + c; more time never increases MDL_T.
- Sophistication (Koppel 1988) is the unbounded ancestor; Chaitin incompleteness: no proof any specific string has
  K(x) > L, where L is "often not more than a few thousand" bits, far from frontier-model sizes.
- Measuring time in FLOPs: training 6ND, evaluating on X 2ND; µP keeps hyperparameters stable across sizes.
- Fig. 2c: prequential estimates are typically several times larger than requential, but they correlate, best
  within a dataset group.
- §6.1 / Fig. 7: chess models pretrained in reverse order (higher epiplexity) do better downstream: puzzle accuracy
  about the same, centipawn evaluation clearly higher.
- §6.2 / Fig. 8a: requential, models up to 160M parameters, time bound 6×10¹⁸ FLOPs: OpenWebText has the most
  epiplexity, then chess; CIFAR-5M has the most total information but the least epiplexity (over 99% random).
  Epiplexity is a tiny fraction of total information in every case.
- §6.3 / Fig. 8b, 9: from published scaling laws L(N,D) = E + (N/N0)^−α + (D/D0)^−β, 1T tokens at 10²⁵ FLOPs
  (about Llama-3-70B's training compute): language has the highest epiplexity, images the least; VQ tokenization
  raises image epiplexity a lot; video has less than images at the same resolution (temporal redundancy).
  Asymptotically S_∞(X) = β/(1−β) · D0^β · D^(1−β): capped by dataset size, larger for smaller β and larger D0.
- §6.4 / Fig. 8c: ADO (Adaptive Data Optimization, Jiang et al. 2025, 1.3B params, 125B Pile tokens) picks subsets
  whose loss falls fastest; it ends with higher prequential epiplexity than natural sampling, and better downstream
  accuracy and OOD perplexity (SlimPajama, FineWeb). (Figure adapted from Jiang et al.; Yiding Jiang is an author
  of both papers.)
- The paper says repeatedly: epiplexity measures *how much* structure, not whether it is relevant to a given task;
  it is not a guarantee of OOD generalization.

## Accuracy notes

- **Fig. 8a: 1B or 5B tokens?** The caption says "1B OpenWebText, Chess, and CIFAR-5M tokens"; §6.2 says "5B tokens
  of data" and "at most 5B tokens". The bars support 5B: CIFAR-5M's total (2.33e10 bits) would be 23 bits per 8-bit
  grey pixel at 1B (impossible) but 4.7 at 5B; OWText would be 7.3 bits per character at 1B (more than log2 96).
  App. C.4 also says 5B. Treat the caption as a typo; say "5 billion tokens" if a number is needed.
- **Fig. 8b shows the infinite-compute limit, not 10²⁵ FLOPs.** Every Fig. 8b S_T bar equals Fig. 9's dashed S_∞
  × 1/ln 2 (within 0.1%), so Fig. 9's unlabelled y axis is in nats and Fig. 8b plots the limit; at 10²⁵ FLOPs Fig. 9's
  curves sit 3-12% below it. The ordering is unaffected. Don't say "at 10²⁵ FLOPs" next to Fig. 8b numbers.
- **Fig. 8c axes are truncated** (accuracy from 0.55, perplexity 1 from 12.0): the differences are small (accuracy
  0.590 vs 0.585; OOD perplexity 12.21 vs 12.25 and 14.97 vs 15.90). Draw from zero or say the gaps are small.
- **Fig. 4a:** forward sits 0.2-1.8 bits above the entropy line; the reverse gap grows with n (about 1.5 bits at
  n = 16 to 12-14 bits at n = 64) rather than staying fixed.
- Fig. 7 agrees with the text: puzzle accuracy 0.258 vs 0.260, centipawn 0.210 vs 0.283 (forward vs reverse).
- The repo README labels hard induction "Section 5.3.2" and emergence "Section 5.4"; the paper has them at 5.3.1 and
  5.3.2. Cite the paper's numbering.
- Easy induction: the text says m "removes h columns" but describes the model as "inducting on the missing rows".
  Say "hides part of the transition table".
- Prequential epiplexity is a heuristic (it relies on symmetry of information, which fails for time-bounded
  complexity); requential is the rigorous estimate. Say so whenever we show an area-under-the-curve picture.
- Rule 30 is *believed* one-way (Wolfram); not proven. Theorems 12-13 assume PRGs / one-way permutations exist.
- "Logical depth was later shown to be equivalent to sophistication through the busy beaver function" (§7): keep the
  paper's wording if used; don't overstate it as plain equivalence.

## Comparison material (our framing, labelled as background)

| measure | of what | observer | random string | PRNG output (k-bit seed → n bits) | rule 54 history / text |
|---|---|---|---|---|---|
| Shannon entropy H (1948) | a distribution | unbounded | n | k (only the seed is random) | ≤ entropy of the initial row |
| Kolmogorov K (1960s) | one string | unbounded, incomputable | ≈ n | ≈ k + small | ≤ initial row + rule |
| sophistication / effective complexity | one string | unbounded | ≈ 0 | small | unbounded compute erases it |
| logical depth (Bennett 1988) | one string | runtime of near-shortest program | ≈ 0 | modest (poly time) | large if no shortcut |
| time-bounded entropy H_T | a distribution | time T | ≈ n | ≈ n (looks random) | medium |
| epiplexity S_T | a distribution | time T | ≈ 0 | ≈ 0 | high |

Background facts safe to state: Shannon 1948 "A Mathematical Theory of Communication" (and his line that the
semantic aspects of communication "are irrelevant to the engineering problem"); Solomonoff 1964, Kolmogorov 1965,
Chaitin 1966/1969 (algorithmic complexity); Martin-Löf 1966; Blum-Micali 1982 and Yao 1982 (pseudorandomness, next-bit
test); Koppel 1988 (sophistication); Bennett 1988 (logical depth); Gell-Mann & Lloyd 1996 (effective complexity);
Grassberger 1986 / Crutchfield-Packard 1983 (excess entropy, the stationary-process cousin of the prequential area);
Shalizi & Crutchfield 2001 (statistical complexity); Xu et al. 2020, ICLR, "A Theory of Usable Information under
Computational Constraints" (V-information: bounds inference only, measures the random part); Rissanen 1978 (MDL);
von Neumann 1951 quote "Anyone who considers arithmetical methods of producing random digits is, of course, in a
state of sin." (quoted in the paper); Anderson 1972 "More is different" (quoted in the paper).

## Our laptop runs (lab/eca_lab.py)

A 4-layer, d=128 transformer (~0.8M params) trained online on fresh ECA samples on Apple MPS; prequential area above
the final loss. A miniature cousin of Figs. 3 and 4a, NOT the paper's result: always label "our run". 32-cell rows,
batch 128, 4,000 steps (~2 min per rule), predicting the row after k steps from a random row (bits per 32-bit row):

| source | k = 8: final / area | k = 16: final / area |
|---|---|---|
| rule 15 | 0.000 / 3.9e6 | 0.000 / 4.0e6 |
| rule 30 | 32.00 / 8.5e3 | 32.00 / 8.6e3 |
| rule 54 | 25.4 / 8.5e5 | 23.1 / 9.9e5 (still falling) |
| rule 110 | 28.7 / 5.0e5 | 27.8 / 6.0e5 |
| coin flips (control) | 32.00 / 9.0e3 | 32.00 / 9.0e3 |

Robust: rule 30 is indistinguishable from coin flips to this observer (no progress, ~zero area). Rule 15 becomes
perfectly predictable. Rules 54 and 110 are partly learned and still improving. NOT robust: at 4,000 steps rule 15's
area is larger than rule 54's (rule 15 takes ~1,800 steps to learn; 54 is unfinished), unlike Fig. 3; a 20,000-step
run (`ours_rules_n32_k16_s20000.json`) checks whether 54 keeps accumulating. **It does:** at k = 16 and 20,000 steps,
rule 15 ends at 0.000 bits with area 3.9e6 (unchanged), rule 30 at 32.00 / 1.2e4, and rule 54 at 17.4 bits with area
9.1e6, more than twice rule 15's (the k = 8 rule 15 hits < 0.01 bits at step ~1,690). Rule 110 ends at 27.1 bits /
area 1.9e6 and the coin control at 32.00 / 1.3e4 (finished later; videos/counting shows all five). The paper's Fig. 3 frontier also
has rule 15 above rule 54 at its smallest budgets (S_T 1.15e6 vs 3.5e5 at 3.5e12 FLOPs) before 54 pulls ahead; that is
how videos/epiplexity presents it. `ours_order_k8_s4000.json` (rule 30, X then Y vs Y then X, n = 8-24) did NOT work:
both directions reach the entropy only at n = 8 and sit at the 2n random-guess level from n = 12 on (the model never
learned the forward map), so it says nothing about Fig. 4a; don't show it. Our compressor check
(`ours_compress.json`, 2^20 bits each; bits per bit, gzip / xz): zeros 0.001 / 0.001; coin 1.000 / 1.000; SHA-256
PRNG 1.000 / 1.000; rule 15 0.032 / 0.017; rule 30 1.000 / 1.000; rule 54 0.62 / 0.47; rule 110 0.37 / 0.28.

## Extracted figure data (data/, from extract_paper.py; all checked against 400-dpi renders)

`fig2c_preq_req.json`, `fig3_eca.json`, `fig4_owf_chess.json`, `fig5_induction.json`, `fig6_emergence.json`,
`fig7_chess_ood.json`, `fig8_natural.json`, `fig9_scaling.json`: each has `source`, units and `note`. Key values:
- Fig. 3 final (bits): rule 15 total 2.16e5 (S_T 2.15e5, peak 1.15e6 early; H_T ≈ 0); rule 30 total 1.00e8 (S_T
  ≈ 1.9e4, H_T 1.00e8); rule 54 total 1.92e7 (S_T 5.41e6, H_T 1.38e7). Compute 1e12-1.7e17 FLOPs.
- Fig. 4a (bits per pair, n = 16, 24, 32, 48, 64): forward 16.2, 24.3, 32.9, 49.7, 65.8; reverse 17.5, 32.6, 41.4,
  61.0, 78.0; entropy n; random guess 2n. Fig. 4c final: H_T fwd 3.42e9 / rev 3.94e9; S_T fwd 2.385e8 / rev 2.796e8.
- Fig. 5b epiplexity for h = 0..5: 2.43, 2.93, 3.27, 3.99, 4.25, 5.56 (×1e6 bits). Fig. 5c for h = 0, 2, 4, 6, 8:
  0.95, 2.72, 3.96, 4.68, 3.20 (×1e6).
- Fig. 6: non-looped S_T peaks 1.456e7 at 7.05e14 FLOPs; the looped model takes over at 1.75e15 FLOPs, where the
  two-part code drops 2.01e8 → 2.50e7; final S_T 5.43e6.
- Fig. 8a (bits) S_T / total: OWText 3.01e8 / 7.29e9; Chess (R) 2.80e8 / 4.22e9; Chess 2.05e8 / 3.67e9; CIFAR-5M
  9.25e7 / 2.33e10 (CIFAR: S_T is 0.4% of total). Fig. 8b S_T / total: Language 9.0e10 / 2.76e12; Img VQ 32² 1.39e10;
  Img VQ 16² 1.37e10; Vid VQ 16³ 7.49e9; Img 32² 5.02e9; Img 16² 3.15e9; Img 8² 1.32e9 (see accuracy note).
- Fig. 8c ADO vs Natural: epiplexity 2.46e10 vs 1.94e10 bits.

## What Whisper mishears here

With `bella-nicole` at speed 0.92 and `PACE` (each sentence is checked on its own, so one wrong word in a sentence
under nine words is flagged):
- pods/episode: "prequential" is heard "frequential" (SAY `pree-quential` fixes it). "Kolmogorov" is heard
  "Kalmogorov"; SAY `Kol-mo-gorov` passes in long sentences but gave "call Mo Gaurav" / "Kolmo Gaurav" in short ones
  (those lines now say "the other classic theory"). "AlphaZero" sometimes comes back "Alpha Zero" (two words: keep it in
  long sentences). "pseudorandom" opening a short sentence is written "pseudorandum". "fair coin flips" became
  "Faircoin flips". "datasets" is written "data sets" (two words each: say "kinds of data", "collection").
  "Sutskever" is "Sutskiver", "Micali" "Macaulay", "Rissanen" "Rissinen", "ADO" "Adu", "trained network" "train network"
  (all pass, one word off in a long sentence). British "neighbours", "colour" come back American (now spelled American).
- Kept off air because of probes: "Martin-Löf" ("Martinlurff", two words off), "Qiu" ("Kyu", "Chiou", "I.Q."),
  "Izmailov" ("Ismailov"), "Kolter" ("Coulter"), "Marc" ("Mark"), "Llama" ("Lama"), "centipawn" ("sent-upon"), and
  "CIFAR five M" (written "CIFAR-5M", which the checker reads as one word). They are named in the show notes instead.
- Numbers and years pass when the script writes years as digits ("1948") and other numbers in words: Whisper's
  digits are spelled out before comparing. "ninety-nine times out of a hundred" comes back "99 times out of 100"
  (passes, one word off).
- videos/counting (`am_michael`, speed 1.0, whole lines checked): a lone number word opening a short line fails ("One:
  all zeros." came back "1 of 0s"; now "The first: all zeros."). "fair coin flips" became "fare coin flips" ("fair"
  dropped). "Pseudorandom:" opening a short sentence came back "Sudorandum" (now "The pseudorandom file"), and
  "Pseudoentropy" is written "pseudo entropy" (two words, flagged; now "measures from cryptography"). "Kolmogorov" with
  SAY `Kol-mo-gorov` is "Kalmogorov" (passes in long lines) but "Shannon and Kolmogorov keep..." gave "Karl Mogorov"
  (flagged; now "the classical measures"). The author list flagged (Qiu "Kiu", Izmailov "Ismailov", Kolter "Coulter"):
  narration says "Finzi and colleagues", the names are on screen. Pass, one word off: "Koppel's" → "Kapel's", "Gell-Mann"
  → "Gelman", "Chaitin" → "Chaitan", "Micali" → "McCauley", "Solomonoff" → "Solomonov", "Martin-Löf" (SAY `Martin Luff`)
  → "Martin Luff", and homophones "rows" → "rose", "too" → "two", "Right" → "Write", "Zeros: no" → "Zeros know".
- videos/epiplexity (`bella-nicole`, speed 1.0, whole lines checked at 12%): the full author list flagged ("Marc" →
  "Mark", Qiu → "Chiu" / "Chu" / "Chayu" even with SAY `Chyoo`, Izmailov → "Ismolov", Kolter → "Coulter", and once
  Yiding → "Yitting"); the title line names Finzi, Qiu and Jiang "and their colleagues" in 18 words, so the two
  unavoidable misses (Mark, Chayu) stay under the limit. "ADO" with SAY `A D O` came back "a DO" (now "Adaptive Data
  Optimization"). "web text holds the most structure, then chess" came back "webtext ... than chess" (now "text from
  the web ..., and chess comes next"). "Pseudorandom bits?" opening a line was written "Pseudo-random bits" (two words;
  now "And the generator's output?"). Pass, one word off: "Sutskever's" → "Sutsgever's"; "TPU hours" passes.
- shorts/* (`bella-nicole` and `am_michael`, speed 1.0, whole lines): "predict each one forty-eight steps ahead" came
  back "each 148" (passed at 0.08; now "look forty-eight steps ahead, for each rule"). "Can the order you read
  something in change..." was heard "...something and change" and "change what you learn from it" as "what you
  learned" (both passed narrowly; now "Can reading things in a different order change what you learn?"). Pass, one
  word off: "seven bytes" → "seven bites" (captions use the script, so they still say bytes). Numbers come back as
  digits and pass ("fifty-six bits" → "56 bits", "ninety-nine percent" → "99%"); "from zero hidden bits" is written
  "from zero, hidden bits" (passes). "epiplexity" with SAY `eppiplexity` passes in a medium line. All five end with
  0 flagged.

### Rule 30 forward vs reverse, k = 3 (our run, `ours_order_k3_s8000*.json`, added after the pieces were built)

With 3 automaton steps instead of 8 the small model can learn the forward map, and the paper's Fig. 4a pattern shows
up in miniature (bits per (X, Y) pair; entropy = n; 8,000 steps): n = 8: forward 8.08 / reverse 8.11; n = 12: 12.13 /
16.52; n = 16: 16.15 / 24.25; n = 24: 24.78 / 30.67. Forward reaches the entropy, reverse keeps a 4-8 bit gap. BUT at
n = 20 the forward run failed to train on two seeds (33.3 and 31.1 bits; reverse 32.6 and 26.0), so the sweep is
suggestive, not clean, and k = 3 is far easier than the paper's 8 steps. None of the built pieces use it; if a future
piece does, show n = 20 too and label it "our run".
