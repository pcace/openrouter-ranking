#!/usr/bin/env bash
# Bootstrap the Goose/OpenRouter model setup on a NEW machine.
#
# No repo clone needed — files are pulled straight from GitHub:
#   curl -fsSL https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose/bootstrap.sh -o bootstrap.sh
#   bash bootstrap.sh
#
# What it sets up:
#   - custom provider with curated models   ~/.config/goose/custom_providers/
#   - providers entry in                    ~/.config/goose/config.yaml (backup)
#   - self-updating launcher + .desktop (Linux) / launchctl (macOS)
#   - GOOSE_PREDEFINED_MODELS in ~/.bashrc or ~/.zshrc
#
# It does NOT touch your API key: add OPENROUTER_API_KEY in Goose afterwards.
set -euo pipefail

REPO_RAW="${GOOSE_CONFIG_RAW:-https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose}"
DEST="${GOOSE_CONFIG_HOME:-$HOME/.local/share/goose-ranking}"

echo "🔄 Goose-Config von $REPO_RAW laden → $DEST"
mkdir -p "$DEST/goose"
for f in install.sh openrouter_code.json predefined_models.min.json; do
  curl -fsSL --max-time 60 "$REPO_RAW/$f" -o "$DEST/goose/$f"
  echo "  ✓ $f"
done
chmod +x "$DEST/goose/install.sh"

if ! command -v goose >/dev/null 2>&1 && [ ! -x /usr/lib/goose/Goose ] \
   && [ ! -x "/Applications/Goose.app/Contents/MacOS/Goose" ]; then
  echo
  echo "⚠️  Goose selbst scheint nicht installiert zu sein."
  echo "    Die Config wird trotzdem installiert — installiere Goose und starte es"
  echo "    über den Desktop-Launcher, damit der Auto-Update-Wrapper greift."
  echo
fi

exec bash "$DEST/goose/install.sh"
