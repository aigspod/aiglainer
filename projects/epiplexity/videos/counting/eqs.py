"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Notation follows arXiv:2601.03220v2 (§2, Def. 1, Def. 8). Colour names match aiglainer/core.py PAL."""
EQS = {
    'surprise': r'\text{surprise}(x) = \log_2 \frac{1}{p(x)}',
    'entropy': r'H(X) = \mathbb{E}\Big[\log_2 \frac{1}{p(X)}\Big]',
    'dpi': r'H\big(f(X)\big) \le H(X)',
    'sym': r'H(X) + H(Y \mid X) = H(Y) + H(X \mid Y)',
    'ml': r'\arg\min_{P}\; \mathbb{E}_{X \sim Q}\Big[\log \frac{1}{P(X)}\Big] = Q',
    'kolm': r'K(x) = \min \{\, |p| \;:\; U(p) = x \,\}',
    'invar': r'\big|\,K_{U_1}(x) - K_{U_2}(x)\,\big| \le C',
    'soph': r'\mathrm{soph}(x) \approx \min_{S} \{\, K(S) \;:\; x \text{ looks typical in } S \,\}',
    'mdl_a': r'P^\star = \arg\min_{P \,\in\, \mathcal{P}_T}',
    'mdl_b': r'{\color{Y}|P|}',
    'mdl_plus': r'+',
    'mdl_c': r'{\color{C}\mathbb{E}\Big[\log \frac{1}{P(X)}\Big]}',
    'st': r'{\color{Y}S_T(X) = |P^\star|}',
    'ht': r'{\color{C}H_T(X) = \mathbb{E}\big[\log 1/P^\star(X)\big]}',
    'kbits': r'K(\text{zeros}) \approx \log_2 n',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
