"""Episode art for the aigs pod feed (1400 x 1400 PNG, Apple's minimum): an epiplexity-style cover instead of the
journal-club felt robot, since this episode is an extra. One field of cells: outside the lens it is rule 30 (looks
like noise), inside the lens rule 54 (structure). Both computed from their rules.

    pixi run python projects/epiplexity/pods/episode/cover.py [out.png]
"""
import os, sys
COVER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(COVER_DIR, '..', '..', 'videos', 'epiplexity'))
from epikit import *          # noqa: E402  (aiglainer.core/kit helpers, eca, draw_eca)

S = 1400

def cover():
    surf = skia.Surface(S, S)
    c = surf.getCanvas()
    # ground: the videos' navy, lifted in the middle
    c.clear(col('bg0'))
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((S / 2, S * 0.47), S * 0.62, [col('bg1'), col('bg0')]))
    c.drawRect(skia.Rect.MakeWH(S, S), p)

    # the field: rule 30 everywhere, faded out at its edges
    fx, fy, fw, cols_ = 60, 300, 1280, 110
    cpx = fw / cols_
    rows = int(700 / cpx)
    g30 = eca(30, cols_, rows, seed=4)
    g54 = eca(54, cols_, rows, seed=11)
    fh = rows * cpx
    c.saveLayer(None, None)
    draw_eca(c, g30, fx, fy, fw, color='g', a=0.8, bg_a=0.05, frame=False, gap=0.22)
    m = skia.Paint(); m.setBlendMode(skia.BlendMode.kDstIn)
    m.setShader(skia.GradientShader.MakeRadial((S / 2, fy + fh / 2), fw * 0.56,
                                               [skia.Color(0, 0, 0, 255), skia.Color(0, 0, 0, 255), skia.Color(0, 0, 0, 0)],
                                               [0.0, 0.55, 1.0]))
    c.drawRect(skia.Rect.MakeWH(S, S), m)
    c.restore()

    # the lens: inside it the same grid shows rule 54
    lx, ly, r = 640, fy + fh / 2 - 10, 250
    c.save()
    path = skia.Path(); path.addCircle(lx, ly, r)
    c.clipPath(path, skia.ClipOp.kIntersect, True)
    bgp = skia.Paint(AntiAlias=True); bgp.setColor(col('bg0', 0.92))
    c.drawCircle(lx, ly, r, bgp)
    draw_eca(c, g54, fx, fy, fw, color='y', a=1.0, bg_a=0.06, frame=False, gap=0.22, glow=5)
    c.restore()
    # handle, then the brass rim on top
    hp = skia.Paint(AntiAlias=True, StrokeWidth=34, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
    hp.setColor(col('#6b4a26'))
    a0 = 0.785
    c.drawLine(lx + (r + 18) * math.cos(a0), ly + (r + 18) * math.sin(a0),
               lx + (r + 210) * math.cos(a0), ly + (r + 210) * math.sin(a0), hp)
    glow = skia.Paint(AntiAlias=True, StrokeWidth=26, Style=skia.Paint.kStroke_Style)
    glow.setColor(col('y', 0.35)); glow.setImageFilter(skia.ImageFilters.Blur(14, 14))
    c.drawCircle(lx, ly, r + 6, glow)
    rim = skia.Paint(AntiAlias=True, StrokeWidth=16, Style=skia.Paint.kStroke_Style)
    rim.setColor(col('y'))
    c.drawCircle(lx, ly, r + 6, rim)
    rim2 = skia.Paint(AntiAlias=True, StrokeWidth=3, Style=skia.Paint.kStroke_Style)
    rim2.setColor(col('#fff1d6', 0.55))
    c.drawCircle(lx, ly, r - 2, rim2)

    # lettering: the series' top lines, then this episode's question
    text(c, 'THE AIGS POD', S / 2, 150, 66, 400, 'ink', align='center', tracking=0.42)
    text(c, 'EP 29', S / 2, 228, 40, 400, 'ink', 0.9, align='center', tracking=0.42)
    w1 = text_width('Random ', 128, 1000, 'display')
    w2 = text_width('to whom?', 120, 1100, 'italic')
    x0 = (S - w1 - w2) / 2
    text(c, 'Random ', x0, 1196, 128, 1000, 'ink', kind='display')
    text(c, 'to whom?', x0 + w1, 1196, 120, 1100, 'y', kind='italic')
    swash(c, x0 + w1 + 6, x0 + w1 + w2, 1236, 'y', 1, 1, w=7)
    text(c, 'epiplexity  ·  an aigs pod extra', S / 2, 1318, 34, 500, 'muted', align='center', kind='mono')
    return surf.makeImageSnapshot()

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(COVER_DIR, 'out', 'cover.png')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cover().save(out, skia.kPNG)
    print(out)
