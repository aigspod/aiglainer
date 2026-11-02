"""Cold open, title, the question, the gaps, the testbed, the law."""
import math
import numpy as np
import skia
from aiglainer.core import *
from aiglainer.kit import *
from aiglainer.timeline import Scene
import walker as WK

RAST = None
def rasters():
    global RAST
    if RAST is None:
        RAST = load_json('rasters.json')
    return RAST

def draw_body(c, cam, Mw, Jw, a=1.0, color='g', bone_a=0.35, r=4.2, glow=7, dim_far=True):
    for b0, b1 in WK.BONES:
        P, _ = cam.project(np.array([Jw[b0], Jw[b1]]))
        line(c, *P[0], *P[1], 'muted', a * bone_a, 2)
    P, d = cam.project(Mw)
    order = np.argsort(-d)
    dn = (d - d.min()) / (np.ptp(d) + 1e-6)
    for i in order:
        k = 1 - 0.45 * dn[i] if dim_far else 1
        circle(c, P[i, 0], P[i, 1], r * (0.8 + 0.3 * k), fill=color, a=a * k, glow=glow)
    return P

def floor_grid(c, cam, a, ext=5, step=1.0):
    for v in np.arange(-ext, ext + 1e-6, step):
        for (p0, p1) in (((v, -ext, 0), (v, ext, 0)), ((-ext, v, 0), (ext, v, 0))):
            seg = np.linspace(p0, p1, 24)
            P, d = cam.project(seg)
            fade = np.clip(1.3 - (d - cam.dist) / 6, 0, 1)
            for i in range(len(P) - 1):
                line(c, P[i, 0], P[i, 1], P[i + 1, 0], P[i + 1, 1], 'g', a * 0.13 * fade[i], 1.2, cap='butt')

