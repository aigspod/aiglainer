# lawful/videos

| name | what | build |
|---|---|---|
| `explainer` | 7:52, beginner-friendly, Bella; `make CUT=full` gives the original 9-minute text-only cut | `make P=lawful/videos/explainer` |

The worked example for every step of docs/NEW_VIDEO.md. Its scenes (`scenes1-4.py`) are borrowed by the shorts, so check
`../shorts/` after changing one. To re-extract figure data, put the PDF in `explainer/paper/` and run `make data`.
