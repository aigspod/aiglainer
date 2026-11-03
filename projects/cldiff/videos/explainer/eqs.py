"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
All from Scheinker & Williams, arXiv:2502.18684 (equation numbers as in the paper). W is the default ink."""
EQS = {
    # Eq. (2): surviving beam current at module m, from the (z, pz) projection
    'bm': r'b_m = \int_z\!\int_{p_z} \rho^m(z, p_z)\, dp_z\, dz',
    # Eq. (13): the overall mapping, c = [settings, currents, which projection, module]
    'map': r'\mathbf{c} = [{\color{F}\mathbf{p}}, {\color{G}\mathbf{b}}, {\color{Y}\mathbf{d}}, {\color{C}m}] \;\longrightarrow\; \rho^m_j',
    # VAE loss: Eq. (9)
    'vae': r'C = R + w\,KL, \qquad w < 1',
    # Diffusion: Eq. (15), one-shot noising
    'noise': r'z_k = \sqrt{\alpha_k}\, z + \sqrt{1-\alpha_k}\, \epsilon, \qquad \epsilon \sim \mathcal{N}(0, I)',
    # Adaptive: Eqs. (21), (22), (23)
    'cost': r'C(\tau, \mathbf{c}) = \big\| \hat{P}\hat{X}(\mathbf{c}, \tau) - P X(\tau) \big\|',
    'es': r'\dot{c}_j = \sqrt{\alpha\,\omega_j}\, \cos\!\big[\omega_j \tau + k\, C(\tau, \mathbf{c})\big]',
    'grad': r'\dot{\mathbf{c}} \approx -\tfrac{k\alpha}{2}\, \nabla_{\mathbf{c}} C',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
