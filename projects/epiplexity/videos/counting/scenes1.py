"""Who's Counting? part 1: the four files and the classical judges (Shannon, Kolmogorov, a real compressor,
sophistication, the cryptographers). Facts: arXiv:2601.03220v2 §2 and §7 (see projects/epiplexity/AGENTS.md).
Compression numbers are OUR check (data/ours_compress*.json); the next-bit predictor is OUR check, computed here."""
from countkit import *
from scipy import ndimage

def title_line(c, s, x, y, size, a=1.0, align='center', prog=1.0):
    """One line of display type with one *amber italic* word and its swash."""
    parts = s.split('*')
    ws = [text_width(p, size, 400, 'italic') if i % 2 else text_width(p, size, 700, tracking=-0.005)
          for i, p in enumerate(parts)]
    xx = x - sum(ws) / 2 if align == 'center' else x
    for i, (p, wd) in enumerate(zip(parts, ws)):
        if not p:
            continue
        if i % 2:
            text(c, p, xx, y, size, 400, 'y', a, kind='italic')
            swash(c, xx - 4, xx + wd + 6, y + size * 0.22, 'y', a, prog)
        else:
            text(c, p, xx, y, size, 700, 'ink', a, tracking=-0.005)
        xx += wd

JUDGES = ['shannon', 'kolmogorov', 'a compressor', 'sophistication', 'the cryptographer', 'epiplexity']

class ColdOpen(Scene):
    dur = 32.0
    fade_in = 0.3
    cues = [(0.3, 'whoosh_soft'), (3.5, 'pop'), (6.0, 'pop'), (9.0, 'pop'), (14.5, 'pop')]
    T = (3.5, 6.0, 9.0, 14.5)
    SUBS = ('nothing but 0s', 'a fair coin, flipped', 'SHA-256 from a 56-bit seed', '8,192 lines of (X, Y)')

    def draw(self, c, t):
        kicker(c, 'four files  ·  1,048,576 bits each', W / 2, 210, ramp(t, 0.5, 0.8), 'muted', 20, 'center')
        s = 360
        for i in range(4):      # empty slots, filled one by one
            ks = ramp(t, 0.6 + i * 0.25, 0.6) * (1 - ramp(t, self.T[i], 0.5))
            if ks > 0:
                rrect(c, 150 + i * 420 - 8, 292, s + 16, s + 16, 10, stroke='faint', sw=1.6, a=ks)
                text(c, str(i + 1), 150 + i * 420 + s / 2, 300 + s / 2 + 20, 64, 300, 'faint', ks, 'center', kind='italic')
        for i, (key, name, _) in enumerate(FILES):
            t0 = self.T[i]
            k = ramp(t, t0, 0.7, e_expo)
            if k <= 0:
                continue
            x = 150 + i * 420
            y = 300
            with layer(c, k):
                with xform(c, 0, (1 - k) * 30):
                    if key == 'ca':
                        h = s * 49 / 64
                        yy = y + (s - h) / 2
                        rrect(c, x - 8, yy - 8, s + 16, h + 16, 10, fill='panel', fa=0.9)
                        dimk = ramp(t, 19.0, 1.0, e_io)
                        rev = ramp(t, t0 + 0.3, 3.4, e_lin)
                        full = bit_image('ca_full', file_bits('ca'), 6, 1, 'ink', 'panel2')
                        dimmed = bit_image('ca', file_bits('ca'), 6, 1, 'ink', 'panel2', dim_rows=range(1, 48))
                        draw_grid(c, full, x, yy, s, h, 1 - dimk, rev)
                        draw_grid(c, dimmed, x, yy, s, h, dimk, rev)
                        kl = ramp(t, 19.6, 0.6)
                        tag(c, 'X · a random row', x, yy - 16, kl, 'y', 15)
                        tag(c, 'Y · the same row, 48 steps later', x, yy + h + 30, kl, 'y', 15)
                        text(c, '47 rows in between: not in the file', x + s / 2, yy + h / 2 + 6, 17, 500, 'muted', kl, 'center')
                    else:
                        rrect(c, x - 8, y - 8, s + 16, s + 16, 10, fill='panel', fa=0.9)
                        im = bit_image(key + '64', file_bits(key)[:64, :64], 6, 1, 'ink', 'panel2')
                        draw_grid(c, im, x, y, s, s, 1, ramp(t, t0 + 0.2, 1.3, e_io))
                    text(c, str(i + 1), x, y + s + 92, 54, 300, 'y', 1, kind='italic')
                    text(c, name, x + 44, y + s + 82, 32, 600, 'ink', 1)
                    text(c, self.SUBS[i], x + 44, y + s + 112, 16, 400, 'muted', 1, kind='mono')
        kq = ramp(t, 24.0, 0.9, e_expo)
        if kq > 0:
            title_line(c, 'Which holds the most *information*?', W / 2, 895 + (1 - kq) * 20, 54, kq, prog=ramp(t, 24.6, 0.8, e_io))
        # the judges, as a row of pills
        kj = ramp(t, 27.0, 0.5)
        if kj > 0:
            size = 18
            ws = [text_width(j, size, 400, 'mono', 0.12) + 30 for j in JUDGES]
            gap = 22
            x = W / 2 - (sum(ws) + gap * (len(ws) - 1)) / 2
            for i, (j, wd) in enumerate(zip(JUDGES, ws)):
                kk = ramp(t, 27.4 + i * 0.35, 0.5, e_back)
                pill(c, x, 950, j, 'y' if j == 'epiplexity' else 'muted', kk * kj, 0.8 + 0.2 * kk, size=size)
                x += wd + gap

