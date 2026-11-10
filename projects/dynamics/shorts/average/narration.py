"""Short: average. Facts: §2.3 and §3.1 of arXiv:2512.21113v2 (softmax weights, one shared output weight, Case 1's
coefficients, Fig. 2b); Case 2's values are our calculation, said on screen."""
VOICE = 'bella'
SAY = {}

SCENES = [
    dict(scene='AvgMix', headline='Attention can only *average*', beats=[
        (0.3, "Why can't one attention head predict a soft spring? Because attention can only average."),
        (3.5, 'Its weights on the last two positions come from a softmax: positive, adding up to one.'),
        (12.0, 'One output number scales both, so both coefficients share its sign.'),
    ]),
    dict(scene='AvgPlane', headline='Attention can only *average*', hold=2.2, beats=[
        (0.4, 'A stiff spring needs two negative coefficients. That works.'),
        (5.0, 'A softer spring needs a plus and a minus: out of reach.'),
        (9.5, 'In the paper, that head comes out too smooth.'),
        (13.0, "That's one head alone. Where else could a minus come from?"),
    ]),
]
