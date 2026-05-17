#!/usr/bin/env bash
set -euo pipefail

rm -rf media output .pytest_cache
find . -type d -name "__pycache__" -prune -exec rm -rf {} +

echo "Cleaned Manim render outputs and Python caches."
