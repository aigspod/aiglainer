"""loopkit: drawing pieces for the WeatherDreamer topic (Duffy, Penn, Ballard, Posch & Vandal, arXiv:2611.18393v1).
Hosted by projects/weatherdreamer/videos/loop; other pieces can list SOURCES = ['weatherdreamer/videos/loop'] and
`from loopkit import *`.

Figures (the paper's figures are raster images: show crops, never redraw)
  fig(name), figcard(c, name, x, y, w=None, a, label='Fig. 4', h=None, src=(x0, y0, x1, y1))
                                  data/figs/<name>.png from projects/weatherdreamer/extract_paper.py (not in git)
Labels (house rule: every chart or drawing carries one)
  tag(c, ILLUS | OURS | 'text', x, y, a, align)   lowercase mono; OURS ('our arithmetic') is amber
  src(c, 'Table 2', x, y, a, align)                'data: Table 2 · arXiv:2611.18393'
  hdr(scene, c, t, num, kick, title, sub)          section header
The globe (an illustration: no coastlines, computed observing patterns)
  Globe(cx, cy, r, lon0, lat0).proj(lon, lat) -> (x, y, front), .draw(c, a), .dots(c, pts, color, r, a),
  .track(c, lons, lats, color, w, a, prog), .disk(c, lon, radius_deg, color, a)
  STATIONS, BALLOONS (seeded, clustered on rough continent centres), polar_track(i, n), GEO_LONS
Diagrams
  node(c, x, y, w, h, title, colr, a, sub), curved(c, p0, p1, bend, colr, a, prog), hbar(...), icons: station,
  balloon, satellite; stamp(...).
Scenes: TitleCard, EndCard, question_cards (same contract as other topics' kits).
Every helper animates from (t, t0) so narrated time-warps work.
"""
import functools, math, os
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
from aiglainer.notes import lamp, sticky, swash, hand_arrow

HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.normpath(os.path.join(HERE, '..', '..', 'data', 'figs'))

PAPER_TITLE = 'WeatherDreamer: Learning a World Model from Multimodal Earth Observations'
AUTHORS = 'Kate Duffy  ·  Elise Penn  ·  Tristan Ballard  ·  August Posch  ·  Thomas J. Vandal'
AFFIL = 'zeus ai, inc.  ·  arxiv:2611.18393  ·  november 2026'
CITE = 'Duffy, Penn, Ballard, Posch & Vandal.  WeatherDreamer.  arXiv:2611.18393v1, 2026.'
ARXIV = 'arxiv.org/abs/2611.18393'
PAPER = 'Duffy et al. 2026'
CARD = '#f6f1e7'

ILLUS, OURS = 'illustration', 'our arithmetic'
# system colours follow the paper's Fig. 4: WeatherDreamer blue, NOAA's GEFS orange (coral), ECMWF's IFS ENS green;
# GSI lilac. Observations are also blue in the loop diagrams, which never share a frame with result charts.
WD, GEFS, IFS, GSI = 'g', 'c', 'f', 'x'
OBS, BG, AN = 'g', 'f', 'y'          # observations blue, background / prior green, analysis / posterior amber

# ---------------------------------------------------------------- figures
@functools.lru_cache(maxsize=32)
def fig(name):
    path = os.path.join(FIGS, name + '.png')
    if not os.path.exists(path):
        raise SystemExit(f'missing {path}: the figure crops are not in git. Put the paper (arXiv:2611.18393v1) at '
                         'projects/weatherdreamer/paper/paper.pdf and run `python projects/weatherdreamer/extract_paper.py`.')
    return skia.Image.open(path)

def figcard(c, name, x, y, w=None, a=1.0, label=None, h=None, pad=10, k=1.0, src=None, credit=True):
    """A crop of one of the paper's figures on a light card, top-left (x, y), width w (or height h).
    src = (x0, y0, x1, y1) in 0..1 picks a sub-rectangle. Returns (w, h) of the image."""
    im = fig(name)
    sx0, sy0, sx1, sy1 = src or (0, 0, 1, 1)
    asp = (im.height() * (sy1 - sy0)) / (im.width() * (sx1 - sx0))
    if w is None:
        w = h / asp
    h = w * asp
    if a <= 0:
        return w, h
    with layer(c, a * k):
        with xform(c, 0, 0, 0.95 + 0.05 * k, 0, x + w / 2, y + h / 2):
            rrect(c, x - pad, y - pad, w + 2 * pad, h + 2 * pad, 10, fill=CARD)
            r = skia.Rect.MakeLTRB(sx0 * im.width(), sy0 * im.height(), sx1 * im.width(), sy1 * im.height())
            c.drawImageRect(im, r, skia.Rect.MakeXYWH(x, y, w, h), skia.SamplingOptions(skia.CubicResampler.Mitchell()),
                            skia.Paint(AntiAlias=True))
    if label and credit:
        note(c, f'{label} · {PAPER}', x - pad, y + h + pad + 24, a, 16, 'muted')
    return w, h

