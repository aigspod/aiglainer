"""LAWFUL short: what the law forbids. A camera over the video's Doppler scene (the law, then radial vs sideways), then
the Fig. 4b chart (tangential scaling: data extracted from the paper)."""
VOICE = 'michael'

SCENES = [
    dict(scene='Doppler', crop=[(0.0, (140, 330, 700, 460)), (8.6, (1000, 300, 810, 570))], vstart=1.8, headline='Check what the law *forbids*', beats=[
        (1.9, 'Want to know if an AI really learned a law of physics? Check what the law forbids.'),
        (2.4, "A radar's Doppler shift depends only on motion toward it, or away from it."),
        (9.0, 'Move sideways across its view, and there is essentially no shift at all.'),
    ]),
    dict(scene='Fig4b', crop=(72, 290, 938, 700), vstart=1.6, headline='Sideways only: does it stay *quiet*?', beats=[
        (1.7, 'So researchers took real walks, removed the motion toward the radar, and scaled only the sideways part.'),
        (3.0, "Physics says the response should stay near zero. That's the blue line."),
        (6.0, 'The network, in green, stays near zero too. And when the body stands still, its predicted Doppler centroid lands right on zero.'),
        (14.0, "That's its behavior. How the network enforces the rule inside is still an open question."),
    ]),
]
