#!/usr/bin/env python3
"""
OpenRouter LLM Ranking Generator (dynamic)

Fetches the live model catalog from OpenRouter and ranks models per use case by
cost-effectiveness, where effectiveness comes from real benchmark scores that the
OpenRouter API embeds in every model object (Artificial Analysis indices and
Design Arena ELO). No model lists are hardcoded; categories are defined by a
metric + filter, so new/removed models appear automatically.

Usage: python generate_ranking_dynamic.py [--output README.md] [--api-key KEY]
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

MODELS_API = "https://openrouter.ai/api/v1/models"
RANKINGS_API = "https://openrouter.ai/api/v1/datasets/rankings-daily"
PROMPT_TOKENS = 750_000
COMPLETION_TOKENS = 250_000
USAGE_WINDOW_DAYS = 7

# Category definitions are pure predicates over model metadata + a metric to rank by.
# "value" = metric_per_dollar = benchmark_index / blended_price_1M (higher is better).
CATEGORIES = [
    {
        "name": "💬 General Assistant",
        "desc": "Everyday chat, Q&A, summaries, translation",
        "metric": "intelligence",
        "filter": lambda m: True,
        "sort": "value",
        "floor": 0.55,
    },
    {
        "name": "💻 Programming / Code",
        "desc": "Code generation, debugging, review",
        "metric": "coding",
        "filter": lambda m: True,
        "sort": "value",
        "floor": 0.70,
    },
    {
        "name": "🧠 Complex Reasoning",
        "desc": "Math, logic, step-by-step problem solving",
        "metric": "intelligence",
        "filter": lambda m: "reasoning" in m["supported_parameters"],
        "sort": "value",
        "floor": 0.75,
    },
    {
        "name": "🤖 Agentic / Tool Use",
        "desc": "Multi-step agents, function calling, computer use",
        "metric": "agentic",
        "filter": lambda m: "tools" in m["supported_parameters"],
        "sort": "value",
        "floor": 0.70,
    },
    {
        "name": "🔍 Research / Long Documents",
        "desc": "Paper analysis, long reports (context ≥ 200K)",
        "metric": "intelligence",
        "filter": lambda m: m["context"] >= 200_000,
        "sort": "value",
        "floor": 0.60,
    },
    {
        "name": "🌐 Multimodal (Image/Video/Audio input)",
        "desc": "Image analysis, charts, screenshots, video",
        "metric": "intelligence",
        "filter": lambda m: bool({"image", "video", "audio"} & set(m["input_modalities"])),
        "sort": "value",
        "floor": 0.55,
    },
    {
        "name": "⚡ Simple Tasks / High Volume",
        "desc": "Cheapest models that still score ≥ 20 on intelligence",
        "metric": "intelligence",
        "filter": lambda m: (m["intelligence"] or 0) >= 20,
        "sort": "price",
    },
]

TOP_N = 10

VARIANT_SUFFIXES = (":free", ":extended", ":nitro", ":floor", ":online", ":thinking", ":beta", ":batch")


def load_env_file(path=".env"):
    """Populate os.environ from a local .env. CI provides real env vars instead."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def fetch_models(api_key=None):
    headers = {"User-Agent": "openrouter-ranking/2.0"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(MODELS_API, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())["data"]


def fetch_usage(api_key):
    """Top models by token usage over the last USAGE_WINDOW_DAYS (needs an API key).

    Returns {permaslug: total_tokens}. Data: OpenRouter (openrouter.ai/rankings), CC BY 4.0.
    """
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=USAGE_WINDOW_DAYS)
    url = f"{RANKINGS_API}?start_date={start}&end_date={end}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "openrouter-ranking/2.0",
        "Authorization": f"Bearer {api_key}",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        rows = json.loads(resp.read())["data"]

    usage = {}
    for row in rows:
        slug = row["model_permaslug"]
        if slug == "other":
            continue
        usage[slug] = usage.get(slug, 0) + int(row["total_tokens"])
    return usage


def match_usage_to_family(permaslug, models):
    """Best-effort join of a rankings permaslug (e.g. `openai/gpt-4o-2024-05-13:free`)
    onto a model family id (`openai/gpt-4o`) by longest prefix match."""
    slug = permaslug.split(":", 1)[0]
    if slug in models:
        return slug
    best = None
    for cid in models:
        if slug.startswith(cid) or cid.startswith(slug):
            if best is None or len(cid) > len(best):
                best = cid
    return best


def canonical_id(mid):
    """Collapse routing/alias variants (~alias, model:variant) to one family id."""
    if mid.startswith("~"):
        mid = mid[1:]
    if ":" in mid:
        mid = mid.split(":", 1)[0]
    return mid


