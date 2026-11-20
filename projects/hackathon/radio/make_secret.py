import os, sys
sys.argv = ['x']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
import make_audio as M
from aiglainer import audio, backend, tts
x = audio.music(M.LOOP + M.XF, lambda t: 1.0, 'cascade')
n, k = int(M.LOOP*audio.SR), int(M.XF*audio.SR); y = x[:n].copy(); r = np.linspace(0,1,k)[:,None]; y[:k] = y[:k]*r + x[n:n+k]*(1-r)
y = y/np.abs(y).max()*0.89; w = os.path.join(M.OUT, 'music_secret.wav'); sf.write(w, y, audio.SR); M.enc(w, w[:-4]+'.m4a', '112k')
CL = {'secret_1': [('michael', "You found every hidden package. Welcome to Hidden Layer, one oh eight. Nobody else knows about this station. Let's keep it that way.")],
      'secret_2': [('bella', "Hidden Layer, one oh eight. The station between the stations. If you can hear this, you looked everywhere.")],
      'secret_3': [('george', "This is Hidden Layer. Tonight's program is brought to you by curiosity, and by nobody reading the documentation.")]}
for cid, parts in CL.items():
    segs = []
    for who, text in parts:
        spec, lang, speed = M.V[who]; a, sr = backend.synth(text, tts.kokoro_voice(spec), speed, lang); segs += [a, np.zeros(int(0.35*sr), np.float32)]
    y = np.concatenate([np.zeros(int(0.15*sr), np.float32)] + segs); y = y/np.abs(y).max()*0.9
    w = os.path.join(M.OUT, cid + '.wav'); sf.write(w, y, sr); M.enc(w, w[:-4]+'.m4a', '64k')
    print(cid, backend.transcribe(w[:-4]+'.m4a')['text'].strip())
