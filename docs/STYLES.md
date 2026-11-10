# Making it your own

The defaults are the aigs pod's: the dark /mull/ look, our voices and our scores. They are defaults, not requirements.
Everything here is a setting in a piece's `project.py` (or `narration.py`), so changing the look never means changing the
engine, and leaving a setting out gives you exactly what the pod uses.

[`projects/examples/videos/light`](../projects/examples/videos/light) is a working example, a light look built from these
settings alone: `make P=examples/videos/light`, then read its `project.py`.

| to change | setting | where |
|---|---|---|
| colours | `THEME` | `project.py` |
| background | `BACKGROUND`, and `ground` in `THEME` | `project.py` |
| typefaces | `FONTS` | `project.py` |
| score, or your own track | `MUSIC['style']` | `project.py` |
| music under the host | `MUSIC['duck_db']` | `project.py` |
| overall music level | `MUSIC['level']` | `project.py` |
| sound effects | `SOUND_EFFECTS` | `project.py` |
| voice | `VOICE` (videos, shorts), `HOSTS` (podcasts) | `narration.py`, `episode.py` |
| layout and animation | your own scenes | `scenes*.py` |

## Colours

`THEME` overrides tokens from `PAL` in `aiglainer/core.py`. Scenes draw with tokens, so the whole piece follows.

```python
THEME = dict(ground='#f5efe3', ink='#231f1a', muted='#6f6a62', y='#b5701f', panel='#fffaf0', fade='#f5efe3')
```

| tokens | what they colour |
|---|---|
| `ground`, `fade` | the background; what the video fades to at the end |
| `ink`, `muted`, `pencil` | text, labels, line drawings and handwriting |
| `faint`, `line`, `panel`, `panel2` | frames and rules, card fills |
| `y` | the accent: emphasized words, swashes, lamp glow, progress bar |
| `f`, `g`, `c`, `v`, `x`, `r` | data colours (green, blue, coral, grey, lilac, red) |
| `sticky`, `sticky_ink`, `sticky_tag`, `pin`, `shadow` | the sticky note |

Equations are images, so they don't follow `THEME`: set `COLORS` in `eqs.py` to match and run `make tex`. For charts of a
paper's data, keep the colours the source figure uses.

## Background

```python
BACKGROUND = dict(image='bg.png', glow=0.5, vignette=0, grain=0.5, frame=False)
```

`image` is a file in the project, scaled to cover the frame (use `ground` for a plain colour). `glow`, `vignette` and `grain`
scale from 0 to 1 and beyond, with 1 as the default; `frame` is the thin inset line. Shorts use `image`, `glow` and `grain`.
With an image, choose `ink` and `muted` so text reads on it, and check every scene.

## Typefaces

```python
FONTS = dict(display='fonts/MyHeading.ttf', italic='fonts/MyHeading-Italic.ttf', sans='/Library/Fonts/Other.ttf')
```

The roles are `display` (headings), `italic` (emphasized words), `sans` (body and captions), `mono` (small labels) and `hand`
(asides). A path can be absolute, in the project, or a file in `aiglainer/fonts/`. Variable fonts take the weight scenes ask
for; static ones ignore it. A glyph the font lacks falls back per character, so check Greek and arrows. Commit only fonts
whose licence allows it, and include the licence.

## Music

`MUSIC['style']` is one of our scores (`night`, the default, `dawn`, `daylight`, `encore`, `analog`, `silencia`, `mysterium`;
docs/WORKFLOW.md describes them), `'none'`, or **your own audio file**:

```python
MUSIC = dict(style='music/mine.m4a', duck_db=16)
```

A file is looped with a crossfade to fit and set to the scores' loudness. Use only music you have the rights to, and keep the
file out of git: media is refused by the commit guard, so say in the piece's `AGENTS.md` where to get it.

**`duck_db`** is how far music drops under the host, and it applies to videos and shorts. With it set, music holds down for
each whole spoken line and rises between lines, so the number is what you get. Without it, music follows the voice's waveform
and breathes back up between words, averaging about 6 dB under speech: pieces built before this setting existed sound that way.
`make new` starts you at 16. **`level`** scales all the music (`0.7` is about 3 dB quieter). Podcasts honour both numbers but
always follow the waveform, and set their bed with `BED`. `SOUND_EFFECTS = False` removes a video's whooshes and pops.

## Voices

`VOICE = 'michael'` picks a host from `aiglainer/hosts.py`; a Kokoro voice id (`VOICE = 'af_nicole'`) also works, with `SPEED` and
`LANG` beside it. Audition with `make voices`. `VOICE = 'bella-nicole'` is Bella blended 70/30 with Nicole: softer and
closer, still called Bella on air. Any blend works as a voice id, `'af_bella:0.6,af_nicole:0.4'`, and descriptions credit it as
a blend. To add a host for everyone, add an entry to `hosts.py`. How words like "aigs" are
said is in `aiglainer/lexicon.py`; pronunciations for one piece go in its own `SAY`.

## What stays the same, whatever the look

These are about being right and being readable, not about taste:

- Charts come from the source's numbers, never drawn by eye. Illustrations are labelled.
- In shorts, what matters stays inside the safe zone: check `safe_*.png`.
- Check contrast with `make frames`, and the thumbnail at its smallest size with `out/thumbnail_sizes.png`.
- Narration still passes the Whisper check, and someone listens once before it goes out.

## Not settings (yet)

Frame size and rate (1920x1080 and 1080x1920, 60 fps), the layout of shorts (`SAFE`, the caption position), and the HUD and
progress bar's positions are in the engine. Narration runs on Apple Silicon only. If you change the engine, `make check` must
still print `IDENTICAL` for existing pieces: add a setting whose default is today's behaviour, as all of the above do.
