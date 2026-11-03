"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
All from Rautela & Scheinker, NAPAC2025 (arXiv:2602.22618). Colour names usable as {\\color{G}...}; W is the default ink."""
EQS = {
    # Background: the forward map and its factorisation (p. 2, "Forward Modeling")
    'hmap': r'X_t = H\big(X_1, X_2, \ldots, X_{t-1}\big)',
    'bayes': r'p({\color{Y}z}\,|\,X)\;\propto\;p(X\,|\,{\color{Y}z})\;p({\color{Y}z})',
    # Eq. (1) as printed: first-order form
    'eq1': r'P({\color{Y}z}_{0:T}) = P({\color{Y}z}_0)\prod_{t=1}^{T} P\big({\color{Y}z}_t \,|\, {\color{Y}z}_{t-1}\big)',
    # what the text says the model actually uses: the full chain rule, AR(1:T)
    'chain': r'P\big({\color{Y}z}_t \,|\, {\color{G}z_0, z_1, \ldots, z_{t-1}}\big)',
    # Inverse I: forward vs reversed latent sequences
    'fwd': r'{\color{Y}z}_0 \rightarrow {\color{Y}z}_1 \rightarrow \cdots \rightarrow {\color{Y}z}_T',
    'rev': r'{\color{C}z}_T \rightarrow {\color{C}z}_{T-1} \rightarrow \cdots \rightarrow {\color{C}z}_0',
    # Inverse II: VALeR regression (p. 3)
    'dag': r'X \;\rightarrow\; {\color{Y}z} \;\rightarrow\; {\color{F}y}',
    'reg': r'\mathcal{L}_{\mathrm{reg}} = \big|\,\hat{{\color{F}y}}({\color{Y}z}) - {\color{F}y}\,\big|^2',
    # Tuning (p. 3)
    'argy': r'{\color{F}y}^{*} = \arg\min_{{\color{F}y}\,\in\,\mathbb{R}^{p}} J({\color{F}y})',
    'argz': r'{\color{Y}z}^{*} = \arg\min_{{\color{Y}z}\,\in\,\mathbb{R}^{d}} J\big(g_\psi({\color{Y}z})\big), \quad d \ll p',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
