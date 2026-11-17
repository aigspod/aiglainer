"""Cold open, title, the problem of "now", the classical loop, the learned loop, no answer key, three lessons
(arXiv:2611.18393v1 §1-§3). Globe pictures are illustrations (computed observing patterns, no coastlines); Fig. 1 is a
crop of the paper's figure; numbers are typed from the text with their section."""
from loopkit import *

# ======================================================================= COLD OPEN
class ColdOpen(Scene):
    """Nobody can see right now: stations, balloons and satellite swaths appear on a turning globe (illustration)."""
    dur = 27.0
    fade_in = 0.8
    cues = [(0.4, 'whoosh_soft'), (5.0, 'blip'), (8.0, 'blip'), (10.5, 'sweep'), (13.8, 'draw'), (20.5, 'riser')]

    def draw(self, c, t):
        g = Globe(600, 570, 380, -70 + 2.2 * t, 22)
        g.draw(c, ramp(t, 0.2, 1.4))
        # the picture "right now" that nobody has: a faint field that never quite resolves
        ks = ramp(t, 5.0, 1.2)
        g.dots(c, STATIONS, 'ink', 3.0, ks * 0.85, prog=ramp(t, 5.0, 2.5, e_io))
        kb = ramp(t, 8.0, 1.0)
        rise = 18 * (0.5 + 0.5 * math.sin(t * 2.0))
        g.dots(c, BALLOONS, 'f', 5.5, kb, prog=ramp(t, 8.0, 1.5, e_io), glow=0)
        kp = ramp(t, 10.5, 1.0)
        for i in range(5):
            lo, la = polar_track(i, lon_start=-30)
            g.track(c, lo, la, 'g', 16, kp * 0.22, prog=ramp(t, 10.5 + i * 0.25, 2.0, e_io))
            g.track(c, lo, la, 'g', 2, kp * 0.7, prog=ramp(t, 10.5 + i * 0.25, 2.0, e_io))
        tag(c, ILLUS, 600, 1000, ramp(t, 1.0, 0.8), 'center')
        # the words
        x0 = 1100
        rich(c, 'Every forecast starts from {y:right now}.', x0, 330, 48, 800, t, 0.8, 0.05, 0.55,
             window(t, 0.8, 20.0, d_out=0.6), base_w=600)
        items = [(5.0, 'stations dot the land', 'ink'), (8.0, 'balloons rise twice a day', 'f'),
                 (10.5, 'satellites sweep past in stripes', 'g')]
        for j, (ti, s, colr) in enumerate(items):
            k = ramp(t, ti, 0.7) * window(t, ti, 20.0, d_out=0.6)
            if k <= 0:
                continue
            y = 520 + j * 64
            circle(c, x0 + 10, y - 9, 8, fill=colr, a=k)
            text(c, s, x0 + 36, y, 30, 500, 'ink', k)
        kd = ramp(t, 13.8, 0.8) * window(t, 13.8, 20.0, d_out=0.6)
        if kd > 0:
            arrow(c, x0 + 10, 740, x0 + 10, 800, 'muted', kd, 2.4, 12, prog=ramp(t, 13.8, 0.6, e_io))
            text(c, 'one picture of now:', x0 + 36, 778, 26, 500, 'muted', kd, kind='mono')
            text(c, 'slow, expensive, and every forecast waits for it', x0 + 36, 822, 26, 400, 'ink', kd, kind='italic')
        rich(c, 'Can a machine learn to see {y:the present},', x0, 420, 50, 740, t, 20.5, 0.05, 0.55, ramp(t, 20.5, 0.6),
             base_w=600)
        rich(c, 'with {y:no answer key}?', x0, 560, 50, 740, t, 22.5, 0.05, 0.55, ramp(t, 22.5, 0.6), base_w=600)

# ======================================================================= TITLE
class Title(TitleCard):
    dur = 10.0

