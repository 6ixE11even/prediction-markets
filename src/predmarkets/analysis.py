"""
Turn raw Polymarket markets into tradeable signals.

  * `to_frame`            — flatten markets into prices, spreads, volume, event id.
  * `event_consistency`   — the real edge: mutually-exclusive outcomes in a neg-risk
                            event must price to ~1. When their YES prices sum away from
                            1, there's a static arbitrage (short the overpriced basket).
  * `summary`             — book-wide stats, incl. the favorite-longshot price spread.
"""
from __future__ import annotations

import json

import pandas as pd


def _outcome_prices(market: dict):
    p = market.get("outcomePrices")
    if isinstance(p, str):
        p = json.loads(p) if p else None
    return p


def to_frame(markets: list[dict]) -> pd.DataFrame:
    rows = []
    for m in markets:
        prices = _outcome_prices(m)
        if not prices or len(prices) < 2:
            continue
        yes, no = float(prices[0]), float(prices[1])
        event = (m.get("events") or [{}])[0]
        rows.append({
            "question": (m.get("question") or "")[:80],
            "outcome": m.get("groupItemTitle") or "Yes",
            "yes": yes, "no": no, "binary_sum": yes + no,
            "spread": float(m.get("spread") or 0.0),
            "volume": float(m.get("volumeNum") or m.get("volume") or 0.0),
            "liquidity": float(m.get("liquidityNum") or m.get("liquidity") or 0.0),
            "neg_risk": bool(m.get("negRisk")),
            "event_id": event.get("id"),
            "event_title": (event.get("title") or "")[:80],
        })
    return pd.DataFrame(rows)


def event_consistency(df: pd.DataFrame, threshold: float = 0.02) -> pd.DataFrame:
    """Neg-risk events whose mutually-exclusive YES prices sum far from 1 — arb candidates."""
    rows = []
    for (eid, title), g in df[df["neg_risk"]].groupby(["event_id", "event_title"]):
        if len(g) < 2:
            continue
        yes_sum = g["yes"].sum()
        rows.append({"event_title": title, "n_outcomes": len(g), "yes_sum": yes_sum,
                     "deviation": yes_sum - 1.0, "volume": g["volume"].sum()})
    out = pd.DataFrame(rows)
    return out if out.empty else out[out["deviation"].abs() > threshold].sort_values("deviation", ascending=False)


def summary(df: pd.DataFrame) -> dict:
    return {
        "markets": len(df),
        "total_volume": float(df["volume"].sum()),
        "mean_yes_prob": float(df["yes"].mean()),
        "mean_spread_cents": float(df["spread"].mean() * 100),
        "wide_spread_>5c": int((df["spread"] > 0.05).sum()),
        "neg_risk_markets": int(df["neg_risk"].sum()),
    }
