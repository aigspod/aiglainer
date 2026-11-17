"""Cold open to clue two (arXiv:2611.18393v1 §1, §3, §4.3, §4.4, §5; Figs. 8, S3, S7; Table 2).
Paper figures are crops (figcard) labelled 'Fig. N'. Charts are drawn from numbers typed from the text and tables,
with the source named on screen and in a comment. Diagrams are labelled 'illustration'."""
from trustkit import *

# Fig. S3 map positions, as fractions of the whole figure (2000 x 1816 px): five columns, four rows per panel.
S3_COLS = [(0.006, 0.194), (0.205, 0.394), (0.405, 0.594), (0.605, 0.794), (0.805, 0.994)]
S3_ROWS_A = [(0.045, 0.150), (0.157, 0.262), (0.269, 0.374), (0.382, 0.486)]
S3_ROWS_B = [(0.548, 0.653), (0.660, 0.765), (0.773, 0.878), (0.885, 0.990)]
S3_A = (0.0, 0.015, 1.0, 0.495)          # panel (a): memory h
S3_B = (0.0, 0.515, 1.0, 1.0)            # panel (b): latent z

def s3map(row, col, b=False):
    rows = S3_ROWS_B if b else S3_ROWS_A
    return (S3_COLS[col][0], rows[row][0], S3_COLS[col][1], rows[row][1])

# ======================================================================= COLD OPEN
class ColdOpen(Scene):
    """Fig. S3a: the memory h at 2024-08-20 00 UTC. Weather channels, then the observing-system footprints."""
    dur = 30.0
    fade_in = 0.8
    cues = [(0.4, 'whoosh_soft'), (11.5, 'draw'), (16.5, 'pop'), (24.5, 'riser')]
    WEATHER = [(0, 0), (1, 0), (0, 1)]
    FOOT = [(1, 2), (3, 0)]
    SWATH = [(1, 4)]

    def draw(self, c, t):
        x, y, w = 120, 250, 1040
        ka = ramp(t, 0.3, 1.2)
        _, h = figcard(c, 'figS3', x, y, w, ka, 'Fig. S3a, memory channels', src=S3_A, k=ramp(t, 0.3, 1.2, e_expo))
        kicker(c, 'inside the memory  ·  20 aug 2024, 00 utc', x - 10, y - 40, ka, 'muted', 18)
        kw = window(t, 6.5, 11.3)
        for i, (r, cc) in enumerate(self.WEATHER):
            rx, ry, rw, rh = crop_rect('figS3', S3_A, x, y, w, s3map(r, cc))
            highlight(c, rx, ry, rw, rh, 'g', kw, ramp(t, 6.5 + i * 0.25, 0.6, e_io))
        for i, (r, cc) in enumerate(self.FOOT + self.SWATH):
            rx, ry, rw, rh = crop_rect('figS3', S3_A, x, y, w, s3map(r, cc))
            highlight(c, rx, ry, rw, rh, 'y', ramp(t, 11.5, 0.4), ramp(t, 11.5 + i * 0.35, 0.6, e_io))
        # enlargements on the right
        ex, ew = 1270, 520
        for j, ((r, cc), lab, t0) in enumerate((((1, 2), 'geostationary disk footprints', 16.5),
                                                ((1, 4), 'polar-orbit swaths', 18.0))):
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            yy = 250 + j * 360
            text(c, lab, ex - 10, yy - 18, 24, 500, 'y', k, kind='mono')
            figcard(c, 'figS3', ex, yy, ew, k, None, src=s3map(r, cc), k=k)
        rich(c, 'Why would a weather model remember {y:where the satellites were looking?}', x, 860, 46, 1050, t, 24.5,
             0.05, 0.6, base_w=600)

class Title(TitleCard):
    dur = 10.0

