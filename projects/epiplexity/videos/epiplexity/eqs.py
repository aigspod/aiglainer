"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Colours: Y amber (structure, S_T), G blue (randomness, H_T), F green, C coral, X lilac, M muted, W ink (default).
Sources: Shannon 1948 (surprise, entropy, data processing); Def. 1 and §5.1 (Kolmogorov); Def. 8, eq. 3-4 (epiplexity);
eq. 8 (prequential), eq. 9 (requential); Thm 9; §5.2 (symmetry); §5.3 (likelihood); §6.3 (S_inf)."""
EQS = {
    'surprise': r'\text{surprise}(x) = \log_2 \frac{1}{p(x)}',
    'entropy':  r'H(X) = \mathbb{E}\Big[\log_2 \frac{1}{p(X)}\Big]',
    'dpi':      r'H\big(f(X)\big) \;\le\; H(X)',
    'kdef':     r'K(x) = \min\{\, |p| \;:\; U(p) = x \,\}',
    'kf':       r'K\big(f(x)\big) \;\le\; K(x) + K(f) + c',
    'pstar':    r'P^\star = \operatorname*{arg\,min}_{P\,\in\,\mathcal{P}_{\color{Y}T}} \; {\color{Y}|P|} \;+\; {\color{G}\mathbb{E}\Big[\log \frac{1}{P(X)}\Big]}',
    'st':       r'{\color{Y}S_T(X) = |P^\star|}',
    'ht':       r'{\color{G}H_T(X) = \mathbb{E}\Big[\log \frac{1}{P^\star(X)}\Big]}',
    'ST':       r'{\color{Y}S_T}',
    'HT':       r'{\color{G}H_T}',
    'preq':     r'|P_{\mathrm{preq}}| \approx \sum_{i} \Big( \log \frac{1}{P_i(Z_i)} - \log \frac{1}{P_M(Z_i)} \Big)',
    'req':      r'|P_{\mathrm{req}}| \approx \sum_{i} \mathrm{KL}\big(P^{\,t}_i \,\big\|\, P^{\,s}_i\big)',
    'thm9':     r'{\color{G}H_{\mathrm{poly}}\big(G(U_k)\big) > n - 2 - n\varepsilon} \qquad {\color{Y}S_{\mathrm{poly}}\big(G(U_k)\big) \le c + n\varepsilon}',
    'sym':      r'H(X) + H(Y\,|\,X) \;=\; H(Y) + H(X\,|\,Y)',
    'mle':      r'\operatorname*{arg\,min}_{P}\; \mathbb{E}_{X\sim Q}\big[-\log P(X)\big] \;=\; Q',
    'twopart':  r'{\color{Y}|P|} \;+\; {\color{G}\mathbb{E}\big[\log 1/P(X)\big]}',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', X='C3A6D8', M='AAA0AD')
