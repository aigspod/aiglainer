# Making a short (YouTube Shorts, TikTok)

A short is a project with `KIND = 'short'`: a 1080×1920, 60 fps video of about 30–60 s, built with `make P=<name>`
(narration, video, audio at −14 LUFS, line-by-line verify, and safe-zone sheets in `out/narrated/qa/safe_*.png`).
`projects/lawful-short-*` are the reference samples (radar, twice, pattern with Bella; probes, forbids with Michael).

```python
# project.py
KIND = 'short'
SOURCES = ['lawful']                      # reuse that project's scenes, data/ and tex/
SCENE_MODULES = ['shortscenes', 'scenes3']
HUD = 'the aigs pod  ·  lawful'           # small line at the top
CITE = 'chen, parker & arora · arxiv 2607.28672'
DESCRIPTION = '...caption and hashtags...'

# narration.py
VOICE = 'bella'
SCENES = [
    dict(scene='Spectrograms', id='SpecA', crop=(40, 310, 740, 440), headline='Can a network learn the *Doppler* effect?',
         beats=[(0.4, 'Can a neural network learn the Doppler effect, without ever being told about it?'), ...]),
    dict(scene='TwiceWrong', headline='Same *slope*, same score', beats=[...]),   # a native vertical scene
]
```

- **Only the centre column matters.** Tall phones crop ~100 px off each side, the app's icons cover the top, its
  Like/Comment/Share column the right, and its handle, description and comment bar the bottom. So everything sits in
  `short.SAFE` (x 140–860, y 290–1400 of 1080×1920); a dim, blurred copy of the visual fills the rest so the frame
  isn't empty. Check `safe_*.png`: nothing that matters in the red. (Learned from a real phone screenshot.)
- **Make it dense and vertical.** One big thing at a time, filling the column:
  - `crop=(x, y, w, h)` shows one region of a 16:9 scene, enlarged. Crop to a chart or panel, never the whole frame.
  - `crop=[(v, rect), ...]` is a camera: it holds each view and moves to the next, arriving at authored time `v`
    (e.g. in on one heatmap, across to the other, back out).
  - `stack=[rect, rect]` shows regions together, side by side or stacked, whichever is bigger (radar vs model,
    circuit vs complement).
  - `vstart` starts a scene partway in, so the first frame of a short already shows something (the hook frame).
  - `make preview P=lawful SCENE=Fig4a T="20"` shows the coordinates. Give each reuse of a scene its own `id`.
- **Native scenes** (`vertical = True`) draw in a 720×700 box with their own origin (see `projects/lawful-short-*/shortscenes.py`).
  Use them when an idea has no good 16:9 picture (a horizontal bar chart, for instance, becomes columns). Big type:
  labels ≥ 19 px, numbers ≥ 28 px. Label illustrations as such.
- **Voice and music.** `VOICE = 'michael'` (any host in `aiglainer/hosts.py`). `MUSIC = dict(style='dawn')` picks the
  score: 'night' (the default: minor ninths, 96 bpm), 'dawn' (brighter major progression, 112 bpm, soft
  pulse), or one after music the pod loves: 'daylight' (strings over a lament bass, after Richter), 'encore' (soft
  solo piano, after Jarrett), 'analog' (mellow piano house, after Martin Roth), 'silencia' (guitar swells and cello)
  or 'mysterium' (strings and a wordless choir), both after Hammock. Styles live in `aiglainer/audio.py` `STYLES`
  (the last five in `aiglainer/scores.py`).
- **Captions are burned in**, a few words at a time with the spoken word in amber, timed from Whisper's word
  timestamps (computed by `make narration`). Many people watch with the sound off.
- **Writing:** one idea per short; the hook in the first line (a question or a surprise, not a title); ~100–130 words;
  end on a question. Same rigour as the long video: hypotheticals said as such, numbers from the paper's tables.
- **Uploading:** turn on the platform's AI-generated/synthetic-media label (the narration is a synthetic voice), and
  paste `youtube_description.txt` as the caption.