# ---------------------------------------------------------------- labels
def tag(c, s, x, y, a=1.0, align='left', size=16):
    colr = 'y' if s.startswith(OURS) or s.startswith('our ') else 'muted'
    note(c, s, x, y, a * (1.0 if colr == 'y' else 0.9), size, colr, align)

def src(c, ref, x, y, a=1.0, align='left', size=16):
    note(c, f'data: {ref}  ·  arXiv:2611.18393', x, y, a * 0.9, size, 'muted', align)

def hdr(scene, c, t, num, kick, title, sub=None, **kw):
    header(c, t, getattr(scene, 'NUM', num), kick, title, sub=sub, **kw)

def stamp(c, s, x, y, color='r', a=1.0, k=1.0, rot=-6, size=34):
    if a <= 0 or k <= 0:
        return
    w = text_width(s, size, 600, 'mono', 0.06) + 44
    h = size + 30
    sc = 1.0 + 0.6 * (1 - k)
    with xform(c, x, y, sc, rot):
        with layer(c, a * clamp(k * 1.4)):
            rrect(c, -w / 2, -h / 2, w, h, 10, fill='panel', fa=0.94)
            rrect(c, -w / 2, -h / 2, w, h, 10, fill=color, fa=0.12)
            rrect(c, -w / 2, -h / 2, w, h, 10, stroke=color, sw=3)
            text(c, s, -w / 2 + 22, size * 0.36, size, 600, color, 1, kind='mono', tracking=0.06)

# ---------------------------------------------------------------- diagrams
def node(c, x, y, w, h, title, colr='line', a=1.0, sub=None, size=28, fill='panel', glow=0, k=1.0, title_kind='sans'):
    """A rounded box with a title (and a sub-line), drawn around its top-left (x, y)."""
    if a <= 0:
        return
    with layer(c, a):
        with xform(c, 0, (1 - k) * 18):
            rrect(c, x, y, w, h, 16, fill=fill, fa=0.9)
            rrect(c, x, y, w, h, 16, stroke=colr, sw=2.4, glow=glow)
            ty = y + h / 2 + (size * 0.36 if sub is None else -6)
            text(c, title, x + w / 2, ty, size, 600 if title_kind == 'sans' else 400, 'ink', 1, 'center', kind=title_kind)
            if sub:
                text(c, sub, x + w / 2, y + h / 2 + 30, 18, 500, 'muted', 1, 'center', kind='mono')

def curved(c, p0, p1, bend, colr, a=1.0, prog=1.0, w=2.6, head=13, dash=None):
    """A quadratic arrow from p0 to p1 bowed by `bend` (fraction of the chord, + is left of travel)."""
    if a <= 0 or prog <= 0:
        return
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    ts = np.linspace(0, prog, 60)
    pts = np.stack([(1 - ts) ** 2 * x0 + 2 * (1 - ts) * ts * cx + ts ** 2 * x1,
                    (1 - ts) ** 2 * y0 + 2 * (1 - ts) * ts * cy + ts ** 2 * y1], 1)
    draw_poly(c, pts, colr, a, w, dash=dash)
    if prog > 0.97:
        ex, ey = pts[-1]
        px, py = pts[-4]
        ang = math.atan2(ey - py, ex - px)
        for s in (-1, 1):
            line(c, ex, ey, ex - head * math.cos(ang + s * 0.45), ey - head * math.sin(ang + s * 0.45), colr, a, w)

