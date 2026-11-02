"""Video 1 of 3, the gap: what Bella says over each scene. Beats are (visual_time, text). Facts: Table 1, Table 2,
Table 8, Eq. 4, §2.1, §3 of arXiv:2609.35686v1."""

VOICE = 'bella'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='ColdOpen', smax=1.2, hold=0.4, beats=[
        (0.5, 'Sara and Courtney went to the hospital. Courtney gave a bone to... whom?'),
        (4.5, 'Sara, of course. But a small language model, GPT-2, sometimes says Courtney.'),
        (9.5, 'Now take the circuit that is supposed to explain how GPT-2 does this. On that same sentence, it says Sara.'),
        (15.0, 'The circuit is right, where the model is wrong. Is that a good explanation of the model?'),
    ]),
    dict(scene='Title', hold=1.0, beats=[
        (0.6, "Today's paper: Rethinking Circuit Evaluation. Do circuits explain model errors? Part one of three: the gap."),
    ]),
    dict(scene='Circuit', beats=[
        (0.5, 'A circuit is a small part of a network that is supposed to explain how the whole network does a task.'),
        (4.5, 'GPT-2 small has a hundred forty-four attention heads: twelve layers, twelve heads each. Each head decides which earlier words to look at.'),
        (11.0, 'For this task, called indirect object identification, a team mapped a circuit of twenty-six heads, by hand.'),
        (17.0, 'Some heads notice that a name is repeated.'),
        (21.0, "Inhibition heads use that to say: don't copy the repeated name."),
        (25.5, 'And name mover heads copy the other name into the answer.'),
    ]),
    dict(scene='Knockout', beats=[
        (0.5, 'To test a circuit, you keep its heads running, and knock out everything else.'),
        (5.0, "Knocking out means replacing a head's output with something uninformative. An average over many sentences. Its output on a different sentence. Or a learned constant."),
        (14.0, 'Then you check faithfulness. On average, does the circuit prefer the right name as strongly as the full model does?'),
        (21.0, 'For the classic circuit, with averages swapped in, the score is about zero point nine six. Very faithful.'),
        (26.0, 'But the model is right more than ninety-nine percent of the time. So that average is mostly an average over successes.'),
    ]),
    dict(scene='TwoPiles', beats=[
        (0.5, "The paper's idea is simple. Score the circuit against the model, not against the right answer."),
        (6.0, 'Here are a thousand test sentences. The model gets fewer than one percent of them wrong.'),
        (11.0, 'Split them into two piles. Sentences the model gets right, and sentences it gets wrong.'),
        (16.5, "On the first pile, agreement means the circuit is right too. That's correct agreement."),
        (22.0, "On the second pile, agreement means the circuit makes the exact same mistake. That's error agreement."),
        (28.0, 'Here there are only two possible answers. So if the circuit misses the mistake, it gives the right name instead.'),
    ]),
    dict(scene='Table1', beats=[
        (0.5, 'So how do the circuits do? Start with the classic circuit.'),
        (4.0, 'On the sentences the model gets right, it agrees ninety-nine point five percent of the time.'),
        (9.0, 'On the sentences the model gets wrong, it agrees only fifteen percent of the time.'),
        (14.0, 'Three automated circuits show the same pattern. Ninety-seven percent or more on the first pile, and at most forty-two on the second.'),
        (21.0, "Two even score above one on faithfulness. On average, they're more confident in the right name than the model itself."),
        (27.0, 'Swap in a different sentence instead of averages, and the gap narrows. But partly because agreement on the first pile drops.'),
    ]),
    dict(scene='Docstring', beats=[
        (0.5, 'A second task, from a tiny model that writes documentation for Python code, makes mistakes about a third of the time.'),
        (7.0, 'Its classic circuit still shows a gap: seventy-seven against thirty-six.'),
        (12.0, 'One automated circuit reproduces errors slightly more often than successes, though its faithfulness is only about zero point six five.'),
        (19.0, "And a small gap isn't always good news. Here it shrinks to eight points, mostly because the first pile collapsed."),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'If a circuit gets the right answer where the model got it wrong, what exactly has it explained?'),
        (10.0, 'And how much of this gap belongs to the knockout method, rather than the circuit itself?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.5, "The takeaway: a circuit can look faithful on average, and still miss most of the model's mistakes."),
        (7.0, 'Two companion videos ask whether the gap can be explained away, and what the circuit left out. See you at journal club.'),
    ]),
]
