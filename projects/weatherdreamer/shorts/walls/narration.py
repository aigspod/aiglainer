"""Short: walls. Facts: Table 2, §4.3.3, §5 of arXiv:2611.18393v1, via projects/weatherdreamer/AGENTS.md."""
VOICE = 'bella-nicole'
SPEED = 1.0

SCENES = [
    dict(scene='WallsRatio', headline='Strong below, weak *above*', hold=0.5, beats=[
        (0.3, "At surface weather stations, a model trained only on observations is within about ten percent of NOAA's own system."),
        (6.5, 'Higher up, it falls behind. Balloon winds are two point six times worse on average.'),
    ]),
    dict(scene='WallsCauses', headline='Strong below, weak *above*', hold=2.4, beats=[
        (0.3, 'The paper gives two reasons. First, its dynamics run on patches about one thousand six hundred kilometres wide, too small for the big, slow circulation aloft.'),
        (5.5, 'By our own arithmetic, a jet stream wind crosses one of those patches in about nine hours.'),
        (11.0, 'Second, it leans only lightly on balloon readings up there.'),
        (16.0, 'If you could fix one, which would it be?'),
    ]),
]
