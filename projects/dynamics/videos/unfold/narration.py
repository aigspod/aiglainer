"""Room to unfold: latent room and parameters. What Bella says over each scene; beats are (visual_time, text).
Facts: §4.2, App. A.4 (Chafee-Infante), §4.3, App. A.5 (cylinder flow), §5.1 of arXiv:2512.21113v2, via
projects/dynamics/AGENTS.md. The climate-emulator scene is our extrapolation and says so."""

VOICE = 'bella'
SAY = {'SamudrACE': 'Samudrace', 'Chafee-Infante': 'Chafee Infante'}

SCENES = [
    dict(scene='ColdOpen', smax=1.4, hold=0.5, beats=[
        (0.5, 'Two small transformers watch a flow through one sensor. Both predict the next reading well.'),
        (7.0, 'Now ask each to rebuild the whole field of one velocity component from what it learned.'),
        (12.0, 'One gets it nearly right. The other is about seventy times worse.'),
        (17.0, 'Both forecast the next step well, but they are very different on the inside.'),
    ]),
    dict(scene='Title', hold=1.0, beats=[
        (0.6, "Today's paper: A Mechanistic Analysis of Transformers for Dynamical Systems."),
    ]),
    dict(scene='Latent', beats=[
        (0.5, 'The model sees one number per time step, from one sensor.'),
        (4.5, 'It takes the last five readings as tokens.'),
        (8.0, 'Then attention mixes them into a short vector, the latent state: its internal guess of where the system is.'),
        (15.0, 'A small network predicts the next reading from it.'),
        (19.5, "The vector's length is the model's room. Two numbers, or three."),
        (24.5, 'Delay embedding theory says five readings are enough for a state on a two-dimensional surface: two times two, plus one.'),
    ]),
    dict(scene='Rod', beats=[
        (0.5, 'First test: a reaction-diffusion equation, known as the Chafee-Infante equation.'),
        (4.0, 'Picture a rod, pinned at zero at both ends. Its shape changes, then settles.'),
        (10.0, 'In the long run, its shapes lie on a two-dimensional surface, built from a few sine waves.'),
        (16.0, 'The model gets one sensor, near the left end. Five readings: in principle, enough information.'),
    ]),
    dict(scene='Fold', beats=[
        (0.5, 'But that surface is symmetric about zero: here is our simulation of it, with its two mirror halves.'),
        (7.5, 'Now view it through the sensor, two readings at a time.'),
        (13.5, 'The wide surface is squeezed into a thin needle. States that were far apart nearly touch.'),
        (20.0, 'In principle, the information is still in the five readings. The model just has to pull it apart.'),
    ]),
    dict(scene='Room', beats=[
        (0.5, 'How much room does that take?'),
        (3.0, 'With a latent of two numbers, the model squashes the surface into a thick curve.'),
        (8.5, 'Across ten seeds it is unstable: some runs do worse than a network with no attention.'),
        (15.5, 'Give it a third number, and the surface unfolds. The sine-wave amplitudes can be read off the latent.'),
        (23.0, "The authors' reading: the extra room lets attention unfold first. Then the network projects back down to two."),
    ]),
    dict(scene='Cylinder', beats=[
        (0.5, 'Second test: flow past a cylinder, shedding a trail of vortices.'),
        (5.0, 'The Reynolds number sets the regime, from one hundred to seven hundred fifty: one run each.'),
        (11.5, 'Again, one sensor, a latent of three numbers, and five to seven readings.'),
        (16.5, 'Testing adds six values inside the training range, and three just outside it.'),
    ]),
    dict(scene='Loops', beats=[
        (0.5, 'First, the model is not told the Reynolds number.'),
        (3.5, 'Its latent loops for different runs overlap. Nearby points can mean different regimes.'),
        (9.5, 'One-step errors are lowest mid-range, and grow toward the edges, most of all for held-out runs.'),
        (17.0, 'Give it the Reynolds number as an input, and the loops separate, in order. Errors drop and even out.'),
    ]),
    dict(scene='Recon', beats=[
        (0.5, 'Then a harder test. From the latent alone, rebuild the whole field of one velocity component.'),
        (5.5, 'With the Reynolds number, the mean absolute error is about one ten-thousandth.'),
        (10.0, 'Without it, about seventy times worse, and fifty times worse in the wake, where shedding is most sensitive.'),
    ]),
    dict(scene='Lesson', beats=[
        (0.5, 'In the first test, the readings held enough information in principle, but the latent had too little room.'),
        (6.5, 'In the second, there was room, but a hidden parameter got folded in.'),
        (11.5, 'Same lesson: one-step accuracy is not latent identifiability. Each true state needs its own place inside.'),
    ]),
    dict(scene='Emulators', beats=[
        (0.5, 'Now, our extrapolation. This part comes from us, not from the paper.'),
        (4.5, 'Climate emulators, like ACE and SamudrACE, learn to step a whole climate state forward.'),
        (10.5, 'Forcing, like carbon dioxide, plays the Reynolds number’s role. Leave it out, and different climates can blur together inside.'),
        (18.5, 'Some of the state may be hidden, like the deep ocean for an atmosphere-only emulator, or deep soil moisture, so the current state alone may not be enough.'),
        (27.0, 'A good one-step score is not enough: test spectra and long-run statistics too.'),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'If two models predict the next step equally well, what test would show which one has the sounder inside?'),
        (10.5, 'And in a climate emulator, what plays the missing Reynolds number? How would we notice?'),
    ]),
    dict(scene='End', hold=2.6, beats=[
        (0.5, 'The takeaway: enough information is not enough. A model needs room to unfold it, and the parameters that tell regimes apart.'),
        (8.0, 'See you at journal club.'),
    ]),
]
