"""Tiny motion-graphics engine on top of skia-python."""
import os, json, math, functools, re
import numpy as np
import skia
from . import project

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1920, 1080
FPS = 60

# ---------------------------------------------------------------- palette
def hexrgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

# The aigspod site's dark ("study at night") tokens, plus data colours that follow the paper's figures
# (g blue, f green, C coral-orange, complement grey), kept distinct from the amber accent.
PAL = dict(
    bg0='#11121c', bg1='#1e1f30', ink='#efe5d6', muted='#aaa0ad', faint='#3d3c55', line='#2e2f45',
    f='#45c99a', g='#5aa6ec', c='#f07a4f', v='#a9a3b8', y='#e3a75a', x='#c3a6d8', r='#e0607a',
    panel='#1b1c2b', panel2='#25263a', pencil='#b9c2d3', sticky='#c9b53f', sticky_ink='#231d05',
)

def col(name_or_hex, a=1.0):
    h = PAL.get(name_or_hex, name_or_hex)
    r, g, b = hexrgb(h)
    return skia.Color(r, g, b, int(max(0, min(1, a)) * 255))

def mix(c1, c2, t):
    a, b = hexrgb(PAL.get(c1, c1)), hexrgb(PAL.get(c2, c2))
    t = max(0.0, min(1.0, t))
    return '#%02X%02X%02X' % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

# ---------------------------------------------------------------- easing / timing
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x

def lerp(a, b, t):
    return a + (b - a) * t

def e_lin(t): return t
def e_out(t): return 1 - (1 - t) ** 3
def e_in(t): return t ** 3
def e_io(t): return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2
def e_expo(t): return 1 if t >= 1 else 1 - 2 ** (-10 * t)
def e_io_expo(t):
    if t <= 0: return 0
    if t >= 1: return 1
    return 2 ** (20 * t - 10) / 2 if t < .5 else (2 - 2 ** (-20 * t + 10)) / 2
def e_back(t, s=1.70158):
    t -= 1
    return t * t * ((s + 1) * t + s) + 1
def e_smooth(t): return t * t * (3 - 2 * t)

def ramp(t, t0, dur, ease=e_out):
    if dur <= 0:
        return 1.0 if t >= t0 else 0.0
    return ease(clamp((t - t0) / dur))

def window(t, t_in, t_out, d_in=0.6, d_out=0.5, ease=e_out):
    """1 while visible between t_in and t_out (with fades)."""
    a = ramp(t, t_in, d_in, ease)
    if t_out is not None:
        a *= 1 - ramp(t, t_out, d_out, e_io)
    return a

# ---------------------------------------------------------------- fonts
# The aigspod site's type: Fraunces (display), Inter (text), Space Mono (labels), Caveat (handwriting).
# Glyphs a face lacks (Greek, arrows, ticks) fall back to Inter, then SF Pro, per character.
FONT_DIR = os.path.join(HERE, 'fonts')
SFNS = '/System/Library/Fonts/SFNS.ttf'
SFNS_I = '/System/Library/Fonts/SFNSItalic.ttf'
_VP = skia.FontArguments.VariationPosition
_AX = dict(wght=0x77676874, opsz=0x6f70737a, SOFT=0x534f4654, WONK=0x574f4e4b)
_tf_cache = {}
_keep = []   # skia only borrows variation coordinates; keep them alive or weights silently reset

def _var(path, **axes):
    key = (path, tuple(sorted(axes.items())))
    if key not in _tf_cache:
        base = skia.Typeface.MakeFromFile(path)
        coords = [_VP.Coordinate(_AX[k], float(v)) for k, v in axes.items()]
        cobj = _VP.Coordinates(coords)
        vp = _VP(cobj)
        arg = skia.FontArguments()
        arg.setVariationDesignPosition(vp)
        _tf_cache[key] = base.makeClone(arg)
        _keep.append((base, coords, cobj, vp, arg))
    return _tf_cache[key]

