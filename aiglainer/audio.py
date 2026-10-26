"""Procedural score + sound design, synced to the timeline cues."""
import os, math
import numpy as np
from scipy.signal import fftconvolve, butter, sosfilt
from . import project

SR = 48000
rng = np.random.default_rng(12)

def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)

def env_adsr(n, a, d, s, r, sr=SR):
    A, D, R = int(a * sr), int(d * sr), int(r * sr)
    S = max(0, n - A - D - R)
    e = np.concatenate([np.linspace(0, 1, A, False), np.linspace(1, s, D, False), np.full(S, s), np.linspace(s, 0, R)])
    return np.pad(e, (0, max(0, n - len(e))))[:n]

def lp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), 'low', output='sos')
    return sosfilt(sos, x, axis=0)

def hp(x, fc, order=2):
    sos = butter(order, fc / (SR / 2), 'high', output='sos')
    return sosfilt(sos, x, axis=0)

def bp(x, f1, f2, order=2):
    sos = butter(order, [f1 / (SR / 2), f2 / (SR / 2)], 'band', output='sos')
    return sosfilt(sos, x, axis=0)

def stereo(x, pan=0.0):
    l = math.cos((pan + 1) * math.pi / 4); r = math.sin((pan + 1) * math.pi / 4)
    return np.stack([x * l, x * r], 1) * 1.414

def reverb_ir(sec=3.2, decay=3.0):
    n = int(sec * SR)
    t = np.arange(n) / SR
    ir = rng.normal(0, 1, (n, 2)) * np.exp(-decay * t)[:, None]
    ir = lp(ir, 6000)
    ir[:int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))[:, None]
    return ir / np.sqrt((ir ** 2).sum(0))

# ---------------------------------------------------------------- music
CHORDS = [
    [50, 57, 60, 64, 65],   # Dm9
    [46, 53, 57, 60, 62],   # Bbmaj7(9)
    [45, 53, 60, 64, 67],   # Fmaj9/A
    [48, 55, 62, 64, 69],   # C6/9
]
CH_LEN = 8.0

def pad_note(freq, n, bright=0.5):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for det in (-0.07, 0.0, 0.07):
        f = freq * 2 ** (det / 12)
        ph = rng.uniform(0, 2 * np.pi)
        for h in range(1, 9):
            out += (bright ** (h - 1)) / h * np.sin(2 * np.pi * f * h * t + ph * h)
    vib = 1 + 0.15 * np.sin(2 * np.pi * 0.13 * t + rng.uniform(0, 6))
    return out * vib / 6

# Styles of the score, chosen by a project's MUSIC['style']. 'night' is the original (and the default).
STYLES = dict(
    night=dict(chords=CHORDS, ch_len=CH_LEN, bpm=96, pattern=[0, 2, 4, 3, 1, 4, 2, 3], pulse=0.0, cutoff=5200),
    # brighter and quicker: C6/9 - Am11 - Fmaj9 - G6sus4, eighth-note arpeggio at 112 bpm, a soft heartbeat on the beat
    dawn=dict(chords=[[48, 55, 62, 64, 69], [45, 52, 57, 60, 62], [41, 48, 57, 60, 64], [43, 50, 55, 60, 64]],
              ch_len=60 / 112 * 8, bpm=112, pattern=[0, 1, 2, 3, 2, 1, 3, 2], pulse=0.07, cutoff=6400),
)