# ======================================================================= COLD OPEN
class ColdOpen(Scene):
    dur = 15.0
    fade_in = 1.2
    cues = [(0.6, 'drone'), (1.2, 'ping'), (3.7, 'ping'), (6.2, 'ping'), (8.7, 'ping'), (10.4, 'whoosh_soft'), (11.2, 'ping'), (13.0, 'riser')]

    def __init__(self):
        self.walk = WK.Walk(seed=11, dur=self.dur + 2, speed=1.1, area=0.9)
        self.radar = np.array([0.4, -3.6, 1.0])
        self.fb = np.linspace(150, -150, 140)
        rng = np.random.default_rng(1)
        self.cols_t = np.arange(0, self.dur + 0.5, 1 / 40)
        cols = []
        for tt in self.cols_t:
            col_, _, _ = WK.doppler_column(self.walk, tt + 0.5, self.radar, self.fb, noise=rng.normal(0, 1.2, len(self.fb)))
            cols.append(col_)
        spec = np.array(cols).T  # (F, T)
        lo, hi = np.percentile(spec, 35), np.percentile(spec, 99.7)
        self.spec = np.clip((spec - lo) / (hi - lo), 0, 1) ** 1.25

    def cam(self, t):
        p = np.mean([self.walk.state(t + 0.5 + d)[0] for d in (-0.6, -0.3, 0, 0.3, 0.6)], 0)
        return WK.Camera(yaw=-1.12 + 0.3 * t / self.dur, pitch=0.16, dist=8.4, focal=1500, cx=640, cy=700, target=(0.5 * p[0], -1.0 + 0.5 * p[1], 0.95))

    def draw(self, c, t):
        cam = self.cam(t)
        ag = ramp(t, 0.3, 2.5)
        floor_grid(c, cam, ag)
        # radar
        Rp, _ = cam.project(self.radar)
        Rp = Rp[0]
        Mw, Wt, Jw = self.walk.markers_world(t + 0.5)
        body_c = Mw.mean(0)
        Bp, _ = cam.project(body_c)
        Bp = Bp[0]
        ar = ramp(t, 0.8, 1.0)
        ang = math.atan2(Bp[1] - Rp[1], Bp[0] - Rp[0])
        # ping wavefronts travelling radar -> body and back
        for k in range(6):
            t0 = 1.2 + k * 2.5
            u = (t - t0) / 1.1
            if 0 <= u <= 1:
                dist = math.hypot(*(Bp - Rp))
                r = 40 + u * (dist - 40)
                arc = skia.Path()
                arc.addArc(skia.Rect.MakeXYWH(Rp[0] - r, Rp[1] - r, 2 * r, 2 * r), math.degrees(ang) - 18, 36)
                c.drawPath(arc, paint('g', ar * (1 - u) ** 0.7 * 0.8, stroke=3))
            u2 = (t - t0 - 1.1) / 1.1
            if 0 <= u2 <= 1:
                dist = math.hypot(*(Bp - Rp))
                r = 30 + u2 * (dist - 60)
                arc = skia.Path()
                arc.addArc(skia.Rect.MakeXYWH(Bp[0] - r, Bp[1] - r, 2 * r, 2 * r), math.degrees(ang) + 180 - 22, 44)
                c.drawPath(arc, paint('y', ar * (1 - u2) * 0.75, stroke=2.5))
        radar_icon(c, Rp[0], Rp[1], 1.5, ar, t, ping=False, direction=ang)
        # body
        ab = ramp(t, 0.2, 1.8)
        draw_body(c, cam, Mw, Jw, ab, color='ink', r=5.0, glow=9)
        # spectrogram panel
        aps = ramp(t, 2.6, 1.2)
        if aps > 0:
            x, y, w, h = 1250, 560, 560, 340
            panel(c, x - 14, y - 52, w + 28, h + 96, aps)
            kicker(c, 'radar · micro-Doppler', x, y - 20, aps, 'g', 17)
            note(c, 'illustration', x + w, y - 20, aps * 0.8, 15, align='right')
            span = 4.0
            n_vis = int(span * 40)
            i1 = int(clamp(t / self.dur) * (len(self.cols_t) - 1))
            i0 = max(0, i1 - n_vis)
            seg = self.spec[:, i0:i1 + 1]
            if seg.shape[1] > 1:
                im = array_image(seg)
                ww = w * seg.shape[1] / n_vis
                draw_image(c, im, x + w - ww, y, ww, h, aps)
            rrect(c, x, y, w, h, 4, stroke='line', sw=1.2, a=aps)
            text(c, 'time →', x + w, y + h + 30, 18, 500, 'muted', aps, 'right', kind='mono')
            text(c, 'Doppler', x, y + h + 30, 18, 500, 'muted', aps, kind='mono')
        # copy
        rich(c, 'A transformer watches a body move…', 120, 250, 64, 1200, t, 1.4, 0.06, 0.7, window(t, 1.4, 5.0, d_out=0.45), base_w=600)
        rich(c, '…and predicts what a radar will see.', 120, 250, 64, 1200, t, 5.7, 0.06, 0.7, window(t, 5.7, 9.4, d_out=0.45), base_w=600)
        rich(c, "It's accurate.", 120, 250, 64, 1200, t, 10.1, 0.06, 0.7, window(t, 10.1, 14.4), base_w=600)
        rich(c, '{y:But has it learned the physics?}', 120, 336, 64, 1300, t, 11.2, 0.06, 0.7, window(t, 11.2, 14.4), base_w=650)

# ======================================================================= TITLE
class Title(Scene):
    dur = 9.0
    fade_in = 0.2
    cues = [(0.0, 'impact')]
    WORDS = [('L', 'aw-'), ('A', 'ligned '), ('W', 'itness for '), ('F', 'aithful '), ('U', 'se of '), ('L', 'atents')]

    def draw(self, c, t):
        from aiglainer.notes import swash, lamp, sticky
        x0 = MX + 40
        kicker(c, 'the aigs pod  ·  /mull/  ·  journal club', x0, 320, ramp(t, 0.2, 0.8), 'muted', 18)
        # the lamp switches on as the title lands
        lamp(c, 1480, 330, 1.7, ramp(t, 0.0, 0.8), on=ramp(t, 0.15, 1.2, e_out))
        word = 'LAWFUL'
        size = 190
        f = font(size, 800)
        widths = [f.measureText(ch) for ch in word]
        trk = 0.02 * size
        x = x0
        for i, ch in enumerate(word):
            k = ramp(t, 0.05 + i * 0.07, 0.9, e_expo)
            with layer(c, k, (1 - k) * 18):
                text(c, ch, x, 520 + (1 - k) * 50, size, 800, 'ink', 1.0)
            x += widths[i] + trk
        swash(c, x0, x - trk, 556, 'y', 1, ramp(t, 0.7, 0.9, e_io), w=4)
        parts = []
        for init, rest in self.WORDS:
            parts.append((init, 'y', 520)); parts.append((rest, 'ink', 380))
        xx = x0
        for j, (s_, colr, w) in enumerate(parts):
            k = ramp(t, 1.1 + j * 0.05, 0.7)
            text(c, s_, xx, 632 + (1 - k) * 12, 44, w, colr, k, kind='italic')
            xx += text_width(s_, 44, w, 'italic')
        ka = ramp(t, 2.2, 0.8)
        text(c, 'Kevin Chen  ·  Kenneth W. Parker  ·  Anish Arora', x0, 720, 30, 500, 'ink', ka)
        text(c, 'The Ohio State University  ·  Independent Researcher', x0, 760, 23, 400, 'muted', ka)
        kb = ramp(t, 2.8, 0.8)
        kicker(c, 'mechanistic interpretability workshop · icml 2026  ·  arxiv:2607.28672', x0, 830, kb, 'muted', 17)
        sticky(c, 1500, 640, ['watch before', 'journal club'], ramp(t, 3.4, 0.5, e_back), rot=5.0, tag='todo')

