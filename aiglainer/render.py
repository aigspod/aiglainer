"""Parallel render -> H.264 segments -> concat."""
import os, subprocess, time, shutil
import multiprocessing as mp
import skia
from .core import W, H, FPS
from .timeline import Timeline
from . import project

CUTS = ('narrated', 'full')

def outdir(cut):
    return project.get().out(cut)

def make_timeline(cut):
    """cut='narrated' (voice-synced, from narration.py) or 'full' (the project's FULL_CUT, played as authored)."""
    P = project.get()
    if P.KIND == 'short' and cut == 'narrated':
        from . import short
        return short.make_timeline()
    if cut == 'full':
        if not P.FULL_CUT:
            raise SystemExit(f'project {P.name} has no FULL_CUT')
        return Timeline(P.FULL_CUT())
    from . import narrated
    scs, placements = narrated.build()
    tl = Timeline(scs)
    tl.placements = placements
    return tl

def worker(args):
    idx, f0, f1, cut = args
    tl = make_timeline(cut)
    w, h = getattr(tl, 'size', (W, H))
    path = os.path.join(outdir(cut), 'seg', f'seg_{idx:04d}.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{w}x{h}', '-r', str(FPS), '-i', '-',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation', '-g', str(FPS * 2), '-bf', '2',
           '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709', '-movflags', '+faststart', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = skia.Surface(w, h)
    c = surf.getCanvas()
    for fr in range(f0, f1):
        c.clear(skia.ColorBLACK)
        tl.render(c, fr)
        p.stdin.write(surf.makeImageSnapshot().toarray().tobytes())
    p.stdin.close()
    p.wait()
    return idx, f1 - f0

def main(cut='narrated', frames=()):
    tl = make_timeline(cut)
    od = outdir(cut)
    shutil.rmtree(os.path.join(od, 'seg'), ignore_errors=True)
    os.makedirs(os.path.join(od, 'seg'))
    n = tl.nframes
    a = frames[0] if frames else 0
    b = frames[1] if len(frames) > 1 else n
    chunk = 300
    jobs = [(i, f, min(f + chunk, b), cut) for i, f in enumerate(range(a, b, chunk))]
    print(f'total {tl.total:.1f}s, {n} frames; rendering {a}-{b} in {len(jobs)} chunks', flush=True)
    t0 = time.time()
    done = 0
    with mp.Pool(int(os.environ.get('NPROC', 16))) as pool:
        for idx, k in pool.imap_unordered(worker, jobs):
            done += k
            el = time.time() - t0
            print(f'  chunk {idx} ok  {done}/{b - a} frames  {el:.0f}s  eta {el / done * (b - a - done):.0f}s', flush=True)
    with open(os.path.join(od, 'list.txt'), 'w') as f:
        for i, _, _, _ in jobs:
            f.write(f"file 'seg/seg_{i:04d}.mp4'\n")
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', os.path.join(od, 'list.txt'),
                    '-c', 'copy', os.path.join(od, 'video_noaudio.mp4')], check=True)
    print('done', time.time() - t0)
