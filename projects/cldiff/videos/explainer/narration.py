"""Narration for the conditional latent diffusion explainer. Beats are (visual_time, text), pointed at the moment
the visual appears. Names stay on screen, not in the voice. Spoken numbers are the paper's (text or figure legends)."""

VOICE = 'af_bella'
SPEED = 1.0
LANG = 'a'
SAY = {'Los Alamos': 'Loss Alamos', 'U-Net': 'you net'}

SCENES = [
    dict(scene='Title', hold=1.0, beats=[
        (0.6, 'Adaptive conditional latent diffusion: turning simple beam monitors into detailed pictures of a particle beam.'),
    ]),
    dict(scene='Question', beats=[
        (0.6, 'Almost every particle accelerator is lined with beam loss and beam current monitors.'),
        (6.0, "They are cheap, and they don't disturb the beam. But each one reports a single number: how many particles are passing, or being lost."),
        (16.0, "What we really want is the beam's full shape, in six dimensional phase space."),
        (22.0, 'Measuring that directly is slow. The first full six dimensional measurement took thirty two hours, and millions of individual measurements.'),
        (31.5, 'So the question is: can a generative model read the full shape of the beam from those simple monitor signals?'),
    ]),
    dict(scene='PhaseSpace', beats=[
        (0.6, 'First, a quick picture of phase space.'),
        (3.5, 'Each particle has three positions and three momenta: six numbers.'),
        (8.5, "Six dimensions can't be drawn, so we look at them two at a time. Six choose two gives fifteen projections."),
        (17.5, 'At this accelerator, the transverse momenta become angles, and the third pair becomes each particle’s phase and energy, relative to the radio frequency wave.'),
        (29.0, "Here are all fifteen, at the last module, from the paper's own simulations."),
    ]),
    dict(scene='Data', beats=[
        (0.6, 'The test bed is the kilometer long proton linear accelerator at Los Alamos, with forty eight radio frequency modules.'),
        (9.0, 'A fast GPU code tracks a million particles through it.'),
        (14.0, 'In each run, the phase and amplitude of the first four cavities are randomly shifted, by up to three degrees and three percent.'),
        (24.0, "That's a big change: operators usually adjust these by about one degree, or one percent."),
        (31.0, 'Five hundred runs, for each of four starting beams. Fifteen images at each of forty eight modules. That is one point four four million images.'),
        (42.0, 'Training uses three of the starting beams. The fourth is held back entirely, to test on a beam the model has never seen.'),
    ]),
    dict(scene='Signals', beats=[
        (0.6, 'Now the input. At each module, the surviving beam current is just the total number of particles left.'),
        (9.0, 'Here it is computed from the simulation, by adding up one projection. That gives forty eight numbers along the machine.'),
        (18.5, 'The model is conditioned on a vector, c, with four parts.'),
        (23.5, 'The eight radio frequency settings. The forty eight currents. A label, d, for which projection we want. And the module number, m.'),
    ]),
    dict(scene='Compress', beats=[
        (0.6, 'Generating big images directly is slow, so the method works in a compressed space.'),
        (6.5, 'A variational autoencoder squeezes each two hundred fifty six by two hundred fifty six image into an eight by eight grid, with three channels.'),
        (17.0, 'That is one hundred ninety two numbers per image: a compression factor of three hundred forty one.'),
        (25.5, 'The decoder rebuilds the image from those numbers. Training balances a faithful rebuild against keeping the latent space smooth and easy to sample.'),
        (36.0, 'The three channels learn different jobs: one tracks the brightest regions, one the edges, and one looks like a tiny copy of the image.'),
    ]),
    dict(scene='Diffuse', beats=[
        (0.6, 'Second, a diffusion model learns to create those latent grids.'),
        (5.0, 'During training, noise is added step by step, until the grid is pure noise.'),
        (11.5, 'A U-Net learns to undo one step at a time. Run it backwards from fresh noise, and a new latent grid appears.'),
        (21.0, 'Because the grid is so small, one hundred steps are enough, instead of the usual thousand.'),
        (28.5, 'And every denoising step is guided by the condition vector, c, so the result matches the currents, the settings, and the projection we asked for.'),
        (40.0, 'Finally, the decoder turns the latent grid back into a full resolution picture of the beam.'),
    ]),
    dict(scene='Label', beats=[
        (0.6, 'One small design choice is worth a closer look: how to tell the model which of the fifteen projections we want.'),
        (9.5, 'Numbering them one to fifteen would put some projections closer together than others, for no physical reason.'),
        (17.5, 'A one hot code makes every pair equally different, ignoring the axes they share.'),
        (24.0, 'Instead, d has six slots, one per phase space coordinate, with a one on each of the two axes being shown.'),
        (32.5, 'Projections that share an axis now overlap, and projections with nothing in common are orthogonal. The authors found this worked best.'),
    ]),
    dict(scene='Results', beats=[
        (0.6, 'So how well does it work? Here is one test case, at the last module.'),
        (6.5, 'On the left, the true fifteen projections. On the right, the generated ones, from currents and settings alone.'),
        (13.5, 'The overlaid profiles match closely, even for the swirling energy structure.'),
        (19.5, 'Along the machine, the generated longitudinal phase space follows the real one, from the first module to the last.'),
    ]),
    dict(scene='Errors', beats=[
        (0.6, 'How big are the errors? The paper reports average percent errors, and they grow at each stage.'),
        (8.0, 'The compression step alone is off by about sixteen percent, on held out images.'),
        (14.0, 'The full chain, diffusion plus decoder, reaches about twenty four percent on the test set, against seventeen percent on training data.'),
        (24.0, 'Beam sizes fitted from the generated images still match well, with errors much smaller than the sizes themselves.'),
        (32.5, "And the error is largest where the beam varies most from run to run, as you'd expect."),
    ]),
    dict(scene='Adaptive', beats=[
        (0.6, "Now the adaptive part. In a real machine, the radio frequency system drifts over minutes to hours, and its true settings aren't known exactly."),
        (11.5, 'So the condition vector, c, slowly goes stale.'),
        (16.0, 'Suppose we can measure one simple profile of the beam, like its energy spread on a screen after a bending magnet.'),
        (25.5, 'Project the generated image the same way, and compare. The difference is a cost, C.'),
        (33.0, 'Extremum seeking then nudges c to lower that cost. Each parameter oscillates at its own frequency, and the cost feeds into the phase of that oscillation.'),
        (45.5, 'On average this behaves like gradient descent, without ever estimating a gradient. And it keeps tracking as the machine drifts.'),
    ]),
    dict(scene='Tracking', beats=[
        (0.6, 'Here are three examples, at modules twenty eight, thirty eight and forty eight.'),
        (6.5, 'Left, the prediction without tracking. Middle, the drifted target. Right, the prediction after tuning c.'),
        (14.5, "The tracked images recover the target's shape, missing only small interior details."),
        (20.5, "That's notable, because a one dimensional profile can't pin down a two dimensional image on its own. A square and a circle can cast the same shadow."),
        (32.5, 'It works because the model only produces beams that the machine can actually make.'),
    ]),
    dict(scene='Limits', beats=[
        (0.6, 'Some cautions before we meet.'),
        (2.5, 'Everything here is simulation. The currents come from summing simulated particles, not from real monitors, which add noise and offsets.'),
        (12.5, 'Only four cavities vary. The other forty four modules, and all the magnets, stay fixed.'),
        (20.0, "Results on the unseen starting beam aren't reported separately from the rest of the test set. And tracking is shown on three examples, without statistics."),
    ]),
    dict(scene='Discussion', beats=[
        (0.6, 'Five questions to think about.'),
        (2.0, 'One. The title says beam loss, but the inputs are simulated currents. What changes with real, noisy monitors?'),
        (9.5, 'Two. If each stage adds error, is a bigger autoencoder the fix, or should the compression go?'),
        (16.5, 'Three. How far can the starting beam change before the model needs retraining?'),
        (22.5, 'Four. When tracking matches a one dimensional profile, how do we know the rest of the image is right?'),
        (29.5, 'Five. Could these monitors and this model be used to tune the machine, not just to watch it?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.6, 'Cheap monitors, a compressed latent space, and a guided diffusion model: together they turn single numbers into detailed pictures of the beam.'),
        (8.0, 'See you at journal club.'),
    ]),
]