# ======================================================================= QUESTION
class Question(Scene):
    dur = 20.5
    chapter = 0
    cues = [(0.2, 'whoosh'), (2.0, 'pop'), (6.0, 'pop'), (10.0, 'pop'), (14.6, 'tick')]
    CARDS = [
        ('1', 'Learned?', 'Has the network learned the governing law as formal, structured knowledge?', 'g'),
        ('2', 'Used?', 'Does its internal computation causally {y:use} that representation, or can a probe merely decode it?', 'f'),
        ('3', 'Valid?', "Does it hold across the law's whole {y:domain of validity}, or only on the training distribution?", 'c'),
    ]

    def draw(self, c, t):
        header(c, t, '01', 'The question', 'Accurate is not the same as *lawful*.')
        cw, gap, y0, ch = 532, 42, 360, 430
        for i, (n, lab, body, colr) in enumerate(self.CARDS):
            t0 = 2.0 + i * 4.0
            k = ramp(t, t0, 0.9, e_expo)
            if k <= 0:
                continue
            x = MX + i * (cw + gap)
            with layer(c, k):
                with xform(c, 0, (1 - k) * 40):
                    panel(c, x, y0, cw, ch, 1.0)
                    line(c, x + 36, y0 + 1, x + 36 + 120 * k, y0 + 1, colr, 1, 4, cap='butt')
                    text(c, n, x + 36, y0 + 118, 96, 800, colr, 0.95)
                    text(c, lab, x + 112, y0 + 104, 40, 700, 'ink', 1)
                    rich(c, body, x + 36, y0 + 200, 33, cw - 72, t, t0 + 0.3, 0.035, 0.5, 1.0, lh=1.36)
        caption(c, t, 'Three distinct claims, not three ways of saying "accurate". Answering them takes {y:mechanistic interpretability},'
                      ' not behavioral evaluation.', 14.6, None, y=900, size=32, maxw=1500)

