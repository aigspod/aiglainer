"""Regression check for engine changes: hash sampled frames, cues and narration placements of a project.

  python -m aiglainer fingerprint -p lawful                 # write out/fingerprint.json (do this BEFORE a change)
  python -m aiglainer fingerprint -p lawful --compare       # after the change: report anything that differs

Renders every 397th frame of each cut the project has (no encoding, a few seconds), so a refactor that should
change nothing can be shown to change nothing. Audio is deterministic too: compare out/<cut>/audio.wav with cmp.
"""
import hashlib, json, os
import skia
from .core import W, H
from . import project

STEP = 397

def take():
    from .render import make_timeline
    P = project.get()
    res = {}
    for cut in ('narrated', 'full'):
        if cut == 'full' and not P.FULL_CUT:
            continue
        tl = make_timeline(cut)
        s = skia.Surface(W, H)
        frames = []
        for f in range(0, tl.nframes, STEP):
            s.getCanvas().clear(skia.ColorBLACK)
            tl.render(s.getCanvas(), f)
            frames.append(hashlib.md5(s.makeImageSnapshot().toarray().tobytes()).hexdigest())
        res[cut] = dict(nframes=tl.nframes, frames=frames, cues=[[round(t, 4), n] for t, n in tl.cues()],
                        placements=[[round(p['t'], 4), p['text']] for p in tl.placements])
    return res

def main(compare=False):
    P = project.get()
    path = P.path('out', 'fingerprint.json')
    now = take()
    if not compare:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(now, open(path, 'w'))
        print(f'wrote {path}: ' + ', '.join(f'{c} {len(v["frames"])} frames' for c, v in now.items()))
        return
    if not os.path.exists(path):
        raise SystemExit(f'no {path}; run without --compare first, before the change')
    ref = json.load(open(path))
    ok = True
    for cut, r in ref.items():
        n = now.get(cut)
        if n is None:
            print(f'{cut}: missing now'); ok = False; continue
        bad = [i * STEP for i, (a, b) in enumerate(zip(r['frames'], n['frames'])) if a != b]
        same = (r['nframes'] == n['nframes'], r['cues'] == n['cues'], r['placements'] == n['placements'])
        print(f'{cut}: {len(r["frames"]) - len(bad)}/{len(r["frames"])} frames identical'
              + (f', first differing frame {bad[0]}' if bad else '')
              + ('' if all(same) else f' | length/cues/placements same: {same}'))
        ok &= not bad and all(same)
    print('IDENTICAL' if ok else 'DIFFERENT')
    if not ok:
        raise SystemExit(1)
