"""Room to unfold: latent room and parameters. §4.2 and App. A.4 (Chafee-Infante), §4.3 and App. A.5 (cylinder flow),
§5.1 (one-step accuracy vs latent identifiability) of arXiv:2512.21113v2. Numbers via projects/dynamics/AGENTS.md.

Data: data/ci.json is OUR Chafee-Infante simulation (simulate.py), labelled on screen. Cylinder numbers are typed from
§4.3 / App. A.5 (CYL_RECON in dynkit). Latent pictures, loops, error shapes and the wake are illustrations, labelled."""
from dynkit import *
from dynkit import _axes_draw

# ---------------------------------------------------------------- local drawing pieces
def arc_pts(cx, cy, r, a0, a1, n=28):
    th = np.linspace(a0, a1, n)
    return np.stack([cx + r * np.cos(th), cy + r * np.sin(th)], 1)

def wake(c, x, y, w, h, t, a=1.0, err=0.0, sensor=1.0, speed=1.0):
    """ILLUSTRATION of vortex shedding behind a cylinder in a channel (not data). err tints the wake coral;
    sensor fades in an amber probe. Returns the sensor position."""
    if a <= 0:
        return (0, 0)
    rrect(c, x, y, w, h, 14, fill='panel', a=a, fa=a * 0.55)
    rrect(c, x, y, w, h, 14, stroke='line', sw=1.4, a=a)
    cx, cy, r = x + w * 0.15, y + h / 2, h * 0.13
    # streamlines that start to wave behind the cylinder
    for j in range(7):
        y0 = y + h * (j + 0.5) / 7
        xs = np.linspace(x + 12, x + w - 12, 90)
        grow = np.clip((xs - cx) / (w * 0.25), 0, 1)
        near = np.exp(-((y0 - cy) / (h * 0.35)) ** 2)
        ys = y0 + grow * near * h * 0.07 * np.sin((xs - cx) / (w * 0.12) * 2 * np.pi - t * 2.4 * speed + j * 0.4)
        bump = np.exp(-((xs - cx) / (r * 1.6)) ** 2) * np.sign(y0 - cy) * r * 0.9 * np.exp(-((y0 - cy) / (r * 2.2)) ** 2)
        draw_poly(c, np.stack([xs, ys + bump], 1), 'line', a, 1.4)
    if err > 0:
        for i in range(5):
            ex = cx + r * 2 + (w * 0.62) * (i + 0.5) / 5
            circle(c, ex, cy, h * 0.16, fill='c', a=a * err * 0.22, glow=26)
    # the vortex street: alternating spinning eddies, carried downstream
    lam = w * 0.17
    phase = (t * 0.11 * speed * w) % lam
    k = 0
    while True:
        vx = cx + r * 1.6 + phase + k * lam / 2
        if vx > x + w - h * 0.12:
            break
        up = k % 2 == 0
        vy = cy + (-1 if up else 1) * h * 0.13
        rv = h * (0.05 + 0.06 * min(1, (vx - cx) / (w * 0.5)))
        fade = clamp((x + w - h * 0.12 - vx) / (w * 0.1)) * clamp((vx - cx - r) / (w * 0.06))
        spin = t * 3.0 * (1 if up else -1)
        colr = 'g' if up else 'x'
        draw_poly(c, arc_pts(vx, vy, rv, spin, spin + 4.4), colr, a * fade * 0.9, 2.4)
        draw_poly(c, arc_pts(vx, vy, rv * 0.55, spin + 1.5, spin + 5.4), colr, a * fade * 0.7, 2.0)
        k += 1
    circle(c, cx, cy, r, fill='panel2', a=a)
    circle(c, cx, cy, r, stroke='muted', sw=2, a=a)
    sx, sy = x + w * 0.52, y + h * 0.40
    if sensor > 0:
        circle(c, sx, sy, 9, fill='y', a=a * sensor, glow=10)
        circle(c, sx, sy, 16, stroke='y', sw=1.6, a=a * sensor * 0.6)
    return (sx, sy)

def sheet3d(c, cx, cy, s, ang, a=1.0, n=13, prog=1.0):
    """ILLUSTRATION: an unfolded, gently curved sheet in a 3-D latent, slowly turning. Lines coloured across u."""
    if a <= 0:
        return
    tilt = 0.55
    def P(u, v):
        X, Y, Z = u, v, 0.32 * np.sin(1.7 * u) + 0.12 * v * v
        xr = X * math.cos(ang) - Y * math.sin(ang)
        yr = X * math.sin(ang) + Y * math.cos(ang)
        return np.stack([cx + s * xr, cy - s * (Z * math.cos(tilt) + yr * math.sin(tilt))], 1)
    g = np.linspace(-1, 1, 60)
    for i in range(n):
        u = -1 + 2 * i / (n - 1)
        k = clamp(prog * n - i)
        if k <= 0:
            continue
        draw_poly(c, P(np.full_like(g, u), g), mix('g', 'y', i / (n - 1)), a * k * 0.95, 2.2)
    for j in range(0, n, 3):
        v = -1 + 2 * j / (n - 1)
        draw_poly(c, P(g, np.full_like(g, v)), 'muted', a * 0.35 * prog, 1.2)

