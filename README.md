# 🏆 OpenRouter LLM Cost-Effectiveness Ranking

> **Updated:** 2026-10-12 12:22 UTC
> **Models on OpenRouter:** 458 · **Families priced:** 338 · **With benchmark scores:** 211
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
| 🥇 Best value | `anthropic/claude-haiku-5.5` | 43 intelligence for 0.200/1M |
| 🥈 Highest score | `anthropic/claude-opus-5.5` | 58 intelligence (absolute top) |
| 🥉 Cheapest usable | `inclusionai/ling-3.0-flash-vl` | $0.031/1M at 25 intelligence |


---

## 📈 Most Used (last 7 days, by tokens)

_Real OpenRouter traffic — what is actually being run, not what is best value._

| # | Model | Share | $/1M | Intelligence |
|---|-------|-------|------|--------------|
| 1 | `deepseek/deepseek-v4.1-flash-20260910` | 25.5% | $0.525 | 39.5 |
| 2 | `z-ai/glm-5.3-flash-20260826` | 7.6% | $0.317 | 41.8 |
| 3 | `xiaomi/mimo-v2.6-flash-20260921` | 7.1% | $0.175 | 37.9 |
| 4 | `stepfun/step-5-preview-20261008` | 5.5% | $1.425 | — |
| 5 | `tencent/hy4-preview-20260827` | 5.2% | $1.251 | — |
| 6 | `openai/gpt-6-luna-20260922` | 4.4% | $0.200 | 38.1 |
| 7 | `nvidia/nemotron-3-ultra-550b-a55b-20260604:free` | 4.3% | $1.050 | 22.9 |
| 8 | `anthropic/claude-opus-5.5-20260921` | 3.1% | $8.000 | 57.6 |
| 9 | `deepseek/deepseek-v4-flash-20260731` | 3.1% | $0.343 | 24.4 |
| 10 | `stealth/space-bunny-alpha` | 2.6% | — | — |
| 11 | `z-ai/glm-5.3-20260816` | 2.4% | $1.259 | 44.8 |
| 12 | `typesafe/jev-1.13-20260917` | 2.1% | — | — |
| 13 | `deepseek/deepseek-v4-flash-20260423` | 1.9% | $0.343 | 24.4 |
| 14 | `tencent/hy3-20260706` | 1.6% | $0.231 | — |
| 15 | `anthropic/claude-sonnet-5.5-20260928` | 1.5% | $4.000 | 56.0 |


---

## 💬 General Assistant
_Everyday chat, Q&A, summaries, translation_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 2 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| ⭐ 3 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.172 | 34.3 | 199 | 1,048,576 | text |
| 4 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 5 | `z-ai/glm-5.3-flash` | 🟡 $0.317 | 41.8 | 132 | 1,048,576 | text+image+video |
| 6 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 7 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 8 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 37.3 | 83 | 1,050,000 | file+image+text |
| 9 | `deepseek/deepseek-v4.1-flash` | 🟠 $0.525 | 39.5 | 75 | 1,048,576 | text+image |
| 10 | `qwen/qwen3.8-27b` | 🟠 $0.605 | 33.7 | 56 | 1,000,000 | text+image+video |


---

## 💻 Programming / Code
_Code generation, debugging, review_

| # | Model | $/1M | Coding idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.172 | 69.1 | 402 | 1,048,576 | text |
| ⭐ 2 | `z-ai/glm-5.3-flash` | 🟡 $0.317 | 71.5 | 225 | 1,048,576 | text+image+video |
| ⭐ 3 | `tencent/hy3-preview` | 🟡 $0.285 | 58.8 | 206 | 262,144 | text |
| 4 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 65.0 | 201 | 1,048,576 | text+image |
| 5 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 71.4 | 159 | 1,050,000 | file+image+text |
| 6 | `qwen/qwen3.8-27b` | 🟠 $0.605 | 68.1 | 113 | 1,000,000 | text+image+video |
| 7 | `minimax/minimax-m3` | 🟠 $0.525 | 58.6 | 112 | 1,048,576 | text+image+video |
| 8 | `xiaomi/mimo-v2.5-pro` | 🟠 $0.544 | 60.2 | 111 | 1,050,000 | text |
| 9 | `z-ai/glm-5.3` | 🟠 $1.259 | 74.8 | 59 | 1,048,576 | text |
| 10 | `google/gemini-3.8-flash` | 🔴 $1.500 | 76.3 | 51 | 1,048,576 | text+image+video+file+audio |


