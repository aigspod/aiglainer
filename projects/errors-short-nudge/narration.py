"""Short: nudge. Facts as noted in project.py's DESCRIPTION."""
VOICE = 'bella'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='NudgeGrid', headline='Same error rate, *different* errors', beats=[
        (0.3, 'Two systems can be wrong equally often, and still be wrong about completely different things.'),
        (5.0, 'Here is a model that gets four of these twenty-four sentences wrong.'),
        (9.0, 'Nudge a circuit toward the wrong answer, and it gets four wrong too. Same error rate.'),
        (14.0, 'But only one of those mistakes is shared. Matching how often is not matching where.'),
        (19.0, 'And that is why circuits that look faithful can still miss the mistakes.'),
    ]),
]
