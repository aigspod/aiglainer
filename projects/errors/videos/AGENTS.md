# errors/videos

| name | what | length | voice, score |
|---|---|---|---|
| `distilled` | the whole paper in about six minutes | 6:27 | Michael, `silencia` |
| `gap` | the measurement: circuits, two piles, Table 1 | 4:30 | Bella, `encore` |
| `excuses` | can the gap be explained away? Fig. 1, close calls, the nudge | 4:32 | Bella, `analog` |
| `wrongname` | what was missing: the 63 additions and two paths | 5:13 | Bella, `mysterium` |

Each stands alone: don't write "last time" or "next time". `excuses` and `wrongname` reuse `gap`'s scenes for their setup.
`distilled` has no scenes of its own beyond a title and ending: `distilled.py` subclasses the others to renumber them.

Section numbers are overridable: scenes read `getattr(self, 'NUM', '01')`, so subclasses set `chapter` and `NUM`.
`scenes3.PathOne` has `PCT_RIGHT`, used by `shorts/bone`; off by default so the videos don't change.

Built before the end-fade and quieter-music rules in `../../AGENTS.md`; those aren't applied yet.
