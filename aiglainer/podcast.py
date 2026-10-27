"""Audio-only episodes: python -m aiglainer podcast -p <project>

A podcast project has `KIND = 'podcast'` in project.py and an `episode.py` script:

  HOSTS = {'H': 'bella'}            # role -> host (aiglainer/hosts.py); a second role makes it a conversation
  SAY = {...}                        # respellings for this episode (the shared aiglainer/lexicon.py always applies)
  SPEED = 1.0                        # optional: overrides every host's own speed
  SEGMENTS = [dict(title='The setup', music='sting', lines=[('H', 'text'), ('H', 'text', 0.8), ...]), ...]

Lines are written for roles, not people: changing HOSTS = {'H': 'michael'} re-voices the whole episode, and a line
says a host's name only as {H} (filled in from hosts.py), so nothing in the script is tied to one voice.
A line is (role, text) or (role, text, pause): pause overrides the silence before it. A role ending in '?' ('H?')
marks a question for the room: spoken as usual, and listed in the show notes' {questions}. `music` before a segment is
'theme' (the full theme, the voice coming in over its tail), 'sting' (a short chord swell between sections) or
None. A line ('~', 'chime') plays a soft two-note cue mid-segment (used before each question for the room); give
the line after a question a long pause, e.g. ('H', 'text', 2.5), so listeners can think. The outro theme follows
the last line. Talk sits on silence unless the project sets BED (a faint pad, 0..1).

Steps: synthesize + Whisper-check every line (cached, same as videos), trim each clip's silences and lay the lines
end to end with conversational gaps, score the music, master to -16 LUFS (the podcast norm), then write to
out/podcast/: <OUTPUT_NAME> (MP3 with chapters), transcript.md, captions.srt, show_notes.txt, placements.json.
Finishes by Whisper-checking the final mix line by line (aiglainer.verify_mix).
"""
import json, os, re, subprocess, wave
import numpy as np
from scipy.signal import oaconvolve, resample_poly
from . import project, tts, hosts
from .audio import SR, music, own_room, reverb_ir, stereo, hp, s_chime, env_adsr, pad_note, mtof, CHORDS
from .finish import ts, write_srt

CUT = 'podcast'
GAP = dict(same=0.38, turn=0.22, segment=0.9)    # silence before a line: same host continuing, a new host speaking
THEME = dict(theme=(11.0, 3.2), sting=(4.2, 2.4), chime=(2.4, 1.2), outro=(13.0, 0.0))   # length, how much of it the voice overlaps
CUE = '~'                                        # a line ('~', 'chime') plays a cue mid-segment
PAN = 0.12                                       # two hosts sit slightly left and right of centre

def trim(a, sr, floor_db=-42, pre=0.03, post=0.10):
    """Cut a clip's leading and trailing silence (Kokoro leaves ~0.4-0.7 s), keeping a little air."""
    e = np.abs(a)
    on = np.flatnonzero(e > e.max() * 10 ** (floor_db / 20))
    if not len(on):
        return a
    return a[max(0, on[0] - int(pre * sr)):on[-1] + int(post * sr)]

def load(path):
    with wave.open(path) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    if ch > 1:
        a = a.reshape(-1, ch).mean(1)
    return trim(a, sr), sr

def sting(dur):
    """A short swell on one chord with a chime on top: the gap between sections."""
    n = int(dur * SR)
    chord = CHORDS[1]
    e = env_adsr(n, 0.35, 0.6, 0.7, 1.8)
    x = np.zeros((n, 2))
    for j, m in enumerate(chord):
        x += stereo(pad_note(mtof(m), n, 0.42) * e * 0.11, (-0.5 + j / (len(chord) - 1)) * 0.8)
    c = s_chime(0.10)[:n]
    x[:len(c)] += c
    return x

def chime(dur):
    """Two soft bell notes: a signal that a question for the room is coming."""
    n = int(dur * SR)
    x = np.zeros((n, 2))
    for k, gain in enumerate((0.07, 0.056)):
        c = s_chime(gain)
        i = int(k * 0.16 * SR)
        x[i:i + len(c)] += c[:n - i]
    return x