class Title(Scene):
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]

    def draw(self, c, t):
        x0 = MX + 40
        kicker(c, 'epiplexity  ·  an explainer', x0, 320, ramp(t, 0.2, 0.8), 'muted', 18)
        k = ramp(t, 0.1, 1.0, e_expo)
        with layer(c, k, (1 - k) * 14):
            w1 = text(c, 'Who’s ', x0, 520 + (1 - k) * 40, 150, 700, 'ink', tracking=-0.01)
            w2 = text(c, 'counting', x0 + w1, 520 + (1 - k) * 40, 150, 400, 'y', kind='italic')
            text(c, '?', x0 + w1 + w2 + 6, 520 + (1 - k) * 40, 150, 700, 'ink')
        swash(c, x0 + w1 - 4, x0 + w1 + w2 + 6, 556, 'y', 1, ramp(t, 0.7, 0.9, e_io), w=4)
        text(c, 'Shannon, Kolmogorov, and the bounded observer', x0, 632, 44, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'a companion to Finzi, Qiu, Jiang, Izmailov, Kolter & Wilson (2026)', x0, 720, 28, 500, 'ink', ramp(t, 4.5, 0.8))
        kicker(c, 'from entropy to epiplexity  ·  arxiv:2601.03220', x0, 776, ramp(t, 5.0, 0.8), 'muted', 17)
        for i, (key, _, _) in enumerate(FILES):
            kk = ramp(t, 0.5 + i * 0.3, 0.7, e_expo)
            x = 1440 + (i % 2) * 210
            y = 300 + (i // 2) * 230 + (25 if key == 'ca' else 0)
            file_thumb(c, key, x, y + (1 - kk) * 20, 170, kk, 1)

class Shannon(Scene):
    dur = 30.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (3.0, 'draw')]

    def draw(self, c, t):
        header(c, t, '01', 'judge 1  ·  shannon, 1948', 'Information is *surprise*',
               sub='Claude Shannon, “A Mathematical Theory of Communication”, Bell Labs, 1948')
        ax = Axes(190, 380, 700, 380, (0, 1), (0, 11))
        ka = ramp(t, 3.0, 0.8, e_expo)
        ax.draw(c, ka, [0, 0.5, 1], [0, 5, 10], prog=ka, fmt='{:g}', xfmt='{:g}')
        text(c, 'probability p', ax.x + ax.w / 2, ax.y + ax.h + 74, 20, 400, 'muted', ka, 'center', kind='mono')
        text(c, 'surprise (bits)', ax.x, ax.y - 22, 20, 400, 'muted', ka, kind='mono')
        p = np.geomspace(2 ** -11, 1, 400)
        draw_poly(c, ax.pts(p, np.log2(1 / p)), 'g', ka, 4, prog=ramp(t, 3.2, 2.0, e_io), glow=5)
        km = ramp(t, 9.0, 0.6)
        if km > 0:
            X, Y = ax.px(0.5, 1.0)
            circle(c, X, Y, 9, fill='y', a=km, glow=8)
            text(c, 'fair coin: p = ½ → 1 bit', X + 18, Y - 18, 24, 600, 'y', km)
        km2 = ramp(t, 10.8, 0.6)
        if km2 > 0:
            X, Y = ax.px(0.001, np.log2(1000))
            circle(c, X, Y, 9, fill='y', a=km2, glow=8)
            text(c, '1 in 1000 → ≈ 10 bits', X + 24, Y + 8, 24, 600, 'y', km2)
        tex(c, 'surprise', 1340, 430, 56, ramp(t, 3.0, 0.8), reveal=ramp(t, 3.0, 1.0, e_io))
        ke = ramp(t, 14.0, 0.8)
        tex(c, 'entropy', 1340, 600, 56, ke, reveal=ramp(t, 14.0, 1.0, e_io))
        note(c, 'the average surprise: no code beats it on average', 1340, 690, ke, 17, 'muted', 'center')
        # it describes a source, not a file
        ks = window(t, 19.0, 21.6, 0.7, 0.5)
        if ks > 0:
            with layer(c, ks):
                rrect(c, 1010, 745, 230, 110, 14, fill='panel2', fa=0.9)
                rrect(c, 1010, 745, 230, 110, 14, stroke='g', sw=2)
                text(c, 'source', 1125, 792, 30, 400, 'ink', 1, 'center', kind='italic')
                text(c, 'p(x)', 1125, 830, 22, 400, 'g', 1, 'center', kind='mono')
                for j in range(3):
                    yy = 735 + j * 58
                    arrow(c, 1250, 800, 1420, yy + 22, 'muted', ramp(t, 19.3 + j * 0.2, 0.4), 2, 10,
                          prog=ramp(t, 19.3 + j * 0.2, 0.5, e_io))
                    im = bit_image(f'src{j}', file_bits('coins')[j * 6:j * 6 + 6, :40], 6, 1, 'ink', 'panel2')
                    draw_grid(c, im, 1440, yy, 300, 45, ramp(t, 19.6 + j * 0.2, 0.4))
                note(c, 'H belongs to the source, not to one file', 1400, 935, 1, 17, 'g', 'center')
        quote_card(c, t, 22.0, 'The semantic aspects of communication are irrelevant to the engineering problem.',
                   'claude shannon, 1948', 990, 740, 810, size=30)

