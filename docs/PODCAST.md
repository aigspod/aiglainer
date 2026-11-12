# Making a podcast episode

An episode is a project with `KIND = 'podcast'` in `project.py` and a script in `episode.py`. `make P=<topic>/<kind>/<name>` then
synthesizes and checks every line, mixes, masters to −16 LUFS and writes `out/podcast/`: the MP3 (with chapters),
`transcript.md`, `captions.srt`, `show_notes.txt`. It ends with a line-by-line Whisper check of the final mix.
`projects/lawful/pods/episode/` is the reference episode; `lawful/pods/solo` and `lawful/pods/duo` are 3-minute pilots.
`MUSIC = dict(style='daylight')` in `project.py` picks the theme, outro and `BED` music from the score styles (see
docs/WORKFLOW.md, **Music**); stings and chimes keep the original pads.

## The script

```python
HOSTS = {'H': 'bella'}              # role -> host in aiglainer/hosts.py
SEGMENTS = [
    dict(title='Cold open', music=None, lines=[
        ('H', "Here's a puzzle."),
        ('H', 'So, did it learn the physics?', 0.6),        # third item: the pause before the line, seconds
    ]),
    dict(title='Welcome', music='theme', lines=[...]),     # 'theme' | 'sting' | None, played before the segment
    dict(title='Step one', music='sting', lines=[
        ...,
        ('~', 'chime'),                                     # the cue that announces a question for the room
        ('H?', 'Question for the room. ...'),               # '?' lists it in the show notes too
    ]),
]
```

- **Hosts are roles.** Lines belong to `'H'` (and `'C'` for a co-host), never to a person. `HOSTS = {'H': 'michael'}`
  re-voices the episode; a line says the host's name only as `{H}`. Hosts live in `aiglainer/hosts.py` (voice,
  name, accent, speed); audition new ones with `make voices`.
- **Pronunciation is shared.** `aiglainer/lexicon.py` teaches every host words Kokoro gets wrong ("aigs" is said
  "aygs", rhyming with "plagues"; never spelled out) and tells the Whisper check what it will hear instead. Add an
  episode-only respelling to `SAY` in `episode.py`.
- **Show notes** come from `DESCRIPTION` in `project.py`: `{chapters}`, `{questions}` and `{voice}` are filled in.

## Pacing: let the host rest

A synthetic host reads without breathing: Kokoro barely pauses between sentences inside a line, and the default gaps
between lines are short (0.38 s). Episode 28 ran at 172 words a minute while speaking, 92% of it speech, and felt
rushed. For new episodes, set in `episode.py`:

```python
HOSTS = {'H': 'bella-nicole'}       # Bella blended 70/30 with Nicole: softer and closer
SPEED = 0.92                        # unhurried
PACE = dict(sentence=0.45, same=0.7, turn=0.35, segment=1.8, question=0.5, rest=1.2)
```

- `sentence`: each line is voiced sentence by sentence with this rest between (the transcript keeps the line as one
  paragraph).
- `same`, `turn`, `segment`: the gaps before a line from the same host, a new host, a new segment.
- `question`: extra silence after any line ending in "?", so a question can land.
- `('~', 'rest')` in a segment's lines: `rest` seconds of silence where one idea ends and the next begins (or
  `('~', 'rest', 2.0)`). Use one at every turn of the story and after every reveal; that is where listeners think.

Episodes without `PACE` are laid out exactly as before.

## A story, told to one listener

A single host holds attention the way a good radio storyteller does: a story with somewhere to go, told to one
person, unhurried, in a voice that's at ease. Practitioners agree on a few things: a solo show without a firm arc
sounds ranty or unstructured; pauses are a production choice, not dead air, and give time to reflect and build
tension; and you write as if speaking to one listener wearing headphones.

