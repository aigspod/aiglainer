"""Short: mystery. Facts: §5.3 and §5.3.1 (Sutskever's quote; hard induction: rule 30, 4 steps, n = 32, first h bits
hidden; 2^h candidates; Fig. 5b epiplexity 2.43 -> 5.56 million bits for h = 0..5) via projects/epiplexity/AGENTS.md."""
VOICE = 'bella-nicole'
SPEED = 1.0

SCENES = [
    dict(scene='MysteryLanes', headline='The reader works *harder*', hold=0.5, beats=[
        (0.3, "When you read a murder mystery, you work harder than the author did."),
        (4.0, "The author can pick the culprit first, then write the clues."),
        (8.0, "But to predict the name, the reader must work it out from the clues."),
    ]),
    dict(scene='MysteryBits', headline='The reader works *harder*', hold=2.4, beats=[
        (0.3, "The paper's tiny version: random bits, scrambled by a simple rule, with a few hidden."),
        (6.5, "To predict the output, the model must reason about the hidden bits. Each one doubles the possibilities."),
        (12.5, "The structure it learns more than doubles, from zero hidden bits to five."),
        (18.5, "So a model can learn more than what made its data. What else must it work out?"),
    ]),
]
