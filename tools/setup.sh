#!/usr/bin/env bash
# One-time setup (macOS, Apple Silicon): the environment, the narration fixes, and the commit guard.
#   .venv  aiglainer (editable) with rendering and narration dependencies, at the versions in uv.lock
set -euo pipefail
cd "$(dirname "$0")/.."

uv sync -q --extra tts
# The espeak-ng library bundled in espeakng_loader looks for its data one directory above where misaki
# points it, so link the data files there too.
P=$(.venv/bin/python -c "import espeakng_loader, os; print(os.path.dirname(espeakng_loader.__file__))")
for f in "$P"/espeak-ng-data/*; do ln -sf "$f" "$P/$(basename "$f")"; done
# refuse commits of media and big files (see tools/hooks/pre-commit)
git config core.hooksPath tools/hooks
echo "environment ready: .venv"
