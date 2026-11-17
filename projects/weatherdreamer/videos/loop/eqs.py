"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Colours: Y amber (the learned parts / analysis), G blue (observations), F green (background / prior), C coral,
M muted. Sources: arXiv:2611.18393v1 Eq. 1-3 (classical DA), Eq. 4-7 (WeatherDreamer), Eq. 17 (prior matching);
the scalar gain is the textbook one-variable form of Eq. 2."""
EQS = {
    'kb':     r'{\color{F}x^{b}_{t}} = M\big(x^{a}_{t-1}\big)',
    'kgain':  r'K_t = B_t H^{\top}\big(H B_t H^{\top} + R_t\big)^{-1}',
    'ka':     r'{\color{Y}x^{a}_{t}} = {\color{F}x^{b}_{t}} + K_t\big({\color{G}y_t} - H({\color{F}x^{b}_{t}})\big)',
    'k1':     r'k = \frac{\sigma_B^2}{\sigma_B^2 + \sigma_O^2}',
    'wmem':   r'h_t = f_{\mathrm{dyn}}\big(h_{t-1},\, z^{*}_{t-1},\, f_t\big)',
    'wprior': r'{\color{F}\hat z_t} = p_\theta(h_t)',
    'wpost':  r'{\color{Y}z_t} = q_\phi(h_t,\, {\color{G}y_t})',
    'wdec':   r'{\color{G}\hat y^{m}_t} = D_m(z^{*}_t)',
    'lprior': r'\mathcal{L}_{\mathrm{prior}} = \sum_t \big\| {\color{F}\hat z_t} - \mathrm{sg}({\color{Y}z_t}) \big\|^2',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