# ======================================================================= CLUES
class Clues(Scene):
    """The observing system (§1, §2.1, Table 1): ~11,000 stations hourly; ~650 soundings at 00 and 12 UTC;
    satellites measure radiances."""
    dur = 30.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (8.5, 'pop'), (14.5, 'pop'), (23.5, 'stamp')]

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the clues', 'What we can *actually* see')
        cw, gap, y0, ch = 532, 42, 340, 520
        cards = [(0.6, '≈ 11,000', 'surface stations', ['report every hour', 'on land, near the ground'], 'ink'),
                 (8.5, '≈ 650', 'weather balloons', ['through the whole column', 'twice a day: 00 and 12 UTC'], 'f'),
                 (14.5, 'light', 'satellites', ['radiance, not temperature', 'glow from a deep column of air'], 'g')]
        for i, (ti, big, lab, lines_, colr) in enumerate(cards):
            k = ramp(t, ti, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    # the icon
                    ix, iy = x + cw / 2, y0 + 200
                    if i == 0:
                        for q in range(5):
                            station_icon(c, ix - 160 + q * 80, iy + 20 - (q % 2) * 14, 0.9, 1, 'ink')
                        line(c, ix - 220, iy + 22, ix + 220, iy + 22, 'faint', 1, 2)
                    elif i == 1:
                        rise = 60 * ((t - ti) * 0.25 % 1.0)
                        balloon_icon(c, ix, iy + 10, 1.3, 1, 'f', rise=rise)
                        for q in range(4):
                            line(c, ix - 200, iy - 120 + q * 40, ix + 200, iy - 120 + q * 40, 'faint', 0.6, 1, dash=[6, 8])
                    else:
                        satellite_icon(c, ix, iy - 120, 1.3, 1, 'ink', beam=ramp(t, ti + 0.6, 0.8), beam_len=170)
                        rrect(c, ix - 150, iy + 30, 300, 16, 4, fill='g', fa=0.18)
                    text(c, big, x + 36, y0 + 340, 60, 300, colr, 1, kind='italic')
                    text(c, lab, x + 36, y0 + 392, 28, 600, 'ink', 1)
                    for q, ln in enumerate(lines_):
                        text(c, ln, x + 36, y0 + 440 + q * 34, 21, 500, 'muted', 1, kind='mono')
        src(c, '§2.1, Table 1', MX, 900, ramp(t, 1.0, 0.8))
        tag(c, 'icons: ' + ILLUS, W - MX, 900, ramp(t, 1.0, 0.8), 'right')
        ks = ramp(t, 23.5, 0.5, e_back)
        stamp(c, 'sparse · irregular · indirect', W / 2, 975, 'c', window(t, 23.5, None), ks, rot=-2, size=30)

# ======================================================================= ANALYSIS
class Analysis(Scene):
    """Data assimilation produces the analysis; global DA every 6 h, hours late, hand-built operators (§1);
    ML forecasters start from analyses (§1). Pipeline diagram: illustration."""
    dur = 30.0
    chapter = 0
    cues = [(0.2, 'whoosh'), (7.5, 'tick'), (15.0, 'pop'), (23.0, 'stamp_soft')]

    def draw(self, c, t):
        hdr(self, c, t, '01', 'the expensive step', 'Building *now*: data assimilation')
        y = 470
        k0 = ramp(t, 0.6, 0.8, e_expo)
        # clues
        with layer(c, k0):
            for j, colr in enumerate(['ink', 'f', 'g']):
                circle(c, MX + 40, y + 10 + j * 50, 12, fill=colr, a=1)
            text(c, 'clues', MX + 20, y + 190, 22, 500, 'muted', 1, kind='mono')
        curved(c, (MX + 80, y + 60), (MX + 230, y + 60), 0, 'muted', k0, ramp(t, 1.0, 0.6, e_io))
        # data assimilation box
        node(c, MX + 250, y - 30, 420, 180, 'data assimilation', 'c', k0, sub='physics model + hand-built parts', size=32,
             k=k0)
        curved(c, (MX + 690, y + 60), (MX + 810, y + 60), 0, 'muted', k0, ramp(t, 1.6, 0.6, e_io))
        # the analysis
        g = Globe(MX + 900, y + 60, 86, -40 + 3 * t, 20)
        with layer(c, k0):
            g.draw(c, 1)
            g.dots(c, STATIONS[::4], 'y', 2.2, 0.8)
        text(c, 'the analysis', MX + 900, y + 200, 24, 500, 'y', k0, 'center', kind='mono')
        # cycle clock and lateness
        kc = ramp(t, 7.5, 0.8)
        if kc > 0:
            cx, cy = MX + 460, y + 290
            circle(c, cx, cy, 52, stroke='c', sw=3, a=kc)
            for q in range(4):
                ang = q * math.pi / 2
                line(c, cx + 42 * math.sin(ang), cy - 42 * math.cos(ang), cx + 52 * math.sin(ang), cy - 52 * math.cos(ang), 'c', kc, 3)
            ang = 2 * math.pi * ((t - 7.5) / 6.0 % 1.0)
            line(c, cx, cy, cx + 38 * math.sin(ang), cy - 38 * math.cos(ang), 'ink', kc, 3)
            text(c, 'every 6 hours', cx + 80, cy - 6, 26, 600, 'ink', kc)
            text(c, 'and it arrives hours late', cx + 80, cy + 30, 22, 500, 'muted', kc, kind='mono')
            text(c, 'for every instrument: an observation operator, a bias correction, an error model',
                 MX + 250, y + 430, 21, 500, 'c', kc, kind='mono')
        # ML forecaster
        kf = ramp(t, 15.0, 0.8, e_expo)
        curved(c, (MX + 1000, y + 60), (MX + 1120, y + 60), 0, 'muted', kf, ramp(t, 15.0, 0.6, e_io))
        node(c, MX + 1140, y - 30, 380, 180, 'AI forecaster', 'y', kf, sub='GraphCast, Pangu-Weather, ...', size=32, k=kf,
             glow=6 * kf)
        kn = ramp(t, 23.0, 0.8)
        if kn > 0:
            line(c, MX + 250, y - 70, MX + 1020, y - 70, 'c', kn, 2.4)
            for xx in (MX + 250, MX + 1020):
                line(c, xx, y - 70, xx, y - 52, 'c', kn, 2.4)
            text(c, 'still physics-built', MX + 635, y - 86, 22, 500, 'c', kn, 'center', kind='mono')
        rich(c, 'They learned to {y:forecast}. They never learned to {c:see}.', W / 2, 1000, 40, 1600, t, 23.0, 0.04,
             0.5, ramp(t, 23.0, 0.6), 'center', base_w=500)
        tag(c, ILLUS, W - MX, 330, ramp(t, 1.0, 0.8), 'right')

# ======================================================================= KALMAN
class Kalman(Scene):
    """The predict-correct loop (Eq. 1-3, Kalman 1960) and a one-variable gain (illustration: 20 vs 22 degrees,
    sigma_B = 1, sigma_O = 0.5, so k = 0.8 and the analysis is 21.6)."""
    dur = 34.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (4.0, 'pop'), (9.5, 'pop'), (15.0, 'draw'), (24.0, 'tick')]

    def draw(self, c, t):
        hdr(self, c, t, '02', 'the old loop', 'Predict, then *correct*')
        # the loop: two nodes on a circle
        cx, cy, R = 470, 600, 190
        k0 = ramp(t, 0.6, 0.8, e_expo)
        node(c, cx - 150, cy - R - 60, 300, 110, 'predict', BG, k0, sub='background', size=32, k=k0)
        node(c, cx - 150, cy + R - 50, 300, 110, 'correct', AN, k0, sub='analysis', size=32, k=k0)
        spin = ramp(t, 1.0, 1.2, e_io)
        curved(c, (cx + 160, cy - R + 10), (cx + 160, cy + R - 10), -0.45, BG, k0, spin)
        curved(c, (cx - 160, cy + R - 10), (cx - 160, cy - R + 10), -0.45, AN, k0, spin)
        ko = ramp(t, 9.5, 0.7)
        if ko > 0:
            for j in range(3):
                circle(c, cx - 420 + j * 26, cy + R + 4, 9, fill=OBS, a=ko)
            arrow(c, cx - 330, cy + R + 4, cx - 165, cy + R + 4, OBS, ko, 2.6, 12, prog=ramp(t, 9.5, 0.6, e_io))
            text(c, 'new observations  y', cx - 420, cy + R + 60, 20, 500, OBS, ko, kind='mono')
        # equations
        tex(c, 'kb', 1300, 380, 44, ramp(t, 4.0, 0.8), reveal=ramp(t, 4.0, 1.0, e_io))
        tex(c, 'ka', 1300, 480, 44, ramp(t, 9.5, 0.8), reveal=ramp(t, 9.5, 1.0, e_io))
        tex(c, 'kgain', 1300, 570, 40, ramp(t, 11.0, 0.8), reveal=ramp(t, 11.0, 1.0, e_io))
        note(c, 'Eq. 1-3 · M: the forecast model · H: what each instrument would see · B, R: error covariances',
             1300, 630, ramp(t, 11.5, 0.7), 16, 'muted', 'center')
        # the one-number example
        ke = ramp(t, 15.0, 0.8)
        if ke > 0:
            x0, x1, y = 1080, 1720, 870
            v0, v1 = 18.0, 24.0
            X = lambda v: x0 + (v - v0) / (v1 - v0) * (x1 - x0)
            line(c, x0, y, x1, y, 'muted', ke, 2)
            for v in range(18, 25):
                line(c, X(v), y - 8, X(v), y + 8, 'muted', ke, 2)
                text(c, f'{v}°', X(v), y + 38, 20, 500, 'muted', ke, 'center', kind='mono')
            # forecast 20 (sigma 1), thermometer 22 (sigma 0.5)
            for v, sg, colr, lab, dy in ((20, 1.0, BG, 'forecast  ±1°', -40), (22, 0.5, OBS, 'thermometer  ±0.5°', -78)):
                rrect(c, X(v - sg), y - 16, X(v + sg) - X(v - sg), 32, 16, fill=colr, fa=ke * 0.22)
                circle(c, X(v), y, 10, fill=colr, a=ke)
                text(c, lab, X(v), y + dy, 22, 500, colr, ke, 'center', kind='mono')
            km = ramp(t, 18.5, 1.2, e_io)
            va = 20 + 0.8 * 2 * km
            circle(c, X(va), y, 13, stroke=AN, sw=3.4, a=ke * clamp(km * 3), glow=8)
            ka = ramp(t, 19.5, 0.6)
            text(c, 'analysis 21.6°: move 80% of the way', X(21.6), y + 84, 22, 600, AN, ka, 'center', kind='mono')
            tex(c, 'k1', 880, y, 38, ka)
            tag(c, ILLUS, x1, y + 125, ke, 'right')
        kk = ramp(t, 24.0, 0.7)
        if kk > 0:
            text(c, 'Rudolf Kalman, 1960', 1300, 700, 28, 400, 'ink', kk, 'center', kind='italic')
            text(c, 'operational systems: every error set by hand', 1300, 740, 20, 500, 'c', kk, 'center', kind='mono')

