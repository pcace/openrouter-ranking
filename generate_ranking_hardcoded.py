#!/usr/bin/env python3
"""
OpenRouter LLM Cost-Effectiveness Ranking Generator
Fetches live pricing from OpenRouter API and generates a ranked README.md
organized by use case with cost-benefit analysis.

Usage: python generate_ranking.py [--output README.md]
"""

import json, urllib.request, sys, os
from datetime import datetime, timezone
from collections import defaultdict

OPENROUTER_API = "https://openrouter.ai/api/v1/models"
OUTPUT_FILE = "README.md"

# ── Task definitions ──────────────────────────────────────────────

TASKS = {
    "💬 Daily Chat / General Assistant": {
        "desc": "Conversations, Q&A, summaries, translation, creative writing",
        "models": [
            "deepseek/deepseek-v4-pro",
            "deepseek/deepseek-v3.2-exp",
            "qwen/qwen3.7-plus",
            "openai/gpt-5-mini",
            "x-ai/grok-4.3",
            "openai/gpt-5",
            "anthropic/claude-sonnet-4.5",
            "google/gemini-3.5-flash",
        ],
        "notes": {
            "deepseek/deepseek-v4-pro": "🔥 Best overall value. GPT-4o-class quality at flash prices.",
            "deepseek/deepseek-v3.2-exp": "DeepSeek experimental. Strong reasoning, cheap.",
            "qwen/qwen3.7-plus": "Qwen's mid-tier workhorse. 1M context, great value.",
            "openai/gpt-5-mini": "GPT-5 Mini. 400K context, affordable OpenAI quality.",
            "x-ai/grok-4.3": "Grok 4.3. 1M context, built-in web search.",
            "openai/gpt-5": "GPT-5. The gold standard for complex tasks.",
            "anthropic/claude-sonnet-4.5": "Claude Sonnet 4.5. 1M context, deep analysis.",
            "google/gemini-3.5-flash": "Gemini Flash. Native multimodal, 1M context.",
        }
    },
    "💻 Programming / Code": {
        "desc": "Code generation, debugging, code review, software architecture",
        "models": [
            "deepseek/deepseek-v4-pro",
            "qwen/qwen3-coder",
            "qwen/qwen3-coder-flash",
            "qwen/qwen3-coder-30b-a3b-instruct",
            "mistralai/codestral-2508",
            "x-ai/grok-build-0.1",
            "openai/gpt-5-codex",
            "anthropic/claude-sonnet-4.5",
        ],
        "notes": {
            "deepseek/deepseek-v4-pro": "🔥 Unbeatable: production-quality code at flash prices.",
            "qwen/qwen3-coder": "Dedicated 480B coder. 1M context.",
            "qwen/qwen3-coder-flash": "Coder Flash. Fast and efficient for code tasks.",
            "qwen/qwen3-coder-30b-a3b-instruct": "Ultra-cheap for simple code. $0.12/1M!",
            "mistralai/codestral-2508": "Mistral's Codestral. Code-focused, solid performance.",
            "x-ai/grok-build-0.1": "Grok Build. Optimized for software engineering.",
            "openai/gpt-5-codex": "GPT-5 Codex. OpenAI's top-tier coding model.",
            "anthropic/claude-sonnet-4.5": "Claude Sonnet. Excellent for refactoring and PR reviews.",
        }
    },
    "🧠 Complex Reasoning": {
        "desc": "Math, logic, science, step-by-step problem solving",
        "models": [
            "deepseek/deepseek-v4-pro",
            "qwen/qwen3-235b-a22b-thinking-2507",
            "deepseek/deepseek-v3.2-exp",
            "qwen/qwen3-next-80b-a3b-thinking",
            "qwen/qwen3.7-max",
            "openai/o4-mini",
            "anthropic/claude-opus-4.8",
            "openai/o3-pro",
        ],
        "notes": {
            "deepseek/deepseek-v4-pro": "🔥 Strong reasoning at lightweight model prices.",
            "qwen/qwen3-235b-a22b-thinking-2507": "235B MoE Thinking for $0.10/1M! The ultimate bargain.",
            "deepseek/deepseek-v3.2-exp": "Excellent on reasoning benchmarks.",
            "qwen/qwen3-next-80b-a3b-thinking": "80B MoE thinking, affordable.",
            "qwen/qwen3.7-max": "Qwen's top reasoning tier. 1M context.",
            "openai/o4-mini": "Accessible OpenAI reasoning.",
            "anthropic/claude-opus-4.8": "Anthropic's best. Pricey but unmatched depth.",
            "openai/o3-pro": "OpenAI's most powerful reasoning model.",
        }
    },
    "🔍 Research / Long Documents": {
        "desc": "Paper analysis, legal docs, long reports (requires >100K context)",
        "models": [
            "qwen/qwen3.7-plus",
            "google/gemini-3.5-flash",
            "anthropic/claude-sonnet-4.5",
            "deepseek/deepseek-v4-pro",
            "openai/gpt-5",
        ],
        "notes": {
            "qwen/qwen3.7-plus": "🔥 1M context for $0.70. Best value for long docs.",
            "google/gemini-3.5-flash": "Native multimodal, handles any format.",
            "anthropic/claude-sonnet-4.5": "Most precise and thorough document analysis.",
            "deepseek/deepseek-v4-pro": "Solid for medium docs (164K ctx).",
            "openai/gpt-5": "OpenAI quality, 400K context.",
        }
    },
    "🌐 Multimodal (Image/Video/Audio)": {
        "desc": "Image analysis, charts, screenshots, video understanding",
        "models": [
            "qwen/qwen3-vl-235b-a22b-instruct",
            "google/gemini-3.5-flash",
            "qwen/qwen3-vl-30b-a3b-instruct",
            "openai/gpt-5",
            "anthropic/claude-sonnet-4.5",
        ],
        "notes": {
            "qwen/qwen3-vl-235b-a22b-instruct": "🔥 235B MoE vision. Unbeatable price.",
            "google/gemini-3.5-flash": "Best multimodal: text+image+audio+video natively.",
            "qwen/qwen3-vl-30b-a3b-instruct": "Compact VL model, very cheap ($0.23/1M).",
            "openai/gpt-5": "Image+file support, OpenAI quality.",
            "anthropic/claude-sonnet-4.5": "Image+file support, precise analysis.",
        }
    },
    "⚡ Simple Tasks / High Volume": {
        "desc": "Classification, extraction, batch processing, repetitive tasks",
        "models": [
            "qwen/qwen3-235b-a22b-2507",
            "openai/gpt-5-nano",
            "google/gemini-2.5-flash-lite",
            "ibm-granite/granite-4.1-8b",
            "mistralai/mistral-small-3.2-24b-instruct",
            "meta-llama/llama-4-scout",
        ],
        "notes": {
            "qwen/qwen3-235b-a22b-2507": "🔥 Cheapest on the list! 235B for $0.09/1M.",
            "openai/gpt-5-nano": "OpenAI quality, cheap ($0.14/1M).",
            "google/gemini-2.5-flash-lite": "Google's budget option + 1M context.",
            "ibm-granite/granite-4.1-8b": "Extremely cheap. $0.06/1M.",
            "mistralai/mistral-small-3.2-24b-instruct": "24B multimodal, affordable.",
            "meta-llama/llama-4-scout": "10M context! Largest on the market.",
        }
    },
}


