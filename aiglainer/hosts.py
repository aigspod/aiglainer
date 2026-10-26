"""The voices that host videos and podcasts. Scripts name a host by key (`HOSTS = {'H': 'bella'}` in an episode,
`VOICE = 'bella'` in a video's narration), so changing who hosts is one word, and every host shares the lexicon.

Add a host by auditioning voices (`make voices`) and adding an entry. `lang` is Kokoro's: 'a' American, 'b' British.
"""

HOSTS = {
    'bella':   dict(voice='af_bella',   name='Bella',   lang='a', speed=1.0),
    'michael': dict(voice='am_michael', name='Michael', lang='a', speed=1.0),
    'eric':    dict(voice='am_eric',    name='Eric',    lang='a', speed=1.0),
    'nicole':  dict(voice='af_nicole',  name='Nicole',  lang='a', speed=1.0),
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