class Thick:
    """ILLUSTRATION: a 2-D surface squashed into a thick curve; colours (the second coordinate) land on top of each
    other. Deterministic points."""
    def __init__(self, n=900, seed=5):
        rng = np.random.default_rng(seed)
        self.s = rng.uniform(0, 1, n)
        self.q = rng.uniform(0, 1, n)
        self.j = rng.normal(0, 1, n)

    def draw(self, c, x, y, w, h, t, t0, a=1.0):
        k = ramp(t, t0, 0.6) * a
        if k <= 0:
            return
        line(c, x, y + h, x + w, y + h, 'muted', k, 1.4)
        line(c, x, y, x, y + h, 'muted', k, 1.4)
        text(c, 'h₁', x + w, y + h + 32, 22, 500, 'muted', k, 'right')
        text(c, 'h₂', x - 12, y + 10, 22, 500, 'muted', k, 'right')
        pr = ramp(t, t0 + 0.3, 1.6, e_io)
        for s, q, j in zip(self.s, self.q, self.j):
            if s > pr:
                continue
            X = x + w * (0.08 + 0.84 * s)
            Y = y + h * (0.5 - 0.3 * math.sin(2 * math.pi * s * 0.9 + 0.4)) + j * h * 0.045
            circle(c, X, Y, 3.6, fill=mix('g', 'y', q), a=k * 0.8)

def re_axis(c, x, w, y, t, t0, a=1.0, fs=19, labels=True):
    """The Reynolds-number line of §4.3: 100 to 750, training band 125-725, six test values inside, three outside."""
    X = lambda re: x + (re - 100) / 650 * w
    k = ramp(t, t0, 0.7) * a
    if k <= 0:
        return X
    kb = ramp(t, t0 + 0.3, 0.8, e_io) * a
    rrect(c, X(125), y - 22, (X(725) - X(125)) * kb, 44, 8, fill='f', a=k, fa=k * 0.16)
    line(c, x, y, x + w * ramp(t, t0, 0.9, e_io), y, 'muted', k, 1.8)
    for re in (100, 200, 300, 400, 500, 600, 700):
        line(c, X(re), y - 8, X(re), y + 8, 'muted', k, 1.4)
        if labels:
            text(c, str(re), X(re), y + 34 + fs * 0.4, fs, 500, 'muted', k, 'center', kind='mono')
    if labels:
        text(c, 'training: Re 125 to 725', X(425), y - 36, fs, 600, 'f', kb, 'center', kind='mono')
    for i, re in enumerate((133, 233, 333, 433, 533, 633)):
        kk = ramp(t, t0 + 1.2 + i * 0.12, 0.4, e_back) * a
        circle(c, X(re), y, 9 * min(kk, 1.2), fill='g', a=min(kk, 1), glow=6)
    for i, re in enumerate((100, 733, 750)):
        kk = ramp(t, t0 + 2.0 + i * 0.15, 0.4, e_back) * a
        circle(c, X(re), y, 9 * min(kk, 1.2), fill='c', a=min(kk, 1), glow=6)
    return X

def bracket_label(c, x, y, s, colr, a, size=18):
    text(c, s, x, y, size, 600, colr, a, kind='mono')

# ---------------------------------------------------------------- scenes
class ColdOpen(Scene):
    dur = 22.0
    fade_in = 0.3
    cues = [(0.4, 'whoosh_soft'), (12.2, 'pop'), (13.4, 'pop')]

    def draw(self, c, t):
        kicker(c, 'two small transformers  ·  one sensor  ·  the same flow', W / 2, 200, ramp(t, 0.4, 0.8), 'muted', 18, align='center')
        for i, (name, val, colr) in enumerate((('model A', CYL_RECON[0][1], 'f'), ('model B', CYL_RECON[0][2], 'c'))):
            x = 150 + i * 840
            k = ramp(t, 0.5 + i * 0.4, 0.8, e_expo)
            if k <= 0:
                continue
            with layer(c, k):
                panel(c, x, 250, 780, 640)
                kicker(c, name, x + 36, 300, 1, 'muted', 18)
                wake(c, x + 36, 330, 708, 230, t, 1, err=(ramp(t, 13.4, 1.0) if i else 0), sensor=ramp(t, 1.6, 0.6))
                kp = ramp(t, 3.4 + i * 0.3, 0.6)
                text(c, 'predicts the next reading', x + 36, 625, 28, 500, 'ink', kp)
                text(c, '✓', x + 744, 625, 32, 700, 'f', kp, 'right')
                kr = ramp(t, 7.0 + i * 0.3, 0.6)
                text(c, 'rebuilds the whole vₓ field', x + 36, 700, 28, 500, 'ink', kr)
                kv = ramp(t, 12.0 + i * 1.2, 0.7, e_expo)
                if kv > 0:
                    text(c, sci(val, 2), x + 36, 800, 60, 700, colr, kv, tracking=-0.01)
                    text(c, 'error over the field', x + 744, 800, 20, 500, 'muted', kv, 'right', kind='mono')
        k70 = ramp(t, 13.6, 0.6, e_back)
        if k70 > 0:
            text(c, '≈ 70× worse', 1734, 712, 40, 700, 'c', min(k70, 1), 'right')
        note(c, 'largest one-step error across both ≈ 2.3 × 10⁻²  (§4.3)  ·  field errors: App. A.5  ·  wakes: illustration',
             W / 2, 930, ramp(t, 4.5, 0.6), 17, 'muted', 'center')
        caption(c, t, 'Both {y:forecast well}, very different {c:on the inside}.', 17.0, None, y=1000, size=40)

class Title(TitleCard):
    TITLE = 'Room to *unfold*'
    STICKY = ['latent room', '& parameters']

def signal(n=26):
    """ILLUSTRATION: a smooth oscillating sensor signal, sampled."""
    ts = np.arange(n) * 0.5
    return ts, 0.9 * np.sin(ts * 0.9) + 0.3 * np.sin(ts * 1.9 + 0.8)

