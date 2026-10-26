# AGENTS.md

Guidance for AI agents (and people) picking up work in this repo. Read this first, then
[docs/WORKFLOW.md](docs/WORKFLOW.md) (how a video is built and changed) and [docs/NEW_VIDEO.md](docs/NEW_VIDEO.md)
(how to make a new one).

## What this is

`aiglainer` (aigspod explainers) makes narrated 1080p60 motion-graphics explainer videos, entirely in code, for the
aigs pod journal club: papers first, books and other topics later. The audience is mostly **beginners**: every
video motivates its question, gives the background a newcomer lacks, follows a visible story spine, defines terms
as they appear, and ends with questions to think about *before* the meeting (the video prepares the discussion; it
doesn't replace it).

- `aiglainer/` is the engine (a Python package and the `aiglainer` command). It knows nothing about any one video.
- `projects/<name>/` is one video: `project.py` (settings), `narration.py`, `scenes*.py`, `margin_notes.py`,
  `thumbnail.py`, `eqs.py`, `data/`. `projects/lawful/` is the complete reference video.
- `aiglainer/template/` is the starter project copied by `make new`.

## Setup and commands

macOS 14.5+ on Apple Silicon only (mlx narration, SF Pro font fallback). The only prerequisite is
[pixi](https://pixi.sh): `pixi install` brings Python, ffmpeg, tectonic and every library into
`.pixi/envs/default`, and the Makefile runs everything from there.

```sh
make setup                      # once: pixi install (+ commit guard)
make P=<name>                   # full build: tex, narration, video, audio, finish, verify, thumbnail (~4 min for LAWFUL)
make plan P=<name>              # timing plan, instant: use it after every narration edit
make preview P=<name> SCENE=X T="2 8 14"   # render one scene at authored times -> out/prev/X.png
make frames P=<name>            # one captioned frame per narration line -> out/narrated/qa/sheet_*.png
make new P=<name> TITLE="..."   # new project from the template
make inspect PDF=... PAGE=N     # find data curves, images and tick labels in a paper's figure
make help                       # everything else
```

Everything also runs as `pixi run aiglainer <command> -p <name>` (or `pixi run python -m aiglainer ...`).

## How to work here

- **Look at what you make.** After drawing or retiming anything, render it (`make preview`, `make frames`,
  `make thumbnail`) and open the PNGs. Most bugs in this repo were visual (overlaps, text off-canvas, a beat landing
  before its visual, glyph boxes) and no test catches them.
- **Never draw data by eye.** Charts are redrawn from numbers extracted from the source (`aiglainer/pdf.py`,
  `projects/lawful/extract_paper.py`) or typed from tables with a comment naming the table. Label anything that is
  only an illustration as `illustration` on screen. Cross-check the paper's text against its tables and say so on
  screen when they disagree.
- **Narration is the spine.** Edit `narration.py`; beats are `(authored_time, text)`, pointed at the moment the
  visual appears. ~145 spoken words per minute; one idea per line; plain words; spell symbols out ("alpha", "tau").
  `make narration` fails if Whisper hears a line differently from the script: rephrase the line (or add a respelling
  to `SAY`) rather than loosening the check.
- **Animate from time.** Every scene draws from `ramp`/`window` of its authored time `t`, never from frame counters
  or state, so the narrated cut can time-warp it.
- **Keep the style.** The aigspod site's dark /mull/ look: Fraunces headings with one `*amber italic*` word and a
  swash, Inter body text, lowercase Space Mono labels, Caveat handwriting only for asides (at most one per scene),
  the lamp and sticky-note doodles, colour tokens from `aiglainer/core.py` `PAL`. Data colours follow the source
  figure's colours.
- **Engine changes must not change existing videos** unless that's the point. Before touching `aiglainer/`, run
  `make fingerprint P=lawful`; after, `make check P=lawful` must print `IDENTICAL`. For audio, compare
  `out/narrated/audio.wav` with `cmp` before and after.
- **Done means verified.** A build is done when `make P=<name>` ends with `0 flagged` (narration) and a mix WER
  near zero (verify), the `make frames` sheets show each line's visual, and `out/thumbnail_sizes.png` still reads
  at the smallest size. Report anything you could not check: nobody has *listened* unless a human did.

## Things that will bite you

- **Whisper quirks.** Long-form transcription of the mix loops and drops words; `verify_mix.py` therefore
  transcribes line by line. It can still drop a lone opening word under music ("Limits.") that is plainly
  audible: retry with context before rewriting the line. Kokoro clips start with ~0.4–0.7 s of silence.
- **Sound effects mask words.** Whooshes go on scene cuts; pops/ticks near a word onset are dropped automatically.
  Don't add cues on narration onsets.
- **skia-python font variations.** Variation coordinates must stay referenced until `makeClone` returns or weights
  silently reset to regular (`core._var` handles it). Light Fraunces weights vanish at thumbnail size.
- **Missing glyphs.** Site fonts lack Greek and arrows; `core.runs` falls back per character. If you see boxes,
  something bypassed `text()`.
- **Imports.** A project's folder is put on `sys.path`, so its modules import each other plainly (`import walker`)
  while engine modules are imported as `aiglainer.<module>`. Don't name project modules after engine modules.
- **Environment.** pixi, configured in `pyproject.toml` under `[tool.pixi.*]`, locked in `pixi.lock`. Most packages
  come from conda-forge; skia-python, mlx-whisper and pymupdf come from PyPI (see the comments there for why).
  Keep PyTorch on conda-forge: a PyPI torch brings its own OpenMP runtime and crashes the process (`OMP: Error #15`).
  Don't add `spacy-curated-transformers`: conda-forge's build breaks spaCy's plugin loading and we don't use it.
  Bump the lock deliberately: pixels depend on skia and numpy versions, so run `make check` after.

## Git

- Never commit media, papers or build outputs: `.gitignore` covers them and `tools/hooks/pre-commit` (enabled by
  `make setup`) refuses media, PDFs and files over 1 MB. Don't bypass it with `--no-verify`.
- `lines.json`, `tex/*.png` and `data/*.json` are committed on purpose: a fresh clone builds without the paper PDF,
  tectonic or a fresh narration run.
- The repo is public (`aigspod/aiglainer`). Ask before pushing, and keep commits small and descriptive.
