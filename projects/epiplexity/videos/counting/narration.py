"""Who's Counting?: what the host says over each scene. Beats are (visual_time, text), visual_time pointing at the
moment in the scene's authored timeline when the thing the line talks about appears.

Facts: arXiv:2601.03220v2 §2 (background), §3 (Def. 8, Thm 9), §4 (prequential / requential), §5 (Thms 12-13,
Figs. 3, 4a, 6), §7 (related work); projects/epiplexity/AGENTS.md lists them with the accuracy notes. Historical
claims are only the safe ones listed there. The compression numbers and the laptop run are ours, and are said to be.
"""

VOICE = 'am_michael'
SPEED = 1.0
LANG = 'a'
SAY = {
    'Kolmogorov': 'Kol-mo-gorov',        # otherwise heard as "Kalmogorov" (topic note)
    "Kolmogorov's": "Kol-mo-gorov's",
    'Martin-Löf': 'Martin Luff',
}

SCENES = [
    dict(scene='ColdOpen', smax=1.3, hold=0.5, beats=[
        (0.5, 'Four files, each about a million bits.'),
        (3.5, 'The first: all zeros.'),
        (6.0, 'The second: a million coin flips.'),
        (9.0, 'The third: the output of a pseudorandom generator, started from a fifty-six bit seed.'),
        (14.5, 'The fourth: cellular automaton rule fifty-four. Each line holds a random row of sixty-four cells, and the row the rule makes from it forty-eight steps later.'),
        (24.0, 'Which file holds the most information?'),
        (27.0, "That depends on who's counting. Let's call in the judges, and keep score."),
    ]),
    dict(scene='Title', hold=1.0, beats=[
        (0.6, "Who's counting? Shannon, Kolmogorov, the cryptographers, and a new measure called epiplexity."),
        (4.5, 'A companion to the 2026 paper, From Entropy to Epiplexity, by Finzi and colleagues.'),
    ]),
    dict(scene='Shannon', beats=[
        (0.5, 'Judge one: Claude Shannon, 1948.'),
        (3.0, 'Information is surprise. An outcome with probability p carries log of one over p bits.'),
        (9.0, 'A fair coin flip: one bit. A one-in-a-thousand event: about ten.'),
        (14.0, 'Entropy is the average surprise, and no code can beat it on average.'),
        (19.0, 'It describes a source, not a file.'),
        (22.0, 'And meaning is set aside on purpose: the semantic aspects, Shannon wrote, are irrelevant to the engineering problem.'),
    ]),
    dict(scene='ScoreShannon', beats=[
        (0.5, 'His scores. All zeros: nothing to be surprised by. Zero bits.'),
        (4.0, 'Coin flips: a million.'),
        (6.5, 'The pseudorandom file: only the seed was random. Fifty-six bits.'),
        (10.0, 'The automaton: only the starting rows were random. Half a million.'),
    ]),
    dict(scene='Rules', beats=[
        (0.5, "Shannon's information obeys three famous rules."),
        (3.0, "One: processing can't create information. A fixed function never raises the entropy."),
        (9.0, "Two: order doesn't matter. X then Y costs the same as Y then X."),
        (15.0, "Three: the true distribution is the best model. So, the story goes, a model can't learn more than its source."),
    ]),
    dict(scene='Kolmogorov', beats=[
        (0.5, 'Judge two, from the 1960s: Solomonoff, Kolmogorov, and Chaitin.'),
        (4.5, 'The information in one string is the length of the shortest program that prints it.'),
        (10.0, 'Change the programming language, and that moves by at most a constant.'),
        (14.5, 'And as Martin-Löf made precise in 1966, a random string has no description much shorter than itself. It is incompressible.'),
    ]),
    dict(scene='ScoreK', beats=[
        (0.5, 'His scores. All zeros: print a zero, a million times. About twenty bits.'),
        (4.5, 'Coin flips: no shortcut, a million.'),
        (7.5, 'The pseudorandom file: the generator plus its seed. Small.'),
        (10.5, 'The automaton: the rule plus the random starts. Half a million.'),
        (14.0, 'Two judges, nearly the same verdict.'),
    ]),
    dict(scene='Incomputable', beats=[
        (0.5, 'But nobody can compute this score: finding the shortest program would solve the halting problem.'),
        (6.5, 'Chaitin showed that, in a given formal system, no specific string can be proven more complex than some fixed limit.'),
        (13.0, 'So we ran real compressors, on our own copies of the files.'),
        (17.5, "Zeros vanish. Coin flips don't shrink, and neither does the pseudorandom file: Kolmogorov says tiny, the compressor says a million bits."),
        (26.0, 'The automaton barely shrinks, to ninety-four percent, where Shannon says fifty.'),
        (31.0, 'A real compressor has limited time. It is already a bounded observer.'),
    ]),
    dict(scene='ScoreZip', beats=[
        (0.5, 'On the scorecard: a tie, between the coin flips and the pseudorandom file.'),
    ]),
    dict(scene='Structure', beats=[
        (0.5, 'Every judge so far crowns the coin flips, which hold nothing to learn.'),
        (5.0, 'So people tried to split information into structure and noise.'),
        (9.5, "Koppel's sophistication counts the bits of the simplest set in which the string looks typical. Effective complexity, from Gell-Mann and Lloyd, has the same aim."),
        (18.5, "Bennett's logical depth asks how long a near-shortest program runs."),
        (23.0, 'Cream stirred into coffee is simple at the start, simple when mixed, and intricate in between.'),
        (29.0, 'But with unlimited computing, the swirls are just the start plus physics, and much of that complexity evaporates.'),
    ]),
    dict(scene='ScoreSoph', beats=[
        (0.5, 'Sophistication scores all four files near zero, even the automaton: a simple rule plus random rows.'),
        (7.0, 'No noise counted as structure. But no structure found, either.'),
    ]),
    dict(scene='Crypto', beats=[
        (0.5, 'The missing piece came from cryptography.'),
        (3.0, 'Von Neumann had written: anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.'),
        (11.0, 'In 1982, Blum and Micali, and Yao, answered: a sequence is pseudorandom if no fast test can tell it from random, or predict its next bit.'),
        (19.0, 'So randomness depends on the observer. Without the seed, our third file is as random as the coins.'),
        (25.0, 'Underneath are one-way functions: easy to compute, hard to undo.'),
    ]),
    dict(scene='ScoreCrypto', beats=[
        (0.5, 'The cryptographer asks: does it look random to a fast observer? Zeros, no. Coins, yes. The pseudorandom file, yes.'),
        (7.0, 'The automaton, no: much of it can be predicted.'),
        (10.5, "But this judge only says yes or no. It doesn't count the structure."),
    ]),
    dict(scene='Epiplexity', beats=[
        (0.5, 'Now, the paper. Give the observer one time budget, T, for learning a model and using it.'),
        (6.5, 'Among programs within budget, find the shortest total code: bits for the model, plus bits for the data given the model.'),
        (14.0, "The model's bits are the epiplexity, S sub T, for epistemic complexity: the structure."),
        (20.0, "What's left is the time-bounded entropy, H sub T: what still looks random."),
    ]),
    dict(scene='ScoreEpi', beats=[
        (0.5, 'The new scores. Zeros: a tiny model, nothing left over.'),
        (4.0, 'Coin flips: the model is just, flip a coin. No structure, and a million random bits.'),
        (8.5, "Pseudorandom: the paper proves it's almost all entropy, with almost no structure."),
        (13.5, 'And the automaton: a learner can partly predict the answers, using gliders and their collisions. The most structure of the four.'),
    ]),
    dict(scene='Measuring', beats=[
        (0.5, 'To measure it, train a network and watch the loss.'),
        (3.5, 'On random data, it never falls. On simple data, it drops fast and stops. On structured data, it keeps falling.'),
        (10.5, "The area above the final loss estimates what the model absorbed. It's a heuristic; a stricter teacher and student code gives smaller numbers that track it."),
        (19.0, "In the paper, rule fifty-four's epiplexity keeps climbing with compute, past five million bits, while rule fifteen peaks and falls, and rule thirty stays near zero."),
    ]),
    dict(scene='Laptop', beats=[
        (0.5, 'We tried a tiny version on a laptop: a small transformer predicting a thirty-two cell row, sixteen steps ahead.'),
        (6.5, 'Rule fifteen is learned completely. Rule thirty and the coins never get below thirty-two bits. Rule fifty-four keeps improving.'),
        (14.0, 'Stop at four thousand steps, and rule fifteen has the bigger area.'),
        (17.5, 'Train five times longer, and rule fifty-four overtakes it. The ranking depends on the budget.'),
    ]),
    dict(scene='Revisited', beats=[
        (0.5, 'Back to the three rules. For a bounded observer, each one bends.'),
        (4.0, 'Processing creates information: a generator makes randomness, and rule fifty-four makes structure.'),
        (10.0, 'Order matters: modeling rule thirty forward nearly reaches the true entropy; in reverse, a gap remains, growing with size.'),
        (18.0, 'And a compute-limited model, predicting rule fifty-four far ahead, builds a far bigger program than the rule itself.'),
        (25.0, 'The classical measures keep all three rules, because they assume unlimited computation.'),
    ]),
    dict(scene='Map', beats=[
        (0.5, 'Here is the family on one map, in our own framing: one string or a distribution, across; unlimited or bounded observer, up.'),
        (8.0, 'Shannon, Kolmogorov, sophistication and logical depth all assume unlimited computation.'),
        (13.0, "Excess entropy measured an area much like the paper's, for stationary processes."),
        (18.0, 'Measures from cryptography, and usable information, bound the observer, but count only the random part.'),
        (23.0, 'Epiplexity takes that corner and counts structure. Minimum description length picks a model for given data; epiplexity picks data for a given budget.'),
    ]),
    dict(scene='Verdict', beats=[
        (0.5, 'So was Shannon wrong? No. He asked how many bits to send. Epiplexity asks how much there is to learn, in the time you have.'),
        (8.5, 'The price: it depends on the observer, it can only be estimated, and it counts structure, not usefulness.'),
    ]),
    dict(scene='Questions', hold=1.2, beats=[
        (0.5, 'Some questions to think about.'),
        (2.5, 'If information depends on the observer, is it still a property of the data?'),
        (8.5, 'A much faster observer sees less randomness. Does it see more structure, or less?'),
        (14.5, 'The laws of physics are short. Is the universe they generate rich in epiplexity, and for whom?'),
    ]),
    dict(scene='End', hold=2.3, beats=[
        (0.5, 'Shannon counts surprise. Kolmogorov counts programs. Epiplexity counts what a bounded learner can extract.'),
        (7.5, 'Same four files. Different winners.'),
    ]),
]
