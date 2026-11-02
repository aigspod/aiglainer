"""Video 2 of 3, can the gap be explained away? Facts: Fig. 1, Table 4, Table 5, Table 7, §3 of arXiv:2609.35686v1.
Fig. 1 is redrawn from its vector paths; its Gemma 1% point doesn't match the text's 80.3/54.4, so that pair isn't quoted."""

VOICE = 'bella'
SAY = {'GPT-2': 'G P T two', 'ACDC': 'A C D C'}

SCENES = [
    dict(scene='Title', hold=0.8, beats=[
        (0.5, "Today's paper, Rethinking Circuit Evaluation, asks whether circuits explain a model's mistakes. This video asks whether the answer can be explained away."),
    ]),
    dict(scene='Piles', vend=27.5, beats=[
        (0.5, 'A circuit is a small part of a network that is supposed to explain how the whole network does a task. The paper scores it against the model, not against the right answer.'),
        (6.0, 'Take a thousand test sentences. The model gets fewer than one percent of them wrong.'),
        (11.0, 'Split them into two piles: the sentences the model gets right, and the ones it gets wrong.'),
        (16.5, "On the first pile, agreement means the circuit is right too. That's correct agreement."),
        (22.0, "On the second, it means the circuit makes the exact same mistake. That's error agreement."),
    ]),
    dict(scene='Gap', vend=13.5, beats=[
        (0.5, "Take a famous circuit in GPT-2 small, for what I'll call the name task: picking who receives something in a sentence."),
        (4.0, 'On the first pile, it agrees with the model ninety-nine point five percent of the time.'),
        (9.0, 'On the second pile, only fifteen percent. Whenever you see a gap like that, look for a boring explanation. The paper tests three.'),
    ]),
    dict(scene='Fig1', beats=[
        (0.5, 'Boring explanation one: errors are rare. If a method almost never sees a mistake, it never learns to make one.'),
        (6.0, 'So the authors test bigger models, on science questions and subtraction, where mistakes are common.'),
        (12.0, "Each panel goes from a tiny circuit to half the network. The solid line is agreement where the model is right. The dashed line is agreement where it's wrong."),
        (21.0, 'Take Gemma on the hard science questions. Thirty-eight percent of the examples used to find its circuit are its own mistakes.'),
        (28.0, 'Yet at every size shown, the dashed line stays below the solid one.'),
    ]),
    dict(scene='Reweight', beats=[
        (0.5, 'What if you weight the mistakes more heavily during the search?'),
        (5.0, 'On the name task, giving errors half the weight raises error agreement from about nine percent to thirty-seven.'),
        (11.0, 'But agreement on the right pile falls, from about ninety-nine to ninety-one.'),
        (16.5, 'Searching on equal numbers of errors and successes makes a similar trade. So rarity is part of the story, but not all of it.'),
    ]),
    dict(scene='CloseCalls', beats=[
        (0.5, 'The second boring explanation: mistakes are close calls.'),
        (4.0, 'When the model is wrong, the two answers often score almost the same. A near tie is easy to tip, so small differences between circuit and model flip the answer.'),
        (13.0, 'So the authors pair each mistake with a correct answer where the model was just as unsure.'),
        (19.0, 'For Llama on the hard science questions, agreement on the right pile falls from eighty percent to about forty-seven among these close calls. Error agreement stays near fifty-five.'),
        (29.0, 'Taken at face value, the gap reverses. The paper calls it narrowed.'),
        (33.0, 'But on the name task, every circuit keeps a positive gap after matching. The classic circuit: about ninety-five against fifteen.'),
    ]),
    dict(scene='Nudge', beats=[
        (0.5, 'Boring explanation three: the circuit is just a bit too sure of the right answer. So nudge it toward the wrong name.'),
        (8.0, "That works, in one sense. Shift the circuit's output toward the repeated name, and it reproduces at least as many errors as more elaborate fixes."),
        (16.0, 'You can even match how often the model is wrong.'),
        (20.0, "But that doesn't consistently recover which answers it gets wrong."),
        (26.5, "The rate of errors is not the identity of errors. That's the heart of this paper."),
    ]),
    dict(scene='Verdicts', beats=[
        (0.5, 'So, three excuses.'),
        (3.0, 'Rare errors explain part of the gap. Close calls explain part of it, in some settings. A nudge gets the error rate, but not the errors.'),
        (12.0, 'And for the name task in GPT-2, the gap survives all three.'),
    ]),
    dict(scene='Discussion', hold=2.0, beats=[
        (0.5, 'Two questions to bring to journal club.'),
        (3.0, 'Is exact error agreement the right test, when so many mistakes are near ties?'),
        (10.0, 'And which knockout would you trust: averages, other sentences, or learned constants?'),
    ]),
    dict(scene='End', hold=3.0, beats=[
        (0.5, 'The takeaway: matching how often a model is wrong is not the same as matching where.'),
        (7.0, 'See you at journal club.'),
    ]),
]
