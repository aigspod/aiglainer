"""LAWFUL short: readable isn't used. Probe R^2 values from Tables 2 and 5."""
VOICE = 'michael'

SCENES = [
    dict(scene='ProbeBars', headline='Readable isn\'t the same as *used*', beats=[
        (0.4, "Here's a trap in AI research. Finding information inside a network doesn't mean the network uses it."),
        (3.0, 'Researchers trained probes to read velocity from a small transformer that predicts radar.'),
        (5.5, 'Right before the attention layer, almost nothing. The best single attention head, a little.'),
        (9.0, "All the circuit's heads together: zero point seven six. Now it's readable."),
        (12.5, "The next layer reads it too. But replace the attention's output with its average, and it drops to almost zero."),
        (17.0, 'Readable tells you where to look. Only an intervention tells you what the network uses.'),
    ]),
]
