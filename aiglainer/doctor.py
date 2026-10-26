"""Check (and where possible fix) a machine for building videos: python -m aiglainer doctor

Reports, in order: platform, command-line tools, rendering libraries, narration libraries, spaCy's English model,
espeak-ng's data path (fixed automatically: the espeakng_loader wheel from PyPI looks one directory too high),
and whether the speech models are already downloaded. Exits non-zero if something required for rendering is
missing; narration problems are reported but only matter for narrated builds.
"""
import importlib, os, platform, shutil, subprocess, sys

OK, WARN, BAD = '  ok ', ' warn', '  !! '

def line(mark, what, detail=''):
    print(f'{mark} {what:38s} {detail}')

def check_import(name):
    try:
        m = importlib.import_module(name)
        return True, getattr(m, '__version__', '')
    except Exception as e:                           # noqa: BLE001 - report anything
        return False, f'{type(e).__name__}: {e}'.splitlines()[0][:90]

def espeak_fix():
    """Return (ok, detail). Symlink espeak-ng's data where the bundled library looks, if needed."""
    try:
        import espeakng_loader
    except ImportError:
        return False, 'espeakng_loader missing'
    pkg = os.path.dirname(espeakng_loader.__file__)
    data = os.path.join(pkg, 'espeak-ng-data')
    if not os.path.isdir(data) or os.path.exists(os.path.join(pkg, 'phontab')):
        return True, 'nothing to fix'
    try:
        from misaki import espeak
        class T: text = 'Xyzzqrth'; tag = 'NN'
        espeak.EspeakFallback(british=False)(T())
        return True, 'works as installed'
    except Exception:                                # noqa: BLE001
        pass
    for f in os.listdir(data):
        dst = os.path.join(pkg, f)
        if not os.path.exists(dst):
            os.symlink(os.path.join(data, f), dst)
    return True, f'fixed: linked espeak-ng data into {pkg}'

def hf_cached(repo):
    root = os.path.expanduser(os.environ.get('HF_HUB_CACHE') or os.path.join(os.environ.get('HF_HOME', '~/.cache/huggingface'), 'hub'))
    return os.path.isdir(os.path.join(root, 'models--' + repo.replace('/', '--'), 'snapshots'))

def main():
    bad = False
    print('platform')
    mac = sys.platform == 'darwin' and platform.machine() == 'arm64'
    line(OK if mac else WARN, 'macOS on Apple Silicon', platform.platform() + ('' if mac else '  (narration needs mlx: Apple Silicon only)'))
    py = sys.version_info
    line(OK if py >= (3, 11) else BAD, 'Python >= 3.11', sys.version.split()[0] + f'  ({sys.executable})')
    bad |= py < (3, 11)

    print('tools')
    for tool, why in (('ffmpeg', 'encoding, required'), ('tectonic', 'equations; only if eqs.py changes')):
        p = shutil.which(tool)
        line(OK if p else (BAD if tool == 'ffmpeg' else WARN), tool, p or f'not found ({why})')
        bad |= tool == 'ffmpeg' and not p

    print('rendering')
    for m in ('aiglainer', 'skia', 'numpy', 'scipy', 'pymupdf', 'PIL', 'matplotlib'):
        ok, v = check_import(m)
        line(OK if ok else BAD, m, v)
        bad |= not ok
    fonts = os.path.exists('/System/Library/Fonts/SFNS.ttf')
    line(OK if fonts else WARN, 'SF Pro (glyph fallback)', 'found' if fonts else 'missing: Greek/arrows may not render')

    print('narration')
    narr = True
    for m in ('mlx', 'mlx_audio', 'mlx_whisper', 'misaki', 'spacy', 'soundfile', 'torch'):
        ok, v = check_import(m)
        line(OK if ok else WARN, m, v)
        narr &= ok
    ok, v = check_import('en_core_web_sm')
    line(OK if ok else WARN, "spaCy model en_core_web_sm", v if ok else 'missing: see README, "Install"')
    narr &= ok
    if narr:
        ok, detail = espeak_fix()
        line(OK if ok else WARN, 'espeak-ng data', detail)
    for repo, size in (('mlx-community/Kokoro-82M-bf16', '~340 MB'), ('mlx-community/whisper-large-v3-turbo', '~1.5 GB')):
        line(OK if hf_cached(repo) else ' info', repo, 'downloaded' if hf_cached(repo) else f'downloads on first narration run ({size})')

    print()
    if bad:
        print('Rendering prerequisites are missing (marked !!).')
        sys.exit(1)
    print('Ready to render.' + (' Narration ready too.' if narr else ' Narration not set up: narrated builds will fail at `make narration`.'))