def build_index(models_data):
    """Group variants, keep one representative per family, attach benchmark scores."""
    families = {}
    for m in models_data:
        mid = m["id"]
        if mid.startswith("~"):
            continue  # alias, not a real model
        p = m.get("pricing") or {}
        try:
            prompt = float(p.get("prompt", 0))
            completion = float(p.get("completion", 0))
        except (TypeError, ValueError):
            continue
        if prompt < 0 or completion < 0:
            continue  # router / invalid pricing
        if prompt == 0 and completion == 0:
            continue  # genuinely free endpoints: no cost-effectiveness to rank

        cid = canonical_id(mid)
        cost_1m = prompt * PROMPT_TOKENS + completion * COMPLETION_TOKENS
        aa = (m.get("benchmarks") or {}).get("artificial_analysis") or {}
        design = (m.get("benchmarks") or {}).get("design_arena") or []

        entry = {
            "id": mid,
            "name": m["name"],
            "context": m.get("context_length", 0),
            "prompt_cost": prompt,
            "completion_cost": completion,
            "cost_1m": cost_1m,
            "intelligence": aa.get("intelligence_index"),
            "coding": aa.get("coding_index"),
            "agentic": aa.get("agentic_index"),
            "design_elo": max((d.get("elo", 0) for d in design), default=None),
            "input_modalities": (m.get("architecture") or {}).get("input_modalities") or [],
            "supported_parameters": m.get("supported_parameters") or [],
            "is_free_variant": mid.endswith(VARIANT_SUFFIXES),
        }
        # Prefer the plain family entry (no routing suffix); otherwise the cheapest variant.
        entry["is_variant"] = mid != cid
        prev = families.get(cid)
        if prev is None or (prev["is_variant"] and not entry["is_variant"]) or (
            prev["is_variant"] == entry["is_variant"] and entry["cost_1m"] < prev["cost_1m"]
        ):
            families[cid] = entry
    return families


def price_bar(cost):
    if cost < 0.15:
        return "🟢"
    if cost < 0.50:
        return "🟡"
    if cost < 1.50:
        return "🟠"
    return "🔴"


def rank(models, category):
    metric = category["metric"]
    eligible = [m for m in models.values() if category["filter"](m) and m.get(metric) is not None]
    if not eligible:
        return []
    # Quality floor: keep only models within `floor` of the category's best score, so
    # the ranking rewards value among *competitive* models rather than the absolute
    # cheapest weak model.
    floor = category.get("floor", 0.0)
    best_score = max(m[metric] for m in eligible)
    candidates = [m for m in eligible if m[metric] >= floor * best_score]
    if category["sort"] == "price":
        candidates.sort(key=lambda m: (m["cost_1m"], -m[metric]))
    else:
        candidates.sort(key=lambda m: m["cost_1m"] / m[metric])
    return candidates[:TOP_N]


def fmt_cost(m):
    return f"{price_bar(m['cost_1m'])} ${m['cost_1m']:.3f}"


def render_table(category, ranked, models):
    metric = category["metric"]
    label = {"intelligence": "Intelligence", "coding": "Coding", "agentic": "Agentic"}[metric]
    out = [f"## {category['name']}", f"_{category['desc']}_", ""]
    out.append(f"| # | Model | $/1M | {label} idx | {'Value' if category['sort']=='value' else 'idx/$'} | Context | In |")
    out.append("|---|-------|------|-----------|-------|---------|----|")
    for i, m in enumerate(ranked, 1):
        score = m[metric]
        value = score / m["cost_1m"]
        inputs = "+".join(m["input_modalities"]) or "text"
        star = "⭐ " if i <= 3 else ""
        out.append(
            f"| {star}{i} | `{m['id']}` | {fmt_cost(m)} | {score:.1f} | "
            f"{value:,.0f} | {m['context']:,} | {inputs} |"
        )
    out.append("")
    return "\n".join(out)


def render_top_overall(models):
    scored = [m for m in models.values() if m["intelligence"] is not None]
    best_abs = max(scored, key=lambda m: m["intelligence"])
    # "Best value" only among models within 60% of the top score, so it reflects a
    # strong model rather than the cheapest weak one.
    competitive = [m for m in scored if m["intelligence"] >= 0.6 * best_abs["intelligence"]]
    best_value = max(competitive, key=lambda m: m["intelligence"] / m["cost_1m"])
    cheapest = min((m for m in models.values() if (m["intelligence"] or 0) >= 20), key=lambda m: m["cost_1m"])
    rows = [
        ("🥇 Best value", best_value, f"{best_value['intelligence']:.0f} intelligence for {best_value['cost_1m']:.3f}/1M"),
        ("🥈 Highest score", best_abs, f"{best_abs['intelligence']:.0f} intelligence (absolute top)"),
        ("🥉 Cheapest usable", cheapest, f"${cheapest['cost_1m']:.3f}/1M at {cheapest['intelligence']:.0f} intelligence"),
    ]
    out = ["## 🏆 Top Picks (computed, not curated)", "", "| | Model | Why |", "|---|-------|-----|"]
    for pos, m, why in rows:
        out.append(f"| {pos} | `{m['id']}` | {why} |")
    out.append("")
    return "\n".join(out)


