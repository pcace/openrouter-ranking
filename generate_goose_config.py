#!/usr/bin/env python3
"""
Goose config generator for OpenRouter models.

Produces, from the live OpenRouter catalog, everything needed to keep a Goose
setup current: a custom provider with correct context/pricing, and a
GOOSE_PREDEFINED_MODELS payload so the model picker shows a readable name plus
price/context per model.

Two selection modes (--mode):

  curated  (default) affordable models people actually run: pinned daily
           drivers, the most used models of the cheap (<$0.30/1M) and mid
           ($0.30–$0.80/1M) tier plus their best value, and one or two strong
           models on top (best under $2.00 and under $3.50). Traffic comes from
           the OpenRouter usage dataset of the last 7 days.

  newest   strictly by release date: the N newest models (`created` timestamp).
           Useful to try fresh releases, useless for a stable setup.

Outputs (into ./goose):
  openrouter_code.json     -> copy to ~/.config/goose/custom_providers/
  predefined_models.json   -> content of the GOOSE_PREDEFINED_MODELS env var
  config.snippet.yaml      -> providers: entry to merge into config.yaml
  README.md                -> setup instructions

Usage:
  python generate_goose_config.py [--api-key KEY] [--out DIR]
  python generate_goose_config.py --verify                     # default mode
  python generate_goose_config.py --mode newest --newest 5
  python generate_goose_config.py --also z-ai/glm-5.3-flash    # keep a favourite
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

MODELS_API = "https://openrouter.ai/api/v1/models"
CHAT_API = "https://openrouter.ai/api/v1/chat/completions"
RANKINGS_API = "https://openrouter.ai/api/v1/datasets/rankings-daily"
REPO_RAW_URL = "https://raw.githubusercontent.com/pcace/openrouter-ranking/main/goose"

PROVIDER_ID = "openrouter_code"
PROVIDER_DISPLAY = "OpenRouter · Code"
API_KEY_ENV = "OPENROUTER_API_KEY"
BASE_URL = "https://openrouter.ai/api/v1"

MIN_CONTEXT = 128_000
USAGE_WINDOW_DAYS = 7

# --- selection knobs --------------------------------------------------------
SELECTION_MODE = "curated"   # "curated" (default) | "newest"
NEWEST_COUNT = 5             # models in newest mode

# The curated list is affordable and follows what people actually run on
# OpenRouter, with one or two strong models on top. USD per 1M blended tokens.
MAX_MODELS = 9               # total size of the list
CHEAP_TIER = (0.0, 0.30)     # "cheap": DeepSeek Flash / GLM Flash territory
MID_TIER = (0.30, 0.80)
CHEAP_CROWD, CHEAP_VALUE = 2, 1
MID_CROWD, MID_VALUE = 1, 1
QUALITY_CAPS = (2.00, 3.50)  # one strong model per cap: solid + the best affordable
MAX_PER_ORG = 2

# Kept regardless of price tiers — the models you run every day.
PINNED = ["deepseek/deepseek-v4.1-flash", "z-ai/glm-5.3-flash"]

PATRONYM = {  # org -> pretty label for the alias
    "deepseek": "DeepSeek", "z-ai": "GLM", "qwen": "Qwen", "openai": "OpenAI",
    "anthropic": "Claude", "google": "Gemini", "x-ai": "Grok", "moonshotai": "Kimi",
    "mistralai": "Mistral", "minimax": "MiniMax", "tencent": "Hunyuan",
    "stepfun": "StepFun", "xiaomi": "MiMo", "upstage": "Solar", "inclusionai": "Ling",
}

PROMPT_TOKENS = 750_000
COMPLETION_TOKENS = 250_000


def _get_json(url, api_key=None):
    headers = {"User-Agent": "openrouter-ranking/goose-config"}
    if api_key:
        # keys copied around often carry a trailing newline — a raw one breaks
        # the header ("Invalid header value") and silently drops the usage data
        headers["Authorization"] = f"Bearer {api_key.strip()}"
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
        if prompt < 0 or completion < 0:
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
            "created": int(m.get("created") or 0),
            "prompt_cost": prompt, "completion_cost": completion, "cost_1m": cost,
            "free": prompt == 0 and completion == 0,
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


def select(models, usage, total=0, api_key=None, verify=False):
    """Affordable models people actually run, with one or two strong ones on top.

    Slot by slot, in priority order:

      1. PINNED    — your daily drivers, always kept
      2. cheap tier (below $0.30/1M) — the models with the most traffic, then
                     the best value (coding score per dollar)
      3. mid tier ($0.30–$0.80/1M) — one by traffic, one by value
      4. quality   — the best scoring model under $2.00 and under $3.50

    Every slot falls through to the next candidate when a model is already in
    the list, breaks MAX_PER_ORG, or — with `verify` — cannot be reached by this
    account (e.g. excluded by a zero-data-retention rule).
    """
    def qualifies(m):
        return (m["tools"] and m["context"] >= MIN_CONTEXT and m["cost_1m"] > 0
                and (m["coding"] is not None or m["intelligence"] is not None))

    def score(m):
        return m["coding"] if m["coding"] is not None else (m["intelligence"] or 0)

    def value(m):
        return score(m) / m["cost_1m"]

    def used(m):
        return usage.get(m["cid"], 0)

    def traffic(m):
        share = f" · {100 * used(m) / total:.1f}%" if total else ""
        return f" · {humanize_tokens(used(m))} tok/{USAGE_WINDOW_DAYS}d{share}"

    pool = [m for m in models.values() if qualifies(m)]
    chosen, why = [], {}

    def take(candidates, reason, slots=1, diversify=True):
        """Fill `slots` from `candidates` in the given order."""
        filled = 0
        for m in candidates:
            if filled >= slots or len(chosen) >= MAX_MODELS:
                return
            if any(c["cid"] == m["cid"] for c in chosen):
                continue
            if diversify and sum(1 for c in chosen if org_of(c["id"]) == org_of(m["id"])) >= MAX_PER_ORG:
                continue
            if verify and api_key and not probe_available(m, api_key):
                continue
            chosen.append(m)
            why[m["id"]] = reason(m)
            filled += 1

    pinned = []
    for pid in PINNED:
        m = next((x for x in pool if x["cid"] == pid or x["id"] == pid), None)
        if m:
            pinned.append(m)
    take(pinned, lambda m: "your daily driver" + traffic(m), slots=len(pinned), diversify=False)

    for (lo, hi), crowd_slots, value_slots, label in (
            (CHEAP_TIER, CHEAP_CROWD, CHEAP_VALUE, "cheap"),
            (MID_TIER, MID_CROWD, MID_VALUE, "mid")):
        tier = [m for m in pool if lo <= m["cost_1m"] < hi]
        take(sorted((m for m in tier if used(m)), key=used, reverse=True),
             lambda m, l=label: f"{l} tier, most traffic" + traffic(m), slots=crowd_slots)
        # a cheap gem nobody runs is a risk; prefer the used ones when we know
        # the traffic (i.e. an API key was available)
        in_use = [m for m in tier if used(m)]
        take(sorted(in_use or tier, key=value, reverse=True),
             lambda m, l=label, lo=lo, hi=hi: f"best {l}-tier value (${lo:.2f}–${hi:.2f}/1M)",
             slots=value_slots)

    for cap in QUALITY_CAPS:
        take(sorted((m for m in pool if m["cost_1m"] <= cap), key=score, reverse=True),
             lambda m, c=cap: f"best quality under ${c:.2f}/1M (score {score(m):.0f})",
             slots=1, diversify=False)

    return sorted(chosen, key=lambda m: m["cost_1m"]), why


def fmt_date(ts):
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d") if ts else "unknown"


def probe_available(model, api_key, timeout=60):
    """One-token completion: is any endpoint of this model usable for this account?

    OpenRouter answers 404 when every endpoint is filtered out by the account's
    data policy (e.g. a zero-data-retention requirement), and the catalog does
    not expose those policies — so a real request is the only reliable check.
    """
    payload = json.dumps({
        "model": model["id"],
        "messages": [{"role": "user", "content": "."}],
        "max_tokens": 1,
    }).encode()
    req = urllib.request.Request(CHAT_API, data=payload, headers={
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "User-Agent": "openrouter-ranking/goose-config",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except urllib.error.HTTPError as e:
        if e.code == 429:  # throttled, but the model itself works
            return True
        print(f"   ✗ skipping {model['id']}: HTTP {e.code}", file=sys.stderr)
        return False
    except Exception as e:  # network hiccup — keep the model
        print(f"   ? could not probe {model['id']} ({e}); keeping it", file=sys.stderr)
        return True


def select_newest(models, count=NEWEST_COUNT, api_key=None, verify=False, include_free=False,
                  also=()):
    """Pick the `count` most recently released models.

    `created` is the release timestamp OpenRouter exposes per model, so this
    follows the catalog itself instead of any judgement of quality. Filtered
    out, because they would only waste a slot in a Goose picker:

      - models without tool calling — Goose cannot run a session on them;
      - non-interactive/duplicate entries — `:batch` endpoints are folded into
        their interactive sibling by build_index(), `~` rolling aliases are
        dropped there as well;
      - `:free` promos (`--include-free` to keep them): rate limited, and often
        the only model whose single endpoint is excluded by an account's data
        policy;
      - optionally anything a probe shows as unusable for this account
        (`--verify`), in which case the next-newest model takes the slot.

    `also` names models that are kept on top of the newest ones, so a personal
    favourite that is months old does not get squeezed out by the release race.
    """
    def usable(m):
        return m["tools"] and m["context"] > 0 and (include_free or not m["free"])

    pool = sorted((m for m in models.values() if usable(m)),
                  key=lambda m: m["created"], reverse=True)

    pinned = []
    for want in also:
        m = next((x for x in models.values() if x["id"] == want), None) or \
            next((x for x in models.values() if x["cid"] == canonical_id(want)), None)
        if not m or not m["tools"]:
            print(f"⚠️  --also {want}: unknown model or no tool support, skipped", file=sys.stderr)
            continue
        if m["id"] not in {x["id"] for x in pinned}:
            pinned.append(m)

    chosen = []
    for m in pool:
        if len(chosen) >= count:
            break
        if m["id"] in {x["id"] for x in pinned}:
            continue  # already in the list, do not burn a newest-slot on it
        if verify and api_key and not probe_available(m, api_key):
            continue
        chosen.append(m)

    why = {m["id"]: f"newest release on OpenRouter ({fmt_date(m['created'])})" for m in chosen}
    for m in pinned:
        why[m["id"]] = f"kept via --also (released {fmt_date(m['created'])})"
    return chosen + pinned, why


def provider_json(models, mode=SELECTION_MODE):
    if mode == "newest":
        display_name = "OpenRouter · Newest"
        description = f"The {len(models)} newest OpenRouter models, regenerated automatically."
    else:
        display_name = "OpenRouter · Best Value"
        description = ("Affordable, widely used OpenRouter models — cheap value picks "
                       "plus one or two strong ones.")
    return {
        "name": PROVIDER_ID,
        "engine": "openai",
        "display_name": display_name,
        "description": description,
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
        price = "free" if m["free"] else f"${m['cost_1m']:.2f}/1M"
        parts = [price, f"{fmt_ctx(m['context'])} ctx"]
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


def write_readme(out_dir, selected, why, now, usage, total, mode=SELECTION_MODE):
    def row(m):
        alias = pretty_alias(m["id"], m["api_name"])
        cost = "free" if m["free"] else f"${m['cost_1m']:.2f}"
        code = f"{m['coding']:.0f}" if m["coding"] is not None else "n/a"
        tokens = usage.get(m["cid"])
        used = f"{humanize_tokens(tokens)} ({100 * tokens / total:.1f}%)" if tokens else "—"
        common = (f"| `{m['id']}` | {alias} | {fmt_date(m['created'])} | {cost} | "
                  f"{m['context']:,} | {modality_tags(m) or 'text'} |")
        if mode == "newest":
            return f"{common} {why.get(m['id'], '')} |"
        return f"{common} {code} | {used} | {why.get(m['id'], '')} |"

    rows = "\n".join(row(m) for m in selected)

    if mode == "newest":
        headline = f"the **{len(selected)} newest models** on OpenRouter"
        intro = ("Selection follows the catalog, not a curation: the models with the latest\n"
                 "`created` timestamp win, so any release that lands on OpenRouter moves in on\n"
                 "the next run. Skipped: models without tool calling (Goose cannot run a\n"
                 "session on them), non-interactive `:batch` endpoints, and `:free` promos\n"
                 "(`--include-free` keeps them). With `--verify` each candidate is probed with a\n"
                 "1-token request, so models your account cannot use — e.g. excluded by a\n"
                 "zero-data-retention setting — make room for the next-newest one. Sorted\n"
                 "newest first.")
        cols = "| Model | Name in picker | Released | $/1M | Context | In | Why |\n"
        cols += "|-------|----------------|----------|------|---------|----|-----|"
    else:
        headline = f"{len(selected)} affordable, widely used models"
        intro = ("Not the newest, not the priciest: cheap value picks first, then the models\n"
                 "OpenRouter users actually spend tokens on, then one or two strong models on top\n"
                 "(best under $2.00 and under $3.50 per 1M tokens). With `--verify` every\n"
                 "candidate is probed with a 1-token request, so models your account cannot reach\n"
                 f"are replaced instead of parked in the picker. Token figures: last {USAGE_WINDOW_DAYS}\n"
                 "days (share of all OpenRouter traffic in the window).")
        cols = "| Model | Name in picker | Released | $/1M | Context | In | Coding | Tokens (7d) | Why |\n"
        cols += "|-------|----------------|----------|------|---------|----|--------|-------------|-----|"

    readme = f"""# Goose config — OpenRouter models

