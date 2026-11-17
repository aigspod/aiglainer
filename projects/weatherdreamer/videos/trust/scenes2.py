"""Clue three to the verdict (arXiv:2611.18393v1 §4.1, §4.2, §5, Text S5.3, S6.2, S6.4; Figs. 4, S3).
Numbers are typed from the text with the section named on screen; paper figures are labelled crops."""
from trustkit import *
from scenes1 import S3_A, S3_B, s3map

# ======================================================================= CLUE 3: THINGS IT NEVER SEES
class Unseen(Scene):
    """§4.2.3, Fig. 6d-h: cloud-top height vs EarthCARE (radar + lidar, never in training); §4.2.1: precipitation."""
    dur = 34.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (9.0, 'pop'), (19.5, 'pop'), (27.0, 'pop')]
    # (metric, WeatherDreamer, GOES ACHA, better is higher?, start)     §4.2.3
    ROWS = [('correlation with the radar', '0.73', '0.70', 'WD', 9.0),
            ('height error (RMSE)', '4.4 km', '4.8 km', 'WD', 10.5),
            ('cloud / clear skill (ETS)', '0.39', '0.28', 'WD', 12.0),
            ('false-alarm ratio', '0.09', '0.19', 'WD', 19.5),
            ('probability of detection', '0.80', '0.90', 'ACHA', 21.5)]

    def draw(self, c, t):
        hdr(c, t, '04', 'clue three', 'What it was never *shown*', sub='never inputs while forecasting: read out of the inner state')
        exhibit(c, 1500, 190, 'exhibit c', ramp(t, 0.6, 0.5), ramp(t, 0.6, 0.5, e_back))
        px_ = MX
        for i, s in enumerate(('cloud-top height', 'rain', 'sunlight at the ground')):
            pill(c, px_, 330, s, 'y', ramp(t, 2.0 + i * 0.3, 0.5), size=17)
            px_ += text_width(s, 17, 400, 'mono', 0.12) + 54
        # the scorecard vs EarthCARE
        x, y0, dy = MX, 470, 62
        ka = ramp(t, 9.0, 0.6)
        if ka > 0:
            text(c, 'cloud tops vs EarthCARE (radar + lidar; never seen in training)', x, y0 - 30, 20, 500, 'muted', ka, kind='mono')
            text(c, 'weatherdreamer', x + 640, y0 + 6, 18, 600, 'y', ka, 'center', kind='mono')
            text(c, 'operational (GOES ACHA)', x + 900, y0 + 6, 18, 600, 'g', ka, 'center', kind='mono')
        for i, (lab, a_, b_, win, t0) in enumerate(self.ROWS):
            k = ramp(t, t0, 0.5)
            if k <= 0:
                continue
            y = y0 + 60 + i * dy
            panel(c, x, y - 34, 1060, 52, k, r=10)
            text(c, lab, x + 20, y + 0, 22, 500, 'ink', k)
            text(c, a_, x + 640, y + 0, 26, 700 if win == 'WD' else 500, 'y', k, 'center', kind='mono')
            text(c, b_, x + 900, y + 0, 26, 700 if win != 'WD' else 500, 'g', k, 'center', kind='mono')
            mx = x + 640 if win == 'WD' else x + 900
            circle(c, mx + 70, y - 8, 7, fill='f', a=k)
        src(c, '§4.2.3, Fig. 6 (28 analyses, 154,860 cloudy footprints)', x, y0 + 60 + 5 * dy, ka)
        # rain
        kr = ramp(t, 27.0, 0.7)
        if kr > 0:
            px, py = 1270, 470
            panel(c, px, py - 40, 530, 400, kr)
            text(c, 'rain (vs IMERG)', px + 28, py + 6, 22, 600, 'ink', kr, kind='mono')
            lines_ = [('best of 3 ensembles to +6 h', 'f'), ('CRPS at +3 h: 0.255 vs 0.310, 0.331 mm', 'muted'),
                      ('≈ ⅔ of the observed rain', 'c'), ('too smooth: 33% vs 56–57% of', 'c'), ('  power below 1,000 km', 'c')]
            for j, (s, colr) in enumerate(lines_):
                text(c, s, px + 28, py + 62 + j * 52, 22, 500, colr, ramp(t, 27.2 + j * 0.3, 0.5))
            src(c, '§4.2.1', px + 28, py + 330, kr)

