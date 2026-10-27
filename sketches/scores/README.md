# Score sketches

Five standalone score prototypes, each after a piece of music the aigs pod loves. They aren't wired into the
engine yet: the plan is to turn each into a `MUSIC['style']` in `aiglainer/audio.py` next to `night` and `dawn`.
Everything here is original material (chords, melodies, voicings) written in the spirit of the pieces, not copied
from them; the recordings themselves are under copyright and must not be used.

| sketch | after | what it is |
|---|---|---|
| `daylight` | Max Richter, *On the Nature of Daylight* | strings over a descending lament bass in E minor (Em - D - Cmaj7 - B, Am7 - Em/G - Cmaj7 - B - Em), 6.6 s a chord, no pulse; violas, then violins join, a soft piano figure moves through the chords, a singing line rises from the second pass. Sad but warm, not spooky: no semitone clusters, the major dominant pulls home |
| `encore` | Keith Jarrett, Encore from Tokyo (*Sun Bear Concerts*, 1976) | soft solo piano, 60 bpm, E minor: a four-bar descending ground (E-D-C-B) played three times as variations, the left hand gently pulsing in eighths, a mid-register melody just behind the beat, one note lifting the third pass (C#m7b5), time loosening into a quiet coda and a rolled Em |
| `analog` | Martin Roth, *An Analog Guy in a Digital World* | mellow piano house, 106 bpm, A minor (Am9 - Fmaj9 - Dm9 - Em7, two bars each): pads and electric piano, a soft kick with a gentle pump from bar 4, bass, hats and shaker from bar 8, an acoustic piano hook from bar 12 to 24, then the beat drops away over tape hiss |

| `silencia` | Hammock, *Silencia* (2019) | serene, D major (Dadd9 - A/C# - Bm7add11 - Gmaj9, 7.5 s each): swelling processed-guitar pads (no pick, volume swells, chorus, an octave shimmer), a cello line forward from the third chord, a few soft piano notes far back, a long dark hall |
| `mysterium` | Hammock, *Mysterium* (2017) | solemn, B minor to D major (Bm - Gmaj7 - D/F# - Em9 - Bm - Gmaj7 - Asus2 - D, 8 s each): low strings, a wordless choir opening from a hushed "oo" to an "ah" at the swell, guitar haze above, violins rising into a final D major, the glimmer of hope |

(`hammock.py` holds both; it borrows the cello from `daylight.py` and the soft piano from `tracks.py`.)

What the reviews said, and what the sketches took from them:

- **Richter**: a ground bass under a cyclical progression; lower strings first, the violin's melody later, drones
  that keep the intensity; grief and hope held together.
- **Jarrett**: "more songful and direct", "melodic lines suspended over left-hand ostinatos", "gently pulsing
  harmonies", "time loosened, rhetoric softened", "almost a set of variations" over a descending repeating bass,
  a coda of "glassy, otherworldly serenity"; "extraordinary sorrow amidst unspeakable beauty".
- **Roth**: a classically trained pianist's touch over synths and layered beats; electric piano and acoustic piano
  together; reflective, romantic, "mellow lower-register depth". Sibling tracks on the album sit at 104-107 bpm in
  minor keys.
- **Hammock**: the Mysterium / Universalis / Silencia trilogy. *Mysterium* (made in grief): strings and a wordless
  choir up front, ambient guitar, a little piano; solemn, slow, soft, with glimmers of hope. *Universalis*: more
  mellow and reserved. *Silencia*: "ambient pads that stem from heavily processed guitar notes and synthesizers, with
  strings and horns adding color", cello moving to the front of the title track, piano motifs, choral washes;
  serene, meditative.

## Render

From the repo root (each writes a ~60 s 48 kHz stereo wav; renders are git-ignored):

```sh
pixi run python sketches/scores/daylight.py sketches/scores/out/daylight.wav
pixi run python sketches/scores/tracks.py encore sketches/scores/out/encore.wav
pixi run python sketches/scores/tracks.py analog sketches/scores/out/analog.wav
pixi run python sketches/scores/hammock.py silencia sketches/scores/out/silencia.wav
pixi run python sketches/scores/hammock.py mysterium sketches/scores/out/mysterium.wav
```

`out/` holds the approved renders as `.m4a` (local only).

## Notes for wiring them in

- Synthesis reuses `aiglainer.audio` helpers (`mtof`, `env_adsr`, filters, `stereo`, `reverb_ir`, its seeded `rng`).
- `tracks.py` has two pianos: `piano` (used by `analog`) and `grand` (used by `encore`), which dulls quickly
  after the strike so held notes don't sound like an organ. If `grand` still isn't convincing, the next step is a
  sampled piano (e.g. Salamander Grand; check its licence first).
- The score engine ducks and mixes; these sketches master themselves. When porting, keep `music()`'s contract
  (a stereo bed of `total` seconds) and run `make check P=lawful` before and after: existing videos must stay
  `IDENTICAL`.