---

## 🧠 Complex Reasoning
_Math, logic, step-by-step problem solving_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 2 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| ⭐ 3 | `z-ai/glm-5.3` | 🟠 $1.259 | 44.8 | 36 | 1,048,576 | text |
| 4 | `meta/muse-spark-1.3` | 🔴 $2.000 | 48.1 | 24 | 1,048,576 | text+image+video+file |
| 5 | `x-ai/grok-4.7` | 🔴 $3.000 | 46.4 | 15 | 500,000 | text+image+file |
| 6 | `qwen/qwen3.8-max-0902` | 🔴 $3.000 | 45.4 | 15 | 1,000,000 | text+image+video |
| 7 | `x-ai/grok-4.6` | 🔴 $3.000 | 44.3 | 15 | 500,000 | text+image+file |
| 8 | `moonshotai/kimi-k3` | 🔴 $3.047 | 43.6 | 14 | 1,048,576 | text+image+video |
| 9 | `anthropic/claude-sonnet-5.5` | 🔴 $4.000 | 56.0 | 14 | 1,000,000 | text+image+file |
| 10 | `openai/gpt-6.1-sol` | 🔴 $4.000 | 51.8 | 13 | 1,050,000 | file+image+text |


---

## 🤖 Agentic / Tool Use
_Multi-step agents, function calling, computer use_

| # | Model | $/1M | Agentic idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.172 | 41.0 | 238 | 1,048,576 | text |
| ⭐ 2 | `z-ai/glm-5.3-flash` | 🟡 $0.317 | 50.9 | 160 | 1,048,576 | text+image+video |
| ⭐ 3 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 47.5 | 147 | 1,048,576 | text+image |
| 4 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 42.1 | 94 | 1,050,000 | file+image+text |
| 5 | `qwen/qwen3.8-27b` | 🟠 $0.605 | 45.8 | 76 | 1,000,000 | text+image+video |
| 6 | `z-ai/glm-5.3` | 🟠 $1.259 | 53.1 | 42 | 1,048,576 | text |
| 7 | `meta/muse-spark-1.3` | 🔴 $2.000 | 55.5 | 28 | 1,048,576 | text+image+video+file |
| 8 | `meta/muse-spark-1.2` | 🔴 $2.000 | 43.2 | 22 | 1,048,576 | text+image+video+file |
| 9 | `deepseek/deepseek-v4-pro-0813` | 🔴 $1.980 | 41.3 | 21 | 1,048,576 | text |
| 10 | `qwen/qwen3.8-max-0902` | 🔴 $3.000 | 56.0 | 19 | 1,000,000 | text+image+video |


---

## 🔍 Research / Long Documents
_Paper analysis, long reports (context ≥ 200K)_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 2 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| ⭐ 3 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 4 | `z-ai/glm-5.3-flash` | 🟡 $0.317 | 41.8 | 132 | 1,048,576 | text+image+video |
| 5 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 6 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 7 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 37.3 | 83 | 1,050,000 | file+image+text |
| 8 | `deepseek/deepseek-v4.1-flash` | 🟠 $0.525 | 39.5 | 75 | 1,048,576 | text+image |
| 9 | `z-ai/glm-5.3` | 🟠 $1.259 | 44.8 | 36 | 1,048,576 | text |
| 10 | `google/gemini-3.8-flash` | 🔴 $1.500 | 40.9 | 27 | 1,048,576 | text+image+video+file+audio |


