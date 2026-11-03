# lem

*Advancing Accelerator Virtual Beam Diagnostics through Latent Evolution Modeling: An Integrated Solution to Forward,
Inverse, Tuning, and UQ Problems*, M. Rautela & A. Scheinker (Los Alamos), NAPAC2025, Sacramento,
[arXiv:2602.22618](https://arxiv.org/abs/2602.22618). Unofficial, not produced by the authors.
Layout and commit rules: [../AGENTS.md](../AGENTS.md).

| kind | what |
|---|---|
| [videos/](videos/AGENTS.md) | a journal-club explainer |

Shared code: `videos/explainer/lemkit.py` (boxes, curved arrows, synthetic phase-space tiles, latent vectors, beamline).

## Accuracy notes

- The paper is a three-page summary with **no figures or tables**. Every beam image, latent vector, trajectory and
  landscape is an illustration (synthetic Gaussians), labelled `illustration` on screen; the video quotes no numbers.
- **Equation and text disagree:** Eq. (1) is printed in first-order (Markov) form, `P(z_t | z_{t-1})`, but the text says
  the model uses the full chain rule, AR(1:T). The `Evolve` and `Limits` scenes say so.
- The 8-dimensional latent drawn on screen is the paper's own example size (p. 3). Results the paper mentions (several
  optima in tuning, beating high-dimensional optimizers) come from its refs. 32–37; the video attributes them.

## What Whisper mishears here

"Los Alamos" is voiced as "Loss Alamos" via `SAY`. Author names stay on screen, not in the voice.
