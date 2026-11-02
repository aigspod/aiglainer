"""Do circuits explain model errors? The full episode (~24 min) for journal club on Nov 4, after LAWFUL (Oct 28).
Every claim traces to the paper (arXiv:2609.35686v1): §2.2 Eq. 1-4 agreement; §2.3 benchmarks; Table 1 (IOI and
Docstring, mean / resample / optimal ablation); Table 2 (IOI error census, 884 of 100,000); §3 and Fig. 1 (MIB);
§3 and Table 4 (recovery attempts); App. C and Table 7 (margin matching); §4.2 and App. D (the 63-rule extension);
§4.3 and Fig. 2 (the two omitted computations); §5 (recommendations); §7 (limitations).
Reviewed twice before synthesis: claims against the paper, and tone/clarity for the ear.
Text says GPT-2, IOI, ACDC as written (that's what Whisper writes back); SAY tells Kokoro how to say them.
The climate-emulator passage is labelled on air as our extrapolation.

A role ending in '?' ('H?') marks a question for the room. ('~', 'chime') plays the soft cue that announces one.
"""

HOSTS = {'H': 'bella'}       # role -> host in aiglainer/hosts.py

SAY = {
    'GPT-2': 'G P T two',
    'IOI': 'I O I',
    'ACDC': 'A C D C',
}

