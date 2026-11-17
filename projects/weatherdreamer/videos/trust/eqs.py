"""Equations, typeset by `make tex` into tex/<key>.png and drawn with tex(c, key, x, y, size).
Sources: Eq. 2-3 (Kalman gain, analysis update); Text S6.10 (Desroziers estimate, gain regression); §3.3 (excess air
mass). The 0.8 is the thermometer illustration in the Gain scene."""
EQS = {
    'gain':     r'k \;=\; \frac{{\color{G}\sigma_B^2}}{{\color{G}\sigma_B^2} + {\color{C}\sigma_O^2}}',
    'gainnum':  r'=\; \frac{1^2}{1^2 + 0.5^2} \;=\; {\color{Y}0.8}',
    'update':   r'{\color{Y}x_a} \;=\; {\color{G}x_b} + k\,\big({\color{C}y} - {\color{G}x_b}\big)',
    'desroz':   r'{\color{C}\sigma_O^2} \;\approx\; \mathrm{cov}\big(O - A,\; O - B\big)',
    'kreg':     r'k \;=\; \frac{\mathrm{cov}(A - B,\; O - B)}{\mathrm{var}(O - B)}',
    'airmass':  r'\ell \;=\; \sec\theta - 1',
}
COLORS = dict(W='EFE5D6', Y='E3A75A', G='5AA6EC', F='45C99A', C='F07A4F', M='AAA0AD')
