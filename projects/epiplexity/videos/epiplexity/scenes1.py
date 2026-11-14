"""Cold open, title, the classic theories, the crack, the definition, examples, measuring (§1-§4 of arXiv:2601.03220v2).
Our compressor check (ours_compress.json) is labelled 'our check'; everything else drawn here is an illustration, an
exact computation (ECA, SHA-256 bits), or the paper's equations."""
import hashlib
from epikit import *

def _sha_bits(n, seed=b'seed:42'):
    """Bits from SHA-256 in counter mode, the same generator as our compressor check (lab/compress_lab.py)."""
    out, ctr = bytearray(), 0
    while len(out) * 8 < n:
        out += hashlib.sha256(seed + ctr.to_bytes(8, 'big')).digest(); ctr += 1
    return np.unpackbits(np.frombuffer(bytes(out), np.uint8))[:n]

# ======================================================================= COLD OPEN
class ColdOpen(Scene):
    """AlphaZero (§1, §5.1): simple rules and algorithm in; megabytes of weights out; the classic theories' verdict."""
    dur = 27.0
    fade_in = 0.8
    cues = [(0.4, 'whoosh_soft'), (10.0, 'draw'), (17.2, 'stamp'), (18.4, 'stamp'), (23.4, 'riser')]
    # a Ruy Lopez opening, to animate "self-play" (an illustration, not a game AlphaZero played)
    MOVES = [('e2', 'e4'), ('e7', 'e5'), ('g1', 'f3'), ('b8', 'c6'), ('f1', 'b5'), ('a7', 'a6'), ('b5', 'a4'), ('g8', 'f6'),
             ('d2', 'd3'), ('f8', 'e7'), ('c2', 'c3'), ('d7', 'd6')]

    def __init__(self):
        pos = {}
        for sqn, g in START.items():
            pos[sqn] = ('w:' + g) if sqn[1] in '12' else g
        self.boards = [dict(pos)]
        for fr, to in self.MOVES:
            pos = dict(pos)
            pos[to] = pos.pop(fr)
            self.boards.append(pos)
        rng = np.random.default_rng(4)
        self.weights = rng.random((16, 46)) ** 2.2

    def draw(self, c, t):
        # the board, with self-play moves from t = 10
        bx, by, bs = 150, 250, 520
        ka = ramp(t, 0.3, 1.0)
        mt = 10.0
        i = int(clamp((t - mt) / 0.55, 0, len(self.MOVES)))
        arrows = []
        if t >= mt and i < len(self.MOVES):
            fr, to = self.MOVES[i]
            arrows = [(fr, to, 'y', ramp(t, mt + i * 0.55, 0.4, e_io))]
        chessboard(c, bx, by, bs, ka, self.boards[i], arrows)
        tag(c, ILLUS, bx, by + bs + 34, ka)
        # the claim
        x0 = 760
        rich(c, 'Zero human games.', x0, 300, 60, 1100, t, 0.8, 0.06, 0.6, window(t, 0.8, 22.8, d_out=0.5), base_w=600)
        rich(c, '{y:So where did it come from?}', x0, 300, 60, 1100, t, 23.5, 0.06, 0.6, ramp(t, 23.5, 0.6), base_w=600)
        # inputs: short to write down
        for j, (title, lines_) in enumerate((('the rules of chess', ['pieces, moves, checkmate', '≈ one page']),
                                            ('a learning algorithm', ['self-play + search', '+ gradient descent']))):
            k = ramp(t, 4.5 + j * 0.5, 0.8, e_expo)
            if k <= 0:
                continue
            x = x0 + j * 360
            with layer(c, k):
                with xform(c, 0, (1 - k) * 24):
                    panel(c, x, 360, 330, 150, stroke='line')
                    text(c, title, x + 24, 408, 28, 400, 'ink', 1, kind='italic')
                    for q, ln in enumerate(lines_):
                        text(c, ln, x + 24, 448 + q * 30, 19, 500, 'muted', 1, kind='mono')
        kn = ramp(t, 6.5, 0.6)
        text(c, 'both short to write down', x0 + 345, 548, 20, 500, 'muted', kn, 'center', kind='mono')
        # the result: megabytes of weights
        kw = ramp(t, 10.0, 0.8)
        if kw > 0:
            arrow(c, x0 + 345, 566, x0 + 345, 620, 'muted', kw, 2.4, 12, prog=ramp(t, 10.0, 0.6, e_io))
            text(c, 'thousands of TPU hours of self-play', x0 + 375, 602, 19, 500, 'muted', kw, kind='mono')
            cw = 680 / 46
            fill = ramp(t, 10.6, 4.5, e_io)
            ncols = int(46 * fill)
            for r in range(16):
                for q in range(ncols):
                    v = self.weights[r, q]
                    rrect(c, x0 + q * cw, 640 + r * cw, cw - 2, cw - 2, 2, fill=mix('faint', PAL['y'], v),
                          fa=kw * (1 - 0.55 * ramp(t, 16.8, 0.6)))
            kt = ramp(t, 14.0, 0.7)
            text(c, 'megabytes of weights', x0, 900, 30, 400, 'y', kt, kind='italic')
            text(c, '→  superhuman play', x0 + 330, 900, 26, 500, 'ink', kt)
        # the verdicts
        ks = ramp(t, 17.0, 0.5, e_back)
        stamp(c, 'shannon: ≈ nothing new', x0 + 330, 735, 'c', window(t, 17.0, None), ks, rot=-5, size=30)
        ks2 = ramp(t, 18.2, 0.5, e_back)
        stamp(c, 'kolmogorov: ≈ nothing new', x0 + 370, 815, 'c', window(t, 18.2, None), ks2, rot=4, size=30)

