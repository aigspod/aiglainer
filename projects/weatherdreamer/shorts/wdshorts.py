"""Native 9:16 scenes for projects/weatherdreamer/shorts/* (now, stripes, trust, limb, walls).

Each scene has `vertical = True` and draws in aiglainer.short.BOX (720 x 700), origin top-left. Big type: labels
>= 19 px, numbers >= 28 px. Built on the topic kit `loopkit.py` (projects/weatherdreamer/videos/loop), so every short
lists SOURCES = ['weatherdreamer/videos/loop']; each short's project.py puts this folder on sys.path.

Data: numbers are typed from arXiv:2611.18393v1 (section or table beside each); paper figures are crops (Fig. S3, S7)
from projects/weatherdreamer/data/figs (run ../extract_paper.py on a fresh clone). Globes, the thermometer number line,
the slant-path sketch and the patch map are illustrations and say so. "Our arithmetic" is ours and says so.

Scenes, by short:
  now      NowClues (globe of clues), NowCycle (6-hourly, hours late vs hourly in ~1.5 min)
  stripes  StripesMemory (Fig. S3a), StripesWhy (memory h vs state z, Fig. S3b)
  trust    TrustGain (forecast vs thermometer, k = 0.8), TrustLearned (§4.3.3 numbers)
  limb     LimbSlant (slant path, cold limbs), LimbFix (Fig. S7a/c, §4.4 corrections)
  walls    WallsRatio (Table 2 ratios), WallsCauses (patches + light gains aloft, §5, §4.3.3)
"""
from loopkit import *


def lab(c, s, x, y, a=1.0, align='left', color='muted', size=19):
    note(c, s, x, y, a, size, color, align)


def col_chart(c, t, t0, vals, x0, yb, hmax, vmax, slot, bw, colors, labels, fmt, fs=30, stagger=0.25, base=None):
    """Vertical columns from a zero baseline, values on top, labels beneath; base draws a reference line."""
    k0 = ramp(t, t0, 0.6)
    if k0 <= 0:
        return
    line(c, x0 - 6, yb, x0 + slot * len(vals) + 6, yb, 'muted', k0, 1.6)
    if base is not None:
        yy = yb - hmax * base / vmax
        line(c, x0 - 6, yy, x0 + slot * len(vals) + 6, yy, 'ink', k0 * 0.7, 2, dash=[6, 6])
    for i, v in enumerate(vals):
        k = ramp(t, t0 + 0.15 + i * stagger, 0.9, e_expo)
        cx = x0 + slot * (i + 0.5)
        for j, s in enumerate(labels[i].split('\n')):
            text(c, s, cx, yb + 32 + j * 24, 20 if j == 0 else 19, 500, 'ink' if j == 0 else 'muted', k0, 'center',
                 kind='mono')
        if k <= 0:
            continue
        h = hmax * v / vmax * k
        rrect(c, cx - bw / 2, yb - h, bw, max(h, 2), 6, fill=colors[i], fa=0.92)
        text(c, fmt(v), cx, yb - h - 14, fs, 700, colors[i], k, 'center')