Generated **{now}**. Mode: **{mode}** — {headline}.
{intro}

{cols}
{rows}

## Setup — new machine

One command, no repo clone needed (Linux/macOS):

```bash
curl -fsSL {REPO_RAW_URL}/bootstrap.sh -o bootstrap.sh && bash bootstrap.sh
```

This installs the provider, merges the `providers:` entry (with backup), writes a
self-updating launcher (`.desktop` on Linux, `launchctl` on macOS) and adds
`GOOSE_PREDEFINED_MODELS` to your shell profile.

**Start Goose afterwards via the desktop launcher** so the wrapper applies —
the launcher refreshes the model list on *every* start.

Then add the `{API_KEY_ENV}` secret in Goose (Settings → provider, or
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

Knobs the launcher reads: `GOOSE_NEWEST_COUNT` (default `{NEWEST_COUNT}`),
`GOOSE_MODEL_MODE` (`newest` or `curated`), `GOOSE_EXTRA_MODELS` (comma-separated
models that stay in the list regardless of their release date, e.g.
`z-ai/glm-5.3-flash`) and `GOOSE_MODEL_REFRESH_MIN` (default `360` — minutes
before the local regeneration runs again).
"""
    with open(os.path.join(out_dir, "README.md"), "w") as f:
        f.write(readme)


def main():
    load_env_file()
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-key", default=os.environ.get("OPENROUTER_API_KEY"))
    ap.add_argument("--out", default="goose")
    ap.add_argument("--mode", choices=["newest", "curated"], default=SELECTION_MODE,
                    help="newest = latest N releases from the catalog (default), "
                         "curated = hand-tuned coding mix")
    ap.add_argument("--newest", type=int, default=NEWEST_COUNT,
                    help=f"how many models in newest mode (default {NEWEST_COUNT})")
    ap.add_argument("--include-free", action="store_true",
                    help="also consider ':free' promo variants (skipped by default)")
    ap.add_argument("--also", action="append", default=[], metavar="MODEL",
                    help="keep this model on top of the newest ones (repeatable), "
                         "e.g. --also z-ai/glm-5.3-flash")
    ap.add_argument("--verify", action="store_true",
                    help="probe each candidate with a 1-token request and skip models "
                         "this account cannot use (needs an API key)")
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    print("🔄 Fetching OpenRouter catalog…", file=sys.stderr)
    models = build_index(_get_json(MODELS_API)["data"])
    if args.mode == "newest":
        # Usage data is only decoration in this mode; skipping it keeps the
        # weekly run cheap (and works without an API key).
        usage, total = {}, 0
        if args.verify and not args.api_key:
            print("⚠️  --verify needs an API key; picking without probing", file=sys.stderr)
        selected, why = select_newest(models, args.newest, api_key=args.api_key,
                                      verify=args.verify, include_free=args.include_free,
                                      also=args.also)
    else:
        usage, total = fetch_usage(args.api_key, models) if args.api_key else ({}, 0)
        selected, why = select(models, usage, total, api_key=args.api_key,
                              verify=args.verify)
    print(f"✅ {len(selected)} models selected ({args.mode}): "
          f"{', '.join(m['id'] for m in selected)}", file=sys.stderr)

    with open(os.path.join(args.out, "openrouter_code.json"), "w") as f:
        json.dump(provider_json(selected, args.mode), f, indent=2)
        f.write("\n")

    pre = predefined_models(selected, usage, total)
    with open(os.path.join(args.out, "predefined_models.json"), "w") as f:
        json.dump(pre, f, indent=2)
        f.write("\n")

    # Single-line copy: GOOSE_PREDEFINED_MODELS is an env var, so it must not
    # contain newlines.
    with open(os.path.join(args.out, "predefined_models.min.json"), "w") as f:
        f.write(json.dumps(pre, separators=(",", ":")))

    # Default model: newest mode puts a free promo first on occasion — start on
    # a paid entry instead so the first session is not rate limited.
    first = next((m["id"] for m in selected if not m["free"]), selected[0]["id"])
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
    write_readme(args.out, selected, why, now, usage, total, args.mode)
    print(f"✅ Wrote {args.out}/ (provider, predefined models, snippet, README)", file=sys.stderr)


if __name__ == "__main__":
    main()
