"""Do circuits explain model errors? A 9:16 short (gap). Build with: make P=errors-short-gap"""
KIND = 'short'
SOURCES = ['errors-gap']
SCENE_MODULES = ['errshorts']
HUD = 'the aigs pod  ·  circuits & errors'
CITE = 'zhang, geng et al. · arxiv 2609.35686'
OUTPUT_NAME = 'circuit_errors_short_gap.mp4'
MUSIC = dict(style='analog')
DESCRIPTION = """A famous circuit inside GPT-2 agrees with the model 99.5% of the time when the model is right, and only 15% of the time when it is wrong. 📊

From "Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?" (Zhang, Geng et al., 2026), arXiv:2609.35686. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Michael"). Numbers from Table 1 (IOI, GPT-2 small, mean ablation).

#interpretability #machinelearning #AI #LLM #science #shorts
"""
