"""Heatmap data cache — daily token usage for the past ~360 days (GitHub-style)."""

import json
import os
from datetime import date, timedelta
from typing import Any

HEATMAP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "heatmap.json")


def load_heatmap() -> dict:
    """Load cached heatmap data. Returns dict of {"YYYY-MM-DD": {...}}."""
    if not os.path.exists(HEATMAP_FILE):
        return {}
    try:
        with open(HEATMAP_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_heatmap(data: dict) -> None:
    """Save heatmap data to cache."""
    with open(HEATMAP_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def build_heatmap_from_api(api) -> dict:
    """Fetch historical monthly usage from the API and build a flat day→data map.

    Iterates the last 12 months and collects per-day total/cache_hit/cache_miss.
    Returns a dict keyed by ISO date string.
    """
    today = date.today()
    heatmap: dict[str, dict] = {}

    for i in range(12):
        y = today.year
        m = today.month - i
        if m <= 0:
            m += 12
            y -= 1
        usage = api.get_monthly_usage(month=m, year=y)
        if not usage:
            continue
        for day_entry in usage.get("days", []):
            ds = day_entry.get("date", "")
            if not ds:
                continue
            if ds not in heatmap:
                heatmap[ds] = {"total": 0, "cache_hit": 0, "cache_miss": 0}
            for me in day_entry.get("data", []):
                for ut in me.get("usage", []):
                    t = ut.get("type", "")
                    a = int(ut.get("amount", "0"))
                    if t == "RESPONSE_TOKEN":
                        heatmap[ds]["total"] += a
                    elif t == "PROMPT_CACHE_HIT_TOKEN":
                        heatmap[ds]["total"] += a
                        heatmap[ds]["cache_hit"] += a
                    elif t == "PROMPT_CACHE_MISS_TOKEN":
                        heatmap[ds]["total"] += a
                        heatmap[ds]["cache_miss"] += a
                    elif t == "PROMPT_TOKEN":
                        heatmap[ds]["total"] += a

    return heatmap


def merge_today(heatmap: dict, daily_series: list[dict]) -> dict:
    """Merge today's data from daily_series into the heatmap cache."""
    for entry in daily_series:
        ds = entry["date"]
        if ds not in heatmap:
            heatmap[ds] = {}
        heatmap[ds]["total"] = entry.get("total", 0)
        heatmap[ds]["cache_hit"] = entry.get("cache_hit", 0)
        heatmap[ds]["cache_miss"] = entry.get("cache_miss", 0)
    return heatmap
