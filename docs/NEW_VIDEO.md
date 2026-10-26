# Making a new video

Written for a paper explainer, since that's what we've made so far. For a book or another topic, skip step 3
(figure data), swap "the paper" for your source (a book's argument, chapters and key passages), and keep the rest:
motivate first, give beginners the background they lack, follow a story spine, end with questions for the meeting.

The recipe that produced the LAWFUL video, as steps. Budget a few hours of iteration; the build itself takes
minutes. `projects/lawful/` is the worked example for every step.

## 1. Start the project

```sh
make new P=sparse-probing TITLE="Sparse Probing"      # copies aiglainer/template
cp ~/Downloads/paper.pdf projects/sparse-probing/paper/
make P=sparse-probing                                # builds the template video: a smoke test of the toolchain
```

## 2. Read the paper for the audience

Our journal club is mostly beginners. Before drawing anything, write down in `project.py` / a scratch note:

- **The question** the paper answers, and why anyone should care. This opens the video.
- **Background a beginner lacks.** Give each missing concept its own short primer scene before the paper's content
  (LAWFUL: *what is mechanistic interpretability*, *probes read vs. patching writes*).
- **The story spine**: the two to four stages of the argument. Put them in `STEPS` and a roadmap scene, so viewers
  always know where they are (LAWFUL: behavior → cause → mechanism).
- **The three to five results** worth a chart, each tied back to a step.
- **Limits**, and **five questions** to think about before the meeting (the video prepares the discussion, it
  doesn't replace it).
- Anything in the paper that doesn't add up. Check text against tables (LAWFUL's text and Table 2 disagreed).

## 3. Get the real numbers

Charts are redrawn from data, never traced by eye.

```sh
make inspect PDF=projects/sparse-probing/paper/paper.pdf PAGE=6
```

lists the page's coloured vector paths (data curves), embedded images (heatmaps, spectrograms) and numeric tick
labels. Write `extract_paper.py` with the helpers in `aiglainer/pdf.py` (`path_points`, `axis_map`, `image`,
`invert_colormap`) to save `data/*.json`; see `projects/lawful/extract_paper.py`. Numbers from tables can be typed
straight into the scene code with a comment naming the table.

## 4. Equations

Put them in `eqs.py` (LaTeX, with colour names from `COLORS`) and run `make tex`. Draw with `tex(c, 'key', x, y, size)`.

## 5. Scenes

One idea per scene, 15–35 authored seconds each. Start from the template's scenes and the LAWFUL ones:

| want | look at |
|---|---|
| title card with lamp and sticky note | `aiglainer/template/scenes.py` `Title`, `lawful/scenes1.py` `Title` |
| three cards that build up | `template` `Question`, `lawful` `Question`, `Roadmap` |
| equation + chart from data | `template` `Method`, `lawful` `Fig4a`, `Score` |
| box-and-arrow framework diagram | `lawful/scenes2.py` `Framework` |
| a network with a highlighted circuit | `lawful/scenes4.py` `MechInterp`, `scenes3.py` `Search` |
| bars from a table | `lawful/scenes3.py` `Probes`, `QKVal` |
| heatmaps from the paper | `lawful/scenes3.py` `Heatmaps`, `Spectrograms` |
| limits cards, discussion questions, takeaway | `lawful/scenes3.py` `Limits`, `Discussion`, `End` |

Iterate with `make preview P=... SCENE=Name T="2 8 14"`. Label anything that is an illustration rather than paper
data as `illustration` on screen.

## 6. Narration

Write `narration.py` for the ear: one idea per line, plain words, define each term the first time it appears, and
open each section by saying why we're doing it. ~145 words a minute, so a 7-minute video is ~1,000 words. Point each
beat at the moment its visual appears. Then:

```sh
make narration P=...     # synthesizes and Whisper-checks every line; fix any line it flags
make plan P=...          # check total length and that no scene runs above ~2x
```

Pick a voice with `make voices` if Bella doesn't suit.

## 7. Notes, thumbnail, description

Add at most one handwritten aside per scene in `margin_notes.py`. Draw the thumbnail in `thumbnail.py` (one focal
image, three to five big words) and check `out/thumbnail_sizes.png`. Fill `CHAPTER_TITLES` and `DESCRIPTION` in
`project.py`, including the paper citation and what is redrawn vs. illustrated.

## 8. Build and check

```sh
make P=...               # everything, ending with the mix verification
make frames P=...        # one frame per line: does each show what it says?
```

Then watch it once with sound, and follow "Before uploading" in [WORKFLOW.md](WORKFLOW.md).
