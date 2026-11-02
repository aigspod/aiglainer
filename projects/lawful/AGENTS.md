# lawful

*LAWFUL: Law-Aligned Witness for Faithful Use of Latents*, Kevin Chen, Kenneth W. Parker, Anish Arora. Mechanistic
Interpretability Workshop, ICML 2026. [arXiv:2607.28672](https://arxiv.org/abs/2607.28672). Journal club Oct 28, 2026.
These are unofficial, not produced by the authors. Layout and commit rules: [../AGENTS.md](../AGENTS.md).

| kind | what |
|---|---|
| [videos/](videos/AGENTS.md) | `explainer`, the complete reference video |
| [shorts/](shorts/AGENTS.md) | five shorts borrowing from the explainer |
| [pods/](pods/AGENTS.md) | the full episode and two pilots |

**Shared code:** every short lists `SOURCES = ['lawful/videos/explainer']`, so changes to its scenes or data reach them.
This is also the repo's regression project: `make fingerprint` / `make check` use `lawful/videos/explainer`.

## Accuracy notes

- Fig. 4 curves come from the PDF's vector paths; Fig. 3 spectrograms and Fig. 5 attention maps are the embedded viridis
  rasters inverted back to values. Numbers come from Tables 1, 2 and 5.
- The walker, radar, trajectory and attention-head diagrams are illustrations, labelled so on screen.
- The paper's text says "six of the seven temporal heads" are more QK-sufficient; its Table 2 gives 5 of 6 temporal heads
  in C† (T.h4 is the exception). We follow the table and say so.
- The "doubled frequency" network is a hypothetical counterexample to the metric, not the paper's model. Say so.
- The climate-emulator passage in the episode is our extrapolation, labelled on air.
