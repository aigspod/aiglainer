"""Rebuilding a hidden state: what Bella says over each scene. Beats are (visual_time, text). Facts: §2.3 (Takens,
Eq. 19), §4.1 (Van der Pol setup, Fig. 5, Fig. 6), Table 1 (App. A.2.1), §5.2 of arXiv:2512.21113v2."""

VOICE = 'bella'
SAY = {'MLP': 'M L P'}

SCENES = [
    dict(scene='ColdOpen', smax=1.2, hold=0.5, beats=[
        (0.5, 'Here is a dot moving up and down. All you can see is its height.'),
        (5.0, 'Right now it sits at one. Is it on the way up, or on the way down?'),
        (10.0, "From one snapshot, you can't tell. But the last few snapshots make it obvious."),
        (15.0, 'The velocity is hidden. The history holds it.'),
    ]),
    dict(scene='Title', hold=1.0, beats=[
        (0.6, "Today: how attention rebuilds a hidden state. From the paper, A Mechanistic Analysis of Transformers for Dynamical Systems."),
    ]),
    dict(scene='VdP', beats=[
        (0.5, "The paper's test case is the Van der Pol oscillator. It has a position, x, and a velocity."),
        (5.5, 'Start it almost anywhere, and it spirals onto the same loop, called a limit cycle.'),
        (12.5, 'The paper simulates short runs from random starts, samples them at steps of one tenth, and trains models to predict the next sample.'),
        (20.0, 'Each point in this plane is a full state. Know both numbers, and the next step is fixed.'),
    ]),
    dict(scene='FullState', beats=[
        (0.5, 'First, give the models the whole state: position and velocity.'),
        (4.5, 'A plain neural network, an MLP, sees only the current state.'),
        (7.0, 'The transformer sees the last five.'),
        (11.0, 'Both reach an error of about ten to the minus seven.'),
        (16.5, 'When the state is complete, history adds nothing.'),
    ]),
    dict(scene='Hide', beats=[
        (0.5, 'Now hide the velocity. The models see only x.'),
        (4.5, 'At x equals one, the oscillator passes twice per lap: once rising, once falling.'),
        (11.0, 'The MLP gets the same input both times. The best it can do is split the difference.'),
        (18.5, 'But the last five samples differ. One window climbs toward one, the other falls toward it.'),
        (25.0, 'History tells the two apart.'),
    ]),
    dict(scene='Takens', beats=[
        (0.5, "There's a theorem behind this, called Takens' theorem."),
        (6.0, 'Slide a window along one measurement, and stack the last few values into a vector.'),
        (12.5, 'Plot those vectors, and they trace a copy of the hidden loop, without ever measuring velocity.'),
        (20.0, 'How many values? For an attractor of dimension d, twice d, plus one, is enough, for a typical measurement.'),
        (27.0, 'The paper takes d as two, which gives the five past samples its transformer reads.'),
    ]),
    dict(scene='Table1', beats=[
        (0.5, "Here are the errors with velocity hidden, typed from the paper's Table 1. Shorter is better."),
        (5.5, "The MLP alone does worst. It can't tell up from down."),
        (10.5, 'A classic baseline, a polynomial fitted to the same five delays, does about ten times better.'),
        (17.0, 'Attention without positional encoding, a tag telling the model which sample is which, lands in the same range.'),
        (24.0, 'With positional encoding and a two dimensional latent, the error falls to two times ten to the minus five.'),
        (31.0, "That's about three orders of magnitude below the MLP, and two below the baseline."),
    ]),
    dict(scene='Latent', beats=[
        (0.5, 'So how does the transformer tell the two phases apart?'),
        (4.5, 'Attention adds a correction from the window to the current sample, and the MLP reads the sum.'),
        (12.0, 'The paper finds two different corrections for the same x: one for each phase.'),
        (19.0, 'Even a plain average of the window can do it. Subtract it from the current sample, plot that against x, and you get a loop.'),
        (25.5, 'And with a two dimensional latent, its internal state traces a copy of the limit cycle.'),
    ]),
    dict(scene='Attention', beats=[
        (0.5, 'Finally, look at attention itself. Across ten training runs, it spreads over several past samples, rather than picking one.'),
        (8.0, 'Without positional encoding, the weights are nearly uniform: a plain average of the window.'),
        (14.0, 'With it, each lag gets its own weight, more like a tuned filter.'),
        (20.0, 'Here the paper disagrees with itself. The text says positional encoding reshapes attention without systematically improving accuracy.'),
        (27.5, 'But its own table shows about eighty-six times lower error in the two dimensional model. A later section agrees, so we follow the table.'),
    ]),
    dict(scene='Discussion', beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'If attention without positions just averages the window, where is the state really rebuilt: in attention, or in the MLP after it?'),
        (11.0, "And, our extrapolation: a climate emulator that steps from today's state alone can't see the deep ocean. How much history would it need?"),
    ]),
    dict(scene='End', hold=2.5, beats=[
        (0.5, 'The takeaway, in these tests: attention helps only when the state is incomplete. Then it rebuilds the hidden part from the recent past.'),
        (8.0, 'See you at journal club.'),
    ]),
]
