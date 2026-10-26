"""Contact sheet of one scene at chosen authored times: python -m explainer preview Fig4a 5 12 20
Writes <project>/out/prev/<Scene>.png (half resolution when there is more than one frame)."""
import os
import numpy as np
import skia
from .core import W, H, FPS
from .timeline import Timeline
from . import project

def frames_sheet(imgs):
    cols = 2 if len(imgs) > 1 else 1
    rows = (len(imgs) + cols - 1) // cols
    sc = 2 if len(imgs) > 1 else 1
    h, w = H // sc, W // sc
    sheet = np.zeros((rows * h, cols * w, 3), np.uint8)
    for i, im in enumerate(imgs):
        r, c = divmod(i, cols)
        sheet[r * h:(r + 1) * h, c * w:(c + 1) * w] = im[::sc, ::sc]
    return sheet

def save_rgb(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rgba = np.concatenate([arr, np.full(arr.shape[:2] + (1,), 255, np.uint8)], -1)
    skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType).save(path, skia.kPNG)

def main(name, times):
    P = project.get()
    tl = Timeline([P.scene_class(name)()])
    imgs = []
    for t in times or [tl.scenes[0].dur / 2]:
        s = skia.Surface(W, H)
        tl.render(s.getCanvas(), int(round(t * FPS)))
        imgs.append(s.makeImageSnapshot().toarray()[:, :, :3])
    out = P.path('out', 'prev', f'{name}.png')
    save_rgb(frames_sheet(imgs), out)
    print(out)
