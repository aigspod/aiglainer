"""Short: pixels. Facts: §6.2 and Fig. 8a (fig8_natural.json; 5B tokens per §6.2, see the topic's accuracy note) via
projects/epiplexity/AGENTS.md: CIFAR-5M has 3.2x OpenWebText's total bits but under a third of its epiplexity."""
VOICE = 'bella-nicole'
SPEED = 1.0
SAY = {'epiplexity': 'eppiplexity'}

SCENES = [
    dict(scene='PixelsTotal', headline='Why text beats *pixels*', hold=0.5, beats=[
        (0.3, "Which holds more information: a pile of web text, or a pile of tiny images?"),
        (5.2, "Count the raw bits, and the images win, with more than three times as many."),
    ]),
    dict(scene='PixelsStructure', headline='Why text beats *pixels*', hold=2.4, beats=[
        (0.4, "Now count only the structure a model can learn. The paper calls it epiplexity."),
        (6.0, "The ranking flips. Text from the web comes out on top, and chess comes next. The images come last."),
        (13.0, "Over ninety-nine percent of their bits are random detail, like the exact shade of each pixel."),
        (19.0, "So what a file holds isn't what a model can learn. What would you rather train on?"),
    ]),
]
