"""Short: seed. Facts: Thm 9 and §3 of arXiv:2601.03220v2 via projects/epiplexity/AGENTS.md; our compressor check
(data/ours_compress.json: SHA-256 counter mode, 7-byte seed, 1,048,576 bits; xz 1.0005 bits per bit, coin flips 1.0005)."""
VOICE = 'bella-nicole'
SPEED = 1.0

SCENES = [
    dict(scene='SeedStretch', headline='A million bits, one *seed*', hold=0.5, beats=[
        (0.3, "This screen holds a million random-looking bits, and they all grew from a seed of just seven bytes."),
        (7.0, "A hash function stretches it out, with no randomness added."),
    ]),
    dict(scene='SeedJudges', headline='Random to *whom*?', hold=2.4, beats=[
        (0.4, "So how much information is in it? Shannon says fifty-six bits, because only the seed was random."),
        (5.6, "Real compressors can't shrink it at all. In our check, it behaves just like coin flips."),
        (11.6, "And to a learner with limited compute, the paper's theorem says it's pure noise, with nothing to learn."),
        (18.0, "Same file, three answers. So is information in the data, or in whoever is looking?"),
    ]),
]