# =============================================================== now
class NowClues(Scene):
    """The observing system as clues on a globe (illustration; numbers §2.1)."""
    vertical = True
    dur = 13.0
    cues = [(0.3, 'whoosh_soft'), (5.5, 'blip'), (7.5, 'sweep')]

    def draw(self, c, t):
        g = Globe(360, 330, 300, -70 + 2.5 * t, 22)
        g.draw(c, ramp(t, 0.0, 1.0))
        g.dots(c, STATIONS, 'ink', 3.0, ramp(t, 5.5, 0.8), prog=ramp(t, 5.5, 1.8, e_io))
        g.dots(c, BALLOONS, 'f', 6.0, ramp(t, 6.6, 0.8), prog=ramp(t, 6.6, 1.2, e_io))
        kp = ramp(t, 7.5, 0.8)
        for i in range(5):
            lo, la = polar_track(i, lon_start=-30)
            pr = ramp(t, 7.5 + i * 0.2, 1.6, e_io)
            g.track(c, lo, la, 'g', 14, kp * 0.22, prog=pr)
            g.track(c, lo, la, 'g', 2, kp * 0.75, prog=pr)
        k1 = ramp(t, 5.5, 0.6)
        lab(c, '≈ 11,000 stations', 20, 660, k1, color='ink', size=21)
        lab(c, '≈ 650 balloons', 360, 660, ramp(t, 6.6, 0.6), 'center', 'f', 21)
        lab(c, 'satellites: light', 700, 660, ramp(t, 7.5, 0.6), 'right', 'g', 21)
        lab(c, ILLUS, 700, 24, ramp(t, 0.5, 0.6), 'right')


class NowCycle(Scene):
    """§1, §5: global analyses every 6 h, hours late; the learned cycle: one hourly global update ≈ 1.5 min on one
    H100. Clocks are illustrations of those numbers."""
    vertical = True
    dur = 22.0
    cues = [(0.3, 'pop'), (7.0, 'pop'), (15.0, 'chime')]

    @staticmethod
    def clock(c, cx, cy, r, colr, ang, a):
        circle(c, cx, cy, r, stroke=colr, sw=4, a=a)
        for q in range(12):
            th = q * math.pi / 6
            line(c, cx + (r - 10) * math.sin(th), cy - (r - 10) * math.cos(th), cx + r * math.sin(th), cy - r * math.cos(th), colr, a * 0.7, 2)
        line(c, cx, cy, cx + (r - 22) * math.sin(ang), cy - (r - 22) * math.cos(ang), 'ink', a, 4)
        circle(c, cx, cy, 6, fill='ink', a=a)

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8, e_expo)
        if k > 0:
            with layer(c, k):
                panel(c, 10, 10, 700, 300, 1, stroke='c')
                lab(c, 'the usual way: physics + hand-built parts', 36, 52, 1, color='c', size=21)
                self.clock(c, 150, 180, 92, 'c', 2 * math.pi * (min(t, 7.0) / 6.0 % 1.0), 1)
                text(c, 'every 6 h', 290, 170, 50, 700, 'ink', 1)
                lab(c, 'and hours late', 292, 214, 1, size=22)
        k2 = ramp(t, 7.0, 0.8, e_expo)
        if k2 > 0:
            with layer(c, k2):
                panel(c, 10, 330, 700, 300, 1, stroke='y')
                lab(c, 'learned from the clues alone', 36, 372, 1, color='y', size=21)
                self.clock(c, 150, 500, 92, 'y', 2 * math.pi * ((t - 7.0) * 0.6 % 1.0), 1)
                text(c, 'every hour', 290, 480, 50, 700, 'ink', 1)
                text(c, '≈ 1.5 min, one GPU', 292, 532, 30, 600, 'y', 1, kind='mono')
                lab(c, 'no reanalysis needed', 292, 572, 1, size=20)
        lab(c, 'clocks: ' + ILLUS + '  ·  §1, §5  ·  arXiv:2611.18393', 360, 676, ramp(t, 0.5, 0.6), 'center')