# ======================================================================= THE TWIST: LEARNED RETRIEVAL
class Twist(Scene):
    """Who uses what: Text S5.3 (cloud-top head learns principally from geostationary IR), §4.2.3 (ACHA from GOES),
    §4.2.1 (IMERG partly from ATMS and geostationary IR). NSRDB being GOES-derived is background, said as such."""
    dur = 28.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (5.0, 'draw'), (12.0, 'draw'), (20.5, 'chime')]

    def node(self, c, x, y, w, s, colr, a, sub=None):
        if a <= 0:
            return
        rrect(c, x, y - 34, w, 68 if not sub else 84, 14, fill='panel', fa=a * 0.95, stroke=colr, sw=2.2, a=a)
        text(c, s, x + w / 2, y + 8, 22, 600, 'ink', a, 'center')
        if sub:
            text(c, sub, x + w / 2, y + 36, 15, 500, 'muted', a, 'center', kind='mono')

    def draw(self, c, t):
        hdr(c, t, '04', 'the twist', 'Inferred is not *clairvoyant*')
        k0 = ramp(t, 0.6, 0.6)
        # sources (left)
        L, M, R = MX, 760, 1360
        self.node(c, L, 420, 440, 'geostationary infrared', 'g', k0, 'goes, meteosat, gk2a')
        self.node(c, L, 640, 440, 'microwave sounders', 'g', k0, 'atms')
        self.node(c, M, 530, 380, 'WeatherDreamer', 'y', k0)
        km = ramp(t, 0.8, 0.8, e_io)
        arrow(c, L + 440, 420, M, 520, 'y', k0, 2.5, 12, prog=km)
        arrow(c, L + 440, 640, M, 545, 'y', k0, 2.5, 12, prog=km)
        # products built from the same sources (right)
        prods = [('cloud tops (ACHA)', 360, 5.0, 'from goes radiances'), ('rain (IMERG)', 530, 12.0, 'partly from atms + geo ir'),
                 ('sunlight (NSRDB)', 700, 13.5, 'derived from goes: background')]
        for (s, y, t0, sub) in prods:
            k = ramp(t, t0, 0.6)
            self.node(c, R, y, 440, s, 'c', k, sub)
            arrow(c, L + 440, 420 if 'IMERG' not in s else 640, R, y, 'c', k * 0.8, 2, 10, prog=ramp(t, t0, 0.8, e_io), dash=[8, 6])
        self.node(c, M, 530, 380, 'WeatherDreamer', 'y', k0)
        ki = ramp(t, 20.5, 0.6)
        if ki > 0:
            panel(c, MX, 820, W - 2 * MX, 110, ki)
            text(c, 'independent checks:', MX + 30, 870, 22, 600, 'f', ki, kind='mono')
            text(c, 'EarthCARE radar + lidar (cloud tops)   ·   ground sunlight stations, USCRN + SOLRAD', MX + 330, 870, 22, 500, 'ink', ki)
            text(c, 'learned retrieval, and good retrieval: not evidence of seeing beyond its inputs', MX + 30, 908, 19, 500, 'muted', ki, kind='mono')
        tag(c, 'who uses what: §4.2, Text S5.3, S6.6', MX, 985, k0)

