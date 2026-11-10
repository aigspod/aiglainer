# hackathon/videos

| name | what | length | voice, score |
|---|---|---|---|
| `invite` | the hype invitation: hook, title drop, models, tools, five open questions, six tracks, welcome, end card | 1:38 | Bella blended with Nicole (`bella-nicole`), its own track (`music.py`) |

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
