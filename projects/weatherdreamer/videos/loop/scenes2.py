"""Results, the turn, causes, the scoreboard, cost, questions and the end (arXiv:2611.18393v1 §4-§5, Table 2, S6).
Bars are typed from the text and Table 2 (section noted beside each); Fig. 4 and Fig. 6 are crops of the paper's
figures; the patch map, gain gauge and timelines are illustrations of numbers in the text; "our arithmetic" is ours."""
from loopkit import *

def legend3(c, x, y, a, fs=20):
    """WeatherDreamer / GEFS / IFS ENS swatches, in Fig. 4's colours."""
    for j, (colr, lab) in enumerate(((WD, 'WeatherDreamer'), (GEFS, 'American ensemble (GEFS)'), (IFS, 'European ensemble (IFS ENS)'))):
        xx = x + [0, 270, 640][j]
        rrect(c, xx, y - 15, 26, 18, 4, fill=colr, fa=a)
        text(c, lab, xx + 36, y, fs, 500, 'ink', a)

# ======================================================================= SURFACE
class Surface(Scene):
    """§4.1, Fig. 4: 534 held-out stations, 12 h forecasts; 10 m wind CRPS 1.09 / 1.31 / 1.15 m/s (mean of 1-12 h);
    T2m best for 8 h; spread-skill 0.63-0.78 / 0.23-0.47 / 0.26-0.41."""
    dur = 32.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (7.5, 'pop'), (13.0, 'whoosh_soft'), (21.0, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '04', 'down here', 'Near the ground, it *works*',
            sub='534 stations it never sees  ·  forecasts out to 12 hours  ·  50 starts, Aug 2024 – Aug 2025')
        # wind CRPS bars
        kw = ramp(t, 7.5, 0.8)
        if kw > 0:
            text(c, '10 m wind, average error score (CRPS, lower is better)', MX, 400, 22, 500, 'muted', kw, kind='mono')
            for j, (v, lab, colr) in enumerate(((1.09, 'WeatherDreamer', WD), (1.31, 'American', GEFS), (1.15, 'European', IFS))):
                hbar(c, MX, 430 + j * 56, 360, 1.4, v, lab, colr, kw, ramp(t, 7.7 + j * 0.2, 0.8, e_expo), fmt='{:.2f}',
                     lab_w=230)
            src(c, '§4.1 (mean of +1 to +12 h)', MX, 620, kw)
        # T2m: the crossover, Fig. 4a-c crop
        kt = ramp(t, 13.0, 0.9, e_expo)
        if kt > 0:
            figcard(c, 'fig4', 900, 360, 900, kt, 'Fig. 4a-c, CRPS vs lead time 0-12 h', k=kt, src=(0.0, 0.03, 0.75, 0.245))
            figcard(c, 'fig4', 1000, 640, 700, kt, None, k=kt, src=(0.12, 0.955, 0.88, 1.0), credit=False)
            text(c, 'temperature: best for 8 hours, then the European ensemble', 900, 740, 21, 600, 'ink', kt, kind='mono')
            note(c, 'in the figure WeatherDreamer is blue; light blue = no station input', 900, 772, kt, 16, 'muted')
        # calibration
        ks = ramp(t, 21.0, 0.8)
        if ks > 0:
            text(c, 'spread vs error (1 = calibrated)', MX, 720, 22, 500, 'muted', ks, kind='mono')
            x0, w = MX + 230, 460
            line(c, x0 + w, 740, x0 + w, 930, 'ink', ks * 0.7, 2, dash=[6, 6])
            text(c, '1.0', x0 + w, 960, 18, 500, 'muted', ks, 'center', kind='mono')
            for j, (lo, hi, lab, colr) in enumerate(((0.63, 0.78, 'WeatherDreamer', WD), (0.23, 0.47, 'American', GEFS),
                                                    (0.26, 0.41, 'European', IFS))):
                hbar(c, MX, 750 + j * 56, w, 1.0, hi, lab, colr, ks, ramp(t, 21.2 + j * 0.2, 0.8, e_expo), lab_w=230, lo=lo)
            note(c, 'all three still overconfident  ·  §4.1', MX, 960, ks, 16, 'muted')

