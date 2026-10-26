#!/usr/bin/env bash
# Create the two virtual environments used by the build (macOS, Apple Silicon).
#   .venv      rendering: skia, numpy, scipy, pymupdf
#   .venv-tts  narration: Kokoro-82M via mlx-audio, Whisper via mlx-whisper
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d .venv ] || uv venv -q .venv --python 3.12
uv pip install -q --python .venv/bin/python -r requirements.txt
uv pip install -q --python .venv/bin/python --no-deps -e .          # the explainer package, editable

[ -d .venv-tts ] || uv venv -q .venv-tts --python 3.12
uv pip install -q --python .venv-tts/bin/python -r requirements-tts.txt
uv pip install -q --python .venv-tts/bin/python --no-deps -e .
# misaki needs spaCy's small English model; its own auto-download fails under uv, so install the wheel.
uv pip install -q --python .venv-tts/bin/python \
  "en_core_web_sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl"
# The espeak-ng library bundled in espeakng_loader looks for its data one directory above where misaki
# points it, so link the data files there too.
P=$(.venv-tts/bin/python -c "import espeakng_loader, os; print(os.path.dirname(espeakng_loader.__file__))")
for f in "$P"/espeak-ng-data/*; do ln -sf "$f" "$P/$(basename "$f")"; done
# refuse commits of media and big files (see tools/hooks/pre-commit)
git config core.hooksPath tools/hooks
echo "environments ready"