def hbar(c, x, y, w_max, vmax, v, label, colr, a=1.0, prog=1.0, h=34, fmt='{:.2f}', fs=22, lab_w=330, lo=None):
    """One horizontal bar (value v of vmax) with a label on the left and the value at its end. lo draws a range bar."""
    if a <= 0:
        return
    text(c, label, x + lab_w - 18, y + h * 0.68, fs, 500, 'ink', a, 'right')
    if lo is None:
        bw = w_max * v / vmax * prog
        rrect(c, x + lab_w, y, max(bw, 2), h, 6, fill=colr, fa=a * 0.85)
        text(c, fmt.format(v), x + lab_w + bw + 12, y + h * 0.7, fs, 600, colr, a * clamp(prog * 2 - 1), kind='mono')
    else:
        x0 = x + lab_w + w_max * lo / vmax
        x1 = x0 + (w_max * (v - lo) / vmax) * prog
        rrect(c, x0, y + h * 0.15, max(x1 - x0, 3), h * 0.7, h * 0.35, fill=colr, fa=a * 0.85)
        text(c, fmt.format(lo) + '–' + fmt.format(v), x1 + 12, y + h * 0.7, fs, 600, colr, a * clamp(prog * 2 - 1), kind='mono')

def station_icon(c, x, y, s=1.0, a=1.0, color='ink'):
    """A little weather mast with a wind cup."""
    if a <= 0:
        return
    with xform(c, x, y, s):
        line(c, 0, 0, 0, -60, color, a, 3)
        line(c, -18, 0, 18, 0, color, a, 3)
        line(c, 0, -52, 22, -52, color, a, 2.4)
        circle(c, 26, -52, 6, stroke=color, sw=2.2, a=a)
        rrect(c, -10, -34, 20, 16, 3, stroke=color, sw=2.2, a=a)

def balloon_icon(c, x, y, s=1.0, a=1.0, color='ink', rise=0.0):
    if a <= 0:
        return
    with xform(c, x, y - rise, s):
        circle(c, 0, -40, 22, fill=color, a=a * 0.25)
        circle(c, 0, -40, 22, stroke=color, sw=2.4, a=a)
        line(c, 0, -18, 0, 20, color, a * 0.8, 1.6)
        rrect(c, -6, 20, 12, 10, 2, fill=color, a=a)

def satellite_icon(c, x, y, s=1.0, a=1.0, color='ink', beam=0.0, beam_len=220):
    if a <= 0:
        return
    with xform(c, x, y, s):
        if beam > 0:
            pth = skia.Path()
            pth.moveTo(-6, 14); pth.lineTo(6, 14); pth.lineTo(46, beam_len); pth.lineTo(-46, beam_len); pth.close()
            c.drawPath(pth, paint('g', a * 0.22 * beam))
        rrect(c, -16, -12, 32, 26, 4, fill='panel2', stroke=color, sw=2.2, a=a)
        for sx in (-1, 1):
            rrect(c, sx * 22 - (34 if sx < 0 else 0), -8, 34, 18, 2, fill='g', fa=a * 0.35)
            rrect(c, sx * 22 - (34 if sx < 0 else 0), -8, 34, 18, 2, stroke=color, sw=1.6, a=a)

