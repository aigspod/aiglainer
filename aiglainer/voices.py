"""Audition narrator voices: python -m aiglainer voices [voice ...]

Reads one representative line from <project>/voice_samples/sample.txt (a line with the paper's hard words),
has each Kokoro-82M voice read it, Whisper-checks every clip, and writes voice_samples/index.html with a
player per voice. Open the page, listen, then set VOICE in the project's narration.py.
"""
import html, json, os, re, subprocess
import numpy as np
from . import project
from .tts import wer

DEFAULT = ['af_heart', 'af_bella', 'af_nicole', 'af_kore', 'am_michael', 'am_fenrir', 'am_puck', 'bf_emma', 'bm_george', 'bm_fable']
ACCENT = dict(a='American', b='British')
GENDER = dict(f='female', m='male')

def main(*voices):
    import soundfile as sf
    import mlx_whisper
    from mlx_audio.tts.utils import load_model
    P = project.get()
    D = P.path('voice_samples')
    os.makedirs(D, exist_ok=True)
    sample = os.path.join(D, 'sample.txt')
    if not os.path.exists(sample):
        raise SystemExit(f'write one representative narration line to {sample} first')
    text = open(sample).read().strip()
    model = load_model('mlx-community/Kokoro-82M-bf16')
    rows = []
    for v in voices or DEFAULT:
        a = np.concatenate([np.array(r.audio) for r in model.generate(text=text, voice=v, speed=1.0, lang_code=v[0])])
        wav = os.path.join(D, f'kokoro_{v}.wav')
        sf.write(wav, a, model.sample_rate)
        m4a = wav[:-4] + '.m4a'
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-c:a', 'aac', '-b:a', '160k', m4a], check=True)
        heard = mlx_whisper.transcribe(wav, path_or_hf_repo='mlx-community/whisper-large-v3-turbo', language='en')['text'].strip()
        os.remove(wav)
        e = wer(text, heard)
        rows.append(dict(voice=v, dur=round(len(a) / model.sample_rate, 1), wer=round(e, 3), heard=heard))
        print(f'{v:12s} {rows[-1]["dur"]:5.1f}s  word errors {e * 100:3.0f}%  {heard}')
    json.dump(rows, open(os.path.join(D, 'voices.json'), 'w'), indent=1)
    items = ''
    for i, r in enumerate(rows, 1):
        v = r['voice']
        name = v.split('_', 1)[1].title()
        kind = f"{ACCENT.get(v[0], v[0])} · {GENDER.get(v[1], v[1])}"
        items += (f'<div class="v"><div class="n">{i:02d}</div><div class="m"><b>{name}</b> <code>{v}</code>'
                  f'<span>{kind} · {r["dur"]}s · Whisper word errors {r["wer"] * 100:.0f}%</span></div>'
                  f'<audio controls preload="none" src="kokoro_{v}.m4a"></audio></div>\n')
    open(os.path.join(D, 'index.html'), 'w').write(f'''<!doctype html><meta charset="utf-8"><title>Narrator voices</title>
<style>body{{font:16px -apple-system,system-ui,sans-serif;background:#161724;color:#efe5d6;max-width:880px;margin:40px auto;padding:0 16px}}
h1{{font:400 30px Georgia,serif}} p{{color:#aaa0ad;line-height:1.5}} code{{color:#e3a75a;font-size:13px}}
.v{{display:flex;gap:16px;align-items:center;padding:12px 0;border-bottom:1px solid #2e2f45;flex-wrap:wrap}}
.n{{font:600 14px ui-monospace,monospace;color:#e3a75a;width:24px}} .m{{flex:1;min-width:260px}} .m span{{display:block;color:#aaa0ad;font-size:14px}}
audio{{width:300px}}</style>
<h1>Pick a narrator</h1><p>Each Kokoro-82M voice reads the same line, generated locally. Set <code>VOICE</code> in narration.py.</p>
<p><i>“{html.escape(text)}”</i></p>{items}''')
    print(os.path.join(D, 'index.html'))
