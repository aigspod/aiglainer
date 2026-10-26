# aiglainers

*aigspod explainers*: narrated, 1080p60 motion-graphics explainer videos in the aigspod site's dark /mull/ style,
about papers, books, or anything else worth a journal-club conversation. The first explains a research paper.

Everything is generated locally, in code: skia-python draws the frames, LaTeX typesets equations, numpy
synthesizes the score and sound effects, Kokoro-82M ("Bella") narrates, Whisper checks every line, and ffmpeg
encodes.

```sh
make setup                                   # once (macOS, Apple Silicon; needs uv, ffmpeg, tectonic)
make new P=mypaper TITLE="Paper Title"       # a new video from the template
make P=mypaper                               # build + verify -> projects/mypaper/out/
```

- **[docs/NEW_VIDEO.md](docs/NEW_VIDEO.md)**: making a new video step by step (written for a paper; most steps apply to any topic).
- **[docs/WORKFLOW.md](docs/WORKFLOW.md)**: the pipeline, changing lines, timing and visuals, the pre-upload
  checklist, and the decisions behind it.

## Videos

| project | topic | video |
|---|---|---|
| [`lawful`](projects/lawful) | *LAWFUL: Law-Aligned Witness for Faithful Use of Latents* (Chen, Parker & Arora, ICML 2026 MI workshop, [arXiv:2607.28672](https://arxiv.org/abs/2607.28672)) | 7:52, beginner-friendly; `make CUT=full` gives the original 9-min text-only cut |

## Layout

```
explainer/           the engine (topic-agnostic); python -m explainer <command> -p <project>
  core.py, kit.py    type (site fonts + fallback), LaTeX, shapes, easing; headers, captions, axes, pills
  notes.py           handwriting, sticky notes, lamp, swash
  timeline.py        sequencing, time warps, background, HUD, story tracker
  narrated.py        time-warps scenes so their beats land on the narration
  render.py, audio.py, finish.py    frames → H.264; score + narration + ducking; loudness, captions, description
  tts.py, verify_mix.py, voices.py  Kokoro synthesis + Whisper checks; mix verification; voice auditions
  thumbnail.py, pdf.py, scaffold.py thumbnails; figure-data extraction helpers; `new`
  fonts/             Fraunces, Inter, Space Mono, Caveat (OFL)
  template/          a complete four-scene example video, copied by `make new`
projects/
  lawful/            the LAWFUL video: settings, scenes, narration, data
tools/setup.sh       creates .venv and .venv-tts, installs the package (editable), enables the commit guard
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
License; see `explainer/fonts/OFL-*.txt`. Figure data under `projects/*/data/` is extracted from the cited papers
and remains credited to their authors.