def music(total, arp_on, style='night'):
    S = STYLES[style]
    CHORDS, CH_LEN = S['chords'], S['ch_len']
    n = int(total * SR) + SR * 4
    out = np.zeros((n, 2))
    k = 0
    t = 0.0
    while t < total + 2:
        chord = CHORDS[k % len(CHORDS)]
        seg = int((CH_LEN + 3.0) * SR)
        i0 = int(t * SR)
        e = env_adsr(seg, 2.2, 0.5, 0.85, 3.2)
        for j, m in enumerate(chord):
            x = pad_note(mtof(m), seg, 0.42) * e * (0.9 if j else 1.0)
            pan = (-0.5 + j / (len(chord) - 1)) * 0.8
            s = stereo(x, pan)
            end = min(n, i0 + seg)
            out[i0:end] += s[:end - i0] * 0.11
        # sub
        sub = np.sin(2 * np.pi * mtof(chord[0] - 12) * np.arange(seg) / SR) * e * 0.10
        end = min(n, i0 + seg)
        out[i0:end] += stereo(sub)[:end - i0]
        # arpeggio plucks
        step = 60 / S['bpm'] / 2
        nsteps = int(CH_LEN / step)
        pattern = S['pattern']
        for s_ in range(nsteps):
            tt = t + s_ * step
            amt = arp_on(tt)
            if amt <= 0.01:
                continue
            m = chord[1:][pattern[(s_ + k) % len(pattern)] % 4] + 12
            L = int(0.9 * SR)
            tl = np.arange(L) / SR
            f = mtof(m)
            x = (np.sin(2 * np.pi * f * tl) + 0.25 * np.sin(2 * np.pi * 2 * f * tl) + 0.08 * np.sin(2 * np.pi * 3 * f * tl)) * np.exp(-tl * 5.5)
            x *= np.minimum(1, tl / 0.004)
            acc = 1.0 if s_ % 4 == 0 else 0.7
            a0 = int(tt * SR)
            if a0 + L < n:
                out[a0:a0 + L] += stereo(x, 0.35 * math.sin(s_ * 1.3)) * 0.035 * amt * acc
            if S['pulse'] and s_ % 2 == 0 and amt > 0.01:      # a soft kick on each beat
                L = int(0.35 * SR)
                tl = np.arange(L) / SR
                x = np.sin(2 * np.pi * np.cumsum(48 + 60 * np.exp(-tl * 30)) / SR) * np.exp(-tl * 9) * np.minimum(1, tl / 0.003)
                if a0 + L < n:
                    out[a0:a0 + L] += stereo(x) * S['pulse'] * amt * (1.0 if s_ % 8 == 0 else 0.75)
        t += CH_LEN
        k += 1
    out = lp(out, S['cutoff'])
    return out[:int(total * SR)]

# ---------------------------------------------------------------- sfx
def s_ping():
    L = int(1.6 * SR); t = np.arange(L) / SR
    f = 1760 * (1 - 0.02 * t)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * np.minimum(1, t / 0.002)
    echo = np.zeros(L)
    d = int(0.42 * SR)
    t2 = np.arange(L - d) / SR
    echo[d:] = np.sin(2 * np.pi * 1810 * t2) * np.exp(-t2 * 9) * 0.35   # the Doppler-shifted return
    return stereo(x * 0.22, -0.3) + stereo(echo * 0.22, 0.4)

def s_whoosh(gain=0.18, dur=0.9):
    L = int(dur * SR); t = np.arange(L) / SR
    noise = rng.normal(0, 1, L)
    e = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    lo = bp(noise, 300, 1800) * e
    hi = bp(noise, 1800, 6000) * e * np.linspace(0.2, 1, L)
    x = (lo * 0.7 + hi * 0.4)
    pan = np.linspace(-0.6, 0.6, L)
    return np.stack([x * (1 - pan) / 2, x * (1 + pan) / 2], 1) * gain * 2

def s_pop(f=740, gain=0.16):
    L = int(0.16 * SR); t = np.arange(L) / SR
    fr = f * (1 + 0.6 * np.exp(-t * 60))
    x = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 32) * np.minimum(1, t / 0.0015)
    return stereo(x * gain, rng.uniform(-0.3, 0.3))

def s_tick(gain=0.12):
    L = int(0.06 * SR); t = np.arange(L) / SR
    x = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 120) + hp(rng.normal(0, 1, L), 3000) * np.exp(-t * 300) * 0.3
    return stereo(x * gain, 0.1)

def s_stamp(gain=0.30):
    L = int(0.5 * SR); t = np.arange(L) / SR
    f = 140 * np.exp(-t * 8) + 50
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 10)
    x += lp(rng.normal(0, 1, L), 2500) * np.exp(-t * 60) * 0.5
    return stereo(x * gain)

def s_chime(gain=0.13):
    L = int(3.0 * SR); t = np.arange(L) / SR
    x = np.zeros(L)
    for f, a, d in ((1318.5, 1, 2.2), (1975.5, 0.6, 2.8), (2637, 0.25, 4), (3951, 0.12, 6)):
        x += a * np.sin(2 * np.pi * f * t) * np.exp(-t * d)
    x *= np.minimum(1, t / 0.003)
    return stereo(x * gain * 0.6, -0.2) + stereo(np.roll(x, int(0.09 * SR)) * gain * 0.3, 0.4)

def s_impact(gain=0.55, soft=False):
    L = int(3.0 * SR); t = np.arange(L) / SR
    f = 38 + 70 * np.exp(-t * 6)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * (1.6 if not soft else 3.0))
    crack = lp(rng.normal(0, 1, L), 3500 if not soft else 1800) * np.exp(-t * 18)
    x = boom + crack * (0.35 if not soft else 0.15)
    return stereo(x * gain * (0.5 if soft else 1))

