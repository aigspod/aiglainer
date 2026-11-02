"""Short: faithful. Facts as noted in project.py's DESCRIPTION."""
VOICE = 'bella'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='Faithful', headline='More faithful than *perfect*?', beats=[
        (0.3, 'Can an explanation be more faithful than the thing it explains?'),
        (3.0, 'Circuits are scored by faithfulness: does the small circuit prefer the right answer as strongly as the full model? One is perfect.'),
        (9.0, 'One automated circuit scores almost one and a half. It is more sure of the right answer than the model itself.'),
        (14.0, "And it reproduces only eleven percent of the model's mistakes. Too right to be faithful."),
    ]),
]
