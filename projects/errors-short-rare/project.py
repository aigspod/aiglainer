"""Do circuits explain model errors? A 9:16 short (rare). Build with: make P=errors-short-rare"""
KIND = 'short'
SOURCES = ['errors-gap', 'errors-excuses']
SCENE_MODULES = ['scenes2']
HUD = 'the aigs pod  ·  circuits & errors'
CITE = 'zhang, geng et al. · arxiv 2609.35686'
OUTPUT_NAME = 'circuit_errors_short_rare.mp4'
MUSIC = dict(style='daylight')
DESCRIPTION = """Do circuits miss a model's mistakes just because mistakes are rare? Not quite: even when 38% of the examples are mistakes, the gap stays. 📉

From "Rethinking Circuit Evaluation: Do Circuits Explain Model Errors?" (Zhang, Geng et al., 2026), arXiv:2609.35686. Full explainers and a podcast: the aigs pod.
Synthetic narration (Kokoro, "Michael"). Chart redrawn from the paper's Fig. 1 (vector data); 430 of 1,119 from Table 5.

#interpretability #machinelearning #AI #LLM #science #shorts
"""