# ======================================================================= THE CASE FILE
class CaseFile(Scene):
    """§1, §3.1: the analysis, the predict-correct loop; WeatherDreamer learns it from 18 systems, no reanalysis."""
    dur = 36.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (8.0, 'draw'), (22.5, 'pop'), (27.0, 'stamp'), (28.0, 'stamp')]
    SYSTEMS = ['geostationary infrared ×4', 'microwave sounders ×4', 'infrared sounders ×2', 'ocean-wind scatterometers',
               'radio occultation', 'cloud radar + lidar', 'surface stations', 'weather balloons', 'rain, sunlight grids']

    def draw(self, c, t):
        hdr(c, t, '01', 'the case file', 'Predict, then *correct*',
            sub='every forecast starts from the analysis: a best guess of the atmosphere right now')
        # the loop (illustration)
        cx, cy, R = 560, 640, 210
        kl = ramp(t, 8.0, 0.8)
        if kl > 0:
            prog = ramp(t, 8.0, 3.0, e_io)
            for j, (a0, colr) in enumerate(((200, 'g'), (20, 'c'))):
                pth = skia.Path()
                pth.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), a0, 140 * clamp(prog * 2 - j))
                c.drawPath(pth, paint(colr, kl, stroke=5, cap='round'))
            for (ang, lab, sub, colr) in ((270, 'predict', 'the background', 'g'), (90, 'correct', 'the analysis', 'c')):
                px = cx + R * math.cos(math.radians(ang))
                py = cy + R * math.sin(math.radians(ang))
                rrect(c, px - 130, py - 44, 260, 88, 16, fill='panel', stroke=colr, sw=2.4, a=kl, fa=kl * 0.95)
                text(c, lab, px, py - 2, 32, 400, 'ink', kl, 'center', kind='italic')
                text(c, sub, px, py + 30, 17, 500, 'muted', kl, 'center', kind='mono')
            text(c, 'every hour', cx, cy + 10, 26, 500, 'y', ramp(t, 9.5, 0.6), 'center', kind='mono')
            tag(c, 'illustration', cx - R, cy + R + 90, kl)
        # the instruments
        ki = ramp(t, 22.5, 0.6)
        if ki > 0:
            text(c, '18 observing systems', 1060, 360, 30, 600, 'ink', ki)
            for i, s in enumerate(self.SYSTEMS):
                k = ramp(t, 22.6 + i * 0.12, 0.5)
                pill(c, 1060 + (i % 2) * 360, 395 + (i // 2) * 52, s, 'g', k, size=15)
            src(c, 'Table 1', 1060, 670, ki)
            note(c, 'cloud radar, rain and sunlight grids: training targets only, never inputs', 1060, 700, ki, 15)
        for j, (s, t0) in enumerate((('a reanalysis to copy', 27.0), ('a table of instrument errors', 28.0))):
            k = ramp(t, t0, 0.5)
            if k <= 0:
                continue
            yy = 740 + j * 76
            panel(c, 1060, yy, 600, 58, k)
            w = text(c, s, 1090, yy + 38, 26, 500, 'muted', k)
            line(c, 1080, yy + 30, 1080 + (w + 24) * ramp(t, t0 + 0.2, 0.4, e_io), yy + 30, 'c', k, 4)
            text(c, 'none', 1640, yy + 38, 22, 600, 'c', k, 'right', kind='mono')
        kn = ramp(t, 22.5, 0.6) * 0.95
        note(c, 'most AI forecasters start from a physics-built analysis;', 1060, 912, kn, 15)
        note(c, 'earlier observation-only models skip the hour-by-hour loop', 1060, 938, kn, 15)

# ======================================================================= THE GAIN
class Gain(Scene):
    """Eq. 2-3: how far to move toward a measurement. The numbers are an illustration."""
    dur = 32.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (7.0, 'pop'), (12.0, 'draw'), (20.5, 'stamp')]

    def draw(self, c, t):
        hdr(c, t, '01', 'the case file', 'A question of *trust*', sub='how far should you move toward each new measurement?')
        x0, x1, yb = 160, 1100, 720
        kn = ramp(t, 6.5, 0.7)
        if kn > 0:
            line(c, x0, yb, x1, yb, 'muted', kn, 2)
            for v in range(18, 25):
                X = x0 + (v - 18) / 6 * (x1 - x0)
                line(c, X, yb, X, yb + 10, 'muted', kn, 2)
                text(c, f'{v}°', X, yb + 40, 22, 500, 'muted', kn, 'center', kind='mono')
            gauss(c, x0, x1, yb, 20, 1.0, 'g', kn, 150, prog=ramp(t, 7.0, 0.8, e_out))
            text(c, 'forecast  20°', x0 + 2 / 6 * (x1 - x0), yb - 175, 24, 600, 'g', kn, 'center', kind='mono')
        kt = ramp(t, 8.5, 0.7)
        if kt > 0:
            gauss(c, x0, x1, yb, 22, 0.5, 'c', kt, 300, prog=ramp(t, 8.5, 0.8, e_out))
            text(c, 'thermometer  22°', x0 + 4 / 6 * (x1 - x0), yb - 325, 24, 600, 'c', kt, 'center', kind='mono')
            thermometer(c, x0 + 4 / 6 * (x1 - x0) + 170, yb - 220, 1.0, kt, 0.7)
        ke = ramp(t, 12.0, 0.6)
        if ke > 0:
            text(c, '± 1°', x0 + 2 / 6 * (x1 - x0) - 120, yb - 70, 22, 500, 'g', ke, 'center', kind='mono')
            text(c, '± 0.5°', x0 + 4 / 6 * (x1 - x0) + 150, yb - 120, 22, 500, 'c', ke, 'center', kind='mono')
        kk = ramp(t, 15.5, 0.6)
        if kk > 0:
            X0 = x0 + 2 / 6 * (x1 - x0)
            Xa = x0 + 3.6 / 6 * (x1 - x0)
            arrow(c, X0, yb + 80, Xa, yb + 80, 'y', kk, 4, 16, prog=ramp(t, 15.5, 1.0, e_io), glow=6)
            circle(c, Xa, yb, 10, fill='y', a=ramp(t, 16.3, 0.4), glow=10)
            text(c, 'new best guess  21.6°', Xa, yb + 128, 24, 600, 'y', ramp(t, 16.3, 0.5), 'center', kind='mono')
        tex(c, 'gain', 1470, 420, 54, ramp(t, 12.0, 0.8))
        tex(c, 'gainnum', 1470, 575, 46, ramp(t, 15.0, 0.8))
        kq = ramp(t, 13.0, 0.7) * 0.9
        note(c, 'σ_B: how wrong the forecast tends to be', 1470, 650, kq, 16, 'g', 'center')
        note(c, 'σ_O: how wrong the instrument tends to be', 1470, 678, kq, 16, 'c', 'center')
        tag(c, 'illustration', x0, yb + 190, kn)
        kp = ramp(t, 20.5, 0.6)
        if kp > 0:
            panel(c, 1210, 700, 540, 190, kp)
            text(c, 'classical systems', 1240, 745, 20, 500, 'muted', kp, kind='mono')
            text(c, 'σ_B, σ_O written down by people', 1240, 785, 24, 500, 'ink', kp)
            text(c, 'weatherdreamer', 1240, 835, 20, 500, 'muted', ramp(t, 23.5, 0.5), kind='mono')
            text(c, 'never given any', 1240, 872, 26, 600, 'y', ramp(t, 23.5, 0.5))

# ======================================================================= CLUE 1: READING TRUST
class Diagnostics(Scene):
    """Text S6.10, §4.3.3, Fig. 8a,c: the Desroziers estimate and the Hollingsworth-Lönnberg check."""
    dur = 40.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (5.5, 'draw'), (13.0, 'pop'), (24.0, 'pop'), (33.0, 'pop')]

    def draw(self, c, t):
        hdr(c, t, '02', 'clue one', 'Reading *trust* out of a black box')
        exhibit(c, 1500, 190, 'exhibit a', ramp(t, 0.6, 0.5), ramp(t, 0.6, 0.5, e_back))
        # O, B, A on a line (illustration)
        y = 470
        kd = ramp(t, 5.5, 0.7)
        if kd > 0:
            pts = {'B': (200, 'g', 'before'), 'A': (520, 'y', 'after'), 'O': (720, 'c', 'measured')}
            line(c, 160, y, 800, y, 'line', kd, 2)
            for i, (lab, (X, colr, sub)) in enumerate(pts.items()):
                k = ramp(t, 5.5 + i * 0.5, 0.5)
                circle(c, X, y, 12, fill=colr, a=k, glow=8)
                text(c, lab, X, y - 30, 28, 600, colr, k, 'center', kind='mono')
                text(c, sub, X, y + 44, 18, 500, 'muted', k, 'center', kind='mono')
            kb = ramp(t, 8.0, 0.6)
            arrow(c, 200, y + 86, 720, y + 86, 'muted', kb, 2, 10, prog=ramp(t, 8.0, 0.6, e_io))
            text(c, 'O − B', 460, y + 116, 20, 500, 'muted', kb, 'center', kind='mono')
            arrow(c, 520, y + 146, 720, y + 146, 'muted', kb, 2, 10, prog=ramp(t, 8.5, 0.6, e_io))
            text(c, 'O − A', 620, y + 176, 20, 500, 'muted', kb, 'center', kind='mono')
            tag(c, 'illustration', 160, y + 220, kd)
        tex(c, 'desroz', 480, 790, 40, ramp(t, 13.0, 0.8))
        note(c, 'Desroziers et al. (2005): the error the update behaves as if it assumes', 480, 840, ramp(t, 13.5, 0.6), 15,
             'muted', 'center')
        note(c, '+ Hollingsworth–Lönnberg (1986): from how O − B errors correlate with distance', 480, 872,
             ramp(t, 18.0, 0.6), 15, 'muted', 'center')
        # Fig. 8a and 8c
        kf = ramp(t, 24.0, 0.8, e_expo)
        fx, fy = 960, 330
        w8, h8 = figcard(c, 'fig8', fx, fy, 600, kf, None, src=(0.0, 0.02, 0.45, 0.44), k=kf)
        kc = ramp(t, 33.0, 0.8, e_expo)
        figcard(c, 'fig8', fx + 640, fy, 170, kc, None, src=(0.80, 0.02, 1.0, 0.44), k=kc)
        note(c, 'Fig. 8a, c · ' + PAPER + '  ·  blue: the update  ·  grey band: instrument noise', fx - 10,
             fy + h8 + 34, kf, 15)
        if kf > 0:
            # ATMS channels 5-9 (tropospheric temperature): x fractions within crop, by eye from the axis ticks
            rx, ry, rw, rh = crop_rect('fig8', (0.0, 0.02, 0.45, 0.44), fx, fy, 600, (0.135, 0.30, 0.228, 0.39))
            highlight(c, rx, ry, rw, rh, 'y', ramp(t, 25.0, 0.5), ramp(t, 25.0, 0.8, e_io))
        stat(c, fx, fy + h8 + 130, '0.2–0.4 K', 'learned error, clear-sky microwave temperature channels = on-orbit noise',
             'y', ramp(t, 26.0, 0.6), 54)
        text(c, 'ocean winds: ≈ triple-collocation retrieval error', fx, fy + h8 + 250, 22, 500, 'f',
             ramp(t, 34.0, 0.6), kind='mono')
        src(c, '§4.3.3, Text S6.10', fx, fy + h8 + 290, ramp(t, 26.0, 0.6))