# ======================================================================= UNSEEN
class Unseen(Scene):
    """§4.2: never inputs at inference. Rain vs IMERG: fair CRPS of 3-h totals at +3 h 0.255 / 0.310 / 0.331 mm,
    best to +6 h, mean rate about two-thirds of IMERG, too smooth. Cloud tops vs EarthCARE (Fig. 6): r 0.73 vs 0.70,
    RMSE 4.4 vs 4.8 km, false-alarm ratio 0.09 vs 0.19, probability of detection 0.80 vs 0.90."""
    dur = 30.0
    chapter = 3
    cues = [(0.2, 'whoosh'), (6.5, 'pop'), (13.0, 'whoosh_soft')]

    def draw(self, c, t):
        hdr(self, c, t, '04', 'down here', 'What it was *never* fed')
        k0 = ramp(t, 0.6, 0.8)
        for j, s in enumerate(['rain', 'sunlight at the ground', 'cloud-top height']):
            pill(c, MX + j * 300 + (0 if j < 2 else 120), 330, s, 'v', k0, filled=False, size=20)
        # rain
        kr = ramp(t, 6.5, 0.8)
        if kr > 0:
            text(c, 'rain, 3-hour totals at +3 h (CRPS, mm)', MX, 430, 22, 500, 'muted', kr, kind='mono')
            for j, (v, lab, colr) in enumerate(((0.255, 'WeatherDreamer', WD), (0.310, 'European', IFS), (0.331, 'American', GEFS))):
                hbar(c, MX, 460 + j * 54, 300, 0.4, v, lab, colr, kr, ramp(t, 6.7 + j * 0.2, 0.8, e_expo), fmt='{:.3f}',
                     lab_w=230)
            text(c, 'best ensemble for 6 hours, but:', MX, 680, 22, 600, 'ink', kr)
            text(c, '· about two-thirds of the observed rain', MX, 716, 21, 500, 'c', kr, kind='mono')
            text(c, '· too smooth at small scales', MX, 748, 21, 500, 'c', kr, kind='mono')
            src(c, '§4.2.1, vs IMERG', MX, 800, kr)
        # cloud tops
        kc = ramp(t, 13.0, 0.9, e_expo)
        if kc > 0:
            figcard(c, 'fig6', 860, 410, 480, kc, 'Fig. 6a (left), 6c', k=kc, src=(0.0, 0.0, 0.385, 0.43))
            figcard(c, 'fig6', 1380, 410, 420, kc, None, k=kc, src=(0.59, 0.0, 1.0, 0.43), credit=False)
            text(c, 'vs a radar + lidar satellite it never trained on (EarthCARE)', 860, 770, 20, 500, 'muted', kc, kind='mono')
            rows = [('height error (RMSE)', '4.4 km', '4.8 km'), ('correlation', '0.73', '0.70'),
                    ('false alarms (ratio)', '0.09', '0.19'), ('cloud detected', '0.80', '0.90')]
            text(c, 'WeatherDreamer', 1340, 815, 19, 600, WD, kc, 'center', kind='mono')
            text(c, 'operational (ACHA)', 1590, 815, 19, 600, 'muted', kc, 'center', kind='mono')
            for q, (lab, a_, b_) in enumerate(rows):
                k = ramp(t, 14.0 + q * 0.5, 0.6)
                y = 855 + q * 34
                text(c, lab, 860, y, 21, 500, 'ink', k)
                text(c, a_, 1340, y, 22, 600, WD, k, 'center', kind='mono')
                text(c, b_, 1590, y, 22, 600, 'muted', k, 'center', kind='mono')
            src(c, '§4.2.3', 860, 1000, kc)

