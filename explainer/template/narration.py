"""Narration: the scene order of the narrated cut, and what Bella says over each scene.

Each beat is (visual_time, text): visual_time is the moment in the scene's authored timeline when the thing the
line talks about appears. The build lays lines end to end and time-warps each scene to meet them.
Optional per scene: smax (fastest catch-up speed, default 1.8), hold (seconds after the last line, 0.75),
vend (authored time to end the scene at), still (seconds frozen at the end).
Write for the ear, ~145 words a minute; spell symbols out ("alpha", "tau"). Respellings go in SAY.
"""

VOICE = 'af_bella'      # audition others with `make voices`
SPEED = 1.0
LANG = 'a'              # a = American, b = British English
SAY = {}                # written form -> what to pronounce, e.g. {'MLP': 'M L P'}

SCENES = [
    dict(scene='Title', hold=1.0, beats=[
        (0.6, '__TITLE__: a short explainer, made with the template.'),
    ]),
    dict(scene='Question', beats=[
        (0.6, 'Every good explainer starts with the question the paper is trying to answer.'),
        (2.0, 'First, say why it matters.'),
        (4.0, 'Then, what makes it hard.'),
        (6.0, 'And finally, what the paper does about it.'),
    ]),
    dict(scene='Method', beats=[
        (0.8, 'Here is the key equation, typeset with LaTeX.'),
        (4.0, 'And here is a curve, drawn from numbers in the data folder, not traced by eye.'),
        (9.0, 'Handwritten notes add the occasional aside.'),
    ]),
    dict(scene='Takeaway', hold=3.0, beats=[
        (0.6, 'End with the takeaway, the key numbers, and where to find the paper. See you at journal club.'),
    ]),
]
