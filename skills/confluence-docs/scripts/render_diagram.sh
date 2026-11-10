#!/usr/bin/env bash
# Render a Mermaid file to a 2x PNG with the team theme.
#   scripts/render_diagram.sh diagrams/10-flow.mmd [out.png]
# Needs mmdc (npm i -g @mermaid-js/mermaid-cli) and a Chrome binary. The bundled Puppeteer Chrome path
# goes stale after updates, so this script looks for Chrome for Testing in the Puppeteer and Playwright
# caches, then the installed Google Chrome, and writes a temporary puppeteer config pointing at it.
set -eu
in=${1:?usage: render_diagram.sh file.mmd [out.png]}
out=${2:-${in%.mmd}.png}
here=$(cd "$(dirname "$0")" && pwd)
theme="$here/../assets/theme.json"

find_chrome() {
  local c
  for c in \
    "$HOME"/.cache/puppeteer/chrome/*/chrome-mac-arm64/"Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" \
    "$HOME"/.cache/puppeteer/chrome/*/chrome-mac-x64/"Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" \
    "$HOME"/Library/Caches/ms-playwright/chromium-*/chrome-mac*/"Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing" \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$HOME"/.cache/puppeteer/chrome/*/chrome-linux64/chrome \
    /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do
    if [ -x "$c" ]; then printf '%s' "$c"; return 0; fi
  done
  return 1
}

chrome=${CHROME_PATH:-$(find_chrome || true)}
if [ -z "$chrome" ]; then echo "no Chrome found; set CHROME_PATH" >&2; exit 1; fi
cfg=$(mktemp -t puppeteer-XXXX.json)
trap 'rm -f "$cfg"' EXIT
printf '{ "executablePath": "%s", "args": ["--no-sandbox"] }\n' "$chrome" > "$cfg"

mmdc -i "$in" -o "$out" -c "$theme" -p "$cfg" -b transparent -s 2 --quiet
echo "rendered $out"
