# epiplexity/pods

| name | what | length | voice, score |
|---|---|---|---|
| `episode` | From Entropy to Epiplexity: one host, AlphaZero to epiplexity and back | 25:41 | Bella blended with Nicole (`bella-nicole`), `SPEED = 0.92`, `PACE`; `encore`, no bed, `duck_db = 9` |

The owner's personal set: follow the naming rule in [../AGENTS.md](../AGENTS.md) everywhere, ID3 tags included.
`project.py` sets `SHOW` and `ARTIST` because the engine's ID3 defaults carry the pod's show name. The
closing questions are "to think about", marked `'H?'` so the show notes list them; there are no chimes.

`make plan` is for videos; an episode has no timeline until it is synthesized. To check that `episode.py` still matches
what was built, compare its lines with `lines.json` (309 sentence clips, all cached and verified on Nov 13, 2026).

The MP3 is `episode/out/podcast/Epiplexity_pod.mp3` (37,003,172 bytes, 1541.67 s, -16.2 LUFS, true peak -4.7 dBTP;
3,338 words, about 130 words a minute overall and 154 while speaking; 0 flagged; mix WER 0.003 over 3,383 words).
Published Nov 14, 2026 as feed episode 29, "Can computation create information?" (archive.org item
`epiplexity-pod`, uploaded by the user from the aigroup account). Its cover is `episode/cover.py` (1400 x 1400, the
videos' look rather than the felt robot, since this is an extra): render it with
`PYTHONPATH=. .pixi/envs/default/bin/python projects/epiplexity/pods/episode/cover.py` and copy `out/cover.png` to the
site's `images/ep029.png`.

It borrows nothing from the videos: no `SOURCES`, no shared code. The script was checked line by line against the
paper (numbers, hedges, attributions) before synthesis; `episode.py`'s docstring says where each claim traces.

## Choices

- Story spine: the AlphaZero puzzle (both classic theories seem to say it learned almost nothing), Shannon, Kolmogorov,
  the pseudorandom crack, epiplexity as a two-part code, measuring, the three puzzles, data, limits, and back to
  AlphaZero.
- Kept off air, named in the show notes: the six authors (Whisper mangles Qiu, Izmailov, Kolter), Per Martin-Löf
  ("a Swedish mathematician"), CIFAR-5M ("tiny images in the style of a classic dataset called CIFAR"), Llama, and
  "centipawn" ("judging who's ahead in a position, and by how much").
- Follows the topic's accuracy notes: Fig. 8a as five billion tokens; Fig. 8b without "10^25 FLOPs"; ADO's gains
  called small; the Fig. 4a reverse gap "widens"; the prequential estimate called a heuristic each time it matters.
- The engine's podcast mix ignores `duck_ramp` (docs/STYLES.md: podcasts follow the waveform), so music is only in
  the theme, stings and outro (`BED = 0`), with `duck_db = 9` where the voice overlaps them. The ending is the
  engine's 13 s outro, which fades over its last 5 s.

## Caveats

- Our laptop runs (`lab/`) are not in the episode: the topic file had no finished numbers when it was written.
- The closing questions are ours. "The whole zoo of creatures was what a limited observer needed" is our reading of
  Fig. 6, in line with the paper's "trading increased program length for reduced computation".
- The owner listened to it before publishing (Nov 14, 2026).
