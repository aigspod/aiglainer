"""1500 AM The Bug Line, shouty edition: a hot-mic host who interrupts, callers on a crunchy phone line."""
import os, sys
sys.argv = ['x']
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, resample_poly
import make_audio as M
from aiglainer import backend, tts

HOST = ('am_eric', 'a', 1.16)
CALLERS = dict(liam=('am_liam', 'a', 1.12), jessica=('af_jessica', 'a', 1.12), lewis=('bm_lewis', 'b', 1.08), adam=('am_adam', 'a', 1.12),
               river=('af_river', 'a', 1.12), daniel=('bm_daniel', 'b', 1.1), sky=('af_sky', 'a', 1.1), alloy=('af_alloy', 'a', 1.12), aoede=('af_aoede', 'a', 1.12))
H = 'host'
CLIPS = {
    'bug_open': [(H, "You're on the Bug Line! Fifteen hundred A M! You got a complaint? I got no patience! Caller, you're on. Make it quick!")],
    'bug_1': [('liam', "Yeah, my job got killed at thirty nine minutes! The limit was forty!"), (H, "Did you use caffeinate?"), ('liam', "I used coffee!"), (H, "Coffee is not caffeinate! Get off my line!")],
    'bug_2': [('jessica', "My coding agent rewrote my entire repo while I was getting a sandwich!"), (H, "And who left the agent alone? You did! Commit your code! Next!")],
    'bug_3': [('lewis', "I've area weighted, I've masked the land, I've quoted the corrector column, and nobody told me what to do next!"), (H, "That's called being done! Go to lunch! Next!")],
    'bug_4': [('adam', "The radio played the same ad twice!"), (H, "It's the radio! That's what radio does! Next!")],
    'bug_5': [('river', "Kooda out of memory! Again!"), (H, "Smaller batch!"), ('river', "It was batch size one!"), (H, "Then get a bigger GPU! We'll be right back!")],
    'bug_6': [('daniel', "There's a pine tree air freshener hanging in my latent space!"), (H, "Don't touch the car! Nobody touches the car!")],
    'bug_7': [('sky', "Is the passcode a lowercase L, or a capital I?"), (H, "There is a copy button! It is right there! Use the copy button!")],
    'bug_8': [('alloy', "Why is the speedometer in miles per hour? We're scientists!"), (H, "Because it's a car! Cars don't do S I units! Next!")],
    'bug_9': [('aoede', "The police keep following me in the mirror!"), (H, "Then stop being so curious! Next!")],
    'bug_file': [(H, "Found a real bug? Open an issue! With steps to reproduce! Complaints without steps get read on air! Next!")],
}

def sos(kind, f, sr): return butter(4, f, kind, fs=sr, output='sos')
def hot(x, sr):            # the host: close, compressed, a little overdriven
    x = sosfilt(sos('highpass', 110, sr), x); x = np.tanh(2.6 * x / np.abs(x).max()) / np.tanh(2.6); return x
def phone(x, sr):          # callers: a narrow, crunchy phone line
    x = sosfilt(sos('bandpass', [320, 3300], sr), x); x = np.tanh(4.0 * x / np.abs(x).max()) / np.tanh(4.0)
    return x + 0.004 * np.random.default_rng(1).standard_normal(len(x))

for cid, parts in CLIPS.items():
    out = np.zeros(0, np.float32); sr = 24000; prev_host = None
    for who, text in parts:
        spec, lang, speed = HOST if who == H else CALLERS[who]
        a, sr = backend.synth(text, tts.kokoro_voice(spec), speed, lang)
        a = hot(a, sr) if who == H else phone(a, sr) * 0.85
        # the host jumps in before the caller has finished; callers wait a beat
        overlap = int((0.35 if who == H and prev_host is False else 0.0) * sr)
        gap = int((0.0 if overlap else 0.18) * sr)
        start = max(0, len(out) - overlap) + gap
        new = np.zeros(max(len(out), start + len(a)), np.float32); new[:len(out)] += out; new[start:start + len(a)] += a; out = new
        prev_host = who == H
    y = np.concatenate([np.zeros(int(0.12 * sr), np.float32), out, np.zeros(int(0.3 * sr), np.float32)]); y = y / np.abs(y).max() * 0.9
    w = os.path.join(M.OUT, cid + '.wav'); sf.write(w, y, sr); M.enc(w, w[:-4] + '.m4a', '64k')
    print(cid, round(len(y) / sr, 1), '|', backend.transcribe(w[:-4] + '.m4a')['text'].strip()[:140], flush=True)