class ScoreShannon(ScoreScene):
    dur = 16.5
    chapter = 0
    COLS_NOW, TIMES, WIN = (0,), (1.8, 4.6, 8.2, 11.6), 13.8
    NUM, KICK, TITLE = '01', 'judge 1  ·  shannon', 'Shannon’s *scores*'

class Rules(Scene):
    dur = 22.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (3.0, 'pop'), (9.0, 'pop'), (15.0, 'pop')]
    CARDS = [("Processing can’t add", 'dpi', 40, 'A fixed function {y:f} never raises the entropy.', 3.0),
             ("Order doesn’t matter", 'sym', 30, 'Reading {y:X} then {y:Y} costs the same as {y:Y} then {y:X}.', 9.0),
             ('The source is the best model', 'ml', 34, 'So, the story goes, a model can’t learn more than its source.', 15.0)]

    def draw(self, c, t):
        header(c, t, '01', 'three rules', 'Three famous *rules*')
        cw, gap, y0, ch = 532, 42, 360, 430
        for i, (title, key, size, body, t0) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, 'g', 1, 4, cap='butt')
                    text(c, str(i + 1), x + 36, y0 + 92, 64, 300, 'y', 1, kind='italic')
                    text(c, title, x + 90, y0 + 82, 31, 400, 'ink', 1, kind='italic')
                    tex(c, key, x + cw / 2, y0 + 220, size, ramp(t, t0 + 0.4, 0.6), reveal=ramp(t, t0 + 0.4, 0.9, e_io))
                    rich(c, body, x + 36, y0 + 335, 30, cw - 72, t, t0 + 0.8, 0.03, 0.45)