def typeface(weight=400, kind='sans', size=30):
    if kind == 'display':      # headings: light Fraunces, the site's h1/h2
        return _var(os.path.join(FONT_DIR, 'Fraunces.ttf'), wght=clamp(300 + (weight - 400) * 0.25, 300, 480), opsz=clamp(size, 9, 144), SOFT=0, WONK=0)
    if kind == 'italic':       # math-ish labels and emphasised display words
        return _var(os.path.join(FONT_DIR, 'Fraunces-Italic.ttf'), wght=clamp(320 + (weight - 400) * 0.3, 300, 520), opsz=clamp(size, 9, 144), SOFT=50, WONK=1)
    if kind == 'mono':
        return _var(os.path.join(FONT_DIR, 'SpaceMono-Bold.ttf' if weight >= 650 else 'SpaceMono-Regular.ttf'))
    if kind == 'hand':
        return _var(os.path.join(FONT_DIR, 'Caveat.ttf'), wght=clamp(weight, 400, 700))
    if kind == 'sf':
        return _var(SFNS, wght=weight, opsz=clamp(size, 17, 96))
    if kind == 'sf-italic':
        return _var(SFNS_I, wght=weight, opsz=clamp(size, 17, 96))
    return _var(os.path.join(FONT_DIR, 'Inter.ttf'), wght=clamp(weight, 100, 900), opsz=clamp(size, 14, 32))

def _resolve(size, weight, kind):
    # big bold sans is a heading: set it in the display face
    if kind == 'sans' and weight >= 650 and size >= 44:
        return 'display'
    return kind