# ======================================================================= THE SCOREBOARD: CLOCKS
class Clocks(Scene):
    """§4.1, Fig. 4a; Text S6.2 (operational latency: GEFS cycle >= 5 h old, IFS ENS >= 7 h old)."""
    dur = 38.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (9.5, 'draw'), (19.0, 'pop'), (26.5, 'pop')]

    def draw(self, c, t):
        hdr(c, t, '05', 'the scoreboard', 'Check the *clocks*')
        k0 = ramp(t, 0.6, 0.6)
        if k0 > 0:
            for i, s in enumerate(('2 m temperature', '2 m dew point', '10 m wind')):
                pill(c, MX + i * 270, 300, s, 'f', ramp(t, 0.8 + i * 0.3, 0.5), size=16)
            text(c, 'beats GEFS (US ensemble) at every lead to 12 h, at 534 held-out stations', MX, 380, 22, 500, 'ink', k0)
        # timeline in hours
        ax0, ax1, ty, h0, h1 = MX + 40, 1060, 560, -8, 16
        X = lambda hh: ax0 + (hh - h0) / (h1 - h0) * (ax1 - ax0)
        kt = ramp(t, 9.5, 0.6)
        if kt > 0:
            line(c, ax0, ty, ax1, ty, 'muted', kt, 2)
            for hh in range(h0, h1 + 1, 4):
                line(c, X(hh), ty - 6, X(hh), ty + 6, 'muted', kt, 2)
                text(c, f'{hh:+d} h' if hh else 'start', X(hh), ty + 36, 18, 500, 'muted', kt, 'center', kind='mono')
            # WeatherDreamer: hourly analyses up to the start
            for hh in range(-7, 1):
                circle(c, X(hh), ty - 40, 6, fill='y', a=kt * (0.5 + 0.5 * (hh == 0)))
            text(c, 'WeatherDreamer: fresh analysis every hour', X(-8), ty - 70, 18, 600, 'y', kt, kind='mono')
            for j, (lab, hh, colr, yy) in enumerate((('GEFS cycle, ≥ 5 h old', -5, 'c', ty + 90), ('IFS ENS cycle, ≥ 7 h old', -7, 'g', ty + 150))):
                k = ramp(t, 11.5 + j * 1.2, 0.6)
                circle(c, X(hh), yy, 9, fill=colr, a=k)
                arrow(c, X(hh) + 12, yy, X(h1), yy, colr, k * 0.7, 2.5, 10, prog=ramp(t, 11.5 + j * 1.2, 1.0, e_io), dash=[10, 6])
                text(c, lab, X(hh) - 8, yy - 18, 18, 600, colr, k, kind='mono')
            ko = ramp(t, 19.0, 0.6)
            if ko > 0:
                line(c, X(8), ty - 100, X(8), ty - 14, 'g', ko, 2.5, dash=[6, 6])
                line(c, X(8), ty + 50, X(8), ty + 190, 'g', ko, 2.5, dash=[6, 6])
                text(c, '+8 h: IFS ENS overtakes on 2 m temperature,', X(8) + 14, ty + 230, 19, 600, 'g', ko, 'center', kind='mono')
                text(c, 'with a forecast more than 15 h old', X(8) + 14, ty + 258, 19, 600, 'g', ko, 'center', kind='mono')
            src(c, 'Text S6.2 (operational latency), §4.1', MX, 870, kt)
        # Fig. 4a crop: 2 m temperature CRPS
        kf = ramp(t, 19.0, 0.8, e_expo)
        fw, fh = figcard(c, 'fig4', 1210, 400, 520, kf, None, src=(0.050, 0.025, 0.272, 0.238), k=kf)
        if kf > 0:
            note(c, 'Fig. 4a · ' + PAPER + ' · CRPS of 2 m temperature (lower is better)', 1200, 400 + fh + 34, kf, 14)
            note(c, 'x: lead time, analysis to +12 h', 1200, 400 - 22, kf, 14)
            for j, (lab, colr, dash) in enumerate((('WeatherDreamer', '#2f6fde', False), ('no station input', '#8fb1f0', True),
                                                   ('GEFS', '#e8862a', True), ('IFS ENS', '#2a9a6a', True))):
                legend_item(c, 1210 + (j % 2) * 290, 400 + fh + 70 + (j // 2) * 30, colr, lab, kf, dash, size=17)
        kp = ramp(t, 26.5, 0.6)
        if kp > 0:
            panel(c, MX, 920, 1700, 78, kp)
            rich(c, 'its lead comes largely from {y:spread}: on ensemble-mean error it beats IFS ENS only for temperature, '
                    'for 3 h  ·  spread–skill 0.63–0.78 vs 0.23–0.47 and 0.26–0.41 (all under-dispersive)',
                 MX + 26, 950, 19, 1650, base_w=500, a=kp)

# ======================================================================= THE SCOREBOARD: FINE PRINT
class FinePrint(Scene):
    """§4.1, §5 (representativeness; held-out stations; ~200 km), Text S6.4 (no lapse-rate adjustment: our reading), COI."""
    dur = 36.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (0.8, 'stamp_soft'), (6.5, 'stamp_soft'), (15.0, 'stamp_soft'), (22.5, 'stamp_soft'), (27.0, 'chime')]
    CARDS = [('points vs boxes', 'it decodes at each station; the ensembles describe grid boxes (§5)', 0.6, 'muted'),
             ('neighbours', 'held-out stations are a random 5%; the network’s help fades beyond ≈ 200 km (§5)', 6.5, 'muted'),
             ('elevation', 'baselines not adjusted for station height (Text S6.4); our reading: helps it at mountain stations', 15.0, 'y'),
             ('who wrote it', 'all five authors work at Zeus AI, which develops the model (conflict-of-interest statement)', 22.5, 'muted')]

    def draw(self, c, t):
        hdr(c, t, '05', 'the scoreboard', 'The fine *print*')
        for i, (head, body, t0, colr) in enumerate(self.CARDS):
            k = ramp(t, t0, 0.7, e_expo)
            if k <= 0:
                continue
            x = MX + (i % 2) * 850
            y = 320 + (i // 2) * 210
            with layer(c, k):
                with xform(c, 0, (1 - k) * 24):
                    panel(c, x, y, 810, 180)
                    exhibit(c, x + 24, y + 40, head, 1, 1, rot=-2)
                    rich(c, body, x + 30, y + 110, 25, 750, base_w=450, base='ink' if colr != 'y' else 'y')
        ks = ramp(t, 27.0, 0.8, e_expo)
        if ks > 0:
            panel(c, MX, 770, W - 2 * MX, 190, ks, stroke='f')
            text(c, 'what survives', MX + 30, 815, 20, 600, 'f', ks, kind='mono')
            rich(c, 'With {f:no surface stations at all}, it still beats GEFS for temperature to {f:11 h} and wind to {f:12 h}, '
                    'and stays better calibrated (§4.1).', MX + 30, 870, 32, W - 2 * MX - 60, t, 27.2, 0.03, 0.5, base_w=500)

# ======================================================================= THE REVEAL
class Reveal(Scene):
    """Fig. S3: memory h (512) vs latent z (64). Caption: the memory records the observing system, 'analogous to the
    observation-density information a conventional filter carries in its error covariance'; z mostly weather."""
    dur = 36.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (4.0, 'draw'), (12.5, 'pop'), (22.0, 'draw'), (30.0, 'chime')]

    def draw(self, c, t):
        hdr(c, t, '06', 'the reveal', 'Why it remembers the *satellites*')
        xa, xb, y, w = MX, 1000, 330, 800
        ka = ramp(t, 0.6, 0.8, e_expo)
        _, h = figcard(c, 'figS3', xa, y, w, ka, None, src=S3_A, k=ka)
        text(c, 'memory h  ·  512 numbers per cell', xa - 10, y - 26, 22, 600, 'ink', ka, kind='mono')
        kb = ramp(t, 22.0, 0.8, e_expo)
        figcard(c, 'figS3', xb, y, w, kb, None, src=S3_B, k=kb)
        text(c, 'state z  ·  64 numbers per cell (what the decoders read)', xb - 10, y - 26, 22, 600, 'y', kb, kind='mono')
        note(c, 'Fig. S3a, b · ' + PAPER, xa - 10, y + h + 34, ka, 15)
        for i, (r, cc) in enumerate(((1, 2), (3, 0), (1, 4))):
            rx, ry, rw, rh = crop_rect('figS3', S3_A, xa, y, w, s3map(r, cc))
            highlight(c, rx, ry, rw, rh, 'y', window(t, 4.0, 21.5), ramp(t, 4.0 + i * 0.3, 0.6, e_io))
        kq = ramp(t, 12.5, 0.7)
        if kq > 0:
            panel(c, MX, 755, 1680, 140, kq)
            rich(c, '“…a record of the observing system… {y:analogous to the observation-density information a conventional '
                    'filter carries in its error covariance}.”', MX + 30, 805, 27, 1620, t, 12.6, 0.02, 0.4, base_w=400)
            note(c, 'Fig. S3 caption', MX + 30, 878, kq, 14)
        kz = ramp(t, 23.0, 0.6)
        note(c, 'z: “dominated by meteorological structure with a weak', xb, y + h + 34, kz, 15, 'y')
        note(c, '   residual imprint at coverage boundaries”', xb, y + h + 58, kz, 15, 'y')
        rich(c, 'Remembering the satellites isn’t the crime. It’s how a filter {y:knows how sure to be}.', W / 2, 950, 34, 1600,
             t, 30.0, 0.04, 0.5, 1, 'center', base_w=500)

# ======================================================================= THE REAL TEST
class RealTest(Scene):
    """§4.1 (one data-denial run: all surface stations withheld), §5 (data denial is inexpensive), §3.5 (zero state,
    12 h window, continuous cycling left to future work). The z-invariance test is ours, labelled as a proposal."""
    dur = 28.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (3.0, 'draw'), (10.5, 'pop'), (18.0, 'pop')]

    def draw(self, c, t):
        hdr(c, t, '06', 'the real test', 'Atmosphere, or *instruments*?', sub='a false choice: the question is whether z holds still')
        k = ramp(t, 3.0, 0.7)
        if k > 0:
            for j, (lab, sub, y) in enumerate((('observing network A', 'all 18 systems', 420), ('observing network B', 'one satellite swapped or withheld', 640))):
                kk = ramp(t, 3.0 + j * 0.8, 0.6)
                rrect(c, MX, y - 50, 470, 110, 16, fill='panel', fa=kk * 0.95, stroke='g', sw=2, a=kk)
                text(c, lab, MX + 30, y, 26, 600, 'ink', kk)
                text(c, sub, MX + 30, y + 36, 18, 500, 'muted', kk, kind='mono')
                arrow(c, MX + 480, y + 5, 900, 530, 'muted', kk, 2.5, 12, prog=ramp(t, 3.5 + j * 0.8, 0.7, e_io))
            rrect(c, 910, 470, 300, 120, 16, fill='panel', fa=k, stroke='y', sw=2.4, a=k)
            text(c, 'the model', 1060, 540, 30, 400, 'ink', k, 'center', kind='italic')
            kz = ramp(t, 6.0, 0.6)
            arrow(c, 1220, 530, 1360, 530, 'y', kz, 2.5, 12, prog=ramp(t, 6.0, 0.6, e_io))
            text(c, 'z  =  z  ?', 1380, 548, 52, 400, 'y', kz, kind='italic')
            text(c, 'same weather state?', 1380, 600, 20, 500, 'muted', kz, kind='mono')
            tag(c, 'illustration: a test the paper does not run', MX, 770, k)
        kd = ramp(t, 10.5, 0.6)
        if kd > 0:
            text(c, 'done: every surface station withheld (§4.1)   ·   not checked: whether z itself stays put', MX, 830, 22, 500, 'ink', kd)
        kc = ramp(t, 18.0, 0.6)
        if kc > 0:
            panel(c, MX, 870, W - 2 * MX, 90, kc, stroke='c')
            text(c, 'every run starts from an empty memory + 12 h of observations; continuous cycling is future work (§3.5, §5)',
                 MX + 30, 925, 23, 500, 'c', kc)

# ======================================================================= QUESTIONS AND END
class Questions(Scene):
    dur = 24.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (8.5, 'pop'), (15.5, 'pop')]

    def draw(self, c, t):
        hdr(c, t, '07', 'to think about', 'Questions for the *case*')
        question_cards(c, t, [
            ('What experiment would convince you its inner state is {y:the atmosphere}, not the observing network?', 2.0),
            ('It trusts instruments well near the ground and {y:leans lightly} on them high up. Why might training do that?', 8.5),
            ('Should an ensemble get credit for spread that comes from {y:predicting single stations}?', 15.5),
        ])
        note(c, 'our questions, not the paper’s', MX, 900, ramp(t, 2.0, 0.6), 15)

class End(EndCard):
    TAKE = ('It learned {y:whom to trust} near the ground, and {y:where it had been looking}. '
            'It hasn’t yet learned to {c:listen closely} high up.')
    STATS = [('0.2–0.4 K', 'learned microwave noise', 'f'),
             ('2.6×', 'balloon-wind error vs NOAA', 'c'),
             ('83–96%', 'limb darkening removed', 'y')]