class Kolmogorov(Scene):
    dur = 23.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (14.5, 'pop')]

    def draw(self, c, t):
        header(c, t, '02', 'judge 2  ·  the 1960s', 'The shortest *program*')
        x = MX
        for i, (s, ti) in enumerate((('solomonoff 1964', 0.8), ('kolmogorov 1965', 1.3), ('chaitin 1966', 1.8))):
            x += (pill(c, x, 330, s, 'x', ramp(t, ti, 0.5, e_back), size=18) or 0) + 18
        kk = ramp(t, 4.5, 0.8)
        tex(c, 'kolm', W / 2, 475, 64, kk, reveal=ramp(t, 4.5, 1.0, e_io), glow=4)
        note(c, 'the length of the shortest program that prints x, on a universal computer U', W / 2, 555, kk, 17, 'muted', 'center')
        ki = ramp(t, 10.0, 0.8)
        tex(c, 'invar', W / 2, 625, 44, ki, reveal=ramp(t, 10.0, 0.9, e_io))
        note(c, 'two languages agree up to a constant C', W / 2, 685, ki, 17, 'muted', 'center')
        for j, (s, prog, verdict, colr, t0) in enumerate((
                ('0101010101', 'repeat "01" five times', 'a short program: simple', 'f', 14.5),
                ('1001011100', 'print "1001011100"', 'no shortcut: random', 'c', 15.5))):
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            xx = MX + j * 860
            with layer(c, k):
                panel(c, xx, 735, 820, 170)
                text(c, s, xx + 40, 805, 44, 700, 'ink', 1, kind='mono', tracking=0.08)
                text(c, '→  ' + prog, xx + 40, 860, 24, 400, colr, 1, kind='mono')
                text(c, verdict, xx + 780, 805, 28, 400, colr, 1, 'right', kind='italic')
        tag(c, 'the paper’s example (§2.1)  ·  martin-löf, 1966: random = incompressible', W / 2, 945,
            ramp(t, 16.5, 0.6), 'muted', 16, 'center')

class ScoreK(ScoreScene):
    dur = 17.5
    chapter = 1
    COLS_DONE, COLS_NOW, TIMES, WIN = (0,), (1,), (2.2, 5.4, 8.6, 11.8), 14.2
    NUM, KICK, TITLE = '02', 'judge 2  ·  kolmogorov', 'Kolmogorov’s *scores*'