# ======================================================================= TITLE
class Title(TitleCard):
    dur = 10.0

# ======================================================================= SHANNON
class Shannon(Scene):
    """Surprise, entropy, and the data processing inequality (Shannon 1948; §2.1, §5.1)."""
    dur = 31.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (6.5, 'pop'), (13.5, 'pop'), (20.5, 'draw')]
    ITEMS = [(1 / 2, 'a fair coin lands heads', 'g'), (1 / 6, 'a die shows six', 'g'), (1 / 1024, 'ten heads in a row', 'y')]

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the classic view', 'Information as *surprise*',
            sub='Claude Shannon, “A Mathematical Theory of Communication”, 1948')
        # left: surprise of single outcomes
        kp = ramp(t, 6.0, 0.7)
        if kp > 0:
            panel(c, MX, 350, 800, 560, kp)
            tex(c, 'surprise', MX + 400, 425, 50, kp)
            for i, (p, lab, colr) in enumerate(self.ITEMS):
                ti = 7.5 + i * 1.2
                k = ramp(t, ti, 0.6)
                if k <= 0:
                    continue
                bits = math.log2(1 / p)
                y = 540 + i * 110
                text(c, lab, MX + 40, y, 26, 500, 'ink', k)
                note(c, f'p = 1/{round(1 / p)}', MX + 40, y + 32, k, 18)
                bw = bits * 32 * ramp(t, ti + 0.2, 0.8, e_expo)
                rrect(c, MX + 360, y - 24, max(bw, 2), 34, 6, fill=colr, fa=k * 0.85)
                text(c, f'{bits:.3g} bit' + ('' if abs(bits - 1) < 1e-6 else 's'), MX + 372 + bw, y + 2, 22, 600, colr, k, kind='mono')
        # right: entropy
        ke = ramp(t, 13.5, 0.8)
        if ke > 0:
            panel(c, 980, 350, 820, 260, ke)
            kicker(c, 'entropy: average surprise', 1010, 392, ke, 'muted', 17)
            tex(c, 'entropy', 1390, 470, 50, ke)
            text(c, '= the shortest average code length for a source', 1390, 572, 22, 500, 'muted', ramp(t, 15.0, 0.7), 'center')
        # right bottom: processing can't add information
        kd = ramp(t, 20.5, 0.8)
        if kd > 0:
            panel(c, 980, 640, 820, 270, kd)
            kicker(c, 'the data processing rule', 1010, 682, kd, 'muted', 17)
            y = 760
            rng = np.random.default_rng(2)
            bits_row(c, rng.integers(0, 2, 12), 1020, y - 18, 18, kd, 'g')
            text(c, 'X', 1128, y + 40, 24, 400, 'g', kd, 'center', kind='italic')
            arrow(c, 1250, y - 8, 1330, y - 8, 'muted', kd, 2.4, 12, prog=ramp(t, 21.0, 0.5, e_io))
            kf = ramp(t, 21.3, 0.5)
            rrect(c, 1345, y - 40, 90, 64, 12, fill='panel2', stroke='ink', sw=1.6, a=kf)
            text(c, 'f', 1390, y + 2, 34, 400, 'ink', kf, 'center', kind='italic')
            arrow(c, 1450, y - 8, 1530, y - 8, 'muted', kf, 2.4, 12, prog=ramp(t, 21.6, 0.5, e_io))
            ko = ramp(t, 21.9, 0.5)
            bits_row(c, (rng.integers(0, 2, 12) * 0 + np.array([1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0])), 1550, y - 18, 18, ko, 'g')
            text(c, 'f(X)', 1658, y + 40, 24, 400, 'g', ko, 'center', kind='italic')
            tex(c, 'dpi', 1390, 870, 40, ramp(t, 22.5, 0.7))

