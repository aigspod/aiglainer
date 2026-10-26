"""LAWFUL short: the what-if radar. Pairs of panels cut from the video's Spectrograms scene (data from Fig. 3)."""
VOICE = 'bella'

GT, F, FX, CIRC, COMP = (105, 360, 330, 390), (435, 360, 330, 390), (825, 360, 330, 390), (1155, 360, 330, 515), (1485, 360, 330, 515)

SCENES = [
    dict(scene='Spectrograms', id='SpecA', stack=[GT, F], vstart=1.6, headline='Can a network learn the *Doppler* effect?', beats=[
        (1.7, 'Can a neural network learn the Doppler effect, without ever being told about it?'),
        (2.0, 'This is radar from a person walking around. The swings are the body moving toward and away from the radar.'),
        (5.5, 'A small network learned to predict it from motion capture alone. Positions in, radar out.'),
    ]),
    dict(scene='Spectrograms', id='SpecB', stack=[F, FX], vstart=2.5, headline='Replay it at *30%* speed', beats=[
        (3.0, 'Now replay the walk with every move toward the radar slowed to thirty percent. Physics says the swings should shrink.'),
        (6.0, "And the network's prediction shrinks, just like physics says."),
    ]),
    dict(scene='Spectrograms', id='SpecC', stack=[CIRC, COMP], vstart=9.5, headline='Which half *does* it?', beats=[
        (11.0, 'Patch in only half the network, the circuit, and it shrinks too.'),
        (14.5, 'Patch in the other half, and the swings stay full size.'),
        (16.0, 'So we know where the behavior lives. How it works is still an open question.'),
    ]),
]
