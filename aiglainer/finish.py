"""Mux video + audio, normalize loudness, and write captions and the YouTube description.

  python -m aiglainer finish --cut narrated
Reads <project>/out/<cut>/video_noaudio.mp4 and audio.wav, writes to the same folder:
  <OUTPUT_NAME>             H.264 + AAC, -14 LUFS integrated (YouTube's reference), -1.5 dBTP
  captions.srt              from the narration script and its exact placements (narrated cut only)
  placements.json           where each narration line starts, for tools/verify_mix.py
  youtube_description.txt   description with chapters computed from the timeline
"""
import json, os, re, subprocess
from .render import make_timeline
from . import project

def ts(t, sep=','):
    ms = int(round(t * 1000))
    return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}{sep}{ms % 1000:03d}'

def caption_chunks(text, maxlen=84):
    """Split a line into caption-sized pieces at sentence, then clause, boundaries."""
    parts = re.split(r'(?<=[.?!])\s+', text)
    out = []
    for p in parts:
        while len(p) > maxlen:
            cut = max(p.rfind(sep, 0, maxlen) for sep in (', ', '; ', ': '))
            if cut < 20:
                cut = p.rfind(' ', 0, maxlen)
            out.append(p[:cut + 1].strip())
            p = p[cut + 1:].strip()
        if p:
            out.append(p)
    return out

def write_srt(placements, path):
    n, rows = 0, []
    for p in placements:
        chunks = caption_chunks(p['text'])
        total = sum(len(c) for c in chunks)
        t = p['t']
        for c in chunks:
            d = p['dur'] * len(c) / total
            n += 1
            rows.append(f'{n}\n{ts(t)} --> {ts(t + d)}\n{c}\n')
            t += d
    open(path, 'w').write('\n'.join(rows))

def loudnorm_filter(audio):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', audio, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    return (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")

def main(cut='narrated'):
    P = project.get()
    od = P.out(cut)
    tl = make_timeline(cut)
    # chapters: first scene of each run of scenes with the same title
    chapters = []
    for s, st in zip(tl.scenes, tl.starts):
        t = int(st)
        chapters.append(f'{t // 60}:{t % 60:02d} {P.CHAPTER_TITLES.get(type(s).__name__, type(s).__name__)}')
    voice = ''
    if tl.placements:
        vname = P.narration().VOICE.split('_', 1)[-1].title()      # af_bella -> Bella
        voice = f'• Narration: Kokoro-82M ("{vname}"), a synthetic voice generated locally.\n'
    open(os.path.join(od, 'youtube_description.txt'), 'w').write(P.DESCRIPTION.format(chapters='\n'.join(chapters), voice=voice))
    if tl.placements:
        write_srt(tl.placements, os.path.join(od, 'captions.srt'))
        json.dump(tl.placements, open(os.path.join(od, 'placements.json'), 'w'), indent=1)
    wav = os.path.join(od, 'audio.wav')
    # Pre-limit with headroom so loudnorm can stay in linear mode (a pure gain, no pumping).
    lim = os.path.join(od, 'audio_lim.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'volume=6dB,alimiter=limit=0.79:attack=4:release=60:level=false',
                    '-c:a', 'pcm_s16le', lim], check=True)
    out = os.path.join(od, P.OUTPUT_NAME)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', os.path.join(od, 'video_noaudio.mp4'), '-i', lim]
    subs = ['-i', os.path.join(od, 'captions.srt')] if tl.placements else []
    cmd += subs + ['-map', '0:v', '-map', '1:a'] + (['-map', '2:s', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng'] if subs else [])
    cmd += ['-c:v', 'copy', '-af', loudnorm_filter(lim) + ',aresample=48000',
            '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', out, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    summary = r.stderr[r.stderr.rindex('Integrated loudness'):]
    I = re.search(r'I:\s+(-?[\d.]+) LUFS', summary).group(1)
    P = re.search(r'Peak:\s+(-?[\d.]+) dBFS', summary).group(1)
    print(f'wrote {out}  ({tl.total:.1f}s, {I} LUFS, true peak {P} dBTP)')