class Latent(Scene):
    dur = 31.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (4.6, 'pop'), (8.2, 'draw'), (19.8, 'pop'), (24.6, 'chime')]

    def __init__(self):
        self.ts, self.xs = signal()

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the latent', 'One sensor, one *latent* state')
        ax = Axes(150, 420, 560, 240, (self.ts[0], self.ts[-1]), (-1.45, 1.45))
        k = ramp(t, 0.5, 0.6)
        P = ax.pts(self.ts, self.xs)
        pr = ramp(t, 0.6, 2.4, e_lin)
        n_on = int(len(P) * pr)
        if k > 0:
            circle(c, 162, 380, 8, fill='y', a=k, glow=8)
            text(c, 'one sensor, one number per step', 182, 387, 20, 500, 'ink', k, kind='mono')
            line(c, 150, 660, 710, 660, 'muted', k, 1.4)
            if n_on >= 2:
                draw_poly(c, P[:n_on], 'g', k * 0.8, 2.4)
            for p in P[:n_on]:
                circle(c, p[0], p[1], 4, fill='g', a=k * 0.75)
            illustration(c, 150, 700, k)
        # the last five readings, boxed, then stacked as tokens
        kw = ramp(t, 4.5, 0.6, e_expo)
        idx = list(range(len(P) - 5, len(P)))
        if kw > 0:
            x0b, x1b = P[idx[0]][0] - 14, P[idx[-1]][0] + 14
            rrect(c, x0b, 404, x1b - x0b, 272, 12, fill='y', a=kw, fa=kw * 0.08)
            rrect(c, x0b, 404, x1b - x0b, 272, 12, stroke='y', sw=1.8, a=kw)
            text(c, 'last 5', (x0b + x1b) / 2, 394, 18, 500, 'y', kw, 'center', kind='mono')
            for i in idx:
                circle(c, P[i][0], P[i][1], 7, fill='y', a=kw, glow=6)
        tok_y = []
        for j, i in enumerate(reversed(idx)):
            kk = ramp(t, 5.0 + j * 0.1, 0.4)
            yy = 395 + j * 58
            tok_y.append(yy + 25)
            if kk <= 0:
                continue
            rrect(c, 770, yy, 112, 50, 9, fill='panel', a=kk, fa=kk * 0.85)
            rrect(c, 770, yy, 112, 50, 9, stroke='y', sw=1.5, a=kk)
            text(c, f'{self.xs[i]:+.2f}'.replace('-', '−'), 826, yy + 33, 20, 600, 'ink', kk, 'center', kind='mono')
            text(c, 'x(t)' if j == 0 else f'x(t−{j})', 894, yy + 32, 17, 400, 'muted', kk, kind='mono')
        # attention box
        ka = ramp(t, 8.0, 0.7, e_expo)
        if ka > 0:
            pa = ramp(t, 8.0, 0.8, e_io)
            for yy in tok_y:
                line(c, 965, yy, lerp(965, 1020, pa), lerp(yy, 515, pa), 'y', ka * 0.5, 1.6)
            panel(c, 1020, 440, 200, 150, ka)
            text(c, 'attention', 1120, 510, 32, 400, 'ink', ka, 'center', kind='italic')
            text(c, 'mixes the tokens', 1120, 552, 16, 500, 'muted', ka, 'center', kind='mono')
        # latent slots
        kl = ramp(t, 9.5, 0.7, e_expo)
        room3 = ramp(t, 20.6, 0.7, e_expo)
        if kl > 0:
            arrow(c, 1226, 515, 1278, 515, 'muted', kl, 2.2, 10, prog=ramp(t, 9.5, 0.5))
            text(c, 'latent h', 1350, 400, 22, 600, 'y', kl, 'center', kind='mono')
            for s in range(3):
                kk = kl if s < 2 else room3
                if kk <= 0:
                    continue
                yy = 420 + s * 66
                rrect(c, 1290, yy, 120, 56, 10, fill='y', a=kk, fa=kk * 0.14)
                rrect(c, 1290, yy, 120, 56, 10, stroke='y', sw=1.8, a=kk, glow=4)
                text(c, f'h{"₁₂₃"[s]}', 1350, yy + 38, 28, 600, 'ink', kk, 'center')
            tex(c, 'h', 1350, 660, 40, ramp(t, 11.0, 0.7))
            note(c, 'newest token + attention (Eq. 11)', 1350, 708, ramp(t, 11.4, 0.7), 15, 'muted', 'center')
        # network and next reading
        kn = ramp(t, 15.0, 0.7, e_expo)
        if kn > 0:
            arrow(c, 1416, 515, 1460, 515, 'muted', kn, 2.2, 10, prog=ramp(t, 15.0, 0.5))
            panel(c, 1466, 460, 150, 110, kn)
            text(c, 'network', 1541, 522, 24, 400, 'ink', kn, 'center', kind='italic')
            arrow(c, 1622, 515, 1664, 515, 'muted', kn, 2.2, 10, prog=ramp(t, 15.3, 0.5))
            rrect(c, 1670, 488, 120, 56, 10, fill='panel', a=kn, fa=kn * 0.85)
            rrect(c, 1670, 488, 120, 56, 10, stroke='g', sw=1.6, a=kn)
            text(c, 'x(t+1)', 1730, 524, 20, 600, 'g', kn, 'center', kind='mono')
            text(c, 'next reading', 1730, 585, 16, 500, 'muted', kn, 'center', kind='mono')
        # room = latent size
        kr = ramp(t, 19.5, 0.7)
        if kr > 0:
            rrect(c, 1270, 380 + 0, 160, 230 if room3 > 0 else 164, 14, stroke='y', sw=1.4, a=kr * 0.6)
            hand(c, 'room: 2 or 3 numbers', 1240, 780, 34, 'pencil', kr, -2.0, ramp(t, 19.6, 1.0, e_lin))
        # Takens
        kt = ramp(t, 24.5, 0.8, e_expo)
        if kt > 0:
            with layer(c, kt):
                panel(c, 150, 790, 980, 150)
                kicker(c, 'delay embedding (takens)', 186, 832, 1, 'muted', 16)
                tex(c, 'takens', 186, 895, 44, 1, align='left')
                rich(c, 'readings, for a {f:2-D} surface', 590, 902, 28, 520, t, 25.0, 0.03, 0.4)

