#!/usr/bin/env python3
"""
Goose config generator for OpenRouter coding models.

Produces, from the live OpenRouter catalog, everything needed to keep a Goose
setup current: a custom provider with correct context/pricing, and a
GOOSE_PREDEFINED_MODELS payload so the model picker shows a readable name plus
price/context per model.

Outputs (into ./goose):
  openrouter_code.json     -> copy to ~/.config/goose/custom_providers/
  predefined_models.json   -> content of the GOOSE_PREDEFINED_MODELS env var
  config.snippet.yaml      -> providers: entry to merge into config.yaml
  README.md                -> setup instructions

Usage: python generate_goose_config.py [--api-key KEY] [--out DIR]
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

MODELS_API = "https://openrouter.ai/api/v1/models"
RANKINGS_API = "https://openrouter.ai/api/v1/datasets/rankings-daily"

PROVIDER_ID = "openrouter_code"
PROVIDER_DISPLAY = "OpenRouter · Code"
API_KEY_ENV = "OPENROUTER_API_KEY"
BASE_URL = "https://openrouter.ai/api/v1"

MIN_CONTEXT = 128_000
MAX_MODELS = 10
USAGE_WINDOW_DAYS = 7

# Models to keep if they still qualify — the user's current favourites.
PINNED = ["deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3"]

# Price tiers (USD per 1M blended tokens) and how many to pick from each.
TIERS = [("cheap", 0.0, 0.20, 3), ("mid", 0.20, 0.80, 3)]
PREMIUM_MAX = 5.0  # best-quality pick must stay under this $/1M
MAX_PER_ORG = 2

PATRONYM = {  # org -> pretty label for the alias
    "deepseek": "DeepSeek", "z-ai": "GLM", "qwen": "Qwen", "openai": "OpenAI",
    "anthropic": "Claude", "google": "Gemini", "x-ai": "Grok", "moonshotai": "Kimi",
    "meta": "Llama", "mistralai": "Mistral", "minimax": "MiniMax", "tencent": "Hunyuan",
    "stepfun": "StepFun", "xiaomi": "MiMo", "upstage": "Solar", "inclusionai": "Ling",
}

PROMPT_TOKENS = 750_000
COMPLETION_TOKENS = 250_000


def _get_json(url, api_key=None):
    headers = {"User-Agent": "openrouter-ranking/goose-config"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def load_env_file(path=".env"):
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def canonical_id(mid):
    if mid.startswith("~"):
        mid = mid[1:]
    return mid.split(":", 1)[0]


KEEP_UPPER = {"vl", "llm", "gpt", "oss", "ai", "moe", "qa", "api"}


def _tidy(name):
    out = []
    for w in name.split():
        if w.lower() in KEEP_UPPER:
            out.append(w.upper())
        elif w.islower() and len(w) > 2:
            out.append(w.capitalize())
        else:
            out.append(w)
    return " ".join(out)


def pretty_alias(model_id, api_name):
    """Human-friendly display name, e.g. 'DeepSeek V4.1 Flash'."""
    org_name, _, slug = model_id.partition("/")
    label = PATRONYM.get(org_name)
    name = api_name.split(":", 1)[1].strip() if api_name and ":" in api_name else slug
    if label:
        name = re.sub(rf"^{re.escape(label)}\b[\s\-]*", "", name, flags=re.I)
    name = _tidy(name.replace("-", " ").replace("_", " ").strip())
    return f"{label} {name}".strip() if label else name


def org_of(mid):
    return mid.split("/", 1)[0]


def fmt_ctx(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M".replace(".0M", "M")
    return f"{n // 1000}K"


def build_index(models):
    families = {}
    for m in models:
        mid = m["id"]
        if mid.startswith("~"):
            continue
        p = m.get("pricing") or {}
        try:
            prompt, completion = float(p.get("prompt", 0)), float(p.get("completion", 0))
        except (TypeError, ValueError):
            continue
        if prompt <= 0 or completion <= 0:
            continue
        aa = (m.get("benchmarks") or {}).get("artificial_analysis") or {}
        cid = canonical_id(mid)
        cost = prompt * PROMPT_TOKENS + completion * COMPLETION_TOKENS

        def _num(v):
            try:
                return float(v)
            except (TypeError, ValueError):
                return 0.0

        cache = _num(p.get("input_cache_read")) > 0 or _num(p.get("input_cache_write")) > 0
        entry = {
            "cid": cid,
            "id": mid, "api_name": m["name"], "context": m.get("context_length", 0),
            "prompt_cost": prompt, "completion_cost": completion, "cost_1m": cost,
            "coding": aa.get("coding_index"), "intelligence": aa.get("intelligence_index"),
            "tools": "tools" in (m.get("supported_parameters") or []),
            "reasoning": bool(m.get("reasoning")),
            "input_modalities": (m.get("architecture") or {}).get("input_modalities") or [],
            "cache": cache,
            "is_variant": mid != cid,
        }
        prev = families.get(cid)
        if prev is None or (prev["is_variant"] and not entry["is_variant"]) or (
            prev["is_variant"] == entry["is_variant"] and entry["cost_1m"] < prev["cost_1m"]
        ):
            families[cid] = entry
    return families


def fetch_usage(api_key, models):
    """Returns ({family_id: tokens}, grand_total) over the usage window.

    The dataset lists the top-50 models per day plus an aggregated ``other`` row,
    so the grand total (including ``other``) is the right denominator for a share.
    """
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=USAGE_WINDOW_DAYS)
    try:
        rows = _get_json(f"{RANKINGS_API}?start_date={start}&end_date={end}", api_key)["data"]
    except Exception as e:
        print(f"⚠️  Usage data unavailable ({e}); picking without popularity", file=sys.stderr)
        return {}, 0
    usage, total = {}, 0
    for row in rows:
        tokens = int(row["total_tokens"])
        total += tokens
        if row["model_permaslug"] == "other":
            continue
        slug = row["model_permaslug"].split(":", 1)[0]
        best = max((cid for cid in models if slug.startswith(cid) or cid.startswith(slug)),
                   key=len, default=None)
        if best:
            usage[best] = usage.get(best, 0) + tokens
    return usage, total


def humanize_tokens(n):
    if n >= 1e12:
        return f"{n / 1e12:.1f}T"
    if n >= 1e9:
        return f"{n / 1e9:.1f}B"
    if n >= 1e6:
        return f"{n / 1e6:.0f}M"
    return str(n)


def select(models, usage):
    """Pick ≤ MAX_MODELS coding models: pinned + best value per tier + best quality + popular."""
    def qualifies(m):
        return m["tools"] and m["context"] >= MIN_CONTEXT and (
            m["coding"] is not None or m["intelligence"] is not None)

    def score(m):
        return m["coding"] if m["coding"] is not None else (m["intelligence"] or 0)

    pool = [m for m in models.values() if qualifies(m)]
    value = lambda m: score(m) / m["cost_1m"]

    chosen, why = {}, {}

    def take(m, reason, diversify=True):
        if not m or m["id"] in chosen:
            return False
        if diversify and sum(1 for c in chosen.values() if org_of(c["id"]) == org_of(m["id"])) >= MAX_PER_ORG:
            return False
        chosen[m["id"]] = m
        why[m["id"]] = reason
        return True

    for pid in PINNED:
        cand = next((m for m in models.values()
                     if qualifies(m) and (canonical_id(m["id"]) == pid or m["id"] == pid)), None)
        take(cand, "your current model", diversify=False)

    for name, lo, hi, n in TIERS:
        taken = 0
        for m in sorted((m for m in pool if lo <= m["cost_1m"] < hi), key=value, reverse=True):
            if taken >= n:
                break
            if take(m, f"best {name}-tier value (${lo:.2f}–${hi:.2f}/1M)"):
                taken += 1

    premium = [m for m in pool if m["cost_1m"] <= PREMIUM_MAX]
    if premium:
        take(max(premium, key=score), f"best quality under ${PREMIUM_MAX:.0f}/1M", diversify=False)

    for m in sorted((m for m in pool if m["cid"] in usage),
                    key=lambda m: usage[m["cid"]], reverse=True)[:3]:
        take(m, f"widely used ({humanize_tokens(usage[m['cid']])} tok/7d)")

    take(max(pool, key=value), "best overall coding value", diversify=False)

    return sorted(chosen.values(), key=lambda m: m["cost_1m"])[:MAX_MODELS], why


def provider_json(models):
    return {
        "name": PROVIDER_ID,
        "engine": "openai",
        "display_name": PROVIDER_DISPLAY,
        "description": "Curated OpenRouter coding models, regenerated weekly.",
        "api_key_env": API_KEY_ENV,
        "base_url": BASE_URL,
        "models": [
            {
                "name": m["id"],
                "context_limit": m["context"],
                "input_token_cost": m["prompt_cost"],
                "output_token_cost": m["completion_cost"],
                "currency": None,
                "supports_cache_control": True if m["cache"] else None,
                "reasoning": m["reasoning"],
            }
            for m in models
        ],
        "headers": None,
        "timeout_seconds": None,
        "supports_streaming": True,
        "requires_auth": True,
        "catalog_provider_id": "openrouter",
        "base_path": None,
        "env_vars": None,
        "dynamic_models": False,
        "skip_canonical_filtering": False,
        "model_doc_link": None,
        "setup_steps": [],
        "preserves_thinking": True,
    }


MODALITY_TAG = {"image": "img", "video": "vid", "audio": "aud", "file": "pdf"}


def modality_tags(m):
    """Non-text input modalities, e.g. 'img+vid'."""
    extra = [MODALITY_TAG.get(x, x) for x in m["input_modalities"] if x != "text"]
    return "+".join(extra)


def predefined_models(models, usage, total):
    out = []
    for m in models:
        parts = [f"${m['cost_1m']:.2f}/1M", f"{fmt_ctx(m['context'])} ctx"]
        if m["coding"] is not None:
            parts.append(f"code {m['coding']:.0f}")
        elif m["intelligence"] is not None:
            parts.append(f"iq {m['intelligence']:.0f}")
        else:
            parts.append("unrated")
        tokens = usage.get(m["cid"])
        if tokens:
            parts.append(f"{humanize_tokens(tokens)} tok/{USAGE_WINDOW_DAYS}d · {100 * tokens / total:.1f}%")
        tags = modality_tags(m)
        if tags:
            parts.append(f"in: {tags}")
        out.append({
            "name": m["id"],
            "provider": PROVIDER_ID,
            "alias": pretty_alias(m["id"], m["api_name"]),
            "subtext": " · ".join(parts),
            "context_limit": m["context"],
            "reasoning": m["reasoning"],
        })
    return out


def write_readme(out_dir, selected, why, now, usage, total):
    def row(m):
        alias = pretty_alias(m["id"], m["api_name"])
        code = f"{m['coding']:.0f}" if m["coding"] is not None else "n/a"
        tokens = usage.get(m["cid"])
        used = f"{humanize_tokens(tokens)} ({100 * tokens / total:.1f}%)" if tokens else "—"
        return (f"| `{m['id']}` | {alias} | ${m['cost_1m']:.2f} | {code} | "
                f"{m['context']:,} | {used} | {modality_tags(m) or 'text'} | {why.get(m['id'], '')} |")

    rows = "\n".join(row(m) for m in selected)
    readme = f"""# Goose config — OpenRouter coding models

