"""Narration script: the single source of truth for the narrated cut.

Each entry is one scene, in order. `beats` are (visual_time, text) pairs: visual_time is the moment in
the scene's own timeline (seconds, as authored in video/scenes*.py) that the line should start on.
The build lays the lines end to end and time-warps each scene so those visual moments land on
their lines (see video/narrated.py).

Optional per-scene keys:
  smax  - fastest the visuals may play while catching up to the next line (default 1.8x)
  hold  - extra seconds of screen time after the last line (default 0.9)
  vend  - visual time the scene ends at (default: the scene's authored duration)
  still - seconds at the very end where the visuals freeze (time to read, or to pause on)

Write text for the ear. Symbols are spelled out ("alpha", "tau", "C dagger"); SAY maps any leftovers.
"""

VOICE = 'af_bella'
SPEED = 1.0
LANG = 'a'          # American English

# Applied to the text before synthesis only (captions keep the written form).
SAY = {
    'MLP': 'M L P',
}

SCENES = [
    dict(scene='ColdOpen', smax=1.15, hold=0.4, beats=[
        (1.4, 'A transformer watches a person move,'),
        (5.7, 'and predicts what a radar will see.'),
        (10.1, "It's accurate. But has it actually learned the physics?"),
    ]),
    dict(scene='Title', hold=1.0, vend=7.0, beats=[
        (0.7, 'LAWFUL, by Kevin Chen, Kenneth Parker, and Anish Arora, is a way to check.'),
    ]),
    dict(scene='MechInterp', beats=[
        (0.6, 'Usually we judge a network by its behavior: inputs in, outputs checked.'),
        (6.0, 'Mechanistic interpretability opens it up, and asks how the computation inside works.'),
        (12.0, 'Often the goal is a circuit: a few parts, like attention heads and MLP layers, that do one job together.'),
        (20.0, 'But to check a circuit, you need the right answer. Language models rarely give us one. Physics does: the law.'),
    ]),
    dict(scene='ProbeVsPatch', beats=[
        (1.5, 'Two basic tools. A probe reads: a simple linear model, trained to predict a quantity like velocity from the activations.'),
        (9.0, "But readable doesn't mean used."),
        (13.0, "Activation patching writes: copy one component's activation from another input, and see if the output changes. If it does, that component matters."),
    ]),
    dict(scene='Question', beats=[
        (0.4, 'So the paper asks three things.'),
        (2.0, 'Has the model learned the law?'),
        (6.0, 'Does it use it, or can a probe merely decode it?'),
        (10.0, 'And does it hold everywhere the law applies, not just on the training data?'),
    ]),
    dict(scene='Roadmap', vend=24.0, beats=[
        (0.5, 'It answers in three steps.'),
        (2.5, 'Behavior: under what-if inputs, does the model respond the way the law says?'),
        (9.0, 'Cause: which components produce that behavior?'),
        (15.0, 'Mechanism: how do they compute it?'),
        (21.0, 'The tracker up top shows where we are.'),
    ]),
    dict(scene='Testbed', beats=[
        (0.6, 'The model maps motion capture to radar.'),
        (1.6, 'Fifty-three body markers go in.'),
        (4.0, 'A spatial transformer relates markers within a frame, and a temporal transformer relates frames over time,'),
        (7.6, 'to predict a micro-Doppler radar spectrogram.'),
        (14.0, 'Crucially, the training data never contains velocities or Doppler frequencies. Only positions in, spectrograms out.'),
    ]),
    dict(scene='Doppler', beats=[
        (1.0, 'Yet radar obeys the Doppler law: the frequency shift is twice the radial velocity, over the wavelength.'),
        (9.0, "Radial means toward or away from the radar. Sideways motion doesn't count."),
        (16.4, 'So to predict Doppler everywhere, the model must compute velocity from positions. Does it?'),
    ]),
    dict(scene='Framework', beats=[
        (0.8, 'Step one, behavior. LAWFUL sets the learned model, f,'),
        (4.5, 'beside a physics model, g: the Doppler law, as code.'),
        (8.8, "An input bridge computes the physical variable from the raw input: each marker's radial velocity."),
        (13.0, 'Perturbing that variable creates what-if inputs, called counterfactuals.'),
        (18.0, 'Output bridges reduce both outputs to one number, the Doppler centroid,'),
        (22.0, 'and a consistency score measures how well they agree, across a continuous range rather than a few examples.'),
    ]),
    dict(scene='Counterfactual', beats=[
        (1.0, 'A what-if input scales the radial part of the motion by a factor, alpha, and keeps the sideways part.'),
        (8.3, 'Alpha of point three: thirty percent speed toward the radar.'),
        (11.0, 'Negative alpha reverses direction.'),
        (21.6, 'At zero, the distance never changes, so the law predicts no Doppler at all.'),
    ]),
    dict(scene='Score', vend=14.5, beats=[
        (0.6, 'Scaling velocity by alpha should scale the Doppler centroid by alpha.'),
        (3.4, "So the paper compares the model's response slope with the physics slope,"),
        (9.0, 'and sums the gaps into one score, where one is a perfect match.'),
    ]),
    dict(scene='Domain', beats=[
        (4.0, 'Within the speeds this radar can measure,'),
        (13.0, 'the model scores zero point nine eight eight. Step one checks out: its behavior follows the law.'),
    ]),
    dict(scene='Patching', beats=[
        (0.5, 'Step two, cause. Which components produce that behavior? Patching tells us.'),
        (2.4, 'Run the original input, and its what-if version.'),
        (6.0, 'Sufficiency: patch the what-if into a candidate circuit, C, alone. Does the output still follow the law?'),
        (14.5, 'Necessity: patch everything except C. Does the law-following disappear?'),
        (27.5, 'A circuit passes at threshold tau if it alone recovers at least tau of the score.'),
    ]),
    dict(scene='Search', beats=[
        (0.6, 'A greedy search grows the circuit as tau rises.'),
        (5.0, 'It starts with three temporal parts: the MLP, and attention heads six and seven.'),
        (12.0, 'It grows almost entirely in the temporal block, the part that looks across time.'),
        (22.5, 'In the end, half the components recover ninety-one percent of the consistency, and random controls do far worse.'),
    ]),
    dict(scene='Spectrograms', beats=[
        (3.0, 'Slow the radial motion to thirty percent, and the Doppler swings shrink.'),
        (11.0, 'Patching just the circuit reproduces that. Patching the rest does not.'),
    ]),
    dict(scene='Fig4a', vend=26.5, beats=[
        (4.2, 'Across alpha, the model, in green, follows the law, in blue.'),
        (12.5, 'So does the circuit.'),
        (17.0, 'The rest of the model barely moves. Behavior and cause line up.'),
        (21.5, 'Outside the radar range, agreement breaks down, for reasons still open.'),
    ]),
    dict(scene='Fig4b', vend=15.0, hold=1.2, beats=[
        (1.0, 'And what the law forbids: sideways motion alone should cause no Doppler shift.'),
        (9.0, 'The model and circuit respect that.'),
    ]),
    dict(scene='Probes', beats=[
        (0.6, 'Step three, mechanism. Where does velocity appear? Now the probes come in.'),
        (8.0, 'No single attention head encodes it well.'),
        (12.5, "But the circuit's heads together do, with an R-squared of point seven six, where one is perfect."),
        (18.0, 'The temporal MLP only inherits it from attention.'),
    ]),
    dict(scene='QKVal', vend=23.0, beats=[
        (0.6, 'An attention head decides where to look, and what to carry.'),
        (8.5, 'Patching only where it looks nearly restores consistency. Patching what it carries does not.'),
        (16.0, "A detail for discussion: the text says six of seven heads, the table shows five of six."),
    ]),
    dict(scene='Heatmaps', vend=24.5, beats=[
        (4.5, 'One key head looks at the earliest frames, another at the latest.'),
        (12.0, 'And velocity is exactly that: a late position minus an early one. Together, the two heads supply both ends.'),
    ]),
    dict(scene='Limits', vend=16.0, beats=[
        (0.5, 'Limits: one linear law, one small model;'),
        (5.0, 'the law is given, not discovered;'),
        (9.0, 'the what-if inputs only rescale speed;'),
        (13.0, 'and the centroid sees only the overall shift.'),
    ]),
    dict(scene='Discussion', vend=29.0, hold=3.5, beats=[
        (0.4, 'Before we meet, think about these.'),
        (1.0, 'Is one number, the centroid slope, enough to say the model uses the law?'),
        (7.0, 'Would a different search find a different circuit?'),
        (13.0, 'How should we read effect sizes on a score with no floor?'),
        (19.0, 'Outside the radar range: physics, or unfamiliar data?'),
        (25.0, 'And what would LAWFUL need for a law nobody knows in advance?'),
    ]),
    dict(scene='End', hold=4.0, vend=14.0, beats=[
        (0.6, 'So: within the radar range, this model follows the Doppler law, through a small temporal circuit that computes velocity as a difference over time.'),
        (6.5, 'And when we know the true law, it can be the ground truth for what a model computes inside. See you at journal club.'),
    ]),
]