# =============================================================== stripes
class StripesMemory(Scene):
    """Fig. S3a: channels of the 512-wide memory h at 20 Aug 2024 00 UTC (crop of the paper's figure)."""
    vertical = True
    dur = 16.0
    cues = [(0.3, 'whoosh_soft'), (5.0, 'pop'), (11.0, 'tick')]
    # map positions in Fig. S3, as fractions of the whole figure (5 columns x 4 rows in panel a)
    COLS = [(0.004, 0.196), (0.204, 0.396), (0.405, 0.597), (0.605, 0.797), (0.806, 0.998)]
    ROWS = [(0.028, 0.140), (0.150, 0.262), (0.271, 0.383), (0.393, 0.505)]

    def cell(self, i, j):
        (x0, x1), (y0, y1) = self.COLS[j], self.ROWS[i]
        return (x0, y0, x1, y1)

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8, e_expo)
        w, h = figcard(c, 'figS3', 20, 20, 680, k * window(t, 0.3, 10.6, d_out=0.5), 'Fig. S3a: the memory h', k=k,
                       src=(0.0, 0.0, 1.0, 0.51))
        # zoom on two observing-system channels (row 2 col 3: geostationary disks; row 2 col 5: polar swaths)
        kz = ramp(t, 11.0, 0.9, e_expo)
        if kz > 0:
            figcard(c, 'figS3', 30, 20, 660, kz, None, k=kz, src=self.cell(1, 2), credit=False)
            lab(c, 'geostationary footprints', 30, 404, kz, color='y', size=22)
        kz2 = ramp(t, 12.5, 0.9, e_expo)
        if kz2 > 0:
            figcard(c, 'figS3', 140, 440, 440, kz2, None, k=kz2, src=self.cell(1, 4), credit=False)
            lab(c, 'polar-orbit stripes', 140, 694, kz2, color='y', size=22)
        if kz > 0:
            lab(c, 'Fig. S3a · ' + PAPER, 690, 404, kz, 'right', size=19)


class StripesWhy(Scene):
    """Fig. S3 caption: memory h carries a record of the observing system, 'analogous to the observation-density
    information a conventional filter carries in its error covariance'; latent z is mostly weather with a weak imprint
    at coverage boundaries (crop of Fig. S3b)."""
    vertical = True
    dur = 21.0
    cues = [(0.3, 'pop'), (9.0, 'pop'), (15.0, 'chime')]

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8, e_expo)
        if k > 0:
            with layer(c, k):
                panel(c, 10, 10, 700, 250, 1, stroke='v')
                lab(c, 'memory h · 512 numbers per cell', 36, 52, 1, color='v', size=21)
                text(c, 'where it has looked', 36, 112, 40, 700, 'ink', 1)
                text(c, 'so it knows how sure to be', 36, 160, 28, 400, 'ink', 1, kind='italic')
                lab(c, 'like a classical filter’s error estimates', 36, 212, 1, size=20)
        k2 = ramp(t, 9.0, 0.8, e_expo)
        if k2 > 0:
            figcard(c, 'figS3', 380, 300, 310, k2, None, k=k2, src=(0.0, 0.53, 1.0, 1.0), credit=False)
            with layer(c, k2):
                lab(c, 'state z · 64 numbers', 20, 330, 1, color='y', size=21)
                text(c, 'mostly weather', 20, 384, 36, 700, 'ink', 1)
                lab(c, 'a faint trace at', 20, 424, 1, size=20)
                lab(c, 'coverage edges', 20, 450, 1, size=20)
                lab(c, 'Fig. S3b', 380, 600, 1, size=19)
        k3 = ramp(t, 15.0, 0.7)
        if k3 > 0:
            with layer(c, k3):
                rrect(c, 10, 620, 700, 70, 14, fill='panel', fa=0.95, stroke='y', sw=2)
                text(c, 'swap a satellite: does z stay put?', 360, 666, 28, 600, 'y', 1, 'center')