def plan(P, E, lines):
    """Place every line and music cue on one timeline. Returns placements, cues [(t, kind, dur)], chapters, total."""
    rng = np.random.default_rng(7)               # a little variation in the gaps, so the rhythm isn't metronomic
    t, k, prev = 0.0, 0, None
    placements, cues, chapters = [], [], []
    for si, seg in enumerate(E.SEGMENTS):
        kind = seg.get('music')
        if kind:
            length, overlap = THEME[kind]
            start = t + (0.4 if t else 0.0)
            cues.append((start, kind, length))
            chapters.append((start, seg['title']))
            t = start + length - overlap
            prev = None
        else:
            chapters.append((t, seg['title']))
            if si:
                t += GAP['segment']
        for line in seg['lines']:
            host = line[0].rstrip('?')
            if host == CUE:                      # an inline music cue, e.g. the chime before a question for the room
                length, overlap = THEME[line[1]]
                cues.append((t + 0.45, line[1], length))
                t += 0.45 + length - overlap
                prev = None
                continue
            l = lines[k]; k += 1
            text = l['text']
            a, sr = load(P.path(l['file']))
            if len(line) > 2:
                t += line[2]
            elif prev is not None:
                t += GAP['same' if host == prev else 'turn'] + rng.uniform(-0.05, 0.05)
            placements.append(dict(t=round(t, 3), dur=round(len(a) / sr, 3), text=text, host=host, file=l['file'], seg=seg['title']))
            t += len(a) / sr
            prev = host
    cues.append((t + 0.8, 'outro', THEME['outro'][0]))
    return placements, cues, chapters, t + 0.8 + THEME['outro'][0]

def mix(P, E, placements, cues, total):
    n = int(total * SR)
    roles = list(E.HOSTS)
    pans = {h: (0.0 if len(roles) == 1 else PAN * (2 * i / (len(roles) - 1) - 1)) for i, h in enumerate(roles)}
    voice = np.zeros((n, 2), np.float32)
    mono = np.zeros(n, np.float32)
    for p in placements:
        a, sr = load(P.path(p['file']))
        a = resample_poly(a, SR, sr).astype(np.float32)
        i = int(p['t'] * SR)
        a = a[:n - i]
        mono[i:i + len(a)] += a
        voice[i:i + len(a)] += stereo(a, pans[p['host']]).astype(np.float32) / 1.414
    voice = hp(voice, 70).astype(np.float32)
    speaking = np.abs(mono) > 1e-3
    g = 10 ** (-18 / 20) / np.sqrt((mono[speaking] ** 2).mean())
    voice *= g; mono *= g
    # ducking envelope: fast attack, slow release, on 10 ms blocks (as for videos)
    blk = SR // 100
    e = np.abs(mono[:n // blk * blk]).reshape(-1, blk).max(1)
    e = np.clip(e / (10 ** (-24 / 20)), 0, 1)
    env = np.zeros_like(e)
    for k in range(1, len(e)):
        env[k] = env[k - 1] + (0.45 if e[k] > env[k - 1] else 0.02) * (e[k] - env[k - 1])
    env = np.pad(np.repeat(env, blk), (0, n - len(e) * blk), mode='edge')
    # MUSIC['style'] picks the theme and bed; a style with its own room (scores.py) goes on `dry`, past the reverb.
    # Stings and chimes stay the original pads.
    style = P.MUSIC.get('style', 'night')
    mus = np.zeros((n, 2), np.float32)
    dry = np.zeros((n, 2), np.float32)
    for (t0, kind, length) in cues:
        x = sting(length) if kind == 'sting' else chime(length) if kind == 'chime' else music(length, lambda tt: 1.0, style)
        bus = dry if own_room(style) and kind not in ('sting', 'chime') else mus
        L = len(x); T = np.arange(L) / SR
        fade = np.clip(T / 0.6, 0, 1) * np.clip((length - T) / (5.0 if kind != 'sting' else 1.6), 0, 1)
        i = int(t0 * SR)
        x = (x * fade[:, None])[:n - i]
        bus[i:i + len(x)] += x.astype(np.float32)
    mus *= (1 - 0.75 * env)[:, None] * 0.85
    dry *= (1 - 0.75 * env)[:, None] * 0.85
    bed = float(getattr(P, 'BED', 0) or 0)
    if bed:     # a steady pad under everything; ducking it would make it swell in every pause
        (dry if own_room(style) else mus)[:] += music(total, lambda tt: 0.0, style)[:n].astype(np.float32) * bed * 0.85 * np.clip(np.arange(n) / SR / 4, 0, 1)[:, None]
    ir = reverb_ir()
    wet = np.stack([oaconvolve(mus[:, c], ir[:, c])[:n] for c in range(2)], 1)
    out = mus * 0.75 + wet * 0.45 + dry + voice
    out = np.tanh(out * 1.1) / 1.1
    return out / np.abs(out).max() * 0.89

def master(wav, mp3, meta, chapters, total):
    """-16 LUFS integrated, -1.5 dBTP, MP3 with ID3 chapter frames."""
    lim = wav[:-4] + '_lim.wav'
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', wav, '-af', 'volume=6dB,alimiter=limit=0.79:attack=4:release=60:level=false',
                    '-c:a', 'pcm_s16le', lim], check=True)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', lim, '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                       capture_output=True, text=True)
    m = json.loads(r.stderr[r.stderr.rindex('{'):r.stderr.rindex('}') + 1])
    ln = (f"loudnorm=I=-16:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    md = wav[:-4] + '_meta.txt'
    esc = lambda s: re.sub(r'([=;#\\\n])', r'\\\1', s)
    rows = [';FFMETADATA1'] + [f'{k}={esc(v)}' for k, v in meta.items()]
    for (t, title), nxt in zip(chapters, [c[0] for c in chapters[1:]] + [total]):
        rows += ['[CHAPTER]', 'TIMEBASE=1/1000', f'START={int(t * 1000)}', f'END={int(nxt * 1000)}', f'title={esc(title)}']
    open(md, 'w').write('\n'.join(rows) + '\n')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', lim, '-i', md, '-map_metadata', '1', '-map_chapters', '1',
                    '-af', ln + ',aresample=44100', '-c:a', 'libmp3lame', '-b:a', '192k', '-id3v2_version', '3', mp3], check=True)
    os.remove(lim); os.remove(md)
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', mp3, '-af', 'ebur128=peak=true', '-f', 'null', '-'], capture_output=True, text=True)
    s = r.stderr[r.stderr.rindex('Integrated loudness'):]
    return re.search(r'I:\s+(-?[\d.]+) LUFS', s).group(1), re.search(r'Peak:\s+(-?[\d.]+) dBFS', s).group(1)

