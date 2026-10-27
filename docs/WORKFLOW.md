# Workflow

How a video is built, how to change one, and how to check it before uploading. Everything runs locally on an
Apple Silicon Mac; nothing is sent to a service. To start a video for a new paper, see [NEW_VIDEO.md](NEW_VIDEO.md).

## Layout

The engine in `aiglainer/` knows nothing about any one paper. Each video is a project in `projects/<name>/`:

```
projects/<name>/
  project.py        settings: HUD label, chapters, story steps, music shape, chapter titles, description, thumbnail
  narration.py      the narrated cut: scene order, (visual time, line) beats, VOICE/SPEED, pronunciations
  scenes*.py        scene classes (draw(c, t) on a 1920x1080 skia canvas)
  margin_notes.py   handwritten asides per scene
  thumbnail.py      draw(c) for the YouTube thumbnail
  eqs.py            LaTeX equations -> tex/*.png
  data/  paper/     extracted figure data, and the source PDF
  extract_paper.py  (optional) how data/ was pulled from the PDF
  lines.json        narration clips with durations and Whisper transcripts (generated, committed)
  voice_samples/    sample.txt + the voice audition page
  cache/  out/      synthesized clips and build outputs (not committed)
```

`aiglainer/template/` is a complete four-scene example (copied by `make new`); `projects/lawful/` is the full LAWFUL video.

## Pipeline

```
paper.pdf
   │  make inspect / extract_paper.py   vector paths → curves; colormapped rasters → values (aiglainer/pdf.py)
   ▼
data/*.json ─────────────┐
eqs.py                   │
   │  make tex           │                LaTeX (tectonic) → tex/*.png, skipped when eqs.py is unchanged
   ▼                     ▼
scenes*.py + margin_notes.py              authored on their own clocks
   │
narration.py                              scene order + beats
   │  make narration                      Kokoro-82M → cache/*.wav, Whisper-checked → lines.json
   ▼
aiglainer/narrated.py                     lays lines end to end, time-warps each scene so beats land on their lines
   │  make video                          skia frames, 15 processes → out/<cut>/video_noaudio.mp4
   │  make audio                          score + sound effects + narration, music ducked under the voice
   │  make finish                         −14 LUFS mux, captions.srt, youtube_description.txt
   ▼
out/narrated/<OUTPUT_NAME>
   │  make verify                         Whisper each line in the final mix: word errors + start offsets
   │  make frames                         one frame per line, captioned, for a visual sync check
   │  make thumbnail                      out/thumbnail.png (1280x720) + thumbnail_sizes.png legibility check
```

## Commands

Every target takes `P=<project>` (default `lawful`).

```sh
make setup                       # once: pixi install (rendering, Kokoro, Whisper, ffmpeg, tectonic)
make P=lawful                    # tex → narration → video → audio → finish → verify → thumbnail
make plan P=lawful               # scene timings and speeds, without rendering
make frames P=lawful             # contact sheets of every narration line → out/narrated/qa/
make preview P=lawful SCENE=Fig4a T="5 12 20"    # one scene at authored times → out/prev/
make thumbnail P=lawful
make voices P=lawful VOICES="af_bella bm_george" # audition voices on voice_samples/sample.txt
make CUT=full P=lawful           # the project's un-narrated cut, if it defines FULL_CUT
make help                        # everything
```

The Makefile calls `python -m aiglainer <command> -p <project>`; you can run that directly too.

Outputs for upload are in `projects/<name>/out/narrated/`: the MP4 (captions embedded as a soft track),
`captions.srt` (upload to YouTube as English captions too), `youtube_description.txt` (chapters included), and
`projects/<name>/out/thumbnail.png`.

## Changing things

**A narration line.** Edit `narration.py` and run `make`. Only changed lines are re-synthesized and re-transcribed
(clips are named by a hash of voice, speed and text). If Whisper flags a line, listen to the clip named in
`lines.json`, then rephrase it; respellings for the synthesizer only go in `SAY`.

**When a line starts.** Each beat is `(visual_time, text)`, where `visual_time` is when the matching thing happens in
the scene's authored timeline (read it off the scene code, or use `make preview`). Per scene you can also set:

| key | effect |
|---|---|
| `smax` | fastest the visuals may run (× authored) while catching up to the next line; default 1.8. If more is needed the line waits instead. |
| `hold` | seconds of screen time after the last line; default 0.75 |
| `vend` | authored time the scene ends at; use it to drop un-narrated tail content rather than fast-forwarding it |
| `still` | seconds at the end where visuals freeze |

Global spacing (`GAP` between lines, `LEAD`, defaults) is at the top of `aiglainer/narrated.py`. `make plan` prints
each scene's speed range; anything above ~2× in the tail column is content flashing by, so trim it with `vend`.

**Voice.** `VOICE` and `SPEED` in `narration.py`; `make voices` builds an audition page.

**Look.** The aigspod site's dark /mull/ style: Fraunces headings with one amber italic word and a hand-drawn swash
(`header(..., 'The plan: *three* steps')`), Inter body text, lowercase Space Mono labels, Caveat handwriting for
asides, the lamp and sticky-note doodles. Fonts are bundled in `aiglainer/fonts/` (OFL); any glyph a face lacks
(Greek, arrows) falls back per character to Inter, then SF Pro. Colours are tokens in `aiglainer/core.py` `PAL`
(override per project with `THEME`); data colours should follow the paper's figures. Keep margin notes to one
aside per scene, never the explanation itself.