# ======================================================================= KOLMOGOROV
class Kolmogorov(Scene):
    """One string's information = its shortest program (Def. 1); random = incompressible; K(f(x)) <= K(x) + K(f) + c."""
    dur = 28.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (9.0, 'pop'), (13.5, 'pop'), (20.5, 'tick')]

    def __init__(self):
        self.rand = np.random.default_rng(11).integers(0, 2, 56)

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the classic view', 'Information as the *shortest* program',
            sub='Solomonoff 1964  ·  Kolmogorov 1965  ·  Chaitin 1966: one string at a time')
        tex(c, 'kdef', W / 2, 395, 50, ramp(t, 1.5, 0.8))
        note(c, 'K(x): the length of the shortest program p that makes a universal computer U print x', W / 2, 452,
             ramp(t, 2.5, 0.7), 18, 'muted', 'center')
        rows = [(9.0, np.tile([0, 1], 28), 'zero one, repeated half a million times', ['print("01" * 500_000)'], '≈ 25 characters', 'f'),
                (13.5, self.rand, 'a million coin flips', ['print("1101000111010010110…', '       …0110100101110100")'],
                 '≈ 1,000,000 bits', 'c')]
        for i, (ti, bits, lab, code, verdict, colr) in enumerate(rows):
            k = ramp(t, ti, 0.7)
            if k <= 0:
                continue
            y = 520 + i * 180
            text(c, lab, MX, y, 24, 500, 'ink', k)
            bits_row(c, bits, MX, y + 22, 13.5, k, 'g', t, ti, 0.02)
            code_card(c, 930, y - 28, 560, code, k, 19, h=104 if len(code) > 1 else 74)
            kv = ramp(t, ti + 1.0, 0.6)
            text(c, verdict, 1520, y + 18, 22, 600, colr, kv, kind='mono')
            if i == 1:
                text(c, 'no shorter program', 1520, y + 48, 18, 500, 'muted', kv, kind='mono')
        kr = ramp(t, 16.0, 0.7)
        text(c, 'random = incompressible  (Martin-Löf, 1966)', MX, 900, 24, 400, 'muted', kr, kind='italic')
        kk = ramp(t, 20.5, 0.8)
        if kk > 0:
            tex(c, 'kf', 1380, 895, 42, kk)

