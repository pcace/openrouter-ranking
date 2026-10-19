# 🏆 OpenRouter LLM Cost-Effectiveness Ranking

> **Updated:** 2026-10-19 19:19 UTC
> **Models on OpenRouter:** 470 · **Families priced:** 346 · **With benchmark scores:** 213
> **Methodology:** value = benchmark index ÷ blended price per 1M tokens (750K prompt + 250K completion). Data via [OpenRouter API](https://openrouter.ai/api/v1/models).

---

## 📖 How this works

Every category below is defined by a **rule** (a benchmark metric plus a filter),
not by a hand-picked list. Any model that OpenRouter ships is scored automatically:

- **Effectiveness** ← Artificial Analysis indices (`intelligence`, `coding`, `agentic`)
  and Design Arena ELO, embedded in each model object from the API.
- **Cost** ← live pricing from the same response.
- Categories filter on capabilities from the API: `supported_parameters` (tools,
  reasoning), `context_length`, and `architecture.input_modalities`.

Add a model to OpenRouter → it shows up here on the next run. No code change.

**Prices in USD per 1M tokens (blended).** 🟢 <$0.15 · 🟡 <$0.50 · 🟠 <$1.50 · 🔴 ≥$1.50.
`In` = accepted input modalities.

---

## 🏆 Top Picks (computed, not curated)

| | Model | Why |
|---|-------|-----|
| 🥇 Best value | `z-ai/glm-5.3-flash` | 42 intelligence for 0.076/1M |
| 🥈 Highest score | `anthropic/claude-opus-5.5` | 58 intelligence (absolute top) |
| 🥉 Cheapest usable | `inclusionai/ling-3.0-flash` | $0.032/1M at 20 intelligence |


---

## 📈 Most Used (last 7 days, by tokens)

_Real OpenRouter traffic — what is actually being run, not what is best value._

| # | Model | Share | $/1M | Intelligence |
|---|-------|-------|------|--------------|
| 1 | `deepseek/deepseek-v4.1-flash-20260910` | 21.5% | $0.043 | 24.7 |
| 2 | `z-ai/glm-5.3-flash-20260826` | 8.0% | $0.076 | 41.8 |
| 3 | `stepfun/step-5-preview-20261008` | 7.5% | $1.425 | 43.7 |
| 4 | `xiaomi/mimo-v2.6-flash-20260921` | 6.5% | $0.175 | 37.9 |
| 5 | `tencent/hy4-preview-20260827` | 5.0% | $1.126 | — |
| 6 | `openai/gpt-6-luna-20260922` | 4.1% | $0.200 | 38.1 |
| 7 | `anthropic/claude-opus-5.5-20260921` | 4.1% | $8.000 | 57.6 |
| 8 | `z-ai/glm-5.3-20260816` | 3.4% | $0.409 | 44.8 |
| 9 | `nvidia/nemotron-3-ultra-550b-a55b-20260604:free` | 3.3% | $1.050 | 22.9 |
| 10 | `deepseek/deepseek-v4-flash-20260731` | 3.1% | $0.114 | 24.4 |
| 11 | `deepseek/deepseek-v4.1-flash-20261017` | 2.4% | $0.043 | 24.7 |
| 12 | `meta/muse-spark-1.3-contributor-20260902` | 2.1% | $0.125 | — |
| 13 | `tencent/hy3-20260706` | 2.0% | $0.144 | — |
| 14 | `deepseek/deepseek-v4-flash-20260423` | 2.0% | $0.114 | 24.4 |
| 15 | `typesafe/jev-1.13-20260917` | 2.0% | — | — |


---

## 💬 General Assistant
_Everyday chat, Q&A, summaries, translation_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 41.8 | 550 | 1,048,576 | text+image+video |
| ⭐ 2 | `inclusionai/ling-3.1-flash` | 🟢 $0.112 | 41.1 | 365 | 262,144 | text |
| ⭐ 3 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| 4 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| 5 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 6 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.195 | 34.3 | 176 | 1,048,576 | text |
| 7 | `deepseek/deepseek-v4.1-flash-1017` | 🟡 $0.262 | 39.5 | 150 | 1,048,576 | text+image |
| 8 | `z-ai/glm-5.3` | 🟡 $0.409 | 44.8 | 109 | 1,048,576 | text |
| 9 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 10 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |


---

## 💻 Programming / Code
_Code generation, debugging, review_

| # | Model | $/1M | Coding idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 71.5 | 941 | 1,048,576 | text+image+video |
| ⭐ 2 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.195 | 69.1 | 355 | 1,048,576 | text |
| ⭐ 3 | `tencent/hy3-preview` | 🟡 $0.285 | 58.8 | 206 | 262,144 | text |
| 4 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 65.0 | 201 | 1,048,576 | text+image |
| 5 | `z-ai/glm-5.3` | 🟡 $0.409 | 74.8 | 183 | 1,048,576 | text |
| 6 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 71.4 | 159 | 1,050,000 | file+image+text |
| 7 | `deepseek/deepseek-v4-pro` | 🟡 $0.494 | 59.4 | 120 | 1,048,576 | text |
| 8 | `minimax/minimax-m3` | 🟠 $0.525 | 58.6 | 112 | 1,048,576 | text+image+video |
| 9 | `xiaomi/mimo-v2.5-pro` | 🟠 $0.544 | 60.2 | 111 | 1,050,000 | text |
| 10 | `qwen/qwen3.8-27b` | 🟠 $0.730 | 68.1 | 93 | 1,000,000 | text+image+video |


---

## 🧠 Complex Reasoning
_Math, logic, step-by-step problem solving_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 2 | `z-ai/glm-5.3` | 🟡 $0.409 | 44.8 | 109 | 1,048,576 | text |
| ⭐ 3 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 4 | `stepfun/step-5-preview` | 🟠 $1.425 | 43.7 | 31 | 1,048,576 | text+image+video |
| 5 | `meta/muse-spark-1.3` | 🔴 $2.000 | 48.1 | 24 | 1,048,576 | text+image+video+file |
| 6 | `x-ai/grok-4.7` | 🔴 $3.000 | 46.4 | 15 | 500,000 | text+image+file |
| 7 | `qwen/qwen3.8-max-0902` | 🔴 $3.000 | 45.4 | 15 | 1,000,000 | text+image+video |
| 8 | `x-ai/grok-4.6` | 🔴 $3.000 | 44.3 | 15 | 500,000 | text+image+file |
| 9 | `anthropic/claude-sonnet-5.5` | 🔴 $4.000 | 56.0 | 14 | 1,000,000 | text+image+file |
| 10 | `moonshotai/kimi-k3` | 🔴 $3.163 | 43.6 | 14 | 1,048,576 | text+image+video |


---

## 🤖 Agentic / Tool Use
_Multi-step agents, function calling, computer use_

| # | Model | $/1M | Agentic idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 50.9 | 670 | 1,048,576 | text+image+video |
| ⭐ 2 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.195 | 41.0 | 211 | 1,048,576 | text |
| ⭐ 3 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 47.5 | 147 | 1,048,576 | text+image |
| 4 | `z-ai/glm-5.3` | 🟡 $0.409 | 53.1 | 130 | 1,048,576 | text |
| 5 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 42.1 | 94 | 1,050,000 | file+image+text |
| 6 | `qwen/qwen3.8-27b` | 🟠 $0.730 | 45.8 | 63 | 1,000,000 | text+image+video |
| 7 | `deepseek/deepseek-v4-pro-0813` | 🟠 $0.990 | 41.3 | 42 | 1,048,576 | text |
| 8 | `meta/muse-spark-1.3` | 🔴 $2.000 | 55.5 | 28 | 1,048,576 | text+image+video+file |
| 9 | `meta/muse-spark-1.2` | 🔴 $2.000 | 43.2 | 22 | 1,048,576 | text+image+video+file |
| 10 | `qwen/qwen3.8-max-0902` | 🔴 $3.000 | 56.0 | 19 | 1,000,000 | text+image+video |


---

## 🔍 Research / Long Documents
_Paper analysis, long reports (context ≥ 200K)_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 41.8 | 550 | 1,048,576 | text+image+video |
| ⭐ 2 | `inclusionai/ling-3.1-flash` | 🟢 $0.112 | 41.1 | 365 | 262,144 | text |
| ⭐ 3 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| 4 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| 5 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 6 | `deepseek/deepseek-v4.1-flash-1017` | 🟡 $0.262 | 39.5 | 150 | 1,048,576 | text+image |
| 7 | `z-ai/glm-5.3` | 🟡 $0.409 | 44.8 | 109 | 1,048,576 | text |
| 8 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 9 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 10 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 37.3 | 83 | 1,050,000 | file+image+text |


---

## 🌐 Multimodal (Image/Video/Audio input)
_Image analysis, charts, screenshots, video_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 41.8 | 550 | 1,048,576 | text+image+video |
| ⭐ 2 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 3 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| 4 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 5 | `deepseek/deepseek-v4.1-flash-1017` | 🟡 $0.262 | 39.5 | 150 | 1,048,576 | text+image |
| 6 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 7 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 8 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 37.3 | 83 | 1,050,000 | file+image+text |
| 9 | `qwen/qwen3.8-27b` | 🟠 $0.730 | 33.7 | 46 | 1,000,000 | text+image+video |
| 10 | `mistralai/mistral-large-4-0` | 🟠 $1.032 | 38.4 | 37 | 1,048,576 | text+image |


---

## ⚡ Simple Tasks / High Volume
_Cheapest models that still score ≥ 20 on intelligence_

| # | Model | $/1M | Intelligence idx | idx/$ | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `inclusionai/ling-3.0-flash` | 🟢 $0.032 | 20.1 | 638 | 262,144 | text |
| ⭐ 2 | `deepseek/deepseek-v4.1-flash` | 🟢 $0.043 | 24.7 | 577 | 1,048,576 | text+image |
| ⭐ 3 | `z-ai/glm-5.3-flash` | 🟢 $0.076 | 41.8 | 550 | 1,048,576 | text+image+video |
| 4 | `upstage/solar-mini4` | 🟢 $0.087 | 24.1 | 275 | 524,288 | text |
| 5 | `inclusionai/ling-3.0-flash-vl` | 🟢 $0.090 | 24.6 | 273 | 131,072 | text+image+video |
| 6 | `inclusionai/ling-3.1-flash` | 🟢 $0.112 | 41.1 | 365 | 262,144 | text |
| 7 | `deepseek/deepseek-v4-flash` | 🟢 $0.114 | 24.4 | 215 | 1,048,576 | text |
| 8 | `upstage/solar-pro4` | 🟡 $0.158 | 28.2 | 179 | 524,288 | text |
| 9 | `nvidia/nemotron-3.5-super-vl` | 🟡 $0.175 | 26.5 | 151 | 1,048,576 | text+image+video |
| 10 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |


---

## 🧪 OpenRouter Evals

_OpenRouter's own evaluations — knowledge/reasoning and tool-calling accuracy._

> Source: OpenRouter evals (openrouter.ai) via OpenRouter (openrouter.ai/rankings).

### GPQA Diamond
_graduate-level science Q&A — accuracy, higher is better_

| # | Model | Accuracy | $/task | Runs |
|---|-------|----------|--------|------|
| 1 | `google/gemini-4-argon` | 96.5% | $0.0947 | 198 |
| 2 | `google/gemini-3.8-flash` | 95.6% | $0.0682 | 191 |
| 3 | `openai/gpt-6-astra-pro` | 95.5% | $0.3326 | 198 |
| 4 | `sakana/fugu-ultra` | 94.6% | $1.1487 | 198 |
| 5 | `google/gemini-3.1-pro-preview` | 94.5% | $0.2020 | 396 |
| 6 | `openai/gpt-6-astra` | 94.4% | $0.1133 | 198 |
| 7 | `openai/gpt-6.1-sol` | 94.4% | $0.0214 | 198 |
| 8 | `openai/gpt-5.6-sol-pro` | 93.9% | $0.2979 | 396 |
| 9 | `google/gemini-3.7-flash` | 93.9% | $0.0293 | 385 |
| 10 | `openai/gpt-5.5` | 93.7% | $0.3093 | 594 |
| 11 | `sakana/fugu-ultra-v2` | 93.3% | $0.5026 | 198 |
| 12 | `x-ai/grok-4.6` | 92.8% | $0.1233 | 396 |

### tau-bench (airline)
_tool-calling agent tasks — accuracy, higher is better_

| # | Model | Accuracy | $/task | Runs |
|---|-------|----------|--------|------|
| 1 | `inclusionai/ling-3.1-flash` | 79.3% | $0.0315 | 50 |
| 2 | `anthropic/claude-fable-5.1` | 79.2% | $0.7162 | 200 |
| 3 | `anthropic/claude-opus-5` | 78.8% | $0.4846 | 550 |
| 4 | `google/gemini-4-argon` | 78.7% | $0.4983 | 50 |
| 5 | `anthropic/claude-sonnet-5.5` | 78.7% | $0.1599 | 150 |
| 6 | `xiaomi/mimo-v2.6-flash` | 78.7% | $0.0154 | 150 |
| 7 | `google/gemini-3.7-flash` | 78.3% | $0.1499 | 146 |
| 8 | `deepseek/deepseek-v4-pro` | 78.1% | $0.1039 | 450 |
| 9 | `amazon/nova-micro-v1` | 78.0% | $1.2758 | 150 |
| 10 | `meta/muse-spark-open` | 78.0% | $0.1159 | 50 |
| 11 | `qwen/qwen3.8-27b` | 77.9% | $0.0731 | 400 |
| 12 | `qwen/qwen3.5-397b-a17b` | 77.6% | $0.1828 | 400 |


---

## 🚀 Trending Apps

_Fastest-growing apps on OpenRouter by token growth vs. prior windows._

| # | App | Tokens | Requests |
|---|-----|--------|----------|
| 1 | Claude Code | 35,310,800,898,654 | 328,774,556 |
| 2 | Kilo Code | 23,860,096,725,769 | 270,073,516 |
| 3 | Cline | 20,122,312,449,788 | 162,627,513 |
| 4 | Hermes Agent | 52,039,724,598,098 | 499,848,099 |
| 5 | Codex | 11,398,724,177,681 | 145,034,331 |
| 6 | pi | 12,751,598,960,544 | 119,386,557 |
| 7 | omp | 10,257,391,779,825 | 68,281,987 |
| 8 | Freebuff | 10,401,742,124,082 | 76,256,070 |
| 9 | DeepSeek Harness | 6,190,301,022,077 | 39,734,376 |
| 10 | Command Code | 4,168,980,384,803 | 46,529,700 |
| 11 | OpenHands | 3,439,163,863,846 | 35,119,608 |
| 12 | OpenClaw | 7,377,395,767,794 | 82,928,645 |
| 13 | Strix | 2,313,902,634,798 | 18,667,814 |
| 14 | Proto Agent | 1,866,291,166,958 | 4,843,131 |
| 15 | HighLevel | 1,676,847,705,222 | 30,420,234 |

*Source: OpenRouter (openrouter.ai/apps), as of 2026-10-19T19:19:33.015Z — CC BY 4.0.*


---

## 🔧 Methodology

- **Source:** [OpenRouter API](https://openrouter.ai/api/v1/models) — live catalog incl. benchmark scores
- **Cost formula:** `prompt_price × 750,000 + completion_price × 250,000`
- **Value:** `benchmark_index / cost_per_1M` (higher is better); ranked descending
- **Family collapse:** routing/alias variants (`:free`, `:nitro`, `~alias`) are merged
  into their base model family, keeping the cheapest representative
- **Coverage:** models without a benchmark score are skipped in metric-based
  categories rather than guessed at
- **Updates:** weekly via GitHub Actions

---

*Data source: OpenRouter (openrouter.ai). Usage figures from openrouter.ai/rankings (CC BY 4.0, as of 2026-10-19 19:19 UTC). Fork of Draxo-io/openrouter-ranking.*

---

## 🤖 Automation

Generated weekly by GitHub Actions (`.github/workflows/update-ranking.yml`).
Run manually: `python generate_ranking.py` (set `OPENROUTER_API_KEY` for the usage section).
