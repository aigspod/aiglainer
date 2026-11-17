# weatherdreamer/shorts

Five 9:16 shorts for arXiv:2611.18393v1. Facts, accuracy notes and the wording rule (an aigs pod extra, not journal
club): [../AGENTS.md](../AGENTS.md).

| name | upload title / headline | hook (first line) | scenes (native, `wdshorts.py`) | voice, score |
|---|---|---|---|---|
| `now` | Nobody can see now | every forecast starts from right now, and nobody can see it | `NowClues` (globe of clues, illustration), `NowCycle` (6-hourly and late vs hourly in ~1.5 min) | `bella-nicole`, `daylight` |
| `stripes` | Its memory holds stripes | the inside of a weather model's memory | `StripesMemory` (Fig. S3a crop and zooms), `StripesWhy` (h vs z, Fig. S3b) | `michael`, `mysterium` |
| `trust` | Nobody told it whom to trust | 20° forecast, 22° thermometer: how far do you move? | `TrustGain` (k = 0.8, illustration), `TrustLearned` (§4.3.3 numbers) | `bella-nicole`, `silencia` |
| `limb` | Satellites see colder at the edge | straight down sees deep; a slant sees higher, colder air | `LimbSlant` (illustration), `LimbFix` (Fig. S7 crops, §4.4 corrections) | `michael`, `analog` |
| `walls` | Strong below, weak above | within ten percent of NOAA at surface stations | `WallsRatio` (Table 2), `WallsCauses` (patches, our arithmetic, gains aloft) | `bella-nicole`, `dawn` |

Every short: `KIND = 'short'`, `SOURCES = ['weatherdreamer/videos/loop']` (the topic kit `loopkit.py`), HUD
`weatherdreamer`, CITE `duffy, penn, ballard, posch & vandal · arxiv 2611.18393`, `MUSIC` `duck_db = 9`, `duck_ramp =
1.2`; the first scene holds 0.5 s, the last 2.4 s. Each `DESCRIPTION` says what is paper data, a crop, an illustration
or our arithmetic. `project.py` puts `shorts/` on `sys.path` so `wdshorts.py` is found.

Built Nov 17, 2026: 0 flagged in all five; mix WER now 0.000, stripes 0.000, trust 0.000, limb 0.009, walls 0.021;
37-47 s of speech each. `safe_*.png` checked (three were re-laid out after the first look: a label past the box edge in
`now`, a label on a crop in `stripes`, labels inside the figure cards in `limb`). Nobody has listened or watched on a
phone. Published Nov 17, 2026 on The AIGS Pod (public, English captions): now PByGHzEwvrg, stripes GVrPWBWMOv4, trust
gE3OIHEmeoQ, limb 6eRu23FOqnQ, walls 2mrBGcQ9yeo (youtube.com/shorts/<id>).
