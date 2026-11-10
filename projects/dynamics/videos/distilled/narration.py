"""The distilled cut, voiced by Michael: one arc through the whole paper. Beats are (visual_time, text), at the part
scenes' authored times. Facts: §2.3, §3.1, App. A.1, §3.2, §4.1, Table 1, §4.2, §4.3, App. A.5, §5.1 of
arXiv:2512.21113v2, via projects/dynamics/AGENTS.md. The one-head fit and the two-head construction are ours and are
said to be; the climate-emulator scene and the third question are our extrapolation and say so."""

VOICE = 'michael'
SAY = {'MLP': 'M L P', 'SamudrACE': 'Samudrace', 'Chafee-Infante': 'Chafee Infante'}

SCENES = [
    dict(scene='ColdOpen', smax=1.4, hold=0.5, beats=[
        (0.5, 'Two small transformers watch a flow through one sensor. Both predict the next reading well.'),
        (7.0, 'Now ask each to rebuild the whole field of one velocity component from what it learned.'),
        (12.0, 'One gets it nearly right. The other is about seventy times worse.'),
        (17.0, 'Both forecast well, but they are very different on the inside.'),
    ]),
    dict(scene='Title', hold=0.8, beats=[
        (0.6, 'This is A Mechanistic Analysis of Transformers for Dynamical Systems. The whole paper, in about six minutes.'),
    ]),
    dict(scene='Recipe', beats=[
        (0.5, 'Start with a mass on a spring, its position sampled twenty-five times a second.'),
        (4.5, 'Each new sample is a fixed weighted sum of the last two: an autoregressive recipe.'),
        (12.0, 'A stiff spring needs two negative coefficients.'),
        (18.0, 'A softer spring needs one positive and one negative.'),
    ]),
    dict(scene='OneHead', beats=[
        (0.5, 'Now give the job to one attention head, with nothing else.'),
        (10.0, 'Its weights come from a softmax, so they are positive and add up to one. Attention averages.'),
        (17.0, 'One shared output number then scales the average,'),
        (21.5, 'so both coefficients always share its sign. The soft spring is out of reach.'),
    ]),
    dict(scene='Springs', vend=28.0, beats=[
        (0.5, "Here are both springs, simulated from the paper's equations, with our best one-head fit."),
        (6.0, 'The stiff one is followed swing for swing.'),
        (16.0, 'The soft one lags and shrinks, and its resonance peak is gone.'),
        (25.5, "The paper's trained head fails the same way. Its response is too smooth."),
    ]),
    dict(scene='TwoHeads', beats=[
        (0.5, "The paper's fix is a second head. Each head still averages,"),
        (9.0, 'but each gets its own output number, and those can have opposite signs.'),
        (22.0, 'A simple version, our own: one head watches only the newest sample, the other only the older one.'),
        (29.0, "With opposite signs, the soft spring's recipe is back."),
        (37.0, 'The paper stresses this is a boundary case. Real transformers have residual paths and many heads.'),
    ]),
    dict(scene='TwoMasses', beats=[
        (0.5, 'Next, two coupled masses, ringing in two ways at once: a slow mode and a fast one.'),
        (8.0, 'Shown both positions over three steps, the transformer finds both modes.'),
        (14.0, 'Shown only the first mass, three steps are not enough.'),
        (20.5, 'Four steps bring both modes back. Time stands in for the missing sensor.'),
    ]),
    dict(scene='Hide', beats=[
        (0.5, 'Now a nonlinear system, the Van der Pol oscillator, which settles onto a loop. Hide its velocity.'),
        (4.5, 'At x equals one, it passes twice per lap: once rising, once falling.'),
        (11.0, 'A plain network, an MLP, gets the same input both times.'),
        (18.5, 'But the last five samples differ. History tells the two apart.'),
    ]),
    dict(scene='Takens', beats=[
        (0.5, "Takens' theorem says past values of one measurement can rebuild a hidden state."),
        (12.5, 'Stack a window of them into a vector, and the vectors trace a copy of the loop.'),
        (20.0, 'For an attractor of dimension d, twice d, plus one, values are enough, for a typical measurement.'),
        (27.0, 'The paper takes the dimension as two, which gives the five samples its transformer reads.'),
    ]),
    dict(scene='Table1', beats=[
        (0.5, "Here are the paper's errors with velocity hidden. Shorter is better."),
        (5.5, 'The MLP does worst.'),
        (10.5, 'A polynomial baseline does about ten times better.'),
        (17.0, 'So does attention without positional encoding, a tag for which sample is which.'),
        (24.0, 'With the tag and two numbers of internal state, the error falls three orders of magnitude below the MLP.'),
        (34.0, "The paper's text says positional encoding gives no systematic gain. Its own table disagrees."),
    ]),
    dict(scene='Room', vend=21.0, beats=[
        (0.5, 'Is history always enough? Next, the Chafee-Infante equation, whose long-run shapes lie on a two-dimensional surface.'),
        (3.0, 'The model packs its window into a short vector, its latent. With two numbers, the surface collapses.'),
        (15.5, 'With three, it unfolds.'),
    ]),
    dict(scene='Loops', vend=24.0, beats=[
        (0.5, 'Last test: flow past a cylinder, with the Reynolds number from one hundred to seven hundred fifty.'),
        (3.5, 'Not told the Reynolds number, the latent loops for different runs overlap.'),
        (9.5, 'One-step errors grow toward the edges of the range.'),
        (17.0, 'Given the Reynolds number as an input, the loops separate, in order.'),
    ]),
    dict(scene='Recon', beats=[
        (0.5, 'Now back to the opening test. From the latent alone, rebuild the whole field of one velocity component.'),
        (5.5, 'With the Reynolds number, the mean absolute error is about one ten-thousandth.'),
        (10.0, 'Without it, about seventy times worse, and fifty times worse in the wake.'),
    ]),
    dict(scene='Lesson', vend=19.0, beats=[
        (0.5, 'In one test, too little room.'),
        (6.5, 'In the other, a hidden parameter.'),
        (11.5, 'Same lesson: one-step accuracy is not latent identifiability.'),
    ]),
    dict(scene='Emulators', beats=[
        (0.5, 'Now, our extrapolation. This part comes from us, not from the paper.'),
        (4.5, 'Climate emulators such as ACE and SamudrACE step a whole climate state forward in time, again and again.'),
        (10.5, "Forcing, like carbon dioxide, plays the Reynolds number's role. Leave it out, and climates can blur together."),
        (18.5, 'Parts of the state may be hidden, like the deep ocean for an atmosphere-only emulator.'),
        (27.0, 'And one-step skill is not enough: test spectra and long-run statistics too.'),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Three questions for journal club.'),
        (3.0, 'In a model with many heads, how would you check that it kept the resonance?'),
        (9.0, 'If attention just averages the window, where is the state rebuilt?'),
        (15.0, 'And, our extrapolation: in a climate emulator, what plays the missing Reynolds number?'),
    ]),
    dict(scene='End', hold=2.5, beats=[
        (0.5, "The takeaway: attention averages, history can stand in for a hidden state, and a good forecast doesn't prove a sound inside."),
        (8.0, 'See you at journal club.'),
    ]),
]
