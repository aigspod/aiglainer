"""Episode art (1400 x 1400 PNG): the videos' look, since this episode is an extra. A globe of scattered clues
(stations, weather balloons, polar-orbit stripes, geostationary footprints), an illustration computed by loopkit.

    PYTHONPATH=. .pixi/envs/default/bin/python projects/weatherdreamer/pods/episode/cover.py [out.png]
"""
import os, sys
COVER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(COVER_DIR, '..', '..', 'videos', 'loop'))
from loopkit import *          # noqa: E402

S = 1400

def cover():
    surf = skia.Surface(S, S)
    c = surf.getCanvas()
    c.clear(col('bg0'))
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((S / 2, S * 0.42), S * 0.65, [col('bg1'), col('bg0')]))
    c.drawRect(skia.Rect.MakeWH(S, S), p)
    g = Globe(S / 2, 560, 430, -62, 24)
    g.draw(c, 1)
    for lon in GEO_LONS:
        g.disk(c, lon, 72, 'g', 0.35)
    for i in range(5):
        lo, la = polar_track(i, lon_start=-30)
        g.track(c, lo, la, 'g', 24, 0.22)
        g.track(c, lo, la, 'g', 3, 0.75)
    g.dots(c, STATIONS, 'ink', 3.6, 0.85)
    g.dots(c, BALLOONS, 'f', 7.5, 1)
    w1 = text_width('The Forecaster', 108, 700)
    text(c, 'The Forecaster', S / 2, 1130, 108, 700, 'ink', 1, 'center')
    w2 = text(c, 'with no answer key', S / 2, 1250, 92, 400, 'y', 1, 'center', kind='italic')
    swash(c, S / 2 - w2 / 2, S / 2 + w2 / 2, 1278, 'y', 1, 1, w=6)
    kicker(c, 'the aigs pod  ·  episode 30', S / 2, 80, 1, 'y', 30, align='center')
    kicker(c, 'weatherdreamer  ·  an explainer', S / 2, 1340, 1, 'muted', 26, align='center')
    return surf.makeImageSnapshot()

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(COVER_DIR, 'out', 'cover.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cover().save(out, skia.kPNG)
    print(out)