# ======================================================================= REVERSAL: NOT OPTIMAL
class Reversal(Scene):
    """§4.3.3, Fig. 8d,f: learned gain vs the Hollingsworth-Lönnberg optimum; upper-air gains."""
    dur = 38.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (3.5, 'draw'), (8.5, 'pop'), (16.0, 'pop'), (26.0, 'drop')]
    # (label, learned k (or (lo, hi)), optimum or None, verdict, colour, t0)    §4.3.3
    ROWS = [('microwave temperature sounding', 0.64, 0.82, 'too timid', 'c', 8.5),
            ('ocean winds (scatterometer)', 0.90, 0.80, 'too trusting', 'c', 16.0),
            ('balloon temperature & wind, 100–300 hPa', (0.10, 0.26), None, 'leans lightly', 'c', 26.0),
            ('radio occultation (bending angle)', 0.012, None, '≈ 0', 'c', 30.0)]

    def draw(self, c, t):
        hdr(c, t, '02', 'clue one, reversed', 'Not *quite* optimal', sub='the gain it applies vs the best gain implied by the same diagnostics')
        x, w, y0, dy = 760, 860, 430, 122
        ka = ramp(t, 3.5, 0.7)
        if ka > 0:
            for v in (0, 0.25, 0.5, 0.75, 1.0):
                X = x + v * w
                line(c, X, y0 - 60, X, y0 + 3 * dy + 40, 'line', ka, 1)
                text(c, f'{v:g}', X, y0 + 3 * dy + 76, 20, 500, 'muted', ka, 'center', kind='mono')
            text(c, 'gain k: how far it moves toward the measurement', x, y0 + 3 * dy + 116, 18, 500, 'muted', ka, kind='mono')
            legend_item(c, x, 350, 'y', 'learned gain', ka, size=20)
            line(c, x + 250, 340, x + 250, 356, 'f', ka, 4, cap='butt')
            text(c, 'best gain (Hollingsworth–Lönnberg)', x + 266, 350, 20, 500, 'ink', ka)
        for i, (lab, k, opt, verdict, colr, t0) in enumerate(self.ROWS):
            kr = ramp(t, t0, 0.6)
            if kr <= 0:
                continue
            y = y0 + i * dy
            rich(c, lab, MX, y + 8, 26, 600, base_w=500, a=kr)
            pr = ramp(t, t0, 0.9, e_io)
            if isinstance(k, tuple):
                hbar(c, x, y, w, k[1], 1.0, 'y', kr, pr, 34, v0=k[0])
                text(c, '0.10–0.26', x + k[1] * w + 16, y + 8, 22, 600, 'y', kr, kind='mono')
            else:
                end = hbar(c, x, y, w, k, 1.0, 'y', kr, pr, 34)
                if k > 0.05:
                    text(c, f'{k:.2f}', x + 12, y + 8, 22, 700, '#1a1206', kr, kind='mono')
            if opt is not None:
                ko = ramp(t, t0 + 1.2, 0.5)
                marker(c, x + opt * w, y, 34, 'f', ko, f'{opt:.2f}')
            pill(c, x + w + 20, y - 18, verdict, colr, ramp(t, t0 + 1.6, 0.5), size=15)
        src(c, '§4.3.3, Fig. 8d, f  ·  occultation "near zero" (bar not to scale)', MX, 985, ramp(t, 3.5, 0.7))

