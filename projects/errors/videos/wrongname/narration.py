"""Video 3 of 3, how the wrong name wins. Facts: §4.2, §4.3, Fig. 2, Table 4, §5, App. D of arXiv:2609.35686v1.
Fig. 2's attention percentages are for its two example prompts only, and are said as such."""

VOICE = 'bella'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='ColdOpen', smax=1.2, hold=0.4, beats=[
        (0.5, 'Sara and Courtney went to the hospital. Courtney gave a bone to... whom?'),
        (4.5, 'Sara, of course. But a small language model, GPT-2, sometimes says Courtney.'),
        (9.5, 'Now take the circuit that is supposed to explain how GPT-2 does this. On that same sentence, it says Sara.'),
        (15.0, 'The circuit is right, where the model is wrong. So what did it leave out?'),
    ]),
    dict(scene='Title', hold=0.8, beats=[
        (0.5, "Today's paper: Rethinking Circuit Evaluation. This video goes inside GPT-2, to find how the wrong name wins."),
    ]),
    dict(scene='Circuit', beats=[
        (0.5, 'A circuit is a small part of a network that is supposed to explain how the whole network does a task.'),
        (11.0, 'For this name task, a team mapped a circuit of twenty-six attention heads in GPT-2 small, by hand.'),
        (17.0, 'Some heads notice that a name is repeated.'),
        (21.0, "Inhibition heads use that to say: don't copy the repeated name."),
        (25.5, 'And name mover heads copy the other name into the answer.'),
    ]),
    dict(scene='Gap', vend=13.5, beats=[
        (0.5, 'Now score that classic circuit against the model, separately where the model is right and where it is wrong.'),
        (4.0, 'Where the model is right, the circuit agrees ninety-nine point five percent of the time.'),
        (9.0, 'Where the model is wrong, it makes the same mistake only fifteen percent of the time.'),
    ]),
    dict(scene='Search', beats=[
        (0.5, 'So what did it leave out? The authors search for additions. One addition is one attention head, at one position in the sentence.'),
        (6.0, 'A hundred forty-four heads, at up to twenty-five positions. Thousands of candidates.'),
        (12.0, "The search adds a few at a time. It rewards reproducing the model's mistakes, allows at most half a point lost on the right pile, and penalizes size."),
        (22.0, 'It settles on sixty-three of them.'),
    ]),
    dict(scene='Result', beats=[
        (0.5, 'Then the extension is frozen, and tested on twenty-six thousand fresh sentences.'),
        (6.0, "The classic circuit reproduces about fourteen percent of the model's mistakes. The extended circuit: about seventy-five."),
        (13.0, 'Agreement on the right pile barely moves, from ninety-nine point three to ninety-eight point nine percent.'),
        (19.0, 'A blanket nudge reaches about twenty percent. Random additions of the same size, seventeen to forty-one.'),
        (26.0, 'So these particular additions recover particular mistakes. One caveat: on a second fresh check, the right pile dropped a little more than the search allowed.'),
    ]),
    dict(scene='PathOne', beats=[
        (0.5, 'Then they trace what the additions do. They find two paths. The first goes through the inhibition heads.'),
        (5.0, 'Recall their job: look at the repeated name, and tell the name movers not to copy it.'),
        (10.0, "Added heads bring in context, including the object, the bone. In the paper's example, one inhibition head looks at the repeated name far less: from about seventy-nine percent of its attention, to about twenty-eight."),
        (20.0, 'Then a name mover looks at Courtney more, and copies the wrong name.'),
        (25.0, 'Patch just that change into the classic circuit, and it makes the mistake on a hundred twenty of the hundred thirty-seven sentences.'),
        (33.0, "Swap the bone for a snack, and the right answer comes back on a hundred seven. What about the object matters, the paper can't yet say."),
    ]),
    dict(scene='PathTwo', beats=[
        (0.5, 'The second path starts in the very first layer.'),
        (4.0, 'Five first-layer heads write at the correct name, Katie. The classic circuit leaves those outputs out.'),
        (10.0, 'They change how Katie looks to the name movers. In this example, the head that copies names looks at Katie a little less.'),
        (14.0, 'And the head that pushes names down looks at her a little more.'),
        (20.0, 'Both favor Vanessa, the wrong name.'),
        (24.0, 'Patch in just those changes at Katie, and the classic circuit makes the mistake on thirty-five of the hundred thirty-seven. Anywhere else, on none.'),
    ]),
    dict(scene='Meaning', beats=[
        (0.5, "So what should circuit studies do differently? The paper's answer is cheap."),
        (4.5, 'Split the sentences by whether the model is right. Report agreement on both piles, with their sizes. On the wrong pile, count only the same wrong answer. And check several circuit sizes.'),
        (15.0, 'Passing that test is necessary, not sufficient. A circuit could copy every answer, for the wrong internal reasons.'),
        (22.0, "And our own extrapolation: the same split could test explanations of climate emulators. Do they reproduce the emulator's known biases, or only its skill?"),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'The extension was found with the mistakes in its objective. What would convince you it found mechanism, and not a fit?'),
        (11.0, 'And what would this test look like for an emulator and its biases?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.5, "The takeaway: explaining how a model succeeds isn't explaining how it fails."),
        (6.0, 'See you on Wednesday, at journal club.'),
    ]),
]
