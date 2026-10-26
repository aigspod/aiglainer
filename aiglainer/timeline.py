"""Scene sequencing, background, HUD."""
import math
import numpy as np
import skia
from .core import *
from .notes import draw_notes
from . import project

class Scene:
    dur = 10.0
    chapter = None      # index into the project's CHAPTERS (None = no HUD)
    cues = ()           # (t, sfx-name)
    fade_in = 0.45
    fade_out = 0.55
    def draw(self, c, t):
        pass

def scene_steps(s):
    if hasattr(s, 'steps'):
        return s.steps
    return project.get().CHAPTER_STEPS.get(s.chapter, ())

# ---------------------------------------------------------------- background
_bg = {}
def _bg_image():
    """The site's night ground: ink-blue paper, a warm lamp glow upper right, a thin inset frame."""
    if 'img' in _bg:
        return _bg['img']
    s = skia.Surface(W, H)
    c = s.getCanvas()
    c.clear(col('#161724'))
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((W * 0.8, H * 0.08), W * 0.55, [col('y', 0.11), col('y', 0.0)], [0.0, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    p = skia.Paint()
    p.setShader(skia.GradientShader.MakeRadial((W / 2, H / 2), W * 0.75, [skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 0), skia.Color(0, 0, 0, 110)], [0.0, 0.6, 1.0]))
    c.drawRect(skia.Rect.MakeWH(W, H), p)
    c.drawRect(skia.Rect.MakeXYWH(16, 16, W - 32, H - 32), paint('faint', 0.9, stroke=1.2))
    _bg['img'] = s.makeImageSnapshot()
    rng = np.random.default_rng(7)
    grains = []
    for _ in range(4):
        n = rng.integers(0, 255, (H // 2, W // 2), dtype=np.uint8)
        rgba = np.stack([n, n, n, np.full_like(n, 9)], -1)
        grains.append(skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType))
    _bg['grain'] = grains
    return _bg['img']

def draw_background(c, T):
    c.drawImage(_bg_image(), 0, 0)

def draw_grain(c, frame):
    g = _bg['grain'][(frame // 2) % 4]
    p = skia.Paint()
    p.setBlendMode(skia.BlendMode.kOverlay)
    c.drawImageRect(g, skia.Rect.MakeWH(W, H), skia.SamplingOptions(), p)

# ---------------------------------------------------------------- HUD
def draw_hud(c, T, total, chapter, a, chapter_starts, step_a=(0, 0, 0), tracker_a=0.0):
    if a <= 0.003:
        return
    P = project.get()
    text(c, P.HUD, 120, 70, 17, 400, 'muted', a * 0.85, kind='mono', tracking=0.14)
    if chapter is not None:
        w = text(c, P.CHAPTERS[chapter].lower(), W - 120, 70, 17, 400, 'ink', a * 0.85, 'right', kind='mono', tracking=0.14)
        text(c, f'{chapter + 1:02d} / ', W - 120 - w, 70, 17, 400, 'y', a * 0.9, 'right', kind='mono', tracking=0.14)
    if tracker_a > 0.003 and project.get().STEPS:
        draw_tracker(c, W / 2, 66, step_a, a * tracker_a)
    # progress bar
    x0, x1, y = 120, W - 120, 1040
    line(c, x0, y, x1, y, 'line', a, 2, cap='butt')
    prog = clamp(T / total)
    line(c, x0, y, x0 + (x1 - x0) * prog, y, 'y', a * 0.8, 2, cap='butt')
    for st in chapter_starts:
        xx = x0 + (x1 - x0) * st / total
        line(c, xx, y - 4, xx, y + 4, 'muted', a * 0.7, 1.4, cap='butt')

def draw_tracker(c, cx, y, step_a, a):
    """The project's story steps (e.g. behavior — cause — mechanism), current step(s) lit in amber."""
    size = 17
    STEPS = project.get().STEPS
    labels = [f'{i + 1} {s}' for i, s in enumerate(STEPS)]
    ws = [text_width(l, size, 400, 'mono', 0.12) for l in labels]
    gap = 54
    x = cx - (sum(ws) + gap * (len(ws) - 1)) / 2
    for i, (l, wd) in enumerate(zip(labels, ws)):
        k = step_a[i]
        colr = mix('faint', PAL['y'], k)
        circle(c, x - 14, y - 6, 4 + 1.5 * k, fill=colr, a=a, glow=6 * k)
        text(c, l, x, y, size, 400, mix('muted', PAL['y'], k), a * (0.55 + 0.45 * k), kind='mono', tracking=0.12)
        x += wd
        if i < len(ws) - 1:
            line(c, x + 12, y - 6, x + gap - 22, y - 6, 'faint', a, 1.4)
            x += gap

def rdur(s):
    """Real (on-screen) duration: the warped length for narrated scenes, else the authored one."""
    return getattr(s, 'rdur', s.dur)

def to_visual(s, t):
    """Map real scene time to the scene's authored (visual) time."""
    if hasattr(s, 'warp'):
        return float(np.interp(t, s.warp[0], s.warp[1]))
    return t

def to_real(s, v):
    if hasattr(s, 'warp'):
        return float(np.interp(v, s.warp[1], s.warp[0]))
    return v

class Timeline:
    def __init__(self, scenes):
        self.scenes = scenes
        for s in scenes:
            NOTES = project.get().NOTES
            if not hasattr(s, 'notes') and type(s).__name__ in NOTES:
                s.notes = NOTES[type(s).__name__]
        self.starts = []
        t = 0.0
        for s in scenes:
            self.starts.append(t)
            t += rdur(s)
        self.total = t
        self.nframes = int(round(t * FPS))
        self.placements = []
        self.chapter_starts = []
        seen = set()
        for s, st in zip(scenes, self.starts):
            if s.chapter is not None and s.chapter not in seen:
                seen.add(s.chapter)
                self.chapter_starts.append(st)

    def locate(self, T):
        for i in range(len(self.scenes) - 1, -1, -1):
            if T >= self.starts[i]:
                return i, T - self.starts[i]
        return 0, T

    def hud_alpha(self, T):
        # smooth HUD alpha across scene boundaries
        def on(T):
            i, _ = self.locate(T)
            return 1.0 if self.scenes[i].chapter is not None else 0.0
        vals = [on(T + d) for d in np.linspace(-0.6, 0.6, 7)]
        return float(np.mean(vals))

    def step_alpha(self, T):
        """Smoothed brightness of each tracker step, and of the tracker itself, around time T."""
        acc, on = np.zeros(max(1, len(project.get().STEPS))), 0.0
        ds = np.linspace(-0.5, 0.5, 5)
        for d in ds:
            i, _ = self.locate(min(max(T + d, 0), self.total - 1e-3))
            st = scene_steps(self.scenes[i])
            if getattr(self.scenes[i], 'tracker', bool(st)):
                on += 1
            for k in st:
                acc[k] += 1
        return acc / len(ds), on / len(ds)

    def render(self, c, frame):
        T = frame / FPS
        i, t = self.locate(T)
        sc = self.scenes[i]
        draw_background(c, T)
        d = rdur(sc)
        a = ramp(t, 0, sc.fade_in, e_out) * (1 - ramp(t, d - sc.fade_out, sc.fade_out, e_io))
        with layer(c, a):
            sc.draw(c, to_visual(sc, t))
        if hasattr(sc, 'notes'):
            with layer(c, a):
                draw_notes(c, sc.notes, to_visual(sc, t))
        sa, ta = self.step_alpha(T)
        draw_hud(c, T, self.total, sc.chapter, self.hud_alpha(T), self.chapter_starts, sa, ta)
        draw_grain(c, frame)
        black = max(1 - ramp(T, 0.0, 0.9, e_io), ramp(T, self.total - 1.6, 1.5, e_io))
        if black > 0:
            c.drawRect(skia.Rect.MakeWH(W, H), paint('#000000', black))

    def cues(self):
        out = []
        for s, st in zip(self.scenes, self.starts):
            for (t, name) in s.cues:
                if to_visual(s, 0) <= t <= to_visual(s, rdur(s)):
                    out.append((st + to_real(s, t), name))
        return sorted(out)
