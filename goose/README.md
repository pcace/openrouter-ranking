# Goose config — OpenRouter models

Generated **2026-10-19 19:18 UTC**. Mode: **curated** — 6 affordable, widely used models.
Not the newest, not the priciest: cheap value picks first, then the models
OpenRouter users actually spend tokens on, then one or two strong models on top
(best under $2.00 and under $3.50 per 1M tokens). With `--verify` every
candidate is probed with a 1-token request, so models your account cannot reach
are replaced instead of parked in the picker. Token figures: last 7
days (share of all OpenRouter traffic in the window).

| Model | Name in picker | Released | $/1M | Context | In | Coding | Tokens (7d) | Why |
|-------|----------------|----------|------|---------|----|--------|-------------|-----|
| `inclusionai/ling-3.0-flash` | Ling 3.0 Flash | 2026-07-23 | $0.03 | 262,144 | text | 51 | — | best cheap-tier value ($0.00–$0.30/1M) |
| `deepseek/deepseek-v4.1-flash` | DeepSeek V4.1 Flash | 2026-09-10 | $0.04 | 1,048,576 | img | n/a | — | your daily driver · 0 tok/7d |
| `z-ai/glm-5.3-flash` | GLM 5.3 Flash | 2026-08-26 | $0.08 | 1,048,576 | img+vid | 72 | — | your daily driver · 0 tok/7d |
| `deepseek/deepseek-v4-flash-vision-exp` | DeepSeek V4 Flash Vision Exp | 2026-08-21 | $0.32 | 1,048,576 | img | 65 | — | best mid-tier value ($0.30–$0.80/1M) |
| `google/gemini-3.8-flash` | Gemini 3.8 Flash | 2026-09-02 | $1.65 | 1,048,576 | img+vid+pdf+aud | 76 | — | best quality under $2.00/1M (score 76) |
| `x-ai/grok-4.6` | Grok 4.6 | 2026-08-12 | $3.00 | 500,000 | img+pdf | 77 | — | best quality under $3.50/1M (score 77) |

## Setup — new machine

One command, no repo clone needed (Linux/macOS):

```bash
curl -fsSL https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh
```

This installs the provider, merges the `providers:` entry (with backup), writes a
self-updating launcher (`.desktop` on Linux, `launchctl` on macOS) and adds
`GOOSE_PREDEFINED_MODELS` to your shell profile.

**Start Goose afterwards via the desktop launcher** so the wrapper applies —
the launcher refreshes the model list on *every* start.

Then add the `OPENROUTER_API_KEY` secret in Goose (Settings → provider, or
`goose configure`) — keys are never part of these files.

## Setup — from a local clone

```bash
./goose/install.sh            # copies provider + patches config.yaml (with backup)
```

## Update

Nothing to do: the launcher refreshes the list on every Goose start — locally it
re-runs `generate_goose_config.py`, otherwise it pulls the generated files — and
the GitHub Action regenerates them weekly (Monday 12:00 UTC). To force it:

```bash
bash "$HOME/.config/goose/launch-goose-with-models.sh"
```

Knobs the launcher reads: `GOOSE_NEWEST_COUNT` (default `5`),
`GOOSE_MODEL_MODE` (`newest` or `curated`), `GOOSE_EXTRA_MODELS` (comma-separated
models that stay in the list regardless of their release date, e.g.
`z-ai/glm-5.3-flash`) and `GOOSE_MODEL_REFRESH_MIN` (default `360` — minutes
before the local regeneration runs again).
