"""9:16 shorts for YouTube Shorts and TikTok: a project with KIND = 'short' builds with the usual `make P=<name>`.

narration.py is a video's (VOICE, SAY, SCENES with timed beats), and each entry also takes:
  headline='Did it learn the *physics*?'   the title at the top; one *amber italic* word
  crop=(x, y, w, h)       show that region of a 16:9 scene (from this project or a SOURCES project), enlarged;
  crop=[(v, rect), ...]   or move between regions over the scene's authored time v (a camera: pan and zoom)
  stack=[rect, rect]      or several regions at once, side by side or stacked, whichever shows them bigger
  vstart=9.5              begin partway into the scene (its authored time), skipping what came before
  id='SpecB'              when the same scene appears twice
A scene class with `vertical = True` is drawn natively instead, in a BOX-sized area (720 x 700) with its own origin.

Everything that matters stays in SAFE, a centred column: tall phones crop ~100 px off each side, the app's icons
cover the top, its buttons the right, and its handle, description and comment bar the bottom. Behind it, a blurred
copy of the visual fills the frame, so the edges aren't empty. Captions are burned in word by word, timed by Whisper
word timestamps of each clip (made by `make narration`, cached as cache/<clip>.words.json).
`make frames` writes contact sheets with everything outside SAFE shaded red: nothing that matters may be in the red.
"""
import difflib, json, os
import numpy as np
import skia
from .core import *
from .notes import swash
from .timeline import Timeline, rdur, to_visual
from . import project, tts

SW, SH = 1080, 1920
SAFE = (140, 290, 860, 1400)         # x0, y0, x1, y1: everything that matters stays inside
CX = (SAFE[0] + SAFE[2]) / 2         # horizontal centre of the safe column
HEAD_Y, HEAD_SIZE = 380, 50          # headline: first baseline, size (two lines fit above the visual)
BOX = (140, 470, 720, 700)           # x, y, w, h of the visual: crops, stacks or a native scene
CAP_Y, CAP_SIZE = 1240, 52           # captions: first baseline, size
GAP = 18                             # between stacked regions

# ---------------------------------------------------------------- word timings
def _norm(tok):
    return ''.join(tts.words(tok))

def align(script, heard):
    """Give each script word a (start, end) from Whisper's words; unmatched words are spread between neighbours."""
    toks = script.split()
    a, b = [_norm(t) for t in toks], [_norm(w['word']) for w in heard]
    times = [None] * len(toks)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            w = heard[blk.b + k]
            times[blk.a + k] = (w['start'], w['end'])
    if not any(times):
        s0, s1 = (heard[0]['start'], heard[-1]['end']) if heard else (0.4, 0.4 + 0.33 * len(toks))
        times = [None] * len(toks)
        times[0] = (s0, s0)
        times[-1] = (s1, s1)
    i = 0
    while i < len(toks):                 # fill gaps proportionally to word length
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(toks) and times[j] is None:
            j += 1
        t0 = times[i - 1][1] if i else (times[j][0] - 0.3 * (j - i) if j < len(toks) else 0.4)
        t1 = times[j][0] if j < len(toks) else t0 + 0.3 * (j - i)
        w = np.cumsum([0] + [len(toks[k]) + 1 for k in range(i, j)])
        for k in range(i, j):
            times[k] = (t0 + (t1 - t0) * w[k - i] / w[-1], t0 + (t1 - t0) * w[k - i + 1] / w[-1])
        i = j
    return [dict(w=t, s=round(s, 3), e=round(e, 3)) for t, (s, e) in zip(toks, times)]

def word_times(P, lines):
    """Whisper word timestamps for every clip, aligned to the script's own words (cached next to the clip)."""
    import mlx_whisper
    for l in lines:
        path = P.path(l['file'])[:-4] + '.words.json'
        if os.path.exists(path):
            continue
        res = mlx_whisper.transcribe(P.path(l['file']), path_or_hf_repo=tts.WHISPER, language='en', word_timestamps=True)
        heard = [w for s in res['segments'] for w in s.get('words', [])]
        json.dump(align(l['text'], heard), open(path, 'w'))
    print(f'word timings for {len(lines)} lines')