class Rod(Scene):
    dur = 27.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (10.2, 'draw'), (16.2, 'pop')]

    def __init__(self):
        d = load_json('ci.json')['rod']
        self.x = np.array(d['x'])
        self.T = np.array(d['t'])
        self.u = np.array(d['u'])
        self.u10 = np.array(d['u10'])
        self.x10 = load_json('ci.json')['x10']

    def draw(self, c, t):
        hdr(self, c, t, '02', 'test 1 · chafee–infante', 'A rod that *settles*')
        k = ramp(t, 0.6, 0.7)
        tex(c, 'ci', 1460, 380, 52, ramp(t, 0.8, 0.8), reveal=ramp(t, 0.8, 1.2, e_io))
        note(c, 'ν = 0.16  ·  u = 0 at both ends  (Eq. 24)', 1460, 440, ramp(t, 1.4, 0.6), 17, 'muted', 'center')
        # the rod
        X0, X1, Y0, S = 170, 1010, 560, 165
        kr = ramp(t, 4.0, 0.7)
        dt_ = clamp((t - 4.6) * 1.3, 0, self.T[-1] * 0.82)
        i = int(round(dt_ / (self.T[1] - self.T[0])))
        if kr > 0:
            line(c, X0, Y0, X1, Y0, 'faint', kr, 1.4, dash=[6, 6])
            for xx in (X0, X1):
                rrect(c, xx - 6, Y0 - 40, 12, 80, 4, fill='muted', a=kr, fa=kr * 0.8)
            text(c, '0', X0, Y0 + 72, 18, 500, 'muted', kr, 'center', kind='mono')
            text(c, 'π', X1, Y0 + 72, 18, 500, 'muted', kr, 'center', kind='mono')
            text(c, 'position x along the rod', (X0 + X1) / 2, 830, 18, 500, 'muted', kr, 'center', kind='mono')
            px = X0 + self.x / np.pi * (X1 - X0)
            py = Y0 - self.u[i] * S
            draw_poly(c, np.stack([px, py], 1), 'g', kr, 3.5, glow=6)
            text(c, 'u(x, t)', X1 - 10, Y0 - 230, 20, 600, 'g', kr, 'right', kind='mono')
            sim_label(c, X0, 905, kr, extra='three sine modes')
        # sensor
        ks = ramp(t, 4.6, 0.6)
        sxp = X0 + self.x10 / np.pi * (X1 - X0)
        sy = Y0 - self.u10[i] * S
        if ks > 0:
            circle(c, sxp, sy, 9, fill='y', a=ks, glow=10)
        kl = ramp(t, 16.0, 0.6)
        if kl > 0:
            hand_arrow(c, 230, 352, sxp - 4, sy - 16, 'y', kl, ramp(t, 16.0, 0.7), -0.3)
            text(c, 'one sensor: the 10th of 256 points, x ≈ 0.11', 170, 336, 22, 600, 'y', kl, kind='mono')
        # what the sensor sees
        kt = ramp(t, 5.0, 0.6)
        if kt > 0:
            ax = Axes(1160, 520, 620, 200, (0, self.T[-1] * 0.82), (-0.2, 0.2))
            _axes_draw(ax, c, kt, (), (-0.2, 0, 0.2), 17, '{:.1f}', '{:g}', True, 1)
            text(c, 'what the sensor sees', 1160, 500, 18, 500, 'y', kt, kind='mono')
            text(c, 'time', 1780, 760, 17, 500, 'muted', kt, 'right', kind='mono')
            m = self.T <= dt_
            if m.sum() >= 2:
                draw_poly(c, ax.pts(self.T[m], self.u10[m]), 'y', kt, 3, glow=4)
        # the long-run surface
        kc = ramp(t, 10.0, 0.8, e_expo)
        if kc > 0:
            with layer(c, kc):
                panel(c, 1120, 830, 680, 140)
                rich(c, 'long run: a {y:2-D surface} in three sine-wave amplitudes', 1150, 876, 24, 640, t, 10.3, 0.03, 0.4)
                tex(c, 'modes', 1460, 930, 34, ramp(t, 11.0, 0.7))
        kf = ramp(t, 16.6, 0.7, e_back)
        if kf > 0:
            pill(c, 1160, 768, '5 readings  ≥  2 × 2 + 1', 'f', min(kf, 1), size=17)