@functools.lru_cache(maxsize=1024)
def font(size, weight=400, kind='sans'):
    kind = _resolve(size, weight, kind)
    f = skia.Font(typeface(weight, kind, size), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setHinting(skia.FontHinting.kNone)
    return f

_FALLBACK = dict(italic=('sf-italic',), display=('sans', 'sf'), mono=('sans', 'sf'), hand=('sans', 'sf'), sans=('sf',))

@functools.lru_cache(maxsize=8192)
def runs(s, size, weight=400, kind='sans'):
    """Split s into (substring, font) runs so every character is drawn by a face that has it."""
    chain = [font(size, weight, kind)] + [font(size, min(weight, 600), k) for k in _FALLBACK.get(_resolve(size, weight, kind), ('sf',))]
    out = []
    for ch in s:
        f = next((f for f in chain if ch.isspace() or f.textToGlyphs(ch)[0]), chain[-1])
        if out and out[-1][1] is f:
            out[-1][0] += ch
        else:
            out.append([ch, f])
    return tuple((t, f) for t, f in out)

def text_width(s, size, weight=400, kind='sans', tracking=0.0):
    w = sum(f.measureText(t) for t, f in runs(s, size, weight, kind))
    return w + tracking * size * max(0, len(s) - 1)

def paint(color='ink', a=1.0, stroke=None, cap='round', aa=True, blur=None, shader=None, effect=None):
    p = skia.Paint(AntiAlias=aa)
    p.setColor(col(color, a) if isinstance(color, str) else color)
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(dict(round=skia.Paint.kRound_Cap, butt=skia.Paint.kButt_Cap, square=skia.Paint.kSquare_Cap)[cap])
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if shader is not None:
        p.setShader(shader)
    if effect is not None:
        p.setPathEffect(effect)
    return p

def text(c, s, x, y, size=36, weight=400, color='ink', a=1.0, align='left', kind='sans', tracking=0.0, glow=0):
    """Draw single-line text. y is the baseline. tracking is in em units."""
    if a <= 0.003 or not s:
        return 0
    w = text_width(s, size, weight, kind, tracking)
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    rs = runs(s, size, weight, kind)
    if glow:
        _text_raw(c, rs, x, y, paint(color, a * 0.55, blur=glow), tracking, size)
    _text_raw(c, rs, x, y, paint(color, a), tracking, size)
    return w

def _text_raw(c, rs, x, y, p, tracking, size):
    for t, f in rs:
        if tracking == 0:
            c.drawString(t, x, y, f, p)
            x += f.measureText(t)
            continue
        widths = f.getWidths(f.textToGlyphs(t))
        xs = []
        for wd in widths:
            xs.append(x)
            x += wd + tracking * size
        c.drawTextBlob(skia.TextBlob.MakeFromPosTextH(t, xs, 0, f), 0, y, p)

def kicker(c, s, x, y, a=1.0, color='y', size=20, align='left'):
    """Small lowercase, letter-spaced mono label (the site's section labels)."""
    return text(c, s.lower(), x, y, size, 400, color, a, align, kind='mono', tracking=0.16)

def hand(c, s, x, y, size=34, color='pencil', a=1.0, rot=-2.5, reveal=1.0, align='left'):
    """A handwritten margin note (Caveat), slightly rotated; `reveal` writes it on left to right."""
    if a <= 0.003 or reveal <= 0:
        return
    w = text_width(s, size, 500, 'hand')
    if align == 'center':
        x -= w / 2
    elif align == 'right':
        x -= w
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    if reveal < 1:
        c.clipRect(skia.Rect.MakeXYWH(-10, -size * 1.4, (w + 20) * reveal, size * 2.2))
    text(c, s, 0, 0, size, 500, color, a, kind='hand')
    c.restore()
    return w

# ---------------------------------------------------------------- rich text
RICH_COLORS = dict(f='f', g='g', c='c', v='v', y='y', x='x', r='r', m='muted', w='ink')
_tok = re.compile(r'\{(\w+):([^}]*)\}|(\S+)|(\s+)')

def parse_rich(s, base='ink', base_w=400):
    """'{y:word word} plain' -> list of (word, color, weight, italic). '*' prefix key bold, '_' italic."""
    words = []
    for m in _tok.finditer(s):
        if m.group(1):
            key = m.group(1)
            bold = 'b' in key and key != 'b' or key == 'b'
            italic = 'i' in key
            ck = key.replace('b', '').replace('i', '') or None
            color = PAL.get(RICH_COLORS.get(ck, ''), None) if ck else None
            color = RICH_COLORS.get(ck, base) if ck else base
            for wd in m.group(2).split(' '):
                if wd:
                    words.append((wd, color, 650 if bold else base_w, italic))
        elif m.group(3):
            words.append((m.group(3), base, base_w, False))
    return words

def layout_rich(s, size, maxw, base='ink', base_w=400, lh=1.32):
    words = parse_rich(s, base, base_w)
    sp = text_width(' ', size, base_w)
    lines, cur, cw = [], [], 0
    for wd in words:
        if wd[0] == '//':
            lines.append(cur); cur, cw = [], 0
            continue
        ww = text_width(wd[0], size, wd[2], 'italic' if wd[3] else 'sans')
        glue = cur and wd[0][0] in ',.;:!?)'
        if glue:
            cw -= sp
        elif cur and cw + sp + ww > maxw:
            lines.append(cur); cur, cw = [], 0
        cur.append((wd, cw, ww))
        cw += ww + sp
    if cur:
        lines.append(cur)
    out = []
    for i, ln in enumerate(lines):
        lw = (ln[-1][1] + ln[-1][2]) if ln else 0
        for (wd, x, ww) in ln:
            out.append(dict(word=wd[0], color=wd[1], weight=wd[2], italic=wd[3], x=x, line=i, lw=lw, w=ww))
    return out, len(lines), size * lh

def rich(c, s, x, y, size=36, maxw=1400, t=1e9, t0=0.0, stagger=0.045, dur=0.55, a=1.0, align='left',
         base='ink', base_w=400, lh=1.32, rise=14):
    """Word-by-word reveal. Returns block height."""
    items, nl, lhp = layout_rich(s, size, maxw, base, base_w, lh)
    for i, it in enumerate(items):
        k = ramp(t, t0 + i * stagger, dur, e_out)
        if k <= 0:
            continue
        xx = x + it['x']
        if align == 'center':
            xx = x - it['lw'] / 2 + it['x']
        yy = y + it['line'] * lhp + (1 - k) * rise
        text(c, it['word'], xx, yy, size, it['weight'], it['color'], a * k, kind='italic' if it['italic'] else 'sans')
    return nl * lhp

def rich_count(s):
    return len(parse_rich(s))

# ---------------------------------------------------------------- latex
_TEX_PX_PER_PT = 1600 / 72.0
_tex_cache = {}

def tex_img(key):
    if key not in _tex_cache:
        _tex_cache[key] = skia.Image.open(os.path.join(project.get().tex, key + '.png'))
    return _tex_cache[key]

def tex_size(key, size):
    im = tex_img(key)
    s = size / (10 * _TEX_PX_PER_PT)
    return im.width() * s, im.height() * s

def tex(c, key, x, y, size=44, a=1.0, align='center', valign='center', reveal=1.0, glow=0):
    """size = the pixel size of 10pt text. (x,y) anchor."""
    if a <= 0.003:
        return
    im = tex_img(key)
    s = size / (10 * _TEX_PX_PER_PT)
    w, h = im.width() * s, im.height() * s
    if align == 'center': x -= w / 2
    elif align == 'right': x -= w
    if valign == 'center': y -= h / 2
    elif valign == 'bottom': y -= h
    c.save()
    if reveal < 1:
        c.clipRect(skia.Rect.MakeXYWH(x - 4, y - 10, (w + 8) * reveal, h + 20))
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(a)
    dst = skia.Rect.MakeXYWH(x, y, w, h)
    samp = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)
    if glow:
        gp = skia.Paint(AntiAlias=True)
        gp.setAlphaf(a * 0.5)
        gp.setImageFilter(skia.ImageFilters.Blur(glow, glow))
        c.drawImageRect(im, dst, samp, gp)
    c.drawImageRect(im, dst, samp, p)
    c.restore()
    return w, h

