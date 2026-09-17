#!/bin/sh
# Renders every visual piece to review/png at full export size, with the
# safe-zone guides hidden, then regenerates review/index.html.
# Run from the repo root. Needs the bundled Chromium only.
set -e
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
mkdir -p review/png
for f in $(find variants templates motion -name "*.html" ! -name "index.html" | sort); do
  d=$(dirname "$f"); tmp="$d/.rv-tmp.html"
  sed 's#</head>#<style>.zone,.zone::before,.zone::after{display:none!important}</style></head>#' "$f" > "$tmp"
  case "$(grep -o 'frame--916\|frame--45\|class="stage"' "$f" | head -1)" in
    frame--916|'class="stage"') H=1920 ;;
    frame--45) H=1350 ;;
    *) H=1080 ;;
  esac
  out="review/png/$(echo "${f%.html}" | tr '/' '_').png"
  "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1080,$H --screenshot="$out" --virtual-time-budget=4000 \
    "file://$(pwd)/$tmp" >/dev/null 2>&1
  rm -f "$tmp"
done
python3 scripts/build-review-index.py