# ======================================================================= DREAMER
class Dreamer(Scene):
    """The learned loop (§3.1-3.6, Eq. 4-7): per ~50 km cell, memory h (512) and latent z (64); prior = background,
    posterior = analysis, decoders = observation operator; the posterior network replaces the gain. Diagram:
    illustration."""
    dur = 34.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (4.5, 'pop'), (12.5, 'pop'), (18.5, 'pop'), (26.0, 'draw')]

    def draw(self, c, t):
        hdr(self, c, t, '03', 'the learned loop', 'The same loop, *learned*')
        # the grid and one cell
        kg = ramp(t, 4.5, 0.8)
        if kg > 0:
            gx, gy, cs = MX, 350, 34
            for i in range(7):
                for j in range(7):
                    rrect(c, gx + j * cs, gy + i * cs, cs - 3, cs - 3, 4, fill='faint', fa=kg * 0.5)
            rrect(c, gx + 3 * cs, gy + 3 * cs, cs - 3, cs - 3, 4, fill='y', fa=kg)
            text(c, '≈ 50 km cells', gx, gy + 7 * cs + 34, 20, 500, 'muted', kg, kind='mono')
            arrow(c, gx + 4 * cs + 4, gy + 3.5 * cs, gx + 300, gy + 60, 'muted', kg, 2, 10, prog=ramp(t, 5.0, 0.5, e_io))
            # memory 512 vs latent 64 (widths to scale)
            bx = gx + 320
            kb = ramp(t, 5.4, 1.0, e_io)
            rrect(c, bx, gy + 30, 512 * 1.4 * kb, 50, 8, fill='v', fa=kg * 0.55)
            for q in range(int(64 * kb)):
                line(c, bx + q * 11.2, gy + 30, bx + q * 11.2, gy + 80, '#000000', kg * 0.12, 1)
            text(c, 'memory  h  ·  512 numbers', bx, gy + 18, 22, 500, 'ink', kg, kind='mono')
            rrect(c, bx, gy + 140, 64 * 1.4 * kb, 50, 8, fill='y', fa=kg * 0.9)
            text(c, 'latent state  z  ·  64', bx, gy + 128, 22, 500, 'y', kg, kind='mono')
            text(c, 'what it remembers', bx + 740, gy + 64, 20, 500, 'muted', kg, kind='mono')
            text(c, 'the weather here, now', bx + 120, gy + 174, 20, 500, 'muted', kg, kind='mono')
        # the flow
        y = 700
        kp = ramp(t, 12.5, 0.8, e_expo)
        node(c, MX, y - 55, 250, 110, 'memory', 'v', kp, sub='h  (t-1 → t)', size=28, k=kp)
        curved(c, (MX + 260, y), (MX + 360, y), 0, 'muted', kp, ramp(t, 12.8, 0.5, e_io))
        node(c, MX + 370, y - 55, 300, 110, 'background', BG, kp, sub='prior', size=28, k=kp)
        tex(c, 'wprior', MX + 520, y + 100, 34, kp)
        kq = ramp(t, 18.5, 0.8, e_expo)
        curved(c, (MX + 680, y), (MX + 780, y), 0, 'muted', kq, ramp(t, 18.8, 0.5, e_io))
        node(c, MX + 790, y - 55, 300, 110, 'analysis', AN, kq, sub='posterior', size=28, k=kq, glow=6 * kq)
        tex(c, 'wpost', MX + 940, y + 100, 34, kq)
        if kq > 0:
            for j in range(6):
                ox = MX + 800 + j * 50
                oy = y - 190 + 40 * (1 - ramp(t, 18.5 + j * 0.12, 0.8, e_io))
                circle(c, ox, oy, 9, fill=OBS, a=kq)
                line(c, ox, oy + 10, MX + 940, y - 58, OBS, kq * 0.35, 1.4)
            text(c, 'observations, read through the memory (attention)', MX + 790, y - 225, 19, 500, OBS, kq, kind='mono')
        kd = ramp(t, 26.0, 0.8, e_expo)
        curved(c, (MX + 1100, y), (MX + 1200, y), 0, 'muted', kd, ramp(t, 26.2, 0.5, e_io))
        node(c, MX + 1210, y - 55, 280, 110, 'decoders', OBS, kd, sub='any instrument, anywhere', size=28, k=kd)
        tex(c, 'wdec', MX + 1350, y + 100, 34, kd)
        # the gain is learned
        kl = ramp(t, 28.0, 0.7)
        if kl > 0:
            pairs = [('background', 'prior'), ('analysis', 'posterior'), ('operator H', 'decoders'), ('gain from B, R', 'learned')]
            for q, (a_, b_) in enumerate(pairs):
                x = MX + q * 420
                text(c, a_, x, 930, 21, 500, 'muted', kl, kind='mono')
                text(c, '→  ' + b_, x + text_width(a_, 21, 500, 'mono') + 12, 930, 21, 600, 'y' if q == 3 else 'ink', kl, kind='mono')
        tag(c, ILLUS + '  ·  Eq. 4-7', W - MX, 330, ramp(t, 1.0, 0.8), 'right')

