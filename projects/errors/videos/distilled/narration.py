"""The distilled cut, voiced by Michael. Facts: Table 1, Table 5, Table 7, Table 8, Fig. 1, Fig. 2A, §3, §4.2, §4.3 of
arXiv:2609.35686v1. "Extra pieces" = the 63 head-position additions (said this way: Whisper hears "additions" as "editions")."""

VOICE = 'michael'
SAY = {'GPT-2': 'G P T two'}

SCENES = [
    dict(scene='ColdOpen', smax=1.2, hold=0.4, beats=[
        (0.5, 'Sara and Courtney went to the hospital. Courtney gave a bone to... whom?'),
        (4.5, 'Sara, of course. But a small language model, GPT-2, sometimes says Courtney.'),
        (9.5, 'Now take the circuit that is supposed to explain how GPT-2 does this. On that same sentence, it says Sara.'),
        (15.0, 'The circuit is right, where the model is wrong. Is that a good explanation of the model?'),
    ]),
    dict(scene='Title', hold=0.8, beats=[
        (0.6, 'This is Rethinking Circuit Evaluation, a new preprint from Toronto, McGill, and Tsinghua. The whole paper, in about six minutes.'),
    ]),
    dict(scene='Circuit', beats=[
        (0.5, 'A circuit is a small part of a network that is supposed to explain how the whole network does a task.'),
        (11.0, 'For this name task, researchers mapped twenty-six attention heads in GPT-2 small, by hand.'),
        (17.0, 'Some heads notice the repeated name.'),
        (21.0, "Inhibition heads say: don't copy it."),
        (25.5, 'And name movers copy the other name into the answer.'),
    ]),
    dict(scene='Knockout', vend=25.5, beats=[
        (0.5, 'To test a circuit, you keep its heads running, and knock out everything else.'),
        (5.0, "Knocking out means swapping a head's output for something uninformative: an average over many sentences, its output on a different sentence, or a learned constant."),
        (14.0, 'Then you check faithfulness. On average, does the circuit prefer the right name as strongly as the full model?'),
        (21.0, 'For this circuit, the score is about zero point nine six. By the usual standard, very faithful.'),
    ]),
    dict(scene='TwoPiles', vend=27.5, beats=[
        (0.5, 'But the model is right more than ninety-nine percent of the time, so that average is mostly about successes. This paper asks something sharper.'),
        (11.0, 'Split the test sentences into two piles: the ones the model gets right, and the ones it gets wrong.'),
        (16.5, 'On the first pile, does the circuit agree with the model?'),
        (22.0, 'On the second, does it make the exact same mistake?'),
    ]),
    dict(scene='Table1', beats=[
        (0.5, 'For the classic circuit, the answer is lopsided.'),
        (4.0, 'Where the model is right, it agrees ninety-nine point five percent of the time.'),
        (9.0, 'Where the model is wrong, only fifteen percent.'),
        (14.0, 'Automated circuit-finding methods show the same pattern, even though they were trained to match the model, mistakes included.'),
        (21.0, 'Two even look better than perfect: on average, more confident in the right name than the model itself.'),
        (27.0, 'And the knockout method matters. Swap averages for other sentences, and the gap narrows, partly because the first pile drops.'),
    ]),
    dict(scene='Fig1', beats=[
        (0.5, 'Can the gap be explained away? Maybe mistakes are just rare, so circuit-finding never learns them.'),
        (12.0, 'But with bigger models, on science questions and subtraction, mistakes are common.'),
        (21.0, 'For Gemma, thirty-eight percent of the examples used to find its circuit are its own mistakes. The dashed line still sits below the solid one.'),
    ]),
    dict(scene='CloseCalls', beats=[
        (0.5, 'Or maybe mistakes are close calls.'),
        (4.0, 'When the model is wrong, the two answers often score almost the same, so a tiny difference between circuit and model tips the answer.'),
        (13.0, 'So the authors pair each mistake with a correct answer where the model was just as unsure.'),
        (19.0, 'For Llama on the hard science questions, the gap disappears, and by the numbers even reverses.'),
        (33.0, 'But on the name task, every circuit keeps its gap. The classic circuit: about ninety-five against fifteen.'),
    ]),
    dict(scene='Nudge', beats=[
        (0.5, 'Or maybe the circuit is just a little too sure of the right answer.'),
        (8.0, 'Nudge it toward the wrong name, and you can match how often the model is wrong.'),
        (20.0, 'But not which sentences it gets wrong. The rate of errors is not the identity of errors.'),
    ]),
    dict(scene='Result', beats=[
        (0.5, 'So what did the classic circuit leave out? A search over thousands of heads and positions settles on sixty-three extra pieces.'),
        (6.0, 'On fresh sentences, the share of mistakes reproduced jumps from about fourteen percent to about seventy-five.'),
        (13.0, 'Agreement on the right pile barely moves.'),
        (19.0, 'A blanket nudge, and random extras of the same size, do far worse.'),
        (26.0, 'One caveat: on a second fresh check, the right pile dropped a little more than the search allowed.'),
    ]),
    dict(scene='PathOne', beats=[
        (0.5, 'Tracing the extras shows how the wrong name wins.'),
        (10.0, "Context from the object, the bone, changes where an inhibition head looks. In the paper's example, it looks at the repeated name far less."),
        (20.0, 'So a name mover looks at Courtney more, and copies the wrong name.'),
        (25.0, 'Patch just that change into the classic circuit, and it makes the mistake on a hundred twenty of the hundred thirty-seven sentences.'),
        (33.0, 'Swap the bone for a snack, and the right answer comes back on a hundred seven.'),
    ]),
    dict(scene='PathTwo', beats=[
        (0.5, 'A second path starts in the very first layer.'),
        (4.0, 'Five first-layer heads write at the correct name, Katie, and the classic circuit leaves those outputs out.'),
        (10.0, 'They change how Katie looks to the name movers. The head that copies names finds her a little less.'),
        (14.0, 'And the head that pushes names down finds her a little more. Both favor Vanessa, the wrong name.'),
        (24.0, 'Patch in just that change, and the classic circuit makes the mistake on thirty-five of the hundred thirty-seven. The two paths overlap.'),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Three questions for journal club.'),
        (3.0, 'When a circuit is right where the model is wrong, what has it explained?'),
        (9.0, 'How much of the gap belongs to the knockout, rather than the circuit?'),
        (15.0, 'And what would this test look like for a climate emulator and its known biases?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.5, "The takeaway: explaining how a model succeeds isn't explaining how it fails. Test circuits on the mistakes, too."),
        (8.0, 'See you at journal club.'),
    ]),
]