# ======================================================================= THE CRACK
class Crack(Scene):
    """A pseudorandom generator (Def. 3, Yao's next-bit test) and our compressor check (ours_compress.json)."""
    dur = 33.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (1.2, 'draw'), (7.5, 'pop'), (13.0, 'pop'), (20.0, 'tick')]

    def __init__(self):
        self.seed = _sha_bits(64, b'the seed')
        self.field = _sha_bits(96 * 19).reshape(19, 96)
        self.comp = tdata('ours_compress.json')['results']

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the crack', 'Random to *whom*?',
            sub='a pseudorandom generator stretches a short seed into a long stream, deterministically')
        k0 = ramp(t, 0.8, 0.7)
        # seed
        if k0 > 0:
            for r in range(8):
                bits_row(c, self.seed[r * 8:(r + 1) * 8], MX + 10, 360 + r * 22, 22, k0, 'y')
            text(c, 'seed: 64 bits', MX + 10, 570, 20, 500, 'y', k0, kind='mono')
            arrow(c, 330, 448, 400, 448, 'muted', k0, 2.5, 12, prog=ramp(t, 1.2, 0.5, e_io))
            rrect(c, 410, 410, 110, 76, 14, fill='panel2', stroke='ink', sw=1.6, a=k0)
            text(c, 'G', 465, 462, 40, 400, 'ink', k0, 'center', kind='italic')
            arrow(c, 530, 448, 600, 448, 'muted', k0, 2.5, 12, prog=ramp(t, 1.6, 0.5, e_io))
            draw_eca(c, self.field, 620, 352, 1180, t, 1.8, 14, color='g', bg_a=0.12, gap=0.22)
            text(c, '1,000,000 bits out  (a slice shown; SHA-256 in counter mode)', 1800, 620, 18, 500, 'muted',
                 ramp(t, 3.0, 0.6), 'right', kind='mono')
        # verdicts
        V = [(7.5, 'shannon', '64 bits: only the seed was random', 'v'),
             (8.6, 'kolmogorov', '≈ 64 bits + a short program', 'v'),
             (13.0, 'efficient learner', 'next bit = a coin toss: a million bits of noise', 'g')]
        for i, (ti, who, what, colr) in enumerate(V):
            k = ramp(t, ti, 0.7, e_expo)
            if k <= 0:
                continue
            y = 650 + i * 92
            with layer(c, k):
                with xform(c, (1 - k) * -30, 0):
                    panel(c, MX, y, 860, 76, stroke=colr if i == 2 else 'line')
                    text(c, who, MX + 24, y + 48, 22, 600, 'ink' if i < 2 else 'g', 1, kind='mono')
                    text(c, what, MX + 290, y + 48, 22, 500, 'muted' if i < 2 else 'ink', 1)
        note(c, 'cryptographic pseudorandomness: Blum & Micali 1982, Yao 1982', MX, 940, ramp(t, 14.5, 0.6), 16)
        # our check: compressed bits per input bit
        kc = ramp(t, 20.0, 0.7)
        if kc > 0:
            x, y, w = 1080, 650, 560
            panel(c, x - 30, y - 18, 750, 300, kc)
            kicker(c, 'compressed size, bits per bit', x, y + 18, kc, 'muted', 16)
            tag(c, CHECK + '  ·  1,048,576 bits each', x + 690, y + 18, kc, 'right')
            rows = [('all zeros', 'zeros', 'f'), ('coin flips', 'coin', 'g'), ('pseudorandom', 'prng', 'y'), ('rule 30 rows', 'rule30', 'r')]
            for i, (lab, key, colr) in enumerate(rows):
                yy = y + 64 + i * 50
                kk = ramp(t, 20.3 + i * 0.35, 0.6) * kc
                text(c, lab, x, yy + 18, 21, 500, 'ink', kk)
                for j, comp in enumerate(('gzip', 'xz')):
                    v = self.comp[key][comp]
                    bw = 300 * min(v, 1.05) * ramp(t, 20.3 + i * 0.35, 0.9, e_expo)
                    rrect(c, x + 190, yy + j * 16, max(bw, 2), 12, 3, fill=colr, fa=kk * (0.95 if j == 0 else 0.6))
                text(c, f'{self.comp[key]["gzip"]:.3f} / {self.comp[key]["xz"]:.3f}', x + 520, yy + 22, 19, 600, colr, kk, kind='mono')
            note(c, 'top bar gzip, lower bar xz', x, y + 280, kc * 0.9, 15)
        caption(c, t, 'Both theories assume an observer with {y:unlimited compute}.', 27.5, None, y=1000, size=32)