class Incomputable(Scene):
    dur = 35.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (13.0, 'draw')]
    ROWS = [('zeros', 'all zeros', 17.5), ('coins', 'coin flips', 19.0), ('prng', 'pseudorandom', 21.0), ('ca', 'rule 54 pairs', 26.0)]

    def draw(self, c, t):
        header(c, t, '02', 'kolmogorov’s catch', 'A score no one can *compute*')
        k1 = ramp(t, 0.5, 0.8, e_expo)
        if k1 > 0:
            with layer(c, k1):
                card(c, MX, 330, 700, 250, 1, 'x', 'Incomputable')
                text(c, 'K(x) = ?', MX + 40, 470, 60, 700, 'x', 1, kind='mono')
                rich(c, 'Finding the shortest program would solve the {x:halting problem}.', MX + 40, 530, 25, 620,
                     t, 1.0, 0.03, 0.45)
        k2 = ramp(t, 6.5, 0.8, e_expo)
        if k2 > 0:
            with layer(c, k2):
                card(c, MX, 610, 700, 270, 1, 'x', 'Chaitin’s limit')
                rich(c, 'In a given formal system, no specific string can be proven to have {x:K(x) > L}.', MX + 40, 730,
                     25, 620, t, 7.0, 0.03, 0.45)
                note(c, 'L: on typical machines, often a few thousand bits', MX + 40, 845, 1, 15, 'muted')
                note(c, '(chaitin, as cited in the paper, §2.2)', MX + 40, 868, 1, 15, 'muted')
        # our compression check
        kc = ramp(t, 13.0, 0.8)
        if kc <= 0:
            return
        x0, bx, bw = 900, 1190, 560
        kicker(c, 'our check  ·  compressed bits per original bit', x0, 360, kc, 'y', 18)
        tag(c, 'xz bars; gzip and bz2 as dots  ·  1,048,576 bits per file', x0, 390, kc, 'muted', 15)
        for v in (0, 0.5, 1.0):
            X = bx + bw * v / 1.05
            line(c, X, 420, X, 860, 'line', kc, 1)
            text(c, f'{v:g}', X, 892, 20, 500, 'muted', kc, 'center', kind='mono')
        for i, (key, name, t0) in enumerate(self.ROWS):
            y = 430 + i * 106
            k = ramp(t, t0, 0.6)
            if k <= 0:
                continue
            file_thumb(c, key, x0 + 4, y + 12 if key != 'ca' else y + 20, 60, k, cell=6)
            text(c, name, x0 + 84, y + 52, 23, 600, 'ink', k)
            v = zip_ratio(key, 'xz')
            g = ramp(t, t0 + 0.2, 1.0, e_io)
            rrect(c, bx, y + 26, max(3, bw * v / 1.05 * g), 40, 6, fill='v', a=k, fa=k * 0.85)
            for comp in ('gzip', 'bz2'):
                X = bx + bw * zip_ratio(key, comp) / 1.05 * g
                circle(c, X, y + 46, 5, fill='ink', a=k * 0.8)
            fmt = f'{v:.3f}' if v < 0.01 else f'{v:.2f}'
            text(c, fmt, bx + bw * v / 1.05 * g + 16, y + 56, 24, 600, 'ink', k * ramp(t, t0 + 0.9, 0.4))
        # Kolmogorov vs the compressor on the pseudorandom file; Shannon vs the compressor on rule 54
        kk = ramp(t, 23.0, 0.6)
        if kk > 0:
            y = 430 + 2 * 106
            line(c, bx + 3, y + 14, bx + 3, y + 78, 'x', kk, 3)
            text(c, 'Kolmogorov: ≈ 56 bits + the generator', bx + 14, y + 96, 16, 500, 'x', kk)
        ks = ramp(t, 27.5, 0.6)
        if ks > 0:
            y = 430 + 3 * 106
            X = bx + bw * 0.5 / 1.05
            line(c, X, y + 8, X, y + 84, 'g', ks, 4, dash=[8, 5])
            text(c, 'Shannon: 0.5', X - 12, y + 96, 16, 500, 'g', ks, 'right')
        caption(c, t, 'A real compressor is already a {y:bounded observer}.', 31.0, None, y=975, size=32)

class ScoreZip(ScoreScene):
    dur = 7.5
    chapter = 1
    COLS_DONE, COLS_NOW, TIMES, WIN = (0, 1), (2,), (0.9, 1.5, 2.1, 2.7), 3.6
    NUM, KICK, TITLE = '02', 'a real compressor  ·  our check', 'The compressor’s *scores*'
    NOTE = 'xz on our copies of the files  ·  M = 1,048,576 bits'

# ---------------------------------------------------------------- structure vs noise
def coffee_field(n=220, swirl=0.0, blur=1.2, seed=0):
    """Cream (1) poured on coffee (0) in a round cup, stirred by a twist and blurred by diffusion: an illustration."""
    yy, xx = np.mgrid[-1:1:n * 1j, -1:1:n * 1j]
    r = np.hypot(xx, yy)
    th = np.arctan2(yy, xx) - swirl * (1 - np.clip(r, 0, 1)) ** 1.4
    xs, ys = r * np.cos(th), r * np.sin(th)
    wob = 0.05 * np.sin(5 * np.arctan2(ys, xs) + seed) * (swirl > 0)
    f = (ys < -0.05 + wob).astype(float)
    f = ndimage.gaussian_filter(f, blur)
    return f, r

_cups = {}
def cup_image(state):
    if state in _cups:
        return _cups[state]
    swirl, blur = {0: (0.0, 1.2), 1: (7.5, 2.2), 2: (7.5, 60.0)}[state]
    f, r = coffee_field(swirl=swirl, blur=blur)
    if state == 2:
        f = np.full_like(f, f[r < 1].mean())
    coffee, cream = np.array(hexrgb('#3a2417'), float), np.array(hexrgb('#ead9bd'), float)
    rgb = coffee + (cream - coffee) * f[..., None]
    a = np.clip((1.0 - r) * 110, 0, 1) * 255
    im = np.concatenate([rgb, a[..., None]], -1).astype(np.uint8)
    _cups[state] = skia.Image.fromarray(np.ascontiguousarray(im), colorType=skia.kRGBA_8888_ColorType)
    return _cups[state]