# ======================================================================= ALOFT (the turn)
class Aloft(Scene):
    """§4.3.2, Table 2: SD of observation-minus-forecast, WeatherDreamer / GSI, matched 3-9 h leads, 30 cycles in
    2024. Ratios typed from Table 2 (range of per-channel ratios where given). §4.1 / Fig. 4d: sea-level pressure."""
    dur = 32.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (8.0, 'pop'), (11.5, 'draw'), (21.0, 'stamp_soft')]
    # (label, ratio, per-channel max or None, group) from Table 2
    ROWS = [('stations: humidity', 1.02, None, 0), ('stations: temperature', 1.04, None, 0), ('stations: wind', 1.08, None, 0),
            ('microwave moisture', 1.04, 1.23, 1), ('radio occultation', 1.15, 1.52, 1), ('balloon humidity', 1.30, None, 1),
            ('ocean winds (satellite)', 1.65, None, 1), ('microwave temp, troposphere', 1.76, 4.55, 1),
            ('balloon temperature', 1.79, None, 1), ('microwave temp, stratosphere', 1.84, 3.64, 1),
            ('balloon wind', 2.62, 3.51, 1)]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'up there', 'Then, higher *up*',
            sub='forecast error vs NOAA’s assimilation (GSI) on the same observations, 3-9 hours ahead')
        x0, lab_w, wmax, vmax = MX, 390, 900, 4.8
        y0, dy = 400, 50
        ka = ramp(t, 0.8, 0.8)
        X1 = x0 + lab_w + wmax / vmax
        if ka > 0:
            line(c, X1, y0 - 20, X1, y0 + len(self.ROWS) * dy, 'ink', ka * 0.7, 2, dash=[6, 6])
            text(c, 'same as NOAA', X1, y0 - 30, 18, 500, 'muted', ka, 'center', kind='mono')
            for v in (2, 3, 4):
                xx = x0 + lab_w + wmax * v / vmax
                line(c, xx, y0 - 20, xx, y0 + len(self.ROWS) * dy, 'line', ka, 1)
                text(c, f'{v}×', xx, y0 - 30, 18, 500, 'muted', ka, 'center', kind='mono')
        for i, (lab, v, vmax_ch, grp) in enumerate(self.ROWS):
            ti = 8.0 if grp == 0 else 11.5 + (i - 3) * 0.35
            k = ramp(t, ti, 0.6)
            if k <= 0:
                continue
            colr = 'f' if v < 1.12 else ('y' if v < 2.0 else 'c')
            y = y0 + i * dy
            hbar(c, x0, y, wmax, vmax, v, lab, colr, k, ramp(t, ti, 0.8, e_expo), fmt='{:.2f}×', lab_w=lab_w, h=32, fs=21)
            if vmax_ch:
                kx = ramp(t, ti + 0.6, 0.6)
                xa, xb = x0 + lab_w + wmax * v / vmax, x0 + lab_w + wmax * vmax_ch / vmax
                if xb - xa > 160:
                    line(c, xa + 90, y + 16, xb, y + 16, colr, kx * 0.6, 2, dash=[4, 5])
                    text(c, f'{vmax_ch:.2f}', xb + 8, y + 22, 17, 500, colr, kx, kind='mono')
                else:
                    text(c, f'(worst {vmax_ch:.2f})', xa + 92, y + 22, 17, 500, colr, kx, kind='mono')
        src(c, 'Table 2 (dashes: worst single channel or level)', MX, y0 + len(self.ROWS) * dy + 30, ka)
        kp = ramp(t, 21.0, 0.9, e_expo)
        if kp > 0:
            figcard(c, 'fig4', 1490, 600, 300, kp, 'Fig. 4d', k=kp, src=(0.755, 0.03, 1.0, 0.245))
            text(c, 'sea-level pressure', 1480, 560, 21, 600, 'c', kp, kind='mono')

