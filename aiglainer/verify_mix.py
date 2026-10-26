"""Check the final mix (after `finish`): transcribe it with Whisper and compare against the script and planned timings.

  python -m aiglainer verify
Transcribes each line's window of the mix on its own, then reports word error rate and how far the first
heard word is from the planned start. Lines that look wrong are listed.
"""
import json, os, sys
import mlx_whisper
from .tts import words, wer
from . import project

def main(cut='narrated'):
    """Whisper each line's window of the final mix separately: long-form transcription over music can
    loop or drop words, which would hide real problems or invent fake ones."""
    import subprocess, tempfile
    import numpy as np
    P = project.get()
    path = os.path.join(P.out(cut), P.OUTPUT_NAME)
    placements = json.load(open(os.path.join(P.out(cut), 'placements.json')))
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, 'mix.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', path, '-ac', '1', '-ar', '16000', wav], check=True)
    import soundfile as sf
    audio, sr = sf.read(wav)
    errs, nwords, worst = 0, 0, 0.0
    def listen(p, lead_s):
        a = int(max(0, p['t'] - lead_s) * sr)
        b = int((p['t'] + p['dur'] + 0.15) * sr)
        res = mlx_whisper.transcribe(audio[a:b].astype(np.float32), path_or_hf_repo='mlx-community/whisper-large-v3-turbo',
                                     language='en', word_timestamps=True, condition_on_previous_text=False)
        lead = p['t'] - a / sr
        # keep words after the previous line ended (Whisper often stamps a first word early, into the silence)
        k = placements.index(p)
        prev_end = (placements[k - 1]['t'] + placements[k - 1]['dur'] - 0.2) if k else 0.0
        cut = max(0.0, prev_end - a / sr)
        ws = [w for s in res['segments'] for w in s.get('words', []) if w['end'] > cut]
        heard = ''.join(w['word'] for w in ws).strip()
        off = (ws[0]['start'] - lead) if ws else float('nan')
        return wer(p['text'], heard), heard, off, ws

    errs, nwords, worst = 0, 0, 0.0
    for p in placements:
        # a second of lead-in; if that isn't word-perfect, retry with more context (Whisper drops a lone
        # opening word like "Limits." in tight windows even when it is plainly audible)
        e, heard, off, ws = listen(p, 1.0)
        if e > 0:
            e2, heard2, off2, ws2 = listen(p, 6.0)
            if e2 < e:
                e, heard, off, ws = e2, heard2, off2, ws2
        n = len(words(p['text']))
        errs += e * n; nwords += n
        if ws and off > -0.5:
            worst = max(worst, abs(off))
        if e > 0.12 or not ws or off > 0.8:
            print(f'  {p["t"]:6.1f}s  wer {e:.2f}  start {off:+.2f}s  heard: {heard}')
    print(f'{len(placements)} lines, mix WER {errs / nwords:.3f} over {nwords} words, worst late start {worst:.2f}s')


