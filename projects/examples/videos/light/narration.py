"""The template video re-narrated, to show a different voice over a different look."""
VOICE = 'michael'       # any host in aiglainer/hosts.py, or any Kokoro voice id
SPEED = 1.0
LANG = 'a'              # a = American, b = British English
SAY = {}                # written form -> what to pronounce, e.g. {'MLP': 'M L P'}

SCENES = [
    dict(scene='Title', hold=1.0, beats=[
        (0.6, 'This is the same engine, in a different look.'),
    ]),
    dict(scene='Question', beats=[
        (0.6, 'Everything here comes from a few settings in one file.'),
        (2.0, 'The colors come from a theme.'),
        (4.0, 'The headings use a different typeface.'),
        (6.0, 'And the voice and the music are one word each.'),
    ]),
    dict(scene='Method', beats=[
        (0.8, 'Equations are typeset to match.'),
        (4.0, 'And charts still come from numbers in the data folder, not traced by eye.'),
        (9.0, 'The music sits lower under the host than the default, because that is one setting too.'),
    ]),
    dict(scene='Takeaway', hold=3.0, beats=[
        (0.6, 'Take what you like, and leave the rest. The guide is in docs slash styles.'),
    ]),
]
