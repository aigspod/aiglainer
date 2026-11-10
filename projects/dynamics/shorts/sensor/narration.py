"""Short: sensor. Facts: §3.2 of arXiv:2512.21113v2 (2-DOF: full observation with 3 tokens works, x1 only with 3
fails, with 4 works; a four-dimensional state). The count is ours, said on screen and on air."""
VOICE = 'bella'
SAY = {}

SCENES = [
    dict(scene='SensorWindow', headline='Time for a missing *sensor*', beats=[
        (0.3, 'Can time stand in for a missing sensor?'),
        (3.0, 'Two coupled masses ring in two modes at once, slow and fast.'),
        (8.5, 'Given both positions and three steps, the transformer finds both modes.'),
        (14.0, 'With only the first mass, three steps fail. The modes are lost.'),
        (19.5, 'Give it four steps, and both modes come back.'),
    ]),
    dict(scene='SensorCount', headline='Time for a missing *sensor*', hold=2.2, beats=[
        (0.4, 'Our rough count: the state is four numbers, two positions and two velocities.'),
        (6.5, 'One sensor adds one number per step. Four steps cover it.'),
        (12.0, "What can't your model see, and how much history would it need?"),
    ]),
]
