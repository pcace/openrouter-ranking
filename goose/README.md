# Goose config — OpenRouter coding models

Generated **2026-10-12 12:22 UTC**. 9 models, selected from the live OpenRouter
catalog by coding score, price and real usage. Token figures are the last
7 days (share of all OpenRouter traffic in the window).

| Model | Name in picker | $/1M | Coding | Context | Tokens (7d) | In | Why |
|-------|----------------|------|--------|---------|-------------|----|-----|
| `inclusionai/ling-3.0-flash-vl` | Ling 3.0 Flash VL | $0.03 | 57 | 262,144 | — | img+vid | best cheap-tier value ($0.00–$0.20/1M) |
| `inclusionai/ling-3.0-flash` | Ling 3.0 Flash | $0.03 | 51 | 262,144 | — | text | best cheap-tier value ($0.00–$0.20/1M) |
| `openai/gpt-oss-120b` | OpenAI GPT OSS 120b | $0.07 | 30 | 131,072 | — | text | best cheap-tier value ($0.00–$0.20/1M) |
| `anthropic/claude-haiku-5.5` | Claude Haiku 5.5 | $0.20 | n/a | 1,000,000 | — | img+pdf | best mid-tier value ($0.20–$0.80/1M) |
| `deepseek/deepseek-v4.1-flash` | DeepSeek V4.1 Flash | $0.26 | n/a | 1,048,576 | — | img | your current model |
| `tencent/hy3-preview` | Hunyuan Hy3 Preview | $0.29 | 59 | 262,144 | — | text | best mid-tier value ($0.20–$0.80/1M) |
| `z-ai/glm-5.3-flash` | GLM 5.3 Flash | $0.32 | 72 | 1,048,576 | — | img+vid | best mid-tier value ($0.20–$0.80/1M) |
| `z-ai/glm-5.3` | GLM 5.3 | $1.27 | 75 | 1,048,576 | — | text | your current model |
| `openai/gpt-5.6-sol` | OpenAI GPT 5.6 Sol | $4.00 | 77 | 1,050,000 | — | pdf+img | best quality under $5/1M |

## Install

```bash
./goose/install.sh            # copies provider + patches config.yaml (with backup)
```

Then make the picker show names + prices. The desktop app reads
GOOSE_PREDEFINED_MODELS from its environment, so it must be set before launch:

  export GOOSE_PREDEFINED_MODELS="$(cat ~/git/openrouter-ranking/goose/predefined_models.min.json)"

The API key is read from the `OPENROUTER_API_KEY` secret in Goose's keyring
(`goose configure` → your provider), same as any other OpenRouter setup.

## Update weekly

```bash
cd ~/git/openrouter-ranking && git pull && ./goose/install.sh
```
