# dynamics/shorts

Shorts for arXiv:2512.21113v2. Facts and accuracy notes: [../AGENTS.md](../AGENTS.md).

| name | hook | scenes | length | voice, score |
|---|---|---|---|---|
| `average` | Attention can only average | native `AvgMix` (weights: illustration), `AvgPlane` (§3.1; soft spring = our calculation) | 0:38 | Bella, `dawn` |
| `twoheads` | Two heads, one subtraction | native `TwoHeadsMix` (W_O from App. A.1), `TwoHeadsSpec` (our simulation, our two-head version) | 0:38 | Michael, `analog` |
| `sensor` | Time for a missing sensor | native `SensorWindow` (§3.2; motion simulated), `SensorCount` (our rough count) | 0:41 | Bella, `encore` |
| `updown` | Same position, two directions | native `UpDownGauge` (our Van der Pol simulation), `UpDownBars` (Table 1) | 0:40 | Michael, `night` |
| `unfold` | Room to unfold | native `FoldV` (our Chafee-Infante simulation), `RoomV` (illustration) | 0:38 | Bella, `silencia` |
| `reynolds` | Tell it the Reynolds number | native `LoopsV` (illustration), `ReconV` (§4.3 / App. A.5) | 0:40 | Michael, `daylight` |

Lengths are the timeline (`make plan`), all under 45 s. Headlines are 3-5 words. All set `MUSIC['duck_db'] = 16` and
end on a hold of 2.2-2.4 s.

**Shared code lives in `../videos/sign/`.** Every short lists `dynamics/videos/sign` in `SOURCES` for `dynkit.py` and its
data. What each borrows:

- `average`, `twoheads`, `sensor`: native scenes in `../videos/sign/dynshorts.py`, with sign's `data/sdof.json` and
  `twodof.json`.
- `updown`: native scenes in `../videos/sign/dynshorts2.py`, with sign's `data/vdp.json`.
- `unfold`, `reynolds`: native scenes in `dynshorts2.py`, which loads `../videos/unfold/scenes.py` by path (several
  pieces have a `scenes.py`) for its `Fold` data, `Thick`, `sheet3d` and `wake`. They also list
  `dynamics/videos/unfold` in `SOURCES` for `ci.json`.

A change to `dynkit.py`, `dynshorts*.py` or `unfold/scenes.py` changes these shorts; rebuild them and check
`out/narrated/qa/safe_*.png`.

## Caveats

- The shorts say "one head" (never "a head", which Whisper hears as "ahead") and avoid the 2-DOF frequencies (see the
  accuracy note). They leave "Van der Pol" and "Chafee-Infante" on screen only, which keeps short lines safe.
- `DESCRIPTION`s cite the paper as 2025 (arXiv v1), like the episode and the site. `reynolds` names ACE and SamudrACE as our extrapolation.
- All six end with 0 flagged (every line WER 0.00) and a mix WER of 0.000 (Nov 9, 2026; `average`, `twoheads` and
  `sensor` rebuilt after the last `dynshorts.py` edit). Nobody has listened.
