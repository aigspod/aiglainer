"""From Entropy to Epiplexity: the full single-host episode (about 26 min). The owner's personal set: see the topic's naming rule.

Every claim traces to the paper (arXiv:2601.03220v2) or to well-known history:
- Cold open: AlphaZero from the rules alone, superhuman, megabytes in its weights, thousands of TPU hours, and
  "both Shannon and algorithmic information theory appear to say" it learned little (§1 p.2, §5.1 p.16-17).
- Shannon: surprisal log 1/P, entropy as the average, lower bound on average code length (§2.1); information
  non-increase H(f(X)) <= H(X) and the data processing inequality (§5.1); symmetry H(X)+H(Y|X) = H(Y)+H(X|Y) (§5.2).
  History: Shannon 1948, Bell Labs, "A Mathematical Theory of Communication", and his line that the semantic aspects
  of communication "are irrelevant to the engineering problem" (fact sheet, background).
- Kolmogorov: Solomonoff 1964, Kolmogorov 1965, Chaitin 1966 (background); Def. 1 shortest program; invariance up to
  a constant (§2.1); random strings are overwhelmingly incompressible (Kraft argument, p.6); Martin-Löf 1966: passing
  all computable tests = incompressible prefixes (§2.1, Def. 2; named only in the show notes); K is incomputable
  (standard); random sequences are incomputable and the von Neumann 1951 quote (p.6).
- Pseudorandomness: PRGs, Blum-Micali 1982, Yao 1982 next-bit test (Def. 3, p.6-7); PRGs conjectured to exist,
  resting on one-way functions (p.6-7); JAX makes random numbers by encrypting 1, 2, ..., N with the seed as key
  (p.7); Shannon entropy of G(U_k) is k, time-bounded K <= k + c (p.11).
- Epiplexity: Def. 7 (T-time model must sample and evaluate within T), Def. 8 (two-part code |P| + E[log 1/P(X)];
  S_T = |P*|, H_T = E[log 1/P*(X)]); name = epistemic complexity (p.3); uniform bits S_T <= c, the 0101/1010 example
  (said as a coin rigged to alternate) O(1) for both (p.10); Thm 9 for CSPRNGs (p.11); MDL two-part code (Def. 6,
  Rissanen; 1978 from the fact sheet) and "epiplexity is its dual: data selection given a compute budget" (p.9).
- Measuring: FLOPs, 6ND training (§4); prequential = area under the loss above the final loss, a heuristic that
  leans on symmetry of information, which fails time-bounded (§4.1, Eq. 8); random data never drops, simple data
  drops fast, both small (§4.1); requential: teacher samples, student pays cumulative KL, explicit code with known
  runtime (§4.2, Eq. 9); 2-10x slower; prequential typically several times larger; correlate well, best within a
  group, not guaranteed (§4.3, Fig. 2c).
- Puzzle one (§5.1): the paradox list (p.3); Thm 12 (H_poly rises by more than n - k - n eps - c); function vs inverse
  asymmetry and the synthetic-data advice (p.17); ECA: 256 rules, cell + two neighbours, random row of 64 cells,
  48 iterations, D = 100M tokens; rule 15 low/low, rule 30 high H_T, no progress, ~no S_T; rule 54 medium H_T, high
  S_T, loss keeps falling (Fig. 3).
- Puzzle two (§5.2): left-to-right vs reversed text, "arrow of time" (Papadopoulos et al. 2024); cryptography; Thm 13
  assumes one-way permutations; Thm 26 Bayes corollary; Fig. 4a rule 30, 8 steps, believed (not proven) one-way;
  forward reaches the Shannon entropy, reverse keeps a gap as n grows; Fig. 4b/c Lichess moves-then-board vs
  board-then-moves: reverse higher H_T and S_T as compute grows, gap vanishes at small compute.
- Puzzle three (§5.3): argmin_P E_Q[-log P] = Q; Sutskever 2019 quote (paraphrased on air) and the author picking the
  murderer first; hard induction (rule 30, 4 steps, n = 32, first h bits hidden, loss -> h, compute exponential in h,
  "consistent with" trying all candidates, epiplexity grows with h; Fig. 5b); easy induction (random Markov chain,
  part of the transition table hidden; epiplexity higher for 0 < h < 8 than h = 0 or h = 8; Fig. 5c; "never present
  in the data-generating process"); emergence (§5.3.2): Game of Life species (blocks, oscillators, gliders, guns,
  collisions), Def. 14, "We have not proven that the Game of Life satisfies this definition"; Fig. 6 rule 54,
  non-looped vs looped (chain-of-thought-like), epiplexity rises then an abrupt drop past a threshold, "likely" brute
  force; unusual case, natural data expected to show more structure with more compute (p.23).
- Data (§6): chess fine-tuning, puzzles about equal, centipawn (said as "judging who's ahead, and by how much")
  clearly higher, the authors' "richer board-state representations" hypothesis (§6.1, Fig. 7); Fig. 8a: OpenWebText >
  chess > CIFAR-5M in epiplexity, CIFAR-5M most total information, over 99% random, epiplexity a tiny fraction
  everywhere (§6.2; "five billion tokens": the topic's accuracy note reads the 1B caption as a typo); Fig. 8b: scaling
  laws, 1T tokens, said as "enormous compute budgets" (the text says 10^25 FLOPs, but the bars match the
  infinite-compute limit, per the topic's accuracy note; the ordering is the same), language highest, images
  least, VQ raises images "likely" via higher-level structure, video below images "likely" from temporal redundancy
  (§6.3); text-vs-images framing (§6.2); ADO picks subsets whose loss falls fastest, 1.3B params, "a little better"
  downstream and in OOD perplexity (the Fig. 8c gaps are small, per the accuracy note), higher prequential
  epiplexity, adapted from Jiang et al. 2025 (§6.4, footnote 5). Fig. 4a: the reverse gap "widens" with n (data note).
- Limits: prequential heuristic, requential slower, agreement not guaranteed (§4.3); estimates improve with better
  hyperparameter tuning (§4.1); amount not relevance, not a guarantee (p.4, §6.1); one-way functions assumed (Thm 10,
  12, 13); rule 30 believed one-way; Life not proven (p.23); Thm 10 only Omega(log n), nonconstructive (p.11); ADO
  figure adapted from a paper sharing an author (Yiding Jiang), with modest gains.
- Close: Shannon's exclusion of meaning (background); "epiplexity measures how much, not what" (p.4); MDL picks a model
  for given data, epiplexity picks data for a compute budget (p.9); AlphaZero: "a description of the AlphaZero
  algorithm and the result of running AlphaZero for thousands of TPU hours are distinct" (p.17). The questions are ours.
Our laptop runs (lab/) are not used: projects/epiplexity/AGENTS.md has no finished numbers yet.

A role ending in '?' ('H?') marks a question to think about; it is listed in the show notes. ('~', 'rest') is a pause
between ideas (PACE['rest'] seconds).
"""

