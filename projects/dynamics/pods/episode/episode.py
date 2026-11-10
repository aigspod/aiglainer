"""What does attention do with a dynamical system? The full episode (about 21 min) for journal club on Nov 11.
Every claim traces to the paper (arXiv:2512.21113v2): §2.2-2.3 attention as an AR model (Eq. 14-18); §3.1 the
single-DOF oscillator (Eq. 20-21, Fig. 2; residual path and MLP off, linear readout); App. A.1 two heads
(W_O = [1.087, -1.244]); §3.2 the 2-DOF system (Figs. 3-4); §4.1 Van der Pol (Fig. 5-6, Table 1); §4.2 Chafee-Infante
(Eq. 24-26, Figs. 7-9, App. A.3-A.4: premature compression first, symmetry as a hedged extra); §4.3 cylinder flow
(Figs. 11-12, App. A.5, Table 2); §5 conclusions and future directions.
Our own checks, said on air: the 2-DOF parameters give natural frequencies near 3.3 and 9.5 Hz (the paper reports
4.1 and 9.5); the paper's text and Table 1 disagree on whether positional encoding helps for Van der Pol; "confirm"
Takens is too strong (and the cylinder works with five delays, below the 2d+1 = 7 the paper's own count asks for).
The emulator passages are labelled on air as our extrapolation.

A role ending in '?' ('H?') marks a question for the room. ('~', 'chime') plays the soft cue that announces one.
"""

HOSTS = {'H': 'bella'}       # role -> host in aiglainer/hosts.py

SAY = {
    'MLP': 'M L P',
    'MLPs': 'M L Ps',
    'Chafee-Infante': 'Chay-fee In-fahn-tay',
}