SEGMENTS = [
    # ---------------------------------------------------------------- cold open: a right answer that is wrong (Fig. 2A, App. D.1)
    dict(title='Cold open', music=None, lines=[
        ('H', 'Here\'s a sentence. "Sara and Courtney went to the hospital. Courtney gave a bone to..."'),
        ('H', 'To whom? Sara, of course. Courtney is the one doing the giving.', 0.4),
        ('H', 'A small language model, GPT-2, usually gets this kind of sentence right. But sometimes it says Courtney.', 0.5),
        ('H', 'Now, researchers found a circuit in GPT-2 for this task. A small set of parts inside the network that is supposed to explain how it picks the name.'),
        ('H', 'Run that circuit on the sentences where the model says the wrong name, and most of the time, the circuit says the right one.'),
        ('H', 'The circuit is right where the model is wrong.', 0.6),
        ('H', 'Is that a good explanation of the model?'),
        ('H', "Today's paper says no. And it shows how often this happens, why, and what was missing."),
    ]),
    dict(title='Welcome', music='theme', lines=[
        ('H', "Welcome to the aigs pod. I'm {H}, and this is our warm-up for journal club."),
        ('H', 'As usual, the voice is synthetic. The paper, the numbers, and the arguments are real.'),
        ('H', "Today's paper is called Rethinking Circuit Evaluation. The subtitle asks: do circuits explain model errors?"),
        ('H', "It's a new preprint from a team at Toronto, McGill, and Tsinghua University."),
        ('H', "It continues our circuits series. Last week, with Lawful, we asked whether a small set of parts inside a network could carry a physical law. We checked those parts on what the model gets right."),
        ('H', "This week's question is the other half. What about what the model gets wrong?"),
        ('H', "Here's the plan. Part one: what a circuit is, and how people usually test one. Part two: the paper's new test, and the headline numbers. Part three: can the gap be explained away? Part four: a case study that goes looking for the missing pieces, and finds two of them. And finally, what I think it all means."),
        ('H', "And now and then, you'll hear a little chime.", 0.5),
        ('~', 'chime'),
        ('H', "That's a question for the room. Something to bring to the meeting on Wednesday. No need to pause. Just hold onto it."),
    ]),

    # ---------------------------------------------------------------- 1. circuits, IOI, ablation, faithfulness (§1, §2.1, §2.3, Table 8)
    dict(title='What a circuit is, and how we test one', music='sting', lines=[
        ('H', "Part one. Let's start with the basics."),
        ('H', 'Mechanistic interpretability tries to explain a neural network by reverse engineering it. Not just what it outputs, but the steps inside that produce the output.'),
        ('H', 'One popular kind of explanation is a circuit. You pick a task. Then you find the smallest set of parts that seems to do it.'),
        ('H', 'The parts are usually attention heads: small units that each decide which earlier words to look at. The circuit also records which parts pass information to which. Those connections are called edges.'),
        ('H', 'And then you say: this is how the model does it.'),
        ('H', "The most famous example is the one from our cold open. It's called indirect object identification. IOI, for short."),
        ('H', 'The sentence has two names. One of them, the subject, appears twice. The right answer is the other name, the one that appears only once. That\'s the indirect object.'),
        ('H', 'A few years ago, Kevin Wang and colleagues mapped a circuit for this in GPT-2 small, by hand. Twenty-six attention heads, at specific positions in the sentence. I\'ll call it the classic circuit.'),
        ('H', "Roughly, here's the story they told. Some heads notice that a name is repeated. Other heads, called inhibition heads, use that to say: don't copy the repeated name."),
        ('H', "And finally, name mover heads look back at the names, and copy the one that wasn't inhibited into the answer."),
        ('H', "Since then, people have built automated methods that find circuits without the detective work. This paper tests three of them. You don't need their names. They all search for a small piece of the network that behaves like the whole thing."),
        ('H', 'So how do you test a circuit?', 0.5),
        ('H', "You keep the circuit's parts running normally. And you knock out everything else."),
        ('H', 'Knocking out a part means replacing its output with something uninformative. This is called ablation, and there are a few ways to do it.'),
        ('H', 'Mean ablation replaces the output with its average over many sentences. Resample ablation replaces it with its output on a different sentence, one with three unrelated names. The paper also tries a third kind, with learned replacement values.'),
        ('H', "Then you measure what's called faithfulness: how well the stripped-down circuit preserves the full model's behavior."),
        ('H', "Usually, that's an average. Take the score the model gives the right name, minus the score for the wrong name. Average it over many sentences. If the circuit's average is close to the full model's, the circuit is called faithful."),
        ('H', "And here's the catch.", 0.5),
        ('H', 'An average over a task where the model is right ninety-nine percent of the time is mostly an average over successes.'),
    ]),

    # ---------------------------------------------------------------- 2. the new test (§2.2 Eq. 1-4)
    dict(title='Score the circuit against the model, not the truth', music=None, lines=[
        ('H', "Part two. The paper's key move is simple."),
        ('H', "Don't ask whether the circuit gets the right answer. Ask whether it gives the same answer as the model."),
        ('H', 'Then split the sentences into two piles. Pile one: the ones the full model gets right. Pile two: the ones the full model gets wrong.'),
        ('H', "On the first pile, agreement means the circuit is also right. The authors call this correct agreement."),
        ('H', 'On the second pile, agreement means the circuit makes the same mistake. Not just any mistake. The exact same wrong answer. They call this error agreement.'),
        ('H', 'Correct agreement, minus error agreement. That\'s the gap.'),
        ('H', "Why should we care about the second pile? Because a circuit is meant to be an explanation of the model's behavior. And the model's behavior includes its mistakes."),
        ('H', "If your explanation removes the mistake, it can't tell you why the mistake happened. And that's often exactly what we want to know, when we're debugging a model."),
        ('H', "One detail is worth holding onto. In the IOI task, there are only two candidate answers: the indirect object, and the subject. So if the circuit doesn't reproduce the model's mistake, it must give the right answer instead."),
    ]),

    # ---------------------------------------------------------------- 3. the headline numbers (Table 1, Table 2, §3)
    dict(title='The headline numbers', music='sting', lines=[
        ('H', "So, how do the circuits do?"),
        ('H', 'First, some context. On this task, the model is wrong less than one percent of the time.'),
        ('H', 'Take the classic circuit, under mean ablation. Its faithfulness score is about zero point nine six. A score of one would mean it preserves the full model\'s average behavior perfectly. By the usual standard, that\'s a very good circuit.'),
        ('H', 'On the sentences the model gets right, it agrees with the model ninety-nine point five percent of the time.'),
        ('H', 'On the sentences the model gets wrong, it agrees only fifteen percent of the time.', 0.6),
        ('H', "Ninety-nine point five percent, against fifteen."),
        ('H', "And it isn't just the classic circuit. Under mean ablation, the four circuits tested on IOI agree on between ninety-seven and ninety-nine point five percent of the correct sentences. But on only eleven to forty-two percent of the errors."),
        ('H', "Here's a detail I find telling. Two of the automated circuits get faithfulness scores above one, under mean ablation. In other words, on average, the circuit is more confident in the right name than the full model is."),
        ('H', 'By an average score, that looks extra faithful. By this new test, it looks like a circuit that is cleaner than the model it is supposed to explain.'),
        ('H', "Something else is striking. In this paper's setup, all three automated methods were trained, or searched, to match the model's full output. Not to get the right answer. They were rewarded for matching the model, mistakes included. And they still mostly miss the mistakes."),
        ('H', 'The ablation method matters, too. Switch the classic circuit to resample ablation, and error agreement rises to about forty-one percent. But correct agreement falls to about ninety-one, and the faithfulness score drops to about zero point six four.'),
        ('H', "Now a second task, called Docstring. A tiny model fills in documentation for Python code. It makes many more mistakes, about a third of the time, and the picture is messier."),
        ('H', "The classic circuit for that task still shows a gap. About seventy-seven percent correct agreement, against about thirty-six for errors."),
        ('H', 'But one automated circuit reproduces errors slightly more often than successes. About sixty-nine percent of errors, against about sixty-six percent of correct sentences. The authors read that as a circuit that keeps a good share of both. Its faithfulness score, though, is only about zero point six five.'),
        ('H', "And a small gap isn't automatically good news. Switch that task's classic circuit to resampling, and its gap shrinks from forty-one points to eight. But mostly because correct agreement falls."),
        ('H', "Quick recap. A circuit can look highly faithful on average, while getting the model's own mistakes mostly wrong. And the size of that blind spot depends on the circuit, the task, and how you knock out everything else."),
        ('~', 'chime'),
        ('H?', "First question for the room. If a circuit gets the right answer where the model got it wrong, is it a worse explanation of the model, or a better description of the task? What, exactly, is a circuit supposed to explain?"),
    ]),

    # ---------------------------------------------------------------- 4. can the gap be explained away? (§3, Fig. 1, Table 4, App. C, Table 7)
    dict(title='Can the gap be explained away?', music='sting', lines=[
        ('H', "Part three. Whenever you see a gap like this, the obvious move is to look for a boring explanation. The paper tries several. I'll take them one at a time."),
        ('H', 'Boring explanation number one: errors are rare. If a circuit-finding method almost never sees a mistake, of course it never learns to make one.'),
        ('H', 'To test this, the authors turn to a benchmark with bigger models and more errors: science multiple-choice questions, and subtraction, on open models such as Llama and Gemma.'),
        ('H', "Take Gemma on the hard science questions. Thirty-eight percent of the examples used to find the circuit are the model's own mistakes. That's not rare at all."),
        ('H', 'And yet, with a circuit that keeps one percent of the edges, correct agreement is about eighty percent, and error agreement is about fifty-four. The gap is smaller than in IOI. But it is still there.'),
        ('H', 'They also try weighting the errors more heavily. In a follow-up on IOI, give errors half the weight in the search, and error agreement rises from about nine percent to thirty-seven. But correct agreement falls, from about ninety-nine to ninety-one.'),
        ('H', "So rarity is part of the story. But it isn't the whole story. More exposure helps, and it costs you on the correct side."),
        ('H', "Boring explanation number two: errors are close calls.", 0.5),
        ('H', "When a model gets something wrong, it's often barely wrong. The scores for the two answers are nearly tied. And a near tie is easy to tip over. Even tiny differences between the circuit and the model could flip the answer."),
        ('H', "So the authors compare like with like. They pair each error with a correct sentence where the model was just as uncertain. Call it matching close calls."),
        ('H', 'This one does change things on the benchmark. For Llama on the hard science questions, with two percent of the edges, correct agreement drops from eighty percent overall, to about forty-seven percent among the matched close calls. Error agreement stays around fifty-five.'),
        ('H', 'Taken at face value, that reverses the gap. The paper itself only calls it narrowed.'),
        ('H', 'So in some settings, much of the apparent gap was about close calls, not about errors as such.'),
        ('H', 'But not everywhere. Gemma on the easier science questions keeps gaps of fifteen to twenty-one points at several circuit sizes. And in IOI, every circuit, under every kind of ablation, still has a positive gap after matching. The classic circuit under mean ablation: about ninety-five, against about fifteen.'),
        ('H', "Boring explanation number three: maybe the circuit is just slightly biased toward the right answer. Nudge it toward the wrong name, and you'll get the errors back."),
        ('H', "And here's a subtle result. On IOI, simply shifting the circuit's output toward the subject's name reproduces at least as many errors as more elaborate fixes the authors try. You can match the model's overall error rate this way."),
        ('H', "But matching how often the model is wrong isn't the same as matching which sentences it is wrong on. A blanket nudge doesn't consistently recover the particular mistakes."),
        ('H', 'That distinction, the rate of errors versus the identity of errors, is the heart of this paper.', 0.5),
        ('H', "Quick recap. Rare errors explain part of the gap. Close calls explain part of it, in some settings. A nudge toward the wrong name gets the error rate right, but not which sentences are wrong. And in IOI, the gap survives all three."),
    ]),

    # ---------------------------------------------------------------- 5. the case study: 63 additions (§4.1, §4.2, App. D, Table 4)
    dict(title='Going looking for the missing pieces', music=None, lines=[
        ('H', "Part four. So far, the paper has measured a blind spot. Now it tries to fill it in."),
        ('H', "The question is: which heads, at which positions, did the classic circuit leave out, that the model needs to make its mistakes?"),
        ('H', 'GPT-2 small has a hundred forty-four heads, and each can be added at any of twenty-five positions in the sentence. That gives about thirty-five hundred candidates.'),
        ('H', "The search adds a few at a time. A quick estimate shortlists promising ones, and the best are tested properly. The goal: reproduce more of the model's errors. Lose no more than half a point of correct agreement. And add as little as possible."),
        ('H', 'The result is an extension of the classic circuit, with sixty-three additions.'),
        ('H', "Then it's frozen, and tested on twenty-six thousand fresh sentences, two hundred twenty-five of which the model gets wrong."),
        ('H', 'On this new test set, the classic circuit reproduces about fourteen percent of those errors. The extended circuit reproduces about seventy-five percent.', 0.6),
        ('H', 'And correct agreement barely moves. From about ninety-nine point three percent to ninety-eight point nine.'),
        ('H', "In absolute terms, that's a hundred thirty-seven more errors reproduced, and a hundred six correct sentences lost. Correct sentences outnumber errors more than a hundred to one, so a tiny percentage there is still a lot of sentences."),
        ('H', "There are two controls, and I think they're good ones."),
        ('H', "First, random extensions of the same size and structure. They reproduce between about seventeen and forty-one percent of the errors. So it isn't just that adding sixty-three of anything helps."),
        ('H', "Second, that blanket nudge toward the subject's name, tuned to lose the same amount of correct agreement. It reproduces only about twenty percent of the errors."),
        ('H', "So these particular additions recover particular mistakes. That's the claim, and the controls support it."),
        ('H', "One caveat, from the appendix. On a second fresh check, correct agreement dropped a little more than the search allowed. Small, but the trade isn't free."),
        ('H', "And under resample ablation, the extension still helps. Error agreement rises from about forty-one percent to about sixty-one. And correct agreement rises too, from about ninety-one to about ninety-eight."),
    ]),

    # ---------------------------------------------------------------- 6. the two omitted computations (§4.3, Fig. 2)
    dict(title='How the wrong name wins', music='sting', lines=[
        ('H', "Now, the part I like most. The authors don't stop at a number. They trace what the added pieces do."),
        ('H', 'They study the hundred thirty-seven newly reproduced errors, using the same tools as the original IOI work. Copy one internal signal from one run into another, and see whether the answer flips. This is called patching.'),
        ('H', 'They find two paths by which left-out computation makes the wrong name win.'),
        ('H', 'The first path goes through the inhibition heads.', 0.5),
        ('H', "Recall their job. They look at the repeated name, and tell the name movers: don't copy that one."),
        ('H', "In the extended circuit, some added heads bring in context from elsewhere in the sentence, including the object being given. That changes where the inhibition heads look."),
        ('H', "In the paper's example, one of them looks at the repeated name much less. Then the name movers attend more to the subject, and they copy the wrong name."),
        ('H', "Here's the key test. Take only the part of the inhibition signal that changed, and patch it into what the name movers look for, in the classic circuit. Leave everything else alone."),
        ('H', "That alone makes the classic circuit choose the wrong name on a hundred twenty of the hundred thirty-seven errors."),
        ('H', "Then they ask, does the object matter? They take the information the added heads pull from the object word, and swap it for what they'd get if the object were a different word. A bone becomes a snack. Nothing else in the sentence changes."),
        ('H', "That swap restores the right answer on a hundred seven of the hundred thirty-seven sentences. And if they hold the inhibition heads' outputs fixed while doing the swap, sixty-eight of those corrections disappear."),
        ('H', "So the object word seems to shape the extended circuit's mistake, partly through the inhibition heads. The authors are careful here. This doesn't tell us which feature of the object matters. Whether it's something about bones, or just something about that word."),
        ('H', 'The second path happens much earlier.', 0.5),
        ('H', "Five heads in the very first layer have outputs at the correct name's position. The classic circuit leaves those outputs out. Two of these heads are in the circuit, but only at the repeated name."),
        ('H', "Together with the layers that follow them, these outputs change how the correct name is represented by the time the name movers look for it."),
        ('H', "Think of it as changing the label on the correct name. The name movers that copy names into the answer find it a bit less. And another set of heads, which push names down, find it a bit more. Both effects favor the wrong name."),
        ('H', "Patch in just those changed labels, at just the correct name's position, and the classic circuit reproduces the error on thirty-five of the hundred thirty-seven sentences. Patch them in anywhere else, and it reproduces none."),
        ('H', "So the first path accounts for most of the recovered errors, and the second for a smaller share. A hundred twenty plus thirty-five is more than a hundred thirty-seven, so the two paths must overlap. And the paper notes that the other parts of the circuit can amplify or oppose both effects."),
        ('H', "Here's my reading. The classic circuit may still describe how GPT-2 usually solves the task. What it leaves out is context that sometimes pushes the same machinery toward the wrong answer. But the paper shows this only for a subset of errors, in one circuit."),
        ('~', 'chime'),
        ('H?', "Here's one for the room. The extension was found by a search that had the errors in its objective. The authors then traced two paths through it. Is that enough to call it mechanism, rather than a good fit? What else would you want to see?"),
    ]),

    # ---------------------------------------------------------------- 7. our reading (§5, §7; extrapolation labelled)
    dict(title='What it means for circuits', music='sting', lines=[
        ('H', "Finally, let's step back. What should we take from this?"),
        ('H', "The paper's recommendation is practical. One, split the sentences by whether the model is right or wrong. Two, report agreement on both piles, with how many sentences are in each. Three, on the error pile, count only the same wrong answer. And four, report it across several circuit sizes, not just one."),
        ('H', "That's cheap to do, and I think it should become standard."),
        ('H', 'The authors are also careful about what passing this test would mean. They call exact error reproduction a necessary test, not a sufficient one. A circuit could reproduce every answer the model gives, for the wrong internal reasons.'),
        ('H', "Now, some things I'd push on.", 0.5),
        ('H', 'First, the ablation. Every circuit is evaluated by replacing everything outside it. And each kind of ablation feeds the circuit something the full model never sees on that sentence.'),
        ('H', 'So how much of the error gap belongs to the circuit, and how much to the knockout? The paper shows the answer changes with the method. That is itself a warning.'),
        ('H', 'Second, the scope. The careful mechanism story is one circuit, in one small model, on one task. The authors say so. The benchmark results are broader, but noisier, and matching close calls shows that they explain a good part of the gap in some settings.'),
        ('H', "Third, a philosophical one. There may be two things we want from a circuit. One is the algorithm for the task: the clean version, the one that gets Sara right. The other is a model of the model, warts and all."),
        ('H', "Classic circuits may be very good at the first. This paper shows they're much weaker at the second."),
        ('H', "And here's why I think that matters for this pod.", 0.6),
        ('H', "This is my extrapolation, not something the paper tests. Think about a machine-learned climate emulator. Suppose someone explains how it represents, say, the response of rainfall to warming. And the explanation reproduces the emulator's skill beautifully."),
        ('H', "But emulators have known biases. Places where they drift, or come out too warm, or too wet. If the explanation doesn't reproduce those biases, then it can't tell us where they come from. And that's exactly where an explanation would be most useful."),
        ('H', "The same split could apply. Agreement where the emulator is right. Agreement where it's wrong, in the same way. Measured separately."),
        ('~', 'chime'),
        ('H?', "Something to bring on Wednesday. How much of the error gap do you think is the circuit, and how much is the way we knock out everything else?"),
        ('~', 'chime'),
        ('H?', "And what would the same test look like for an emulator and its known biases?"),
    ]),

    # ---------------------------------------------------------------- wrap-up
    dict(title='Wrap-up', music='sting', lines=[
        ('H', "Let's recap."),
        ('H', "Circuits are usually judged by how well they keep the model's average behavior. This paper judges them on two piles separately: what the model gets right, and what it gets wrong. On the wrong pile, only the same wrong answer counts."),
        ('H', 'On IOI in GPT-2 small, under mean ablation, every circuit tested kept nearly all of the successes, but missed most of the mistakes. The classic circuit: ninety-nine point five percent, against fifteen.'),
        ('H', 'Some of the gap comes from errors being rare, and some from errors being close calls. But in IOI, it survives both checks.'),
        ('H', "Matching how often a model is wrong isn't the same as matching where."),
        ('H', 'Adding sixty-three carefully chosen heads and positions to the classic circuit brings error reproduction from about one in seven to about three quarters of the held-out errors. That costs a little on the correct side, and it beats random and blanket-nudge controls.'),
        ('H', 'And the missing pieces have a story. Context that changes where the inhibition heads look. And early processing that changes how the correct name is found.'),
        ('H', 'I think the lesson goes well beyond this one task.', 0.6),
        ('H', "An explanation of how a model succeeds isn't automatically an explanation of how it fails. If we want explanations we can debug with, we have to test them on the failures."),
        ('H', "Here are the questions once more, for the room."),
        ('~', 'chime'),
        ('H?', 'One. When a circuit is right where the model is wrong, what has it explained?'),
        ('H?', 'Two. The extension was searched for with the errors in mind. What would convince you it found mechanism?'),
        ('H?', 'Three. How much of the gap belongs to the ablation, rather than the circuit?'),
        ('H?', 'And four. What would this test look like for an emulator and its biases?', 0.4),
        ('H', "Bring your disagreements. That's what journal club is for.", 2.0),
        ('H', 'Thanks for listening to the aigs pod. See you on Wednesday.', 0.6),
    ]),
]
