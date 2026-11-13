# cldiff

*Adaptive conditional latent diffusion maps beam loss to 2D phase space projections*, A. Scheinker & A. Williams
(Los Alamos), 2025, [arXiv:2502.18684](https://arxiv.org/abs/2502.18684). Unofficial, not produced by the authors.
Layout and commit rules: [../AGENTS.md](../AGENTS.md).

| kind | what |
|---|---|
| [videos/](videos/AGENTS.md) | a journal-club explainer |

Shared code: `videos/explainer/cldkit.py` (`figcard` for paper-figure crops, beamline, 8x8x3 latent grid, chip vectors).

## Accuracy notes

- The paper's figures are raster images. `videos/explainer/extract_paper.py` crops them from the PDF into `data/fig*.png`
  (300 dpi, captions excluded; kept out of git like the PDF, as the paper is under arXiv's non-exclusive licence);
  scenes show them as crops labelled "Fig. N", never redrawn.
- The `Errors` bars are typed from the **legends of Fig. 8** (mean absolute % error, train/test): VAE 15.67/15.55,
  latent diffusion 8.07/14.05 (on latents, not images), full chain 16.53/23.79. Narration rounds to 16 / 17 / 24 %.
- The beam currents `b_m` are computed by summing the simulated (z, pz) projection (Eq. 2), not read from real
  monitors, although the title says "beam loss". `Signals` and `Limits` say so.
- The text cites "Figure 2" for the overview that is actually Fig. 1; the video uses the figure numbers as printed on figures.
- Results on the unseen 4th initial condition aren't reported separately; tracking (Fig. 12) is three examples. Said in `Limits`.
- Monitor readouts in `Question`, the latent grids and noising in `Diffuse`/`Compress`, the extremum-seeking toy in
  `Adaptive` (Eq. 22 on a 2D quadratic cost) and the square/circle shadows in `Tracking` are illustrations, labelled on screen.

## What Whisper mishears here

"autoencoder" in a short line came out as "Archwing coder" (reworded to "the compression step"); "U-Net" is voiced as
"you net" via `SAY` and heard as "UNET". "Los Alamos" is voiced as "Loss Alamos". Avoid saying "LANSCE".