- **A spine, not a list of sections.** Open on a scene or a puzzle (a model that forecasts perfectly and still
  doesn't know what's going on). Say what's at stake, follow one question through the paper, give the turn (the
  surprise), then the payoff and what it means for us. Each segment answers the question the last one raised.
- **One listener.** "You", not "listeners". "Imagine you're…" for thought experiments. Contractions. Short sentences
  with the occasional long one; one idea each.
- **Rest at the turns.** A `('~', 'rest')` after a reveal and before a new idea; a question gets its silence.
- **Ease and honesty.** Admit what's unclear, say what's surprising, keep asides warm and brief. The host is a
  synthetic voice: no invented personal anecdotes ("when I was a student…"). Stories come from the paper itself,
  how the authors set up their problem, the history of the idea, or "imagine…" scenarios.
- **Budget ~130–140 words per minute** of finished audio with `PACE` (pauses and music included): ~3,000 words for
  23 minutes.

## Writing for the ear

Listeners can't rewind or see a figure, and the voice reads literally, with no emphasis or emotion of its own.

- **Hook in the first 30 seconds.** Open on the puzzle, not the title.
- **Say where we're going, then signpost every turn** ("Step two, cause."), and tease what's next. Recap after any
  dense stretch ("Quick recap."), and recap the whole thing at the end.
- **Short sentences, one idea each.** Follow a long sentence with a short one. Everyday words; define a term the
  first time it appears and reuse the same word afterwards.
- **Emphasis comes from wording**: a short sentence on its own ("They're not."), a pause before a reveal
  (`, 0.6`), repetition of the key three words.
- **Sound like a person.** Normal transitions ("Okay.", "Here's the catch.", "Now, the physics."), the occasional
  aside and opinion ("Now the part I like most"), and admitting what's unclear.
- **No visuals.** Describe what a figure shows in words; never "as you can see". Spell out numbers and symbols.
- **Questions for the room** go at the ends of sections, never mid-explanation, and stay brief: evidence on embedded
  reflection prompts is mixed, and they can break the flow (Menon et al. 2025). Repeat them all in the wrap-up.
- **Budget ~145–165 words per minute** without `PACE` (older episodes); with it, ~130–140 (see above).

## Review before building

Have the script reviewed before synthesizing: one adversarial reviewer checks every claim against the source (numbers,
hedges the source makes, simplifications that become false), another checks tone, clarity for beginners and how
well it sets up the discussion. The ear reviewer also checks:

- Is there a hook in the first 30 seconds, and one question carried through to a payoff?
- Does it talk to one listener ("you"), with no invented personal anecdotes?
- Is there a `('~', 'rest')` at every turn and after every reveal, and does each question get its silence?
- Words per minute: with `PACE`, under ~140 of finished audio. Then listen to the whole episode once: nobody has heard it until a person has.

Sources: [Wistia: how to write a podcast script](https://wistia.com/blog/podcasting-part-2-how-to-write-a-script-with-jay-acunzo),
[NPR: writing a script in your own voice](https://www.npr.org/2023/02/17/1156597697/how-to-write-script-speech-podcast-voice),
[UF/IFAS: writing for broadcast](https://edis.ifas.ufl.edu/publication/wc193),
[helloaudio: structure for retention](https://helloaudio.fm/podcast-structure/),
[Menon et al. 2025, reflection prompts in AI-generated podcasts](https://arxiv.org/abs/2508.04787),
[Message Heard: solocasts](https://messageheard.com/mediahub/tag/Solocast),
[CMB: radio shows need more pauses](https://cmbonline.org/on-air/radio-shows-need-more-pauses/),
[CBC Doc Project: 16 tips for writing for radio](https://www.cbc.ca/radio/docproject/blog/the-craft-of-writing-for-radio-16-tips-from-a-veteran-script-writer-1.3562474),
[ArtsHub: creating intimacy in an audio story](https://www.artshub.co.uk/news/features/how-do-we-create-intimacy-in-an-audio-story-259145-1290957/).
