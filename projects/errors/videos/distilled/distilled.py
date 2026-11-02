"""The ~6-minute distilled cut: the best scene of each act from the three part videos, renumbered, with its own
title, questions and ending. Scenes come from errors/videos/gap (scenes), errors/videos/excuses (scenes2), errors/videos/wrongname (scenes3)."""
from errkit import *
import scenes as P1, scenes2 as P2, scenes3 as P3

def _sub(cls, chapter, num):
    return type(cls.__name__, (cls,), dict(chapter=chapter, NUM=num))

ColdOpen = P1.ColdOpen
Circuit = _sub(P1.Circuit, 0, '01')
Knockout = _sub(P1.Knockout, 0, '01')
TwoPiles = _sub(P1.TwoPiles, 0, '01')
Table1 = _sub(P1.Table1, 1, '02')
Fig1 = _sub(P2.Fig1, 2, '03')
CloseCalls = _sub(P2.CloseCalls, 2, '03')
Nudge = _sub(P2.Nudge, 2, '03')
Result = _sub(P3.Result, 3, '04')
PathOne = _sub(P3.PathOne, 3, '04')
PathTwo = _sub(P3.PathTwo, 3, '04')

class Title(TitleCard):
    STICKY = ['the whole paper', 'in six minutes']

class Discussion(Scene):
    dur = 22.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (9.0, 'chime'), (15.0, 'chime')]

    def draw(self, c, t):
        header(c, t, '05', 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('When a circuit is {y:right} where the model is {r:wrong}, what has it explained?', 3.0),
                              ('How much of the gap belongs to the {y:knock-out}, rather than the circuit?', 9.0),
                              ('What would this test look like for a {y:climate emulator} and its known biases?', 15.0)],
                       y0=320, dy=200, h=170, size=34)

class End(EndCard):
    TAKE = 'Explaining how a model {f:succeeds} isn’t explaining how it {r:fails}. Test circuits on the {y:mistakes}, too.'
    STATS = [('99.5% vs 15.2%', 'classic circuit: right pile vs wrong pile', 'c'), ('14 → 75%', 'mistakes reproduced, 63 extra pieces', 'y'),
             ('120 & 35 / 137', 'mistakes traced through two paths', 'f')]
    NEXT = 'the longer versions: three part videos and a 23-minute podcast'