def pages(placements):
    """Caption pages: a few words at a time, broken after punctuation, each shown until the next begins."""
    out = []
    for p in placements:
        ws = json.load(open(p['file'][:-4] + '.words.json'))
        cur = []
        for k, w in enumerate(ws):
            cur.append(dict(w=w['w'], s=p['t'] + w['s'], e=p['t'] + w['e']))
            chars = sum(len(x['w']) + 1 for x in cur)
            if w['w'][-1] in ',.;:?!' or len(cur) >= 3 or chars >= 18 or k == len(ws) - 1:
                out.append(cur)
                cur = []
    for i, pg in enumerate(out):
        nxt = out[i + 1][0]['s'] if i + 1 < len(out) else pg[-1]['e'] + 0.6
        pg_end = min(nxt, pg[-1]['e'] + 0.6)
        for k, w in enumerate(pg):
            w['until'] = pg[k + 1]['s'] if k + 1 < len(pg) else pg_end
    return out

# ---------------------------------------------------------------- the visual
_cache = {}
def _surface(key, w, h):
    if key not in _cache:
        _cache[key] = skia.Surface(int(w), int(h))
    return _cache[key]

def _background():
    if 'bg' not in _cache:
        s = skia.Surface(SW, SH)
        c = s.getCanvas()
        c.clear(col('#161724'))
        p = skia.Paint()
        p.setShader(skia.GradientShader.MakeRadial((SW * 0.85, SH * 0.06), SW * 0.9, [col('y', 0.12), col('y', 0.0)], [0.0, 1.0]))
        c.drawRect(skia.Rect.MakeWH(SW, SH), p)
        _cache['bg'] = s.makeImageSnapshot()
        rng = np.random.default_rng(7)
        _cache['grain'] = []
        for _ in range(4):
            n = rng.integers(0, 255, (SH // 2, SW // 2), dtype=np.uint8)
            rgba = np.stack([n, n, n, np.full_like(n, 9)], -1)
            _cache['grain'].append(skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType))
    return _cache['bg']

def camera(crop, tv):
    """A fixed region, or one eased between keyframes [(v, rect), ...] at authored time tv."""
    if not crop or isinstance(crop[0], (int, float)):
        return crop or (0, 0, W, H)
    if tv <= crop[0][0]:
        return crop[0][1]
    for (v0, r0), (v1, r1) in zip(crop, crop[1:]):
        if tv < v1:
            d = max(1e-6, min(1.2, v1 - v0))         # hold, then move over the last (at most) 1.2 s, arriving at v1
            k = e_io(clamp((tv - (v1 - d)) / d))
            return tuple(a + (b - a) * k for a, b in zip(r0, r1))
    return crop[-1][1]

def arrange(rects, bw, bh):
    """Destination rects for regions shown together: a row or a column, whichever makes them bigger."""
    n = len(rects)
    ws, hs = [r[2] for r in rects], [r[3] for r in rects]
    s_row = min((bw - GAP * (n - 1)) / sum(ws), bh / max(hs))
    s_col = min(bw / max(ws), (bh - GAP * (n - 1)) / sum(hs))
    out = []
    if s_row >= s_col:
        s = s_row
        x = (bw - (sum(ws) * s + GAP * (n - 1))) / 2
        for w, h in zip(ws, hs):
            out.append((x, (bh - h * s) / 2, w * s, h * s)); x += w * s + GAP
    else:
        s = s_col
        y = (bh - (sum(hs) * s + GAP * (n - 1))) / 2
        for w, h in zip(ws, hs):
            out.append(((bw - w * s) / 2, y, w * s, h * s)); y += h * s + GAP
    return out

def visual(sc, e, tv):
    """The scene's visual for this moment, drawn into a BOX-sized image."""
    bw, bh = BOX[2], BOX[3]
    vs = _surface('vis', bw, bh)
    vc = vs.getCanvas()
    vc.clear(skia.ColorTRANSPARENT)
    if getattr(sc, 'vertical', False):
        sc.draw(vc, tv)
    else:
        off = _surface('off', W, H)
        oc = off.getCanvas()
        oc.clear(skia.ColorTRANSPARENT)
        sc.draw(oc, tv)
        img = off.makeImageSnapshot()
        rects = e.get('stack') or [camera(e.get('crop'), tv)]
        for src, dst in zip(rects, arrange(rects, bw, bh)):
            vc.drawImageRect(img, skia.Rect.MakeXYWH(*src), skia.Rect.MakeXYWH(*dst), skia.SamplingOptions(skia.FilterMode.kLinear))
    return vs.makeImageSnapshot()

def backdrop(c, img, a):
    """The visual, blurred and enlarged to fill the whole frame, very dim: the edges carry colour, not content."""
    small = _surface('blur', SW // 4, SH // 4)
    sc_ = small.getCanvas()
    sc_.clear(skia.ColorTRANSPARENT)
    s = max(SW / img.width(), SH / img.height()) / 4 * 1.15
    p = skia.Paint(); p.setImageFilter(skia.ImageFilters.Blur(9, 9))
    w, h = img.width() * s, img.height() * s
    sc_.drawImageRect(img, skia.Rect.MakeXYWH((SW / 4 - w) / 2, (SH / 4 - h) / 2, w, h), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    p = skia.Paint(); p.setAlphaf(0.30 * a)
    c.drawImageRect(small.makeImageSnapshot(), skia.Rect.MakeWH(SW, SH), skia.SamplingOptions(skia.FilterMode.kLinear), p)

# ---------------------------------------------------------------- type
def headline(c, s, t, a=1.0, animate=True, size=HEAD_SIZE, y=HEAD_Y):
    """Top title: display type, one *amber italic* phrase with a swash; words rise in one after another."""
    words = []
    for i, part in enumerate(s.split('*')):
        words += [(w, bool(i % 2)) for w in part.split()]
    maxw, lh = SAFE[2] - SAFE[0], size * 1.14
    sp = text_width(' ', size, 700)
    lines, cur, cw = [], [], 0
    for w, em in words:
        ww = text_width(w, size, 400 if em else 700, 'italic' if em else 'sans')
        if cur and w[0] in ',.;:!?)':               # punctuation after the amber word: no space, never on its own line
            cw -= sp
        elif cur and cw + sp + ww > maxw:
            lines.append(cur); cur, cw = [], 0
        cur.append((w, em, cw, ww)); cw += ww + sp
    lines.append(cur)
    n = 0
    for li, ln in enumerate(lines):
        yy0 = y + li * lh
        for (w, em, x, ww) in ln:
            k = ramp(t, 0.05 + n * 0.06, 0.5, e_expo) if animate else 1.0
            n += 1
            yy = yy0 + (1 - k) * 18
            if em:
                text(c, w, SAFE[0] + x, yy, size, 400, 'y', a * k, kind='italic')
                swash(c, SAFE[0] + x - 4, SAFE[0] + x + ww + 6, yy + 16, 'y', a * k, ramp(t, 0.5 + n * 0.06, 0.6, e_io) if animate else 1.0)
            else:
                text(c, w, SAFE[0] + x, yy, size, 700, 'ink', a * k, tracking=-0.005)

def captions(c, pg, T):
    """One page of burned-in captions, centred, the word being spoken in amber."""
    size, lh = CAP_SIZE, CAP_SIZE * 1.18
    maxw = SAFE[2] - SAFE[0] - 20
    sp = text_width(' ', size, 800, 'heavy')
    lines, cur, cw = [], [], 0
    for w in pg:
        ww = text_width(w['w'], size, 800, 'heavy')
        if cur and cw + sp + ww > maxw:
            lines.append((cur, cw - sp)); cur, cw = [], 0
        cur.append((w, cw, ww)); cw += ww + sp
    lines.append((cur, cw - sp))
    k = ramp(T, pg[0]['s'] - 0.05, 0.14, e_out)
    for li, (ln, lw) in enumerate(lines):
        x0 = CX - lw / 2
        for (w, x, ww) in ln:
            now = w['s'] <= T < w['until']
            text(c, w['w'], x0 + x, CAP_Y + li * lh + (1 - k) * 10, size, 800, 'y' if now else 'ink',
                 k * (1.0 if now or T >= w['s'] else 0.82), kind='heavy')

# ---------------------------------------------------------------- the frame
class ShortTimeline(Timeline):
    size = (SW, SH)

    def __init__(self, scenes, placements):
        super().__init__(scenes)
        self.placements = placements
        self.pages = pages(placements)

    def render(self, c, frame):
        T = frame / FPS
        P = project.get()
        i, t = self.locate(T)
        sc = self.scenes[i]
        e = getattr(sc, 'entry', {})
        c.drawImage(_background(), 0, 0)
        d = rdur(sc)
        a_in = 1.0 if i == 0 else ramp(t, 0, sc.fade_in, e_out)
        a = a_in * (1 - ramp(t, d - sc.fade_out, sc.fade_out, e_io)) if i < len(self.scenes) - 1 else a_in
        img = visual(sc, e, to_visual(sc, t))
        backdrop(c, img, a)
        p = skia.Paint(); p.setAlphaf(a)
        c.drawImage(img, BOX[0], BOX[1], skia.SamplingOptions(), p)
        # brand line and headline (the headline only animates when it changes)
        text(c, P.HUD, SAFE[0], SAFE[1] + 22, 19, 400, 'muted', 0.9, kind='mono', tracking=0.12)
        hl = e.get('headline', '')
        prev = getattr(self.scenes[i - 1], 'entry', {}).get('headline') if i else None
        if hl:
            same = hl == prev
            ha = 1.0 if same else a_in
            if i < len(self.scenes) - 1 and getattr(self.scenes[i + 1], 'entry', {}).get('headline') != hl:
                ha *= 1 - ramp(t, d - sc.fade_out, sc.fade_out, e_io)
            headline(c, hl, t, ha, animate=not same)
        for pg in self.pages:
            if pg[0]['s'] - 0.05 <= T < pg[-1]['until']:
                captions(c, pg, T)
                break
        if getattr(P, 'CITE', ''):
            text(c, P.CITE, CX, SAFE[3] - 22, 18, 400, 'muted', 0.85, 'center', kind='mono', tracking=0.06)
        g = _cache['grain'][(frame // 2) % 4]
        p = skia.Paint(); p.setBlendMode(skia.BlendMode.kOverlay)
        c.drawImageRect(g, skia.Rect.MakeWH(SW, SH), skia.SamplingOptions(), p)
        black = ramp(T, self.total - 0.4, 0.4, e_io)
        if black > 0:
            c.drawRect(skia.Rect.MakeWH(SW, SH), paint('#000000', black))

def make_timeline():
    from . import narrated
    scs, placements = narrated.build()
    return ShortTimeline(scs, placements)

# ---------------------------------------------------------------- QA
def qa():
    """A frame just after each line starts, everything outside SAFE shaded red -> out/narrated/qa/safe_*.png."""
    P = project.get()
    tl = make_timeline()
    od = os.path.join(P.out('narrated'), 'qa')
    os.makedirs(od, exist_ok=True)
    for f in os.listdir(od):
        os.remove(os.path.join(od, f))
    s = skia.Surface(SW, SH)
    imgs = []
    for p in tl.placements:
        cv = s.getCanvas()
        cv.clear(skia.ColorBLACK)
        tl.render(cv, int((p['t'] + min(1.0, p['dur'] * 0.5)) * FPS))
        x0, y0, x1, y1 = SAFE
        for r in ((0, 0, SW, y0), (0, y1, SW, SH - y1), (0, y0, x0, y1 - y0), (x1, y0, SW - x1, y1 - y0)):
            cv.drawRect(skia.Rect.MakeXYWH(*r), paint('#ff3030', 0.25))
        imgs.append(s.makeImageSnapshot().toarray()[::3, ::3, :3])
    cols, h, w = 4, imgs[0].shape[0], imgs[0].shape[1]
    from .preview import save_rgb
    for k in range(0, len(imgs), 8):
        chunk = imgs[k:k + 8]
        rows = (len(chunk) + cols - 1) // cols
        sheet = np.zeros((rows * h, cols * w, 3), np.uint8)
        for j, im in enumerate(chunk):
            r, cc = divmod(j, cols)
            sheet[r * h:(r + 1) * h, cc * w:(cc + 1) * w] = im
        save_rgb(sheet, os.path.join(od, f'safe_{k // 8 + 1:02d}.png'))
    print('wrote', od)
