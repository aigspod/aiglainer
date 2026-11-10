# dynamics/pods

| name | what | length | voice, score |
|---|---|---|---|
| `episode` | What does attention do with a dynamical system? Feed episode 28 | 20:57 | Bella, `silencia` with a faint bed (`BED = 0.1`, `duck_db = 16`) |

`make plan` is for videos; an episode has no timeline until it is synthesized. To check that `episode.py` still matches
what was built, compare its lines with `lines.json` (155 lines, all cached and verified on Nov 9, 2026).

The MP3 is `episode/out/podcast/Dynamics_pod.mp3` (30,184,564 bytes, 1257.57 s, -16.2 LUFS, true peak -5.3 dBTP;
mix WER 0.003 over 3,327 words). It is to be published at `https://archive.org/download/dynamics-pod/Dynamics_pod.mp3`,
and the feed entry in aigspod.github.io records its exact byte length. Rebuilding changes the file: re-upload it and
update the feed's `length`. The episode art is `episode/ART_PROMPT.md` until the image exists.

It borrows nothing from the videos: no `SOURCES`, no shared code. The script was reviewed against the paper
(claims, hedges, numbers) and for the ear before synthesis, and the fixes were applied; `episode.py`'s docstring
says where claims trace.

## Caveats

- The emulator segment is labelled on air as our extrapolation. "Many emulators, including ones we work with, aren't
  even transformers" and the Reynolds-number gloss are our own background, not the paper's; the sixty/forty sign
  example is our illustration.
- The topic's accuracy notes ([../AGENTS.md](../AGENTS.md)) are said on air and in the show notes: the 2-DOF frequencies,
  positional encoding (text vs Table 1), and "consistent with" Takens rather than "confirm".
- The citation says 2025 (arXiv 2512, v2 2026), as the site's reading list does; the videos and shorts now match.
- Lines that pass with a word off (WER 0.03-0.09) are listed in the topic's "What Whisper mishears here".
- Nobody has listened to it: not the mix, the bed, or the outro fade.
