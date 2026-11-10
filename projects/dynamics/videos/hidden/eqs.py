"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Colour names below can be used as {\\color{G}...}; W is the default ink."""
EQS = {
    'vdp': r'\ddot{x} \;-\; {\color{Y}\mu}\,(1 - x^2)\,\dot{x} \;+\; x \;=\; 0',          # Eq. 23, §4.1
    'takens': r'n \;\ge\; 2\,{\color{Y}d} + 1',                                         # Eq. 19, §2.3
    'hsum': r'{\color{F}h_t} \;=\; e_t \;+\; {\color{G}z_t}',                            # §4.1, h_t = e_t + z_t
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
