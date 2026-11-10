# aiglainer

*aigspod explainers*: narrated, 1080p60 motion-graphics explainer videos in the aigspod site's dark /mull/ style,
and audio-only podcast episodes, about papers, books, or anything else worth a journal-club conversation.

Everything is generated locally, in code: skia-python draws the frames, LaTeX typesets equations, numpy
synthesizes the score and sound effects, Kokoro-82M ("Bella") narrates, Whisper checks every line, and ffmpeg
encodes.

```sh
make setup                                           # once: see Install below
make new P=mypaper/videos/main TITLE="Paper Title"   # a new video from the template
make P=mypaper/videos/main                           # build + verify -> projects/mypaper/videos/main/out/
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
make P=lawful/videos/explainer       # build the LAWFUL video to check everything works (~4 min)
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
| Music Flamingo (optional) | ~16 GB | first `make listen` | Hugging Face cache |
| TeX packages | ~60 MB | first `make tex` | tectonic's cache |

Fonts ship with the repo. Papers aren't included: to re-extract figure data, put the PDF in the project's `paper/`
folder (see the project's `extract_paper.py`). Run `make doctor` any time to see what's installed and what's missing.

- **[docs/STYLES.md](docs/STYLES.md)**: make it your own: colours, background, typefaces, voices, your own music. The pod's look is only the default.
- **[docs/SHORTS.md](docs/SHORTS.md)**: 9:16 shorts for YouTube Shorts and TikTok (`KIND = 'short'`), reusing a video's scenes.
- **[docs/PODCAST.md](docs/PODCAST.md)**: audio-only episodes (`KIND = 'podcast'`): scripts, hosts, pronunciation, writing for the ear.
- **[sketches/scores/](sketches/scores/README.md)**: the prototypes of five score styles after music we love (Richter, Jarrett, Martin Roth, Hammock), now `MUSIC['style']` options.
- **[docs/NEW_VIDEO.md](docs/NEW_VIDEO.md)**: making a new video step by step (written for a paper; most steps apply to any topic).
- **[AGENTS.md](AGENTS.md)**: orientation and ground rules for AI agents (and people) picking up the work.
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)**: the pipeline, changing lines, timing and visuals, the pre-upload
  checklist, and the decisions behind it.

## Projects

Everything we've made, under `projects/<topic>/{videos,shorts,pods}/<name>/`. [projects/AGENTS.md](projects/AGENTS.md) says how
it's organized and how to commit; each folder has its own `AGENTS.md`. Build any of them with `make P=<path>`.

| topic | source | what's there |
|---|---|---|
| [`lawful`](projects/lawful/AGENTS.md) | *LAWFUL: Law-Aligned Witness for Faithful Use of Latents* (Chen, Parker & Arora, ICML 2026 MI workshop, [arXiv:2607.28672](https://arxiv.org/abs/2607.28672)) | a 7:52 video (`videos/explainer`, `make CUT=full` gives the original 9-min cut), a ~27-min episode and two pilots (`pods/`), five shorts |
| [`errors`](projects/errors/AGENTS.md) | *Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?* (Zhang, Geng et al., 2026, [arXiv:2609.35686](https://arxiv.org/abs/2609.35686)) | three standalone videos and a six-minute cut, a ~24-min episode, seven shorts |
| [`dynamics`](projects/dynamics/AGENTS.md) | *A Mechanistic Analysis of Transformers for Dynamical Systems* (Duthé, Evangelou et al., 2025, [arXiv:2512.21113](https://arxiv.org/abs/2512.21113)) | three standalone videos and a six-minute cut, a ~21-min episode, six shorts |
| [`examples`](projects/examples/AGENTS.md) | how to use the engine | `videos/light`: a different look from settings alone |

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
  listen.py          `make listen`: ask NVIDIA Music Flamingo about a render (a dev tool, never in a build)
projects/            <topic>/{videos,shorts,pods}/<name>/, an AGENTS.md at each level (see projects/AGENTS.md)
tools/setup.sh       pixi install (Python, ffmpeg, tectonic, all libraries, package editable), commit guard, doctor
tools/hooks/         pre-commit: refuses media files and anything over 1 MB
```

Paper explainers here are unofficial, not produced by the papers' authors. Each topic's `AGENTS.md` keeps its accuracy notes.

## License

Code: MIT ([LICENSE](LICENSE)). Bundled fonts (Fraunces, Inter, Space Mono, Caveat) are under the SIL Open Font
License; see `aiglainer/fonts/OFL-*.txt`. Figure data under `projects/*/data/` is extracted from the cited papers
and remains credited to their authors.
