"""Short: rare. Facts as noted in project.py's DESCRIPTION."""
VOICE = 'michael'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='Fig1', vstart=12.2, crop=(722, 320, 600, 300),
         headline='Are mistakes just *rare*?', beats=[
        (12.4, "Maybe circuits miss a model's mistakes because mistakes are rare. Nothing to learn from."),
        (15.5, "So test models that make lots of them. Solid line: agreement where the model is right. Dashed: the same mistake where it's wrong."),
        (21.5, 'For Gemma on hard science questions, thirty-eight percent of the examples used to find the circuit are its own mistakes.'),
        (27.0, 'And the dashed line still sits below the solid one, at every size. Rarity is part of the story, not all of it.'),
    ]),
]