# ---------------------------------------------------------------- shapes
def rrect(c, x, y, w, h, r, fill=None, stroke=None, sw=2, a=1.0, fa=None, glow=0):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r)
    if fill is not None:
        if glow:
            c.drawRRect(rr, paint(fill, (fa if fa is not None else a) * 0.6, blur=glow))
        c.drawRRect(rr, paint(fill, fa if fa is not None else a))
    if stroke is not None:
        c.drawRRect(rr, paint(stroke, a, stroke=sw))

def line(c, x0, y0, x1, y1, color='ink', a=1.0, w=2, dash=None, cap='round', glow=0):
    eff = skia.DashPathEffect.Make(dash, 0) if dash else None
    if glow:
        c.drawLine(x0, y0, x1, y1, paint(color, a * 0.6, stroke=w * 2, blur=glow, cap=cap))
    c.drawLine(x0, y0, x1, y1, paint(color, a, stroke=w, cap=cap, effect=eff))

def circle(c, x, y, r, fill=None, stroke=None, sw=2, a=1.0, glow=0):
    if fill is not None:
        if glow:
            c.drawCircle(x, y, r * 1.6, paint(fill, a * 0.5, blur=glow))
        c.drawCircle(x, y, r, paint(fill, a))
    if stroke is not None:
        c.drawCircle(x, y, r, paint(stroke, a, stroke=sw))

def arrow(c, x0, y0, x1, y1, color='ink', a=1.0, w=2.5, head=12, prog=1.0, dash=None, glow=0):
    if a <= 0 or prog <= 0:
        return
    x1p, y1p = lerp(x0, x1, prog), lerp(y0, y1, prog)
    line(c, x0, y0, x1p, y1p, color, a, w, dash=dash, glow=glow)
    ang = math.atan2(y1p - y0, x1p - x0)
    pth = skia.Path()
    pth.moveTo(x1p, y1p)
    pth.lineTo(x1p - head * math.cos(ang - 0.42), y1p - head * math.sin(ang - 0.42))
    pth.lineTo(x1p - head * math.cos(ang + 0.42), y1p - head * math.sin(ang + 0.42))
    pth.close()
    c.drawPath(pth, paint(color, a))