def s_riser(dur=2.2, gain=0.16):
    L = int(dur * SR); t = np.arange(L) / SR
    noise = rng.normal(0, 1, L)
    e = (t / dur) ** 2.2
    x = hp(noise, 1200) * e * 0.6
    f = 200 + 1400 * (t / dur) ** 2
    x += np.sin(2 * np.pi * np.cumsum(f) / SR) * e * 0.35
    return stereo(x * gain)

def s_sweep(gain=0.07):
    L = int(1.6 * SR); t = np.arange(L) / SR
    f = 330 * 2 ** (t / 1.6 * 1.0)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / 1.6) ** 2
    x += 0.4 * np.sin(2 * np.pi * np.cumsum(f * 1.5) / SR) * np.sin(np.pi * t / 1.6) ** 2
    return stereo(x * gain, 0.2)

_blip_n = [0]
def s_blip(gain=0.13):
    notes = [74, 77, 79, 81, 84, 86]
    m = notes[_blip_n[0] % len(notes)]; _blip_n[0] += 1
    L = int(0.5 * SR); t = np.arange(L) / SR
    f = mtof(m)
    x = (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 9) * np.minimum(1, t / 0.002)
    return stereo(x * gain)

def s_draw(gain=0.05):
    L = int(2.2 * SR); t = np.arange(L) / SR
    x = np.zeros(L)
    for f in (880, 1320, 1760):
        x += np.sin(2 * np.pi * f * t * (1 + 0.04 * t))
    x *= np.sin(np.pi * t / 2.2) ** 2
    return stereo(x * gain / 3, -0.1)

def s_count(gain=0.09):
    L = int(2.2 * SR)
    out = np.zeros((L, 2))
    times = np.cumsum(0.035 * 1.13 ** np.arange(18))
    for k, tt in enumerate(times):
        if tt > 2.0:
            break
        clk = s_tick(gain * (1 - tt / 2.4))
        i = int(tt * SR)
        out[i:i + len(clk)] += clk[:L - i]
    return out

def s_drop(gain=0.12):
    L = int(1.4 * SR); t = np.arange(L) / SR
    f = 900 * np.exp(-t * 2.2) + 80
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.8) * np.minimum(1, t / 0.01)
    return stereo(x * gain)

def s_outro(gain=0.18):
    L = int(5 * SR); t = np.arange(L) / SR
    x = np.zeros(L)
    for m in (62, 69, 74, 76, 81):
        x += np.sin(2 * np.pi * mtof(m) * t) * np.exp(-t * 0.9)
    x *= np.minimum(1, t / 0.01)
    return stereo(x * gain / 5)

def s_drone():
    return None  # handled in the score as the cold-open bed

SFX = dict(ping=s_ping, whoosh=s_whoosh, whoosh_soft=lambda: s_whoosh(0.10, 1.3), pop=s_pop, tick=s_tick,
           stamp=s_stamp, stamp_soft=lambda: s_stamp(0.18), chime=s_chime, impact=s_impact,
           impact_soft=lambda: s_impact(0.5, soft=True), riser=s_riser, sweep=s_sweep, blip=s_blip,
           draw=s_draw, count=s_count, drop=s_drop, outro=s_outro, drone=s_drone)

