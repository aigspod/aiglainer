# errors

*Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?*, Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke
Zhang, Haolin Ye, Xujie Si (2026). Preprint, [arXiv:2609.35686](https://arxiv.org/abs/2609.35686). Journal club Nov 4,
2026; feed episode 27. These are unofficial, not produced by the authors. Layout and commit rules: [../AGENTS.md](../AGENTS.md).

| kind | what |
|---|---|
| [videos/](videos/AGENTS.md) | three standalone explainers and a six-minute cut |
| [shorts/](shorts/AGENTS.md) | seven shorts of about 30 s |
| [pods/](pods/AGENTS.md) | the 24-minute episode |

**Shared code lives in `videos/gap/`,** and nearly everything depends on it:
`errkit.py` (head grid, bars, title and end cards), `errshorts.py` (native 9:16 scenes), `scenes.py`, `data/fig1.json`.
Changing those can change every video and short; rebuild and check whatever lists `errors/videos/gap` in `SOURCES`.

## Accuracy notes

- Bars are typed from Tables 1, 4, 7 and 8. Fig. 1 is redrawn from the PDF's vector paths (`videos/gap/extract_paper.py`);
  its tick calibration reproduces the text's Llama numbers (80.0 / 54.9 at 2%).
- **Text and figure disagree:** the text's Gemma ARC-Challenge 80.3% / 54.4% at a 1% budget doesn't match Fig. 1's plotted
  points. The videos show the curves and don't quote that pair. (The podcast quotes the text.)
- **Text and numbers disagree:** Llama ARC-Challenge at 2% (80.0 overall, 46.7 matched, 54.9 errors) implies a reversed gap;
  the paper calls it "narrowed". We say both.
- Table 4: the 0.41-point drop on correct agreement was 0.85 on a fresh 5,200-prompt check, past the search's 0.5 tolerance.
- Fig. 2's attention percentages are for its two example prompts only; say so. Only five of the 63 added head-positions are
  named in the paper, so the search-space picture is an illustration.
- The dot field, the score bars in `CloseCalls` and the tiles in `Nudge` are illustrations, labelled on screen.
- The climate-emulator passages are our extrapolation, labelled so.

## What Whisper mishears here

"route" (root), "additions" (editions), "versus" (verses), "two" (too), "Li Zhang" (Lijiang), "thirty-five hundred"
(writes 3,500), and sometimes "IOI". "Sara" becomes "Sarah", which costs one word and is fine in a long line. Write
`GPT-2`, `IOI`, `ACDC` as such in the text and let `SAY` handle the speech.