class Structure(Scene):
    dur = 34.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (9.5, 'pop'), (13.8, 'pop'), (18.5, 'pop'), (23.0, 'whoosh_soft')]

    def draw(self, c, t):
        header(c, t, '03', 'structure vs noise', 'Structure, or *noise*?')
        # stage A: the coin flips win every judge so far
        ka = window(t, 0.5, 9.0, 0.7, 0.6)
        if ka > 0:
            with layer(c, ka):
                file_thumb(c, 'coins', 180, 360, 300, 1)
                for i, (s, ti) in enumerate((('shannon  ·  1 M', 0.9), ('kolmogorov  ·  ≈ 1 M', 1.3), ('compressor  ·  1.00 M', 1.7))):
                    pill(c, 530, 380 + i * 62, s, 'y', ramp(t, ti, 0.5, e_back), size=18)
                kb = ramp(t, 5.0, 0.8)
                if kb > 0:
                    bx, by, bw = 1010, 470, 770
                    split = ramp(t, 6.0, 1.0, e_io)
                    sw = bw * 0.36 * split
                    rrect(c, bx, by, bw, 64, 10, fill='v', a=kb, fa=kb * 0.5)
                    if split > 0:
                        rrect(c, bx, by, sw, 64, 10, fill='y', a=kb, fa=kb * 0.85)
                        line(c, bx + sw, by - 10, bx + sw, by + 74, 'ink', kb * split, 2)
                    text(c, 'information', bx, by - 22, 22, 400, 'muted', kb, kind='mono')
                    text(c, 'structure', bx + 20, by + 42, 26, 600, 'panel', kb * split)
                    text(c, 'noise', bx + bw - 20, by + 42, 26, 600, 'ink', kb * split, 'right')
                    tag(c, 'the wish  ·  illustration', bx, by + 110, kb, 'muted', 15)
        # stage B: three attempts
        for i, (title, who, body, t0, extra) in enumerate((
                ('sophistication', 'Koppel, 1988', 'The bits for the simplest set in which the string looks typical.', 9.5, 'soph'),
                ('effective complexity', 'Gell-Mann & Lloyd, 1996', 'The same aim: the regularities, not the random part.', 13.8, None),
                ('logical depth', 'Bennett, 1988', 'How long a near-shortest program takes to run.', 18.5, None))):
            k = window(t, t0, 22.4, 0.9, 0.6, e_expo)
            if k <= 0:
                continue
            x = MX + i * 574
            with layer(c, k):
                with xform(c, 0, (1 - ramp(t, t0, 0.9, e_expo)) * 30):
                    panel(c, x, 350, 532, 400)
                    line(c, x + 36, 351, x + 156, 351, 'f', 1, 4, cap='butt')
                    text(c, title, x + 36, 420, 36, 400, 'ink', 1, kind='italic')
                    note(c, who.lower(), x + 36, 456, 1, 16, 'f')
                    rich(c, body, x + 36, 530, 27, 460, t, t0 + 0.4, 0.03, 0.45)
                    if extra:
                        tex(c, extra, x + 266, 680, 23, ramp(t, t0 + 1.0, 0.6))
        kn = window(t, 19.5, 22.4, 0.6, 0.6)
        note(c, 'and no proof can show that a specific string is highly sophisticated (Chaitin)', W / 2, 810, kn, 17, 'muted', 'center')
        # stage C: cream in coffee
        if t < 22.6:
            return
        labels = ('the start: simple', 'swirls: intricate', 'mixed: simple again')
        for i in range(3):
            k = ramp(t, 23.0 + i * 1.4, 0.8, e_expo)
            if k <= 0:
                continue
            cx = 430 + i * 530
            r = 140
            with layer(c, k):
                circle(c, cx, 480, r + 10, fill='panel2', stroke='pencil', sw=2)
                draw_image(c, cup_image(i), cx - r, 480 - r, 2 * r, 2 * r, 1)
                text(c, labels[i], cx, 672, 24, 500, 'ink', 1, 'center')
        # the curves (illustration): entropy rises, coarse complexity rises and falls
        kc = ramp(t, 26.0, 0.8)
        if kc > 0:
            x0, y0, w, h = 300, 770, 1320, 150
            line(c, x0, y0 + h, x0 + w, y0 + h, 'muted', kc, 1.6)
            text(c, 'time →', x0 + w, y0 + h + 30, 18, 400, 'muted', kc, 'right', kind='mono')
            u = np.linspace(0, 1, 200)
            ent = 1 - np.exp(-4 * u)
            flat = ramp(t, 29.5, 2.0, e_io)
            hump = (np.exp(-((u - 0.45) / 0.17) ** 2)) * (1 - 0.88 * flat)
            draw_poly(c, np.stack([x0 + u * w, y0 + h - ent * h], 1), 'v', kc, 3, prog=ramp(t, 26.2, 1.6, e_io))
            draw_poly(c, np.stack([x0 + u * w, y0 + h - hump * h * 0.95], 1), 'y', kc, 4, prog=ramp(t, 26.6, 1.6, e_io), glow=5)
            text(c, 'disorder', x0 + w - 10, y0 + 46, 20, 500, 'v', kc, 'right')
            text(c, 'apparent complexity', x0 + 12, y0 + 30, 20, 500, 'y', kc)
            tag(c, 'illustration  ·  after Aaronson, Carroll & Ouellette (2014), cited in the paper', x0, y0 - 8, kc, 'muted', 14)
            kf = ramp(t, 29.5, 0.8)
            text(c, 'with unlimited compute, just the start + physics: the complexity evaporates', x0 + 0.45 * w, y0 + h + 34, 20, 600, 'y', kf * 0.95, 'center')

