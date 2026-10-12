# Goose config — OpenRouter coding models

Generated **2026-10-12 12:25 UTC**. 10 models, selected from the live OpenRouter
catalog by coding score, price and real usage. Token figures are the last
7 days (share of all OpenRouter traffic in the window).

| Model | Name in picker | $/1M | Coding | Context | Tokens (7d) | In | Why |
|-------|----------------|------|--------|---------|-------------|----|-----|
| `inclusionai/ling-3.0-flash-vl` | Ling 3.0 Flash VL | $0.03 | 57 | 262,144 | — | img+vid | best cheap-tier value ($0.00–$0.20/1M) |
| `inclusionai/ling-3.0-flash` | Ling 3.0 Flash | $0.03 | 51 | 262,144 | — | text | best cheap-tier value ($0.00–$0.20/1M) |
| `openai/gpt-oss-120b` | OpenAI GPT OSS 120b | $0.07 | 30 | 131,072 | 419.8B (0.2%) | text | best cheap-tier value ($0.00–$0.20/1M) |
| `xiaomi/mimo-v2.6-flash` | MiMo V2.6 Flash | $0.18 | n/a | 1,050,000 | 11.5T (6.7%) | img+vid+aud | widely used (11.5T tok/7d) |
| `anthropic/claude-haiku-5.5` | Claude Haiku 5.5 | $0.20 | n/a | 1,000,000 | 1.1T (0.6%) | img+pdf | best mid-tier value ($0.20–$0.80/1M) |
| `deepseek/deepseek-v4.1-flash` | DeepSeek V4.1 Flash | $0.26 | n/a | 1,048,576 | 41.0T (23.8%) | img | your current model |
| `tencent/hy3-preview` | Hunyuan Hy3 Preview | $0.29 | 59 | 262,144 | — | text | best mid-tier value ($0.20–$0.80/1M) |
| `z-ai/glm-5.3-flash` | GLM 5.3 Flash | $0.32 | 72 | 1,048,576 | 12.2T (7.1%) | img+vid | best mid-tier value ($0.20–$0.80/1M) |
| `z-ai/glm-5.3` | GLM 5.3 | $1.27 | 75 | 1,048,576 | 3.8T (2.2%) | text | your current model |
| `openai/gpt-5.6-sol` | OpenAI GPT 5.6 Sol | $4.00 | 77 | 1,050,000 | 1.6T (0.9%) | pdf+img | best quality under $5/1M |

## Setup — new machine

One command, no repo clone needed (Linux/macOS):

```bash
curl -fsSL https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh
```

This installs the provider, merges the `providers:` entry (with backup), writes a
self-updating launcher (`.desktop` on Linux, `launchctl` on macOS) and adds
`GOOSE_PREDEFINED_MODELS` to your shell profile.

**Start Goose afterwards via the desktop launcher** so the wrapper applies —
the launcher re-downloads the latest model list on *every* start.

Then add the `OPENROUTER_API_KEY` secret in Goose (Settings → provider, or
`goose configure`) — keys are never part of these files.

## Setup — from a local clone

```bash
./goose/install.sh            # copies provider + patches config.yaml (with backup)
```

## Update

Nothing to do: the launcher pulls the latest list on every Goose start, and the
GitHub Action regenerates it weekly (Monday 12:00 UTC). To force it:

```bash
bash "$HOME/.config/goose/launch-goose-with-models.sh"
```