# ======================================================================= THE TRACE: TABLE 2
class Departures(Scene):
    """§4.3.2, Table 2: SD of observation-minus-forecast, WeatherDreamer / NCEP GSI background, 3-9 h, 30 cycles in 2024."""
    dur = 34.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (10.5, 'pop'), (17.0, 'pop'), (25.5, 'pop')]
    # (label, WD/GSI ratio, per-channel range or None, group start time)        Table 2
    ROWS = [('surface temperature (held-out stations)', 1.04, None, 10.5),
            ('surface humidity (held-out stations)', 1.02, None, 10.5),
            ('surface wind speed (held-out stations)', 1.08, None, 10.5),
            ('ocean winds (scatterometer)', 1.65, None, 12.5),
            ('balloon wind, 1000–100 hPa', 2.62, (1.27, 3.51), 17.0),
            ('microwave temperature, troposphere', 1.76, (1.35, 4.55), 25.5),
            ('microwave temperature, stratosphere', 1.84, (1.38, 3.64), 26.0),
            ('balloon temperature, 1000–100 hPa', 1.79, (1.19, 2.50), 26.5),
            ('microwave water vapour', 1.04, (0.96, 1.23), 28.0),
            ('infrared sounder temperature (HIRS)', 0.86, (0.82, 1.21), 28.0)]

    def draw(self, c, t):
        hdr(c, t, '02', 'the trace', 'Strong low, *weak* high',
            sub='spread of observation-minus-forecast errors, WeatherDreamer ÷ NOAA’s operational background, 3–9 h ahead')
        x, w, y0, dy, vmax = 760, 900, 360, 52, 5.0
        ka = ramp(t, 0.6, 0.8)
        if ka > 0:
            for v in (0, 1, 2, 3, 4, 5):
                X = x + v / vmax * w
                line(c, X, y0 - 30, X, y0 + len(self.ROWS) * dy - 20, 'line' if v != 1 else 'f', ka * (1 if v != 1 else 0.9), 1 if v != 1 else 2.5)
                text(c, f'{v}×', X, y0 + len(self.ROWS) * dy + 14, 20, 500, 'muted', ka, 'center', kind='mono')
            text(c, '1× = as good as NOAA’s background', x + w / vmax + 10, y0 - 40, 18, 500, 'f', ka, kind='mono')
        for i, (lab, r, rng, t0) in enumerate(self.ROWS):
            k = ramp(t, t0 + (i % 3) * 0.15, 0.6)
            if k <= 0:
                continue
            y = y0 + i * dy
            text(c, lab, x - 24, y + 8, 21, 500, 'ink', k, 'right')
            colr = 'f' if r < 1.2 else 'c'
            hbar(c, x, y, w, r, vmax, colr, k, ramp(t, t0, 0.8, e_io), 26)
            if rng:
                X0, X1 = x + rng[0] / vmax * w, x + rng[1] / vmax * w
                line(c, X0, y, X1, y, 'ink', k * 0.8, 2)
                line(c, X1, y - 10, X1, y + 10, 'ink', k * 0.8, 2)
            text(c, f'{r:.2f}', x + r / vmax * w * ramp(t, t0, 0.8, e_io) - 10, y + 8, 20, 700, '#1a1206', k, 'right', kind='mono')
        kn = ramp(t, 17.5, 0.6)
        note(c, 'balloon wind: 1.6–1.7× at 925–850 hPa, 3.2–3.5× at 300–200 hPa (Table S5)', x, 935, kn, 15)
        note(c, 'whiskers: range across channels or levels  ·  NOAA uses far more instruments (favours NOAA); WD is scored as an ensemble mean (favours WD)',
             MX, 965, ramp(t, 25.5, 0.6), 15)
        src(c, 'Table 2 (30 cycles, 2024)', MX, 995, ka)