class Fold(Scene):
    dur = 27.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (7.6, 'sweep'), (13.8, 'pop')]

    def __init__(self):
        d = load_json('ci.json')
        self.br = [(b['kind'], b['half'], np.array(b['phi']), np.array(b['delay'])) for b in d['branches']]
        # the highlighted pair: an upper-half point and the lower-half point that lands nearest it in the delay view,
        # chosen to be far apart in the true coordinates (computed, not picked by eye)
        U = np.concatenate([np.hstack([p, q]) for kd, h, p, q in self.br if h > 0])
        L = np.concatenate([np.hstack([p, q]) for kd, h, p, q in self.br if h < 0])
        U, L = U[U[:, 1] > 0.2][::2], L[L[:, 1] < -0.2][::2]          # clearly inside each half
        dd = np.linalg.norm(U[:, None, 2:] - L[None, :, 2:], axis=2)
        dp = np.linalg.norm(U[:, None, :2] - L[None, :, :2], axis=2)
        score = np.where(dp > 0.8, dp / (dd + 2e-3), 0)
        i, j = np.unravel_index(np.argmax(score), score.shape)
        self.pair = (U[i], L[j])

    def draw(self, c, t):
        hdr(self, c, t, '03', 'test 1 · the fold', 'Symmetry *folds* the view')
        colr = {1: 'y', -1: 'g'}
        # true coordinates
        k = ramp(t, 0.6, 0.7)
        A = Axes(170, 380, 700, 470, (-1.3, 1.3), (-0.87, 0.87))
        if k > 0:
            text(c, 'true coordinates', 170, 360, 20, 600, 'ink', k, kind='mono')
            X0, Y0 = A.px(0, 0)
            line(c, A.x, Y0, A.x + A.w, Y0, 'faint', k, 1.2)
            line(c, X0, A.y, X0, A.y + A.h, 'faint', k, 1.2)
            text(c, 'φ₁', A.x + A.w + 10, Y0 + 8, 22, 500, 'muted', k)
            text(c, 'φ₂', X0 + 12, A.y + 14, 22, 500, 'muted', k)
            pr = ramp(t, 1.0, 2.0, e_io)
            for kd, h, p, q in self.br:
                draw_poly(c, A.pts(p[:, 0], p[:, 1]), colr[h], k * (0.95 if kd == 'edge' else 0.55), 3.4 if kd == 'edge' else 1.4, pr)
            kh = ramp(t, 3.0, 0.6)
            text(c, 'upper half', A.px(-0.62, 0)[0] - 14, A.px(0, 0.5)[1], 20, 600, 'y', kh, 'right')
            text(c, 'lower half', A.px(-0.62, 0)[0] - 14, A.px(0, -0.5)[1] + 14, 20, 600, 'g', kh, 'right')
            note(c, 'mirror image through zero', A.x + A.w, A.y + A.h + 64, kh, 16, 'muted', 'right')
        # the sensor's two-reading view
        kd_ = ramp(t, 7.5, 0.7)
        B = Axes(1180, 380, 470, 470, (-0.2, 0.2), (-0.2, 0.2))
        if kd_ > 0:
            arrow(c, 920, 730, 1120, 730, 'y', kd_, 2.4, 12, prog=ramp(t, 7.5, 0.7, e_io))
            text(c, 'one sensor', 1020, 710, 18, 600, 'y', kd_, 'center', kind='mono')
            text(c, 'two readings', 1020, 765, 18, 500, 'muted', kd_, 'center', kind='mono')
            text(c, 'what one sensor sees', 1180, 360, 20, 600, 'ink', kd_, kind='mono')
            rrect(c, B.x, B.y, B.w, B.h, 6, stroke='line', sw=1.4, a=kd_)
            X0, Y0 = B.px(0, 0)
            line(c, B.x, Y0, B.x + B.w, Y0, 'faint', kd_, 1.2)
            line(c, X0, B.y, X0, B.y + B.h, 'faint', kd_, 1.2)
            text(c, 'u(t − τ)', B.x + B.w, B.y + B.h + 30, 18, 500, 'muted', kd_, 'right', kind='mono')
            text(c, 'u(t)', B.x - 10, B.y + 14, 18, 500, 'muted', kd_, 'right', kind='mono')
            pr = ramp(t, 8.2, 2.0, e_io)
            for kd, h, p, q in self.br:
                draw_poly(c, B.pts(q[:, 0], q[:, 1]), colr[h], kd_ * (0.95 if kd == 'edge' else 0.55), 3.0 if kd == 'edge' else 1.4, pr)
        sim_label(c, 170, 950, max(k, kd_), extra='three sine modes, sensor at x ≈ 0.11, τ = 4/9')
        # far apart -> nearly touching
        kp = ramp(t, 13.5, 0.6, e_back)
        if kp > 0:
            u, l = self.pair
            kk = min(kp, 1)
            pa, pb = A.px(u[0], u[1]), A.px(l[0], l[1])
            line(c, pa[0], pa[1], pb[0], pb[1], 'ink', kk * 0.7, 1.6, dash=[6, 6])
            for (p, cc) in ((pa, 'y'), (pb, 'g')):
                circle(c, p[0], p[1], 10 * min(kp, 1.2), fill=cc, a=kk, glow=10)
                circle(c, p[0], p[1], 16, stroke='ink', sw=1.6, a=kk * 0.8)
            qa, qb = B.px(u[2], u[3]), B.px(l[2], l[3])
            for (p, cc) in ((qa, 'y'), (qb, 'g')):
                circle(c, p[0], p[1], 9 * min(kp, 1.2), fill=cc, a=kk, glow=10)
            circle(c, (qa[0] + qb[0]) / 2, (qa[1] + qb[1]) / 2, 24, stroke='ink', sw=1.6, a=kk * 0.8)
            mx_, my_ = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
            text(c, 'far apart', mx_ + 10, my_ - 34, 22, 700, 'ink', kk, 'center')
            text(c, 'nearly touch', (qa[0] + qb[0]) / 2 + 34, (qa[1] + qb[1]) / 2 + 30, 22, 700, 'ink', kk)
        caption(c, t, 'In principle, the information is still in {y:five readings}. The model has to {y:pull it apart}.', 20.0, None, y=1010, size=30)

