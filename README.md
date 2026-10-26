# aiglainer

*aigspod explainers*: narrated, 1080p60 motion-graphics explainer videos in the aigspod site's dark /mull/ style,
and audio-only podcast episodes, about papers, books, or anything else worth a journal-club conversation.

Everything is generated locally, in code: skia-python draws the frames, LaTeX typesets equations, numpy
synthesizes the score and sound effects, Kokoro-82M ("Bella") narrates, Whisper checks every line, and ffmpeg
encodes.

```sh
make setup                                   # once: see Install below
make new P=mypaper TITLE="Paper Title"       # a new video from the template
make P=mypaper                               # build + verify -> projects/mypaper/out/
```

## Install

**You need** a Mac with Apple Silicon (M1 or later) on macOS 14.5+, `git` and `make` (Xcode's command-line tools:
`xcode-select --install`), and about 6 GB of disk. Narration runs on Apple's MLX, so it's Apple Silicon only;
rendering may work elsewhere but is untested.

### Option A: pixi (recommended)

[pixi](https://pixi.sh) installs everything (Python, ffmpeg, tectonic and every library) into the repo, at the exact
versions in `pixi.lock`, without touching the rest of your system. Install pixi first
([instructions](https://pixi.sh/latest/installation/)):

```sh
curl -fsSL https://pixi.sh/install.sh | sh          # or: brew install pixi
```

Then:

```sh
git clone https://github.com/aigspod/aiglainer.git
cd aiglainer
make setup          # pixi install, enable the commit guard, run `make doctor`
make P=lawful       # build the LAWFUL video to check everything works (~4 min)
```

`make` uses the pixi environment automatically; `pixi run aiglainer ...` and `pixi shell` work too.

### Option B: pip (or uv) in your own virtual environment

Use this if you'd rather not use pixi. You provide Python 3.11+, ffmpeg and tectonic (e.g. `brew install python
ffmpeg tectonic`); versions aren't pinned, so output can differ slightly from the reference build.

```sh
git clone https://github.com/aigspod/aiglainer.git
cd aiglainer
python3 -m venv .venv && source .venv/bin/activate     # any Python 3.11+
pip install -e ".[tts]"                                # or: uv pip install -e ".[tts]"
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl
git config core.hooksPath tools/hooks                  # the commit guard
make doctor                                            # checks everything; fixes espeak's data path if needed
```

With the virtual environment active, `make` uses its `python3` (or pass `make PY=/path/to/python`).

### Option C: rendering only

`pip install -e .` (no `[tts]`) is enough to render frames, previews, thumbnails and the un-narrated cut, and to
work on scenes. Narrated builds stop at `make narration` until the `tts` extra is installed.

### What gets downloaded

| what | size | when | where |
|---|---|---|---|
| pixi environment (Python, PyTorch, ffmpeg, ...) | ~2.1 GB | `make setup` | `.pixi/` in the repo |
| Kokoro-82M voice model | ~340 MB | first narration run | Hugging Face cache (`~/.cache/huggingface`) |
| Whisper large-v3-turbo | ~1.5 GB | first narration run | Hugging Face cache |
| TeX packages | ~60 MB | first `make tex` | tectonic's cache |

Fonts ship with the repo. Papers aren't included: to re-extract figure data, put the PDF in the project's `paper/`
folder (see the project's `extract_paper.py`). Run `make doctor` any time to see what's installed and what's missing.

- **[docs/SHORTS.md](docs/SHORTS.md)**: 9:16 shorts for YouTube Shorts and TikTok (`KIND = 'short'`), reusing a video's scenes.
- **[docs/PODCAST.md](docs/PODCAST.md)**: audio-only episodes (`KIND = 'podcast'`): scripts, hosts, pronunciation, writing for the ear.
- **[docs/NEW_VIDEO.md](docs/NEW_VIDEO.md)**: making a new video step by step (written for a paper; most steps apply to any topic).
- **[AGENTS.md](AGENTS.md)**: orientation and ground rules for AI agents (and people) picking up the work.
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)**: the pipeline, changing lines, timing and visuals, the pre-upload
  checklist, and the decisions behind it.

## Videos

| project | topic | video |
|---|---|---|
| [`lawful-pod`](projects/lawful-pod) | the same paper as a ~25-min audio episode (podcast) | `make P=lawful-pod`; `lawful-pod-solo` / `-duo` are 3-min pilots |
| [`lawful-short-*`](projects) | three ~45 s vertical shorts from the same paper | `make P=lawful-short-radar` (also `-twice`, `-pattern`) |
| [`lawful`](projects/lawful) | *LAWFUL: Law-Aligned Witness for Faithful Use of Latents* (Chen, Parker & Arora, ICML 2026 MI workshop, [arXiv:2607.28672](https://arxiv.org/abs/2607.28672)) | 7:52, beginner-friendly; `make CUT=full` gives the original 9-min text-only cut |

## Layout

```
aiglainer/           the engine (topic-agnostic); python -m aiglainer <command> -p <project>
  core.py, kit.py    type (site fonts + fallback), LaTeX, shapes, easing; headers, captions, axes, pills
  notes.py           handwriting, sticky notes, lamp, swash
  timeline.py        sequencing, time warps, background, HUD, story tracker
  narrated.py        time-warps scenes so their beats land on the narration
  render.py, audio.py, finish.py    frames → H.264; score + narration + ducking; loudness, captions, description
  tts.py, verify_mix.py, voices.py  Kokoro synthesis + Whisper checks; mix verification; voice auditions
  podcast.py         audio-only episodes: lines end to end, theme/stings/chimes, -16 LUFS MP3 with chapters
  hosts.py, lexicon.py              the hosts (voice, name, accent); how every host says words like "aigs"
  short.py           9:16 shorts: crops of 16:9 scenes or native vertical scenes, burned-in word captions, safe zones
  thumbnail.py, pdf.py, scaffold.py thumbnails; figure-data extraction helpers; `new`
  doctor.py, fingerprint.py         machine check (`make doctor`); regression check (`make fingerprint` / `make check`)
  fonts/             Fraunces, Inter, Space Mono, Caveat (OFL)
  template/          a complete four-scene example video, copied by `make new`
projects/
  lawful/            the LAWFUL video: settings, scenes, narration, data
tools/setup.sh       pixi install (Python, ffmpeg, tectonic, all libraries, package editable), commit guard, doctor
tools/hooks/         pre-commit: refuses media files and anything over 1 MB
```

## Accuracy notes (LAWFUL)

- Fig. 4 curves come from the PDF's vector paths. Fig. 3 spectrograms and Fig. 5 attention maps are the embedded
  viridis rasters inverted back to values (mean colour error < 1/255). Numbers come from Tables 1, 2 and 5.
- The walker, radar, trajectory and attention-head diagrams are illustrations and are labelled as such on screen.
- The paper's text says "six of the seven temporal heads" are more QK-sufficient. Its Table 2 gives 5 of 6
  temporal heads in C† (T.h4 is the exception). The video follows the table and says so.
- Paper explainers here are unofficial, not produced by the papers' authors.

## License

Code: MIT ([LICENSE](LICENSE)). Bundled fonts (Fraunces, Inter, Space Mono, Caveat) are under the SIL Open Font
License; see `aiglainer/fonts/OFL-*.txt`. Figure data under `projects/*/data/` is extracted from the cited papers
and remains credited to their authors.
