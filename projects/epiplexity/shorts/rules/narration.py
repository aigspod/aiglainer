"""Short: rules. Facts: §5.1 and Fig. 3 of arXiv:2601.03220v2 (fig3_eca.json) via projects/epiplexity/AGENTS.md.
The automata are computed from the rules."""
VOICE = 'michael'
SPEED = 1.0

SCENES = [
    dict(scene='RulesGrow', headline='Three rules, three *fates*', hold=0.5, beats=[
        (0.3, "Here are three tiny rules, each short enough to fit on one line."),
        (5.0, "Rule fifteen just repeats. Rule thirty looks like static."),
        (9.2, "And rule fifty-four sends out gliders that travel and collide."),
    ]),
    dict(scene='RulesFig3', headline='Three rules, three *fates*', hold=2.4, beats=[
        (0.3, "The paper trained models to look forty-eight steps ahead, for each rule."),
        (5.6, "Rule fifteen is learned fast, and holds little."),
        (9.2, "Rule thirty stays random. The model never finds a pattern."),
        (13.2, "Rule fifty-four keeps paying off: more compute, more structure found."),
        (19.4, "Same tiny programs, wildly different information. What makes something worth learning?"),
    ]),
]
