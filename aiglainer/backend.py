"""Narration backends: Kokoro-82M (speech) and Whisper (checks), on Apple MLX or on PyTorch/CUDA.

On an Apple Silicon Mac with mlx-audio / mlx-whisper installed, this is exactly the original path
(mlx-community/Kokoro-82M-bf16, mlx-community/whisper-large-v3-turbo). Elsewhere (Linux, e.g. an NVIDIA GPU
node) it uses the reference PyTorch Kokoro (`pip install kokoro`, hexgrad/Kokoro-82M) and faster-whisper's
large-v3-turbo. Same voices, same 24 kHz output, same transcript format; audio is close to, not bit-identical
with, the Mac build. Force one with AIGLAINER_BACKEND=mlx|torch.
"""
import functools, os
import numpy as np

SAMPLE_RATE = 24000
MLX_KOKORO = 'mlx-community/Kokoro-82M-bf16'
MLX_WHISPER = 'mlx-community/whisper-large-v3-turbo'
TORCH_KOKORO = 'hexgrad/Kokoro-82M'
TORCH_WHISPER = os.environ.get('AIGLAINER_WHISPER', 'large-v3-turbo')

@functools.lru_cache(maxsize=1)
def name():
    forced = os.environ.get('AIGLAINER_BACKEND')
    if forced:
        return forced
    try:
        import mlx_audio, mlx_whisper  # noqa: F401
        return 'mlx'
    except ImportError:
        return 'torch'

def _device():
    import torch
    return 'cuda' if torch.cuda.is_available() else 'cpu'

# ---------------------------------------------------------------- speech
@functools.lru_cache(maxsize=1)
def _mlx_tts():
    from mlx_audio.tts.utils import load_model
    return load_model(MLX_KOKORO)

@functools.lru_cache(maxsize=4)
def _torch_tts(lang):
    from kokoro import KPipeline
    return KPipeline(lang_code=lang, repo_id=TORCH_KOKORO, device=_device())

def synth(text, voice, speed=1.0, lang='a'):
    """Speak text with a Kokoro voice; returns (float32 mono array, sample rate)."""
    if name() == 'mlx':
        m = _mlx_tts()
        a = np.concatenate([np.array(r.audio) for r in m.generate(text=text, voice=voice, speed=speed, lang_code=lang)])
        return a.astype(np.float32), m.sample_rate
    pipe = _torch_tts(lang)
    parts = [r.audio.detach().cpu().numpy() for r in pipe(text, voice=voice, speed=speed) if r.audio is not None]
    return np.concatenate(parts).astype(np.float32), SAMPLE_RATE

# ---------------------------------------------------------------- listening
@functools.lru_cache(maxsize=1)
def _fw():
    from faster_whisper import WhisperModel
    dev = _device()
    return WhisperModel(TORCH_WHISPER, device=dev, compute_type='float16' if dev == 'cuda' else 'int8')

def transcribe(audio, word_timestamps=False, condition_on_previous_text=True):
    """Whisper a file path or a 16 kHz float32 array. Returns mlx_whisper's shape:
    {'text': str, 'segments': [{'start', 'end', 'text', 'words': [{'word', 'start', 'end'}]}]}."""
    if name() == 'mlx':
        import mlx_whisper
        return mlx_whisper.transcribe(audio, path_or_hf_repo=MLX_WHISPER, language='en',
                                      word_timestamps=word_timestamps, condition_on_previous_text=condition_on_previous_text)
    if isinstance(audio, str):      # load + resample ourselves (faster-whisper's PyAV loader is version-fragile)
        import soundfile as sf
        from math import gcd
        from scipy.signal import resample_poly
        a, sr = sf.read(audio, dtype='float32', always_2d=True)
        a = a.mean(1)
        if sr != 16000:
            g = gcd(16000, sr)
            a = resample_poly(a, 16000 // g, sr // g).astype(np.float32)
        audio = a
    segs, _ = _fw().transcribe(audio, language='en', beam_size=5, word_timestamps=word_timestamps,
                               condition_on_previous_text=condition_on_previous_text, vad_filter=False)
    out = []
    for s in segs:
        d = dict(start=s.start, end=s.end, text=s.text)
        if word_timestamps:
            d['words'] = [dict(word=w.word, start=w.start, end=w.end) for w in (s.words or [])]
        out.append(d)
    return dict(text=''.join(s['text'] for s in out), segments=out)
