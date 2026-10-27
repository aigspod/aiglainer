# Making a podcast episode

An episode is a project with `KIND = 'podcast'` in `project.py` and a script in `episode.py`. `make P=<name>` then
synthesizes and checks every line, mixes, masters to −16 LUFS and writes `out/podcast/`: the MP3 (with chapters),
`transcript.md`, `captions.srt`, `show_notes.txt`. It ends with a line-by-line Whisper check of the final mix.
`projects/lawful-pod/` is the reference episode; `lawful-pod-solo` and `lawful-pod-duo` are 3-minute pilots.
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
- **Budget ~145–165 words per minute** of finished audio, music and pauses included: ~3,700 words for 25 minutes.

## Review before building

Have the script reviewed before synthesizing: one adversarial reviewer checks every claim against the source (numbers,
hedges the source makes, simplifications that become false), another checks tone, clarity for beginners and how
well it sets up the discussion. Then listen to the whole episode once: nobody has heard it until a person has.

Sources: [Wistia: how to write a podcast script](https://wistia.com/blog/podcasting-part-2-how-to-write-a-script-with-jay-acunzo),
[NPR: writing a script in your own voice](https://www.npr.org/2023/02/17/1156597697/how-to-write-script-speech-podcast-voice),
[UF/IFAS: writing for broadcast](https://edis.ifas.ufl.edu/publication/wc193),
[helloaudio: structure for retention](https://helloaudio.fm/podcast-structure/),
[Menon et al. 2025, reflection prompts in AI-generated podcasts](https://arxiv.org/abs/2508.04787).
