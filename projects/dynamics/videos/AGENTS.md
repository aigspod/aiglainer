# dynamics/videos

| name | what | length | voice, score |
|---|---|---|---|
| `distilled` | the whole paper in about six minutes | 6:38 | Michael, `daylight` |
| `sign` | attention can only average: the sign problem, two heads, two masses (§2.3, §3.1, App. A.1, §3.2) | 4:55 | Bella, `encore` |
| `hidden` | rebuilding a hidden state: Van der Pol, Takens, Table 1 (§4.1) | 4:54 | Bella, `analog` |
| `unfold` | room to unfold: Chafee-Infante, cylinder flow and the Reynolds number, our emulator extrapolation (§4.2, §4.3) | 5:12 | Bella, `mysterium` |

Lengths are the timeline (`make plan`), which the final MP4 matches.
All set `MUSIC['duck_db'] = 16` and end on a hold of 2.5-3.0 s.

Each stands alone: don't write "last time" or "next time".

**Shared code lives in `sign/`:** `dynkit.py` (headers via `hdr`, the `sim_label` / `illustration` / `extrap_label`
tags, `convex_mix`, spring-mass drawings, trace, spectrum, phase and latent-loop plots, bar charts, title and end cards), `simulate.py` (writes `data/sdof.json`, `twodof.json`, `vdp.json` from the paper's equations), and the
shorts' native scenes `dynshorts.py` and `dynshorts2.py`. `unfold/` has its own `simulate.py` for `data/ci.json` (our
Chafee-Infante run) and the scenes the Chafee-Infante and cylinder shorts reuse. A change to `dynkit.py` can change
every video and short in the topic.

What each borrows:

- `sign`: nothing; it hosts the kit.
- `hidden`: `SOURCES = ['dynamics/videos/sign']` for `dynkit.py` and `vdp.json`.
- `unfold`: `SOURCES = ['dynamics/videos/sign']` for `dynkit.py`; its own `ci.json`.
- `distilled`: all three. It has no scenes of its own beyond `Title`, `Table1`, `Discussion` and `End`: `distilled.py`
  subclasses the parts' scenes to renumber them (`chapter`, `NUM`; headers read `getattr(self, 'NUM', ...)` through
  `dynkit.hdr`). It opens on `unfold.ColdOpen` and takes `Recipe`, `OneHead`, `Springs`, `TwoHeads`, `TwoMasses` from
  `sign`, `Hide`, `Takens`, `Table1` from `hidden`, and `Room`, `Loops`, `Recon`, `Lesson`, `Emulators` from `unfold`.
  All three parts name their module `scenes.py`, so `distilled.py` loads each from its file under its own module name
  rather than with `import scenes`. Its `Table1` adds the text-vs-table note on positional encoding (the part makes
  that point in `hidden.Attention`, which the cut drops). A change to a part's scene changes `distilled` too.

## Caveats

- `hidden/tex/takens.png` and `unfold/tex/takens.png` differ; SOURCES order makes the key resolve to hidden's, so don't
  add `unfold.Latent` to the cut without renaming one of them.
- Descriptions cite the paper as 2025 (arXiv v1, 2512); the on-screen line says v2 2026.
- Every simulation is labelled on screen as ours; the emulator scene in `unfold` is labelled our extrapolation.
- Built Nov 9, 2026: `sign` (mix WER 0.000), `hidden` (0.001), `unfold` (0.003) and `distilled` (0.004 over 819 words)
  end with 0 flagged after the review fixes. Nobody has listened to any of them yet.