def render_usage_section(usage, models, top=15):
    """What people actually run, vs. what's best value."""
    ranked = sorted(usage.items(), key=lambda kv: kv[1], reverse=True)[:top]
    if not ranked:
        return None
    total = sum(usage.values())
    out = [f"## 📈 Most Used (last {USAGE_WINDOW_DAYS} days, by tokens)", "",
           "_Real OpenRouter traffic — what is actually being run, not what is best value._", "",
           "| # | Model | Share | $/1M | Intelligence |", "|---|-------|-------|------|--------------|"]
    for i, (slug, tokens) in enumerate(ranked, 1):
        cid = match_usage_to_family(slug, models)
        m = models.get(cid) if cid else None
        share = f"{100 * tokens / total:.1f}%" if total else "?"
        cost = f"${m['cost_1m']:.3f}" if m else "—"
        intel = f"{m['intelligence']:.1f}" if m and m["intelligence"] is not None else "—"
        out.append(f"| {i} | `{slug}` | {share} | {cost} | {intel} |")
    out.append("")
    return "\n".join(out)


def build_readme(models, now, total_models, usage=None):
    scored = sum(1 for m in models.values() if m["intelligence"] is not None)
    sections = [render_top_overall(models)]
    if usage:
        usage_section = render_usage_section(usage, models)
        if usage_section:
            sections.append(usage_section)
    for cat in CATEGORIES:
        ranked = rank(models, cat)
        if ranked:
            sections.append(render_table(cat, ranked, models))

    return f"""# 🏆 OpenRouter LLM Cost-Effectiveness Ranking

> **Updated:** {now}
> **Models on OpenRouter:** {total_models} · **Families priced:** {len(models)} · **With benchmark scores:** {scored}
> **Methodology:** value = benchmark index ÷ blended price per 1M tokens ({PROMPT_TOKENS // 1000}K prompt + {COMPLETION_TOKENS // 1000}K completion). Data via [OpenRouter API]({MODELS_API}).

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

""" + "\n\n---\n\n".join(sections) + f"""

---

## 🔧 Methodology

- **Source:** [OpenRouter API]({MODELS_API}) — live catalog incl. benchmark scores
- **Cost formula:** `prompt_price × {PROMPT_TOKENS:,} + completion_price × {COMPLETION_TOKENS:,}`
- **Value:** `benchmark_index / cost_per_1M` (higher is better); ranked descending
- **Family collapse:** routing/alias variants (`:free`, `:nitro`, `~alias`) are merged
  into their base model family, keeping the cheapest representative
- **Coverage:** models without a benchmark score are skipped in metric-based
  categories rather than guessed at
- **Updates:** weekly via GitHub Actions

---

*Data source: OpenRouter (openrouter.ai). Usage figures from openrouter.ai/rankings (CC BY 4.0, as of {now}). Fork of Draxo-io/openrouter-ranking.*

---

## 🤖 Automation

Generated weekly by GitHub Actions (`.github/workflows/update-ranking.yml`).
Run manually: `python generate_ranking.py` (set `OPENROUTER_API_KEY` for the usage section).
"""


def main():
    load_env_file()
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="README.md")
    ap.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY"),
                    help="or set OPENROUTER_API_KEY; only needed for the usage section")
    args = ap.parse_args()

    print("🔄 Fetching live catalog from OpenRouter…", file=sys.stderr)
    data = fetch_models(args.api_key)
    models = build_index(data)
    print(f"✅ {len(data)} models → {len(models)} priced families", file=sys.stderr)

    usage = None
    if args.api_key:
        try:
            usage = fetch_usage(args.api_key)
            print(f"✅ Usage data: {len(usage)} models over {USAGE_WINDOW_DAYS} days", file=sys.stderr)
        except Exception as e:
            print(f"⚠️  Usage section skipped ({e})", file=sys.stderr)
    else:
        print("ℹ️  No API key → skipping usage section (set OPENROUTER_API_KEY)", file=sys.stderr)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    readme = build_readme(models, now, len(data), usage)
    with open(args.output, "w") as f:
        f.write(readme)
    print(f"✅ Written to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
