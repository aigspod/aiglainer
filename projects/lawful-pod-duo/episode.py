"""Episode script (see aiglainer/podcast.py). Facts follow projects/lawful/narration.py, which cites the paper.
The host explains; the co-host asks what a newcomer would ask."""

HOSTS = {'H': 'bella', 'C': 'michael'}       # host and co-host, from aiglainer/hosts.py

SEGMENTS = [
    dict(title='Cold open', music=None, lines=[
        ('H', 'A neural network watches a person walk, and predicts what a radar will see.'),
        ('C', "And it's good at it?"),
        ('H', 'Very good. But did it learn the physics, or did it just get good at guessing?'),
        ('C', 'And today, a paper that found a way to check.'),
    ]),
    dict(title='Welcome', music='theme', lines=[
        ('H', 'Welcome to the aigs pod. This is a short pilot for our journal club.'),
        ('C', 'Quick note: both of our voices are synthetic, generated on a laptop.'),
        ('H', 'The paper is LAWFUL, by Kevin Chen, Kenneth Parker, and Anish Arora, from the mechanistic interpretability workshop at ICML.'),
    ]),
    dict(title='The setup', music='sting', lines=[
        ('C', 'So start me off. What does this model actually do?'),
        ('H', 'It takes in motion capture: fifty-three markers on a moving body, frame after frame. And it predicts a radar spectrogram.'),
        ('C', 'Which is what, exactly?'),
        ('H', 'A picture of how fast each part of the body moves toward or away from the radar, over time.'),
        ('C', "And there's a law for that."),
        ('H', 'The Doppler law. The frequency shift is twice the speed toward the radar, divided by the wavelength.'),
        ('H', "Here's the catch. The model was never shown a single velocity. Only positions in, and radar out.", 0.6),
        ('C', 'So if it gets the radar right, it must be working out speed somewhere inside.'),
        ('H', "That's the bet. And the paper checks it in three steps: behavior, cause, and mechanism."),
    ]),
    dict(title='Behavior', music='sting', lines=[
        ('C', 'Behavior first. How do you test whether a model follows a law?'),
        ('H', 'You ask it what-if questions. Take a recording of someone walking, and slow every movement toward the radar to thirty percent. Leave the sideways motion alone.'),
        ('C', 'And physics says the Doppler shift should drop to thirty percent too.'),
        ('H', 'Exactly. Do that across a whole range, from fast, to frozen, to reversed, and compare the model with the law.'),
        ('C', 'And?'),
        ('H', 'Within the speeds this radar can measure, the agreement is zero point nine eight eight, out of one.'),
        ('C', "That's close to perfect."),
    ]),
    dict(title='Cause and mechanism', music='sting', lines=[
        ('C', 'Okay, but a model can get the right answer for the wrong reason. Which parts are doing the work?'),
        ('H', "That's step two. The tool is activation patching. You copy what a few components compute on the what-if input into the original run, and see if the output follows."),
        ('C', 'So you transplant a few parts, and see if the behavior comes with them.'),
        ('H', 'Right. A search grows that set of parts. About half the components recover ninety-one percent of the agreement. And nearly all of them look across time, not across the body.'),
        ('C', 'Which makes sense. Speed is a change over time.'),
        ('H', 'And step three shows how. One attention head looks at the earliest frames. Another looks at the latest.'),
        ('C', 'Late position, minus early position.'),
        ('H', "That's velocity."),
    ]),
    dict(title='For journal club', music='sting', lines=[
        ('C', 'So what should people bring to the meeting?'),
        ('H', 'Three questions. Is one number, the average Doppler shift, enough to say the model uses the law?'),
        ('C', "Outside the radar's range, the agreement breaks down. Is that physics, or just unfamiliar data?"),
        ('H', 'And what would this method need, for a law nobody knows in advance?'),
        ('C', "That's the pilot.", 0.7),
        ('H', 'See you at journal club.'),
    ]),
]
