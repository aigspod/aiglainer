"""Contact sheets with one frame per narration line, captioned with the line, to eyeball sync.

  python -m aiglainer frames          -> <project>/out/narrated/qa/sheet_*.png
Each frame is taken just after its line starts (half the line, at most 1.2 s, in).
"""
import json, os, subprocess
from . import project

def main(cut='narrated'):
    P = project.get()
    od = P.out(cut)
    video = os.path.join(od, P.OUTPUT_NAME)
    qa = os.path.join(od, 'qa')
    os.makedirs(qa, exist_ok=True)
    for f in os.listdir(qa):
        os.remove(os.path.join(qa, f))
    P = json.load(open(os.path.join(od, 'placements.json')))
    for i, p in enumerate(P):
        t = p['t'] + min(1.2, p['dur'] * 0.5)
        txt = f"{i:02d}  {p['text'][:70]}".replace("'", '').replace(':', ' ').replace(',', ' ')
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', f'{t:.2f}', '-i', video,
                        '-frames:v', '1', '-vf', f"scale=640:360,drawtext=fontfile=/System/Library/Fonts/SFNS.ttf:text='{txt}'"
                        ":x=6:y=340:fontsize=13:fontcolor=yellow:box=1:boxcolor=black@0.75", os.path.join(qa, f'l_{i:02d}.png')], check=True)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-pattern_type', 'glob', '-i', os.path.join(qa, 'l_*.png'),
                    '-vf', 'tile=3x5', os.path.join(qa, 'sheet_%02d.png')], check=True)
    print('wrote', qa)