def voice_track(placements, n):
    """Place the narration clips (24 kHz mono) on a 48 kHz timeline. Returns mono voice and a 0..1 ducking envelope."""
    import wave
    from scipy.signal import resample_poly
    v = np.zeros(n + SR * 12)
    for p in placements:
        with wave.open(p['file']) as w:
            sr, ch = w.getframerate(), w.getnchannels()
            a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
        if ch > 1:
            a = a.reshape(-1, ch).mean(1)
        a = resample_poly(a, SR, sr)
        i = int(p['t'] * SR)
        v[i:i + len(a)] += a
    v = hp(v[:n], 70)
    # loudness-match the voice: ~ -18 dBFS RMS while speaking
    speaking = np.abs(v) > 1e-3
    rms = np.sqrt((v[speaking] ** 2).mean()) if speaking.any() else 1
    v *= 10 ** (-18 / 20) / rms
    # ducking envelope: fast attack, slow release, on 10 ms blocks
    blk = SR // 100
    e = np.abs(v[:len(v) // blk * blk]).reshape(-1, blk).max(1)
    e = np.clip(e / (10 ** (-24 / 20)), 0, 1)
    env = np.zeros_like(e)
    for k in range(1, len(e)):
        coef = 0.45 if e[k] > env[k - 1] else 0.035
        env[k] = env[k - 1] + coef * (e[k] - env[k - 1])
    env = np.repeat(env, blk)
    env = np.pad(env, (0, n - len(env)), mode='edge')
    return v, env

def build(out_wav, cut='narrated'):
    from .render import make_timeline
    tl = make_timeline(cut)
    total = tl.total
    # The project's MUSIC setting shapes the score with scene names:
    #   intro_until  a quiet drone bed until this scene starts (a cold open), with a riser into it
    #   arp_from / arp_until  the plucked arpeggio plays between these scenes
    M = project.get().MUSIC
    names = [type(s).__name__ for s in tl.scenes]
    def start(name, default):
        return tl.starts[names.index(name)] if name in names else default
    title_t = start(M.get('intro_until'), 0.0)
    fw = start(M.get('arp_from'), tl.starts[min(2, len(tl.starts) - 1)])
    disc = start(M.get('arp_until'), tl.starts[-1])
    def arp_on(tt):
        return float(np.clip((tt - fw) / 6, 0, 1) * np.clip((disc + 4 - tt) / 6, 0, 1))
    mus = music(total, arp_on, M.get('style', 'night'))
    n = len(mus)
    T = np.arange(n) / SR
    # music level: cold open = quiet drone bed, swell into title, gentle dip under dense sections, fade out
    lvl = np.where(T < title_t, 0.35 + 0.25 * np.clip((T - (title_t - 2.5)) / 2.5, 0, 1), 1.0)
    lvl *= np.clip(T / 2.0, 0, 1)
    lvl *= np.clip((total - T) / 4.0, 0, 1)
    voice, env = voice_track(tl.placements, n) if tl.placements else (None, np.zeros(n))
    lvl *= 1 - 0.6 * env          # duck the score ~8 dB under the narrator
    mus *= lvl[:, None] * 0.85
    # cold-open drone
    dr = np.zeros(n)
    m = (T < title_t + 1) if title_t > 0 else np.zeros(n, bool)
    dr[m] = (np.sin(2 * np.pi * 73.42 * T[m]) + 0.5 * np.sin(2 * np.pi * 110 * T[m] + 0.3 * np.sin(2 * np.pi * 0.2 * T[m]))) * 0.06
    dr *= np.clip(T / 3, 0, 1) * np.clip((title_t + 0.3 - T) / 0.6, 0, 1)
    mus += stereo(dr)
    ir = reverb_ir()
    wet = np.stack([fftconvolve(mus[:, i], ir[:, i])[:n] for i in range(2)], 1)
    mix = mus * 0.75 + wet * 0.45
    # sfx bus
    sfx = np.zeros((n + SR * 6, 2))
    # Kokoro clips start with ~0.4 s of silence; small UI sounds right on a word's onset can mask it.
    onsets = np.array([p['t'] + 0.4 for p in tl.placements]) if tl.placements else np.array([])
    for (tt, name) in tl.cues():
        if name in ('pop', 'tick', 'blip') and len(onsets) and np.min(np.abs(onsets - tt)) < 0.45:
            continue
        f = SFX.get(name)
        if f is None:
            continue
        x = f()
        if x is None:
            continue
        if name == 'riser':
            tt = title_t - len(x) / SR
        if name.startswith('whoosh') and tl.placements:
            tt -= 0.55          # on the cut itself, clear of the scene's first spoken word
        i = int(tt * SR)
        if i < 0:               # a cue moved before the start of the video (a whoosh on its first frame): start it at 0
            x, i = x[-i:], 0
        sfx[i:i + len(x)] += x
    sfx = sfx[:n] * (1 - 0.7 * env)[:, None] * (0.7 if tl.placements else 1.0)
    sw = np.stack([fftconvolve(sfx[:, i], ir[:, i])[:n] for i in range(2)], 1)
    mix += sfx * 0.9 + sw * 0.18
    if voice is not None:
        room = fftconvolve(voice, ir[:, 0] * 0.5 + ir[:, 1] * 0.5)[:n]
        mix *= 0.8 if cut != 'full' else 1.0
        mix += stereo(voice * 0.95 + room * 0.035) / 1.414
    # soft limiter
    mix = np.tanh(mix * 1.1) / 1.1
    peak = np.abs(mix).max()
    mix = mix / peak * 0.89
    import wave
    data = (mix * 32767).astype(np.int16)
    with wave.open(out_wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(data.tobytes())
    print('wrote', out_wav, total)

def main(cut='narrated'):
    od = project.get().out(cut)
    os.makedirs(od, exist_ok=True)
    build(os.path.join(od, 'audio.wav'), cut)
