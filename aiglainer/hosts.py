"""The voices that host videos and podcasts. Scripts name a host by key (`HOSTS = {'H': 'bella'}` in an episode,
`VOICE = 'bella'` in a video's narration), so changing who hosts is one word, and every host shares the lexicon.

Add a host by auditioning voices (`make voices`) and adding an entry. `lang` is Kokoro's: 'a' American, 'b' British.
A `voice` can blend Kokoro voices with weights, 'af_bella:0.7,af_nicole:0.3' (`tts.kokoro_voice` builds the mix from
Kokoro's own voice files, so nothing extra is committed); `make voices af_bella:0.6,af_nicole:0.4` auditions a mix.
"""

HOSTS = {
    'bella':   dict(voice='af_bella',   name='Bella',   lang='a', speed=1.0),
    'michael': dict(voice='am_michael', name='Michael', lang='a', speed=1.0),
    'eric':    dict(voice='am_eric',    name='Eric',    lang='a', speed=1.0),
    'nicole':  dict(voice='af_nicole',  name='Nicole',  lang='a', speed=1.0),
    # Bella, softer and closer: 70% Bella, 30% Nicole. Still introduced as Bella on air.
    'bella-nicole': dict(voice='af_bella:0.7,af_nicole:0.3', name='Bella', lang='a', speed=1.0),
    'fable':   dict(voice='bm_fable',   name='Fable',   lang='b', speed=1.0),
    'lewis':   dict(voice='bm_lewis',   name='Lewis',   lang='b', speed=1.0),
    'emma':    dict(voice='bf_emma',    name='Emma',    lang='b', speed=1.0),
}

def get(h):
    """A host by key, or a dict given inline (voice, name, lang, speed) for one-off voices."""
    if isinstance(h, dict):
        return dict(dict(name=h['voice'].split('_', 1)[-1].title(), lang=h['voice'][0], speed=1.0), **h)
    if h not in HOSTS:
        raise SystemExit(f'unknown host {h!r}; known: {", ".join(HOSTS)} (or add one to aiglainer/hosts.py)')
    return HOSTS[h]

def mix(spec):
    """[(kokoro voice id, weight)] for a voice or a blend like 'af_bella:0.7,af_nicole:0.3'; weights sum to 1."""
    parts = [(v.split(':')[0].strip(), float(v.split(':')[1]) if ':' in v else 1.0) for v in spec.split(',')]
    total = sum(w for _, w in parts)
    return [(v, w / total) for v, w in parts]

def credit(spec):
    """How a description names the voice: '"Bella"', or '"Bella" blended 70/30 with "Nicole"'."""
    names = [(f'"{v.split("_", 1)[-1].title()}"', round(w * 100)) for v, w in mix(spec)]
    if len(names) == 1:
        return names[0][0]
    return f'{names[0][0]} blended {"/".join(str(w) for _, w in names)} with {" and ".join(n for n, _ in names[1:])}'

def label(spec):
    """The Kokoro ids for show notes: 'af_bella', or 'af_bella 70% + af_nicole 30%'."""
    m = mix(spec)
    return m[0][0] if len(m) == 1 else ' + '.join(f'{v} {round(w * 100)}%' for v, w in m)
