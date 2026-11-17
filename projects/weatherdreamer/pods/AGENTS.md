# weatherdreamer/pods

An aigs pod extra: read [../AGENTS.md](../AGENTS.md) first (numbers, accuracy notes, the review check, wording rules).

| name | what | length | voice, score |
|---|---|---|---|
| `episode` | The Forecaster With No Answer Key: one host, the dark room (predict, then correct) to an hourly learned picture of now and back | 22:03 | `bella-nicole`, `SPEED = 0.92`, `PACE`; `silencia`, no bed, `duck_db = 9` |

The owner's personal set: `project.py` sets `SHOW` and `ARTIST` (mahf708) because the engine's ID3 defaults carry the
pod's show name. The cover says "the aigs pod · episode 30" (owner's request). Closing questions are "to think about" (`'H?'`); no chimes. Cover: `episode/cover.py` (1400 × 1400,
the videos' globe), `PYTHONPATH=. .pixi/envs/default/bin/python projects/weatherdreamer/pods/episode/cover.py`.

Built Nov 17, 2026: `episode/out/podcast/WeatherDreamer_pod.mp3`, 22:03, 235 sentence clips, 0 flagged, mix WER 0.003
over 3,050 words (about 138 words a minute overall, 160 while speaking), −16.2 LUFS. Nobody has listened to it yet.
Published Nov 17, 2026 as feed episode 30, "Can a weather model learn without an answer key?" (archive.org item
`weatherdreamer-pod`, uploaded from the aigroup account; `aigspod.github.io` commit 52dffe5, art `images/ep030.png`).

## Choices

- Story spine: the dark room (predict, correct) → nobody can see right now → the old hand-built loop → an apprentice
  with no answer key → it works near the ground → the turn (up there) and its two causes → reading the scoreboard →
  what it learned to trust (gains, limb darkening) → what's in its memory (Fig. S3) → waking up every hour.
- The script was fact-checked line by line by an independent reviewer before the final build; fixes: the paper does
  run one data-denial test (stations); "within 10 %" is surface stations only (ocean winds 1.65×); moisture "within
  25 %" is the microwave channels; gains aloft are "light", not zero (only radio occultation ≈ 0); "fast winds" is our
  arithmetic, the paper's cause is the large, slow circulation; the ~200 km figure is where assimilation stops helping
  a hidden station; EarthCARE is radar + lidar and WD detects less cloud; GSI's larger observing system is named.
- Off air, in the show notes: GEFS, IFS ENS, GSI, ASCAT, EarthCARE, CloudSat, IMERG (plain words on air). The authors
  after Kate Duffy are named in the notes ("Kate Duffy and four colleagues" on air).

## What Whisper mishears here

"WeatherDreamer" is heard as "Weather Dreamer" (two words): fine in long sentences, flagged in short ones (now "this
model" / "the new model"). Years spoken as words ("twenty twenty") flag; write digits. "sixteen hundred kilometers"
flagged against "1,600" (now "one thousand six hundred"). "taught it the" → "taught at the"; "low air a patch" → "low
era patch" (both reworded).
