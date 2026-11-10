# projects/: how work is organized and committed

For people and agents. Read the repo's [AGENTS.md](../AGENTS.md) first, then the `AGENTS.md` in the topic you are
working in. The engine in `aiglainer/` never knows about any of this content.

## Layout

```
projects/<topic>/              one paper, book or subject
  AGENTS.md                    the source, what exists, shared code, accuracy notes
  videos/<name>/               16:9 explainers (docs/NEW_VIDEO.md)    KIND = 'video' (the default)
  shorts/<name>/               9:16 shorts of 30-45 s (docs/SHORTS.md)     KIND = 'short'
  pods/<name>/                 audio-only episodes (docs/PODCAST.md)  KIND = 'podcast'
```

Each of `videos/`, `shorts/` and `pods/` has its own `AGENTS.md`: what is in it, and what to know before changing it.
Skip a kind the topic doesn't have.

The full path is the project's name: `make P=errors/shorts/sara`, `SOURCES = ['errors/videos/gap']`.
Names are lowercase with `-`: the topic is short and recognizable (`lawful`, `errors`); `name` says what the piece is.

## Starting something

- **New topic, first video:** `make new P=<topic>/videos/<name> TITLE="..."` copies the template. Then write
  `projects/<topic>/AGENTS.md` and `videos/AGENTS.md`, modelled on [errors/](errors/AGENTS.md).
- **New short or podcast:** there is no template for these. Copy the closest sibling (`lawful/shorts/twice`,
  `lawful/pods/episode`), or follow docs/SHORTS.md and docs/PODCAST.md.
- **Reusing another piece's scenes or data:** list it in `SOURCES`, and subclass its scenes rather than copying them.
  `SCENE_MODULES` is searched in order, so your own module goes first. Override `chapter` and the like in a subclass;
  a change to shared scene code changes every piece that uses it (each topic's `AGENTS.md` says which).

Add the piece to the lists in its kind's `AGENTS.md` when you add it.

## House rules for what we make

These are the pod's. The dark /mull/ look and our scores are the default; [docs/STYLES.md](../docs/STYLES.md) says how to change them.

- **Endings:** leave 1-2 s after the last line for the picture and music to fade out; set the last scene's `hold`.
- **Short titles:** 5-6 words at most, on screen (`headline`) and in the upload title.
- **Music sits well under the host.** Raise it only rarely, on purpose: a title card, a turn, the outro. Set
  `MUSIC['duck_db']` (`make new` starts at 16); without it, music averages only about 6 dB under speech and swells between words.
  Keep the changes gentle so the music always feels like background: `duck_ramp` (about 1.2 s) with a `duck_db` of 8-10
  fades smoothly and stays down through short pauses, where `duck_db` alone steps 16 dB at every line.
- **Accuracy:** never draw data by eye; label illustrations on screen; say so when a paper's text and tables disagree;
  note it in the topic's `AGENTS.md`. Have scripts reviewed against the source before synthesizing (docs/PODCAST.md).

## Committing

Commit what rebuilds the piece, and nothing it can regenerate:

| commit | don't commit (ignored or refused) |
|---|---|
| `project.py`, `narration.py` / `episode.py`, scenes, `eqs.py`, `thumbnail.py`, `extract_paper.py` | `out/`, `cache/`, `__pycache__/` |
| `lines.json`, `tex/*.png`, `data/*.json` (so a fresh clone builds without the PDF or a narration run) | MP4, MP3, WAV and other media |
| the `AGENTS.md` files you changed | papers (`paper/*.pdf`), anything over 1 MB |

- **One thing per commit,** and start the subject with the path: `errors/shorts/sara: shorter headline`. Separate
  content from engine changes, so a content commit never changes another topic.
- **Before committing:** the piece builds with `make P=<path>` ending in `0 flagged` and a mix WER near zero; you looked
  at `make frames` (and `safe_*.png` for shorts). Say what you could not check: nobody has heard it until a person has.
- **Engine changes:** `make fingerprint P=lawful/videos/explainer` before, `make check P=...` after must print `IDENTICAL`.
- **The guard:** `make setup` enables `tools/hooks/pre-commit`, which refuses media and big files. Don't use `--no-verify`.
- **Branch, then ask before pushing.** The repo is public. Use `<github-handle>/<topic>` for branches.
