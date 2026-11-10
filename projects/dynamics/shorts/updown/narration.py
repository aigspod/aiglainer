"""Short: updown. Facts: §4.1 and Table 1 of arXiv:2512.21113v2, via projects/dynamics/AGENTS.md (see project.py's
DESCRIPTION). The windows are our simulation and say so on screen."""
VOICE = 'michael'
SAY = {'MLP': 'M L P'}

SCENES = [
    dict(scene='UpDownGauge', headline='Same position, two *directions*', beats=[
        (0.3, 'This dot moves up and down. All you see is its height.'),
        (4.5, "Right now it's at one. Is it rising, or falling? From one snapshot, you can't tell."),
        (11.0, 'But the last five snapshots can. One window climbs toward one, the other falls toward it.'),
    ]),
    dict(scene='UpDownBars', headline='Same position, two *directions*', hold=2.4, beats=[
        (0.3, 'Hide the velocity, and a network that sees only the current position does worst.'),
        (6.0, 'A one-layer transformer reading the last five samples does about three orders of magnitude better.'),
        (12.5, 'So how much history does a model need, to see what is hidden?'),
    ]),
]