class Room(Scene):
    dur = 30.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (3.2, 'draw'), (15.7, 'sweep')]

    def __init__(self):
        self.thick = Thick()

    def draw(self, c, t):
        hdr(self, c, t, '04', 'test 1 · latent room', 'Two numbers or *three*', sub='Chafee–Infante, one sensor, five readings, ten training seeds each (§4.2, Fig. 8–9)')
        kq = ramp(t, 0.6, 0.6) * (1 - ramp(t, 2.6, 0.4))
        if kq > 0:
            rich(c, 'how many latent numbers does it take to {y:unfold} the surface?', W / 2, 640, 40, 1500, t, 0.6, 0.03, 0.4, kq, 'center')
        # latent of 2
        k = ramp(t, 3.0, 0.7, e_expo)
        if k > 0:
            with layer(c, k):
                panel(c, 120, 360, 800, 560)
                kicker(c, 'a latent of 2 numbers', 156, 405, 1, 'c', 18)
            self.thick.draw(c, 200, 450, 640, 270, t, 3.2)
            illustration(c, 884, 405, k, align='right')
            text(c, 'collapses into a thick curve', 156, 790, 28, 600, 'ink', ramp(t, 4.5, 0.6))
            rich(c, 'unstable across seeds · some runs {c:worse than the MLP alone}', 156, 840, 24, 740, t, 8.6, 0.03, 0.4, base='muted')
        # latent of 3
        k3 = ramp(t, 15.5, 0.7, e_expo)
        if k3 > 0:
            with layer(c, k3):
                panel(c, 1000, 360, 800, 560)
                kicker(c, 'a latent of 3 numbers', 1036, 405, 1, 'f', 18)
            sheet3d(c, 1400, 600, 172, 0.55 + 0.35 * math.sin(0.35 * t), k3, prog=ramp(t, 15.7, 1.6, e_io))
            illustration(c, 1764, 405, k3, align='right')
            text(c, 'unfolds into a surface', 1036, 790, 28, 600, 'ink', ramp(t, 16.2, 0.6))
            rich(c, 'the {f:sine-wave amplitudes} can be read off the latent', 1036, 840, 24, 740, t, 18.5, 0.03, 0.4, base='muted')
        caption(c, t, 'The authors’ reading: {y:unfold first} with three numbers, then the network {y:projects down} to two.', 23.0, None, y=1000, size=30)

class Cylinder(Scene):
    dur = 28.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (5.2, 'pop'), (16.8, 'sweep')]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'test 2 · cylinder flow', 'Flow past a *cylinder*')
        k = ramp(t, 0.5, 0.8)
        sp = wake(c, 140, 340, 980, 320, t, k, sensor=ramp(t, 11.5, 0.6))
        illustration(c, 1120, 690, k, align='right')
        ks = ramp(t, 11.6, 0.6)
        if ks > 0:
            lw = text_width('one sensor: vₓ at (35, 45)', 22, 600)
            rrect(c, sp[0] + 16, sp[1] - 74, lw + 24, 36, 8, fill='bg0', a=ks, fa=ks * 0.85)
            text(c, 'one sensor: vₓ at (35, 45)', sp[0] + 28, sp[1] - 49, 22, 600, 'y', ks)
        for i, (lab, body, ti) in enumerate((('reynolds number', 'sets the regime · {y:Re 100 to 750}, one run each', 5.0),
                                             ('the model', 'a latent of {y:3 numbers} · {y:5–7} readings', 11.5))):
            kk = ramp(t, ti, 0.8, e_expo)
            if kk <= 0:
                continue
            yy = 340 + i * 170
            with layer(c, kk):
                panel(c, 1180, yy, 620, 150)
                kicker(c, lab, 1214, yy + 44, 1, 'muted', 16)
                rich(c, body, 1214, yy + 96, 26, 560, t, ti + 0.2, 0.03, 0.4)
        X = re_axis(c, 200, 1520, 790, t, 16.5)
        kl = ramp(t, 18.2, 0.6)
        if kl > 0:
            circle(c, 220, 893, 8, fill='g', a=kl)
            text(c, 'test inside: 133, 233, 333, 433, 533, 633', 240, 900, 20, 600, 'g', kl)
            circle(c, 820, 893, 8, fill='c', a=ramp(t, 18.8, 0.6))
            text(c, 'test just outside: 100, 733, 750', 840, 900, 20, 600, 'c', ramp(t, 18.8, 0.6))
            note(c, 'Re values from §4.3 (Geneva & Zabaras data)', 1720, 900, kl, 16, 'muted', 'right')