# ======================================================================= THE OBSERVER
class Observer(Scene):
    """Def. 7-8: the shortest two-part code among programs that sample and evaluate within time T; S_T and H_T."""
    dur = 34.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (5.5, 'pop'), (11.0, 'draw'), (19.5, 'pop'), (26.5, 'pop')]
    # candidate models: (program bits, data bits) in arbitrary units; the middle one has the shortest total
    CANDS = [('memorize nothing:  a coin', 40, 760, False), ('a good model', 330, 300, True), ('memorize everything', 690, 120, False)]
    CHIPS = [(70, 0.3), (210, 0.9), (120, 0.2), (340, 0.6), (90, 1.4), (260, 0.5), (180, 1.8), (300, 0.8), (150, 0.4),
             (230, 2.2), (110, 0.7), (280, 1.1)]

    def draw(self, c, t):
        hdr(self, c, t, '02', 'the idea', 'Put the *observer* in the definition',
            sub='Def. 8: among programs that run within a time budget T, the shortest two-part code wins')
        dial = 0.15 + 0.4 * ramp(t, 1.0, 2.5, e_io)
        observer(c, 300, 500, 1.15, ramp(t, 0.6, 0.8), dial, t, 'time budget  T')
        # programs within T (the rest are too slow)
        kc = window(t, 5.5, 10.6, 0.6, 0.6)
        if kc > 0:
            note(c, 'programs that can sample the data and score it', 620, 380, kc, 18, 'ink')
            for i, (L, runtime) in enumerate(self.CHIPS):
                r, q = divmod(i, 4)
                x, y = 620 + q * 290, 420 + r * 82
                k = ramp(t, 5.8 + i * 0.08, 0.4) * kc
                slow = runtime > 1.0
                ks = ramp(t, 8.0, 0.6) if slow else 0
                rrect(c, x, y, 260, 60, 10, fill='panel2', stroke='muted' if not slow else 'r', sw=1.4, a=k * (1 - 0.6 * ks))
                rrect(c, x + 14, y + 22, L * 0.5, 16, 4, fill='y', fa=k * 0.8 * (1 - 0.6 * ks))
                text(c, f'{runtime:.1f} T', x + 246, y + 38, 17, 500, 'r' if slow else 'muted', k, 'right', kind='mono')
                if ks > 0:
                    line(c, x + 8, y + 30, x + 8 + 244 * ks, y + 30, 'r', k * 0.9, 2.5)
            note(c, 'too slow: over budget', 1780, 690, ramp(t, 8.2, 0.6) * kc, 16, 'r', 'right')
        # two-part codes
        kb = ramp(t, 11.0, 0.7)
        if kb > 0:
            tex(c, 'pstar', 1190, 410, 46, kb)
            for i, (lab, pb, db, best) in enumerate(self.CANDS):
                y = 520 + i * 92
                k = ramp(t, 11.8 + i * 0.6, 0.7)
                if k <= 0:
                    continue
                text(c, lab, 620, y + 30, 22, 500, 'ink' if best else 'muted', k)
                x = 960
                prog = ramp(t, 11.8 + i * 0.6, 1.0, e_expo)
                info_bar(c, x, y, pb * 0.9, db * 0.9, 42, k, labels=False, prog=prog)
                tot = (pb + db) * 0.9
                kbst = ramp(t, 15.5, 0.6)
                if best:
                    rrect(c, x - 10, y - 10, tot * prog + 20, 62, 12, stroke='y', sw=2.5, a=kbst, glow=8)
                    text(c, 'P★  shortest total', x + tot + 24, y + 30, 22, 600, 'y', kbst, kind='mono')
            kl = ramp(t, 12.4, 0.6)
            text(c, 'bits for the program', 960, 500, 18, 500, S_COL, kl, kind='mono')
            text(c, '+ bits for the data, encoded with it', 1260, 500, 18, 500, H_COL, kl, kind='mono')
        # S_T and H_T
        ks = ramp(t, 19.5, 0.8)
        if ks > 0:
            panel(c, 620, 820, 560, 120, ks, stroke=S_COL)
            tex(c, 'st', 900, 862, 40, ks)
            text(c, 'epiplexity: the structure it can learn', 900, 918, 21, 500, 'ink', ks, 'center')
        kh = ramp(t, 26.5, 0.8)
        if kh > 0:
            panel(c, 1220, 820, 580, 120, kh, stroke=H_COL)
            tex(c, 'ht', 1510, 858, 38, kh)
            text(c, 'time-bounded entropy: what looks random to it', 1510, 918, 21, 500, 'ink', kh, 'center')

