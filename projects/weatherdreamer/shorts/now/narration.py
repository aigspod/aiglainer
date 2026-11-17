"""Short: now. Facts: §1, §2.1, §4.1, §5 of arXiv:2611.18393v1, via projects/weatherdreamer/AGENTS.md."""
VOICE = 'bella-nicole'
SPEED = 1.0

SCENES = [
    dict(scene='NowClues', headline='Nobody can see *now*', hold=0.5, beats=[
        (0.3, 'Every weather forecast starts from a picture of the atmosphere right now. And nobody can see right now.'),
        (5.5, 'Stations dot the land. Balloons rise twice a day. Satellites sweep past in stripes, measuring light, not temperature.'),
    ]),
    dict(scene='NowCycle', headline='Nobody can see *now*', hold=2.4, beats=[
        (0.3, 'Stitching those clues into one picture usually takes big physics machinery, every six hours, and it arrives hours late.'),
        (7.0, 'A new model learns the whole job from the clues alone, with no answer key. A fresh global picture every hour, in about a minute and a half on one GPU.'),
        (15.0, 'Near the ground, it already competes with the big forecasts. What would you do with a fresh picture every hour?'),
    ]),
]