**Story spine.** A project can set `STEPS` (e.g. `['behavior', 'cause', 'mechanism']`) and `CHAPTER_STEPS`; a tracker
at the top then shows the current step. For beginners, say in the narration which step each section serves and why.
A scene can override with `steps = (i,)` or `tracker = False`.

**Visuals.** Scenes are plain Python drawing on a skia canvas: `draw(c, t)` with `t` in authored seconds, using
helpers from `aiglainer/core.py` (text, LaTeX, shapes, easing), `kit.py` (headers, captions, axes, pills, radar
icon) and `notes.py` (handwriting, sticky, lamp). Build every animation from `ramp`/`window` of `t` so the
narrated cut can warp it. To add a scene: write the class in a module listed in `SCENE_MODULES`, give it a chapter
title in `project.py`, and add an entry with beats to `narration.py`.

**Music.** `MUSIC = dict(intro_until=..., arp_from=..., arp_until=...)` names the scenes that shape the generated
score: a quiet drone and a riser before `intro_until`, a plucked arpeggio between the other two. `style` picks the
score: 'night' (the default: minor ninths, 96 bpm), 'dawn' (brighter major progression, 112 bpm, soft
  pulse), or one after music the pod loves: 'daylight' (strings over a lament bass, after Richter), 'encore' (soft
  solo piano, after Jarrett), 'analog' (mellow piano house, after Martin Roth), 'silencia' (guitar swells and cello)
  or 'mysterium' (strings and a wordless choir), both after Hammock. Every style
fits any length and sits at the same loudness, so trying one is a one-word change (`make audio` to hear it). The
last five live in `aiglainer/scores.py` and use the arp window for their moving part (the piano figure, the drums and
hook, the violins); `sketches/scores/` has the 60-second prototypes they grew from.

## Before uploading

1. `make` finishes with `0 flagged` from narration and a mix WER near zero from verify. Kokoro clips start with
   ~0.4–0.7 s of silence, so small late starts are expected. Whisper sometimes drops a lone opening word in the mix
   ("Limits.") even when it is plainly audible; the verifier retries with more context, and anything it still lists
   is worth one listen.
2. `make frames` and look at every sheet: each frame should show the thing its line talks about.
3. Look at `out/thumbnail_sizes.png`: the words must still read at the smallest size.
4. Watch the video once with sound. The checks above are automatic; listening is the only check for prosody.
5. Upload the MP4 and thumbnail, add `captions.srt` as English captions, paste `youtube_description.txt`.

## Decisions and lessons

- **Voice.** macOS system voices sound robotic. F5-TTS (cached locally) works but slurred "LAWFUL", paused oddly
  and took ~30× longer. Kokoro-82M's built-in voices were word-perfect under Whisper and need no cloning.
  "Bella" (`af_bella`) was chosen by listening.
- **Verification.** Whisper over the whole soundtrack loops ("The control. The control.") and drops words under
  music. `aiglainer/verify_mix.py` transcribes each line's window separately; that is reliable. The per-line check
  also catches script problems: the template once said "eqs dot py", which Kokoro read as "x dot pi".
- **Length.** A first beginner script for LAWFUL ran to 11 minutes of speech; trimming every line to one idea brought
  it to ~6.7 minutes of speech in a 7:52 video. Speech runs ~145 words/minute; budget words per scene.
- **Sound effects vs. narration.** Whooshes sit on the scene cut, and pops/ticks within 0.45 s of a word onset are
  dropped; they otherwise mask first words.
- **Sync.** Rather than re-authoring scenes around narration, each scene's clock is warped piecewise-linearly so
  authored moments meet their lines, with a speed cap so animation never looks rushed.
- **Figure data.** Vector figures give exact curves; rasters inverted by nearest colour are exact to < 1/255 when
  the colormap guess is right (`invert_colormap` reports the error). Tick labels can be split from their minus
  signs in the PDF text layer, so check signs against the figure.
- **Thumbnails.** Light display weights vanish at phone size; the LAWFUL thumbnail uses the heaviest Fraunces and
  drops every word that didn't survive `thumbnail_sizes.png`.
- **skia-python gotcha.** Font variation coordinates must stay referenced until `makeClone` returns, or weights
  silently fall back to regular (`core._var` keeps them alive).
- **Dependencies.** One pixi environment (`[tool.pixi.*]` in `pyproject.toml`, locked in `pixi.lock`): conda-forge for
  Python, the scientific stack, ffmpeg, tectonic, mlx, mlx-audio, misaki, spaCy and its English model, and
  PyTorch; PyPI for skia-python and mlx-whisper (not on conda-forge) and pymupdf (pixi would otherwise install
  conda's and PyPI's side by side). PyTorch must come from conda: PyPI's bundles a second OpenMP runtime that
  crashes the process. conda-forge's `spacy-curated-transformers` breaks spaCy's plugin loading, so it's left out
  (only transformer pipelines need it). Pixel output depends on skia and numpy versions: bump the lock
  deliberately and run `make check`. For F5-TTS (not used in the build): remove `torchcodec` and pin
  `torch`/`torchaudio` 2.8.
- **Refactor checks.** Splitting the engine from the LAWFUL project, renaming the package to `aiglainer`, and moving
  moving from two environments to one locked one, and then to pixi were each checked the same way: 155 sampled frames from both cuts,
  every cue and narration placement, and the final audio, compared against the original build. All identical.