# ======================================================================= GAPS
class Gaps(Scene):
    dur = 19.5
    chapter = 0
    cues = [(0.2, 'whoosh'), (1.6, 'tick'), (3.4, 'tick'), (5.2, 'tick'), (7.0, 'tick'), (9.4, 'stamp'), (10.0, 'stamp'), (11.4, 'stamp_soft'), (12.0, 'stamp_soft')]
    ROWS = [
        ('A {y:coverage-aware} causal-consistency measure over continuous counterfactuals', 'closed', 'f'),
        ('A {y:domain-of-validity} test for the identified circuit', 'closed', 'f'),
        ("Verifying the law's {y:invariants} and forbidden behaviors inside the circuit", 'groundwork', 'y'),
        ('Quantifying how a derived physical quantity {y:flows} through the circuit', 'groundwork', 'y'),
    ]

    def draw(self, c, t):
        header(c, t, '01', 'The question', 'Four gaps for laws over continuous variables')
        y0 = 380
        for i, (s, st, colr) in enumerate(self.ROWS):
            t0 = 1.6 + i * 1.8
            k = ramp(t, t0, 0.8, e_expo)
            if k <= 0:
                continue
            y = y0 + i * 118
            with layer(c, k):
                with xform(c, (1 - k) * -40, 0):
                    rrect(c, MX, y - 52, 1680, 96, 14, fill='panel', fa=0.6)
                    text(c, f'{i + 1}', MX + 34, y + 12, 44, 800, 'muted', 1)
                    rich(c, s, MX + 100, y + 10, 32, 1200, t, t0 + 0.2, 0.025, 0.4)
            ts = 9.4 + (i % 2) * 0.6 + (i // 2) * 2.0
            ks = ramp(t, ts, 0.45, e_back)
            if ks > 0:
                lbl = 'closed here' if st == 'closed' else 'groundwork laid'
                wpx = text_width(lbl.lower(), 22, 400, 'mono', 0.12) + 30
                pill(c, MX + 1680 - 30 - wpx, y - 26, lbl, colr, min(1, ks * 1.2), scale=0.6 + 0.4 * ks, size=22)
        caption(c, t, 'Existing causal-abstraction measures score consistency only on narrowly sampled, {y:discrete} counterfactual pairs.',
                14.0, None, y=905, size=30, maxw=1600)

# ======================================================================= TESTBED
class Testbed(Scene):
    dur = 26.0
    chapter = 1
    cues = [(0.2, 'whoosh'), (1.2, 'pop'), (4.0, 'pop'), (5.6, 'pop'), (7.6, 'pop'), (14.0, 'impact_soft'), (19.8, 'tick')]

    def __init__(self):
        r = rasters()
        self.model_spec = np.array(r['spec']['model'], float) / 255.0
        self.gt_spec = np.array(r['spec']['gt'], float) / 255.0

    def draw(self, c, t):
        header(c, t, '02', 'The testbed', 'The testbed: motion in, *radar* out')
        kd = ramp(t, 13.6, 0.8, e_io)
        with layer(c, 1 - kd * 0.88, blur=kd * 6):
            # --- body panel
            k1 = ramp(t, 1.2, 0.9, e_expo)
            bx, by, bw, bh = MX, 340, 470, 520
            with layer(c, k1):
                panel(c, bx, by, bw, bh)
                kicker(c, 'input · motion capture', bx + 28, by + 44, 1, 'ink', 17)
                cam = WK.Camera(yaw=-0.5 + 0.12 * math.sin(t * 0.3), pitch=0.12, dist=5.0, focal=900, cx=bx + bw / 2, cy=by + 262, target=(0, 0, 0.9))
                J = WK.skeleton(t * 2 * math.pi * 0.9)
                M, Wt = WK.markers(J)
                draw_body(c, cam, M, J, 1.0, color='g', r=4.2, glow=7)
                text(c, '53', bx + 28, by + bh - 40, 56, 800, 'g', 1)
                text(c, 'reflective markers', bx + 100, by + bh - 62, 22, 500, 'ink', 1)
                text(c, '× 256 frames × (x, y, z)', bx + 100, by + bh - 34, 22, 500, 'muted', 1)
            # --- model
            mx, my, mw = 700, 340, 520
            for j, (title, sub, colr, t0) in enumerate([
                    ('Spatial transformer', 'attention across markers, within a frame', 'x', 4.0),
                    ('Temporal transformer', 'attention across frames, over time', 'c', 5.6)]):
                k = ramp(t, t0, 0.9, e_expo)
                if k <= 0:
                    continue
                yy = my + j * 270
                with layer(c, k):
                    with xform(c, 0, (1 - k) * 30):
                        panel(c, mx, yy, mw, 240)
                        line(c, mx + 28, yy + 1, mx + 148, yy + 1, colr, 1, 4, cap='butt')
                        text(c, title, mx + 28, yy + 60, 32, 700, 'ink')
                        text(c, sub, mx + 28, yy + 96, 22, 400, 'muted')
                        text(c, '1 self-attention layer (8 heads) + MLP', mx + 28, yy + 214, 17, 500, 'muted', 0.9, kind='mono')
                        if j == 0:
                            pts = [(mx + 90 + 340 * (0.5 + 0.45 * math.cos(q * 2.4)), yy + 150 + 30 * math.sin(q * 1.7 + 0.5)) for q in range(9)]
                            for q in range(9):
                                for r_ in range(q + 1, 9):
                                    if (q * 7 + r_ * 3) % 4 == 0:
                                        line(c, *pts[q], *pts[r_], colr, 0.25 + 0.25 * math.sin(t * 2 + q + r_), 1.5)
                            for p in pts:
                                circle(c, p[0], p[1], 6, fill=colr, glow=6)
                        else:
                            n = 16
                            xs = [mx + 50 + i * 27 for i in range(n)]
                            for i in range(n):
                                line(c, xs[i], yy + 140, xs[i], yy + 172, colr, 0.6, 3)
                            q = int((t * 3) % n)
                            for i in range(n):
                                if i != q:
                                    h = 26 + abs(i - q) * 4
                                    arc = skia.Path(); arc.moveTo(xs[q], yy + 138)
                                    arc.quadTo((xs[q] + xs[i]) / 2, yy + 138 - h, xs[i], yy + 138)
                                    c.drawPath(arc, paint(colr, 0.15 + 0.5 * math.exp(-abs(i - q) / 4), stroke=1.5))
                            circle(c, xs[q], yy + 132, 6, fill='y', glow=6)
            # arrows
            ka = ramp(t, 3.4, 0.8)
            arrow(c, bx + bw + 14, 600, mx - 14, 600, 'muted', ka, 2.5, prog=ka)
            arrow(c, mx + mw / 2, my + 244, mx + mw / 2, my + 266, 'muted', ramp(t, 5.4, 0.5), 2.5)
            kb = ramp(t, 7.4, 0.8)
            arrow(c, mx + mw + 14, 600, 1300 - 14, 600, 'muted', kb, 2.5, prog=kb)
            if ka >= 1:
                flow_dots(c, np.array([[bx + bw + 14, 600], [mx - 14, 600]]), t, 'g', 1, 2, 0.6)
            if kb >= 1:
                flow_dots(c, np.array([[mx + mw + 14, 600], [1300 - 14, 600]]), t, 'c', 1, 2, 0.6)
            # --- output spectrogram (paper data: model prediction, Fig. 3)
            k3 = ramp(t, 7.6, 0.9, e_expo)
            ox, oy, ow, oh = 1300, 340, 500, 520
            if k3 > 0:
                with layer(c, k3):
                    panel(c, ox, oy, ow, oh)
                    kicker(c, 'output · micro-Doppler', ox + 28, oy + 44, 1, 'ink', 17)
                    sx, sy, sw, sh = ox + 28, oy + 70, ow - 56, 330
                    rev = ramp(t, 8.0, 4.5, e_lin)
                    ncol = max(2, int(self.model_spec.shape[1] * rev))
                    im = array_image(self.model_spec[:, :ncol])
                    draw_image(c, im, sx, sy, sw * ncol / self.model_spec.shape[1], sh)
                    rrect(c, sx, sy, sw, sh, 3, stroke='line', sw=1.2)
                    text(c, 'dB-scale spectrum, K Doppler bins', ox + 28, oy + oh - 76, 22, 500, 'ink')
                    note(c, 'model prediction · data from Fig. 3', ox + 28, oy + oh - 40, 1, 16)
        # --- the crucial point
        k4 = window(t, 14.0, None, 0.8)
        if k4 > 0:
            rich(c, 'Neither {y:f(t)} nor {y:v(t)} appears in the training data.', W / 2, 560, 64, 1700, t, 14.0, 0.07, 0.7, k4, 'center', base_w=700)
            rich(c, 'Inputs are marker positions; targets are spectrograms. No velocity or Doppler-frequency values are ever given.', W / 2, 640, 32, 1500, t, 15.4, 0.03, 0.5, k4, 'center', base='muted')
            k5 = ramp(t, 19.8, 0.8)
            with layer(c, k5):
                yy = 760
                for j, (big, small) in enumerate([('Trained on', 'fixed-direction walks'), ('Evaluated on', 'held-out random walks'), ('Model size', '3.2 M parameters')]):
                    x = W / 2 + (j - 1) * 470
                    text(c, big.lower(), x, yy, 17, 400, 'muted', 1, 'center', kind='mono', tracking=0.14)
                    text(c, small, x, yy + 44, 32, 600, 'ink', 1, 'center')
                note(c, 'Random walks are a class disjoint from training: an out-of-distribution test.', W / 2, yy + 110, 0.9, 18, 'muted', 'center')

# ======================================================================= DOPPLER LAW
class Doppler(Scene):
    dur = 23.5
    chapter = 1
    cues = [(0.2, 'whoosh'), (1.0, 'chime'), (5.6, 'pop'), (9.0, 'tick'), (16.0, 'tick')]

    def draw(self, c, t):
        header(c, t, '02', 'The testbed', 'The law it *should* have learned')
        k = ramp(t, 1.0, 1.0, e_expo)
        tex(c, 'doppler', 470, 470, 92 * (0.9 + 0.1 * k), k, glow=8 * k)
        # leader labels
        for j, (lbl, desc, xx, yy, colr) in enumerate([('f(t)', 'Doppler frequency shift', 160, 640, 'ink'),
                                                       ('v(t)', 'radial velocity toward / away from the radar', 160, 700, 'g'),
                                                       ('λ', 'radar wavelength', 160, 760, 'ink')]):
            kk = ramp(t, 2.4 + j * 0.6, 0.6)
            text(c, lbl, xx, yy, 30, 700, colr, kk, kind='italic')
            text(c, desc, xx + 90, yy, 28, 400, 'muted', kk)
        # ---- geometry diagram (right)
        kd = ramp(t, 5.6, 1.0, e_expo)
        if kd > 0:
            ox, oy = 1000, 300
            panel(c, ox, oy, 800, 560, kd)
            note(c, 'illustration', ox + 780, oy + 34, kd * 0.8, 15, align='right')
            R = np.array([ox + 110, oy + 250])
            radar_icon(c, R[0], R[1], 1.0, kd, t, ping=True, direction=0.0)
            # marker on a looping path
            th = t * 0.55
            P = np.array([ox + 530 + 160 * math.cos(th), oy + 240 + 125 * math.sin(th * 1.0)])
            V = np.array([-160 * math.sin(th), 125 * math.cos(th)]) * 0.6
            los = (P - R) / np.linalg.norm(P - R)
            vr = np.dot(V, los) * los
            vt = V - vr
            # trail
            trail = np.array([[ox + 530 + 160 * math.cos(th - s), oy + 240 + 125 * math.sin(th - s)] for s in np.linspace(0, 2.2, 40)])
            draw_poly(c, trail[::-1], 'ink', kd * 0.25, 2)
            line(c, *R, *P, 'muted', kd * 0.7, 1.5, dash=[6, 6])
            sc = 1.0
            arrow(c, *P, *(P + V * sc), 'ink', kd, 3, 13)
            kr = ramp(t, 9.0, 0.8)
            arrow(c, *P, *(P + vr * sc), 'g', kd * kr, 5, 15, glow=6)
            arrow(c, *P, *(P + vt * sc), 'v', kd * kr, 3, 12)
            circle(c, *P, 9, fill='ink', a=kd, glow=10)
            if kr > 0:
                q = P + vr * sc
                text(c, 'radial', q[0] + 12 * np.sign(vr[0] + 1e-9), q[1] - 10, 22, 600, 'g', kd * kr, 'left' if vr[0] >= 0 else 'right')
                q = P + vt * sc
                text(c, 'tangential', q[0] + 12, q[1] + 26, 22, 500, 'v', kd * kr)
            # Doppler readout bar
            vrad = -np.dot(V, los) / 60.0  # toward radar = positive shift
            kb = ramp(t, 10.0, 0.8)
            bx, by = ox + 40, oy + 500
            text(c, 'Doppler shift', bx, by - 14, 20, 600, 'muted', kd * kb, kind='mono')
            line(c, bx + 200, by - 20, bx + 720, by - 20, 'line', kd * kb, 6)
            mid = bx + 460
            line(c, mid, by - 20, mid + vrad * 230, by - 20, 'g', kd * kb, 6, glow=6)
            line(c, mid, by - 32, mid, by - 8, 'muted', kd * kb, 2)
        caption(c, t, 'Only motion {g:along the line of sight} shifts the frequency; tangential motion adds no first-order shift.', 11.5, 16.0, y=960, size=31)
        caption(c, t, 'The input holds only positions. To obey this law, the network must {y:compute velocity itself}, from positions over time.', 16.4, None, y=960, size=31)
