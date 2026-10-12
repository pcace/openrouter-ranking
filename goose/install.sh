#!/usr/bin/env bash
# Install the generated Goose/OpenRouter config into ~/.config/goose.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_DIR/goose"
GOOSE_DIR="${GOOSE_CONFIG_DIR:-$HOME/.config/goose}"

[ -f "$SRC/openrouter_code.json" ] || { echo "✗ $SRC/openrouter_code.json missing — run generate_goose_config.py"; exit 1; }
command -v python3 >/dev/null || { echo "✗ python3 required"; exit 1; }

mkdir -p "$GOOSE_DIR/custom_providers"
cp "$SRC/openrouter_code.json" "$GOOSE_DIR/custom_providers/openrouter_code.json"
echo "✓ provider → $GOOSE_DIR/custom_providers/openrouter_code.json"

python3 - "$GOOSE_DIR/config.yaml" "$SRC/config.snippet.yaml" <<'PY'
import datetime, shutil, sys, yaml
cfg_path, snip_path = sys.argv[1], sys.argv[2]
snippet = yaml.safe_load(open(snip_path))["providers"]
try:
    cfg = yaml.safe_load(open(cfg_path)) or {}
except FileNotFoundError:
    cfg = {}
cfg.setdefault("providers", {}).update(snippet)
if cfg:
    backup = f"{cfg_path}.bak-{datetime.datetime.now():%Y%m%d%H%M%S}"
    shutil.copy2(cfg_path, backup)
    print(f"✓ merged providers entry into {cfg_path} (backup: {backup})")
with open(cfg_path, "w") as f:
    yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)
PY

# --- Make the picker show names + prices -------------------------------------
# The app reads GOOSE_PREDEFINED_MODELS from its own environment at launch, and
# the value must be a single line.
MIN="$SRC/predefined_models.min.json"
EXPORT_LINE="export GOOSE_PREDEFINED_MODELS=\"\$(cat $MIN)\""

case "$(uname -s)" in
  Linux)
    mkdir -p "$HOME/.config/environment.d"
    printf 'GOOSE_PREDEFINED_MODELS=%s\n' "$(cat "$MIN")" \
      > "$HOME/.config/environment.d/50-goose-predefined-models.conf"
    echo "✓ wrote ~/.config/environment.d/50-goose-predefined-models.conf"
    echo "  → takes effect after the next login (or launch Goose from a shell)"

    # Desktop launcher override: GNOME menu launches don't inherit shell env.
    # A wrapper keeps the JSON out of the .desktop quoting rules entirely.
    if [ -f /usr/share/applications/goose.desktop ]; then
      WRAPPER="$GOOSE_DIR/launch-goose-with-models.sh"
      mkdir -p "$HOME/.local/share/applications"
      cat > "$WRAPPER" <<WRAP
#!/usr/bin/env bash
export GOOSE_PREDEFINED_MODELS="\$(cat "$MIN")"
exec /usr/lib/goose/Goose "\$@"
WRAP
      chmod +x "$WRAPPER"
      cat > "$HOME/.local/share/applications/goose.desktop" <<DESK
[Desktop Entry]
Name=Goose
Exec=$WRAPPER %U
Icon=/usr/share/pixmaps/goose.png
Terminal=false
Type=Application
Categories=Development;
MimeType=x-scheme-handler/goose;
DESK
      echo "✓ wrote ~/.local/share/applications/goose.desktop (via $WRAPPER)"
    fi
    ;;
  Darwin)
    launchctl setenv GOOSE_PREDEFINED_MODELS "$(cat "$MIN")" 2>/dev/null \
      && echo "✓ launchctl setenv GOOSE_PREDEFINED_MODELS (until reboot)"
    ;;
esac

cat <<EOF

Model names + prices are enabled via GOOSE_PREDEFINED_MODELS. For terminals,
add this to ~/.bashrc (or ~/.zshrc):

  $EXPORT_LINE

Then fully quit and restart Goose. The API key is read from Goose's keyring
under OPENROUTER_API_KEY (the same secret the wigolo extension already uses).
EOF