# ======================================================================= TWO SUSPECTS
class Suspects(Scene):
    """§5: little use of upper-air data; ~1,600 km patches. The crossing time is our arithmetic."""
    dur = 26.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (0.8, 'stamp'), (7.0, 'stamp'), (17.5, 'draw')]

    def draw(self, c, t):
        hdr(c, t, '02', 'the trace', 'Two *suspects*', sub='the paper’s own explanation for the gap aloft (§5)')
        k1 = ramp(t, 0.8, 0.6, e_back)
        exhibit(c, MX, 380, 'suspect 1', ramp(t, 0.8, 0.5), k1)
        rich(c, 'The correction step {y:draws little} from upper-air observations', MX, 470, 34, 640, t, 1.0, 0.04, base_w=500)
        for i, (lab, v, t0) in enumerate((('balloons, 100–300 hPa', 0.26, 2.0), ('radio occultation', 0.015, 2.4))):
            k = ramp(t, t0, 0.6)
            y = 640 + i * 70
            text(c, lab, MX, y + 8, 22, 500, 'muted', k, kind='mono')
            hbar(c, MX + 340, y, 360, v, 1.0, 'c', k, ramp(t, t0, 0.8, e_io), 26)
            text(c, 'gain ≤ 0.26' if i == 0 else 'gain ≈ 0', MX + 340 + v * 360 + 14, y + 8, 20, 600, 'c', k, kind='mono')
        # suspect 2: the patch (illustration)
        k2 = ramp(t, 7.0, 0.6, e_back)
        exhibit(c, 1000, 380, 'suspect 2', ramp(t, 7.0, 0.5), k2)
        px, py, ps = 1000, 450, 420
        kp = ramp(t, 7.5, 0.8)
        if kp > 0:
            rrect(c, px, py, ps, ps, 6, fill='panel', fa=kp * 0.9, stroke='y', sw=2.4, a=kp)
            n = 32
            for i in range(1, n):
                q = i / n * ps
                line(c, px + q, py, px + q, py + ps, 'line', kp * 0.7, 1)
                line(c, px, py + q, px + ps, py + q, 'line', kp * 0.7, 1)
            text(c, '≈ 1,600 km', px + ps / 2, py + ps + 40, 24, 600, 'y', kp, 'center', kind='mono')
            note(c, '32 × 32 cells of ≈ 50 km, one memory per patch; patches overlap 50% and are blended', px - 20, py + ps + 76, kp, 14)
        kw = ramp(t, 17.5, 0.6)
        if kw > 0:
            y = py + 120
            arrow(c, px - 40, y, px + ps + 40, y, 'c', kw, 5, 18, prog=ramp(t, 17.5, 1.2, e_io), glow=8)
            text(c, 'jet-level wind, 50 m/s', px + ps + 60, y - 6, 21, 600, 'c', kw, kind='mono')
            text(c, 'crosses in ≈ 9 h', px + ps + 60, y + 24, 21, 600, 'c', kw, kind='mono')
            y2 = py + 300
            arrow(c, px + 60, y2, px + 60 + 0.27 * ps, y2, 'g', kw, 4, 14, prog=ramp(t, 18.5, 0.8, e_io))
            k2 = ramp(t, 18.5, 0.6)
            text(c, 'surface wind, 5–10 m/s', px + ps + 60, y2 - 6, 21, 600, 'g', k2, kind='mono')
            text(c, '200–430 km in 12 h', px + ps + 60, y2 + 24, 21, 600, 'g', k2, kind='mono')
            tag(c, 'our arithmetic', px + ps + 60, y2 + 80, kw)
            tag(c, 'illustration', px + ps + 60, y2 + 106, kw)
        src(c, '§5: patches "limit their ability to represent the large-scale, slowly evolving circulation"', MX, 985, ramp(t, 7.0, 0.6))

