# weatherdreamer

*WeatherDreamer: Learning a World Model from Multimodal Earth Observations*, Kate Duffy, Elise Penn, Tristan
Ballard, August Posch, Thomas J. Vandal (Zeus AI, Inc., Cambridge, Massachusetts). arXiv:2611.18393v1 [cs.LG],
13 Nov 2026. [arxiv.org/abs/2611.18393](https://arxiv.org/abs/2611.18393). No code release is mentioned. These pieces
are unofficial and not made by the authors. Layout and commit rules are in [../AGENTS.md](../AGENTS.md).

**Like epiplexity, an aigs pod extra** (Nov 2026; the owner asked for "an episode like we did for epiplexity"): no
"/mull/", "journal club", "before the meeting" or "see you at the desk" in HUDs, cards, endings, descriptions or
narration. HUD `weatherdreamer  ·  an explainer`. End on questions "to think about". If the owner later says it is
a journal-club paper, only the HUDs, end cards and descriptions need changing. House audio: `duck_db` 8-10,
`duck_ramp` about 1.2, a 1.5-2.5 s fade at the end; podcasts use the paced settings (docs/PODCAST.md).

| kind | what |
|---|---|
| `videos/` | two ~10-minute explainers with different angles: `loop` (the predict-correct cycle learned with no answer key) and `trust` (a detective story: what the black box learned to trust, and what is in its memory) |
| `pods/` | `episode`, a single-host episode (feed episode 30) |
| [shorts/](shorts/AGENTS.md) | five 9:16 shorts (`now`, `stripes`, `trust`, `limb`, `walls`), native scenes in `shorts/wdshorts.py` on `loopkit.py` |
| `data/figs/` | the paper's figures as PNGs (`extract_paper.py`; not in git). Every figure is a raster image: show crops labelled "Fig. N", never redraw |

## The paper in one breath

Machine-learning weather models now rival operational forecasts, but they all start from an *analysis* (the best
estimate of the current atmosphere) made by a separate, expensive, physics-based data assimilation (DA) system,
which for global models runs every 6 h and arrives hours late. WeatherDreamer learns the whole DA cycle end to end
from 18 observing systems, with **no reanalysis** in training or inference: a Dreamer-style recurrent state-space
model (Hafner et al.) on a HEALPix grid of about 50 km (Nside 128). Each hour it **predicts** (memory h_t ∈ R^512 per
node, updated by a graph GRU; prior ẑ_t ∈ R^64 = the background) and **corrects** (posterior z_t from attention over
nearby observation tokens, conditioned on h_t = the analysis; the posterior network replaces the Kalman gain and its
prescribed B and R). Decoders (local implicit functions) play the observation operator H and can be queried at any
location, time, level and viewing angle.

## Numbers (section / table noted; all checked against the text)

- **Data (§2, Table 1):** 18 observing systems and two derived gridded products (IMERG precip, NSRDB irradiance).
  Geostationary IR (GOES-16/19, GOES-18, GK2A, Meteosat SEVIRI), microwave sounders (ATMS on NOAA-20 and S-NPP,
  AMSU-A on MetOp-B/C), HIRS/4 IR, ASCAT ocean winds, GPS radio occultation, CloudSat/CALIPSO cloud tops, ~11,000
  ISD surface stations (11,065), radiosondes (~650 soundings at each of 00 and 12 UTC). CloudSat, IMERG and NSRDB
  are always withheld as inputs at inference. CloudSat covers only 2020 of training. Forcing: solar geometry,
  clear-sky irradiance, elevation.
- **Model (§3):** 50 M trainable parameters + 99 M frozen tokenizer parameters (spherical VAEs for the geostationary
  imagers only). Patches of 32 × 32 latent nodes (≈ 1,600 km). Graph GRU: 4 rounds of message passing over 8
  neighbours, "up to about 200 km per hour". Observation step: k = 16 nearest tokens per modality, one shared
  softmax so modalities compete; a learned "no observation" embedding. Viewing angle enters as excess air mass
  ℓ = sec θ − 1 (zero at nadir) in encoders and FiLM-conditioned decoders.
- **Training (§3.7, S5):** 2020-2023, from scratch, one joint phase. Three losses: reconstruction (weights 1 / 2 / 3
  for seen / block-masked / modality-masked targets), prior matching ||ẑ − sg(z)||² ("the prior can match the
  posterior only by anticipating the observations about to arrive"), and a rollout loss: almost-fair CRPS over 6
  (then 12) steps with 2 members. Masking: whole observing systems (p = 0.5), a spatial block (p = 0.5), 5-30 % of
  stations. 70,000 steps on 4 NVIDIA GH200 GPUs; CloudSat head fine-tuned afterwards with everything else frozen.
- **Inference:** memory and latent start at **zero**; 12 h of assimilation (13 steps) then the forecast. 8 perturbed
  members + 1 control (AR(1) correlated noise, ρ = 0.9, via FiLM). Patches tiled at 50 % overlap, each with its own
  memory, blended with a Hann window. **Continuous cycling is left to future work.** One global hourly step ≈ 1.5 min
  on one H100 (≈ 45 s model, ≈ 45 s reading observations); 12 h, 8 + 1 member forecast ≈ 11 min.
- **Evaluation sets (S6.1-2):** Set A, 50 initializations Aug 2024-Aug 2025, *with operational latency*: WD withholds
  polar sounders, ASCAT and RO for the final 2 h and radiosondes for 4 h; baselines use the newest cycle that would
  have been out: GFS ≥ 4 h old, GEFS ≥ 5 h, IFS ENS ≥ 7 h, HRRR 2 h. Set B, 30 GSI cycles Jan-Oct 2024, no latency,
  forecasts at matched 3-9 h leads, decoded at each observation's viewing geometry.
- **Surface (§4.1, Fig. 4; 534 held-out ISD stations = 5 %):** CRPS beats GEFS for T2m, dew point and wind at every
  lead to 12 h. Wind is best of the three at every lead: 1.09 vs 1.31 (GEFS) vs 1.15 m/s (IFS ENS), mean of 1-12 h.
  T2m best for the first 8 h, then IFS ENS (WD's CRPS grows with lead, the operational ones stay flat). Dew point:
  beats IFS ENS only for 2 h (1.29 vs 1.35 K at +1 h); beats GEFS 1.51 vs 1.79 K. Ensemble-mean MAE: closer; beats
  IFS ENS only for temperature over the first 3 h ("its lead in CRPS comes largely from its ensemble spread").
  Analysis T2m MAE at unseen stations 1.60 vs 1.95 (GEFS) and 1.72 K (IFS). Spread-skill 0.63-0.78 vs 0.23-0.47
  (GEFS) and 0.26-0.41 (IFS) (all under-dispersive). No station input at all: CRPS +10 % wind, +17 % T, +24 % dew
  point, +76 % SLP; still beats GEFS for T2m to 11 h and wind at every lead; IFS better for all four. SLP is "the
  clear weakness": correlation of forecast vs observed 6-12 h pressure change ≈ 0.45 vs 0.6-0.9; in Fig. 4d WD's SLP
  CRPS sits far above both operational ensembles at every lead (read the figure crop; don't quote a number). Biases:
  T −0.11 to +0.09 K vs −0.25 to −0.36 K for the operational ensembles.
- **Inferred, never inputs at inference (§4.2):** *Precipitation* (vs IMERG): best ensemble through +6 h (fair CRPS
  0.255 vs 0.310 IFS ENS vs 0.331 GEFS at +3 h); behind IFS by +9 h and both by +12 h; at a forecast 50 %, rain
  observed 40 % (vs 31 % IFS ENS, 28 % GEFS); ETS ≥ 5 mm/h 0.22 vs 0.10 for GFS at +1 h; **too dry** (mean rate about
  two-thirds of IMERG at every lead, already at the analysis) and **too smooth** (sub-1000 km power 33 % vs 56-57 %).
  *Irradiance* (116 USCRN + 7 SOLRAD): analysis r 0.96, RMSE 86 W/m² vs 0.91-0.93 and 109-122; CRPS 16-22 W/m²
  better than HRRR at every lead; IFS ENS best from +6 h. *Cloud-top height* vs EarthCARE (never seen in training;
  28 analyses, 154,860 cloudy footprints): r 0.73 / RMSE 4.4 km vs 0.70 / 4.8 km for GOES ACHA; detection ETS 0.39
  vs 0.28, POD 0.80 vs 0.90, false-alarm ratio 0.09 vs 0.19 (half); both biased low (2.4 / 2.8 km).
- **Window length (§4.3.1, Fig. S6):** 1 h of assimilation vs 12 h: CRPS +15 % for 925 hPa radiosonde T, +8-16 % for
  winds; most of the gain within the first 3-6 h; spread shrinks with the window for T and dew point.
- **vs GSI first guess (§4.3.2, Table 2, SD of O−F, GSI / WD / ratio):** ATMS window 5.06 / 5.35 / 1.06; tropo T
  0.38 / 0.67 / 1.76 (per-channel 1.35-4.55); strato T 0.53 / 0.98 / 1.84; water vapour 3.39 / 3.54 / 1.04; HIRS T
  4.49 / 3.87 / 0.86; HIRS WV+window 6.83 / 6.14 / 0.90; GPS-RO 5-30 km 4.96 / 5.69 % / 1.15; radiosonde T 1.38 / 2.47
  / 1.79; radiosonde q 1.06 / 1.38 / 1.30; **radiosonde wind 3.01 / 7.89 m/s / 2.62** (1.6-1.7 at 925-850 hPa, 3.2-3.5
  at 300-200 hPa); held-out surface T 2.37 / 2.47 / 1.04, q 1.37 / 1.39 / 1.02, wind 2.05 / 2.22 / 1.08; ASCAT 1.31 /
  2.16 / 1.65. WD's sounding-channel biases are small (|b| ≤ 0.18 K) where GSI's uncorrected ones reach −0.9 K; WD's
  surface T bias −0.28 K vs GSI +1.51 K. Clear-sky geostationary 10.3 µm: 5.0 vs 0.7 K (WD puts cloud where it's
  clear); all-sky one case vs GFS simulated imagery: 9.9 vs 11.6 K. GSI uses a far larger observing system
  (aircraft, satellite winds, hyperspectral IR, more RO) and decades of work; WD is scored as an ensemble mean
  (an advantage the paper notes).
- **Learned weighting (§4.3.3, Fig. 8):** Desroziers σ_O for clear-sky ATMS temperature channels 0.2-0.4 K, at the
  on-orbit instrument noise; ASCAT close to the triple-collocation error. Gain vs Hollingsworth-Lönnberg optimum:
  near optimal for water vapour and IR; **too timid** for microwave temperature sounding (k ≈ 0.64 vs k_opt ≈ 0.82);
  **too trusting** for ASCAT (≈ 0.9 vs 0.8; ignores representativeness error). Stations correct the state mainly
  within ~200 km; station wind barely spreads. Radiosonde T and wind gains fall to 0.1-0.26 at 100-300 hPa; **near
  zero for radio occultation**. The paper ties this under-use to its upper-air gap.
- **Viewing angle (§4.4, Figs. 9, S7):** decoding at nadir recovers 83-96 % of observed limb darkening (collocated
  GOES-East/West, ≤ ~2.5 K off at the limb). Near 80°: 11.2 µm window ≈ 6 K, 6.9 µm water vapour 14 K, 13.3 µm CO₂
  16 K, 9.6 µm ozone 22 K. Scene dependence at 11.2 µm, 70-78°: ≈ 3.5 K over the coldest scenes, ≈ 15 K near 250 K.
  ATMS crossovers: 13.6 K per unit secant (ch 7) and 6.1 K (ch 20); the observed-angle decode reproduces them, the
  nadir decode gives 0.3 and 0.1 K. vs GPM MergIR: observed-angle decode bias −3.2 K (−7.8 beyond 60°), nadir decode
  0.0 K (−1.1). Radiometric only: parallax of high cloud remains.
- **Fig. S3:** the 512-wide memory h carries forcing (solar terminator, land-sea), weather, **and a record of the
  observing system: geostationary disk footprints and polar-orbiter swaths**, "analogous to the observation-density
  information a conventional filter carries in its error covariance". The 64-wide latent z is "dominated by
  meteorological structure with a weak residual imprint at coverage boundaries".
- **Conflict of interest:** all authors are employees of Zeus AI, which develops WeatherDreamer and may sell it.
  Funding: DOE Office of Science BER, ONR, NASA; compute at NERSC and NASA NCCS.

## Accuracy notes

- **"Up to five times" (abstract) vs Table 2.** The abstract says temperature-sounding departures are "up to five
  times larger"; the largest per-channel ratio in the text and Table 2 is 4.6 (ATMS ch 7-12: 2.7-4.6; Table 2 range
  up to 4.55). Say "up to about four and a half times".
- **Radiosonde winds are 2.62 × GSI averaged over 1000-100 hPa;** the ratio is 1.6-1.7 low down and 3.2-3.5 at 300-200
  hPa. Don't call 2.62 "the upper-air wind ratio".
- **HIRS is the exception aloft:** WD fits HIRS better than GSI's background (0.86-0.90), on all-sky observations GSI
  mostly doesn't assimilate. Don't say WD is worse "for every upper-air observation".
- **Latency:** Set A compares WD's hourly analysis with baselines that are 4-7 h older. That is fair for usefulness,
  not for the quality of the dynamics: IFS ENS overtakes WD's T2m at ~+8 h even though its forecast is then 15+ h old.
- **Independence:** IMERG is built partly from ATMS and geostationary IR, which WD ingests; ACHA cloud tops come from
  the same GOES radiances; NSRDB irradiance is itself derived from GOES imagery (background fact, not in the paper).
  The fully independent references are EarthCARE (cloud tops) and the USCRN / SOLRAD ground stations (sunlight). "Inferred" means learned retrieval from related radiances, not
  clairvoyance.
- **Held-out stations** are a random 5 %; many have assimilated neighbours, and the benefit vanishes beyond ~200 km.
  GEFS and IFS are interpolated to stations **without a lapse-rate (elevation) adjustment** (S6.4), while WD's station
  decoder is conditioned on elevation; our reading: this favours WD at mountain stations. Say "our reading".
- **"Recursive" in practice:** every reported run starts from a zero state with a 12 h window. The recursion is real
  but its memory never exceeds 12 h in any result, so it is tested only as well as a 12 h window model is.
- **Two causes of the upper-air gap, both in the paper (§5):** the update draws little from upper-air observations,
  and the dynamics run on ~1,600 km patches that can't hold the large, slow circulation. Name both.
- **Our arithmetic (label it):** a 50 m/s upper-level wind is 180 km/h and crosses a 1,600 km patch in about 9 h; a
  5-10 m/s surface wind moves 200-430 km in 12 h. Each patch keeps its own memory, so what blows in from beyond the
  patch edge is unseen.

## A reader's review, checked (Nov 17, 2026)

The owner shared an AI-written review before production. Checked line by line against the paper:
- **Right:** the framing (one learned system for DA and forecasting, no reanalysis), the architecture table, the
  h/z equations, the three losses and masking, the results table (wind, T2m crossover at ~8 h, precipitation dry and
  smooth, upper air worse), 1.5 min / 11 min, radiosonde wind 7.89 vs 3.01 (2.62×), the 1,600 km patches, the
  Desroziers caveat (matching statistics ≠ optimal filtering), the limb correction, all four reservations, and the
  IMERG caveat. Bottom line (the contribution is the learned observation-native cycle, not the architecture) agreed.
- **Incomplete or off:** (1) it blames the upper-air gap on the dynamics alone; the paper's own gains (0.1-0.26 aloft,
  ≈ 0 for RO) show the update also ignores upper-air data. (2) It omits sea-level pressure, the paper's "clear
  weakness" and the best evidence for its own synoptic-scale point. (3) It misses Fig. S3, which partly answers its
  closing question: the memory *does* hold the observing network, as a filter's covariance should; the latent z is
  mostly weather. "Atmosphere or observing network" is a false choice; the real test is whether z is invariant to
  the network. (4) "Cross-modal inference" is mostly learned retrieval from related radiances (CloudSat head trained
  from geostationary IR; IMERG and NSRDB built from inputs). (5) It misses the held-out-neighbour, elevation and
  conflict-of-interest caveats. (6) The "no climate-length integrations" reservation is fair for climate-model use,
  but not a claim the paper makes. (7) Minor: 50 M trainable plus 99 M frozen; "18 systems and two derived products".
- Its E3SM / MICE / ACE section is the owner's own research context: not in the public pieces, except one closing
  question (could an observation-driven latent state initialize other models; the paper suggests it in §5).

## Background facts safe to state

Kalman 1960 (the predict-correct filter; used in Apollo navigation). Data assimilation: background, analysis, first
guess, observation operator, B and R. Hafner et al. 2019-2023: Dreamer world models from model-based reinforcement
learning ("Dream to Control: Learning Behaviors by Latent Imagination"). Predictive-coding accounts of perception
(Friston 2010, Clark 2013; cited by the paper). Radiosondes are weather balloons launched twice a day. Limb darkening:
a slanted view crosses more atmosphere and sees higher, colder layers. GraphCast, Pangu-Weather start from ERA5-style
analyses. WeatherNext3 ingests satellite data hourly but starts from an analysis nearly 6 h old (the paper, §1).