# =============================================================== trust
class TrustGain(Scene):
    """The one-variable gain (illustration): forecast 20° ± 1, thermometer 22° ± 0.5, k = 1/(1 + 0.25) = 0.8 -> 21.6°."""
    vertical = True
    dur = 16.0
    cues = [(0.3, 'pop'), (6.0, 'draw')]

    def draw(self, c, t):
        x0, x1, y = 40, 680, 300
        X = lambda v: x0 + (v - 18) / 6 * (x1 - x0)
        k = ramp(t, 0.3, 0.7)
        line(c, x0, y, x1, y, 'muted', k, 2)
        for v in range(18, 25):
            line(c, X(v), y - 8, X(v), y + 8, 'muted', k, 2)
            lab(c, f'{v}°', X(v), y + 40, k, 'center', size=20)
        for v, sg, colr, lab_, dy in ((20, 1.0, BG, 'forecast ±1°', -50), (22, 0.5, OBS, 'thermometer ±0.5°', -96)):
            rrect(c, X(v - sg), y - 18, X(v + sg) - X(v - sg), 36, 18, fill=colr, fa=k * 0.25)
            circle(c, X(v), y, 12, fill=colr, a=k)
            lab(c, lab_, X(v), y + dy, k, 'center', colr, 22)
        km = ramp(t, 6.0, 1.4, e_io)
        va = 20 + 1.6 * km
        circle(c, X(va), y, 16, stroke=AN, sw=4, a=clamp(km * 3), glow=8)
        ka = ramp(t, 7.4, 0.6)
        text(c, 'move 80% of the way', 360, 430, 36, 700, AN, ka, 'center')
        lab(c, 'that fraction is the gain', 360, 474, ka, 'center', size=22)
        tex(c, 'k1', 360, 570, 40, ramp(t, 8.0, 0.7))
        lab(c, ILLUS, 700, 24, k, 'right')


class TrustLearned(Scene):
    """§4.3.3, Fig. 8: learned observation error for clear-sky ATMS temperature channels 0.2-0.4 K (= on-orbit noise);
    gains: microwave temperature 0.64 vs optimum 0.82; ocean winds ≈ 0.9 vs 0.8; balloons aloft 0.10-0.26."""
    vertical = True
    dur = 24.0
    cues = [(0.3, 'pop'), (9.0, 'pop'), (17.0, 'chime')]

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8, e_expo)
        if k > 0:
            with layer(c, k):
                panel(c, 10, 10, 700, 230, 1, stroke='f')
                lab(c, 'nobody told it the noise', 36, 52, 1, color='f', size=21)
                text(c, '0.2–0.4 K', 36, 130, 66, 700, 'ink', 1)
                lab(c, 'assumed noise, microwave temperature channels', 36, 178, 1, size=20)
                lab(c, '= the instruments’ real noise in orbit', 36, 208, 1, color='f', size=20)
        rows = [('microwave temp', 0.64, 0.82, 'too timid'), ('ocean winds', 0.90, 0.80, 'too trusting'),
                ('balloons, high up', 0.26, None, 'barely listens')]
        x0, x1 = 230, 640
        X = lambda v: x0 + (x1 - x0) * v
        k2 = ramp(t, 9.0, 0.7)
        if k2 > 0:
            lab(c, 'gain: 0 = ignore, 1 = believe fully', 20, 290, k2, size=20)
            for v in (0, 0.5, 1):
                line(c, X(v), 310, X(v), 610, 'line', k2, 1)
                lab(c, f'{v:g}', X(v), 636, k2, 'center', size=19)
        for i, (name, v, best, verdict) in enumerate(rows):
            kk = ramp(t, 9.0 + i * 2.2, 0.6)
            if kk <= 0:
                continue
            y = 350 + i * 96
            lab(c, name, 20, y + 8, kk, color='ink', size=21)
            lab(c, verdict, 20, y + 36, kk, color='c', size=19)
            if best is None:
                rrect(c, X(0.10), y - 10, X(0.26) - X(0.10), 26, 13, fill='c', fa=kk * 0.9)
                text(c, '0.10–0.26', X(0.26) + 12, y + 12, 26, 700, 'c', kk, kind='mono')
            else:
                circle(c, X(v), y + 3, 13, fill='y', a=kk)
                text(c, f'{v:.2f}', X(v), y - 22, 26, 700, 'y', kk, 'center', kind='mono')
                circle(c, X(best), y + 3, 13, stroke='f', sw=3, a=kk)
                lab(c, f'best {best:.2f}', X(best), y + 44, kk, 'center', 'f', 19)
        lab(c, '§4.3.3, Fig. 8 · arXiv:2611.18393', 360, 680, ramp(t, 9.0, 0.6), 'center')


