# Score sketches

Five standalone score prototypes, each after a piece of music the aigs pod loves. Each is now a score style in the
engine (`aiglainer/scores.py`), picked with `MUSIC = dict(style='encore')` like `night` and `dawn`; these 60-second
versions stay as the reference for how each should sound.
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

Three more after Max Richter, *nor earth, nor boundless sea* (*Sleep*, 2015), in `sleep.py`. The title is the first
line of Shakespeare's Sonnet 65, and all three follow the poem: fourteen phrases, one per line, each two shorter
notes leading into a long one (the line resting on its last word), played legato and woven into the strings.
The strings swell and breathe: each line grows towards its middle and eases off (brighter as it grows, like more
bow), riding a larger arc that builds to each quatrain's third line.
Lines 1-8 sigh downwards in D minor, coloured by major sevenths and ninths (Dm - Dm/C - Bbmaj7 - Am7,
Gm9 - Fmaj7 - Bbmaj9 - Am7); lines 9-12 ("O fearful meditation!", four questions) repeat notes and climb, and line 12
hangs on Am7; the couplet ("in black ink my love may still shine bright") turns to F major, then the loop falls back
to D minor (the hope is fragile). The strings thin to near-silence at each quatrain's end; the room is close, not a
hall. Strings in front throughout. Not yet engine styles.

The phrase began as a spoken "ta... ta... taaah" (two short, separated notes, then a long one); heard against
everything else it sounded odd, so it is now legato and quieter, and the swelling strings carry the piece.

| sketch | after | what it is |
|---|---|---|
| `boundless` | the main bed | 8 s a line: cellos and basses, then violas and violins; the phrases on cellos for the first quatrain, then violins; a piano note in the gap of every other line in the busy middle |
| `sonnet` | the soprano | 8 s a line: hushed strings and a soft organ; one wordless soprano sings the phrases (violins take them on alternate sonnets at a video's quiet edges) |
| `brass` | the stillest | 11 s a line, low strings crossfading slowly, the phrases soft and low on cellos, one solo-violin A held high across everything (it sits in every chord) |

These are the first sketches with **real string samples**: violin, viola and cello sections, solo violin and
contrabass from the Versilian Studios Chamber Orchestra 2 Community Edition (VSCO 2 CE) by Sam Gossner / Versilian
Studios, released under CC0 1.0 (https://github.com/sgossner/VSCO-2-CE; credit given here as its readme asks).
`samples.py` fetches the sustained-vibrato folders once (~300 MB) into `~/.cache/aiglainer/vsco2ce/`, measures every
sample's pitch (the filenames' octave numbers don't follow one convention), and plays any note at any length by
repitching the nearest sample and looping its sustain with crossfades. The soprano and organ are still synthesized
(no free soprano samples), as is the piano.

Checked with `make listen` (Music Flamingo), against what it says about the recording (heard in five stretches
across its 19 minutes; the recording itself is never used or kept here). It hears the recording as D minor, minor
harmony lit by major sevenths and sixths, a phrase of "2 short and 2 long" notes (short ~0.5 s, long ~1.5 s, rests
0.5-1.5 s), near-silences, slow chords, minimal vibrato, a close and intimate sound; melancholic, contemplative.
It calls the recording's strings "synth pads" too, so its "synth" verdicts on slow strings mean little.
How the sketches got there:

- synthesized strings: heard as "synthesizers"; `sonnet` "dark, unsettling"
- sampled strings: "real acoustic strings", "mellow, peaceful", B-flat minor; phrase "short, long"
- quicker phrase, D minor, brighter chords, breaths at quatrain ends, close room, the bed blending two samples a note
  (their vibratos don't line up, so together they waver less): "minimal vibrato", "close, intimate", D minor,
  "melancholic, somber, reflective", "silences", phrase "2 short and 2 long ... held ~1.5 s, a rest of ~0.5 s"
- legato phrase, swelling strings: "the strings swell and breathe, growing and fading"; the melody "not a distinct,
  foregrounded line but woven into the texture"; D minor; "calm, introspective, melancholic"

It doesn't hear the synthesized soprano as a voice (it misses the recording's piano too), and splits our held note in
two just as it does the recording's, so its rhythm answers are coarse.

## Render

From the repo root (each writes a ~60 s 48 kHz stereo wav; renders are git-ignored):

```sh
pixi run python sketches/scores/daylight.py sketches/scores/out/daylight.wav
pixi run python sketches/scores/tracks.py encore sketches/scores/out/encore.wav
pixi run python sketches/scores/tracks.py analog sketches/scores/out/analog.wav
pixi run python sketches/scores/hammock.py silencia sketches/scores/out/silencia.wav
pixi run python sketches/scores/hammock.py mysterium sketches/scores/out/mysterium.wav
pixi run python sketches/scores/sleep.py boundless sketches/scores/out/boundless.wav    # one whole sonnet (137 s; brass 186 s)
pixi run python sketches/scores/sleep.py sonnet sketches/scores/out/sonnet.wav
pixi run python sketches/scores/sleep.py brass sketches/scores/out/brass.wav
```

`out/` holds the approved renders as `.m4a` (local only).

## How they became engine styles

- `aiglainer/scores.py` loops each sketch to any length: the chord loop repeats, the layers enter as in the sketch,
  and the video's arp window (`arp_on`) drives the moving part (daylight's piano figure, encore's eighth-note left
  hand, analog's hook, silencia's piano, mysterium's violins). Encore keeps its coda for the last three bars.
- Each style renders in its own room, seeds its own generator and is scaled to the RMS of `night` after its reverb,
  so swapping styles keeps the voice/music balance; `build()` and the podcast mix skip their own reverb for them.
- These sketches use `aiglainer.audio`'s shared `rng`, so their renders here can differ slightly from the engine's.
- `tracks.py` has two pianos: `piano` (used by `analog`) and `grand` (used by `encore`), which dulls quickly
  after the strike so held notes don't sound like an organ. If `grand` still isn't convincing, the next step is a
  sampled piano (e.g. Salamander Grand; check its licence first).
- Adding them left existing outputs untouched: `make check P=lawful` printed `IDENTICAL`, and the night and dawn
  scores and a podcast mix hashed the same before and after.