# ======================================================================= WALLS
class Walls(Scene):
    """§5: dynamics on regional patches of about 1,600 km (32 × 32 nodes of ~50 km), each with its own memory
    (patches overlap 50 % and are blended, §3.7). Our arithmetic: 50 m/s = 180 km/h -> ~9 h to cross 1,600 km;
    5-10 m/s -> 220-430 km in 12 h. Map: illustration."""
    dur = 28.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (0.8, 'draw'), (9.0, 'sweep'), (16.0, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'cause one', 'The *walls*')
        mx, my, mw, mh = MX, 340, 1100, 560
        P = 220          # one patch = 1,600 km on this map (5 x ~2.5 patches shown)
        k0 = ramp(t, 0.8, 0.8)
        if k0 > 0:
            rrect(c, mx, my, mw, mh, 12, fill='#141827', fa=k0)
            for i in range(6):
                line(c, mx + i * P, my, mx + i * P, my + mh, 'faint', k0, 2)
            for j in range(3):
                line(c, mx, my + j * P, mx + mw, my + j * P, 'faint', k0, 2)
            rrect(c, mx + 2 * P, my + P, P, P, 6, stroke='y', sw=3.4, a=k0, glow=6)
            text(c, '≈ 1,600 km', mx + 2.5 * P, my + 2 * P + 30, 20, 600, 'y', k0, 'center', kind='mono')
            text(c, 'own memory', mx + 2.5 * P, my + 1.5 * P + 8, 20, 500, 'y', k0, 'center', kind='mono')
            tag(c, ILLUS + '  ·  §3.7, §5', mx, my + mh + 30, k0)
        # jet stream
        kj = ramp(t, 9.0, 0.8)
        if kj > 0:
            xs = np.linspace(mx + 10, mx + mw - 10, 200)
            ys = my + 1.5 * P + 70 * np.sin((xs - mx) / 170 + 2.2)
            pr = ramp(t, 9.0, 2.5, e_io)
            draw_poly(c, np.stack([xs, ys], 1), 'c', kj, 6, prog=pr, glow=8)
            text(c, 'jet stream, 50 m/s', mx + mw - 20, my + 60, 22, 600, 'c', kj, 'right', kind='mono')
            text(c, 'crosses a patch in ≈ 9 h', mx + mw - 20, my + 92, 22, 500, 'c', kj, 'right', kind='mono')
            # surface wind: a short arrow, 12 h of travel
            sx, sy = mx + 2 * P + 50, my + 1.7 * P
            arrow(c, sx, sy, sx + P * 330 / 1600, sy, 'f', kj, 4, 12, prog=ramp(t, 10.5, 0.8, e_io))
            text(c, 'surface wind: 220-430 km in 12 h', mx + 20, my + mh - 24, 20, 500, 'f', kj, kind='mono')
            tag(c, OURS, mx + mw, my + mh + 30, kj, 'right')
        # the big slow circulation
        kb = ramp(t, 16.0, 1.0)
        if kb > 0:
            with layer(c, kb * 0.9):
                c.drawOval(skia.Rect.MakeXYWH(mx + 40, my + 50, 800, 440), paint('x', 0.08))
                c.drawOval(skia.Rect.MakeXYWH(mx + 40, my + 50, 800, 440), paint('x', 0.8, stroke=3))
                text(c, 'L', mx + 300, my + 200, 80, 700, 'x', 0.9, 'center')
        x2 = 1290
        rich(c, 'The paper: patches limit the {x:large, slowly evolving circulation} that governs upper-level winds and pressure changes.',
             x2, 420, 30, 520, t, 16.3, 0.03, 0.5, kb, base_w=400)
        src(c, '§5', x2, 640, kb)

# ======================================================================= LISTENING
class Listening(Scene):
    """§4.3.3, Fig. 8: learned gain vs optimum. Radiosonde T and wind gains 0.1-0.26 at 100-300 hPa; radio occultation
    near zero; microwave temperature channels k ≈ 0.64 vs k_opt ≈ 0.82. Gauge: illustration of those numbers."""
    dur = 22.0
    chapter = 4
    cues = [(0.2, 'whoosh'), (3.5, 'tick'), (13.0, 'stamp_soft')]

    def draw(self, c, t):
        hdr(self, c, t, '05', 'cause two', 'It barely *listens* up there',
            sub='gain: how far each correction moves toward an observation (0 = ignore, 1 = believe it fully)')
        x0, x1, y0 = MX + 420, W - MX - 60, 420
        X = lambda v: x0 + (x1 - x0) * v
        k0 = ramp(t, 1.0, 0.8)
        if k0 > 0:
            for v in (0, 0.25, 0.5, 0.75, 1.0):
                line(c, X(v), y0 - 20, X(v), y0 + 330, 'line', k0, 1)
                text(c, f'{v:g}', X(v), y0 - 32, 18, 500, 'muted', k0, 'center', kind='mono')
        rows = [(3.5, 'balloons, 100-300 hPa', 0.10, 0.26, 'c'), (6.0, 'radio occultation', 0.0, 0.03, 'c'),
                (8.5, 'microwave temperature', 0.64, 0.64, 'y')]
        for i, (ti, lab, lo, hi, colr) in enumerate(rows):
            k = ramp(t, ti, 0.7)
            if k <= 0:
                continue
            y = y0 + i * 110
            text(c, lab, x0 - 24, y + 24, 25, 500, 'ink', k, 'right')
            if hi > lo:
                rrect(c, X(lo), y, (X(hi) - X(lo)) * ramp(t, ti, 0.8, e_expo), 34, 17, fill=colr, fa=k * 0.85)
                txt = '≈ 0' if hi < 0.05 else f'{lo:.2f}–{hi:.2f}'
                text(c, txt, X(hi) + 16, y + 26, 22, 600, colr, k, kind='mono')
            else:
                circle(c, X(lo), y + 17, 12, fill=colr, a=k)
                text(c, '0.64', X(lo) - 20, y + 26, 22, 600, colr, k, 'right', kind='mono')
                kx = ramp(t, ti + 0.8, 0.6)
                circle(c, X(0.82), y + 17, 12, stroke='f', sw=3, a=kx)
                text(c, 'best ≈ 0.82', X(0.82) + 22, y + 26, 22, 600, 'f', kx, kind='mono')
        src(c, '§4.3.3, Fig. 8', MX, y0 + 360, k0)
        tag(c, 'gauge: ' + ILLUS, W - MX, y0 + 360, k0, 'right')
        rich(c, 'It leans only lightly on the clues it {c:needed most}.', W / 2, 960, 40, 1600, t, 13.0, 0.04, 0.5,
             ramp(t, 13.0, 0.6), 'center', base_w=500)