def fetch_models():
    """Fetch all models from OpenRouter API."""
    req = urllib.request.Request(OPENROUTER_API, headers={"User-Agent": "openrouter-ranking/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data["data"]


def build_model_index(models_data):
    """Build a lookup of model_id -> pricing info."""
    index = {}
    for m in models_data:
        mid = m["id"]
        p = m.get("pricing", {})
        prompt = float(p.get("prompt", 0))
        completion = float(p.get("completion", 0))

        # Skip free, router-only, or invalid pricing
        if ":free" in mid or prompt < 0 or completion < 0 or (prompt == 0 and completion == 0):
            continue

        mixed = prompt * 750_000 + completion * 250_000
        index[mid] = {
            "name": m["name"],
            "context": m.get("context_length", 0),
            "prompt_cost": prompt,
            "completion_cost": completion,
            "cost_per_1M": mixed,
            "ratio": completion / prompt if prompt > 0 else 0,
        }
    return index


def price_bar(cost):
    if cost < 0.15:
        return "🟢"
    elif cost < 0.50:
        return "🟡"
    elif cost < 1.50:
        return "🟠"
    else:
        return "🔴"


def format_price(price_per_token):
    """Format price per token to display as $X.XX/1M tokens equivalent in cents."""
    cost_1M = price_per_token * 1_000_000
    if cost_1M < 0.01:
        return f"${cost_1M:.4f}"
    elif cost_1M < 1:
        return f"${cost_1M:.2f}¢"
    else:
        return f"${cost_1M:.2f}"


def generate_tables(model_index):
    """Generate markdown tables for each task category."""
    sections = []

    for task_name, task_info in TASKS.items():
        lines = []
        lines.append(f"## {task_name}")
        lines.append(f"_{task_info['desc']}_")
        lines.append("")
        lines.append("| # | Model | $/1M Tokens | Prompt (¢/1M) | Compl (¢/1M) | P/C | Context | Notes |")
        lines.append("|---|--------|------------|--------------|--------------|-----|----------|------|")

        for i, mid in enumerate(task_info["models"]):
            m = model_index.get(mid)
            if not m:
                continue

            star = "⭐" if i < 3 else ""
            bar = price_bar(m["cost_per_1M"])
            note = task_info["notes"].get(mid, "")

            lines.append(
                f"| {star} {i+1} | `{mid}` | {bar} ${m['cost_per_1M']:.4f} | "
                f"${m['prompt_cost']*1_000_000:.2f} | ${m['completion_cost']*1_000_000:.2f} | "
                f"{m['ratio']:.1f}x | {m['context']:,} | {note} |"
            )

        lines.append("")
        sections.append("\n".join(lines))

    return sections


def generate_summary(model_index):
    """Generate executive summary with top picks."""
    top_models = [
        ("🥇 Best Overall", "deepseek/deepseek-v4-pro", "Best quality/price ratio across all categories."),
        ("🥈 Best Bargain", "qwen/qwen3-235b-a22b-2507", "235B parameters (MoE) for only $0.09/1M tokens."),
        ("🥉 Best All-Rounder", "qwen/qwen3.7-plus", "1M context, multimodal, versatile at $0.70/1M."),
    ]

    lines = [
        "## 🏆 Top 3 Overall",
        "",
        "| Position | Model | Why |",
        "|----------|------|-----|",
    ]
    for pos, mid, reason in top_models:
        m = model_index.get(mid, {})
        price = f"${m.get('cost_per_1M', 0):.2f}/1M" if m else "N/A"
        lines.append(f"| {pos} | `{mid}` ({price}) | {reason} |")

    lines.append("")
    return "\n".join(lines)


def generate_cheatsheet():
    """Generate the quick-reference cheat sheet."""
    tips = [
        ("💸 Cheapest possible?", "`qwen/qwen3-235b-a22b-2507` ($0.09/M) and `qwen/qwen3-235b-a22b-thinking-2507` ($0.10/M)"),
        ("⭐ Best all-rounder?", "`deepseek/deepseek-v4-pro` ($0.54/M) — does everything well"),
        ("📚 Need 1M context?", "`qwen/qwen3.7-plus` ($0.70/M)"),
        ("💻 Code?", "`qwen/qwen3-coder-flash` ($0.39/M) or `qwen/qwen3-coder` ($0.62/M)"),
        ("👁️ Multimodal / Vision?", "`qwen/qwen3-vl-235b-a22b-instruct` ($0.37/M)"),
        ("🏔️ No budget limit?", "`anthropic/claude-sonnet-4.5` ($6/M) or `openai/gpt-5` ($3.44/M)"),
    ]

    lines = [
        "## 💡 Quick Recommendations",
        "",
        "| Scenario | Best Pick |",
        "|----------|-----------|",
    ]
    for scenario, pick in tips:
        lines.append(f"| {scenario} | {pick} |")

    lines.append("")
    return "\n".join(lines)


def main():
    print("🔄 Fetching models from OpenRouter API...", file=sys.stderr)
    models_data = fetch_models()
    model_index = build_model_index(models_data)
    print(f"✅ Loaded {len(model_index)} paid models", file=sys.stderr)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    total_models = len(models_data)

    tables = generate_tables(model_index)
    summary = generate_summary(model_index)
    cheatsheet = generate_cheatsheet()
    joined_tables = "\n\n---\n\n".join(tables)

    readme = f"""# 🏆 OpenRouter LLM Cost-Effectiveness Ranking

[![Update Ranking](https://github.com/Draxo-io/openrouter-ranking/actions/workflows/update-ranking.yml/badge.svg)](https://github.com/Draxo-io/openrouter-ranking/actions/workflows/update-ranking.yml)
[![Last Updated](https://img.shields.io/badge/updated-{now.replace(' ', '%20')}-blue)](https://github.com/Draxo-io/openrouter-ranking)

> **Updated:** {now}  
> **Total models on OpenRouter:** {total_models}  
> **Paid models analyzed:** {len(model_index)}  
> **Methodology:** Price per 1M tokens (750K prompt + 250K completion). Data via [OpenRouter API](https://openrouter.ai/api/v1/models).

---

## 📖 About

This ranking is generated **automatically every week** and orders models available on [OpenRouter](https://openrouter.ai) by **cost-effectiveness**, organized by real-world use cases:

- 💬 Daily chat and general assistant
- 💻 Programming and code
- 🧠 Complex reasoning (math, logic)
- 🔍 Research and long document analysis
- 🌐 Multimodal (image, video, audio)
- ⚡ Simple tasks and high volume

**Prices in USD.** Symbols: 🟢 cheap (<$0.15/M) 🟡 medium ($0.15-$0.50/M) 🟠 premium ($0.50-$1.50/M) 🔴 elite (>$1.50/M).

⭐ = Top 3 recommendations per category.

---

{summary}

---

{cheatsheet}

---

{joined_tables}

---

## 🔧 Methodology

- **Source:** [OpenRouter API](https://openrouter.ai/api/v1/models) (real-time data)
- **Cost formula:** `(prompt_price × 750,000) + (completion_price × 250,000)` = cost per 1M tokens
- **Ratio:** Assumes 75% prompt / 25% completion (typical chat usage)
- **Ranking:** Ordered by cost-effectiveness within each category, not just price
- **Updates:** Weekly (via GitHub Actions)

---

## 🤖 Automation

This repository is updated automatically via:
- **GitHub Actions:** Every Monday at 12:00 UTC
- **Hermes Agent:** Weekly cron job that generates and publishes the ranking

To run manually: `python generate_ranking.py`

---

*Created by [@Draxo-io](https://github.com/Draxo-io) · [draxo.io](https://draxo.io)*
"""

    output = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_FILE
    with open(output, "w") as f:
        f.write(readme)

    print(f"✅ Written to {output}", file=sys.stderr)


if __name__ == "__main__":
    main()