# ---------------------------------------------------------------- the globe (illustration)
class Globe:
    """Orthographic globe centred on (lon0, lat0) degrees. No coastlines: it is a stage for observing patterns."""
    def __init__(self, cx, cy, r, lon0=-40.0, lat0=20.0):
        self.cx, self.cy, self.r, self.lon0, self.lat0 = cx, cy, r, lon0, lat0

    def proj(self, lon, lat):
        lon, lat = np.radians(np.asarray(lon, float)), np.radians(np.asarray(lat, float))
        l0, p0 = math.radians(self.lon0), math.radians(self.lat0)
        x = np.cos(lat) * np.sin(lon - l0)
        y = math.cos(p0) * np.sin(lat) - math.sin(p0) * np.cos(lat) * np.cos(lon - l0)
        z = math.sin(p0) * np.sin(lat) + math.cos(p0) * np.cos(lat) * np.cos(lon - l0)
        return self.cx + self.r * x, self.cy - self.r * y, z

    def draw(self, c, a=1.0, grid=True):
        if a <= 0:
            return
        p = skia.Paint(AntiAlias=True)
        p.setShader(skia.GradientShader.MakeRadial((self.cx - self.r * 0.35, self.cy - self.r * 0.4), self.r * 1.5,
                                                   [col('#2a3352', a), col('#141827', a), col('#0c0e18', a)], [0, 0.6, 1]))
        c.drawCircle(self.cx, self.cy, self.r, p)
        if grid:
            for lat in range(-60, 61, 30):
                lons = np.linspace(-180, 180, 181)
                self._curve(c, lons, np.full_like(lons, lat), 'line', a * 0.9, 1.2)
            for lon in range(-180, 180, 30):
                lats = np.linspace(-90, 90, 91)
                self._curve(c, np.full_like(lats, lon), lats, 'line', a * 0.9, 1.2)
        circle(c, self.cx, self.cy, self.r, stroke='faint', sw=2, a=a)
        c.drawCircle(self.cx, self.cy, self.r * 1.04, paint('g', a * 0.10, stroke=6, blur=10))

    def _curve(self, c, lons, lats, color, a, w, prog=1.0):
        X, Y, Z = self.proj(lons, lats)
        n = max(2, int(len(X) * prog))
        seg = []
        for i in range(n):
            if Z[i] > 0:
                seg.append((X[i], Y[i]))
            elif seg:
                if len(seg) > 1:
                    draw_poly(c, np.array(seg), color, a, w)
                seg = []
        if len(seg) > 1:
            draw_poly(c, np.array(seg), color, a, w)

    def track(self, c, lons, lats, color='g', w=3, a=1.0, prog=1.0):
        if a > 0:
            self._curve(c, lons, lats, color, a, w, prog)

    def dots(self, c, pts, color='ink', r=3.2, a=1.0, prog=1.0, glow=0):
        if a <= 0 or prog <= 0:
            return
        n = int(len(pts) * prog)
        X, Y, Z = self.proj(pts[:n, 0], pts[:n, 1])
        pnt = paint(color, a)
        for x, y, z in zip(X, Y, Z):
            if z > 0.02:
                c.drawCircle(x, y, r * (0.55 + 0.45 * z), pnt)

    def disk(self, c, lon, radius=70.0, color='g', a=1.0, lat=0.0, fill=0.10):
        """The footprint of a geostationary satellite: a small circle of `radius` degrees about (lon, lat)."""
        if a <= 0:
            return
        th = np.linspace(0, 2 * np.pi, 181)
        la0, lo0, d = math.radians(lat), math.radians(lon), math.radians(radius)
        la = np.arcsin(np.sin(la0) * np.cos(d) + np.cos(la0) * np.sin(d) * np.cos(th))
        lo = lo0 + np.arctan2(np.sin(th) * np.sin(d) * np.cos(la0), np.cos(d) - np.sin(la0) * np.sin(la))
        self._curve(c, np.degrees(lo), np.degrees(la), color, a, 2.4)

def _clusters(n, centres, seed):
    rng = np.random.default_rng(seed)
    w = np.array([cw for *_, cw in centres], float)
    idx = rng.choice(len(centres), n, p=w / w.sum())
    out = []
    for i in idx:
        lo, la, slo, sla, _ = centres[i]
        out.append((lo + rng.normal() * slo, np.clip(la + rng.normal() * sla, -80, 80)))
    return np.array(out)

# rough continent centres (lon, lat, spread lon, spread lat, weight): stations are dense on northern land
LAND = [(-98, 40, 14, 8, 6), (-75, 43, 6, 4, 2), (10, 49, 10, 6, 6), (40, 55, 16, 6, 3), (95, 47, 22, 9, 4),
        (113, 31, 8, 7, 4), (78, 22, 6, 6, 2), (138, 36, 3, 3, 1.5), (-55, -18, 10, 12, 2), (22, 2, 14, 14, 1.5),
        (135, -27, 12, 7, 1.2), (-150, 61, 10, 4, 0.6), (45, 30, 10, 6, 1.2)]
STATIONS = _clusters(1600, LAND, 7)
BALLOONS = np.vstack([_clusters(70, LAND, 21), np.random.default_rng(5).uniform([-180, -60], [180, 60], (22, 2))])
GEO_LONS = [-75.2, -137.0, 0.0, 128.2]          # GOES-East, GOES-West, Meteosat 0°, GK2A (sub-satellite longitudes)

def polar_track(i, n=360, inc=98.7, lon_start=0.0, shift=-25.3):
    """Ground track of a sun-synchronous polar orbit (inclination ~98.7°), pass i shifted west by Earth's rotation
    (~25° per ~101-minute orbit). Returns (lons, lats) for one ascending + descending pass."""
    u = np.linspace(-np.pi, np.pi, n)
    ir = math.radians(inc)
    lat = np.degrees(np.arcsin(np.sin(ir) * np.sin(u)))
    lon = np.degrees(np.arctan2(np.cos(ir) * np.sin(u), np.cos(u))) + lon_start + i * shift
    lon = (lon + 180) % 360 - 180
    return lon, lat

