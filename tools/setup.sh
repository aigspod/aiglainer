#!/usr/bin/env bash
# One-time setup (macOS 14.5+, Apple Silicon): the pixi environment and the commit guard.
#   .pixi/envs/default  python, ffmpeg, tectonic, the rendering and narration stacks, and aiglainer (editable),
#                       at the versions in pixi.lock
set -euo pipefail
cd "$(dirname "$0")/.."
command -v pixi >/dev/null || { echo "install pixi first: https://pixi.sh"; exit 1; }
pixi install
# refuse commits of media and big files (see tools/hooks/pre-commit)
git config core.hooksPath tools/hooks
echo "environment ready: .pixi/envs/default"
