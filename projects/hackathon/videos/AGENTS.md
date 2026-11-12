# hackathon/videos

| name | what | length | voice, score |
|---|---|---|---|
| `invite` | the hype invitation: hook, title drop, models, tools, five open questions, six tracks, welcome, end card | 1:38 | Bella blended with Nicole (`bella-nicole`), its own track (`music.py`) |
| `invite-jazz` | the jazz edition: the same invitation, calmer, warmer and more intimate | 2:02.5 | `bella-nicole` at speed 0.94, its own jazz tune (`music.py`) |

Lengths are the timeline (`make plan`), which the final MP4 matches.

## invite: not the house look

- **Look** (`poster.py`): heavy Inter capitals on paper and on full-bleed cobalt, orange, lime and black slabs, riso-style
  misregistered type, slice glitches, scanlines, halftone globes. Colours are extra THEME tokens (`paper`, `ink`,
  `cobalt`, `orange`, `lime`, `night`) in `project.py`. No HUD or progress bar (every scene has `chapter = None`); hard
  cuts (`fade_in = fade_out = 0`).
- **Grid** (`beat.py`): 120 bpm, a bar is 2 s. Each scene in `narration.py` has `bars` and `mus` (the music section per
  bar). `_snap()` there lays the lines from the cached clips' lengths and sets `hold`, `vend` and `smax = 1`, so every
  scene lasts exactly its bars with an **unwarped clock**: hits authored at `b(bar, beat)` in `scenes.py` land on the beat.
  After editing a line run `make narration` twice (the first run synthesizes it; it says so when it had to guess).
  If a scene's lines outgrow its bars, it prints how much is missing: add a bar (and a `mus` entry).
- **Music** (`music.py`): an original track (kick, clap, hats, offbeat bass, sidechained supersaw, pluck arpeggio, a
  lead hook, risers, snare rolls) built from the scenes' `mus` sections. `project.py` calls `music.ensure()`, which
  renders `cache/music_<hash>.wav` (hash of `music.py` and the arrangement, ~5 s) if missing; the file is never
  committed. Under the voice: `duck_db = 8`, `duck_ramp = 1.2`, `duck_bridge = 2.0`; `level = 1.3` so the
  music-only drops ride above the voiced verses. `LEVELS` in `music.py` sets section loudness after the limiter;
  falls ease over 0.5 s before a cut. Run it alone with
  `.pixi/envs/default/bin/python projects/hackathon/videos/invite/music.py`.
- **Date**: `WHEN` in `event.py` feeds the title drop, end card, thumbnail, description and the last line (spoken as
  "16th" via `event.spoken`). Changing it changes the last line: run `make narration` twice, then `make`.
- Strobes change colour at most 3 times a second with no dark/light alternation (WCAG 2.3.1); keep it that way.
- Sound effects: impacts on the three drops, whooshes on cuts, ticks on card slams (the engine drops ticks near line onsets).

Built Nov 10, 2026: 0 flagged, mix WER 0.000 over 87 words, -13.9 LUFS. Published Nov 10, 2026: https://youtu.be/0R4ix18rNB0

## invite-jazz: the jazz edition

The same facts and story as `invite`, said to one listener over an original small-combo jazz tune. Nothing in `invite/`
is changed or shared except `event.py`: `project.py` puts `invite/` on the path (the engine runs `project.py` before it
adds `SOURCES`), so `WHEN` and `spoken` come from there and one edit updates both videos.

- **Look** (`sleeve.py`): a late-night record sleeve. Fraunces with its SOFT and WONK axes up for display and its italic
  for warm words (drawn by `sleeve.say`, with Inter as the per-glyph fallback, e.g. for ₂), Inter body, Space Mono labels;
  cream paper, deep navy and teal, mustard, terracotta, sage and rose (extra THEME tokens). A turning record whose label is a
  little planet, then a network, then the title's rising "sun" with mid-century arcs; portholes, LP-sleeve paper cards,
  a back-of-sleeve tracklist, a table with a glowing empty seat. No cuts and no flashes: each scene opens its ground over the
  previous scene's colour with a slow iris (`sleeve.iris`), or crossfades on the same paper; type rises softly into place.
- **Grid** (`beat.py`): 96 bpm swung, a bar is 2.5 s; `narration.py` has `bars` and `mus` per scene and the same `_snap()`
  as `invite`, so scene changes land on phrase boundaries with an unwarped clock.
- **Music** (`music.py`): brushes (swish, taps), ride with hi-hat foot, a feathered kick, an additive upright-style
  bass (walking or two-feel, generated from the chords), an FM Rhodes comping rootless 9th/13th voicings over ii-V-I,
  a vibraphone lead with the motif (5-6-1 up to the major 7th; on the last bar it resolves up to the tonic), soft muted-brass
  pads under the choruses. In F, lifting to G for the open questions (`lift`) and ending on a held Gmaj9. Sections:
  intro, two, walk, turn, chorus, lift, break, coda, outro. It reads the line times from `narration.py`: the vibes lay out
  and the drummer plays at about 60% under the voice. `LEVELS` eases every section change over a beat either side (no
  steps); `limit()` is a gentle peak limiter. Rendered by `ensure()` to `cache/music_<hash>.wav` (never committed). Under the
  voice: `duck_db = 7.5`, `duck_ramp = 1.4`, `duck_bridge = 2.0`, `level = 1.15`. `SOUND_EFFECTS = False`.
- **Whisper traps found here:** at speed 0.94 Kokoro's "aigs" is heard as "Agues" in "a hackathon, from the aigs pod journal
  club" (fine at 1.0), so the line is "The aigs pod journal club is throwing a hackathon." Under the fuller sections the mix
  once lost "code" ("cold") and "16th" ("16"); a calmer section under those lines and the lighter drums under the voice fixed it.

Built Nov 10, 2026: 0 flagged, mix WER 0.000 over 104 words, -14.0 LUFS.

Published Nov 10, 2026: https://youtu.be/AQ5_Rd7OGuk
