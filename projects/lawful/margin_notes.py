"""Handwritten margin notes for the LAWFUL video: scene name -> notes (format in explainer/notes.py)."""

NOTES = {}

NOTES.update({
    'MechInterp':    [dict(t=7.5, text='opening the box', x=1195, y=340, rot=-4, arrow=(1190, 330, 1150, 372))],
    'Question':      [dict(t=15.0, text='accuracy is the easy part', x=1290, y=236, rot=-3)],
    'Testbed':       [dict(t=2.5, until=13.4, text='no velocity anywhere in here', x=150, y=915, rot=-2, arrow=(380, 890, 360, 852))],
    'Doppler':       [dict(t=10.0, text='sideways? no shift.', x=1440, y=282, rot=-3)],
    'Framework':     [dict(t=23.5, text='two models, one yardstick', x=1265, y=462, rot=-4)],
    'Counterfactual':[dict(t=8.0, until=10.6, text='slow-mo, but only toward the radar', x=1240, y=272, rot=-3, size=32)],
    'Score':         [dict(t=6.0, text='steeper line = bigger response', x=1080, y=236, rot=-3)],
    'Domain':        [dict(t=8.0, text="the radar's speed limit", x=1400, y=378, rot=-3, arrow=(1420, 392, 1374, 432))],
    'Patching':      [dict(t=8.0, until=22.0, text='swap in the what-if, see what follows', x=1520, y=460, rot=-3, size=30)],
    'Search':        [dict(t=14.0, until=22.2, text='mostly the part that looks across time', x=720, y=812, rot=-2, size=30)],
    'Fig4a':         [dict(t=10.0, text='the model keeps up with the law...', x=640, y=400, rot=-3, size=30),
                      dict(t=22.0, text='...until the radar runs out of road', x=960, y=900, rot=-2, size=30, color='r', arrow=(1010, 868, 965, 815))],
    'Fig4b':         [dict(t=11.5, text='standing still = silence', x=290, y=640, rot=-3, size=30, arrow=(450, 655, 600, 815))],
    'Probes':        [dict(t=13.0, text='no single head knows. together, they do.', x=1300, y=640, rot=-3, size=30)],
    'QKVal':         [dict(t=12.0, until=15.6, text='where to look > what to carry', x=1240, y=650, rot=-3)],
    'Heatmaps':      [dict(t=14.0, until=24.4, text='early + late = a difference = velocity', x=1130, y=868, rot=-2, size=30)],
})
