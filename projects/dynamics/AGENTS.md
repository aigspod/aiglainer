# dynamics

*A Mechanistic Analysis of Transformers for Dynamical Systems*, Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G.
Kevrekidis, Eleni Chatzi (ETH Zürich, Johns Hopkins, Singapore-ETH Centre). arXiv:2512.21113v2, 5 Aug 2026.
[arxiv.org/abs/2512.21113](https://arxiv.org/abs/2512.21113). Journal club Nov 11, 2026; feed episode 28. These are
unofficial, not produced by the authors. Layout and commit rules: [../AGENTS.md](../AGENTS.md).

| kind | what |
|---|---|
| [videos/](videos/AGENTS.md) | three standalone explainers and a six-minute cut |
| [shorts/](shorts/AGENTS.md) | six shorts of about 40 s |
| [pods/](pods/AGENTS.md) | the 21-minute episode |

## The paper in one breath

A single-layer, mostly single-head transformer, studied as a dynamical-systems object. **Linear systems (§3):** attention
is a data-adaptive autoregressive (AR) model whose lag weights are softmax weights: positive, summing to one, times one
shared output matrix (Eq. 17-18). So one head can't make mixed-sign AR coefficients: it oversmooths. **Nonlinear systems
(§4):** attention acts as an adaptive delay embedding (Takens), helping only under partial observation; the latent
dimension must be big enough to unfold the reconstructed geometry; parameters (Reynolds number) may need to be inputs.

## Numbers you may use (with where they come from)

- §3.1 SDOF: m = 1 kg, c = 0.5 Ns/m, sampled at 25 Hz (Δt = 0.04 s), only displacement observed, AR(2) target.
  Case 1: k = 2000 N/m, f_n ≈ 7.12 Hz, AR coefficients a1 = −0.4352, a2 = −0.9802 (same sign: works, needs w_o < 0).
  Case 2: k = 500 N/m, f_n ≈ 3.56 Hz, a1 > 0, a2 < 0 (mixed: fails; oversmoothed, no resonance peak, Fig. 2b).
  The paper gives no numbers for Case 2's coefficients. Our computation from Eq. 20: a1 ≈ +1.24, a2 ≈ −0.98 (label "our calculation").
- App. A.1: two heads fix Case 2; learned W_O = [1.087, −1.244] (opposite signs).
- §3.2 2-DOF: m1 = m2 = 1, c = 0.5, k1 = 1000, k2 = 1500. Full obs, n = 3 tokens: both modes. Partial (x1 only), n = 3:
  fails. Partial, n = 4: both modes back. Attention flips between lags when it fails, steadier when it works (Fig. 3b).
- §4.1 Van der Pol: µ = 0.5, Δt = 0.1, 1500 initial conditions in U(−3,3)², trajectories over [0, 6.5], n = 5 tokens.
  Full observation: MLP and transformers both MSE ~1e-7. Partial (x only), Table 1: MLP only 2.485e-2; attn 1D no PE
  1.789e-3; attn 2D no PE 1.770e-3; attn 1D PE 5.848e-4; attn 2D PE 2.065e-5; polynomial NARX 2.192e-3.
  (MLP / best ≈ 1200×; NARX / best ≈ 106×; 2D no-PE / 2D PE ≈ 86×.) 10 seeds each.
  Without PE attention is ~uniform averaging over the window; with PE, lag-specific weights. The 2D latent "recovers a limit-cycle structure" (a loop shaped like the cycle, not the cycle itself).
- §4.2 Chafee-Infante: u_t = u − u³ + ν u_xx, ν = 0.16, u = 0 at x = 0 and π; long-term dynamics on a 2-D inertial
  manifold. One sensor: u at the 10th of 256 grid points (x ≈ 0.11). n = 5. d_lat = 2: collapses to a thick curve,
  unstable across seeds (some worse than the MLP). d_lat = 3: unfolds; Fourier modes readable from the latent. The
  manifold's symmetry about the origin folds the single-sensor delay view (App. A.4). PE: no systematic improvement.
- §4.3 Cylinder flow: Re ∈ [100, 750] (Geneva & Zabaras data), train Re ∈ [125, 725], test {133,233,333,433,533,633}
  plus out-of-distribution {100, 733, 750}. One sensor: v_x at (x = 35, y = 45). d_lat = 3, 5-7 tokens. Largest
  one-step MAE ≈ 2.3e-2. Without Re: latent loops overlap, errors rise at the range edges. With Re: separated, ordered,
  uniform errors. Full-field reconstruction (Geometric Harmonics, 5-fold CV): with Re 1.12e-4 (wake 2.48e-4); without
  Re 7.45e-3 (wake 1.33e-2): ~70× worse overall, ~50× in the wake (66.5× and 53.6× exactly).
- Key line (§5.1): one-step prediction accuracy and latent-state identifiability are not equivalent.

## Accuracy notes: where the paper and its own numbers disagree

- **2-DOF frequencies.** The paper says the analytic modes are f1 ≈ 4.1 Hz and f2 ≈ 9.5 Hz. From its stated parameters
  (M = I, K = [[2500, −1500], [−1500, 1500]]) we get **3.26 and 9.52 Hz**. Don't present 4.1 Hz as the analytic value;
  say the paper reports peaks at 4.1 and 9.5 Hz and that the listed parameters give about 3.3 and 9.5.
- **Positional encoding (Van der Pol).** §4.1 says PE reshapes attention "without systematically improving prediction
  accuracy", but Table 1 shows 2D+PE ≈ 86× better than 2D without PE under partial observation, and §5.2 says PE
  "yields a measurable improvement for the Van der Pol example". Follow the table; say the text disagrees.
- **Cross-validation spread.** A.5 says the fold-to-fold spread is "two orders of magnitude smaller" than the gap; it is
  about 13× (one order).
- **Takens.** §5.1 says the experiments "confirm" n ≥ 2d_A + 1 is sufficient. The paper only claims sufficiency (the
  bound is a sufficient condition), so the objection is to "confirm": an experiment can't confirm a theorem. Say
  "consistent with". Too little history is tested (§3.2, one sensor and three steps fails), and for the cylinder
  (§4.3, d_A ≤ 3 so the bound asks for 7) five to seven tokens already work: five and six are below the bound.
- Case 1's a1: we compute −0.428 from Eq. 20; the paper says −0.4352. Minor; use the paper's.

## Our extrapolation (label it on screen and on air)

Links to ML climate emulators (SamudrACE, ACE): forcing (CO₂, SSTs) plays the Reynolds number's role; most emulators
step from the current state alone, fine only if the state is complete (deep ocean, soil are hidden); one-step skill
doesn't prove a sound internal state (check spectra, modes, long-run statistics); emulator smoothing resembles the sign
problem but mostly comes from training loss, not softmax.

## Simulations

Paper figures are raster images, not vector data. Charts are typed from the tables above, or simulated from the
paper's stated equations (SDOF, 2-DOF, Van der Pol) and labelled "simulated from the paper's equations". Never trace
the paper's figures by eye, and never present a simulation of ours as the paper's trained-model result.

## What Whisper mishears here

- videos/sign: "a head" heard as "ahead" (say "one head"); "oversmoothed" written as "over-smoothed" (say "too smooth"). Numbers come back as digits ("7.1 Hz" for "seven point one hertz"), which passes. "no peak" can come back "no peek" (passes, one word off in a long line).
- pods/episode: "three and a half hertz" is written "3.5 hertz" (flagged in a test; say "three and a half times a
  second"). "Van der Pol" comes back as "Van Der Paul" (one word; keep it in long lines). "Chafee-Infante" becomes
  "Chaffee and Fant" without a respelling, "Chaffey-Infante" with SAY "Chay-fee In-fahn-tay". "Takens'" is written
  "Taken's" or "takin's" (passes). "Singapore-ETH Centre" comes back "Singapore ETH Center". "trained networks" was
  heard as "train networks", "a head is" as "ahead is" (say "one head"), "take in a step" as "taken a step", "sea
  surface" as "see surface". "feed-forward" is written "feedforward", and "after attention" became "after a tension"
  (avoid both). "plain MLP" can become "plane MLP".
- videos/hidden: "two d plus one" is written "2D plus 1" (flagged: the checker reads "2d" as one word; say "twice d,
  plus one"). "twelve hundred times" is written "1,200 times" (flagged: say "three orders of magnitude"); "fifteen
  hundred" comes back "1,500" (passed narrowly; dropped from speech). "attention weights" was heard as "attention
  waits" (avoid "weights" after a pause). "Van der Pol" again "Van Der Paul" (passes in a long line). "at steps of one tenth" comes back "1 tenth" (passes).
- videos/unfold: "very different insides" was heard "in sides" (say "on the inside"). A curly "paper’s" was read
  "paper S" (rephrase without the possessive). "SamudrACE" comes back "Samadra ACE" (SAY "Samudrace" gives
  "Samadrace", one word off: keep it in a line of 12+ words). "Attention" opening a line was heard "A tension" (start
  with "Then attention"). "Chafee-Infante" is written "Chaffee-Infante" (one word off: keep the line long). "one in ten
  thousand" is written "1 in 10,000" (passes, one word off); its replacement "one ten-thousandth" comes back "one ten
  thousandth" (passes).
- shorts/reynolds: "Its runs separate" was heard "It runs separate" (passed, one word off; now "and the runs
  separate"). shorts/updown: "it's at one" comes back "at 1" (passes). The shorts say "an oscillator" and "a rod"
  and leave "Van der Pol" and "Chafee-Infante" on screen only, which keeps short lines safe.
- shorts/twoheads, average, sensor: nothing flagged. "one point zero eight seven" and "minus one point two four four"
  come back as "1.087" and "minus 1.244" (pass). Bella's "softmax: positive, adding up to one" loses the colon
  (passes). Short lines with "one head" stayed clear of "ahead".
- videos/distilled (Michael): "the paper takes d as two" came back "Diaz II" (flagged: say "the dimension as two"). "ACE and SamudrACE learn to step" came back "Samadres learned" (flagged: "such as ACE and SamudrACE step a whole climate state forward in time, again and again" passes, one word off). "trained head" is heard "train head" and "one-step errors" "one-step arrows" (both pass, one word off); "a plain network" again "a plane network" (passes).
