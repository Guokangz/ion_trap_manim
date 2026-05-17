#!/usr/bin/env bash
set -euo pipefail

export XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}"

FORMAT="mp4"
QUALITY="-qh"
SCENE_FILE="scenes/ion_trap_intro.py"

if [ "$#" -gt 0 ]; then
  SCENES=("$@")
else
  # Development/default review list. This can include optional scenes.
  SCENES=(
    RodToRadialPotential
    PotentialToSaddle
    StaticSaddleEscape
    DrivenSaddleComparison
    PseudopotentialConfinement
  )
fi

for scene in "${SCENES[@]}"; do
  manim "$QUALITY" --format "$FORMAT" "$SCENE_FILE" "$scene"
done
