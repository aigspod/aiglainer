"""LAWFUL (Chen, Parker & Arora, ICML 2026 MI workshop): settings for this video. See aiglainer/template/project.py."""
from margin_notes import NOTES

HUD = 'the aigs pod  ·  /mull/  ·  lawful'
OUTPUT_NAME = 'LAWFUL_journal_club.mp4'

CHAPTERS = ['The question', 'The testbed', 'The framework', 'Counterfactuals', 'Circuits', 'Results', 'Mechanism', 'Limits & discussion']

# The story spine shown in the tracker (see the Roadmap scene): which chapters serve which step.
STEPS = ['behavior', 'cause', 'mechanism']
CHAPTER_STEPS = {2: (0,), 3: (0,), 4: (1,), 5: (0, 1), 6: (2,)}

SCENE_MODULES = ['scenes1', 'scenes2', 'scenes3', 'scenes4']

def FULL_CUT():
    import scenes
    return scenes.build()

MUSIC = dict(intro_until='Title', arp_from='Framework', arp_until='Discussion')

CHAPTER_TITLES = {
    'ColdOpen': 'Cold open: did it learn the physics?', 'Title': 'LAWFUL', 'Question': 'The question: accurate ≠ lawful',
    'Gaps': 'Four interpretability gaps', 'Testbed': 'The testbed: MoCap-to-Radar', 'Doppler': 'The Doppler law f = 2v/λ',
    'Framework': 'The LAWFUL framework', 'Instantiation': 'Instantiation for Doppler',
    'Counterfactual': 'Counterfactual bodies (radial scaling)', 'Score': 'Same slope, same physics: the consistency score',
    'Domain': 'Domain of validity and M₀ = 0.988', 'Patching': 'Activation patching: sufficiency & necessity',
    'Search': 'Greedy circuit search over τ (Table 1)', 'Spectrograms': 'Counterfactual spectrograms (Fig. 3)',
    'Fig4a': 'Radial scaling over the domain (Fig. 4a)', 'Fig4b': 'Tangential invariance test (Fig. 4b)',
    'Probes': 'Where velocity appears: linear probes', 'QKVal': 'Pattern, not payload: QK vs VAL',
    'Heatmaps': 'Two heads, two ends of the window', 'Limits': 'Limitations', 'Discussion': 'Questions to think about before we meet',
    'End': 'Takeaway & citation', 'MechInterp': 'Mechanistic interpretability, briefly',
    'ProbeVsPatch': 'Two tools: probes (read) and patching (write)', 'Roadmap': 'The plan: behavior, cause, mechanism',
}

DESCRIPTION = """LAWFUL: Law-Aligned Witness for Faithful Use of Latents, a motion-graphics explainer for journal club.

When a neural network predicts a physical system accurately, has it learned the governing law, does its internal computation actually use it, and does that hold across the law's domain of validity? This video walks through LAWFUL, a framework that aligns a learned model with an explicit physics law, scores their agreement over continuous counterfactual perturbations, and finds "physically consistent circuits" by activation patching. The case study: a MoCap-to-Radar transformer and the Doppler law f = 2v/λ.

Paper: Kevin Chen, Kenneth W. Parker, Anish Arora (2026). LAWFUL: Law-Aligned Witness for Faithful Use of Latents. Mechanistic Interpretability Workshop, ICML 2026. arXiv:2607.28672
Code: https://github.com/aciculachen/LAWFUL

Chapters
{chapters}

Notes
• Charts (Fig. 3, 4a, 4b, 5 and Tables 1–2) are redrawn from data extracted from the paper's figures and tables.
• The walking figure, radar, top-down trajectory and attention-head diagrams are illustrations, not paper data.
• The paper's text says "six of the seven temporal heads" are more QK-sufficient; its Table 2 values give 5 of 6 temporal heads in C† (T.h4 is the exception), and S.h4 also favors VAL. The video follows the table.
{voice}• This is an unofficial explainer, not produced by the authors.
"""


def THUMBNAIL(c):
    from thumbnail import draw
    draw(c)
