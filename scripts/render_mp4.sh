#!/usr/bin/env bash
set -euo pipefail

export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}"

SCENE="${1:-IonTrapDemo}"

manim -qh --format mp4 scenes/ion_trap_intro.py "$SCENE"