# ======================================================================= CLUE 2: GEOMETRY
class Limb(Scene):
    """§4.4: limb darkening (illustration of slant paths); §3.3, §3.6: excess air mass, zero at nadir."""
    dur = 32.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (3.0, 'draw'), (12.5, 'pop'), (19.0, 'pop')]

    def draw(self, c, t):
        hdr(c, t, '03', 'clue two', 'The view from an *angle*')
        exhibit(c, 1500, 190, 'exhibit b', ramp(t, 0.6, 0.5), ramp(t, 0.6, 0.5, e_back))
        # atmosphere slab and two rays (illustration)
        x0, x1, yg = 140, 1000, 860
        kg = ramp(t, 3.0, 0.8)
        if kg > 0:
            layers = [('#5a3a2c', 'warm, low'), ('#3f4a6b', ''), ('#2c3858', 'cold, high')]
            for i, (cl, lab) in enumerate(layers):
                rrect(c, x0, yg - (i + 1) * 70, x1 - x0, 70, 0, fill=cl, fa=kg * 0.75)
                if lab:
                    text(c, lab, x0 + 14, yg - i * 70 - 26, 18, 500, 'ink', kg * 0.9, kind='mono')
            line(c, x0, yg, x1, yg, 'ink', kg, 3)
            sx, sy = 620, 340
            satellite(c, sx, sy, 1.0, kg)
            # nadir ray
            kr = ramp(t, 4.0, 0.8, e_io)
            arrow(c, sx, sy + 20, sx, yg - 4, 'f', kg, 4, 14, prog=kr, glow=6)
            text(c, 'straight down: short path', sx + 16, 560, 20, 600, 'f', ramp(t, 4.5, 0.6), kind='mono')
            ks = ramp(t, 6.5, 1.0, e_io)
            arrow(c, sx - 10, sy + 16, x0 + 40, yg - 150, 'c', kg, 4, 14, prog=ks, glow=6)
            text(c, 'at a slant: long path,', x0 + 20, 380, 20, 600, 'c', ramp(t, 7.5, 0.6), kind='mono')
            text(c, 'sees higher, colder air', x0 + 20, 408, 20, 600, 'c', ramp(t, 7.5, 0.6), kind='mono')
            tag(c, 'illustration', x0, yg + 40, kg)
        # disks with cold limbs and a seam (illustration)
        kd = ramp(t, 12.5, 0.8)
        if kd > 0:
            for j, cxx in enumerate((1230, 1530)):
                r = 190
                p = skia.Paint(AntiAlias=True)
                p.setShader(skia.GradientShader.MakeRadial((cxx, 560), r, [col('#e0a45a', kd), col('#c08060', kd), col('#3f5f8a', kd)],
                                                           [0.0, 0.55, 1.0]))
                c.drawCircle(cxx, 560, r, p)
            line(c, 1380, 400, 1380, 720, 'ink', ramp(t, 14.0, 0.5), 2, dash=[8, 6])
            text(c, 'seam', 1380, 390, 20, 600, 'ink', ramp(t, 14.0, 0.5), 'center', kind='mono')
            text(c, 'cold limbs', 1230, 790, 20, 500, 'g', kd, 'center', kind='mono')
            tag(c, 'illustration', 1060, 830, kd)
        tex(c, 'airmass', 1380, 900, 40, ramp(t, 19.0, 0.8))
        note(c, 'the angle each view is decoded at · 0 straight down', 1380, 950, ramp(t, 19.5, 0.6), 16, 'muted', 'center')

