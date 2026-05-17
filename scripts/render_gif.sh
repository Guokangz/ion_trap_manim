#!/usr/bin/env bash
set -euo pipefail

export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}"

SCENE="${1:-IonTrapDemo}"

# GIF is useful for quick preview only. Use render_mp4.sh for PPT material.
manim -qm --format gif scenes/ion_trap_intro.py "$SCENE"