HOSTS = {'H': 'bella-nicole'}   # role -> host in aiglainer/hosts.py: Bella blended 70/30 with Nicole
SPEED = 0.92                    # unhurried
PACE = dict(sentence=0.45, same=0.7, turn=0.35, segment=1.8, question=0.5, rest=1.2)

SAY = {
    'prequential': 'pree-quential',     # Kokoro's own reading is heard as "frequential"
    'Kolmogorov': 'Kol-mo-gorov',       # otherwise heard as "Kalmogorov"
    "Kolmogorov's": "Kol-mo-gorov's",
}

REST = ('~', 'rest')

SEGMENTS = [
    # ---------------------------------------------------------------- cold open: AlphaZero learned nothing?
    dict(title='Cold open', music=None, lines=[
        ('H', "Imagine you hand a computer the rules of chess, and nothing else. No games played by people, and no advice."),
        ('H', "It plays against itself, over and over, for thousands of hours on special chips. And it comes out superhuman."),
        ('H', "That's AlphaZero. Its trained network holds megabytes of what it worked out: openings, what each piece is worth, tactics, and strategy."),
        ('H', "Now ask the two great theories of information a simple question. How much did it learn?", 0.6),
        ('H', "Their answer is, almost nothing.", 0.6),
        ('H', "The rules are short to write down. So is the learning algorithm. And in both theories, running a short program can't create information."),
        ('H', "So everything it knows was, in a sense, already there in the rules and the algorithm."),
        REST,
        ('H', "That answer is clearly missing something. Today's paper says what, and gives it a name."),
    ]),

    # ---------------------------------------------------------------- welcome and the plan
    dict(title='Welcome', music='theme', lines=[
        ('H', "Hello, and welcome. I'm {H}, and this is an explainer about one paper. The voice you're hearing is synthetic. The paper, the numbers, and the arguments are real."),
        ('H', "The paper is called From Entropy to Epiplexity: Rethinking Information for Computationally Bounded Intelligence."),
        ('H', "It's by six researchers at Carnegie Mellon and New York University. You'll find all six names in the show notes."),
        ('H', "Its central idea fits in one sentence. How much information something holds depends on how much computing the observer can afford."),
        REST,
        ('H', "Here's where we're going. First, the two classic ways to measure information, and the crack in both."),
        ('H', "Then the new idea, called epiplexity, and how to measure it. Then three puzzles it untangles, what it says about data, and where it's still shaky."),
    ]),

    # ---------------------------------------------------------------- 1. Shannon: information as surprise
    dict(title='Surprise, by the bit', music='sting', lines=[
        ('H', "Let's begin in 1948. Claude Shannon, at Bell Labs, publishes a paper called A Mathematical Theory of Communication."),
        ('H', "His key move is to measure information as surprise."),
        ('H', "Flip a fair coin. Heads or tails, each half the time. Learning the result gives you exactly one bit of surprise."),
        ('H', "Now imagine a coin that lands heads ninety-nine times out of a hundred. Heads tells you almost nothing. Tails is a real surprise."),
        ('H', "Entropy is the average surprise. For fair coin flips, it's one bit per flip. For the lopsided coin, it's far less."),
        ('H', "And Shannon showed that this number is a hard limit. No code, however clever, can send the outcomes in fewer bits, on average."),
        REST,
        ('H', "Two consequences matter for our story."),
        ('H', "The first is that processing can't add information. Run data through any fixed recipe, and the information stays the same, or goes down. One version of this is called the data processing inequality."),
        ('H', "The second is that order doesn't matter. Read two things in either order, and the total information you gain is the same."),
        ('H', "Hold on to both of those. Both are about to wobble."),
        REST,
        ('H', "And notice what Shannon left out, on purpose. He wrote that the meaning of a message is irrelevant to the engineering problem."),
        ('H', "His measure is also about a source of messages, not one message in particular. So what about a single object?"),
    ]),

    # ---------------------------------------------------------------- 2. Kolmogorov: the shortest program
    dict(title='The shortest program', music=None, lines=[
        ('H', "In the 1960s, three people found the same answer on their own: Ray Solomonoff, Andrey Kolmogorov, and Gregory Chaitin."),
        ('H', "The information in a string, they said, is the length of the shortest computer program that prints it."),
        ('H', "Take a million zeros. A tiny program prints that: write zero, a million times. So there's very little information in it."),
        ('H', "Now take a million fair coin flips. Almost always, no program does much better than quoting the whole string. It can't be squeezed."),
        ('H', "That's the algorithmic definition of random. A random string is one you can't compress."),
        ('H', "In 1966, a Swedish mathematician made this precise: a sequence is random if it passes every test of randomness a computer could carry out. That turns out to mean the same thing as being incompressible."),
        ('H', "Two more facts: the programming language barely matters, and no algorithm can find the shortest program in general."),
        REST,
        ('H', "This view has a striking consequence. A truly random sequence can't be produced by any program at all."),
        ('H', "John von Neumann saw this coming. In 1951 he wrote that anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin."),
        ('H', "And yet, the computers around you make random numbers with arithmetic, all day long."),
    ]),

    # ---------------------------------------------------------------- 3. the crack: pseudorandomness
    dict(title='Randomness from a recipe', music='sting', lines=[
        ('H', "Here's how they do it. A pseudorandom generator takes a short random seed, and stretches it into millions of bits."),
        ('H', "Everything after the seed is plain arithmetic. The same seed always gives the same bits."),
        ('H', "So how much information is in the output? Shannon and Kolmogorov agree: the seed, plus at most a short program. Millions of bits add almost nothing."),
        ('H', "But now try to tell that output apart from real coin flips.", 0.6),
        ('H', "In 1982, cryptographers including Manuel Blum, Silvio Micali, and Andrew Yao set the modern standard. A good generator is one that no efficient algorithm can tell apart from true randomness."),
        ('H', "Put another way, no efficient algorithm can guess the next bit better than a coin toss, beyond a vanishingly small edge."),
        ('H', "Nobody has proven that such generators exist. But modern cryptography rests on the bet that they do."),
        REST,
        ('H', "So here's the crack. To an observer with unlimited time, the output is nearly empty. Just a seed. To any observer you could actually build, it's millions of bits of pure randomness."),
        ('H', "The same string, with two different answers. And what separates them is the observer's computing budget."),
        ('H', "Both classic theories measure information as if the observer could compute anything. Real learners can't."),
        ('H', "So the paper's key move is simple to state. Make the observer's compute part of the definition of information."),
    ]),

    # ---------------------------------------------------------------- 4. defining epiplexity: the two-part code
    dict(title='Epiplexity', music='sting', lines=[
        ('H', "Here's an everyday picture. Imagine you have to send a friend a huge file, in as few bits as possible, in two parts."),
        ('H', "Part one is a model: a program that captures the patterns in the data. Part two is everything the model couldn't predict, the leftover surprise, written down with the model's help."),
        ('H', "A bigger model costs more to send, but leaves less surprise. The best package makes the total as small as it can be."),
        ('H', "That's an old idea, the minimum description length principle, proposed by Jorma Rissanen in 1978."),
        REST,
        ('H', "Now the new rule. The model has to run within a fixed amount of computation, both to produce examples and to score them."),
        ('H', "Find the best two-part package under that limit. Then read off two numbers."),
        ('H', "The size of the model part is the epiplexity. It's the structure, what a bounded observer can learn from the data."),
        ('H', "The size of the leftover part is the time-bounded entropy. It's whatever still looks random, to that observer."),
        ('H', "Epiplexity is short for epistemic complexity."),
        REST,
        ('H', "Let's try it on three examples."),
        ('H', "First, the coin flips we started with. The best model is tiny: every bit is fifty-fifty. So there's huge time-bounded entropy, and almost no epiplexity."),
        ('H', "Second, a coin rigged to alternate: heads, tails, heads, tails, starting on either side with equal odds. A tiny model, and almost nothing left over. Low on both."),
        ('H', "Third, and most telling of all, the pseudorandom generator from before. To any efficient observer, it looks like coin flips: nearly maximal time-bounded entropy, and next to no epiplexity. The paper proves this, for a secure generator."),
        ('H', "Lots of randomness, and no structure worth learning. The interesting data sit in between."),
        ('H', "And here's a framing from the paper I like. The minimum description length principle picks a model for the data you have. Epiplexity turns that around, to pick data for the compute you have."),
    ]),

    # ---------------------------------------------------------------- 5. measuring it
    dict(title='Reading it off a loss curve', music=None, lines=[
        ('H', "In practice, the authors use neural networks, and their training runs."),
        ('H', "They measure time in floating point operations, and for each budget, they look for the model size and data that give the shortest total code."),
        ('H', "The first method is called prequential coding. Picture a training curve. The loss starts high, falls, and then flattens out."),
        ('H', "Each piece of data is scored just before the model trains on it. The flat level at the end is what stays random. And the area under the curve, above that final level, is roughly what the model absorbed. That area is the estimate of epiplexity."),
        ('H', "For random data, the curve never drops, so the area is tiny. For simple data, it drops fast and stops, so it's small again. A big area means slow, sustained learning."),
        ('H', "The authors are frank that this is a heuristic. It leans on a symmetry that no longer holds once compute is limited."),
        REST,
        ('H', "The second method is rigorous, and it's called requential coding. A teacher model, trained on real data, generates examples. A student learns only from those examples."),
        ('H', "The cost of describing the student adds up, step by step, how far its predictions sit from the teacher's. That gives an explicit code, with a known running time."),
        ('H', "The catch is speed. It's typically two to ten times slower."),
        ('H', "The area method usually comes out several times bigger. But the two tend to put different kinds of data in the same order, especially kinds that are alike."),
        ('H', "So here's a quick recap. Time-bounded entropy is roughly where the loss ends up: what stays random. Epiplexity is the learning along the way: the structure absorbed."),
    ]),

    # ---------------------------------------------------------------- 6. paradox 1: computation creates information
    dict(title='Puzzle one: creating information', music='sting', lines=[
        ('H', "Now the payoff. The paper names three ideas that the classic theories seem to prove, and that modern practice seems to break."),
        ('H', "Puzzle one. A fixed, deterministic process can't create information."),
        ('H', "And yet, there are pseudorandom generators, synthetic data that makes models better, mathematicians deriving new results from axioms, and AlphaZero."),
        ('H', "With a time limit, the puzzle dissolves. The paper proves that a secure generator raises the time-bounded entropy from the size of the seed to nearly the full length of the output."),
        ('H', "Here's the deeper reason. With unlimited compute, a function and its inverse are about equally complex. With limited compute, they can be wildly different: easy one way, hopeless the other."),
        ('H', "The practical advice for synthetic data: if you want a transformation to create something new, choose one with no simple, efficient way to undo it."),
        REST,
        ('H', "Then an experiment, with what are called elementary cellular automata."),
        ('H', "Picture a row of black and white cells. At each tick, every cell looks at itself and its two neighbors, and a fixed rule sets its next color. There are only two hundred fifty-six such rules."),
        ('H', "The authors take a random row of sixty-four cells, run a rule forty-eight times, and ask a transformer to predict the result from the starting row. One hundred million tokens of it."),
        ('H', "Rule fifteen makes simple, repeating patterns. The model learns them quickly. Little randomness, and little structure."),
        ('H', "Rule thirty looks like noise. The model makes no progress at all. Lots of time-bounded entropy, and essentially no epiplexity."),
        ('H', "Rule fifty-four makes complex patterns, little structures that travel and collide. Its loss keeps falling as compute grows. Some randomness, and a lot of structure."),
        ('H', "The same kind of tiny program, and the same compute, give nothing, or noise, or something worth learning."),
    ]),

    # ---------------------------------------------------------------- 7. paradox 2: order matters
    dict(title='Puzzle two: order matters', music=None, lines=[
        ('H', "Puzzle two. In both classic theories, the order you read things in doesn't change the total information."),
        ('H', "And yet, language models compress English better forward than reversed, an arrow of time. And cryptography is built on functions that are easy one way and hard the other."),
        ('H', "With a time limit, the paper proves that order can matter, assuming one-way functions exist. As a corollary, no efficient model that fits such a function forward can also obey Bayes' rule."),
        ('H', "The experiment uses rule thirty again, run for eight steps, as a stand-in for a one-way function. It's believed to be one, though nobody has proven it."),
        ('H', "Predict the output from the input, and the model reaches the true entropy. Predict the input from the output, and a gap remains, and widens as the rows get longer."),
        REST,
        ('H', "Then chess. The authors take a large collection of games from Lichess, an online chess site, and write each one two ways."),
        ('H', "Forward means the moves, then the final board. That part is easy to compute: you just play the moves."),
        ('H', "Reverse means the final board first, then the moves. Now the model has to work out how the game could have reached that board."),
        ('H', "As compute grows, the reverse order has both higher time-bounded entropy and higher epiplexity. It's harder to predict, and it teaches more structure. At small compute, the gap disappears."),
        ('H', "The same games, the same information in Shannon's sense, and different amounts learned. Keep that in mind. It comes back."),
    ]),

    # ---------------------------------------------------------------- 8. paradox 3: learning more than the source
    dict(title='Puzzle three: more than the source', music='sting', lines=[
        ('H', "Puzzle three. Training by likelihood just matches the process that made the data. So, the argument goes, a model can't learn more than went into making its data."),
        ('H', "The paper answers with two ideas: induction, and emergence."),
        ('H', "Induction first. The AI researcher Ilya Sutskever once put the idea like this. You're reading a murder mystery, and at some point the text reveals the criminal. If a model can predict the name, it must have figured out who did it from the evidence."),
        ('H', "But the author never had to make that deduction. They may have picked the murderer first, and written the story around them. The model has to do work the writer never did."),
        REST,
        ('H', "The authors build that gap in miniature. Take random bits, run rule thirty for four steps, and hide some of the starting bits from the model."),
        ('H', "To predict the output, the model has to infer the hidden bits. Its loss settles at exactly the number of hidden bits. But the compute it needs grows exponentially with how many are hidden, as if it's trying every possibility. And its measured epiplexity grows too."),
        ('H', "In a gentler version, sequences come from a random Markov chain with part of its transition table hidden. The model has to use the rules it's given, and infer the rest from the sequence itself."),
        ('H', "Epiplexity is highest when only part of the table is hidden, rather than all of it or none."),
        ('H', "In both cases, the model learns a strategy that was never part of the process that made the data."),
        REST,
        ('H', "Now emergence. Think of John Conway's Game of Life: a grid of cells, and one simple rule. An observer with unlimited compute just runs the rule, step by step."),
        ('H', "A bounded observer can't afford that. So it learns the creatures that emerge: blocks that sit still, oscillators that blink, gliders that travel, and guns that fire gliders, and what happens when they collide. That's a much longer program."),
        ('H', "The paper turns this into a definition of emergence. The authors say plainly that they haven't proven the Game of Life meets it."),
        ('H', "But they show the effect with rule fifty-four, and two transformers. One predicts the final row directly. The other, a looped model, can unroll the rule one step at a time, a bit like a chain of thought."),
        ('H', "At low compute, the direct model does better, and its epiplexity climbs as compute grows. It's learning more of the creatures."),
        ('H', "Then, past a threshold, the looped model takes over.", 0.5),
        ('H', "Its total code length drops abruptly, and so does the epiplexity. It has likely found the brute force answer: just run the rule."),
        ('H', "So with more compute, the structure went away. The whole zoo of creatures was what a limited observer needed."),
        ('H', "The authors add that this case is unusual. With natural data, they expect more compute to reveal more structure, not less."),
    ]),

    # ---------------------------------------------------------------- 9. what it says about data
    dict(title='What it says about data', music='sting', lines=[
        ('H', "So what does any of this say about the data we train on?"),
        ('H', "Start with chess. The authors fine-tune both models on two new tasks: solving chess puzzles, and judging who's ahead in a position, and by how much."),
        ('H', "On puzzles, the two orderings do about the same. On judging a position, the reverse-order model, the one with more epiplexity, does clearly better. The authors' reading is that it was forced to build a richer picture of the board."),
        REST,
        ('H', "Next, three kinds of data compared at the same budget: web text, chess games, and millions of tiny images in the style of a classic collection called CIFAR. Five billion tokens of each."),
        ('H', "In every case, epiplexity is a tiny fraction of the total. Web text has the most, then chess. The images hold the most information, but the least epiplexity: over ninety-nine percent of it is random, the exact value of each pixel."),
        ('H', "Then, using published scaling laws, they estimate much bigger cases: a trillion tokens, and enormous compute budgets."),
        ('H', "Language comes out with the most epiplexity, and images the least. Turning images into tokens with a learned codebook raises it a lot. And video has less than still images, probably because neighboring frames repeat each other."),
        ('H', "That's a candidate answer to a real puzzle. Why does training on text transfer so broadly, when training on images mostly doesn't?"),
        REST,
        ('H', "One more example. A method called ADO, for adaptive data optimization, steers training toward the data whose loss is falling fastest."),
        ('H', "In earlier experiments with a model of one point three billion parameters, ADO did a little better than ordinary sampling, on downstream tasks and on text from outside its training mix. And it had picked data with higher epiplexity."),
        ('H', "Faster learning means a bigger area under the curve."),
    ]),

    # ---------------------------------------------------------------- 10. honest limits
    dict(title="Where it's still shaky", music=None, lines=[
        ('H', "Now, honestly, where is this still on shaky ground?"),
        ('H', "First, the measuring. The easy method, the area under the curve, is a heuristic. The rigorous one is slower. They usually agree on rankings, but nothing guarantees it."),
        ('H', "And every estimate depends on how well the networks are tuned."),
        ('H', "Second, epiplexity measures how much structure there is, not whether it's useful for your task. The authors say this again and again. Higher epiplexity is not a promise of better transfer. The chess and data selection results are evidence, not proof."),
        ('H', "Third, the theorems rest on assumptions from cryptography, like the existence of one-way functions. Those are widely believed, and unproven. Rule thirty is only believed to be one-way. And the Game of Life hasn't been shown to be emergent in their sense."),
        ('H', "Fourth, the paper proves that data with growing epiplexity exist, but only growing slowly, like a logarithm. The big numbers come from measurements, not theorems."),
        ('H', "And one small thing: the data selection results are adapted from an earlier paper that shares an author with this one, and the gains there are modest."),
    ]),

    # ---------------------------------------------------------------- 11. close: the observer comes back
    dict(title='The observer comes back', music='sting', lines=[
        ('H', "Let's step back."),
        ('H', "In 1948, Shannon set meaning aside, on purpose, and that choice helped build the digital world."),
        ('H', "Epiplexity doesn't bring meaning back. It measures how much structure there is, not what that structure is about. But it brings back something Shannon and Kolmogorov left out: the observer, and the limits of what it can compute."),
        ('H', "And it flips a familiar question. The minimum description length principle asks, given this data, which model? Epiplexity asks, given this budget, which data?"),
        REST,
        ('H', "Here's the whole story, in brief."),
        ('H', "Shannon measures surprise, and the other classic theory measures the shortest program. Both assume unlimited compute, so both see a pseudorandom stream as nearly empty."),
        ('H', "Limit the observer's compute, and information splits in two. Time-bounded entropy is what still looks random. Epiplexity is the structure you can actually learn."),
        ('H', "With that split, computation can create information, order matters, and a model can learn more than went into making its data."),
        REST,
        ('H', "Here are a few things to sit with."),
        ('H?', "If information depends on who's looking, is there still a fact about how much information a book holds?"),
        ('H?', "Text beats images on this measure. Is that a fact about the world, or about our tokenizers and our models?"),
        ('H?', "If you were making synthetic data, how would you choose a transformation that creates structure, rather than just noise?"),
        ('H?', "And with rule fifty-four, more compute made the structure vanish. Is some of the structure we see in the world a sign of our own limits?"),
        ('H', "Back to where we started, with a program that learned chess from nothing but the rules.", 2.0),
        ('H', "The two classic theories seem to say it learned almost nothing. Put a limited observer back in the picture, and the answer changes. A short description of AlphaZero, and the result of running it for thousands of hours, are not the same thing. The computation is where the new information came from."),
        ('H', "Thanks for listening.", 1.0),
    ]),
]
