"""97.7 The Block (two original hip-hop beats), 1500 AM The Bug Line (hold music + call-in clips), and more ads."""
import os, sys
sys.argv = ['x'] + sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, soundfile as sf
import make_audio as M
from aiglainer import audio, backend, tts
from aiglainer.audio import SR, lp, hp, bp, mtof

rng = np.random.default_rng(977)
LEN = 150.0

def env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

def kick():
    n = int(0.5 * SR); t = np.arange(n) / SR
    f = 46 + 95 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, 0.28)
    x += 0.25 * rng.standard_normal(n) * env(n, 0.0005, 0.004)
    return np.tanh(1.6 * x) * 0.9

def snare():
    n = int(0.4 * SR); t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 1400, 7000) * env(n, 0.001, 0.13)
    body = np.sin(2 * np.pi * 185 * t) * env(n, 0.001, 0.06)
    return (0.75 * noise / np.abs(noise).max() + 0.5 * body) * 0.7

def hat(open_=False):
    n = int((0.25 if open_ else 0.06) * SR)
    x = hp(rng.standard_normal(n), 7500) * env(n, 0.0005, 0.12 if open_ else 0.022)
    return x / np.abs(x).max() * (0.22 if open_ else 0.16)

def rhodes(midi, dur):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(midi)
    x = (np.sin(2*np.pi*f*t) + 0.35*np.sin(2*np.pi*2*f*t + 0.3) + 0.08*np.sin(2*np.pi*3*f*t)) * env(n, 0.006, 1.6)
    x *= 1 + 0.18 * np.sin(2 * np.pi * 4.6 * t)       # tremolo
    x *= np.minimum(1, (n - np.arange(n)) / (0.05 * SR))
    return x

def bass808(midi, dur, glide_to=None):
    n = int(dur * SR); t = np.arange(n) / SR
    f = np.full(n, mtof(midi))
    if glide_to is not None:
        k = int(0.7 * n); f[k:] = mtof(midi) + (mtof(glide_to) - mtof(midi)) * np.minimum(1, (np.arange(n - k)) / (0.08 * SR))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.004, 0.9)
    x *= np.minimum(1, (n - np.arange(n)) / (0.03 * SR))
    return np.tanh(2.2 * x) * 0.55

def whine(notes, step):
    """G-funk lead: a portamento sine-saw with vibrato, high up."""
    n = int(len(notes) * step * SR); t = np.arange(n) / SR
    tgt = np.repeat([mtof(m) if m else 0 for m in notes], int(step * SR))[:n]
    tgt = np.pad(tgt, (0, n - len(tgt)), mode='edge')
    f = np.copy(tgt); a = np.exp(-1 / (0.06 * SR))
    for i in range(1, n):                               # portamento
        f[i] = f[i - 1] * a + tgt[i] * (1 - a) if tgt[i] else f[i - 1]
    f *= 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t)
    ph = np.cumsum(f) / SR
    x = np.sin(2 * np.pi * ph) + 0.3 * (2 * (ph % 1) - 1)
    gate = (tgt > 0).astype(float); gate = np.convolve(gate, np.ones(int(0.03 * SR)) / int(0.03 * SR), 'same')
    return lp(x * gate, 3200) * 0.11

