# weatherdreamer/videos

An aigs pod extra, not a journal-club piece: read [../AGENTS.md](../AGENTS.md) first (HUD, endings, no journal-club
wording, numbers, accuracy notes, the review check). Each piece stands alone: don't write "last time" or "in the
other video".

| name | what | length | voice, score |
|---|---|---|---|
| `loop` | The Forecaster With No Answer Key: the forecast loop. Nobody can see now; data assimilation and the analysis; the Kalman loop; the learned loop (memory, background, analysis, decoders); no reanalysis (Fig. 1); three lessons; near the ground (Fig. 4); what it was never fed (rain, Fig. 6 cloud tops); the turn higher up (Table 2, Fig. 4d); the walls and not listening; the scoreboard; cost and the zero-memory limit; questions | 8:21 | `bella-nicole`, `daylight` |
| `trust` | What Did It Learn to Trust?: a detective story. Cold open on the striped memory (Fig. S3); the case file and the gain; clue one, the learned observation errors and gains (Fig. 8) and where they're timid, too trusting or nearly absent; the trace in Table 2 and the two suspects (§5); clue two, limb darkening and the vanishing swath stripes (Figs. 9b, S7); clue three, cloud tops vs EarthCARE and rain, then learned retrieval; the scoreboard read with care (clocks, Fig. 4a; fine print); the reveal (memory h vs state z) and the real test (is z invariant to the network?); questions | 10:41 | `am_michael`, `mysterium` |

Music: `duck_db` 9, `duck_ramp` 1.2, `duck_bridge` 2.0; last scene `hold` 2.4.

## The topic kit: `loop/loopkit.py`

Other pieces can use it with `SOURCES = ['weatherdreamer/videos/loop']` and `from loopkit import *` (its docstring is
the API). In short: `fig`/`figcard` (crops of the paper's figures from `projects/weatherdreamer/data/figs`, made by
`../extract_paper.py`, not in git: a fresh clone must run it first), `tag`/`src`/`hdr`/`stamp`, `node`/`curved`/`hbar`,
station/balloon/satellite icons, `Globe` (orthographic, no coastlines; `STATIONS`, `BALLOONS`, `GEO_LONS`,
`polar_track`), `TitleCard`, `EndCard`, `question_cards`. System colours follow Fig. 4: WeatherDreamer blue (`WD`),
GEFS coral, IFS ENS green; observations blue in the loop diagrams. The podcast cover imports it too.

## `loop` caveats

- Every globe is an illustration (clustered dots on rough continent centres, computed polar-orbit tracks and
  geostationary footprints, no coastlines), labelled. The Kalman number line (20° vs 22°, σ 1 and 0.5, k = 0.8) is an
  illustration of Eq. 2's one-variable form.
- Bars are typed from the text and Table 2 with the section beside them. `Aloft` shows Table 2's ratios with the worst
  channel or level as a dash; Fig. 4d is shown as a crop for sea-level pressure (no number is quoted).
- `Walls` labels the 50 m/s jet crossing a patch in ~9 h as "our arithmetic" and gives the paper's own reason (the
  large, slowly evolving circulation, §5). `Scoreboard` labels the elevation point "our reading".
- Narration avoids "WeatherDreamer" in short lines (Whisper hears "Weather Dreamer"). Built Nov 17, 2026: 59 lines,
  0 flagged, mix WER 0.014, 500.7 s, −14 LUFS; frame sheets checked. Nobody has listened to it yet.

## `trust`: its own kit, `trust/trustkit.py`

Independent of `loopkit.py` (built in parallel): `fig`/`figcard`/`crop_rect`/`highlight` (crops from
`projects/weatherdreamer/data/figs`, with a clear error telling you to run `../extract_paper.py`), `tag`/`src`/`hdr`,
`exhibit` (the manila evidence tag, the piece's motif), `hbar`/`marker`, `satellite`, `thermometer`, `gauss`,
`question_cards`, `TitleCard` (Fig. S3a behind the title), `EndCard`. Fig. S3 map positions are `S3_COLS`/`S3_ROWS_*`
in `scenes1.py` (fractions of the whole figure; checked against previews).

## `trust` caveats

- Paper figures are crops: Fig. S3a/b (memory and latent), Fig. 8a/c (learned σ_O), Fig. S7a/c (ATMS ch 7 observed vs
  nadir decode), Fig. 4a (2 m temperature CRPS; the legend under it is ours, in the figure's colours). The amber
  highlight boxes only point at regions; they are not data.
- Charts typed from the text: gains (§4.3.3: 0.64/0.82, 0.90/0.80, 0.10-0.26, radio occultation "near zero", drawn
  as a sliver and said "not to scale"), Table 2 ratios with per-channel/level whiskers, limb corrections near 80°
  (§4.4: 6/14/16/22 K), crossover lines drawn from the fitted slopes (−13.6/−0.3, −6.1/−0.1 K per unit sec θ),
  cloud tops vs EarthCARE (§4.2.3), rain (§4.2.1).
- Illustrations, labelled: the loop, the thermometer (k = 0.8), the O/B/A line, the slant-path slab and cold-limb
  disks, the patch grid, the network-swap test. "Our arithmetic" (50 m/s crosses 1,600 km in ~9 h) and "our reading"
  (no elevation adjustment, Text S6.4) are amber.
- Facts adjusted after the podcast fact-check: the paper *does* run one data-denial experiment (all surface stations,
  §4.1); what it never checks is whether z stays the same when the network changes. Upper-air gains are "leans only
  lightly" (0.1-0.26), only radio occultation is near zero. "Within ~10%" is surface stations only (ocean winds 1.65×).
  The ~200 km is where the network's help at a held-out station fades. Sunlight is verified at ground stations
  (USCRN, SOLRAD), so the independent checks are EarthCARE *and* those stations (topic notes updated to match).
- Narration says "WeatherDreamer" only in long lines (heard "Weather Dreamer", one word off). Built Nov 17, 2026: 71
  lines, 1,444 words, 0 flagged, mix WER 0.010, 640.8 s; frame sheets and thumbnail sizes checked. Nobody has
  listened to it yet.

### What Whisper mishears in `trust` (`am_michael`, speed 1.0, whole lines)

All 71 lines passed. One word off and passing: "WeatherDreamer" → "Weather Dreamer", "cloud-top" → "Cloudtop", "read
out" → "red out", "it's scored" → "it scored". Kept off air (on screen only): Desroziers, Hollingsworth-Lönnberg,
EarthCARE, ASCAT, IMERG, GEFS, IFS, GSI, CRPS.

## Published (Nov 17, 2026, The AIGS Pod channel, public)

Videos: `loop` https://youtu.be/pEcxWdpC2hs ("The Forecaster With No Answer Key: a weather model that learns from
observations alone"), `trust` https://youtu.be/H5E3G0QZGwY ("What Did It Learn to Trust? Inside a weather model that
learned its own forecast loop"). Each has its description, thumbnail and captions.srt as English subtitles; not for
kids, paid promotion No, altered content No.
