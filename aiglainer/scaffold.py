"""python -m aiglainer new <topic>/videos/<name> ["Paper Title"]  ->  projects/<topic>/videos/<name>/, copied from aiglainer/template/.

The template is a complete four-scene video (title, question, method with an equation and a data-driven chart,
takeaway) with narration, a margin note and a thumbnail, so `make P=<name>` works straight away; then
replace its content scene by scene. See projects/AGENTS.md and docs/NEW_VIDEO.md.
"""
import os, re, shutil
from .project import TEMPLATE

SKIP = {'cache', 'out', '__pycache__', 'tex', 'lines.json'}

def main(name=None, title=None):
    part = r'[a-z0-9][a-z0-9_-]*'
    if not name or not re.fullmatch(f'{part}/videos/{part}', name):
        raise SystemExit('usage: python -m aiglainer new <topic>/videos/<name> ["Paper Title"]   (e.g. sparse-probing/videos/main; '
                         'lowercase letters, digits, - or _). The template is a video; for a short or a podcast, see projects/AGENTS.md')
    # new projects go to $AIGLAINER_PROJECTS, else ./projects in the current directory
    root = os.path.abspath(os.environ.get('AIGLAINER_PROJECTS') or 'projects')
    src, dst = TEMPLATE, os.path.join(root, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit(f'{dst} already exists')
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])
    topic = name.split('/')[0]
    title = title or topic.replace('-', ' ').replace('_', ' ').title()
    slug = name.replace('/videos/', '-')       # __NAME__ goes into file names and the HUD
    for root, _, files in os.walk(dst):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(('.py', '.txt', '.md')):
                s = open(p).read()
                open(p, 'w').write(s.replace('__NAME__', slug).replace('__TITLE__', title))
    print(f'created {dst}\nnext:  make P={name}        (builds the template video as a smoke test)\n       then follow docs/NEW_VIDEO.md; projects/AGENTS.md says how to commit it')