class Loops(Scene):
    dur = 30.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (3.6, 'draw'), (17.2, 'sweep')]
    RES = (100, 133, 233, 333, 433, 533, 633, 733, 750)

    def __init__(self):
        self.over = illus_loops(self.RES, separated=False, seed=3)
        self.sep = illus_loops(self.RES, separated=True)
        self.cols = [mix('g', 'y', i / 8) for i in range(9)]

    def errs(self, c, x, y, w, h, vals, colr, t, t0, a):
        """ILLUSTRATION of the error profile's shape across the nine test Re (no values: Fig. 11a is not typed)."""
        k = ramp(t, t0, 0.6) * a
        if k <= 0:
            return
        line(c, x, y + h, x + w, y + h, 'muted', k, 1.4)
        text(c, 'one-step error', x, y - 12, 16, 500, 'muted', k, kind='mono')
        for i, (re, v) in enumerate(zip(self.RES, vals)):
            X = x + (re - 100) / 650 * w
            g = ramp(t, t0 + 0.2 + i * 0.06, 0.6, e_expo)
            bh = h * v * g
            rrect(c, X - 7, y + h - bh, 14, bh, 3, fill=colr, a=k, fa=k * (0.9 if re in (100, 733, 750) else 0.6))
        text(c, 'Re 100', x, y + h + 26, 15, 500, 'muted', k, kind='mono')
        text(c, '750', x + w, y + h + 26, 15, 500, 'muted', k, 'right', kind='mono')

    def draw(self, c, t):
        hdr(self, c, t, '06', 'test 2 · the latent', 'Overlap, or *order*')
        for i, (lab, loops, t0, colr) in enumerate((('without Re as an input', self.over, 3.3, 'c'),
                                                     ('with Re as an input', self.sep, 17.0, 'f'))):
            k = ramp(t, t0 - 2.8 if i == 0 else t0, 0.7, e_expo)
            if k <= 0:
                continue
            x = 120 + i * 880
            with layer(c, k):
                panel(c, x, 330, 800, 640)
                kicker(c, lab, x + 36, 375, 1, colr, 18)
            illustration(c, x + 764, 375, k, align='right')
            latent_loop(c, x + 90, 410, 620, 330, loops, t, t0, k, colors=self.cols, frame=False, stagger=0.12,
                        dur=1.4, dot_speed=0.18, widths=[2.4] * 9)
            kl = ramp(t, t0 + 2.0, 0.6) * k
            text(c, 'Re 100', x + 70, 770, 17, 600, 'g', kl, kind='mono')
            text(c, '→ Re 750', x + 160, 770, 17, 600, 'y', kl, kind='mono')
            vals = ([0.95, 0.62, 0.42, 0.3, 0.26, 0.3, 0.42, 0.85, 1.0] if i == 0 else
                    [0.3, 0.27, 0.25, 0.24, 0.24, 0.25, 0.26, 0.3, 0.32])
            self.errs(c, x + 360, 830, 400, 90, vals, colr, t, (9.5 if i == 0 else 20.0), k)
        kc = ramp(t, 9.6, 0.6) * (1 - ramp(t, 16.5, 0.4))
        if kc > 0:
            hand(c, 'worst at the edges', 160, 905, 32, 'pencil', kc, -2.5, ramp(t, 9.8, 0.8, e_lin))
        note(c, 'shapes as described in §4.3 / Fig. 11 · out-of-range Re drawn darker', W / 2, 1010, ramp(t, 10.0, 0.6), 16, 'muted', 'center')

class Recon(Scene):
    dur = 24.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (5.6, 'pop'), (10.2, 'pop'), (12.0, 'pop')]
    LO, HI = 1e-5, 1e-1

    def draw(self, c, t):
        hdr(self, c, t, '07', 'test 2 · rebuild the field', 'From the latent to the *whole field*')
        k = ramp(t, 0.6, 0.7)
        rich(c, 'a kernel regression, {y:geometric harmonics}, maps the latent to the full vₓ field · 5-fold cross-validation, App. A.5',
             MX, 350, 24, 1500, t, 0.8, 0.02, 0.4, base='muted')
        bx, w = 400, 900
        L = lambda v: (math.log10(v) - math.log10(self.LO)) / (math.log10(self.HI) - math.log10(self.LO)) * w
        y0 = 500
        if k > 0:
            for e in range(-5, 0):
                X = bx + L(10.0 ** e)
                line(c, X, y0 - 40, X, y0 + 330, 'line', k * 0.8, 1)
                text(c, decade(e), X, y0 - 52, 19, 500, 'muted', k, 'center')
            text(c, 'mean absolute error · log scale', bx + w, y0 + 370, 16, 500, 'muted', k, 'right', kind='mono')
        for i, (lab, v1, v2) in enumerate(CYL_RECON):
            yy = y0 + i * 180
            kr = ramp(t, 5.0 + i * 0.4, 0.6)
            if kr <= 0:
                continue
            text(c, lab, bx - 24, yy + 44, 28, 600, 'ink', kr, 'right')
            for j, (v, colr, nm, ti) in enumerate(((v1, 'f', 'with Re', 5.5 + i * 0.4), (v2, 'c', 'without Re', 10.0 + i * 0.6))):
                kk = ramp(t, ti, 0.6)
                if kk <= 0:
                    continue
                yb = yy + j * 48
                ww = max(3, L(v) * ramp(t, ti, 1.0, e_expo))
                rrect(c, bx, yb, ww, 38, 6, fill=colr, a=kk, fa=kk * 0.85)
                text(c, f'{sci(v, 2)}', bx + ww + 14, yb + 29, 22, 600, colr, kk)
                text(c, nm, bx + 14, yb + 27, 18, 700, 'bg0', kk, kind='mono')
        for i, (big, small, ti) in enumerate((('66.5×', 'worse over the whole field', 11.0), ('53.6×', 'worse in the wake', 12.0))):
            kk = ramp(t, ti, 0.8, e_expo)
            stat(c, 1500, 560 + i * 180, big, small, 'c', kk, 66)
        hand(c, '≈ 70× and ≈ 50×', 1500, 900, 32, 'pencil', ramp(t, 13.0, 0.6), -2.5, ramp(t, 13.0, 0.9, e_lin))
        note(c, 'fold-to-fold spread ≈ 13× smaller than the gap  (App. A.5 says “two orders of magnitude”)',
             W / 2, 1000, ramp(t, 15.0, 0.6), 17, 'muted', 'center')

