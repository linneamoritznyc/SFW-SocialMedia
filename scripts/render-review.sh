#!/bin/sh
# Renders every visual piece to review/<set>/ at full export size, safe-zone
# guides hidden. Headless Chromium reserves ~87px of window height for chrome,
# so we render 120px tall and crop back with scripts/pngcrop.py.
# Run from the repo root.
set -e
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
ROOT=$(pwd)
rm -rf review/*/ 2>/dev/null || true

render() { # $1 html  $2 outpath  $3 height
  d=$(dirname "$1"); tmp="$d/.rv-tmp.html"
  sed 's#</head>#<style>.zone,.zone::before,.zone::after{display:none!important}</style></head>#' "$1" > "$tmp"
  mkdir -p "$(dirname "$2")"
  "$CH" --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --window-size=1080,$(( $3 + 120 )) --screenshot="$2" --virtual-time-budget=4000 \
    "file://$ROOT/$tmp" >/dev/null 2>&1
  rm -f "$tmp"
  python3 scripts/pngcrop.py "$2" "$3"
}

height() {
  case "$(grep -o 'frame--916\|frame--45\|class="stage"' "$1" | head -1)" in
    frame--916|'class="stage"') echo 1920 ;;
    frame--45) echo 1350 ;;
    *) echo 1080 ;;
  esac
}

for f in $(find variants templates motion -name "*.html" ! -name "index.html" | sort); do
  b=$(basename "$f" .html)
  case "$f" in
    variants/umass/*)        set="2-umass-amherst" ;;
    variants/scholarships/*) set="3-scholarships" ;;
    variants/india/*)        set="4-india-tour" ;;
    templates/*)             set="5-templates" ;;
    motion/*)                set="6-motion-stills" ;;
    *)                       set="1-graduate-celebration" ;;
  esac
  render "$f" "review/$set/$b.png" "$(height "$f")"
done



# The graduate set is 27 directions. Six go in start-here so nobody has to
# review all 27. The rest stay available in more-options.
G=review/1-graduate-celebration
mkdir -p $G/start-here $G/more-options
for n in 01-number-first 04-field-photograph 05-quote-card 06-honest-ledger 07-specimen-sheet 13-magazine-cover; do
  [ -f "$G/$n.png" ] && mv "$G/$n.png" "$G/start-here/"
done
for f in $G/*.png; do [ -f "$f" ] && mv "$f" "$G/more-options/"; done
python3 scripts/build-review-index.py