# ======================================================================= SPECTRUM
class Spectrum(Scene):
    """The bar for simple objects (§3: uniform bits, 0101..), a PRG (Thm 9), and Fig. 1's code examples (illustration)."""
    dur = 32.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (0.6, 'pop'), (5.5, 'pop'), (9.0, 'pop'), (17.5, 'tick')]
    CODE = [(18.5, 'config with random keys', ['API_KEY = "sk_7aF2jK1ycP9LmvYzz34"', 'USER_ID = "usr_4f8a2c1e9b7d3065"',
                                                'SEED = 9284715'], 30, 560),
            (21.0, 'repetitive code', ['def is_even(n):', '  if n == 0: return True', '  elif n == 1: return False', '  ...'], 26, 70),
            (23.5, 'a real algorithm', ['def dijkstra(g, s):', '  D[s] = 0; q = [(0, s)]', '  while q: d, u = pop(q) ...'], 420, 230)]

    def __init__(self):
        rng = np.random.default_rng(8)
        self.coin = rng.integers(0, 2, 40)
        self.prng = _sha_bits(40, b'spectrum')

    def draw(self, c, t):
        hdr(self, c, t, '02', 'the idea', 'Structure and *randomness*, object by object',
            sub='bars are illustrations of the definitions (§3, Thm 9; code examples after Fig. 1)')
        rows = [(0.6, 'a string of zeros', np.zeros(40, int), 3, 6, 'almost nothing of either'),
                (5.5, 'coin flips', self.coin, 3, 640, 'all randomness'),
                (9.0, 'pseudorandom bits', self.prng, 6, 632, 'nearly all randomness')]
        for i, (ti, lab, bits, s_w, h_w, verdict) in enumerate(rows):
            k = ramp(t, ti, 0.7)
            if k <= 0:
                continue
            y = 410 + i * 160
            text(c, lab, MX, y, 26, 500, 'ink', k)
            bits_row(c, bits, MX + 330, y - 20, 14, k, 'g')
            info_bar(c, MX, y + 32, s_w, h_w, 40, k, labels=False, prog=ramp(t, ti + 0.3, 1.0, e_expo))
            text(c, verdict, MX + max(s_w + h_w, 60) + 20, y + 62, 20, 500, 'muted', ramp(t, ti + 0.8, 0.5), kind='mono')
        bar_legend(c, MX, 330, ramp(t, 0.9, 0.6))
        kt = ramp(t, 11.0, 0.8)
        if kt > 0:
            tex(c, 'thm9', MX + 330, 920, 30, kt)
            note(c, 'Theorem 9: for a secure generator, against any polynomial-time observer', MX, 870, kt, 16)
        # Fig. 1's examples
        for i, (ti, title, lines_, s_w, h_w) in enumerate(self.CODE):
            k = ramp(t, ti, 0.7, e_expo)
            if k <= 0:
                continue
            y = 360 + i * 200
            with layer(c, k):
                hh = code_card(c, 1100, y, 700, lines_, 1, 17, title=title, lh=1.35)
                info_bar(c, 1100, y + hh + 10, s_w, h_w, 22, 1, labels=False, prog=ramp(t, ti + 0.4, 0.9, e_expo))
        tag(c, ILLUS + ' · after Fig. 1', 1800, 990, ramp(t, 18.5, 0.6), 'right')

# ======================================================================= MEASURING
def _sketch(kind, n=200):
    """Illustration loss curves (not data): random stays flat, simple drops at once, structured keeps improving."""
    x = np.linspace(0, 1, n)
    if kind == 'random':
        y = 1.0 + 0.012 * np.sin(x * 60)
    elif kind == 'simple':
        y = 0.08 + 0.92 * np.exp(-x / 0.03)
    else:
        y = 0.3 + 0.7 * np.exp(-x / 0.33) - 0.1 * x
    return x, y