class Lesson(Scene):
    dur = 24.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (6.7, 'pop'), (11.7, 'chime')]
    CARDS = [('chafee–infante', 'enough readings, {c:too little room}', 'the surface folds', 0.5),
             ('cylinder flow', 'enough room, a {c:hidden parameter}', 'the regimes overlap', 6.5)]

    def draw(self, c, t):
        hdr(self, c, t, '08', 'both tests', 'Good forecasts, folded *insides*')
        for i, (lab, body, res, ti) in enumerate(self.CARDS):
            k = ramp(t, ti, 0.8, e_expo)
            if k <= 0:
                continue
            x = MX + i * 860
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    panel(c, x, 340, 820, 250)
                    line(c, x + 36, 341, x + 156, 341, 'y', 1, 4, cap='butt')
                    kicker(c, lab, x + 36, 392, 1, 'muted', 17)
                    rich(c, body, x + 36, 462, 36, 760, t, ti + 0.2, 0.03, 0.4)
                    text(c, '→ ' + res, x + 36, 540, 26, 500, 'muted', 1, kind='italic')
        kk = ramp(t, 11.5, 0.9, e_expo)
        if kk > 0:
            with layer(c, kk):
                wd = text_width('One-step accuracy is not ', 64, 700) + text_width('latent identifiability', 64, 400, 'italic')
                x0 = W / 2 - wd / 2
                w1 = text(c, 'One-step accuracy is not ', x0, 760, 64, 700, 'ink')
                w2 = text(c, 'latent identifiability', x0 + w1, 760, 64, 400, 'y', kind='italic')
                swash(c, x0 + w1, x0 + w1 + w2, 784, 'y', 1, ramp(t, 12.2, 0.8, e_io), w=4)
        rich(c, 'identifiable: each true state gets {y:its own place} in the latent  (§5.1)', W / 2, 860, 30, 1500, t, 15.5,
             0.03, 0.45, 1, 'center', base='muted')

class Emulators(Scene):
    dur = 34.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (10.7, 'pop'), (18.7, 'pop'), (27.2, 'pop')]
    CARDS = [('forcing ≈ Re', 'feed in {y:CO₂} and other forcings, so the latent can keep climates apart', 'y', 10.5,
              'in the paper: Re as an input separated the loops'),
             ('hidden state', '{g:deep ocean} (if atmosphere-only), {g:deep soil}: stepping from today’s state assumes it is complete', 'g', 18.5,
              'in the paper: one sensor needed past readings to stand in for the state'),
             ('test beyond one step', 'check {f:spectra} and {f:long-run statistics}, not just step error', 'f', 27.0,
              'in the paper: good one-step skill in both hid a 66.5× gap')]

    def draw(self, c, t):
        hdr(self, c, t, '09', 'our extrapolation', 'Climate *emulators*')
        ke = ramp(t, 0.4, 0.6)
        if ke > 0:
            w = text_width(EXTRAP, 22, 500, 'mono', 0.04) + 36
            rrect(c, W - MX - w, 150, w, 44, 22, fill='y', a=ke, fa=ke * 0.14)
            rrect(c, W - MX - w, 150, w, 44, 22, stroke='y', sw=1.6, a=ke)
            extrap_label(c, W - MX - 18, 180, ke, 22, 'right')
            note(c, 'not a claim of the paper', W - MX, 226, ke, 16, 'muted', 'right')
        rich(c, '{y:ACE}, {y:SamudrACE}: learned models that step a whole climate state forward', MX, 360, 30, 1600, t, 4.6, 0.03, 0.45)
        for i, (lab, body, colr, ti, foot) in enumerate(self.CARDS):
            k = ramp(t, ti, 0.8, e_expo)
            if k <= 0:
                continue
            x = MX + i * 568
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    panel(c, x, 430, 540, 420)
                    line(c, x + 36, 431, x + 156, 431, colr, 1, 4, cap='butt')
                    text(c, lab, x + 36, 510, 38, 400, 'ink', 1, kind='italic')
                    rich(c, body, x + 36, 580, 27, 470, t, ti + 0.3, 0.025, 0.4)
                    line(c, x + 36, 740, x + 504, 740, 'line', 1, 1.2)
                    rich(c, foot, x + 36, 785, 21, 470, t, ti + 1.2, 0.02, 0.4, base='muted')

class Discussion(Scene):
    dur = 20.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.0, 'chime'), (10.5, 'chime')]

    def draw(self, c, t):
        hdr(self, c, t, '10', 'before we meet', 'Questions to *bring*')
        question_cards(c, t, [('Two models predict the next step {y:equally well}. What test shows which has the {y:sounder inside}?', 3.0),
                              ('In a climate emulator, what plays the {y:missing Reynolds number}, and how would we notice?', 10.5)])

class End(EndCard):
    dur = 15.0
    TAKE = 'Enough information is not enough: a model needs {y:room to unfold} it, and the {y:parameters} that tell regimes apart.'
    STATS = [('2 → 3', 'latent numbers: collapsed → unfolded', 'f'), ('≈ 70×', 'worse field rebuild without Re', 'c'),
             ('5', 'readings from one sensor', 'y')]
    NEXT = 'one-step accuracy is not latent identifiability  ·  journal club, nov 11'
