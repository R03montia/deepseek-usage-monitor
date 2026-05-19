"""Client for platform.deepseek.com internal APIs (Bearer token auth).

Extract your token from browser localStorage:
  JSON.parse(localStorage.getItem('userToken')).value
"""

from datetime import date
from typing import Any

import requests

BASE = "https://platform.deepseek.com/api/v0"


class DeepSeekPlatform:
    """Thin client around platform.deepseek.com internal endpoints."""

    def __init__(self, bearer_token: str):
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {bearer_token}",
            "x-app-version": "1.0.0",
            "Origin": "https://platform.deepseek.com",
            "Referer": "https://platform.deepseek.com/usage",
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/148.0.0.0 Safari/537.36"
            ),
        })

    def _get(self, path: str, **params) -> dict[str, Any] | None:
        """Make a GET request. Returns JSON data or None on failure."""
        try:
            resp = self._session.get(f"{BASE}{path}", params=params, timeout=15)
            resp.raise_for_status()
            body = resp.json()
            if body.get("code") != 0:
                return None
            biz = body.get("data", {})
            if biz.get("biz_code") != 0:
                return None
            return biz.get("biz_data")
        except requests.RequestException:
            return None

    # ── Public helpers ────────────────────────────────────────────────

    def get_user_summary(self) -> dict[str, Any] | None:
        """Return user summary (wallet balances, monthly totals)."""
        return self._get("/users/get_user_summary")

    def get_monthly_usage(self, month: int | None = None, year: int | None = None
                          ) -> dict[str, Any] | None:
        """Return per-day token usage for a given month."""
        today = date.today()
        return self._get(
            "/usage/amount",
            month=month or today.month,
            year=year or today.year,
        )

    def get_monthly_cost(self, month: int | None = None, year: int | None = None
                         ) -> dict[str, Any] | None:
        """Return per-day cost for a given month."""
        today = date.today()
        return self._get(
            "/usage/cost",
            month=month or today.month,
            year=year or today.year,
        )

    # ── Composite: get everything in one go ────────────────────────────

    def fetch_all(self, target_date: str | None = None
                  ) -> dict[str, Any]:
        """Fetch summary + monthly usage + cost. Return a flat dict."""
        if target_date is None:
            target_date = date.today().isoformat()

        summary = self.get_user_summary()
        usage   = self.get_monthly_usage()
        cost    = self.get_monthly_cost()

        return self._flatten(summary, usage, cost, target_date)

    @staticmethod
    def _flatten(summary: dict | None,
                 usage: dict | None,
                 cost: dict | None,
                 today: str) -> dict[str, Any]:
        """Merge the three API responses into a flat dict for the widget."""
        result: dict[str, Any] = {
            "ok": False,
            "error": None,
            "balance": "--",
            "bonus_balance": "--",
            "monthly_tokens": 0,
            "monthly_cost": "--",
            "today_prompt": 0,
            "today_completion": 0,
            "today_cache_hit": 0,
            "today_cache_miss": 0,
            "today_total": 0,
            "today_cost": "--",
        }

        # ── Summary ────────────────────────────────────────────────
        if summary:
            result["ok"] = True
            wallets = summary.get("normal_wallets", [])
            result["balance"] = (
                wallets[0].get("balance", "0") if wallets else "0"
            )
            bonus = summary.get("bonus_wallets", [])
            result["bonus_balance"] = (
                bonus[0].get("balance", "0") if bonus else "0"
            )
            result["monthly_tokens"] = int(
                summary.get("monthly_token_usage", "0")
            )
            costs = summary.get("monthly_costs", [])
            result["monthly_cost"] = (
                costs[0].get("amount", "0") if costs else "0"
            )
        else:
            result["error"] = "ERR: Cannot fetch summary"

        # ── Today's usage from monthly breakdown ───────────────────
        if usage:
            days = usage.get("days", [])
            today_entry = next((d for d in days if d.get("date") == today), None)
            if today_entry:
                prompt_tokens = 0
                completion_tokens = 0
                cache_hit = 0
                cache_miss = 0
                for model_entry in today_entry.get("data", []):
                    for usage_type in model_entry.get("usage", []):
                        t = usage_type.get("type", "")
                        amt = int(usage_type.get("amount", "0"))
                        if t == "PROMPT_TOKEN":
                            prompt_tokens += amt
                        elif t == "PROMPT_CACHE_HIT_TOKEN":
                            prompt_tokens += amt
                            cache_hit += amt
                        elif t == "PROMPT_CACHE_MISS_TOKEN":
                            prompt_tokens += amt
                            cache_miss += amt
                        elif t == "RESPONSE_TOKEN":
                            completion_tokens += amt
                result["today_prompt"] = prompt_tokens
                result["today_completion"] = completion_tokens
                result["today_cache_hit"] = cache_hit
                result["today_cache_miss"] = cache_miss
                result["today_total"] = prompt_tokens + completion_tokens
            result["ok"] = True
        else:
            result["error"] = "ERR: Cannot fetch usage"

        # ── Today's cost ───────────────────────────────────────────
        if cost:
            cost_container = cost[0] if isinstance(cost, list) else cost
            days = cost_container.get("days", [])
            today_entry = next((d for d in days if d.get("date") == today), None)
            if today_entry:
                total_cost = 0.0
                for model_entry in today_entry.get("data", []):
                    for c in model_entry.get("usage", []):
                        amt_str = c.get("amount", "0")
                        total_cost += float(amt_str)
                result["today_cost"] = f"{total_cost:.4f}"
            result["ok"] = True
        else:
            result["error"] = "ERR: Cannot fetch cost"

        # ── Daily series for sidebar charts ────────────────────────
        daily_series: list[dict] = []
        if usage and cost:
            usage_days = {d.get("date"): d for d in usage.get("days", [])}
            cost_container = cost[0] if isinstance(cost, list) else cost
            cost_days = {d.get("date"): d for d in cost_container.get("days", [])}
            all_dates = sorted(set(list(usage_days) + list(cost_days)))
            for date_str in all_dates:
                day_usage = usage_days.get(date_str, {})
                pt = ct = ch = cm = 0
                for me in day_usage.get("data", []):
                    for ut in me.get("usage", []):
                        t = ut.get("type", ""); a = int(ut.get("amount", "0"))
                        if t == "RESPONSE_TOKEN":          ct += a
                        elif t == "PROMPT_CACHE_HIT_TOKEN": pt += a; ch += a
                        elif t == "PROMPT_CACHE_MISS_TOKEN":pt += a; cm += a
                        elif t == "PROMPT_TOKEN":           pt += a
                dc = 0.0
                for me in cost_days.get(date_str, {}).get("data", []):
                    for c2 in me.get("usage", []):
                        dc += float(c2.get("amount", "0"))
                daily_series.append(dict(date=date_str, prompt=pt,
                    completion=ct, total=pt+ct, cost=dc,
                    cache_hit=ch, cache_miss=cm))
        result["daily_series"] = daily_series

        return result