# ======================================================================= CLUE 2: RESULT
class LimbResult(Scene):
    """§4.4, Fig. 9b (≈80°: 11.2 µm 6 K, 6.9 µm 14 K, 13.3 µm 16 K, 9.6 µm 22 K); Fig. S7e,j crossover slopes."""
    dur = 32.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (7.5, 'draw'), (20.5, 'draw')]
    BANDS = [('11.2 µm window', 6, 7.5), ('6.9 µm water vapour', 14, 10.5), ('13.3 µm CO₂', 16, 11.5), ('9.6 µm ozone', 22, 12.5)]

    def draw(self, c, t):
        hdr(c, t, '03', 'clue two', 'It learned the *geometry*')
        stat(c, MX, 380, '83–96%', 'of the observed limb darkening recovered (collocated GOES-East/West views, §4.4)', 'y',
             ramp(t, 0.6, 0.8), 84, k=ramp(t, 0.6, 0.8, e_expo))
        ka = ramp(t, 7.5, 0.6)
        x, w, y0 = 470, 420, 520
        if ka > 0:
            text(c, 'learned correction near 80°', MX, y0 - 20, 22, 500, 'muted', ka, kind='mono')
        for i, (lab, v, t0) in enumerate(self.BANDS):
            k = ramp(t, t0, 0.6)
            y = y0 + 30 + i * 70
            text(c, lab, x - 20, y + 8, 22, 500, 'ink', k, 'right')
            hbar(c, x, y, w, v, 24, 'y', k, ramp(t, t0, 0.8, e_io), 30)
            text(c, f'≈ {v} K', x + v / 24 * w + 14, y + 8, 22, 600, 'y', k, kind='mono')
        note(c, 'more absorbing air → bigger correction', MX, y0 + 340, ramp(t, 15.0, 0.6), 17, 'f')
        src(c, '§4.4, Fig. 9b', MX, y0 + 380, ka)
        # crossovers: fitted slopes as lines (Fig. S7e, j)
        kc = ramp(t, 20.5, 0.6)
        if kc > 0:
            for j, (lab, s_obs, s_nad, xx) in enumerate((('ch 7 (54.4 GHz)', -13.6, -0.3, 1140), ('ch 20 (183 GHz)', -6.1, -0.1, 1520))):
                ax = Axes(xx, 470, 300, 280, (-1, 1), (-15, 15))
                ax.draw(c, kc, [-1, 0, 1], [-15, 0, 15], fmt='{:g}')
                text(c, lab, xx, 440, 20, 600, 'ink', kc, kind='mono')
                for (sl, colr, t0, dash) in ((s_obs, 'muted', 21.0, None), (s_nad, 'g', 23.5, None)):
                    pr = ramp(t, t0, 0.8, e_io)
                    if pr > 0:
                        draw_poly(c, ax.pts([-1, 1], [-sl, sl]), colr, kc, 4, prog=pr, dash=dash)
                text(c, f'observed {s_obs:+.1f} K', xx, 830, 18, 600, 'muted', ramp(t, 21.0, 0.6), kind='mono')
                text(c, f'straight down {s_nad:+.1f} K', xx, 858, 18, 600, 'g', ramp(t, 23.5, 0.6), kind='mono')
            note(c, 'two satellites over one spot: brightness difference vs difference in sec θ', 1140, 905, kc, 14)
            note(c, 'lines drawn from the fitted slopes, Fig. S7e, j', 1140, 930, kc, 14)