SEGMENTS = [
    # ---------------------------------------------------------------- cold open: the spring that attention can't copy
    dict(title='Cold open', music=None, lines=[
        ('H', 'Picture a weight on a spring, bouncing up and down, slowly losing energy.'),
        ('H', 'Now train the smallest possible transformer to predict its next position, from its last two positions.'),
        ('H', 'With a stiff spring, it works beautifully. The prediction rings at the right frequency.'),
        ('H', 'Make the spring softer, and something odd happens.', 0.6),
        ('H', "It still goes up and down. But it no longer rings at the spring's own frequency. The model smooths the motion out, and no amount of training fixes it."),
        ('H', "The reason is one line of arithmetic. Attention can only take averages. And some physics needs subtraction."),
        ('H', "Today's paper takes the simplest transformer apart, and asks what it can and cannot do with a dynamical system."),
    ]),
    dict(title='Welcome', music='theme', lines=[
        ('H', "Welcome to the aigs pod. I'm {H}, and this is our warm-up for journal club."),
        ('H', 'The voice is synthetic. The paper, the numbers, and the arguments are real.'),
        ('H', "Today's paper is called A Mechanistic Analysis of Transformers for Dynamical Systems."),
        ('H', "It's from a team at ETH Zurich, Johns Hopkins, and the Singapore-ETH Centre."),
        ('H', "A lot of interpretability work opens up trained networks, and searches them for circuits: small sets of parts that do one job."),
        ('H', "This paper works the other way round. It starts from classical theory, and asks what a one-layer transformer must be doing."),
        ('H', "That matters for us, because transformers now sit inside weather and climate models. The paper itself points to Aurora, a foundation model for the Earth system."),
        ('H', "Here's the plan. Part one: what attention is, seen as a classic forecasting model. Part two: the sign problem, with springs."),
        ('H', "Part three: what attention does when it can't see the whole system. Part four: when the model needs more room inside, and needs to be told which physical setting it's in. And then, what it might mean for emulators."),
        ('H', "And now and then, you'll hear a little chime.", 0.5),
        ('~', 'chime'),
        ('H', "That's a question for the room. Something to bring to the meeting on Wednesday. No need to pause. Just hold onto it."),
    ]),

    # ---------------------------------------------------------------- 1. attention as an autoregressive model (§2.2-2.3)
    dict(title='Attention, seen as a forecasting model', music='sting', lines=[
        ('H', "Part one. Let's set the stage."),
        ('H', 'A dynamical system is anything whose next state follows from its current state. A pendulum. A chemical reaction. The atmosphere.'),
        ('H', "The state is everything you need to know right now, to say what happens next. For a pendulum, that's its angle, and how fast it's swinging."),
        ('H', 'Sample a system at regular steps, and the task is easy to describe. Given the recent past, predict the next value.'),
        ('H', 'Weather forecasting does the same thing, at a vastly bigger scale.'),
        ('H', "Classical forecasting has a workhorse for this, called an autoregressive model. The next value is a weighted sum of the last few values, and the weights can be positive or negative."),
        ('H', "A positive weight says, add some of this step. A negative weight says, take some of it away."),
        ('H', 'Now the transformer. The authors use the smallest one they can: one layer, one attention head.'),
        ('H', 'One head is one set of attention weights. Big models run many of them side by side.'),
        ('H', "It reads a short window of past observations. Attention gives each past step a weight, and adds up the steps with those weights. Then an output layer turns that sum into a prediction."),
        ('H', "Write that down, and it looks just like an autoregressive model. A weighted sum of the past. With one twist."),
        ('H', 'The weights come out of a function called softmax. Softmax weights are always positive, and they always add up to one.', 0.5),
        ('H', "So attention can only take an average of the past. A blend. Never a difference."),
        ('H', 'The output layer can multiply that blend by one number, which can be negative. But it is the same number for every past step.'),
        ('H', "Say the blend gives the last step sixty percent, and the step before forty. Multiply by minus two, and both weights turn negative. Multiply by plus two, and both stay positive."),
        ('H', "Either way, the two weights always share a sign. That's the whole catch."),
        ('H', "Keep that in mind. Everything in part two follows from it."),
    ]),

    # ---------------------------------------------------------------- 2. the sign problem (§3.1, Fig. 2, App. A.1)
    dict(title='The sign problem', music='sting', lines=[
        ('H', 'Part two. Back to the spring.'),
        ('H', 'The authors simulate a single mass on a spring, with light damping, sampled twenty-five times a second. Only the position is observed.'),
        ('H', "For this test, they also switch off the shortcut, a path that would carry the input straight past attention. So attention is the only route from the past to the prediction."),
        ('H', "For this system, there's an exact rule. The next position is a weighted sum of the last two positions, and physics tells you the two weights."),
        ('H', 'Case one: a stiff spring, ringing about seven times a second. Physics says both weights are negative.'),
        ('H', "Both the same sign. So attention can do it. Blend the two past steps with positive weights, and let the output layer flip the sign of the result."),
        ('H', "And it works. The predicted motion matches. Break that motion down by frequency, into its spectrum, and there's a sharp peak right at the spring's own frequency."),
        ('H', "Case two: a softer spring, ringing about three and a half times a second.", 0.5),
        ('H', "Now the physics needs one positive weight and one negative weight. Roughly, add the last step, subtract the one before."),
        ('H', "Attention can't do that. Its two weights are positive. The single output number scales both the same way. There is no setting that gives one plus and one minus."),
        ('H', "And that's what the experiment shows. The prediction still goes up and down. But the peak is gone from its spectrum. The model has smoothed the dynamics."),
        ('H', "It's a lovely example of mechanism. The failure isn't bad training. It's arithmetic. The model cannot express the answer."),
        ('H', "The authors are careful about how far this goes. It's a single head. There's no second network after attention, and the shortcut is switched off. Real transformers have both, and many heads."),
        ('H', 'And in an appendix, they show that two heads are enough. Each head still averages. But the output layer weighs the two heads with opposite signs. One plus, one minus, about the same size.'),
        ('H', "Two averages, one subtracted from the other. That is enough to make a difference, and the peak comes back."),
        ('H', "So the lesson isn't that transformers can't model springs. It's that you can see exactly which piece of the architecture does the subtracting."),
        ('H', "Quick recap. If the physics needs weights of the same sign, one head can do it. If it needs one plus and one minus, one head can't. Two heads can.", 0.4),
        ('~', 'chime'),
        ('H?', "First question for the room. If a second head fixes the sign problem, what is the single-head result really teaching us? A limit of transformers, or a way to read what each part of one does?"),
    ]),

    # ---------------------------------------------------------------- 3a. seeing enough: the 2-DOF system (§3.2, Figs. 3-4)
    dict(title='Trading space for time', music=None, lines=[
        ('H', 'Part three. What if the model can\'t see the whole system? Back to springs. Two of them, this time.'),
        ('H', 'Picture two masses on springs, coupled together. Now there are two ways to vibrate, called modes, each with its own frequency.'),
        ('H', "If the model sees both positions, and three past steps, it finds both modes. Its spectrum has both peaks."),
        ('H', "If it sees only the first mass, with three past steps, it fails. One sensor and a short memory just isn't enough to tell the two modes apart."),
        ('H', 'But give it four past steps, still with one sensor, and both modes come back.', 0.5),
        ('H', "That's the idea that runs through the whole paper. What you can't measure in space, you can sometimes recover from time. A longer history stands in for a missing sensor."),
        ('H', "Look at the attention weights, and they tell the same story. With too little history, attention jumps around from step to step. With enough, it becomes more structured, spreading across more of the past steps."),
        ('H', 'One small thing we noticed, about the two frequencies.'),
        ('H', 'The paper reports the lower one at about four point one hertz, that is, cycles per second. From the parameters it lists, we get about three point three.'),
        ('H', "The higher one agrees, at about nine point five. It doesn't change the story. But it's worth asking about."),
    ]),

    # ---------------------------------------------------------------- 3b. attention as delay embedding: Van der Pol (§4.1, Table 1, Fig. 6)
    dict(title='Rebuilding a hidden state', music='sting', lines=[
        ('H', 'Now make it nonlinear. Here, attention alone is not enough.'),
        ('H', "The transformer's second part takes over: a small, ordinary neural network that comes after the attention step. It's often called an MLP, and it does the nonlinear work."),
        ('H', 'The system is the Van der Pol oscillator. Almost wherever it starts, it settles onto the same smooth loop, called a limit cycle.'),
        ('H', "Its state has two numbers: a position, and a velocity."),
        ('H', "First experiment: show the models the full state. The comparison is a plain MLP on its own, with no attention, predicting from the current state alone."),
        ('H', "It does as well as the transformer. Both are essentially perfect, with a mean squared error of about ten to the minus seven."),
        ('H', "That makes sense. If you can see the whole state, the past adds nothing. The system has no memory beyond its present."),
        ('H', 'Second experiment: hide the velocity. Show only the position.', 0.5),
        ('H', "Now the plain MLP is stuck. The same position happens twice on every loop, once going up, once coming down. From one number, it can't tell which."),
        ('H', "The transformer reads five past positions. And with those, it can tell up from down."),
        ('H', "If the last few positions were rising, it's on the way up. If they were falling, it's on the way down."),
        ('H', "The numbers are striking. The best transformer's error is more than a thousand times smaller than the plain MLP's."),
        ('H', 'More than a thousand times.', 0.4),
        ('H', "There's a classic result behind this, called Takens' theorem."),
        ('H', 'Take a single measurement, and stack up copies of it from the recent past. Those past copies are called delays.'),
        ('H', "Under mild conditions, enough delays pin down the full state of the system. The count it gives is twice the system's dimension, plus one."),
        ('H', "Van der Pol has two dimensions, position and velocity. So five delays."),
        ('H', "The authors look inside, and what they find fits that picture. For the same position, attention adds a different correction, depending on where the cycle is."),
        ('H', "The model passes what it reads through a small internal space, just a few numbers wide. Give that space two dimensions, and the loop itself appears in it."),
        ('H', "Attention also spreads its weight over several past steps, rather than picking one. Which is what you'd expect, if it's building a state out of several delays."),
        ('H', "There's a classical baseline, too. A polynomial model gets the same five delays. It does about as well as the simpler transformers, and much worse than the best one."),
        ('H', 'Now, a detail where the paper disagrees with itself.', 0.5),
        ('H', "The best model is also told the order of the past steps. That's called positional encoding."),
        ('H', "In this section, the text says positional encoding changes the attention pattern, but doesn't systematically improve accuracy."),
        ('H', "The paper's own table says otherwise. With only the position observed, the model with two internal dimensions is about eighty-six times more accurate with positional encoding than without it."),
        ('H', "And the conclusions say it helps. Worth raising on Wednesday."),
        ('H', "Quick recap. If the model sees the whole state, history adds nothing. If part of it is hidden, attention rebuilds it from the recent past. That's Takens' idea, carried out by a network.", 0.4),
        ('H', "But rebuilding it is one thing. Can a small model hold what it rebuilds?"),
    ]),

    # ---------------------------------------------------------------- 4a. room to unfold: Chafee-Infante (§4.2, Figs. 7-9, App. A.3-A.4)
    dict(title='Room to unfold', music='sting', lines=[
        ('H', "Part four. Here's a case where the history is long enough, but the model's internal space is too small."),
        ('H', 'The test is a reaction-diffusion equation, known as Chafee-Infante. Picture a temperature-like quantity along a rod.'),
        ('H', 'It spreads out along the rod. And at each point, it gets pushed toward one of two values.'),
        ('H', "In the experiment, the authors simulate it with three sine-wave patterns. And over time, the motion settles onto a surface with just two dimensions."),
        ('H', "The model sees the field at a single point. Five past values of it. By Takens' theorem, that should in principle be enough to rebuild the two-dimensional surface."),
        ('H', "Give the transformer two internal dimensions, and it can't lay the surface out. Its internal states collapse onto a thick curve."),
        ('H', "And it's unreliable. From one training run to the next, the results swing a lot, and some runs do worse than the plain MLP."),
        ('H', "Give it three internal dimensions, and in all but one of their training runs, the surface unfolds. The field's main patterns line up smoothly with the model's internal coordinates."),
        ('H', "Why would it need three dimensions to represent a two-dimensional surface?", 0.5),
        ('H', "The authors' answer: the model has two jobs. First, unfold the past values. Then, squeeze them down onto the surface. With only two dimensions, it has to squeeze too early."),
        ('H', "Here's a picture. Crumple a sheet of paper into a ball. It's still a flat sheet. But to see that, you have to smooth it out first, and smoothing it out takes room."),
        ('H', "A third direction gives it room to unfold first, and flatten afterwards."),
        ('H', "And the system's symmetry may make it harder. From that one sensor, states that are far apart can look nearly the same."),
        ('H', "One thing to keep in mind. The authors picked two and three dimensions because they already knew the surface was two-dimensional. With a new system, you'd have to estimate that first."),
        ('H', "Takens' theorem says the information is in the history. It does not say a small model can hold it. That's the point I like most in this paper."),
    ]),

    # ---------------------------------------------------------------- 4b. telling regimes apart: cylinder flow (§4.3, Figs. 11-12, A.5)
    dict(title='Telling regimes apart', music='sting', lines=[
        ('H', 'The last system is the most physical. A fluid flowing past a cylinder, shedding swirls called vortices, like a flag fluttering behind a pole.'),
        ('H', "How fast the vortices shed, and the shape of the wake behind the cylinder, depend on one number, the Reynolds number."),
        ('H', "Roughly, it compares how fast the flow is with how sticky the fluid is."),
        ('H', "In this data, every flow settles into a steady rhythm of shedding. A loop that repeats."),
        ('H', 'The data run from a Reynolds number of one hundred to seven hundred fifty. The model trains on the middle of that range. It\'s tested inside the range, and just beyond both ends.'),
        ('H', "Again, it sees only one point in the flow: how fast the fluid is moving downstream, at a single spot behind the cylinder."),
        ('H', "The authors train two versions. One sees only that single point. The other is also told the Reynolds number."),
        ('H', "Both get three internal dimensions. The authors' reasoning: two for the loop, and one for the Reynolds number."),
        ('H', "Both predict the next step reasonably well. The question is what they've learned inside."),
        ('H', "Each flow traces a loop inside the model. Without the Reynolds number, the loops for different flows pile on top of each other. And the errors grow toward the edges of the range, and beyond it."),
        ('H', 'Tell it the Reynolds number, and the loops separate, lined up in order. Errors become low, and even across the range.', 0.5),
        ('H', "Then the real test. Can you rebuild the whole flow field from the model's internal state?"),
        ('H', "To find out, they fit a separate method that maps the internal state back to the flow everywhere around the cylinder."),
        ('H', 'With the Reynolds number, yes, accurately. Without it, the errors are about seventy times larger over the whole field.'),
        ('H', "In the wake, right where the shedding depends most on the Reynolds number, they're about fifty times larger."),
        ('H', "Here's the line from the paper I'd underline. Predicting the next step well, and having an internal state you can read the physics from, are not the same thing.", 0.4),
        ('H', "A model can predict the next step well, while quietly mixing up different regimes inside: different physical situations that it treats as one."),
        ('~', 'chime'),
        ('H?', "Something to bring on Wednesday. Picture two models that predict the next step equally well. Only one has an internal state you could rebuild the physics from. How would you even notice the difference?"),
    ]),

    # ---------------------------------------------------------------- 5. emulators (our extrapolation)
    dict(title='What it might mean for emulators', music='sting', lines=[
        ('H', "Now, our own corner. This part is our extrapolation, not something the paper tests."),
        ('H', "Machine-learned climate emulators learn to step the atmosphere, and sometimes the ocean, forward in time. Many of them predict from the current state alone, with no memory of the past."),
        ('H', "The Van der Pol result suggests that's fine, if the state is complete. But an emulator usually isn't shown everything. The deep ocean, the soil, processes it never sees."),
        ('H', "That is exactly where the paper finds history earns its keep."),
        ('H', "The cylinder result might be the closest match. Swap the Reynolds number for the forcing: greenhouse gases, sea surface temperatures."),
        ('H', "An emulator that is never told the forcing might quietly mix climates together inside. And it might struggle most at the edge of its training. A warmer future climate sits at, or past, that edge."),
        ('H', "It also argues for how we test emulators. Low error on the next six hours doesn't prove a sound internal state. Spectra, modes, and long-run statistics are where that would show."),
        ('H', "One caution. Emulators are often too smooth, which sounds like the sign problem. But in big models, we suspect that smoothing comes mostly from how they are trained, not from softmax. Similar symptom, probably a different cause."),
        ('H', "And many emulators, including ones we work with, aren't even transformers. So it's the general lessons that carry over, not the softmax details."),
        ('H', "Some emulators already use a step or two of the past as input. This paper gives us a way to ask what that history is actually doing."),
        ('~', 'chime'),
        ('H?', "Here's one for us. Which hidden variables, or forcings, should an emulator be told explicitly, and which should it be left to infer from history?"),
    ]),

    # ---------------------------------------------------------------- 6. our reading (§5; caveats)
    dict(title='How far it goes', music=None, lines=[
        ('H', "Let's be fair about the limits."),
        ('H', "Everything here is a one-layer model, mostly with one head, on clean simulated data."),
        ('H', "Real measurements are noisy. How much history a model needs when the data are noisy is a fair question to bring."),
        ('H', "The authors say the single-head limit shouldn't be read as a limit of real transformers. And they say deeper models might not need to be told the Reynolds number. They leave that for future work."),
        ('H', "The conclusions say the experiments confirm Takens' theorem. That's too strong. You can't confirm a theorem with an experiment. The results are consistent with it."),
        ('H', "In the nonlinear examples, they mostly give the model at least as much history as the theorem asks for. And for the cylinder, five past values were already enough. That's fewer than the seven the theorem asks for, by the paper's own count."),
        ('H', "They also note that the Reynolds numbers in their data are fairly close together, which may make the flows harder to tell apart."),
        ('H', "And there are those two small inconsistencies: the two-mass frequencies, and what the text and the table say about positional encoding."),
        ('H', "Still, I like this paper a lot. It does what mechanistic interpretability should do. It predicts, from the math, where a model will fail. Then it shows the failure, and then the fix."),
    ]),

    # ---------------------------------------------------------------- wrap-up
    dict(title='Wrap-up', music='sting', lines=[
        ('H', "Let's recap."),
        ('H', 'A single attention head, with nothing else around it, behaves like a classic forecasting model, with one catch. It can only average the past, so dynamics that need subtraction get smoothed. A second head with an opposite sign fixes it.'),
        ('H', "When the full state is visible, attention adds little. When it's hidden, attention rebuilds it from history, in a way that matches Takens' theorem."),
        ('H', "But history isn't everything. The model needs enough internal room to unfold what it rebuilds. And it may need to be told the parameters that separate one regime from another."),
        ('H', 'Above all, predicting the next step well is not the same as having an internal state you can rebuild the physics from.', 0.6),
        ('H', "Here are the questions once more, for the room."),
        ('~', 'chime'),
        ('H?', 'One. If a second head fixes the sign problem, what is the single-head result teaching us?'),
        ('H?', 'Two. How would you notice that a model predicts well, but mixes up regimes inside?'),
        ('H?', 'And three. What should an emulator be told, and what should it infer from history?', 0.4),
        ('H', "Bring your disagreements. That's what journal club is for.", 2.0),
        ('H', 'Thanks for listening to the aigs pod. See you on Wednesday.', 0.6),
    ]),
]
