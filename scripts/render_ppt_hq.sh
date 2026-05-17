#!/usr/bin/env bash
set -euo pipefail

SCENE="${1:-RodToRadialPotential}"
SRC_FILE="scenes/ion_trap_intro.py"
MEDIA_DIR="output"
HQ_DIR="output/ppt_hq"

mkdir -p "$HQ_DIR"

XDG_CACHE_HOME="${XDG_CACHE_HOME:-/tmp}" manim -qh --fps 30 --media_dir "$MEDIA_DIR" "$SRC_FILE" "$SCENE"

INPUT="$(find "$MEDIA_DIR/videos" -name "${SCENE}.mp4" | sort | tail -n 1)"

if [[ -z "$INPUT" ]]; then
    echo "Could not find rendered MP4 for scene: $SCENE" >&2
    exit 1
fi

OUTPUT="$HQ_DIR/${SCENE}_PPT_HQ.mp4"

ffmpeg -y -i "$INPUT" \
    -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p \
    "$OUTPUT"

echo "PPT high-quality video written to: $OUTPUT"