def polyline_path(pts, prog=1.0):
    pth = skia.Path()
    n = len(pts)
    if n < 2 or prog <= 0:
        return pth
    # arc-length param
    seg = np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))
    L = seg.sum() * prog
    pth.moveTo(*pts[0])
    acc = 0
    for i in range(n - 1):
        if acc + seg[i] >= L:
            t = (L - acc) / seg[i] if seg[i] > 0 else 0
            pth.lineTo(*(pts[i] + (pts[i + 1] - pts[i]) * t))
            break
        pth.lineTo(*pts[i + 1])
        acc += seg[i]
    return pth

def draw_poly(c, pts, color, a=1.0, w=3, prog=1.0, dash=None, glow=0):
    pts = np.asarray(pts, float)
    pth = polyline_path(pts, prog)
    if glow:
        c.drawPath(pth, paint(color, a * 0.45, stroke=w * 2.2, blur=glow))
    eff = skia.DashPathEffect.Make(dash, 0) if dash else None
    c.drawPath(pth, paint(color, a, stroke=w, effect=eff))
    return pth

def end_point(pts, prog):
    pts = np.asarray(pts, float)
    seg = np.hypot(np.diff(pts[:, 0]), np.diff(pts[:, 1]))
    L = seg.sum() * clamp(prog)
    acc = 0
    for i in range(len(seg)):
        if acc + seg[i] >= L:
            t = (L - acc) / seg[i] if seg[i] > 0 else 0
            return pts[i] + (pts[i + 1] - pts[i]) * t
        acc += seg[i]
    return pts[-1]

class layer:
    """with layer(c, alpha): ... draws group with opacity."""
    def __init__(self, c, a=1.0, blur=0):
        self.c, self.a, self.blur = c, a, blur
    def __enter__(self):
        p = skia.Paint()
        p.setAlphaf(clamp(self.a))
        if self.blur > 0.2:
            p.setImageFilter(skia.ImageFilters.Blur(self.blur, self.blur))
        self.c.saveLayer(None, p)
        return self.c
    def __exit__(self, *a):
        self.c.restore()

class xform:
    def __init__(self, c, tx=0, ty=0, s=1.0, rot=0, cx=0, cy=0):
        self.c, self.args = c, (tx, ty, s, rot, cx, cy)
    def __enter__(self):
        tx, ty, s, rot, cx, cy = self.args
        self.c.save()
        self.c.translate(tx + cx, ty + cy)
        if rot: self.c.rotate(rot)
        if s != 1: self.c.scale(s, s)
        self.c.translate(-cx, -cy)
        return self.c
    def __exit__(self, *a):
        self.c.restore()

# ---------------------------------------------------------------- colormap (ink -> slate -> lamp amber -> paper)
def make_cmap():
    stops = [(0.0, '#0e0f19'), (0.2, '#232846'), (0.42, '#3f5f8a'), (0.62, '#8f8a8c'), (0.8, '#e0a45a'), (1.0, '#fbf1d8')]
    xs = np.array([s[0] for s in stops]); cs = np.array([hexrgb(s[1]) for s in stops], float)
    t = np.linspace(0, 1, 256)
    return np.stack([np.interp(t, xs, cs[:, i]) for i in range(3)], 1).astype(np.uint8)
CMAP = make_cmap()

def array_image(v, cmap=CMAP, vmin=0, vmax=1, alpha=255):
    """2D float array -> skia.Image via colormap."""
    idx = np.clip(((np.asarray(v) - vmin) / (vmax - vmin) * 255), 0, 255).astype(np.uint8)
    rgb = cmap[idx]
    rgba = np.concatenate([rgb, np.full(rgb.shape[:2] + (1,), alpha, np.uint8)], -1)
    return skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)

def draw_image(c, im, x, y, w, h, a=1.0, smooth=True):
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(a))
    samp = skia.SamplingOptions(skia.FilterMode.kLinear if smooth else skia.FilterMode.kNearest)
    c.drawImageRect(im, skia.Rect.MakeXYWH(x, y, w, h), samp, p)

# ---------------------------------------------------------------- data
def load_json(name):
    """Read a JSON file from the current project's data/ folder."""
    return json.load(open(os.path.join(project.get().data, name)))

if project._current is not None:
    PAL.update(project._current.THEME)
