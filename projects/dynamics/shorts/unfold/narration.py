"""Short: unfold. Facts: §4.2 and App. A.4 of arXiv:2512.21113v2, via projects/dynamics/AGENTS.md (see project.py's
DESCRIPTION). The fold is our simulation; the latent pictures are illustrations; both say so on screen."""
VOICE = 'bella'

SCENES = [
    dict(scene='FoldV', headline='Room to *unfold*', beats=[
        (0.3, 'A model can have all the information it needs, and still not have room to use it.'),
        (5.5, 'Here is our simulation of a rod whose shapes settle onto a surface with two mirror halves.'),
        (11.0, 'Through one sensor, that surface folds. States far apart nearly touch.'),
    ]),
    dict(scene='RoomV', headline='Room to *unfold*', hold=2.4, beats=[
        (0.4, 'Give a small transformer a latent of two numbers, and it squashes the surface into a thick curve.'),
        (8.5, 'Give it three, and the surface unfolds.'),
        (12.0, 'Five readings held the information. What it lacked was room. How much room does your model have?'),
    ]),
]
