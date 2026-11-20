"""Render the station music (aiglainer scores) and the DJ breaks / ads (Kokoro) for the hackathon radio page."""
import os, shutil, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')))   # the aiglainer root
from aiglainer import audio, backend, tts

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'audio')
os.makedirs(OUT, exist_ok=True)
FFMPEG = shutil.which('ffmpeg') or 'ffmpeg'   # `make` puts the pixi env's ffmpeg on PATH

def enc(wav, m4a, br):
    subprocess.run([FFMPEG, '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'aac', '-b:a', br, m4a], check=True)
    os.remove(wav)

MUSIC = dict(latent='analog', skip='encore', samudra='velours', deep='mysterium')
LOOP, XF = 150.0, 4.0
if 'music' in sys.argv:
    for name, style in MUSIC.items():
        x = audio.music(LOOP + XF, lambda t: 1.0, style)
        n, k = int(LOOP * audio.SR), int(XF * audio.SR)
        y = x[:n].copy()
        r = np.linspace(0, 1, k)[:, None]
        y[:k] = y[:k] * r + x[n:n + k] * (1 - r)          # seamless loop: tail fades into the head
        y = y / max(1e-9, np.abs(y).max()) * 0.89
        w = os.path.join(OUT, f'music_{name}.wav')
        sf.write(w, y, audio.SR)
        enc(w, w[:-4] + '.m4a', '112k')
        print('music', name, style)

BELLA, MICHAEL = 'af_bella:0.85,af_nicole:0.1,af_heart:0.05', 'am_michael:0.85,am_onyx:0.15'
V = dict(bella=(BELLA, 'a', 1.0), michael=(MICHAEL, 'a', 0.96), puck=('am_puck', 'a', 1.12), nicole=('af_nicole', 'a', 0.92),
         fenrir=('am_fenrir', 'a', 0.9), george=('bm_george', 'b', 1.0), heart=('af_heart', 'a', 1.05),
         eric=('am_eric', 'a', 1.1), onyx=('am_onyx', 'a', 0.95), sky=('af_sky', 'a', 1.0), emma=('bf_emma', 'b', 1.0))

CLIPS = {
    # Latent FM 101.1: synthwave, Bella
    'latent_1': [('bella', "You're locked in to Latent F M, one oh one point one. All the hits from the hidden layers. Smooth activations, all day long.")],
    'latent_2': [('bella', "That one goes out to everybody in session one. Noon to two, Eastern. Grab a coffee, open a notebook, and find me a circuit.")],
    'latent_3': [('bella', "Latent F M. Where every feature has a story. And some of them even mean just one thing.")],
    'latent_4': [('bella', "If you're just tuning in, session two starts at three, Eastern. Bring a friend. Bring a hypothesis.")],
    # The Skip 88.5: house, Puck
    'skip_1': [('puck', "Eighty eight point five, The Skip! Why go deep, when you can go straight to the output?")],
    'skip_2': [('puck', "This is The Skip, and we are running at full resolution all day long! No bottleneck! No regrets!")],
    'skip_3': [('puck', "Hackathon people, make some noise! Session two, three o'clock Eastern! Let's patch some paths!")],
    'skip_4': [('puck', "Big skip, little skip, we play them all. You're listening to The Skip!")],
    # Radio Samudra 94.7: ocean chill, Nicole
    'samudra_1': [('nicole', "Radio Samudra, ninety four point seven. Waves, warm water, and a five day window. Breathe in. Breathe out.")],
    'samudra_2': [('nicole', "Sea surface temperature is steady. The mixed layer is deep. The ocean is thinking. Probably.")],
    'samudra_3': [('nicole', "A gentle reminder from Radio Samudra. Area weight your means. The poles are smaller than they look.")],
    # Deep Path Radio 66.6: dark ambient, Fenrir
    'deep_1': [('fenrir', "Deep Path Radio. For the signals that go all the way down. Through the bottleneck. And back again.")],
    'deep_2': [('fenrir', "Some forcing takes the shortcut. Some takes the long way around. Tonight, we take the long way.")],
    'deep_3': [('fenrir', "You are still listening to Deep Path Radio. Somewhere below you, a gradient is vanishing.")],
    # Port Samudra Public Radio 1220 AM: news and talk
    'talk_news': [('george', "Good morning. This is Port Samudra Public Radio. In today's headlines: a team of climate scientists has gathered to open up a machine learned climate model and look at what's inside. Sessions run from noon to two, and from three to five, Eastern time.")],
    'talk_traffic': [('george', "Now, the traffic. Heavy congestion on the full resolution skip this morning. The deep path is moving freely, if you don't mind the bottleneck. And expect delays at the physics corrector.")],
    'talk_weather': [('michael', "And the weather. A coupled forecast today, with the ocean and the atmosphere checking in every few hours. Clear skies in the latent space, with a good chance of interpretability by late afternoon.")],
    'talk_call': [('michael', "Let's go to the phones. Caller, you're on the air."),
                  ('sky', "Hi! Long time listener. So, my probe says the ocean is reading the thermometer upside down. Is that normal?"),
                  ('michael', "Great question. Nobody knows yet. That's what today is for. Next caller."),
                  ('eric', "Yeah, hi. How many seeds is enough?"),
                  ('michael', "More than one. Always more than one. Thanks for calling.")],
    'talk_rules': [('george', "And now, a public service announcement. Report the spread, not just the mean. Quote the corrector column. And if two of your numbers are the same number, say so. Thank you.")],
    # Ads: shared by every station
    'ad_weight': [('heart', "Feeling heavy at the poles? Try Area Weight Watchers! We weight every grid cell by its true size, so the Arctic stops hogging your mean. Area Weight Watchers. It's what's inside, by latitude.")],
    'ad_mask': [('eric', "Mask Depot! Land masks. Ice masks. Masks for the grid cells you'd rather not talk about. If it isn't ocean, it isn't in your mean. Mask Depot!")],
    'ad_seed': [('emma', "At Seed Spread Savings, we never bank on a single seed. Five seeds, error bars, and a spread for every date. Seed Spread Savings. Your mean deserves company.")],
    'ad_corrector': [('onyx', "Did your result survive the physics corrector? With Corrector Insurance, you'll always know. Corrector in. Corrector out. Both columns, every time.")],
    'ad_restate': [('sky', "Restatement Realty. Is that a second finding, or the same number in a new outfit? We'll tell you, before your reviewers do.")],
    'ad_prereg': [('michael', "Ask your team lead if a preregistration sheet is right for you."),
                  ('eric', "Side effects of skipping it may include forking paths, a garden of p values, and a very long Monday.")],
}

if 'voices' in sys.argv:
    for cid, parts in CLIPS.items():
        segs = []
        for who, text in parts:
            spec, lang, speed = V[who]
            a, sr = backend.synth(text, tts.kokoro_voice(spec), speed, lang)
            segs += [a, np.zeros(int(0.35 * sr), np.float32)]
        y = np.concatenate([np.zeros(int(0.15 * sr), np.float32)] + segs)
        y = y / max(1e-9, np.abs(y).max()) * 0.9
        w = os.path.join(OUT, cid + '.wav')
        sf.write(w, y, sr)
        enc(w, w[:-4] + '.m4a', '64k')
        print('clip', cid, round(len(y) / sr, 1), 's')