# ---------------------------------------------------------------- cards
def question_cards(c, t, qs, y0=300, dy=176, h=148, size=33):
    for i, (q, ti) in enumerate(qs):
        k = ramp(t, ti, 0.9, e_expo)
        if k <= 0:
            continue
        yy = y0 + i * dy
        with layer(c, k):
            with xform(c, 0, (1 - k) * 30):
                panel(c, MX, yy, W - 2 * MX, h)
                line(c, MX + 36, yy + 1, MX + 156, yy + 1, 'y', 1, 4, cap='butt')
                text(c, f'{i + 1}', MX + 50, yy + h * 0.66, 64, 300, 'y', 1, kind='italic')
                rich(c, q, MX + 140, yy + h * 0.45, size, W - 2 * MX - 200, t, ti + 0.3, 0.025, 0.45)

class TitleCard(Scene):
    """Title over a slowly turning globe of observing patterns (illustration)."""
    dur = 10.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]
    TITLE = 'Weather*Dreamer*'
    SUBTITLE = 'Learning a World Model from Multimodal Earth Observations'
    KICKER = 'an explainer of arXiv:2611.18393'

    def draw(self, c, t):
        g = Globe(1450, 560, 330, -60 + 4 * t, 18)
        ka = 0.75 * ramp(t, 0.0, 1.2)
        g.draw(c, ka)
        g.dots(c, STATIONS, 'ink', 2.4, ka * 0.55)
        for lon in GEO_LONS:
            g.disk(c, lon, 72, 'g', ka * 0.45)
        for i in range(6):
            lo, la = polar_track(i, lon_start=-40)
            g.track(c, lo, la, 'g', 5, ka * 0.25)
        x0 = MX + 40
        kicker(c, self.KICKER, x0, 330, ramp(t, 0.2, 0.8), 'muted', 18)
        k = ramp(t, 0.1, 1.0, e_expo)
        size = 128
        with layer(c, k):
            xx, yy = x0, 500 + (1 - k) * 40
            for i, part in enumerate(self.TITLE.split('*')):
                if not part:
                    continue
                if i % 2:
                    wd = text(c, part, xx, yy, size, 400, 'y', 1, kind='italic')
                    swash(c, xx - 4, xx + wd + 6, yy + size * 0.22, 'y', 1, ramp(t, 0.8, 0.9, e_io), w=4)
                else:
                    wd = text(c, part, xx, yy, size, 700, 'ink', 1, tracking=-0.01)
                xx += wd
        text(c, 'Learning a World Model from', x0, 600, 36, 400, 'ink', ramp(t, 1.2, 0.7), kind='italic')
        text(c, 'Multimodal Earth Observations', x0, 648, 36, 400, 'ink', ramp(t, 1.3, 0.7), kind='italic')
        text(c, AUTHORS, x0, 740, 23, 500, 'ink', ramp(t, 2.0, 0.8))
        kicker(c, AFFIL, x0, 790, ramp(t, 2.6, 0.8), 'muted', 17)
        tag(c, ILLUS, 1450, 935, ramp(t, 1.5, 0.8), 'center')

class EndCard(Scene):
    """Takeaway + citation. Subclasses set TAKE (rich), STATS [(big, small, colour)]."""
    dur = 14.0
    fade_out = 1.6
    cues = [(0.2, 'chime'), (12.5, 'outro')]
    TAKE, STATS, NEXT = '', [], 'an unofficial explainer, not made by the authors'

    def draw(self, c, t):
        kicker(c, 'the takeaway', W / 2, 210, ramp(t, 0.3, 1.0, e_expo), 'y', 20, align='center')
        rich(c, self.TAKE, W / 2, 290, 46, 1560, t, 0.6, 0.05, 0.6, 1, 'center', base_w=600, lh=1.25)
        n = max(1, len(self.STATS))
        step = min(560, (W - 2 * MX - 80) / n)
        for i, (big, small, colr) in enumerate(self.STATS):
            k = ramp(t, 2.5 + i * 0.35, 0.8, e_expo)
            stat(c, MX + 40 + i * step, 560, big, small, colr, k, 60)
        k2 = ramp(t, 4.0, 0.9)
        with layer(c, k2):
            line(c, MX, 690, W - MX, 690, 'line', 1, 1.5)
            text(c, CITE, MX, 745, 24, 600, 'ink')
            text(c, ARXIV, MX, 790, 22, 500, 'g', 1, kind='mono')
            if self.NEXT:
                kicker(c, self.NEXT, MX, 850, 1, 'muted', 17)
