"""Synthesize every narration line with Kokoro-82M, then verify each clip with Whisper.

  python -m aiglainer tts            # synthesize (cached) + verify
Writes <project>/cache/<hash>.wav (24 kHz mono) and <project>/lines.json:
  [{scene, i, v, text, file, dur, heard, wer}, ...]
Clips are cached by (voice, speed, spoken text), so editing one line only re-synthesizes that line.
Exits non-zero if any line's word error rate exceeds MAX_WER, so a mispronunciation can't slip through.
"""
import hashlib, json, os, re, sys
import numpy as np
from . import project, lexicon, hosts, backend

MAX_WER = 0.12
WHISPER = 'mlx-community/whisper-large-v3-turbo'
KOKORO = 'mlx-community/Kokoro-82M-bf16'

def kokoro_voice(spec):
    """What to hand Kokoro for a voice: the id itself, or for a blend ('af_bella:0.7,af_nicole:0.3') the path of a
    voice file mixed from Kokoro's own, made once under ~/.cache/aiglainer/voices. Clips stay cached by the spec."""
    if ',' not in spec and ':' not in spec:
        return spec
    out = os.path.join(os.path.expanduser('~/.cache/aiglainer/voices'), hashlib.sha1(spec.encode()).hexdigest()[:16] + '.safetensors')
    if not os.path.exists(out):
        import mlx.core as mx
        from huggingface_hub import hf_hub_download
        packs = [(mx.load(hf_hub_download(KOKORO, f'voices/{v}.safetensors'))['voice'], w) for v, w in hosts.mix(spec)]
        mixed = sum(w * p.astype(mx.float32) for p, w in packs).astype(packs[0][0].dtype)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        mx.save_safetensors(out, {'voice': mixed})
    return out

def spoken(text, SAY):
    """What Kokoro is given: the project's SAY over the shared lexicon, in one pass (a replacement is never re-scanned)."""
    say = dict(lexicon.SAY, **SAY)
    if not say:
        return text
    pat = '|'.join(rf'\b{re.escape(k)}\b' for k in sorted(say, key=len, reverse=True))
    return re.sub(pat, lambda m: say[m.group(0)], text)

def heard_as_written(s):
    for pat, rep in lexicon.HEARD.items():
        s = re.sub(pat, rep, s, flags=re.I)
    return s

ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()

def say_int(n):
    if n < 20:
        return ONES[n]
    if n < 100:
        return TENS[n // 10] + ('' if n % 10 == 0 else ' ' + ONES[n % 10])
    return say_int(n // 100) + ' hundred' + ('' if n % 100 == 0 else ' ' + say_int(n % 100))

def say_numbers(s):
    """Whisper writes digits; the script spells them. Spell digits out so both compare alike."""
    s = re.sub(r'(\d+)%', r'\1 percent', s)
    s = re.sub(r'(\d*)\.(\d+)', lambda m: (say_int(int(m.group(1))) + ' ' if m.group(1) else '') + 'point ' + ' '.join(ONES[int(d)] for d in m.group(2)), s)
    s = re.sub(r'\d+', lambda m: say_int(int(m.group(0))), s)
    return s.replace('zero point', 'point')

def words(s):
    s = say_numbers(s.lower().replace('’', "'").replace('-', ' '))
    return re.sub(r'[^a-z ]', ' ', s.replace("'", '')).split()

def wer(ref, hyp):
    r, h = words(ref), words(heard_as_written(hyp))
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[-1] / max(1, len(r))

def main():
    P = project.get()
    N = P.narration()
    lines = []
    for sc in N.SCENES:
        for i, (v, text) in enumerate(sc['beats']):
            lines.append(dict(scene=sc.get('id', sc['scene']), i=i, v=v, text=text, say=spoken(text, getattr(N, 'SAY', {}))))
    voice = N.VOICE
    if voice in hosts.HOSTS:                     # a host's key ('bella') rather than a raw Kokoro voice id
        h = hosts.get(voice)
        voice, speed, lang = h['voice'], getattr(N, 'SPEED', h['speed']), getattr(N, 'LANG', h['lang'])
    else:
        speed, lang = N.SPEED, N.LANG
    bad = synthesize(P, lines, voice, speed, lang)
    if not bad and P.KIND == 'short':
        from . import short
        short.word_times(P, lines)
    sys.exit(1 if bad else 0)

def synthesize(P, lines, voice, speed, lang):
    """Synthesize (cached) and Whisper-check lines in place, write <project>/lines.json, return the number flagged.
    Each line is a dict with scene, i, text and say; a line may carry its own 'voice', 'speed' and 'lang'
    (another host)."""
    import soundfile as sf
    os.makedirs(P.cache, exist_ok=True)
    os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
    for l in lines:
        v, sp, lg = l.pop('voice', voice), l.pop('speed', speed), l.pop('lang', lang)
        key = hashlib.sha1(f'{v}|{sp}|{l["say"]}'.encode()).hexdigest()[:16]
        l['file'] = os.path.join('cache', key + '.wav')
        l['_voice'] = (v, sp, lg)
    todo = [l for l in lines if not os.path.exists(P.path(l['file']))]
    if todo:
        for l in todo:
            audio, sr = backend.synth(l['say'], kokoro_voice(l['_voice'][0]), l['_voice'][1], l['_voice'][2])
            sf.write(P.path(l['file']), audio, sr)
            print(f"  synthesized {l['scene']}[{l['i']}]")
    for l in lines:
        if l['_voice'][0] != voice:
            l['voice'] = l['_voice'][0]
        del l['_voice']
    # clips are named by content, so a transcript from the previous run is still valid for the same file
    prev = {}
    if os.path.exists(P.path('lines.json')):
        prev = {l['file']: l.get('heard') for l in json.load(open(P.path('lines.json')))}
    bad = 0
    for l in lines:
        a, sr = sf.read(P.path(l['file']))
        l['dur'] = round(len(a) / sr, 3)
        l['heard'] = prev.get(l['file']) or backend.transcribe(P.path(l['file']))['text'].strip()
        l['wer'] = round(wer(l['text'], l['heard']), 3)
        flag = '  <-- CHECK' if l['wer'] > MAX_WER else ''
        bad += bool(flag)
        print(f"{l['scene']:>14s}[{l['i']}] {l['dur']:5.2f}s wer {l['wer']:.2f}  {l['heard']}{flag}")
    json.dump(lines, open(P.path('lines.json'), 'w'), indent=1)
    total = sum(l['dur'] for l in lines)
    print(f'{len(lines)} lines, {total:.1f}s of speech, {bad} flagged')
    return bad
