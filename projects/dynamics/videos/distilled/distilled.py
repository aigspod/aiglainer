"""The ~6-minute distilled cut: the key scenes of the three part videos, renumbered, with its own title, questions and
ending. Scenes come from dynamics/videos/sign, dynamics/videos/hidden and dynamics/videos/unfold.

All three parts name their scene module `scenes.py`, so a plain `import scenes` would only ever find the first one on
sys.path. Each is loaded here from its own file under a distinct module name instead (they import only dynkit, which
lives in sign/ and is on sys.path through SOURCES). Classes are subclassed, never copied: a change to a part's scene
changes this cut too.

tex/: hidden and unfold both have a tex/takens.png (different formulas). SOURCES lists hidden before unfold, so the
key resolves to hidden's, which is the one hidden.Takens needs; unfold.Latent (the other user) is not in this cut."""
import importlib.util, os, sys
from dynkit import *

_VIDEOS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _load(part):
    name = f'_dynamics_{part}_scenes'
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, os.path.join(_VIDEOS, part, 'scenes.py'))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod

S, H, U = _load('sign'), _load('hidden'), _load('unfold')

def _sub(cls, chapter, num, **kw):
    return type(cls.__name__, (cls,), dict(chapter=chapter, NUM=num, **kw))

# 0 · the sign problem (sign)
ColdOpen = U.ColdOpen
Recipe = _sub(S.Recipe, 0, '01')
OneHead = _sub(S.OneHead, 0, '01')
Springs = _sub(S.Springs, 0, '01')
TwoHeads = _sub(S.TwoHeads, 0, '01')
# 1 · history stands in for a sensor (sign, hidden)
TwoMasses = _sub(S.TwoMasses, 1, '02')
Hide = _sub(H.Hide, 1, '02')
Takens = _sub(H.Takens, 1, '02')
# 2 · room and parameters (unfold)
Room = _sub(U.Room, 2, '03')
Loops = _sub(U.Loops, 2, '03')
Recon = _sub(U.Recon, 2, '03')
Lesson = _sub(U.Lesson, 2, '03')
# 3 · our extrapolation (unfold)
Emulators = _sub(U.Emulators, 3, '04')


class Table1(H.Table1):
    """hidden.Table1 plus the text-vs-table note on positional encoding (projects/dynamics/AGENTS.md accuracy notes):
    this cut drops hidden.Attention, where the part video makes that point."""
    chapter = 1
    NUM = '02'
    dur = 39.0

    def draw(self, c, t):
        super().draw(c, t)
        k = ramp(t, 34.0, 0.6)
        if k > 0:
            rich(c, 'the paper’s text (§4.1) says PE gives {c:no systematic gain}; Table 1 and §5.2 {y:disagree}, and we follow the table',
                 120, 985, 19, 1400, t, 34.2, 0.02, 0.4, base='muted')


class Title(TitleCard):
    TITLE = 'Inside a *forecasting* transformer'
    STICKY = ['the whole paper', 'in six minutes']


class Discussion(Scene):
    dur = 22.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (9.0, 'chime'), (15.0, 'chime')]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('In a model with {y:many heads}, how would you check that it kept the {y:resonance}, rather than averaging it away?', 3.0),
                              ('If attention just {y:averages the window}, where is the state rebuilt: in attention, or the {g:network} after it?', 9.0),
                              ('In a {y:climate emulator}, what plays the {y:missing Reynolds number}, and how would we notice?', 15.0)],
                       y0=320, dy=200, h=170, size=34)
        extrap_label(c, W - MX - 36, 320 + 2 * 200 + 156, ramp(t, 15.3, 0.6), 18, 'right')


class End(EndCard):
    TAKE = 'Attention {y:averages}, {g:history} can stand in for a hidden state, and a good forecast doesn’t prove a sound {c:inside}.'
    STATS = [('same sign', 'one head’s two coefficients (§2.3, §3.1)', 'y'),
             ('≈ 1200×', 'MLP error ÷ best transformer, x only (Table 1)', 'g'),
             ('≈ 70×', 'worse field rebuild without Re (App. A.5)', 'c')]
    NEXT = 'one-step accuracy is not latent identifiability  ·  journal club, nov 11'
