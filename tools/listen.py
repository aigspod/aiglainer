"""Ask NVIDIA Music Flamingo about a piece of audio: a way to *listen* to a score before a person does.
A development tool only, never part of a build. The model (nvidia/music-flamingo-2601-hf, ~16 GB, NVIDIA OneWay
Noncommercial licence: fine for aigs pod, which is non-commercial) downloads from Hugging Face on first use.

  make listen F=sketches/scores/out/boundless.m4a
  make listen F=song.m4a Q="Which instrument carries the melody?" Q2="Is there a repeating motif?" START=60 DUR=90
  python tools/listen.py FILE ["question" ...] [--start S] [--dur D] [--tokens N]

What to trust (checked on our own renders, whose content we know): key, chords (often spelled enharmonically: F#
for Gb), mood and timbre are good; tempo is meaningless when there is no pulse; it misses quiet or synthetic voices;
rhythm answers are coarse (it heard 'ta... ta... taaah' as 'ta... taaah'). Ask short, specific questions.
Runs on Apple Silicon (MPS) in bf16 with two workarounds below; ~3 s to load once cached, a few seconds a question.
"""
import sys, time, subprocess, argparse
import numpy as np
import torch
from transformers import MusicFlamingoForConditionalGeneration, AutoProcessor
from transformers.models.musicflamingo import modeling_musicflamingo as mf

MODEL = "nvidia/music-flamingo-2601-hf"
MAX_SEC = 300                             # a whole 19-minute track asked for an 89 GB attention matrix; 165 s is fine
ASK = ("Describe this piece in detail: tempo, key and mode, which instrument carries the melody, "
       "the rhythm of the melodic phrases (note lengths, rests, any repeating motif), harmony, texture and mood.")

def rotary_f32(hidden_states, cos, sin):
    """The model's rotary time embedding in float32: it asks for float64, which MPS doesn't have."""
    dt = hidden_states.dtype
    x = hidden_states.float()
    cos, sin = cos.to(x), sin.to(x)
    r = cos.shape[-1]
    rot = x[..., :r] * cos + mf.rotate_half(x[..., :r]) * sin
    return torch.cat((rot, x[..., r:]), dim=-1).to(dt)

def load(path, start, dur, sr=16000):
    """Any format via ffmpeg, as mono 16 kHz float32 (what the encoder expects). The model hears at most 20 minutes."""
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + \
          ["-i", path, "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("audio"); ap.add_argument("questions", nargs="*")
    ap.add_argument("--start", type=float, default=0); ap.add_argument("--dur", type=float, default=None)
    ap.add_argument("--tokens", type=int, default=700)
    a = ap.parse_args()
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    mf.apply_rotary_time_emb = rotary_f32
    t = time.time()
    proc = AutoProcessor.from_pretrained(MODEL)
    # eager attention: MPS's fused bf16 attention kernel fails to build for the audio encoder
    model = MusicFlamingoForConditionalGeneration.from_pretrained(MODEL, dtype=torch.bfloat16,
                                                                  attn_implementation="eager").to(dev).eval()
    print(f"[loaded in {time.time() - t:.0f}s on {dev}]", file=sys.stderr)
    audio = load(a.audio, a.start, a.dur)
    if len(audio) > MAX_SEC * 16000:      # eager attention's memory grows with the square of the length
        sys.exit(f"{len(audio) / 16000:.0f} s is too long to hear at once on {dev}; "
                 f"ask about stretches of up to {MAX_SEC} s with START= and DUR=")
    for q in a.questions or [ASK]:
        conv = [{"role": "user", "content": [{"type": "text", "text": q}, {"type": "audio", "audio": audio}]}]
        inputs = proc.apply_chat_template(conv, tokenize=True, add_generation_prompt=True, return_dict=True).to(dev)
        inputs["input_features"] = inputs["input_features"].to(model.dtype)
        with torch.inference_mode():
            out = model.generate(**inputs, max_new_tokens=a.tokens, do_sample=False)
        print(f"\n### {q}\n" + proc.batch_decode(out[:, inputs.input_ids.shape[1]:], skip_special_tokens=True)[0].strip())

if __name__ == "__main__":
    main()
