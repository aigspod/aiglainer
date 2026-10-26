"""LAWFUL short: pattern, not payload. A native vertical scene (numbers from Table 2), then the heatmap crop (Fig. 5)."""
VOICE = 'bella'

SCENES = [
    dict(scene='WhereVsWhat', headline='Where it *looks*, or what it carries?', beats=[
        (0.4, 'Inside a transformer, every attention head does two jobs.'),
        (1.8, 'It decides where to look, and what to carry back.'),
        (5.0, 'Researchers swapped each job separately, using what-if versions of a walk.'),
        (8.0, 'Swap only where the heads look, and about two thirds of the law-following comes back.'),
        (11.5, 'Swap only what they carry, and the score drops below zero.'),
    ]),
    # the camera: both heads, then in on head six (earliest frames), across to head seven (latest), back out to both
    dict(scene='Heatmaps', crop=[(9.0, (110, 295, 950, 520)), (12.0, (125, 295, 460, 520)), (14.0, (595, 295, 460, 520)),
                                 (19.0, (110, 295, 950, 520))], vstart=4.0, headline='Two heads, two *ends* of time', beats=[
        (5.0, 'So where do they look?'),
        (12.0, 'One head watches the earliest moments. Another watches the latest.'),
        (20.0, "Late minus early. That's velocity. Maybe. The paper calls it a possible explanation, not a proof."),
    ]),
]
