"""The on-air moments: a news-desk interruption when each session starts and when it wraps.
The page plays them over whatever is on (and flashes the pager) at 12:00, 14:00, 15:00 and 17:00 ET."""
import os, sys
sys.argv = ['x']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
import make_audio as M
from aiglainer import backend, tts

CLIPS = {
    'live_s1': [('george', "We interrupt this program. Session one of the hackathon is live, right now, on Teams. The link is on the page. Go!")],
    'wrap_s1': [('george', "That's a wrap on session one. Stretch your legs. Session two starts at three o'clock, Eastern. Same page, new link.")],
    'live_s2': [('george', "We interrupt this program. Session two is live, right now, on Teams. Pull up, and bring your checkpoints.")],
    'wrap_all': [('george', "And that's a wrap on the hackathon. Thanks for hacking, Port Samudra. Drive safe, and commit your code.")],
}
for cid, parts in CLIPS.items():
    segs = []
    for who, text in parts:
        spec, lang, speed = M.V[who]
        a, sr = backend.synth(text, tts.kokoro_voice(spec), speed, lang); segs += [a, np.zeros(int(0.35 * sr), np.float32)]
    y = np.concatenate([np.zeros(int(0.15 * sr), np.float32)] + segs); y = y / np.abs(y).max() * 0.9
    w = os.path.join(M.OUT, cid + '.wav'); sf.write(w, y, sr); M.enc(w, w[:-4] + '.m4a', '64k')
    print(cid, round(len(y) / sr, 1), '|', backend.transcribe(w[:-4] + '.m4a')['text'].strip(), flush=True)