class ScoreSoph(ScoreScene):
    dur = 12.0
    chapter = 2
    COLS_DONE, COLS_NOW, TIMES, WIN = (0, 1, 2), (3,), (1.6, 2.4, 3.2, 5.0), None
    NUM, KICK, TITLE = '03', 'structure vs noise', 'Sophistication’s *scores*'
    NOTE = 'sophistication: the structure part, with unlimited compute'

# ---------------------------------------------------------------- cryptography
def prng_bits(n):
    out, ctr = bytearray(), 0
    while len(out) * 8 < n:
        out += hashlib.sha256(b'seed:42' + ctr.to_bytes(8, 'big')).digest(); ctr += 1
    return np.unpackbits(np.frombuffer(bytes(out), np.uint8))[:n]

_pred = {}
def next_bit_check(n=20000, order=10):
    """OUR check: an order-10 context-counting predictor run online over the generator's bits. Returns the bits,
    the predictions and the running accuracy."""
    if not _pred:
        b = prng_bits(n + order)
        counts = np.zeros((1 << order, 2), np.int64)
        ctx = 0
        for i in range(order):
            ctx = ((ctx << 1) | int(b[i])) & ((1 << order) - 1)
        pred = np.zeros(n, np.uint8)
        for i in range(n):
            bit = int(b[order + i])
            pred[i] = 1 if counts[ctx, 1] > counts[ctx, 0] else 0
            counts[ctx, bit] += 1
            ctx = ((ctx << 1) | bit) & ((1 << order) - 1)
        hit = (pred == b[order:]).astype(float)
        _pred.update(bits=b[order:], pred=pred, acc=np.cumsum(hit) / np.arange(1, n + 1))
    return _pred

