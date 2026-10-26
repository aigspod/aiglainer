from scenes1 import ColdOpen, Title, Question, Gaps, Testbed, Doppler
from scenes2 import Framework, Instantiation, Counterfactual, Score, Domain
from scenes4 import MechInterp, ProbeVsPatch, Roadmap
from scenes3 import Patching, Search, Spectrograms, Fig4a, Fig4b, Probes, QKVal, Heatmaps, Limits, Discussion, End

def build():
    return [ColdOpen(), Title(), Question(), Gaps(), Testbed(), Doppler(),
            Framework(), Instantiation(), Counterfactual(), Score(), Domain(),
            Patching(), Search(), Spectrograms(), Fig4a(), Fig4b(),
            Probes(), QKVal(), Heatmaps(), Limits(), Discussion(), End()]