def mmss(t):
    t = int(t)
    return f'{t // 60}:{t % 60:02d}'

def main():
    P = project.get()
    E = __import__('importlib').import_module(getattr(P, 'EPISODE', 'episode'))
    say = getattr(E, 'SAY', {})
    H = {role: dict(hosts.get(h)) for role, h in E.HOSTS.items()}
    for h in H.values():
        h['speed'] = getattr(E, 'SPEED', h['speed'])
    names = {role: h['name'] for role, h in H.items()}
    first = H[next(iter(H))]
    lines, questions = [], []
    for seg in E.SEGMENTS:
        for i, line in enumerate(l for l in seg['lines'] if l[0] != CUE):
            host, text = line[0].rstrip('?'), line[1].format(**names)
            if line[0].endswith('?'):
                questions.append(text)
            l = dict(scene=seg['title'][:14], i=i, v=host, text=text, say=tts.spoken(text, say))
            l.update({k: H[host][k] for k in ('voice', 'speed', 'lang') if H[host][k] != first[k]})
            lines.append(l)
    if tts.synthesize(P, lines, first['voice'], first['speed'], first['lang']):
        raise SystemExit('fix the flagged lines (rephrase, or add a respelling to SAY) and run again')
    placements, cues, chapters, total = plan(P, E, lines)
    od = P.out(CUT)
    os.makedirs(od, exist_ok=True)
    out = mix(P, E, placements, cues, total)
    wav = os.path.join(od, 'audio.wav')
    with wave.open(wav, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((out * 32767).astype(np.int16).tobytes())
    meta = dict(title=getattr(P, 'TITLE', P.name), artist=getattr(P, 'ARTIST', 'the aigs pod'), album=getattr(P, 'SHOW', 'the aigs pod'),
                genre='Podcast', comment=getattr(P, 'SUMMARY', ''))
    I, TP = master(wav, os.path.join(od, P.OUTPUT_NAME), meta, chapters, total)
    # transcript, captions, show notes
    md, seg = [f'# {meta["title"]}\n'], None
    for p in placements:
        if p['seg'] != seg:
            seg = p['seg']
            md.append(f'\n## {seg}\n')
        md.append(f'**[{mmss(p["t"])}] {names[p["host"]]}:** {p["text"]}\n' if len(names) > 1 else f'[{mmss(p["t"])}] {p["text"]}\n')
    open(os.path.join(od, 'transcript.md'), 'w').write('\n'.join(md))
    write_srt(placements, os.path.join(od, 'captions.srt'))
    json.dump(placements, open(os.path.join(od, 'placements.json'), 'w'), indent=1)
    voices = ', '.join(f'{v["name"]} (Kokoro-82M {v["voice"]})' for v in H.values())
    notes = getattr(P, 'DESCRIPTION', '{chapters}\n').format(
        chapters='\n'.join(f'{mmss(t)} {title}' for t, title in chapters),
        voice=f'• Voices: {voices}, synthetic voices generated locally.\n',
        questions='\n'.join(f'{i}. {q}' for i, q in enumerate(questions, 1)))
    open(os.path.join(od, 'show_notes.txt'), 'w').write(notes)
    speech = sum(p['dur'] for p in placements)
    words = sum(len(p['text'].split()) for p in placements)
    print(f'wrote {os.path.join(od, P.OUTPUT_NAME)}  ({mmss(total)}, {speech / total:.0%} speech, '
          f'{words / speech * 60:.0f} words/min while speaking, {I} LUFS, true peak {TP} dBTP)')
    from . import verify_mix
    verify_mix.main(CUT)