# ======================================================================= NO ANSWER KEY
class NoKey(Scene):
    """No reanalysis in training or inference (§1); 18 observing systems, 2020-2023 (§2, §3.7); Fig. 1 crop; earlier
    observation-to-observation models build each forecast from a fixed window in one pass (§1)."""
    dur = 30.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (7.5, 'stamp'), (14.5, 'whoosh_soft'), (21.5, 'pop')]
    SYSTEMS = ['geostationary infrared ×4', 'microwave sounders ×4', 'infrared sounders ×2', 'ocean-wind scatterometers',
               'radio occultation', 'cloud radar + lidar', 'surface stations', 'weather balloons', '+ rain, sunlight grids']

    def draw(self, c, t):
        hdr(self, c, t, '03', 'the learned loop', 'No *answer key*')
        kl = ramp(t, 0.6, 0.8) * window(t, 0.6, 14.2, d_out=0.5)
        if kl > 0:
            text(c, '18 observing systems', MX, 380, 40, 400, 'y', kl, kind='italic')
            text(c, 'trained on 2020–2023 · tested on 2024–2025', MX, 425, 21, 500, 'muted', kl, kind='mono')
            for q, s in enumerate(self.SYSTEMS):
                k = ramp(t, 1.0 + q * 0.18, 0.5) * kl
                circle(c, MX + 10, 485 + q * 46 - 7, 6, fill=OBS, a=k)
                text(c, s, MX + 30, 485 + q * 46, 24, 500, 'ink', k)
            kr = ramp(t, 7.5, 0.6) * kl
            panel(c, 1000, 460, 680, 250, kr)
            text(c, 'reanalysis', 1040, 540, 44, 400, 'ink', kr, kind='italic')
            text(c, 'a physics-built record of past weather (e.g. ERA5)', 1040, 590, 20, 500, 'muted', kr, kind='mono')
            text(c, 'most AI weather models learn from it, and its biases', 1040, 630, 20, 500, 'muted', kr, kind='mono')
            stamp(c, 'not used', 1520, 735, 'c', kr, ramp(t, 7.6, 0.5, e_back), rot=-8, size=32)
        kf = ramp(t, 14.5, 0.9, e_expo) * window(t, 14.5, 21.2, d_out=0.5)
        if kf > 0:
            figcard(c, 'fig1', 310, 330, 1300, kf, 'Fig. 1: one latent state, decoded as every instrument', k=kf)
        kt = ramp(t, 21.5, 0.8)
        if kt > 0:
            rows = [('earlier models, observations in', 'one pass over a fixed window', 'muted', False),
                    ('WeatherDreamer', 'a running memory, corrected every hour', 'y', True)]
            for q, (lab, sub, colr, rec) in enumerate(rows):
                y = 470 + q * 220
                k = ramp(t, 21.5 + q * 0.8, 0.7)
                text(c, lab, MX, y - 40, 30, 600, 'ink', k)
                text(c, sub, MX, y - 6, 22, 500, colr, k, kind='mono')
                x0, x1 = MX + 600, W - MX
                line(c, x0, y - 14, x1, y - 14, 'faint', k, 2)
                for hh in range(13):
                    xx = x0 + (x1 - x0) * hh / 12
                    circle(c, xx, y - 14, 5, fill=OBS, a=k * 0.8)
                if not rec:
                    rrect(c, x0 - 10, y - 50, (x1 - x0) * 0.75, 72, 14, stroke='muted', sw=2.4, a=k)
                    arrow(c, x0 + (x1 - x0) * 0.75, y - 14, x1 + 10, y - 14, 'muted', k, 2.4, 12)
                else:
                    pr = ramp(t, 22.3, 2.5, e_io)
                    for hh in range(12):
                        if hh / 12 < pr:
                            curved(c, (x0 + (x1 - x0) * hh / 12, y - 30), (x0 + (x1 - x0) * (hh + 1) / 12, y - 30), 0.4, 'y', k, 1, w=2.2, head=8)
            text(c, 'keeping the loop is the new part', W / 2, 920, 30, 400, 'y', kt, 'center', kind='italic')
            tag(c, ILLUS + '  ·  §1', W - MX, 330, kt, 'right')

