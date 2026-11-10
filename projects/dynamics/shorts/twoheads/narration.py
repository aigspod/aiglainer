"""Short: twoheads. Facts: App. A.1 of arXiv:2512.21113v2 (two heads, W_O = [1.087, -1.244], opposite signs); the
spectra are our simulation, the one-head fit and the two-head version ours, said on screen."""
VOICE = 'michael'
SAY = {}

SCENES = [
    dict(scene='TwoHeadsMix', headline='Two heads, one *subtraction*', beats=[
        (0.3, "One attention head can't model a soft spring. Two heads can, with a subtraction."),
        (5.0, 'Each head still averages, with positive weights.'),
        (10.0, 'But each has its own output number. In the paper: one point zero eight seven, and minus one point two four four.'),
        (17.5, 'Opposite signs: one average minus the other.'),
    ]),
    dict(scene='TwoHeadsSpec', headline='Two heads, one *subtraction*', hold=2.2, beats=[
        (0.4, 'In our simulation, one head flattens the resonance.'),
        (3.6, 'Our two-head version brings it back.'),
        (8.0, 'So is the limit attention, or just one head?'),
    ]),
]
