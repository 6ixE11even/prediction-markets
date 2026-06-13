"""
Polymarket Gamma API client (public, no key, no synthetic data).

Pulls live markets; results are cached to data/ so analysis is reproducible offline
after the first pull.
"""
from __future__ import annotations

import json
from pathlib import Path

import requests

GAMMA = "https://gamma-api.polymarket.com"
CACHE = Path(__file__).resolve().parents[2] / "data" / "markets.json"


def fetch_markets(limit: int = 400, order: str = "volume24hr") -> list[dict]:
    """Active markets, most-traded first."""
    params = {"limit": limit, "closed": "false", "active": "true", "order": order, "ascending": "false"}
    resp = requests.get(f"{GAMMA}/markets", params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def load_markets(limit: int = 400, use_cache: bool = True) -> list[dict]:
    if use_cache and CACHE.exists():
        return json.loads(CACHE.read_text())
    markets = fetch_markets(limit=limit)
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(markets))
    return markets
