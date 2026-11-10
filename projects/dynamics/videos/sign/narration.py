"""Attention can only average: what Bella says over each scene. Beats are (visual_time, text). Facts: §2.3 (Eq. 17-18),
§3.1 (Eq. 20-21, Case 1 and 2), App. A.1 (W_O), §3.2 of arXiv:2512.21113v2. Case 2's coefficients, the one-head fit, the
two-head construction and the AR(p) check are ours, and are said to be."""

VOICE = 'bella'
SAY = {}

SCENES = [
    dict(scene='ColdOpen', smax=1.2, hold=0.4, beats=[
        (0.5, 'Pull a mass on a spring, and let it go. It rings, and slowly dies away.'),
        (5.0, 'Guessing its next position from the last two is a one-line recipe.'),
        (9.5, 'A single attention head can learn that recipe for a stiff spring.'),
        (14.0, 'Make the spring softer, and the same head fails. Not for lack of data. Because of a minus sign.'),
    ]),
    dict(scene='Title', hold=1.0, beats=[
        (0.6, "Today's paper: A Mechanistic Analysis of Transformers for Dynamical Systems. This video is about why attention can only average."),
    ]),
    dict(scene='Recipe', beats=[
        (0.5, "Sample the spring's position twenty-five times a second."),
        (4.5, 'With no push, each new sample is a fixed weighted sum of the last two. That is an autoregressive model, of order two.'),
        (12.0, 'A stiff spring, ringing at seven point one hertz, has two negative coefficients.'),
        (18.0, 'A softer spring, at three point six hertz, needs one positive coefficient and one negative.'),
    ]),
    dict(scene='OneHead', beats=[
        (0.5, 'Now hand the job to a single attention head, with nothing else.'),
        (4.5, 'The head looks back at the last two samples, and gives each one a weight.'),
        (10.0, 'The weights come from a softmax, so they are positive, and they add up to one. Attention averages.'),
        (17.0, 'Then one shared output number scales the average.'),
        (21.5, 'So both coefficients are that one number times a positive weight. They always share its sign.'),
    ]),
    dict(scene='Plane', beats=[
        (0.5, 'Put every pair of coefficients on a plane. The first coefficient across, the second up.'),
        (5.5, 'One head can only reach the two corners where the signs agree.'),
        (9.5, 'The stiff spring sits inside. One head matches it exactly, with a negative output number.'),
        (15.0, 'The soft spring sits outside, where no single head can get.'),
        (20.5, 'In our own fit, with the weights held fixed, the best one head does is drop the older sample.'),
    ]),
    dict(scene='Springs', beats=[
        (0.5, "Here are both springs, simulated from the paper's equations, with our best one-head fit."),
        (6.0, 'For the stiff spring, the fit follows every swing.'),
        (10.5, 'Its spectrum peaks right at seven point one hertz, as in the paper.'),
        (16.0, 'For the soft spring, the guesses still wiggle, but they lag and shrink.'),
        (22.0, 'And the spectrum has lost its resonance peak.'),
        (25.5, "The paper's trained head fails the same way. Its response is too smooth, with no peak."),
    ]),
    dict(scene='TwoHeads', beats=[
        (0.5, "The paper's fix is a second head."),
        (3.5, 'Each head still averages, with positive weights that add up to one.'),
        (9.0, 'But each head gets its own output number, and those can have opposite signs.'),
        (15.0, "In the paper's two-head model, they are one point zero eight seven, and minus one point two four four."),
        (22.0, 'A simple version, our own: one head watches only the newest sample, and the other only the older one.'),
        (29.0, "Scale them by plus one point two four and minus zero point nine eight, and the soft spring's recipe is back."),
        (37.0, 'The paper stresses this is a boundary case: one head, attention only. Real transformers have residual paths and many heads.'),
    ]),
    dict(scene='TwoMasses', beats=[
        (0.5, 'The paper then couples two masses. Now the system rings in two ways at once, a slow mode and a fast one.'),
        (8.0, 'Show the transformer both positions and three past steps, and it finds both modes.'),
        (14.0, 'Show it only the first mass, and three steps are not enough. The modes are lost.'),
        (20.5, 'Give it four steps, and both modes come back.'),
        (24.5, 'Time stands in for the missing sensor.'),
    ]),
    dict(scene='Delay', beats=[
        (0.5, 'We can check the count with a plain linear recipe, fit to the first mass alone.'),
        (6.0, 'With three past values, its spectrum misses both modes.'),
        (11.5, 'With four, it fits to rounding error, and both peaks appear. Two modes need four numbers of state.'),
        (19.0, 'One honest note. The stated parameters give modes at three point three and nine point five hertz. The paper reports four point one and nine point five.'),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'Real models have many heads. How would you check that a trained model kept the resonance, rather than averaging it away?'),
        (12.0, "And, as our own extrapolation: a climate emulator steps forward from today's state. Which missing variables could a longer history stand in for?"),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.5, 'The takeaway: one attention-only head can only average. To ring, it needs a minus sign from somewhere else, like a second head, and enough history to see the whole state.'),
        (9.0, 'See you at journal club.'),
    ]),
]