# ======================================================================= THE STRIPES VANISH
class Stripes(Scene):
    """Fig. S7a, c: ATMS channel 7, observed vs WeatherDreamer analysis decoded at nadir; parallax remains (§4.4)."""
    dur = 16.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (0.8, 'sweep')]
    A = (0.094, 0.094, 0.312, 0.254)
    C = (0.551, 0.094, 0.755, 0.254)

    def draw(self, c, t):
        hdr(c, t, '03', 'clue two', 'The *stripes* vanish', sub='microwave channel 7 (54.4 GHz), 20 Aug 2024, 12 hours of passes')
        for j, (sub, lab, xx, t0) in enumerate(((self.A, 'observed (two satellites)', 160, 0.6), (self.C, 'decoded straight down', 1000, 1.6))):
            k = ramp(t, t0, 0.8, e_expo)
            _, hh = figcard(c, 'figS7', xx, 372, 760, k, None, src=sub, k=k)
            text(c, lab, xx - 10, 346, 24, 600, 'g' if j else 'ink', k, kind='mono')
        note(c, 'Fig. S7a, c · ' + PAPER, 150, 925, ramp(t, 0.6, 0.6), 15)
        rich(c, 'It corrects {y:brightness}, not position: tall clouds seen at a slant stay slightly out of place.',
             W / 2, 985, 30, 1500, t, 5.5, 0.03, 0.5, 1, 'center')