# ======================================================================= SCOREBOARD
class Scoreboard(Scene):
    """S6.2: Set A runs with operational latency: baselines use the newest cycle disseminated by the start time:
    GEFS >= 5 h old, IFS ENS >= 7 h old. §4.1: IFS ENS overtakes WD's T2m CRPS after ~8 h; ensemble-mean MAE beats
    IFS ENS only for T, first 3 h; §5: held-out stations are a random 5 %, many with assimilated neighbours; §4.1:
    with ISD withheld, WD still beats GEFS for T2m to 11 h and wind at every lead. Timeline: illustration."""
    dur = 32.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (0.8, 'pop'), (9.0, 'tick'), (17.5, 'pop'), (25.5, 'chime')]

    def draw(self, c, t):
        hdr(self, c, t, '06', 'the scoreboard', 'Reading the *scoreboard*')
        x0, x1, y = MX + 80, W - MX - 40, 470
        h0, h1 = -9, 13
        X = lambda hh: x0 + (x1 - x0) * (hh - h0) / (h1 - h0)
        k0 = ramp(t, 0.8, 0.8)
        if k0 > 0:
            line(c, x0, y, x1, y, 'muted', k0, 2)
            for hh in range(h0, h1 + 1, 3 if False else 1):
                if hh % 3 == 0:
                    line(c, X(hh), y - 8, X(hh), y + 8, 'muted', k0, 2)
                    text(c, f'{hh:+d} h' if hh else 'start', X(hh), y + 40, 18, 500, 'muted', k0, 'center', kind='mono')
            circle(c, X(0), y, 13, fill=WD, a=k0, glow=8)
            text(c, 'WeatherDreamer: fresh analysis', X(0), y - 70, 21, 600, WD, k0, 'center', kind='mono')
            text(c, 'every hour', X(0), y - 42, 19, 500, WD, k0, 'center', kind='mono')
            for hh, lab, colr, dy in ((-5, 'American: ≥ 5 h old', GEFS, -42), (-7, 'European: ≥ 7 h old', IFS, -86)):
                kk = ramp(t, 1.4 + (0.4 if hh == -7 else 0), 0.6)
                circle(c, X(hh), y, 10, fill=colr, a=kk)
                line(c, X(hh), y - 10, X(hh), y + dy + 14, colr, kk * 0.6, 1.5)
                text(c, lab, X(hh) - 12, y + dy, 20, 600, colr, kk, 'right', kind='mono')
        kx = ramp(t, 9.0, 0.8)
        if kx > 0:
            line(c, X(-7), y + 80, X(8), y + 80, IFS, kx, 3)
            for xx in (X(-7), X(8)):
                line(c, xx, y + 70, xx, y + 90, IFS, kx, 3)
            text(c, 'at +8 h the European forecast is 15+ hours old, and still pulls ahead on temperature', X(0.5), y + 120,
                 21, 600, IFS, kx, 'center', kind='mono')
            text(c, 'fair for usefulness, not a test of the forecasting engine', X(0.5), y + 152, 19, 500, 'muted', kx,
                 'center', kind='mono')
        ks = ramp(t, 17.5, 0.8)
        if ks > 0:
            panel(c, MX, 700, 820, 170, ks)
            text(c, 'its edge comes mostly from spread', MX + 30, 750, 24, 600, 'ink', ks)
            text(c, 'average forecast beats the European one', MX + 30, 790, 20, 500, 'muted', ks, kind='mono')
            text(c, 'only for temperature, first 3 hours', MX + 30, 820, 20, 500, 'muted', ks, kind='mono')
            panel(c, MX + 860, 700, 820, 170, ks)
            text(c, 'hidden stations have neighbours', MX + 890, 750, 24, 600, 'ink', ks)
            text(c, 'a random 5%: many sit near stations it reads', MX + 890, 790, 20, 500, 'muted', ks, kind='mono')
            text(c, 'baselines not adjusted for station height (our reading)', MX + 890, 820, 20, 500, 'y', ks, kind='mono')
        kn = ramp(t, 25.5, 0.8)
        rich(c, 'With {y:no stations at all}: still beats the American ensemble, temperature to 11 h, wind to 12 h.',
             W / 2, 950, 32, 1600, t, 25.5, 0.03, 0.5, kn, 'center', base_w=500)
        src(c, 'S6.2, §4.1, §5', W - MX, 330, k0, 'right')