# ======================================================================= THREE LESSONS
class Lessons(Scene):
    """The three losses (§3.7, Eq. 15-18): reconstruction with masking (weights 1 / 2 / 3), prior matching, a CRPS
    rollout of 6-12 h with an ensemble. Cards: illustration."""
    dur = 28.0
    chapter = 2
    cues = [(0.2, 'whoosh'), (0.8, 'pop'), (8.5, 'pop'), (16.5, 'pop')]

    def draw(self, c, t):
        hdr(self, c, t, '03', 'how it is taught', 'Three *lessons*')
        cw, gap, y0, ch = 532, 42, 340, 560
        for i, (ti, lab, colr) in enumerate([(0.8, 'rebuild what was seen', OBS), (8.5, 'anticipate the next hour', BG),
                                            (16.5, 'run alone, as an ensemble', AN)]):
            k = ramp(t, ti, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch)
                    line(c, x + 36, y0 + 1, x + 156, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, f'{i + 1}', x + 36, y0 + 80, 54, 300, colr, 1, kind='italic')
                    text(c, lab, x + 90, y0 + 72, 27, 600, 'ink', 1)
                    cx, cy = x + cw / 2, y0 + 270
                    if i == 0:
                        rng = np.random.default_rng(3)
                        for r in range(4):
                            for q in range(6):
                                hidden = (q == 2) or (r == 1 and q in (4, 5))
                                rrect(c, cx - 200 + q * 68, cy - 120 + r * 62, 58, 52, 6,
                                      fill='faint' if hidden else OBS, fa=0.5 if hidden else 0.35 + 0.5 * rng.random())
                                if hidden:
                                    text(c, '?', cx - 171 + q * 68, cy - 82 + r * 62, 26, 600, 'ink', 0.8, 'center')
                        text(c, 'whole instruments and blocks hidden', x + 36, y0 + 470, 20, 500, 'muted', 1, kind='mono')
                        text(c, 'guessing them counts 2-3× more', x + 36, y0 + 504, 20, 500, OBS, 1, kind='mono')
                    elif i == 1:
                        tex(c, 'lprior', cx, cy - 40, 34, ramp(t, ti + 0.5, 0.8))
                        text(c, 'the guess before the hour', cx, cy + 50, 22, 500, BG, 1, 'center', kind='mono')
                        text(c, '= the picture after it', cx, cy + 84, 22, 500, AN, 1, 'center', kind='mono')
                        text(c, 'the only way: anticipate', x + 36, y0 + 470, 20, 500, 'muted', 1, kind='mono')
                        text(c, 'the observations', x + 36, y0 + 504, 20, 500, 'muted', 1, kind='mono')
                    else:
                        rng = np.random.default_rng(8)
                        pr = ramp(t, ti + 0.4, 2.0, e_io)
                        for m in range(7):
                            ys = np.cumsum(rng.normal(0, 9, 24)) * np.linspace(0.2, 1.2, 24)
                            pts = np.stack([cx - 210 + np.arange(24) * 18, cy + ys], 1)
                            draw_poly(c, pts, AN, 0.7, 2.2, prog=pr)
                        circle(c, cx - 210, cy, 8, fill=AN, a=1)
                        text(c, '6, then 12 hours, no observations', x + 36, y0 + 470, 20, 500, 'muted', 1, kind='mono')
                        text(c, 'scored on the spread (CRPS)', x + 36, y0 + 504, 20, 500, AN, 1, kind='mono')
        src(c, '§3.7, Eq. 15-18', MX, 960, ramp(t, 1.0, 0.8))
        tag(c, 'pictures: ' + ILLUS, W - MX, 960, ramp(t, 1.0, 0.8), 'right')
