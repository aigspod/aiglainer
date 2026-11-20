# hackathon/radio: Port Samudra radio for the hackathon page

Everything that made the audio, and the share thumbnail, for the throwaway hackathon page
**https://aigspod.github.io/hack/circuits/** (source: `aigspod.github.io/hack/circuits/index.html`, one self-contained
HTML file plus `audio/*.m4a`). Built on Nov 20, 2026 for "exege hacks circuits". The look is an original
early-2000s night city: no game names, logos, fonts or characters. Keep it that way.

## Run

From the aiglainer root, with the pixi env (it has Kokoro, Whisper, ffmpeg):

```sh
export PATH=$PWD/.pixi/envs/default/bin:$PATH
python projects/hackathon/radio/make_audio.py music voices   # 4 station loops + DJ clips + the first 6 ads
python projects/hackathon/radio/make_more.py                 # second track for each station (5 minutes before a repeat)
python projects/hackathon/radio/make_secret.py               # Hidden Layer 108.0 (unlocked by 6 hidden packages)
python projects/hackathon/radio/make_block.py music voices   # 97.7 The Block beats, Bug Line hold music, 7 more ads
python projects/hackathon/radio/make_bug.py                  # 1500 AM The Bug Line, shouty edition
python projects/hackathon/radio/make_live.py                 # news-desk interruptions at 12:00, 14:00, 15:00, 17:00 ET
cp projects/hackathon/radio/audio/*.m4a ../aigspod.github.io/hack/circuits/audio/
```

Output goes to `radio/audio/` (ignored). Every voice script prints Whisper's transcript next to each clip; read it.
Note `make_block.py` and `make_secret.py` import `make_audio`, which renders whatever `music`/`voices` you pass, so
`make_block.py music voices` also re-renders make_audio's set (same output, slower).

## What is where

| file | makes |
|---|---|
| `make_audio.py` | `music_{latent,skip,samudra,deep}` (aiglainer score styles analog, encore, velours, mysterium; 150 s, seam crossfaded) and DJ/talk/ad clips; holds `V`, the voice table |
| `make_more.py` | `music_*2`: a second style per station (nuit, daylight, berceuse, silencia), 2 s fades for the page's crossfade |
| `make_secret.py` | `music_secret` (cascade) and `secret_1..3` |
| `make_block.py` | `music_block` (boom bap, 88 BPM, C minor) and `music_block2` (G-funk, 92 BPM, Eb minor, portamento lead), synthesized from scratch in numpy; `music_bugline*` hold music; `block_*` DJ lines and verses; seven ads |
| `make_bug.py` | `bug_*`: a hot, overdriven host (am_eric 1.16x) who talks over callers by 0.35 s; callers through a 320-3300 Hz phone band with saturation |
| `make_live.py` | `live_s1`, `wrap_s1`, `live_s2`, `wrap_all` |
| `og/` | the 1200x630 share image: `python og/serve.py out.png`, open `http://127.0.0.1:8778/` in Chrome; the page draws the hero scene (`hero.js`, copied from the page) plus the title on a canvas and POSTs the PNG back. Then `sips -s format jpeg -s formatOptions 85` |

## The page, for whoever edits it next

- **Stations** are the `STATIONS` array (`id, freq, band, name, tag, dj, music, clips, tracks`, optional `bed` for
  music level under talk, `open` for a talk show's first clip). `TRACKS(st)` plays `music_<music>` then
  `music_<music>2`. Talk-format stations are listed in `isTalk`. Captions come from `TEXT[id]`; a caption that starts
  with `<b>` carries its own speaker labels.
- **Breaks:** 90-180 s apart on music stations (DJ 45%, one ad 35%, two ads and a DJ back-announce 20%), never one of
  the last four clips; talk stations shuffle their clips with 4-9 s gaps and an ad 30% of the time. Verses
  (`block_verse*`) duck the beat to 0.7 instead of 0.3.
- **Music** runs on two decks that crossfade: 3 s between tracks, about 1 s between stations, under a burst of static.
- **On-air moments** (`MOMENTS`): within 20 minutes after a session starts or ends, the news desk interrupts the radio,
  the pager flashes and a banner shows; once per browser (localStorage `psm<clip>`). The hero button turns into
  "Join session N now" while a session is live.
- **Car:** cruise control holds about 35 mph; W or the pedal adds throttle (top speed about 100), S brakes, H honks.
  From curiosity 3 stars a police cruiser shows in the mirror and passes; more often at 4 and 5.
- **Hidden packages** (`data-pkg` 1-6) unlock `SECRET` as the last preset.

## Gotchas

- Audio only starts from a real click (an `el.click()` from a script leaves the AudioContext suspended), so test the
  radio with an actual click.
- `python3 -m http.server` has no Range support, so seeking (the "live" station offset) fails locally; GitHub Pages
  is fine.
- Link previews: Slack, Teams and iMessage cache the first unfurl of a URL. The first push had no share tags, so the
  image was renamed (`thumb-v2.jpg`) to force a refetch. Rename again if you change it.
- Kokoro reads ALL CAPS as letters and "CUDA" as "C-U-D-A"; write "Kooda". It can't shout: exclamation marks, a
  faster speed and the overdrive in `make_bug.py` do the job.
