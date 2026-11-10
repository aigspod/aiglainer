"""Short: reynolds. Facts: §4.3 and App. A.5 of arXiv:2512.21113v2, via projects/dynamics/AGENTS.md (see project.py's
DESCRIPTION). The wake and the loops are illustrations and say so on screen."""
VOICE = 'michael'

SCENES = [
    dict(scene='LoopsV', headline='Tell it the *Reynolds number*', beats=[
        (0.3, 'Two small transformers watch flow past a cylinder, through one sensor.'),
        (4.5, 'The first is never told the Reynolds number, which sets the regime. Inside, its runs overlap.'),
        (11.5, 'The second gets the Reynolds number as an input, and the runs separate, in order.'),
    ]),
    dict(scene='ReconV', headline='Tell it the *Reynolds number*', hold=2.4, beats=[
        (0.4, "Now rebuild the full field of one velocity component from each model's inner state."),
        (6.0, 'Without the Reynolds number, the error is about seventy times worse.'),
        (11.0, 'Both predict the next reading well. So what is your model not being told?'),
    ]),
]
