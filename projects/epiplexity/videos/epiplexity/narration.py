"""From Entropy to Epiplexity: what Bella says over each scene. Beats are (visual_time, text), pointed at the moment the
visual appears in the scene's authored timeline (scenes*.py). Facts: arXiv:2601.03220v2 (§ and Fig. noted per scene);
our laptop runs (lab/eca_lab.py, lab/compress_lab.py) are said to be ours. See projects/epiplexity/AGENTS.md."""

VOICE = 'bella-nicole'
SPEED = 1.0
LANG = 'a'
SAY = {
    'Qiu': 'Chyoo',
    'Finzi': 'Finzee',
    'Izmailov': 'Izmylov',
    'Kolmogorov': 'Kolmogorov',
    'Solomonoff': 'Solomonoff',
    'Chaitin': 'Chaytin',
    'epiplexity': 'eppiplexity',
    'Epiplexity': 'Eppiplexity',
    'CIFAR': 'Seefar',
    'xz': 'X Z',
}

SCENES = [
    # §1, §5.1: AlphaZero (zero human data; simple rules and algorithm; thousands of TPU hours; megabytes in the weights)
    dict(scene='ColdOpen', smax=1.3, hold=0.5, beats=[
        (0.8, "AlphaZero learned chess without a single human game."),
        (4.5, "It was given only the rules and a learning algorithm, both short to write down."),
        (10.0, "After thousands of TPU hours of self-play, its weights hold megabytes, and it plays better than any person."),
        (17.0, "Yet classic information theory seems to say it learned almost nothing new."),
        (23.5, "So where did that come from?"),
    ]),
    dict(scene='Title', hold=0.9, vend=8.0, beats=[
        (0.7, "This paper, by Marc Finzi, Shikai Qiu, Yiding Jiang and their colleagues, proposes an answer to that question."),
        (6.8, "Its name for it: epiplexity, short for epistemic complexity."),
    ]),
    # Shannon 1948; §2.1; §5.1 (data processing, information non-increase)
    dict(scene='Shannon', hold=0.5, beats=[
        (0.6, "Start with the classic view. In 1948, Claude Shannon measured information as surprise."),
        (6.5, "An outcome with probability p carries log of one over p bits. A fair coin flip: one bit."),
        (13.5, "Entropy is the average surprise: the shortest code, on average, for what a source sends."),
        (20.5, "And a rule follows: processing data with any fixed function can never raise its entropy."),
    ]),
    # Def. 1; Martin-Löf; §5.1: K(f(x)) <= K(x) + K(f) + c
    dict(scene='Kolmogorov', hold=0.5, beats=[
        (0.6, "In the 1960s, Solomonoff, Kolmogorov and Chaitin measured one string instead: the length of the shortest program that prints it."),
        (9.0, "Zero one, repeated half a million times, has a tiny program."),
        (13.5, "A million coin flips has nothing much shorter than itself. Random means incompressible."),
        (20.5, "The same rule holds: running a program on x adds at most that program's length."),
    ]),
    # Def. 3 (PRG), Yao 1982 next-bit test; ours_compress.json (our check)
    dict(scene='Crack', beats=[
        (0.6, "Now the crack. A pseudorandom generator stretches a short seed, say sixty-four bits, into a million bits."),
        (7.5, "To Shannon and to Kolmogorov, that is about sixty-four bits of information."),
        (13.0, "But if the generator is secure, no efficient algorithm can predict its next bit better than chance."),
        (20.0, "In our own check, gzip and xz need a full bit per bit, just as for real coin flips."),
        (27.5, "Both theories assume an observer with unlimited compute. No real learner is that observer."),
    ]),
    # Def. 7, Def. 8 (eq. 3-4)
    dict(scene='Observer', hold=0.5, beats=[
        (0.6, "So the paper puts the observer into the definition, with a time budget, T."),
        (5.5, "Among programs that can sample and score the data within that budget,"),
        (11.0, "pick the one with the shortest two-part code: bits for the program, plus bits for the data encoded with it."),
        (19.5, "That program's length is the epiplexity, S sub T: the structure this observer can learn."),
        (26.5, "What it still cannot predict is the time-bounded entropy, H sub T: what looks random to it."),
    ]),
    # §3 (uniform: S_T <= c; 0101/1010: both O(1)); Thm 9; Fig. 1 left (illustration)
    dict(scene='Spectrum', hold=0.5, beats=[
        (0.6, "Try it on a few objects. A string of zeros: almost nothing of either kind."),
        (5.5, "Coin flips: all randomness, no structure."),
        (9.0, "And the generator's output? The paper proves that to any polynomial-time observer, it is nearly all randomness."),
        (17.5, "Code shows the range. A config file of random keys is mostly randomness. Repetitive code has little of either. A real algorithm is rich in structure."),
    ]),
    # §4.1 (eq. 8, heuristic), §4.2 (eq. 9), §4.3 (2-10x slower; Fig. 2c)
    dict(scene='Measuring', beats=[
        (0.6, "To measure it, let a neural network be the observer, and watch its loss as it trains."),
        (6.5, "The area under the curve, above where it ends, estimates the structure absorbed into the weights. It is a heuristic."),
        (15.0, "Random data never improves: no area. Simple data is learned at once: a sliver. Structured data keeps paying off."),
        (23.0, "A rigorous version, requential coding, costs two to ten times more."),
        (31.0, "The two correlate, though the area runs larger."),
    ]),
    # §5.1, Fig. 3 left (rollouts computed here from the rules)
    dict(scene='Automata', hold=0.5, beats=[
        (0.6, "Now the three paradoxes. Paradox one: computation cannot create information."),
        (5.5, "Test it on elementary cellular automata: a row of cells, each updated from itself and its two neighbours by a fixed rule."),
        (14.0, "Rule fifteen is simple and periodic. Rule thirty looks like noise. Rule fifty-four grows gliders that travel and collide."),
    ]),
    # Fig. 3 right (fig3_eca.json); Thm 12 guidance
    dict(scene='Fig3', hold=0.5, beats=[
        (0.6, "The paper trains transformers to predict the row forty-eight steps later, at many compute budgets."),
        (7.0, "Rule fifteen: little of either. Rule thirty: the loss makes no progress, so it is all time-bounded entropy."),
        (15.5, "Rule fifty-four: the loss keeps falling, and epiplexity climbs with compute, to about five million bits."),
        (23.0, "A short program created structure. The advice for synthetic data: use transformations without an easy inverse."),
    ]),
    # ours_rules_n32_k8.json and ours_rules_n32_k16_s20000.json (our runs; the long one predicts 16 steps)
    dict(scene='OurRun', beats=[
        (0.6, "We ran a miniature version on a laptop: a small transformer, thirty-two cells, eight steps."),
        (8.0, "Rule fifteen is learned perfectly, after about seventeen hundred steps."),
        (12.5, "Rule thirty never leaves thirty-two bits, like coin flips: pure randomness to this observer."),
        (19.5, "Rules fifty-four and one hundred ten end partway, still improving."),
        (24.5, "At this tiny scale, rule fifteen even has the bigger area, as in the paper's figure at its smallest budgets."),
        (30.5, "Train five times longer, and rule fifty-four keeps learning. Its area grows to more than twice rule fifteen's."),
    ]),
    # §5.2, Thm 13, Fig. 4a (fig4_owf_chess.json)
    dict(scene='OneWay', hold=0.5, beats=[
        (0.6, "Paradox two: order should not matter. Shannon's total is the same either way round."),
        (7.0, "But multiplying two primes is easy, and factoring the product is hard. Cryptography runs on such one-way functions."),
        (14.5, "Rule thirty, run for eight steps, is believed to be one-way. Input, then output: the model reaches the true entropy."),
        (22.5, "Output, then input: it keeps a gap, and the gap widens as the rows grow."),
    ]),
    # Fig. 4b/c, §6.1, Fig. 7 (fig7_chess_ood.json)
    dict(scene='Chess', hold=0.5, beats=[
        (0.6, "Chess games can be written as the moves and then the final board, or the board first, then the moves."),
        (8.0, "Board first is the harder direction. With enough compute, it shows more randomness, and also more structure."),
        (15.5, "And it seems to pay off. Fine-tuned to evaluate positions, reverse-order models score twenty-eight percent against twenty-one. On puzzles, they tie."),
    ]),
    # §5.3, §5.3.1, Fig. 5a/b (fig5_induction.json)
    dict(scene='Induction', beats=[
        (0.6, "Paradox three: a model can at best match the process that generated its data."),
        (6.5, "Ilya Sutskever's example: to name the culprit in a murder mystery, the reader must deduce it. The author may simply have picked the murderer first."),
        (15.5, "The paper builds a version: random bits with some hidden, plus rule thirty applied to all of them."),
        (22.5, "The loss settles at one bit per hidden bit, but the compute it takes grows exponentially."),
        (29.0, "And epiplexity rises with every hidden bit: an inference the generator never made."),
    ]),
    # §5.3.2, Def. 14 (not proven for Life), Fig. 6 (fig6_emergence.json)
    dict(scene='Emergence', beats=[
        (0.6, "Emergence tells the same story. In the Game of Life, an unbounded observer just runs the rule."),
        (7.0, "A bounded one must learn gliders, guns and their collisions: a longer program. That is not proven for Life."),
        (15.0, "On rule fifty-four, predicting many steps ahead, epiplexity rises with compute, to about fifteen million bits."),
        (22.5, "Then a looped model that unrolls the rule step by step takes over, and epiplexity drops."),
    ]),
    # §6.2, Fig. 8a (5B tokens: see accuracy note), §6.3, Fig. 8b (infinite-compute limit), Fig. 9
    dict(scene='Natural', hold=0.5, beats=[
        (0.6, "What about real data? On five billion tokens each, text from the web holds the most structure, and chess comes next."),
        (7.5, "Images hold the most information in total, but over ninety-nine percent of it is randomness: the exact pixels."),
        (14.5, "Extrapolated from published scaling laws, language again leads, raw images trail, and turning images into discrete tokens helps a lot."),
    ]),
    # §6.4, Fig. 8c (small differences), §2.3 (MDL dual)
    dict(scene='Selection', hold=0.5, beats=[
        (0.6, "A data selection method, Adaptive Data Optimization, favours data whose loss falls fastest."),
        (7.0, "It ends up with more epiplexity than plain sampling, and slightly better downstream scores."),
        (12.5, "Classic minimum description length picks a model for your data. Epiplexity turns it around: it picks data for your compute."),
    ]),
    # §2.2, §7 (sophistication, V-information); the comparison table is our framing
    dict(scene='Family', hold=0.5, beats=[
        (0.6, "Side by side: Shannon and Kolmogorov assume unlimited compute, so both call a pseudorandom stream simple."),
        (8.0, "Sophistication tried to measure structure, but unlimited compute explains much of it away."),
        (14.0, "Usable information limits the observer, but still counts only the randomness. Epiplexity limits the observer, and counts the structure."),
    ]),
    # accuracy notes in projects/epiplexity/AGENTS.md
    dict(scene='Limits', hold=0.5, beats=[
        (0.6, "Some limits. The numbers depend on the network and optimizer standing in for the observer."),
        (9.5, "Epiplexity counts how much structure, not whether it helps your task, and the downstream links are correlations."),
        (17.0, "And a typo: Figure eight a's caption says one billion tokens; the text and the bars say five."),
    ]),
    dict(scene='Questions', vend=21.0, hold=1.5, beats=[
        (0.5, "A few questions to think about."),
        (2.0, "Is information really relative to the observer, or is this a new quantity with an old name?"),
        (8.5, "Could we design synthetic data to maximize epiplexity, and what would go wrong?"),
        (14.5, "If physics could simulate everything, is nature's structure an artifact of our limits?"),
    ]),
    dict(scene='End', hold=2.4, vend=11.0, beats=[
        (0.6, "The takeaway: information depends on who is looking. Epiplexity is the part a bounded learner can carry away."),
    ]),
]
