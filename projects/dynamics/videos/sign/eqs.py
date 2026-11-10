"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Colour names below can be used as {\\color{G}...}; W is the default ink. Sources: Eq. 14 (AR), §3.1 (one head),
App. A.1 Eq. 30-32 (two heads) of arXiv:2512.21113v2."""
EQS = {
    'ar2': r'x(t{+}1) = {\color{Y}a_1}\,x(t) + {\color{Y}a_2}\,x(t{-}1)',
    'onehead': r'\hat x(t{+}1) = {\color{G}w_o}\,\big[\,{\color{F}\alpha}\,x(t) + ({\color{F}1-\alpha})\,x(t{-}1)\,\big]',
    'betas': r'{\color{Y}a_1} = {\color{F}\alpha}\,{\color{G}w_o} \qquad {\color{Y}a_2} = ({\color{F}1-\alpha})\,{\color{G}w_o}',
    'twohead': r'\hat x(t{+}1) = {\color{F}w_{o,1}}\,[\,\mathrm{head\ 1}\,] + {\color{C}w_{o,2}}\,[\,\mathrm{head\ 2}\,]',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
