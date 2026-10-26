"""Locating and loading a project (one paper / one video).

A project is a folder under projects/ with a `project.py` (settings, see aiglainer/template/project.py),
a narration script, scene modules, and its data. The engine never imports a specific paper's code; it
asks `get()` for the current project, chosen by the AIGLAINER_PROJECT environment variable (a name under
projects/ or a path). The project folder is put on sys.path, so its scene modules import each other plainly.

This module stays importable without skia, so the narration tools don't load the renderer.
"""
import importlib, importlib.util, os, sys

PACKAGE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(PACKAGE, 'template')

def projects_dir():
    """Where projects live: $AIGLAINER_PROJECTS, else ./projects, else the projects/ beside this checkout."""
    if os.environ.get('AIGLAINER_PROJECTS'):
        return os.path.abspath(os.environ['AIGLAINER_PROJECTS'])
    if os.path.isdir('projects'):
        return os.path.abspath('projects')
    return os.path.join(os.path.dirname(PACKAGE), 'projects')

DEFAULTS = dict(
    HUD='',                     # top-left label, lowercase mono
    CHAPTERS=[],                # chapter names; scenes refer to them by index (Scene.chapter)
    STEPS=[],                   # optional story spine shown as a tracker, e.g. ['behavior', 'cause', 'mechanism']
    CHAPTER_STEPS={},           # chapter index -> tuple of step indices lit in the tracker
    SCENE_MODULES=['scenes'],   # modules searched for scene classes by name
    FULL_CUT=None,              # optional: function returning the scene list for the un-narrated cut
    NOTES={},                   # margin notes per scene name (see aiglainer/notes.py)
    CHAPTER_TITLES={},          # scene name -> YouTube chapter title (default: the class name)
    DESCRIPTION='{chapters}\n', # YouTube description; {chapters} and {voice} are filled in
    OUTPUT_NAME='video.mp4',
    THEME={},                   # overrides for core.PAL colour tokens
    MUSIC={},                   # intro_until / arp_from / arp_until: scene names that shape the score
    THUMBNAIL=None,             # optional: function(canvas) drawing a 1280x720 thumbnail
)

class Project:
    def __init__(self, path):
        self.dir = os.path.abspath(path)
        self.name = os.path.basename(self.dir.rstrip('/'))
        spec = importlib.util.spec_from_file_location('_aiglainer_project_settings', os.path.join(self.dir, 'project.py'))
        if self.dir not in sys.path:
            sys.path.insert(0, self.dir)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.cfg = mod
        for k, v in DEFAULTS.items():
            if not hasattr(mod, k):
                setattr(mod, k, v)

    # -- paths
    def path(self, *p):
        return os.path.join(self.dir, *p)
    @property
    def data(self): return self.path('data')
    @property
    def tex(self): return self.path('tex')
    @property
    def cache(self): return self.path('cache')
    def out(self, cut=''):
        return self.path('out', cut)

    # -- content
    def narration(self):
        return importlib.import_module('narration')

    def scene_class(self, name):
        for m in self.cfg.SCENE_MODULES:
            mod = importlib.import_module(m)
            if hasattr(mod, name):
                return getattr(mod, name)
        raise KeyError(f'no scene {name!r} in {self.cfg.SCENE_MODULES}')

    def __getattr__(self, k):
        return getattr(self.cfg, k)

_current = None

def resolve(name):
    if name and os.path.isdir(name) and os.path.exists(os.path.join(name, 'project.py')):
        return name
    root = projects_dir()
    p = os.path.join(root, name or '')
    if name and os.path.exists(os.path.join(p, 'project.py')):
        return p
    have = sorted(d for d in os.listdir(root) if os.path.exists(os.path.join(root, d, 'project.py'))) if os.path.isdir(root) else []
    raise SystemExit(f'unknown project {name!r}; set AIGLAINER_PROJECT or pass -p. Projects: {", ".join(have)}')

def get():
    global _current
    if _current is None:
        _current = Project(resolve(os.environ.get('AIGLAINER_PROJECT')))
        _apply_theme(_current)
    return _current

def _apply_theme(p):
    if p.THEME and 'aiglainer.core' in sys.modules:
        sys.modules['aiglainer.core'].PAL.update(p.THEME)
