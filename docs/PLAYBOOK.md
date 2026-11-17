# Playbook: one paper, a whole set

How a full set (two videos with different angles, ~5 shorts, a podcast episode) gets made from one paper in one
session, and what we learned doing it. Written after the WeatherDreamer set (Nov 17, 2026); the epiplexity set
(Nov 13-14) used most of the same steps. [NEW_VIDEO.md](NEW_VIDEO.md), [SHORTS.md](SHORTS.md) and
[PODCAST.md](PODCAST.md) cover each kind; [PUBLISHING.md](PUBLISHING.md) covers the uploads.

## The order that worked

1. **Read the whole paper, supplement included, before anything else.** `pymupdf` is in the pixi env
   (`.pixi/envs/default/bin/python -I -c "import pymupdf ..."`); system `pdftotext` and `fitz` aren't installed.
   `grep` on the extracted text may report "Binary file matches": use `grep -a`. The supplement is where the best
   material hid (WeatherDreamer's Fig. S3: satellite stripes inside the model's memory became a whole video's spine).
2. **If the owner shares someone's review, check it line by line against the paper** and write the verdict into the
   topic `AGENTS.md` ("A reader's review, checked"). Agree where it's right, say plainly where it's incomplete or off.
   This doubles as the accuracy notes every script must respect.
3. **Write the topic `AGENTS.md` first**: the paper in one breath, numbers with section/table, accuracy notes (text vs
   tables, abstract rounding, hedges, independence of checks, conflicts of interest), "our arithmetic / our reading"
   rules, background facts safe to state, wording rules (extra vs journal club). Every later piece and agent reads it.
4. **Look up storytelling craft** (house rule; see the memory "story first"), then pick a distinct angle per piece.
   What worked: video A as a journey (problem, old way, new way, works, turn, causes, fair scoreboard, payoff); video B
   as a detective story opened on the strangest figure and closed on its explanation; the podcast as one listener and
   one image ("a dark room": predict, then correct) returned to at the end; shorts as one idea each with the hook in
   the first line.
5. **Podcast script first, then start its build in the background** (synthesis + Whisper take ~5-10 min), and send the
   script to an independent fact-checker at the same time (see below). Fixes only re-synthesize changed lines.
6. **Videos in parallel:** write one video yourself and fork the other (`Agent` with `subagent_type: "fork"`), with a
   brief that names its folder, angle, scene list, voice/score, and what not to touch. Forward the fact-checker's
   corrections to the fork with `SendMessage` as soon as they arrive.
7. **Look at every frame**: `make preview` per scene while building, then `make frames` sheets after the build. Then
   shorts (they can import the first video's kit via `SOURCES`) and `safe_*.png`.
8. **Publish** ([PUBLISHING.md](PUBLISHING.md)) and update the topic's `AGENTS.md` files with ids and links.

## Accuracy: what an independent fact-check catches

An adversarial reviewer agent (a fresh `general-purpose` agent given the paper text, the script, the show notes and
the topic `AGENTS.md`, asked for a numbered list of errors, risky simplifications and nits) found **no wrong numbers**
in the WeatherDreamer episode but eight real problems. Expect these kinds every time:
- **Something the paper does that the script says it doesn't** ("the paper never runs data denial": it removes all
  stations once). Absolute negatives need a grep.
- **A number's scope widened** ("within 10 % near the ground" was true at surface stations, not for ocean winds;
  "moisture within 25 %" was the microwave channels only).
- **Our reasoning presented as the paper's** (our jet-crossing arithmetic stated as the cause). Label it on screen and
  say "by our arithmetic" / "in our reading" aloud.
- **Hedges dropped** ("ignores" for a gain of 0.1-0.26; "better calibrated" without "all three still overconfident").
- **Caveats that cut only one way**: list the ones that favour the baseline too.
- **Missing prior work** that makes the novelty claim sound bigger than it is.
Apply the fixes to every piece, not only the one checked.

## Figures

- `make inspect PDF=... PAGE=N` tells you whether a figure is vector (extractable curves) or a raster image. If every
  page lists only `images`, there is no data to extract: write an `extract_paper.py` that saves the embedded images to
  the topic's `data/figs/` (gitignored), show them as labelled crops (`figcard`), and draw charts only from numbers in
  the text and tables, with the section on screen.
- Use the source figure's colours for systems that appear in both a crop and a redrawn chart (WeatherDreamer blue,
  GEFS orange, IFS green), or viewers can't map one onto the other.
- Find crop rectangles by saving a downscaled preview (`sips -Z 1200`) and reading it; check each crop in `make
  preview`, since text labels placed under a crop collide with it when its aspect ratio is not what you guessed.

## Narration and Whisper

- A CamelCase name ("WeatherDreamer") is heard as two words and fails short lines: say "the model" / "it" in short
  sentences, keep the name for long ones. Years as digits ("2020"), not words. "1,600" is not "sixteen hundred" to the
  checker: write "one thousand six hundred". Homophones that flagged: "taught it the" → "taught at the", "low air a
  patch" → "low era patch". Rephrase; never loosen the check.
- Spell names Whisper mangles only on screen and in show notes.

## Layout bugs that recur

Labels placed at a fixed y under a crop whose height you didn't compute; a 3-digit hex colour (`'#111'` crashes:
use `'#111111'`); text wider than the 720 px short box; a margin note landing on a label; an animated curve crossing
its own caption. All were caught only by looking at previews.

## Housekeeping

- Before a piece: branch `mahf708/<topic>` (owner's handle, never "naser"). Don't commit media, PDFs or `data/figs`.
- Topic `AGENTS.md` + each kind's `AGENTS.md` (table of pieces, caveats, "what Whisper mishears", build numbers, what
  nobody has checked yet), and add the topic to the README's project table.
- Podcast covers carry "the aigs pod · episode N" (owner's request, Nov 17, 2026). The next N is one more than the last
  `<itunes:episode>` in `aigspod.github.io/feed.xml`.
