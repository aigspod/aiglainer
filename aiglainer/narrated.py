"""The narrated cut: scenes from the project's narration.py, time-warped to the synthesized lines.

For each scene the lines are laid end to end (GAP apart). Line k starts at real time r_k, and the
scene's visual clock is warped piecewise-linearly so visual time v_k (from the script) lands on r_k.
Visuals may play faster than authored, up to `smax`, to reach the next line; if they would need more,
the line waits instead (silence), so animation never looks rushed. Long holds after the last line are
fast-forwarded to `vend`.

build() -> (scenes, placements); each scene gets .warp = (r_points, v_points) and .rdur (real length).
placements: [{t, file, text, dur}] with t in seconds from the start of the video.
"""
import json, os
import numpy as np

from . import project

GAP = 0.3       # silence between consecutive lines
LEAD = 0.45     # earliest a scene's first line may start
SMAX = 1.8
HOLD = 0.75

def build():
    P = project.get()
    SCRIPT = P.narration().SCENES
    lines = json.load(open(P.path('lines.json')))
    by_scene = {}
    for l in lines:
        by_scene.setdefault(l['scene'], []).append(l)
    out, placements, T = [], [], 0.0
    for sd in SCRIPT:
        inst = P.scene_class(sd['scene'])()
        inst.entry = sd                 # the script entry, for layouts that read extra keys (shorts: crop, headline)
        smax = sd.get('smax', SMAX)
        r_pts, v_pts = [0.0], [sd.get('vstart', 0.0)]      # vstart: begin partway into the scene (shorts)
        t_free = LEAD
        for l in by_scene[sd.get('id', sd['scene'])]:
            v = l['v']
            r = max(t_free, r_pts[-1] + (v - v_pts[-1]) / smax)
            r_pts.append(r); v_pts.append(v)
            placements.append(dict(t=T + r, file=P.path(l['file']), text=l['text'], dur=l['dur']))
            t_free = r + l['dur'] + GAP
        rend = t_free - GAP + sd.get('hold', HOLD)
        vend = sd.get('vend', inst.dur)
        still = sd.get('still', 0.0)
        if still:
            r_pts.append(rend - still); v_pts.append(max(vend, v_pts[-1] + 0.01))
            vend = v_pts[-1] + 0.01
        r_pts.append(rend); v_pts.append(max(vend, v_pts[-1] + 0.01))
        inst.warp = (np.array(r_pts), np.array(v_pts))
        inst.rdur = rend
        out.append(inst)
        T += rend
    return out, placements

def plan():
    """Print each scene's real length and visual speed range, without rendering."""
    scs, pl = build()
    T = 0
    for s in scs:
        r, v = s.warp
        slopes = np.diff(v) / np.diff(r)
        print(f'{T // 60:.0f}:{T % 60:05.2f}  {type(s).__name__:15s} {s.rdur:6.2f}s  (authored {s.dur:5.1f}s)  speed {slopes.min():.2f}-{slopes[:-1].max() if len(slopes) > 1 else slopes.max():.2f}x, tail {slopes[-1]:.2f}x')
        T += s.rdur
    print(f'total {T // 60:.0f}:{T % 60:04.1f}  ({len(pl)} lines)')
