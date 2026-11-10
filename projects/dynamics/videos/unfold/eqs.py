"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Sources: Eq. 24 (Chafee-Infante), Eq. 25 (three sine modes), Eq. 11 (effective latent), Takens bound (§4.2)."""
EQS = {
    'ci': r'u_t = u - u^3 + \nu\, u_{xx}',
    'modes': r'u \approx {\color{Y}\varphi_1}\sin x + {\color{G}\varphi_2}\sin 2x + \varphi_3 \sin 3x',
    'h': r'{\color{Y}h_t} = e_t + z_t',
    'takens': r'n \;\ge\; 2\,{\color{F}d} + 1 \;=\; 5',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
