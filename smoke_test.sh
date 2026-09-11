#!/usr/bin/env bash
set -euo pipefail
URL="${1:-https://www.youtube.com/watch?v=BaW_jenozKc}"
python3 -m yt_dlp --no-warnings --skip-download --print '%(extractor)s|%(title)s|%(duration)s' "$URL"
