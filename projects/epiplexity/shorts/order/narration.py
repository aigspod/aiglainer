"""Short: order. Facts: §5.2, Fig. 4b-c (fig4_owf_chess.json), §6.1 and Fig. 7 (fig7_chess_ood.json: puzzles 25.8% vs
25.9%, centipawn 21.0% vs 28.2%) via projects/epiplexity/AGENTS.md."""
VOICE = 'michael'
SPEED = 1.0

SCENES = [
    dict(scene='OrderTwoWays', headline='Same games, different *lesson*', hold=0.5, beats=[
        (0.3, "Can reading things in a different order change what you learn?"),
        (4.0, "Write a chess game as its moves, then the final board. Or flip it: the board first, then the moves."),
        (11.5, "For Shannon, the total information is the same either way."),
    ]),
    dict(scene='OrderData', headline='Same games, different *lesson*', hold=2.4, beats=[
        (0.3, "But to a model with limited compute, the reverse order holds more structure."),
        (7.5, "From the board, it has to work out how the game got there."),
        (12.5, "Then both were tuned on new tasks. On puzzles, they tie. At judging who has the advantage, the reverse model does clearly better."),
        (22.0, "If order changes what's learnable, how should we arrange our training data?"),
    ]),
]
