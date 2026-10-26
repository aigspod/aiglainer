"""Episode script (see aiglainer/podcast.py). Facts follow projects/lawful/narration.py, which cites the paper."""

HOSTS = {'H': 'bella'}       # role -> host in aiglainer/hosts.py; 'michael' re-voices the episode

SEGMENTS = [
    dict(title='Cold open', music=None, lines=[
        ('H', "Here's a puzzle. A neural network watches a person walk, and predicts what a radar will see."),
        ('H', "It's accurate. Really accurate. But did it learn the physics, or did it just get good at guessing?"),
        ('H', 'Today: a paper that found a way to check.'),
    ]),
    dict(title='Welcome', music='theme', lines=[
        ('H', "Welcome to the aigs pod. This is a short pilot for our journal club. The voice you're hearing is synthetic, generated on a laptop."),
        ('H', 'The paper is called LAWFUL, by Kevin Chen, Kenneth Parker, and Anish Arora, from the mechanistic interpretability workshop at ICML.'),
    ]),
    dict(title='The setup', music='sting', lines=[
        ('H', 'First, the setup. The model takes in motion capture: fifty-three markers on a moving body, frame after frame.'),
        ('H', 'And it predicts a radar spectrogram. Think of it as a picture of how fast each part of the body is moving toward or away from the radar, over time.'),
        ('H', 'Radar obeys a simple law, the Doppler law. The frequency shift is twice the speed toward the radar, divided by the wavelength.'),
        ('H', "Here's the catch. The model was never shown a single velocity. Only positions in, and radar out.", 0.6),
        ('H', 'So if it predicts the radar correctly, somewhere inside, it has to turn positions into speed. Does it?'),
    ]),
    dict(title='Behavior, cause, mechanism', music='sting', lines=[
        ('H', 'The paper checks in three steps: behavior, cause, and mechanism.'),
        ('H', 'Behavior first. Imagine taking a recording of someone walking, and replaying it with every movement toward the radar slowed to thirty percent. The sideways motion stays the same.'),
        ('H', 'Physics tells you exactly what should happen: the Doppler shift should shrink to thirty percent too.'),
        ('H', "These what-if inputs are called counterfactuals. Run lots of them, from fast, to frozen, to reversed, and compare the model's response with the law's."),
        ('H', 'Within the speeds this radar can actually measure, the agreement score is zero point nine eight eight, where one is perfect. The behavior follows the law.'),
        ('H', 'Step two, cause. Which parts of the network produce that behavior?', 0.8),
        ('H', 'The tool is activation patching. You copy what a few components compute on the what-if input into the original run, and see whether the output follows.'),
        ('H', 'A search grows that set of components, piece by piece. About half of them recover ninety-one percent of the agreement, and nearly all sit in the part of the model that looks across time.'),
        ('H', 'Step three, mechanism. How do those parts compute speed?', 0.8),
        ('H', 'Two attention heads give it away. One looks at the earliest frames. The other looks at the latest.'),
        ('H', "And velocity is exactly that: where you are late, minus where you were early."),
    ]),
    dict(title='For journal club', music='sting', lines=[
        ('H', 'Some things to bring to the meeting.'),
        ('H', 'Is one number, the average Doppler shift, enough to say the model uses the law?'),
        ('H', "Outside the radar's range, the agreement breaks down. Is that physics, or just data the model never saw?"),
        ('H', 'And the big one: what would this method need, for a law nobody knows in advance?'),
        ('H', "That's the pilot. See you at journal club.", 0.9),
    ]),
]