# =============================================================== limb
class LimbSlant(Scene):
    """Limb darkening (§4.4): a slanted view crosses more air and sees higher, colder layers. Illustration."""
    vertical = True
    dur = 15.0
    cues = [(0.3, 'pop'), (8.0, 'draw')]

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8)
        # the Earth's curve and an atmosphere shell
        cx, cy, R = 360, 1250, 900
        with layer(c, k):
            c.drawCircle(cx, cy, R + 110, paint('g', 0.10))
            c.drawCircle(cx, cy, R + 55, paint('g', 0.10))
            c.drawCircle(cx, cy, R, paint('#141827', 1))
            circle(c, cx, cy, R, stroke='faint', sw=2)
        satellite_icon(c, 360, 70, 1.3, k)
        # nadir ray (short path) and a slant ray (long path)
        kr = ramp(t, 1.5, 0.8)
        arrow(c, 360, 100, 360, 350, 'f', kr, 4, 14, prog=ramp(t, 1.5, 0.8, e_io))
        lab(c, 'straight down: sees deep', 380, 300, kr, color='f', size=21)
        ks = ramp(t, 4.0, 0.8)
        arrow(c, 340, 100, 70, 520, 'c', ks, 4, 14, prog=ramp(t, 4.0, 1.0, e_io))
        lab(c, 'at a slant: more air,', 20, 600, ks, color='c', size=21)
        lab(c, 'higher, colder layers', 20, 626, ks, color='c', size=21)
        # the cold-limb disk
        kd = ramp(t, 8.0, 0.8)
        if kd > 0:
            p = skia.Paint(AntiAlias=True)
            p.setShader(skia.GradientShader.MakeRadial((560, 470), 120, [col('#e9d7b0', kd), col('#4a6fa8', kd)], [0.4, 1.0]))
            c.drawCircle(560, 470, 120, p)
            lab(c, 'warm middle, cold edges', 560, 630, kd, 'center', 'ink', 20)
        lab(c, ILLUS, 700, 24, k, 'right')


class LimbFix(Scene):
    """Fig. S7a/c (crops): ATMS ch 7 observed vs the analysis decoded at nadir; §4.4: 83-96 % of limb darkening
    recovered; corrections near 80°: 11.2 µm 6 K, 6.9 µm 14 K, 13.3 µm 16 K, 9.6 µm 22 K."""
    vertical = True
    dur = 22.0
    cues = [(0.3, 'whoosh_soft'), (6.0, 'pop'), (14.0, 'chime')]

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.8, e_expo)
        figcard(c, 'figS7', 20, 20, 330, k, None, k=k, src=(0.09, 0.09, 0.32, 0.27), credit=False)
        lab(c, 'observed', 20, 290, k, color='ink', size=21)
        k2 = ramp(t, 2.5, 0.8, e_expo)
        figcard(c, 'figS7', 370, 20, 330, k2, None, k=k2, src=(0.54, 0.09, 0.77, 0.27), credit=False)
        lab(c, 'redrawn straight down', 370, 290, k2, color='y', size=21)
        lab(c, 'Fig. S7a, c (ATMS 54 GHz) · ' + PAPER, 360, 320, k, 'center', size=19)
        kb = ramp(t, 6.0, 0.7)
        if kb > 0:
            text(c, '83–96%', 20, 400, 56, 700, 'y', kb)
            lab(c, 'of the edge cooling removed', 250, 390, kb, color='ink', size=21)
            col_chart(c, t, 7.0, [6, 14, 16, 22], 30, 630, 160, 24, 165, 90, ['g', 'x', 'c', 'y'],
                      ['window\n11.2 µm', 'water vap.\n6.9 µm', 'CO₂\n13.3 µm', 'ozone\n9.6 µm'], lambda v: f'{v} K')
            lab(c, 'correction near 80° · §4.4', 700, 430, kb, 'right', size=19)


