# Goose config — OpenRouter models

Generated **2026-10-19 19:19 UTC**. Mode: **curated** — 9 affordable, widely used models.
Not the newest, not the priciest: cheap value picks first, then the models
OpenRouter users actually spend tokens on, then one or two strong models on top
(best under $2.00 and under $3.50 per 1M tokens). With `--verify` every
candidate is probed with a 1-token request, so models your account cannot reach
are replaced instead of parked in the picker. Token figures: last 7
days (share of all OpenRouter traffic in the window).

| Model | Name in picker | Released | $/1M | Context | In | Coding | Tokens (7d) | Why |
|-------|----------------|----------|------|---------|----|--------|-------------|-----|
| `deepseek/deepseek-v4.1-flash` | DeepSeek V4.1 Flash | 2026-09-10 | $0.04 | 1,048,576 | img | n/a | 36.6T (22.3%) | your daily driver · 36.6T tok/7d · 22.3% |
| `z-ai/glm-5.3-flash` | GLM 5.3 Flash | 2026-08-26 | $0.08 | 1,048,576 | img+vid | 72 | 12.2T (7.5%) | your daily driver · 12.2T tok/7d · 7.5% |
| `inclusionai/ling-3.1-flash` | Ling 3.1 Flash | 2026-10-02 | $0.11 | 262,144 | text | n/a | 190.0B (0.1%) | best cheap-tier value ($0.00–$0.30/1M) |
| `deepseek/deepseek-v4-flash` | DeepSeek V4 Flash 0423 | 2026-04-24 | $0.11 | 1,048,576 | text | 52 | 7.7T (4.7%) | cheap tier, most traffic · 7.7T tok/7d · 4.7% |
| `xiaomi/mimo-v2.6-flash` | MiMo V2.6 Flash | 2026-09-21 | $0.18 | 1,050,000 | img+vid+aud | n/a | 9.9T (6.1%) | cheap tier, most traffic · 9.9T tok/7d · 6.1% |
| `z-ai/glm-5.3` | GLM 5.3 | 2026-08-18 | $0.41 | 1,048,576 | text | 75 | 5.2T (3.2%) | mid tier, most traffic · 5.2T tok/7d · 3.2% |
| `openai/gpt-5.6-luna` | OpenAI GPT 5.6 Luna | 2026-07-09 | $0.45 | 1,050,000 | pdf+img | 71 | 1.7T (1.0%) | best mid-tier value ($0.30–$0.80/1M) |
| `google/gemini-3.8-flash` | Gemini 3.8 Flash | 2026-09-02 | $1.65 | 1,048,576 | img+vid+pdf+aud | 76 | 1.8T (1.1%) | best quality under $2.00/1M (score 76) |
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