---

## 🌐 Multimodal (Image/Video/Audio input)
_Image analysis, charts, screenshots, video_

| # | Model | $/1M | Intelligence idx | Value | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| ⭐ 2 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| ⭐ 3 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |
| 4 | `z-ai/glm-5.3-flash` | 🟡 $0.317 | 41.8 | 132 | 1,048,576 | text+image+video |
| 5 | `deepseek/deepseek-v4-flash-vision-exp` | 🟡 $0.323 | 34.8 | 108 | 1,048,576 | text+image |
| 6 | `xiaomi/mimo-v2.6-pro` | 🟠 $0.544 | 46.3 | 85 | 1,050,000 | text+image+video+audio |
| 7 | `openai/gpt-5.6-luna` | 🟡 $0.450 | 37.3 | 83 | 1,050,000 | file+image+text |
| 8 | `deepseek/deepseek-v4.1-flash` | 🟠 $0.525 | 39.5 | 75 | 1,048,576 | text+image |
| 9 | `qwen/qwen3.8-27b` | 🟠 $0.605 | 33.7 | 56 | 1,000,000 | text+image+video |
| 10 | `google/gemini-3.8-flash` | 🔴 $1.500 | 40.9 | 27 | 1,048,576 | text+image+video+file+audio |


---

## ⚡ Simple Tasks / High Volume
_Cheapest models that still score ≥ 20 on intelligence_

| # | Model | $/1M | Intelligence idx | idx/$ | Context | In |
|---|-------|------|-----------|-------|---------|----|
| ⭐ 1 | `inclusionai/ling-3.0-flash-vl` | 🟢 $0.031 | 24.6 | 790 | 262,144 | text+image+video |
| ⭐ 2 | `inclusionai/ling-3.0-flash` | 🟢 $0.032 | 20.1 | 638 | 262,144 | text |
| ⭐ 3 | `inclusionai/ling-3.0-flash-fin` | 🟢 $0.062 | 22.6 | 363 | 262,144 | text |
| 4 | `upstage/solar-mini4` | 🟢 $0.087 | 24.1 | 275 | 524,288 | text |
| 5 | `upstage/solar-pro4` | 🟡 $0.158 | 28.2 | 179 | 524,288 | text |
| 6 | `deepseek/deepseek-v4-flash-0731` | 🟡 $0.172 | 34.3 | 199 | 1,048,576 | text |
| 7 | `xiaomi/mimo-v2.6-flash` | 🟡 $0.175 | 37.9 | 217 | 1,050,000 | text+image+video+audio |
| 8 | `xiaomi/mimo-v2.5` | 🟡 $0.175 | 25.2 | 144 | 1,050,000 | text+audio+image+video |
| 9 | `anthropic/claude-haiku-5.5` | 🟡 $0.200 | 43.4 | 217 | 1,000,000 | text+image+file |
| 10 | `openai/gpt-6-luna` | 🟡 $0.200 | 38.1 | 190 | 1,050,000 | file+image+text |


---

## 🧪 OpenRouter Evals

_OpenRouter's own evaluations — knowledge/reasoning and tool-calling accuracy._

> Source: OpenRouter evals (openrouter.ai) via OpenRouter (openrouter.ai/rankings).

### GPQA Diamond
_graduate-level science Q&A — accuracy, higher is better_

| # | Model | Accuracy | $/task | Runs |
|---|-------|----------|--------|------|
| 1 | `google/gemini-3.8-flash` | 95.6% | $0.0682 | 191 |
| 2 | `openai/gpt-6-astra-pro` | 95.5% | $0.3326 | 198 |
| 3 | `sakana/fugu-ultra` | 94.6% | $1.1487 | 198 |
| 4 | `google/gemini-3.1-pro-preview` | 94.5% | $0.2020 | 396 |
| 5 | `openai/gpt-6-astra` | 94.4% | $0.1133 | 198 |
| 6 | `openai/gpt-6.1-sol` | 94.4% | $0.0214 | 198 |
| 7 | `openai/gpt-5.6-sol-pro` | 93.9% | $0.2979 | 396 |
| 8 | `google/gemini-3.7-flash` | 93.9% | $0.0293 | 385 |
| 9 | `openai/gpt-5.5` | 93.7% | $0.3093 | 594 |
| 10 | `sakana/fugu-ultra-v2` | 93.3% | $0.5026 | 198 |
| 11 | `x-ai/grok-4.6` | 92.8% | $0.1233 | 396 |
| 12 | `google/gemini-3.6-flash` | 92.6% | $0.0596 | 594 |

