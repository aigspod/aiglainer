"""Do circuits explain model errors? A 9:16 short (bone). Build with: make P=errors/shorts/bone"""
KIND = 'short'
SOURCES = ['errors/videos/gap', 'errors/videos/wrongname']
SCENE_MODULES = ['boneshort', 'scenes3']
HUD = 'the aigs pod  ·  circuits & errors'
CITE = 'zhang, geng et al. · arxiv 2609.35686'
OUTPUT_NAME = 'circuit_errors_short_bone.mp4'
MUSIC = dict(style='mysterium')
DESCRIPTION = """Why does GPT-2 sometimes give the bone to the wrong person? Part of the answer is the bone. 🦴🐕

From "Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?" (Zhang, Geng et al., 2026), arXiv:2609.35686. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Bella"). Diagram redrawn from Fig. 2A (one example sentence); 120/137 and 107/137 from §4.3.

#interpretability #machinelearning #AI #LLM #science #shorts
"""