class Measuring(Scene):
    """§4: prequential (eq. 8, a heuristic), requential (eq. 9, explicit, 2-10x slower), Fig. 2c (data)."""
    dur = 37.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (1.0, 'draw'), (15.0, 'pop'), (23.0, 'pop'), (31.0, 'pop')]

    def __init__(self):
        self.f2c = tdata('fig2c_preq_req.json')

    def draw(self, c, t):
        hdr(self, c, t, '02', 'measuring it', 'Structure is the area *under* the curve',
            sub='§4: train a network as the observer; read structure off its loss curve')
        ax = LinAxes(200, 390, 760, 300, (0, 1), (0, 1.1))
        ka = ramp(t, 0.6, 0.7)
        if ka > 0:
            ax.draw(c, ka, (), (), grid=False)
            text(c, 'training data seen  →', 960, 728, 19, 500, 'muted', ka, 'right', kind='mono')
            text(c, 'loss', 200, 372, 19, 500, 'muted', ka, kind='mono')
            x, y = _sketch('structured')
            fin = loss_curve(c, ax, x, y, 'y', t, 1.0, 3.5, final=float(y[-1]), area=t >= 6.5, fa=0.28 * ramp(t, 6.5, 1.0))
            _, Yf = ax.px(0, fin)
            kf = ramp(t, 6.5, 0.6)
            line(c, 200, Yf, 960, Yf, 'muted', kf, 1.4, dash=[8, 6])
            text(c, 'final loss', 950, Yf - 12, 17, 500, 'muted', kf, 'right', kind='mono')
            text(c, 'area = structure absorbed', 470, 540, 24, 400, 'y', ramp(t, 7.5, 0.6), kind='italic')
            tag(c, ILLUS + ' (curves)', 200, 728, ka)
            tex(c, 'preq', 580, 800, 32, ramp(t, 9.0, 0.7))
            note(c, 'prequential: a heuristic (eq. 8)', 580, 852, ramp(t, 9.5, 0.7), 16, 'muted', 'center')
        # three regimes (illustrations)
        kr = window(t, 15.0, 30.4, 0.6, 0.6)
        for i, (kind, lab, colr) in enumerate((('random', 'random: no area', 'g'), ('simple', 'simple: a sliver', 'f'),
                                                ('structured', 'structured: keeps paying off', 'y'))):
            ti = 15.0 + i * 1.6
            k = ramp(t, ti, 0.6) * kr
            if k <= 0:
                continue
            y0 = 380 + i * 175
            mx = LinAxes(1180, y0, 300, 120, (0, 1), (0, 1.1))
            mx.draw(c, k, (), (), grid=False)
            x, y = _sketch(kind)
            loss_curve(c, mx, x, y, colr, t, ti, 1.2, final=float(y[-1]), fa=0.3, w=2.5, a=k)
            text(c, lab, 1510, y0 + 70, 22, 500, colr, k)
        # requential
        kq = ramp(t, 23.0, 0.7)
        if kq > 0:
            k2 = kq * (1 - ramp(t, 30.4, 0.6)) if False else kq
            tex(c, 'req', 580, 915, 30, kq)
            note(c, 'requential: a student trained on a teacher’s samples; explicit, 2-10× slower (eq. 9)', 580, 965,
                 kq, 16, 'muted', 'center')
        # Fig. 2c
        kd = ramp(t, 31.0, 0.7)
        if kd > 0:
            # the paper's panel ticks (Fig. 2c), each panel on its own linear axes
            groups = [('ECA', (0, 1.0), (0, 5.0), (0, 0.5, 1.0), (0, 2.5, 5.0)),
                      ('Induct Easy', (0.05, 1.0), (3.8, 6.6), (0.1, 0.5, 0.9), (4, 5, 6)),
                      ('Induct Hard', (0.4, 1.05), (3.5, 6.6), (0.5, 0.75, 1.0), (4, 5, 6)),
                      ('Natural', (5, 52), (5, 95), (10, 30, 50), (10, 50, 90))]
            for i, (g, xr, yr, xt, yt) in enumerate(groups):
                d = self.f2c['groups'][g]
                r, q = divmod(i, 2)
                x0, y0 = 1180 + q * 330, 400 + r * 240
                ax2 = LinAxes(x0, y0, 240, 140, xr, yr)
                ax2.draw(c, kd, (), (), grid=False)
                for v in xt:
                    X, _ = ax2.px(v, yr[0])
                    text(c, f'{v:g}', float(X), y0 + 140 + 22, 14, 500, 'muted', kd, 'center', kind='mono')
                for v in yt:
                    _, Y = ax2.px(xr[0], v)
                    text(c, f'{v:g}', x0 - 8, float(Y) + 5, 14, 500, 'muted', kd, 'right', kind='mono')
                text(c, g.lower(), x0 + 4, y0 - 10, 17, 500, 'ink', kd, kind='mono')
                for j, (xx, yy) in enumerate(zip(d['S_req_MB'], d['S_preq_MB'])):
                    kk = ramp(t, 31.3 + j * 0.05 + i * 0.2, 0.4) * kd
                    X, Y = ax2.px(xx, yy)
                    circle(c, float(X), float(Y), 6, fill=d['color'], stroke='ink', sw=1, a=kk)
            note(c, 'across: requential (MB)   up: prequential (MB)', 1150, 880, kd, 16, 'muted')
            src(c, 'Fig. 2c', 1150, 906, kd)
