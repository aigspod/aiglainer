"""Short: trust. Facts: §3.1 (gain), §4.3.3, Fig. 8 of arXiv:2611.18393v1, via projects/weatherdreamer/AGENTS.md."""
VOICE = 'bella-nicole'
SPEED = 1.0

SCENES = [
    dict(scene='TrustGain', headline='Nobody told it whom to *trust*', hold=0.5, beats=[
        (0.3, 'Your forecast says twenty degrees. A thermometer says twenty-two. How far should you move?'),
        (6.0, 'It depends on how noisy each one is. That fraction is called the gain, and forecasting systems usually set the errors behind it by hand.'),
    ]),
    dict(scene='TrustLearned', headline='Nobody told it whom to *trust*', hold=2.4, beats=[
        (0.3, 'This model was never told. Yet for its microwave temperature channels, the noise it assumes is two to four tenths of a degree, the real noise of those instruments in orbit.'),
        (9.0, "It isn't perfect. It's timid there, moving sixty-four percent of the way where about eighty-two would be best."),
        (13.5, "It's too trusting of satellite winds over the ocean, and it barely listens to weather balloons high up."),
        (19.0, 'How would you teach a model whom to trust?'),
    ]),
]
