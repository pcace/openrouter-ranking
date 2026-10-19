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
import datetime, os, shutil, sys, yaml
cfg_path, snip_path = sys.argv[1], sys.argv[2]
snippet = yaml.safe_load(open(snip_path))["providers"]
try:
    cfg = yaml.safe_load(open(cfg_path)) or {}
except FileNotFoundError:
    cfg = {}
cfg.setdefault("providers", {}).update(snippet)
if cfg and os.path.exists(cfg_path):
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
    # The wrapper also refreshes the model list from the repo on every launch.
    if [ -f /usr/share/applications/goose.desktop ]; then
      WRAPPER="$GOOSE_DIR/launch-goose-with-models.sh"
      MODEL_MODE="${GOOSE_MODEL_MODE:-curated}"
      NEWEST="${GOOSE_NEWEST_COUNT:-5}"
      EXTRA_MODELS="${GOOSE_EXTRA_MODELS:-}"
      GOOSE_BIN_RESOLVED="$(command -v goose 2>/dev/null || true)"
      if [ -z "$GOOSE_BIN_RESOLVED" ]; then
        for _c in /usr/lib/goose/Goose /opt/homebrew/bin/goose /usr/local/bin/goose \
                  "/Applications/Goose.app/Contents/MacOS/Goose"; do
          [ -x "$_c" ] && { GOOSE_BIN_RESOLVED="$_c"; break; }
        done
      fi
      echo "✓ goose binary: ${GOOSE_BIN_RESOLVED:-NICHT GEFUNDEN}"
      mkdir -p "$HOME/.local/share/applications"
      cat > "$WRAPPER" <<WRAP
#!/usr/bin/env bash
# Auto-updating Goose launcher.
# Refreshes the OpenRouter model list, then starts Goose with
# GOOSE_PREDEFINED_MODELS set. The refresh never blocks startup — anything that
# fails falls back to the last good copy on disk.
set -u

REPO_RAW="https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose"
LOCAL_REPO="$REPO_DIR"
GOOSE_CFG="\${GOOSE_CONFIG_DIR:-\$HOME/.config/goose}"
CACHE="\${XDG_CACHE_HOME:-\$HOME/.cache}/goose-openrouter"
GOOSE_BIN="\${GOOSE_BIN:-$GOOSE_BIN_RESOLVED}"
MODE="\${GOOSE_MODEL_MODE:-$MODEL_MODE}"
NEWEST="\${GOOSE_NEWEST_COUNT:-$NEWEST}"
EXTRA="\${GOOSE_EXTRA_MODELS:-$EXTRA_MODELS}"
REFRESH_MIN="\${GOOSE_MODEL_REFRESH_MIN:-360}"

if [ -z "\$GOOSE_BIN" ]; then
  echo "✗ goose binary nicht gefunden — bitte GOOSE_BIN setzen"
  exit 1
fi

mkdir -p "\$CACHE" "\$GOOSE_CFG/custom_providers"

fetch() { # \$1=url \$2=dest ; keeps any previous file if the download fails
  local tmp
  tmp="\$(mktemp "\$CACHE/.dl.XXXXXX")"
  if curl -fsSL --max-time 15 "\$1" -o "\$tmp" 2>/dev/null && [ -s "\$tmp" ]; then
    mv "\$tmp" "\$2"
    return 0
  fi
  rm -f "\$tmp"
  return 1
}

stale() { [ ! -s "\$1" ] || [ -n "\$(find "\$1" -mmin +"\$REFRESH_MIN" 2>/dev/null)" ]; }

# API key for the probe: from the environment, else from Goose's own secret
# store (same key the provider uses), so --verify can tell whether a freshly
# released model is actually usable for this account.
GOOSE_KEY="\${OPENROUTER_API_KEY:-}"
if [ -z "\$GOOSE_KEY" ] && command -v secret-tool >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  GOOSE_KEY="\$(secret-tool lookup service goose 2>/dev/null \\
    | python3 -c 'import json,sys;print(json.load(sys.stdin).get("OPENROUTER_API_KEY",""))' 2>/dev/null || true)"
