"""Do circuits explain model errors? The audio episode for journal club (Nov 4). Script in episode.py;
build with: make P=errors-pod"""
KIND = 'podcast'
TITLE = 'Do circuits explain model errors?'
OUTPUT_NAME = 'Circuit_Errors_pod.mp3'
SUMMARY = 'Rethinking Circuit Evaluation: Do Circuits Explain Model Errors? (Zhang, Geng et al., 2026), explained for the aigs pod journal club.'
BED = 0.1                   # faint music under the talk, 0..1 (0: talk on silence, the podcast norm)
MUSIC = dict(style='daylight')   # theme, outro and bed from the Richter-like strings (aiglainer/scores.py)

DESCRIPTION = """Do circuits explain model errors? An audio episode for the aigs pod journal club.

A circuit is a small piece of a neural network that is supposed to explain how the whole network does a task. The
usual test asks whether the circuit still does the task. This paper asks a different question: when the model gets
an answer wrong, does the circuit get it wrong in the same way? Mostly, it doesn't. On indirect object
identification in GPT-2 small, under mean ablation, the circuits tested agree with the model on 97 to 99.5 percent of the prompts it gets
right, but on only 11 to 42 percent of the ones it gets wrong. We walk through the measurement, the attempts to close
the gap, a case study that adds 63 head positions to the classic circuit and recovers most of the missing errors,
and the two omitted computations that make the wrong name win. Then we ask what a circuit is an explanation of.

Paper: Li Zhang, Chuqin Geng, Mark Zhang, Chen Yang, Luke Zhang, Haolin Ye, Xujie Si (2026). Rethinking Circuit
Evaluation: Do Circuits Explain Model Errors? Preprint. arXiv:2609.35686

Chapters
{chapters}

Questions to discuss
1. If a circuit gets the right answer where the model got it wrong, is it a worse explanation, or a better
   description of the task? What is a circuit an explanation of?
2. The case-study extension was searched for with the model's errors in its objective. What would convince you it
   found mechanism rather than a fit?
3. How much of the gap is the ablation rather than the circuit? Which replacement values would you trust?
4. What would this test look like for a machine-learned climate emulator and its known biases?
5. (Not on air.) Is exact error agreement the right test, given how close to a tie many errors are?

Notes
• IOI has only two candidate answers, so a circuit that misses one of the model's errors gives the correct answer.
• The 0.41-point drop in correct agreement is on the 26,000-prompt test set; on a fresh 5,200-prompt check the drop
  was 0.85 points, beyond the search's own 0.5-point tolerance (Table 4).
• The §3 scalar subject-logit shifts were calibrated on evaluation correct cases (Table 4); the case-study subject-bias
  control was fitted on validation correct cases (§4.2).
• The climate-emulator passage is our extrapolation, not a result of the paper.
{voice}• An unofficial summary, not produced by the authors.
"""
