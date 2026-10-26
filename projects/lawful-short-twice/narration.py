"""LAWFUL short: twice wrong, perfect score. A crop of the video's Fig. 4a scene, then a native vertical scene.
The doubled model is a thought experiment about the consistency score (Eq. 9-10), said as such on air."""
VOICE = 'bella'

SCENES = [
    dict(scene='Fig4a', crop=(72, 300, 938, 690), vstart=2.0, headline='Twice wrong, and a *perfect* score?', beats=[
        (2.1, "A model could be twice wrong, and still ace this physics test. Here's how."),
        (4.2, 'Speed up the motion toward a radar, and physics says the Doppler signal scales with it. That\'s the blue line.'),
        (8.0, 'A real network, in green, follows it closely. A score of zero point nine eight eight.'),
    ]),
    dict(scene='TwiceWrong', headline='Same *slope*, same score', beats=[
        (0.4, 'But the score compares each model with its own starting point.'),
        (2.4, 'So picture a second model that always predicts twice the right frequency.'),
        (5.2, 'Slow the motion, and it slows. Speed it up, and it speeds up.'),
        (12.0, 'Same slopes. Same perfect score. Still twice wrong.'),
        (15.5, 'So this score checks the scaling, not the size. What test would you add?'),
    ]),
]