# ======================================================================= SPEED
class Speed(Scene):
    """§5: one global hourly step ≈ 1.5 min on one H100 (≈ 45 s model, ≈ 45 s reading observations); a 12 h, 8 + 1
    member forecast ≈ 11 min. §3.5, §3.7: memory and latent start at zero; 12 h (13-step) windows; continuous cycling
    left to future work."""
    dur = 26.0
    chapter = 5
    cues = [(0.2, 'whoosh'), (0.8, 'count'), (8.5, 'pop'), (12.0, 'drop')]

    def draw(self, c, t):
        hdr(self, c, t, '06', 'the cost', 'An analysis every *hour*')
        k0 = ramp(t, 0.8, 0.9, e_expo)
        stat(c, MX, 470, '≈ 1.5 min', 'one global hourly update, one GPU (H100)', 'y', k0, 92)
        kb = ramp(t, 3.5, 0.8)
        if kb > 0:
            bx, bw = MX, 700
            rrect(c, bx, 560, bw / 2 * ramp(t, 3.5, 0.8, e_expo), 40, 6, fill='y', fa=kb * 0.85)
            rrect(c, bx + bw / 2, 560, bw / 2 * ramp(t, 4.0, 0.8, e_expo), 40, 6, fill='muted', fa=kb * 0.6)
            text(c, '≈ 45 s model', bx + 12, 588, 19, 600, '#1a1206', kb, kind='mono')
            text(c, '≈ 45 s reading the data', bx + bw / 2 + 12, 588, 19, 600, '#111111', kb, kind='mono')
        k2 = ramp(t, 8.5, 0.9, e_expo)
        stat(c, 1050, 470, '11 min', '12-hour ensemble forecast (8 + control)', 'g', k2, 92)
        src(c, '§5', MX, 650, k0)
        # the limit: a memory that starts empty
        kl = ramp(t, 12.0, 0.8)
        if kl > 0:
            panel(c, MX, 700, W - 2 * MX, 240, kl)
            text(c, 'every run in the paper', MX + 40, 755, 26, 600, 'ink', kl)
            x0, x1 = MX + 40, W - MX - 380
            for r in range(3):
                xs = x0 + r * (x1 - x0) / 3
                fill_ = ramp(t, 12.6 + r * 0.9, 0.9, e_io)
                rrect(c, xs, 800, (x1 - x0) / 3 - 30, 34, 8, stroke='v', sw=2, a=kl)
                rrect(c, xs, 800, ((x1 - x0) / 3 - 30) * fill_, 34, 8, fill='v', fa=kl * 0.6)
                text(c, 'memory = 0 → 12 h catch-up → forecast', xs, 870, 17, 500, 'muted', kl, kind='mono')
            text(c, 'continuous cycling:', W - MX - 340, 805, 22, 600, 'c', kl, kind='mono')
            text(c, 'future work', W - MX - 340, 840, 22, 600, 'c', kl, kind='mono')
            tag(c, ILLUS + '  ·  §3.5', MX + 40, 920, kl)

# ======================================================================= QUESTIONS, END
class Questions(Scene):
    dur = 24.0
    chapter = 6
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (9.0, 'pop'), (14.5, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '07', 'to think about', 'Questions to *think* about')
        question_cards(c, t, [
            ('Trained only on observations, does it inherit our {y:instruments’ habits}, the way reanalysis passes on a physics model’s?', 2.0),
            ('How would you teach it to listen to {y:rare, precise} instruments high up?', 9.0),
            ('Could a learned picture of the present one day {y:start climate models}?', 14.5),
        ], y0=320, dy=200, h=170)

class End(EndCard):
    dur = 14.0
    TAKE = 'A forecast loop can be learned from {y:the clues alone}. Near the ground it already sees well; up high, it still has to {y:learn to listen}.'
    STATS = [('1.5 min', 'per global hourly analysis', 'y'), ('2.6×', 'balloon-wind error vs NOAA', 'c'),
             ('0', 'reanalysis used', 'g')]
