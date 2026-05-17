#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -gt 0 ]; then
  SCENES=("$@")
else
  # Formal PPT default list.
  SCENES=(
    RodToRadialPotential
    PotentialToSaddle
    DrivenSaddleComparison
    PseudopotentialConfinement
  )
fi

for scene in "${SCENES[@]}"; do
  bash scripts/render_ppt_hq.sh "$scene"
done