# =============================================================== walls
class WallsRatio(Scene):
    """Table 2: SD of observation-minus-forecast, WeatherDreamer / NOAA's GSI, 3-9 h ahead, 30 cycles in 2024:
    surface stations 1.02-1.08 (temperature 1.04 shown), ocean winds 1.65, balloon temperature 1.79, balloon wind 2.62
    (averaged over 1000-100 hPa)."""
    vertical = True
    dur = 15.0
    cues = [(0.3, 'pop'), (6.5, 'draw')]

    def draw(self, c, t):
        k = ramp(t, 0.3, 0.7)
        lab(c, 'error vs NOAA’s own system (1 = same)', 360, 30, k, 'center', 'ink', 21)
        vals = [1.04, 1.65, 1.79, 2.62]
        col_chart(c, t, 0.3, vals[:1], 40, 560, 420, 2.8, 160, 100, ['f'], ['stations\nsurface'], lambda v: f'{v:.2f}×',
                  base=1.0)
        col_chart(c, t, 6.5, vals[1:], 200, 560, 420, 2.8, 160, 100, ['y', 'y', 'c'],
                  ['ocean\nwinds', 'balloon\ntemp', 'balloon\nwind'], lambda v: f'{v:.2f}×', stagger=0.4)
        lab(c, 'Table 2 · balloon wind averaged over all levels', 360, 676, k, 'center', size=19)


class WallsCauses(Scene):
    """§5: dynamics on ~1,600 km patches can't hold the large, slowly evolving circulation (illustration); our
    arithmetic: 50 m/s crosses 1,600 km in ~9 h; §4.3.3: balloon gains 0.10-0.26 at 100-300 hPa."""
    vertical = True
    dur = 20.0
    cues = [(0.3, 'pop'), (5.5, 'sweep'), (11.0, 'pop'), (16.0, 'chime')]

    def draw(self, c, t):
        mx, my, P = 30, 30, 220
        k = ramp(t, 0.3, 0.7)
        if k > 0:
            for i in range(4):
                line(c, mx + i * P, my, mx + i * P, my + 2 * P, 'faint', k, 2)
            for j in range(3):
                line(c, mx, my + j * P, mx + 3 * P, my + j * P, 'faint', k, 2)
            rrect(c, mx + P, my + P / 2, P, P, 6, stroke='y', sw=3.4, a=k, glow=6)
            lab(c, '≈ 1,600 km patch', mx + 1.5 * P, my + 1.5 * P + 34, k, 'center', 'y', 20)
            lab(c, 'own memory', mx + 1.5 * P, my + P - 6, k, 'center', 'y', 20)
        kj = ramp(t, 5.5, 0.8)
        if kj > 0:
            xs = np.linspace(mx + 4, mx + 3 * P - 4, 160)
            ys = my + P + 70 * np.sin((xs - mx) / 110)
            draw_poly(c, np.stack([xs, ys], 1), 'c', kj, 6, prog=ramp(t, 5.5, 2.0, e_io), glow=8)
            lab(c, 'jet, 50 m/s: across in ≈ 9 h', 360, 500, kj, 'center', 'c', 22)
            lab(c, OURS, 360, 528, kj, 'center', 'y', 19)
        kg = ramp(t, 11.0, 0.7)
        if kg > 0:
            with layer(c, kg):
                rrect(c, 10, 560, 700, 120, 14, fill='panel', fa=0.95, stroke='c', sw=2)
                lab(c, 'and up there it barely listens', 36, 600, 1, color='ink', size=22)
                text(c, 'gain 0.10–0.26', 36, 652, 36, 700, 'c', 1, kind='mono')
                lab(c, 'balloons, 100–300 hPa · §4.3.3', 690, 652, 1, 'right', size=19)
