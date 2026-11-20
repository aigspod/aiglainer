import os, sys
sys.argv = ['x']; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
import make_audio as M
from aiglainer import audio
for name, style in dict(deep2='silencia', skip2='daylight', samudra2='berceuse', latent2='nuit').items():
    x = audio.music(M.LOOP + M.XF, lambda t: 1.0, style); n = int(M.LOOP*audio.SR); y = x[:n]
    k = int(2.0*audio.SR); y[:k] *= np.linspace(0, 1, k)[:, None]; y[-k:] *= np.linspace(1, 0, k)[:, None]
    y = y/np.abs(y).max()*0.89; w = os.path.join(M.OUT, f'music_{name}.wav'); sf.write(w, y, audio.SR); M.enc(w, w[:-4]+'.m4a', '112k'); print(name, style)