class Crypto(Scene):
    dur = 30.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (11.0, 'pop'), (15.5, 'draw'), (25.0, 'pop')]

    def draw(self, c, t):
        header(c, t, '04', 'the cryptographers', 'Random *to whom*?')
        kq = 1 - ramp(t, 24.4, 0.6, e_io)
        if kq > 0:
            quote_card(c, t, 3.0, 'Anyone who considers arithmetical methods of producing random digits is, of course, in a state of sin.',
                       'john von neumann, 1951  ·  quoted in the paper', MX, 320, W - 2 * MX, size=32, a=kq)
        # one-way function (replaces the quote)
        kw = ramp(t, 25.0, 0.8)
        if kw > 0:
            with layer(c, kw):
                y = 400
                for j, (a_, b_, lab, colr, dash) in enumerate((('x', 'f(x)', 'easy', 'f', None), ('f(x)', 'x', 'hard', 'c', [10, 8]))):
                    xx = 260 + j * 760
                    text(c, a_, xx, y + 14, 40, 400, 'ink', 1, 'center', kind='italic')
                    arrow(c, xx + 60, y, xx + 400, y, colr, 1, 3, 14, prog=ramp(t, 25.3 + j * 0.8, 0.7, e_io), dash=dash)
                    text(c, b_, xx + 470, y + 14, 40, 400, 'ink', 1, 'center', kind='italic')
                    text(c, lab, xx + 230, y - 22, 24, 600, colr, ramp(t, 25.6 + j * 0.8, 0.5), 'center')
                tag(c, 'a one-way function: the engine under pseudorandom generators', W / 2, y + 80, 1, 'muted', 16, 'center')
        # two grids and a fast test
        kt = ramp(t, 11.0, 0.8, e_expo)
        if kt > 0:
            with layer(c, kt):
                file_thumb(c, 'coins', 150, 590, 200, 1)
                file_thumb(c, 'prng', 690, 590, 200, 1)
                text(c, 'coin flips', 250, 830, 22, 600, 'ink', 1, 'center')
                text(c, 'pseudorandom', 790, 830, 22, 600, 'ink', 1, 'center')
                rrect(c, 410, 640, 220, 100, 14, fill='panel2', fa=0.95)
                rrect(c, 410, 640, 220, 100, 14, stroke='c', sw=2)
                text(c, 'any fast test', 520, 684, 22, 600, 'c', 1, 'center')
                text(c, '?', 520, 726, 30, 400, 'ink', 1, 'center', kind='italic')
                arrow(c, 362, 690, 404, 690, 'muted', 1, 2, 9)
                arrow(c, 678, 690, 636, 690, 'muted', 1, 2, 9)
                kc = ramp(t, 13.5, 0.6)
                text(c, 'can’t tell them apart', 520, 780, 22, 500, 'c', kc, 'center', kind='italic')
                tag(c, 'blum & micali · yao, 1982', 520, 880, kc, 'muted', 15, 'center')
        kd = ramp(t, 19.0, 0.6)
        if kd > 0:
            pill(c, 160, 912, 'with the seed: predictable', 'f', kd, size=16)
            pill(c, 560, 912, 'without it: random', 'c', ramp(t, 19.6, 0.6), size=16)
        # next-bit predictor, OUR check
        kp = ramp(t, 15.5, 0.8, e_expo)
        if kp > 0:
            d = next_bit_check()
            x0, y0 = 1050, 590
            with layer(c, kp):
                panel(c, x0, y0, 750, 330)
                text(c, 'predict the next bit', x0 + 36, y0 + 56, 30, 400, 'ink', 1, kind='italic')
                n = len(d['acc'])
                prog = ramp(t, 16.0, 7.0, e_io)
                i = max(1, int(prog * (n - 1)))
                win = d['bits'][max(0, i - 20):i]
                for j, b in enumerate(win):
                    rrect(c, x0 + 36 + j * 28, y0 + 92, 22, 34, 4, fill='ink' if b else 'panel2', fa=0.9)
                    rrect(c, x0 + 36 + j * 28, y0 + 92, 22, 34, 4, stroke='faint', sw=1.2)
                pb = int(d['pred'][i])
                rrect(c, x0 + 36 + 20 * 28 + 10, y0 + 88, 28, 42, 5, stroke='c', sw=2)
                text(c, str(pb), x0 + 36 + 20 * 28 + 24, y0 + 118, 24, 600, 'c', 1, 'center', kind='mono')
                text(c, 'guess', x0 + 36 + 20 * 28 + 24, y0 + 152, 14, 400, 'c', 1, 'center', kind='mono')
                acc = d['acc'][i]
                text(c, f'{acc * 100:.1f}%', x0 + 36, y0 + 235, 64, 700, 'ink', 1)
                text(c, f'right, after {i + 1:,} guesses', x0 + 270, y0 + 225, 22, 500, 'muted', 1)
                tag(c, 'our check: an order-10 context predictor on the generator’s bits', x0 + 36, y0 + 300, 1, 'muted', 14)

class ScoreCrypto(ScoreScene):
    dur = 14.0
    chapter = 3
    COLS_DONE, COLS_NOW, TIMES, WIN = (0, 1, 2, 3), (4,), (4.2, 5.1, 6.0, 7.6), None
    NUM, KICK, TITLE = '04', 'the cryptographers', 'The cryptographer’s *verdicts*'
    NOTE = 'does it look random to a fast (polynomial-time) observer?'
