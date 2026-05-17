#!/usr/bin/env bash
set -euo pipefail

SCENES=(
  RodToRadialPotential
  PotentialToSaddle
  DrivenSaddleComparison
  PseudopotentialConfinement
)

HQ_DIR="output/ppt_hq"
LIST_FILE="$HQ_DIR/full_video_list.txt"
OUTPUT="$HQ_DIR/IonTrap_FullTalk_PPT_HQ.mp4"

mkdir -p "$HQ_DIR"

for SCENE in "${SCENES[@]}"; do
  bash scripts/render_ppt_hq.sh "$SCENE"
done

: > "$LIST_FILE"
for SCENE in "${SCENES[@]}"; do
  FILE="$HQ_DIR/${SCENE}_PPT_HQ.mp4"
  if [[ ! -f "$FILE" ]]; then
    echo "Missing expected file: $FILE" >&2
    exit 1
  fi
  printf "file '%s'\n" "$(realpath "$FILE")" >> "$LIST_FILE"
done

ffmpeg -y -f concat -safe 0 -i "$LIST_FILE" \
  -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -r 30 \
  "$OUTPUT"

echo "Full video written to: $OUTPUT"