Generated **{now}**. {len(selected)} models, selected from the live OpenRouter
catalog by coding score, price and real usage. Token figures are the last
{USAGE_WINDOW_DAYS} days (share of all OpenRouter traffic in the window).

| Model | Name in picker | $/1M | Coding | Context | Tokens (7d) | In | Why |
|-------|----------------|------|--------|---------|-------------|----|-----|
{rows}

## Install

```bash
./goose/install.sh            # copies provider + patches config.yaml (with backup)
```

Then make the picker show names + prices. The desktop app reads
GOOSE_PREDEFINED_MODELS from its environment, so it must be set before launch:

  export GOOSE_PREDEFINED_MODELS="$(cat ~/git/openrouter-ranking/goose/predefined_models.min.json)"

The API key is read from the `{API_KEY_ENV}` secret in Goose's keyring
(`goose configure` → your provider), same as any other OpenRouter setup.

## Update weekly

```bash
cd ~/git/openrouter-ranking && git pull && ./goose/install.sh
```
"""
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write(readme)


def main():
    load_env_file()
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY"))
    ap.add_argument("--out", default="goose")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    print("🔄 Fetching OpenRouter catalog…", file=sys.stderr)
    models = build_index(_get_json(MODELS_API)["data"])
    usage, total = fetch_usage(args.api_key, models) if args.api_key else ({}, 0)
    selected, why = select(models, usage)
    print(f"✅ {len(selected)} models selected: {', '.join(m['id'] for m in selected)}", file=sys.stderr)

    with open(os.path.join(args.out, "openrouter_code.json"), "w") as f:
        json.dump(provider_json(selected), f, indent=2)
        f.write("\n")

    pre = predefined_models(selected, usage, total)
    with open(os.path.join(args.out, "predefined_models.json"), "w") as f:
        json.dump(pre, f, indent=2)
        f.write("\n")

    # Single-line copy: GOOSE_PREDEFINED_MODELS is an env var, so it must not
    # contain newlines.
    with open(os.path.join(args.out, "predefined_models.min.json"), "w") as f:
        f.write(json.dumps(pre, separators=(",", ":")))

    first = selected[0]["id"]
    snippet = (
        "# merge under the top-level `providers:` key in ~/.config/goose/config.yaml\n"
        "providers:\n"
        f"  {PROVIDER_ID}:\n"
        "    enabled: true\n"
        f"    model: {first}\n"
        "    configured: true\n"
    )
    with open(os.path.join(args.out, "config.snippet.yaml"), "w") as f:
        f.write(snippet)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    write_readme(args.out, selected, why, now, usage, total)
    print(f"✅ Wrote {args.out}/ (provider, predefined models, snippet, README)", file=sys.stderr)


if __name__ == "__main__":
    main()
