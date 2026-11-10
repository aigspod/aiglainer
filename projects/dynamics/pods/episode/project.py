"""What does attention do with a dynamical system? The audio episode for journal club (Nov 11). Script in episode.py;
build with: make P=dynamics/pods/episode"""
KIND = 'podcast'
TITLE = 'What does attention do with a dynamical system?'
OUTPUT_NAME = 'Dynamics_pod.mp3'
SUMMARY = 'A Mechanistic Analysis of Transformers for Dynamical Systems (Duthé, Evangelou, Liu, Kevrekidis, Chatzi), explained for the aigs pod journal club.'
BED = 0.1                   # faint music under the talk, 0..1 (0: talk on silence, the podcast norm)
MUSIC = dict(style='silencia', duck_db=16)   # theme, outro and bed (aiglainer/scores.py); music well under the host

DESCRIPTION = """What does attention do with a dynamical system? An audio episode for the aigs pod journal club.

This paper takes the smallest transformer, one layer and mostly one attention head, and reads it with classical
dynamical-systems theory. For linear systems, attention is an autoregressive model whose lag weights come from
softmax: positive and summing to one, times a single output layer. So one head cannot make weights of opposite
sign, and a damped spring that needs them gets smoothed out; two heads fix it. For nonlinear systems, attention
works like an adaptive delay embedding, in the spirit of Takens' theorem: it helps when part of the state is hidden
(Van der Pol), but the model also needs enough internal room to unfold what it rebuilds (Chafee-Infante), and it may
need to be told the parameter that separates one regime from another (flow past a cylinder). The key line: predicting
the next step well is not the same as having an internal state you can rebuild the physics from. We end with what
this might mean for machine-learned climate emulators.

Paper: Gregory Duthé, Nikolaos Evangelou, Wei Liu, Ioannis G. Kevrekidis, Eleni Chatzi (2025). A Mechanistic
Analysis of Transformers for Dynamical Systems. Preprint, v2 2026. arXiv:2512.21113

Chapters
{chapters}

Questions to discuss
1. If a second head fixes the sign problem, what is the single-head result really teaching us? A limit of
   transformers, or a way to read what each part of one does?
2. Picture two models that predict the next step equally well, but only one has an internal state you could rebuild
   the physics from. How would you even notice the difference?
3. Which hidden variables, or forcings, should an emulator be told explicitly, and which should it be left to infer
   from history?

Notes
• Two-mass system: the paper reports modal frequencies of about 4.1 and 9.5 Hz; from the parameters it lists
  (m1 = m2 = 1, k1 = 1000, k2 = 1500) we get about 3.26 and 9.52 Hz.
• Positional encoding, Van der Pol: the §4.1 text says it does not systematically improve accuracy, but Table 1
  shows the two-dimensional model with it at about 86 times lower error (2.065e-5 against 1.770e-3), and §5.2 says
  it helps. The best transformer (2.065e-5) is about 1,200 times better than the MLP alone (2.485e-2).
• The paper says its experiments "confirm" Takens' bound; we read them as consistent with it.
• The emulator passages are our extrapolation, not results of the paper.
{voice}• An unofficial summary, not produced by the authors.
"""