### tau-bench (airline)
_tool-calling agent tasks — accuracy, higher is better_

| # | Model | Accuracy | $/task | Runs |
|---|-------|----------|--------|------|
| 1 | `xiaomi/mimo-v2.6-flash` | 79.7% | $0.0173 | 100 |
| 2 | `anthropic/claude-fable-5.1` | 79.2% | $0.7162 | 200 |
| 3 | `anthropic/claude-opus-5` | 78.7% | $0.4871 | 500 |
| 4 | `google/gemini-3.7-flash` | 78.5% | $0.1149 | 96 |
| 5 | `amazon/nova-micro-v1` | 78.0% | $1.2758 | 150 |
| 6 | `anthropic/claude-sonnet-5.5` | 78.0% | $0.1563 | 100 |
| 7 | `qwen/qwen3.8-27b` | 77.6% | $0.0758 | 350 |
| 8 | `deepseek/deepseek-v4-pro` | 77.4% | $0.1051 | 400 |
| 9 | `stepfun/step-3.7-flash` | 77.3% | $0.0201 | 50 |
| 10 | `qwen/qwen3.5-397b-a17b` | 77.2% | $0.1748 | 400 |
| 11 | `openai/gpt-5.1` | 77.1% | $0.4149 | 150 |
| 12 | `z-ai/glm-5.3` | 76.9% | $0.0619 | 300 |


---

## 🚀 Trending Apps

_Fastest-growing apps on OpenRouter by token growth vs. prior windows._

| # | App | Tokens | Requests |
|---|-----|--------|----------|
| 1 | Claude Code | 30,679,975,933,614 | 305,297,469 |
| 2 | Cline | 19,535,292,351,875 | 156,509,681 |
| 3 | Hermes Agent | 51,580,640,357,392 | 505,409,763 |
| 4 | Kilo Code | 22,264,637,743,257 | 266,153,612 |
| 5 | Codex | 11,637,868,014,881 | 145,845,329 |
| 6 | pi | 11,970,333,447,469 | 110,287,437 |
| 7 | omp | 10,197,171,380,901 | 67,872,723 |
| 8 | Freebuff | 8,271,861,148,116 | 63,201,910 |
| 9 | DeepSeek Harness | 5,847,442,746,724 | 39,324,526 |
| 10 | Command Code | 4,180,050,397,423 | 46,706,274 |
| 11 | OpenHands | 3,096,103,746,053 | 31,942,997 |
| 12 | OpenClaw | 6,175,105,902,946 | 78,715,803 |
| 13 | Strix | 1,682,790,601,129 | 13,970,582 |
| 14 | CodeGPT | 1,254,797,112,408 | 8,958,727 |
| 15 | ZCode | 1,892,557,200,522 | 10,010,227 |

*Source: OpenRouter (openrouter.ai/apps), as of 2026-10-12T12:22:56.502Z — CC BY 4.0.*


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

*Data source: OpenRouter (openrouter.ai). Usage figures from openrouter.ai/rankings (CC BY 4.0, as of 2026-10-12 12:22 UTC). Fork of Draxo-io/openrouter-ranking.*

---

## 🤖 Automation

Generated weekly by GitHub Actions (`.github/workflows/update-ranking.yml`).
Run manually: `python generate_ranking.py` (set `OPENROUTER_API_KEY` for the usage section).
