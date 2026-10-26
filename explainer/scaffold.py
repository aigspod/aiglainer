"""python -m explainer new <name> ["Paper Title"]  ->  projects/<name>/, copied from explainer/template/.

The template is a complete four-scene video (title, question, method with an equation and a data-driven chart,
takeaway) with narration, a margin note and a thumbnail, so `make P=<name>` works straight away; then
replace its content scene by scene. See docs/NEW_VIDEO.md.
"""
import os, re, shutil
from .project import TEMPLATE

SKIP = {'cache', 'out', '__pycache__', 'tex', 'lines.json'}

def main(name=None, title=None):
    if not name or not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', name):
        raise SystemExit('usage: python -m explainer new <name> ["Paper Title"]   (name: lowercase letters, digits, - or _)')
    # new projects go to $EXPLAINER_PROJECTS, else ./projects in the current directory
    root = os.path.abspath(os.environ.get('EXPLAINER_PROJECTS') or 'projects')
    src, dst = TEMPLATE, os.path.join(root, name)
    os.makedirs(root, exist_ok=True)
    if os.path.exists(dst):
        raise SystemExit(f'{dst} already exists')
    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])
    title = title or name.replace('-', ' ').replace('_', ' ').title()
    for root, _, files in os.walk(dst):
        for f in files:
            p = os.path.join(root, f)
            if f.endswith(('.py', '.txt', '.md')):
                s = open(p).read()
                open(p, 'w').write(s.replace('__NAME__', name).replace('__TITLE__', title))
    print(f'created {dst}\nnext:  make P={name}        (builds the template video as a smoke test)\n       then follow docs/NEW_VIDEO.md')
