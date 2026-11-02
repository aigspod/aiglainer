"""Do circuits explain model errors? A 9:16 short (faithful). Build with: make P=errors/shorts/faithful"""
KIND = 'short'
SOURCES = ['errors/videos/gap']
SCENE_MODULES = ['errshorts']
HUD = 'the aigs pod  ·  circuits & errors'
CITE = 'zhang, geng et al. · arxiv 2609.35686'
OUTPUT_NAME = 'circuit_errors_short_faithful.mp4'
MUSIC = dict(style='encore')
DESCRIPTION = """One circuit scores 1.49 on faithfulness, where 1 means perfect: more sure of the right answer than the model it explains. It reproduces 11% of the model's mistakes. 🎯

From "Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?" (Zhang, Geng et al., 2026), arXiv:2609.35686. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Bella"). Numbers from Table 1 (IOI, edge pruning circuit, mean ablation).

#interpretability #machinelearning #AI #LLM #science #shorts
"""