def place(out, x, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= len(out): return
    x = x[:len(out) - i]
    out[i:i + len(x), 0] += x * gain * (1 - max(0, pan))
    out[i:i + len(x), 1] += x * gain * (1 + min(0, pan))

def beat(bpm, chords, kicks, swing, gfunk, seed):
    global rng
    rng = np.random.default_rng(seed)
    n = int(LEN * SR); out = np.zeros((n, 2))
    beat_s = 60 / bpm; bar = 4 * beat_s; s16 = beat_s / 4
    K, S, H, HO = kick(), snare(), [hat() for _ in range(4)], hat(True)
    nbars = int(LEN / bar) + 1
    for b in range(nbars):
        t0 = b * bar
        root, voicing = chords[b % len(chords)]
        drums = b >= 4 and (b % 16 != 15)                  # 4-bar intro, a 1-bar break every 16
        for m in voicing:                                    # chord stabs on 1 and the 'and' of 2
            for at, v in [(0, 0.16), (1.5 * beat_s, 0.11)]:
                place(out, rhodes(m, bar * 0.6), t0 + at + rng.uniform(0, 0.01), v, pan=rng.uniform(-0.3, 0.3))
        if b >= 2:
            nxt = chords[(b + 1) % len(chords)][0]
            place(out, bass808(root - 12, beat_s * 1.6), t0, 0.9)
            place(out, bass808(root - 12, beat_s * 1.1, glide_to=nxt - 12 if b % 2 else None), t0 + 2.5 * beat_s, 0.75)
        if not drums: continue
        for st in range(16):
            sw = swing * s16 if st % 2 else 0
            at = t0 + st * s16 + sw
            if kicks[st]: place(out, K, at, 0.95)
            if st in (4, 12): place(out, S, at + 0.008, 0.85)
            if st % 2 == 0: place(out, H[st // 2 % 4], at, 0.9 if st % 4 == 0 else 0.6, pan=0.25)
            elif rng.random() < 0.25: place(out, H[1], at, 0.35, pan=0.25)
        if b % 4 == 3: place(out, HO, t0 + 14 * s16 + swing * s16, 0.8, pan=0.25)
        if gfunk and b >= 8 and (b // 4) % 2 == 0:
            motif = [[84, 0, 87, 89, 0, 87, 84, 0], [82, 0, 84, 0, 87, 0, 84, 82]][(b // 2) % 2]
            place(out, whine(motif, beat_s / 2), t0, 1.0, pan=-0.2)
    # vinyl: hiss + crackle
    hiss = hp(rng.standard_normal(n), 3000) * 0.004
    crack = np.zeros(n); idx = rng.integers(0, n, int(LEN * 9)); crack[idx] = rng.uniform(-0.25, 0.25, len(idx))
    crack = hp(crack, 1500)
    out[:, 0] += hiss + crack; out[:, 1] += np.roll(hiss, 37) + np.roll(crack, 11)
    out = lp(out, 11000)
    k = int(2.0 * SR); out[:k] *= np.linspace(0, 1, k)[:, None]; out[-k:] *= np.linspace(1, 0, k)[:, None]
    return np.tanh(out * 1.3) / 1.3

def save(name, y, br='128k'):
    y = y / max(1e-9, np.abs(y).max()) * 0.89
    w = os.path.join(M.OUT, f'music_{name}.wav'); sf.write(w, y, SR); M.enc(w, w[:-4] + '.m4a', br); print('music', name)

if 'music' in sys.argv:
    # The Block 1: boom bap in C minor; 2: G-funk in Eb minor with the whine
    save('block', beat(88, [(60, [63, 67, 70, 74]), (65, [63, 68, 72, 75]), (68, [63, 67, 72, 75]), (67, [62, 65, 71, 74])],
                       [1,0,0,0, 0,0,0,1, 0,0,1,0, 0,0,0,0], 0.16, False, 1))
    save('block2', beat(92, [(63, [61, 66, 70, 73]), (59, [63, 66, 70, 75]), (68, [66, 71, 75, 78]), (70, [62, 68, 72, 74])],
                        [1,0,0,1, 0,0,1,0, 1,0,0,0, 0,1,0,0], 0.12, True, 2))
    # The Bug Line: hold music from the engine's pad styles
    for name, style in dict(bugline='dawn', bugline2='night').items():
        x = audio.music(LEN, lambda t: 1.0, style); k = int(2.0 * SR); x[:k] *= np.linspace(0, 1, k)[:, None]; x[-k:] *= np.linspace(1, 0, k)[:, None]
        save(name, x, '96k')

V = dict(M.V, adam=('am_adam', 'a', 1.05), onyxv=('am_onyx', 'a', 1.0), sarah=('af_sarah', 'a', 1.0), liam=('am_liam', 'a', 1.0),
         jessica=('af_jessica', 'a', 1.0), lewis=('bm_lewis', 'b', 0.95), river=('af_river', 'a', 1.0), daniel=('bm_daniel', 'b', 1.0),
         nova=('af_nova', 'a', 1.05), santa=('am_santa', 'a', 1.0), fable=('bm_fable', 'b', 1.0), alloy=('af_alloy', 'a', 1.0), aoede=('af_aoede', 'a', 1.0))
CLIPS = {
    'block_1': [('adam', "Ninety seven point seven, The Block! Straight outta the residual stream. U-Net Boyz in the building. Latent Gs on deck.")],
    'block_2': [('adam', "This next one goes out to everybody whose loss went flat at epoch three. Keep your head up. Lower your learning rate.")],
    'block_3': [('adam', "You're locked to The Block. Hip-hop for people who read the attention maps.")],
    'block_4': [('adam', "Shout out to session two, three o'clock Eastern. Pull up. Bring your checkpoints.")],
    'block_verse1': [('onyxv', "Yo. Started from the bottleneck, now we here. Skip connection, full resolution, crystal clear. Gradients flowing, never vanish, never fear. Latent Gs in the stream, all year.")],
    'block_verse2': [('onyxv', "Check it. I patch the edge, then I patch it again. Area weighted, masked the land, counted to ten. One seed's a rumor, five seeds is a trend. U-Net Boyz, from the encoder to the end.")],
    'bug_open': [('sarah', "You're on the Bug Line, fifteen hundred A M. The only station where every complaint is a feature request. Lines are open. Caller, go ahead.")],
    'bug_1': [('liam', "Yeah, hi. My job got killed at thirty nine minutes. The limit was forty. I had one minute left."), ('sarah', "Did you use caffeinate?"), ('liam', "I used coffee."), ('sarah', "That's not the same thing. Next caller.")],
    'bug_2': [('jessica', "Hi. My coding agent rewrote my entire repo while I was getting a sandwich."), ('sarah', "Was the sandwich good?"), ('jessica', "Honestly? Yes."), ('sarah', "Then it was a fair trade. Commit early, commit often.")],
    'bug_3': [('lewis', "I've area weighted my means, masked the land, and quoted the corrector column. Nobody told me what to do next."), ('sarah', "Sir, that's called being done. Please hang up and go to lunch.")],
    'bug_4': [('adam', "Yeah. The radio played the same ad twice."), ('sarah', "Sir. This is the radio.")],
    'bug_5': [('river', "CUDA out of memory. Again."), ('sarah', "Have you tried a smaller batch?"), ('river', "It was batch size one."), ('sarah', "We'll be right back.")],
    'bug_6': [('eric', "There's a pine tree air freshener hanging in my latent space."), ('sarah', "That's a known issue. It's from the car. Don't touch the car.")],
    'bug_7': [('sky', "Is the passcode a lowercase L, or a capital I?"), ('sarah', "It's on the page. There's a copy button. Use the copy button.")],
    'bug_file': [('sarah', "Found a real bug? Open an issue on GitHub, with steps to reproduce. Complaints without steps to reproduce will be read on air.")],
    'ad_clip': [('daniel', "Exploding gradients? Come on down to the Gradient Clipping Barbershop. We'll take a little off the top. Norm of one, every time. Walk-ins welcome.")],
    'ad_lrcars': [('santa', "Learning Rate Used Cars! Prices slashed on a cosine schedule! No warmup required! Our prices are so low, they're practically one e minus five! Learning Rate Used Cars. We converge, eventually.")],
    'ad_dropout': [('nova', "Memorizing the training set? Doctor Dropout's clinic can help. We randomly forget half of everything, so you don't have to. Doctor Dropout. Generalize responsibly.")],
    'ad_attention': [('liam', "Can't focus? Try Multi Head, the energy drink with sixteen heads of attention. Side effects may include looking everywhere at once. Multi Head. Pay attention.")],
    'ad_null': [('aoede', "Lonely? Try Null Hypothesis Dating. We'll never reject you. We'll just fail to reject you. Null Hypothesis Dating. P less than point oh five, or your money back.")],
    'ad_storage': [('fable', "Is your home directory full? Try Scratch Space Storage. We keep your checkpoints for ninety days, then delete them without telling you. Scratch Space Storage. Back it up.")],
    'ad_seed42': [('alloy', "And now, this week's seed lottery. The winning seed is, forty two. Again. It's always forty two.")],
}
if 'voices' in sys.argv:
    for cid, parts in CLIPS.items():
        segs = []
        for who, text in parts:
            spec, lang, speed = V[who]; a, sr = backend.synth(text, tts.kokoro_voice(spec), speed, lang); segs += [a, np.zeros(int(0.4 * sr), np.float32)]
        y = np.concatenate([np.zeros(int(0.15 * sr), np.float32)] + segs); y = y / np.abs(y).max() * 0.9
        w = os.path.join(M.OUT, cid + '.wav'); sf.write(w, y, sr); M.enc(w, w[:-4] + '.m4a', '64k')
        print(cid, round(len(y) / sr, 1), '|', backend.transcribe(w[:-4] + '.m4a')['text'].strip()[:150], flush=True)