fi

GENERATED=0
if stale "\$CACHE/openrouter_code.json" && command -v python3 >/dev/null 2>&1 \\
   && [ -f "\$LOCAL_REPO/generate_goose_config.py" ]; then
  # Preferred path: rebuild the list locally from the live OpenRouter catalog,
  # so the picker really holds the newest models instead of last week's.
  ALSO_ARGS=""
  for _m in \$(echo "\$EXTRA" | tr ',' ' '); do
    ALSO_ARGS="\$ALSO_ARGS --also \$_m"
  done
  if ( cd "\$LOCAL_REPO" && OPENROUTER_API_KEY="\$GOOSE_KEY" python3 generate_goose_config.py \\
         --mode "\$MODE" --newest "\$NEWEST" --verify \$ALSO_ARGS --out "\$CACHE" ) >/dev/null 2>&1; then
    GENERATED=1
  fi
fi

if [ "\$GENERATED" != 1 ] && stale "\$CACHE/openrouter_code.json"; then
  fetch "\$REPO_RAW/predefined_models.min.json" "\$CACHE/predefined_models.min.json" \\
    || cp -f "\$LOCAL_REPO/goose/predefined_models.min.json" "\$CACHE/" 2>/dev/null || true
  fetch "\$REPO_RAW/openrouter_code.json" "\$CACHE/openrouter_code.json" \\
    || cp -f "\$LOCAL_REPO/goose/openrouter_code.json" "\$CACHE/" 2>/dev/null || true
fi

if [ -s "\$CACHE/openrouter_code.json" ]; then
  cp -f "\$CACHE/openrouter_code.json" "\$GOOSE_CFG/custom_providers/openrouter_code.json"
fi

# If the configured default model vanished from the refreshed list, fall back
# to the first entry so Goose can still start a session.
if command -v python3 >/dev/null 2>&1 && [ -s "\$GOOSE_CFG/config.yaml" ] \\
   && [ -s "\$GOOSE_CFG/custom_providers/openrouter_code.json" ]; then
  python3 - "\$GOOSE_CFG/config.yaml" "\$GOOSE_CFG/custom_providers/openrouter_code.json" <<'PY' || true
import json, sys, yaml
cfg_path, prov_path = sys.argv[1], sys.argv[2]
cfg = yaml.safe_load(open(cfg_path)) or {}
names = [m["name"] for m in json.load(open(prov_path))["models"]]
entry = (cfg.get("providers") or {}).get("openrouter_code")
if entry and names and entry.get("model") not in names:
    entry["model"] = names[0]
    with open(cfg_path, "w") as f:
        yaml.safe_dump(cfg, f, sort_keys=False, allow_unicode=True)
PY
fi

if [ -s "\$CACHE/predefined_models.min.json" ]; then
  export GOOSE_PREDEFINED_MODELS="\$(cat "\$CACHE/predefined_models.min.json")"
fi

exec "\$GOOSE_BIN" "\$@"
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

# Shell profile: so terminals that launch Goose see the variable too.
for _f in "$HOME/.zshrc" "$HOME/.bashrc"; do
  if [ -f "$_f" ]; then
    SHELLRC="$_f"
    break
  fi
done
if [ -n "${SHELLRC:-}" ] && ! grep -qF "GOOSE_PREDEFINED_MODELS" "$SHELLRC"; then
  printf '\n# Goose: newest OpenRouter models with prices (auto-updated)\nexport GOOSE_PREDEFINED_MODELS="$(cat %s)"\n' "$MIN" >> "$SHELLRC"
  echo "✓ export added to $SHELLRC"
fi

cat <<EOF

Model names + prices are enabled via GOOSE_PREDEFINED_MODELS.
Then fully quit and restart Goose (via the desktop launcher).

The API key is read from Goose's keyring under OPENROUTER_API_KEY —
add it on this machine; keys are never shipped with these files.
EOF

