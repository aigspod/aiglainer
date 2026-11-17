"""Short: stripes. Facts: Fig. S3 and caption; §4.1 (station denial); §5 of arXiv:2611.18393v1, via projects/weatherdreamer/AGENTS.md."""
VOICE = 'michael'
SPEED = 1.0

SCENES = [
    dict(scene='StripesMemory', headline='Its memory holds *stripes*', hold=0.5, beats=[
        (0.3, "This is the inside of a weather model's memory, mapped across the globe."),
        (5.0, 'Some channels look like weather. But others show round footprints, and long diagonal stripes.'),
        (11.0, 'Those are the places its satellites were looking.'),
    ]),
    dict(scene='StripesWhy', headline='Its memory holds *stripes*', hold=2.4, beats=[
        (0.3, 'Why remember that? A filter has to know where it looked, to know how sure to be. Classical filters keep that in their error estimates.'),
        (9.0, 'The narrow weather state that the model reads out from is mostly weather, with only a faint trace.'),
        (15.0, 'The open test: swap one satellite for another. Does the weather picture stay put?'),
    ]),
]
