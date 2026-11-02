"""Short: gap. Facts as noted in project.py's DESCRIPTION."""
VOICE = 'michael'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='GapBars', headline='*99.5%* vs 15%', beats=[
        (0.3, "Here's a strange number about how we explain neural networks."),
        (3.0, 'A famous circuit inside GPT-2 agrees with the model ninety-nine point five percent of the time, when the model is right.'),
        (8.0, 'When the model is wrong, it makes the same mistake only fifteen percent of the time.'),
        (13.0, "By the usual average score, it looks very faithful. But an explanation that skips the mistakes can't tell you why they happen."),
    ]),
]
