"""Narration for the LEM explainer. Beats are (visual_time, text), pointed at the moment the visual appears.
Names stay on screen, not in the voice (Whisper can't check them). ~145 words a minute."""

VOICE = 'af_bella'
SPEED = 1.0
LANG = 'a'
SAY = {'Los Alamos': 'Loss Alamos'}

SCENES = [
    dict(scene='Title', hold=1.0, beats=[
        (0.6, 'Latent evolution models: one compact model for forward, inverse, tuning and uncertainty problems in particle accelerators.'),
    ]),
    dict(scene='Question', beats=[
        (0.6, 'A particle accelerator is a long chain of modules: radio frequency cavities and magnets, each with its own settings.'),
        (4.5, 'As a bunch of charged particles travels through them, its shape keeps changing.'),
        (9.0, 'But we can only measure the beam in a few places, and many measurements disturb it.'),
        (13.5, 'Full physics simulations can fill the gaps, but they are slow.'),
        (17.5, "So the field builds virtual diagnostics: fast learned models that tell us what the beam looks like where we can't look."),
    ]),
    dict(scene='PhaseSpace', beats=[
        (0.6, 'First, what does the shape of the beam actually mean?'),
        (2.5, 'Each particle has a position in three directions, and a momentum in three directions. Six numbers.'),
        (7.5, 'Together, all the particles fill a six dimensional cloud, called phase space.'),
        (11.5, 'Six dimensions are impossible to picture, so we look at them two at a time. There are fifteen such pairs.'),
        (17.0, 'These fifteen images are the beam state, X, that the model works with.'),
    ]),
    dict(scene='Roadmap', beats=[
        (0.6, 'This paper, from Los Alamos, asks: can one model handle every job we need?'),
        (4.5, 'Forward: predict the beam downstream from what it looks like upstream.'),
        (7.5, 'Inverse: run that backwards, and recover the upstream beam, with error bars.'),
        (10.5, 'A second inverse: read off the machine settings that produced a beam.'),
        (13.5, 'And tuning: find the settings that lose the fewest particles.'),
    ]),
    dict(scene='Compress', beats=[
        (0.6, 'The trick is to stop working with the images directly.'),
        (3.0, 'An encoder squeezes the fifteen images through a narrow bottleneck: a short list of numbers, called the latent vector, z.'),
        (8.5, 'A decoder then rebuilds the images from z alone. If the rebuild is good, z has kept what matters.'),
        (13.5, 'This is a variational autoencoder, so the encoder outputs a whole distribution for z, a mean and a spread, not a single point.'),
        (19.0, 'It is trained by maximizing the evidence lower bound, which balances a faithful rebuild against a tidy latent space.'),
    ]),
    dict(scene='Evolve', beats=[
        (0.6, 'Step two learns how the beam changes, but inside the latent space.'),
        (3.5, 'Encode the beam at every module, and you get a path of latent vectors, from the first module to the last.'),
        (8.0, 'A transformer learns to predict each next point on that path.'),
        (11.5, 'Equation one writes this as each step depending only on the step before.'),
        (16.0, 'But the text says the model goes further: each step can look back at all the earlier ones.'),
        (21.0, "That matches how it's trained, from one past state and from many."),
        (24.5, 'Space and time are learned separately, then joined when the model is used.'),
    ]),
    dict(scene='Forward', beats=[
        (0.6, 'Now the four problems. Forward first.'),
        (3.0, 'Encode the upstream beam, let the transformer step the latent vector down the machine, and decode.'),
        (9.0, 'Out come all fifteen images at a downstream module, without running the full simulation.'),
    ]),
    dict(scene='InverseBeam', beats=[
        (0.6, 'The first inverse problem runs time backwards: from downstream measurements, recover the beam upstream.'),
        (5.0, 'This is hard, because different upstream beams can look alike downstream.'),
        (9.0, 'The reverse model trains a transformer on the latent paths read backwards.'),
        (13.5, 'The encoder and decoder stay frozen. Only the time model is retrained.'),
        (18.0, 'And because the encoder gives a distribution, we can draw many samples, run each one back, and get a spread of answers.'),
        (25.0, 'That spread is an error bar on the reconstruction: an estimate of the uncertainty in the data itself.'),
    ]),
    dict(scene='InverseSettings', beats=[
        (0.6, 'The second inverse problem asks for the machine settings, like the phases and amplitudes of the radio frequency cavities.'),
        (6.0, 'Learning that straight from the images is hard.'),
        (8.5, 'So split it in two: images to latent vector, which the encoder already does, then latent vector to settings.'),
        (13.5, 'Only that last step is new: a small dense network, trained on simulations with a mean squared error.'),
        (19.0, 'The encoder has already done the hard work of finding good features.'),
    ]),
    dict(scene='Tuning', beats=[
        (0.6, 'Last, tuning: find the settings that minimize beam loss.'),
        (4.0, 'With tens or hundreds of knobs, and a slow simulation for every try, even Bayesian optimization struggles.'),
        (9.5, 'So search the latent space instead, which might have just eight dimensions.'),
        (14.0, 'Each latent point maps to settings through the regression network, and gets a score.'),
        (19.0, "But points far from the training data can decode to beams that can't exist."),
        (23.5, 'A classifier prunes those points, so the search stays on realistic beams.'),
        (28.0, 'The authors report that this found several distinct optima, and beat standard high dimensional optimizers.'),
    ]),
    dict(scene='Limits', beats=[
        (0.6, 'A few cautions before we meet.'),
        (2.5, 'This is a short conference summary. Every result it mentions lives in earlier papers, so this video shows no numbers, and every picture is an illustration.'),
        (10.0, 'The tuning claims come from simulation studies. How well they carry over to a real machine is a question for those papers.'),
        (16.5, 'And equation one, as printed, looks only one step back, while the text describes a model that sees the whole history.'),
    ]),
    dict(scene='Discussion', beats=[
        (0.6, 'Here are five questions to think about.'),
        (1.5, 'One. What does the latent space throw away, and could that matter for beam loss?'),
        (7.5, "Two. When is the encoder's spread enough uncertainty, and when do we also need the model's own uncertainty?"),
        (14.0, 'Three. If many settings give the same beam, what does a settings estimate even mean?'),
        (20.0, 'Four. Is the feasibility classifier just defining physical as looking like the training data?'),
        (26.0, 'Five. Could one shared latent space be a single point of failure for all four tasks at once?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.6, "One encoder, one time model, four jobs: that's the idea of latent evolution models."),
        (5.0, 'The paper is from the North American Particle Accelerator Conference. See you at journal club.'),
    ]),
]
