"""Analysis logic on a fixture shaped like real Polymarket data (offline)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from predmarkets.analysis import event_consistency, summary, to_frame

# Three mutually-exclusive outcomes of one event priced to sum to 1.1 (an arb), plus an
# unrelated binary market.
MARKETS = [
    {"question": "Team A wins?", "groupItemTitle": "A", "outcomePrices": '["0.5","0.5"]',
     "spread": 0.02, "volumeNum": 1000, "negRisk": True, "events": [{"id": "E1", "title": "The Match"}]},
    {"question": "Team B wins?", "groupItemTitle": "B", "outcomePrices": '["0.4","0.6"]',
     "spread": 0.03, "volumeNum": 900, "negRisk": True, "events": [{"id": "E1", "title": "The Match"}]},
    {"question": "Team C wins?", "groupItemTitle": "C", "outcomePrices": '["0.2","0.8"]',
     "spread": 0.04, "volumeNum": 800, "negRisk": True, "events": [{"id": "E1", "title": "The Match"}]},
    {"question": "Rain tomorrow?", "outcomePrices": '["0.3","0.7"]',
     "spread": 0.01, "volumeNum": 500, "negRisk": False, "events": [{"id": "E2", "title": "Weather"}]},
]


def test_to_frame_parses_string_prices():
    df = to_frame(MARKETS)
    assert len(df) == 4
    assert abs(df.iloc[0]["yes"] - 0.5) < 1e-9


def test_summary_keys():
    s = summary(to_frame(MARKETS))
    assert s["markets"] == 4 and s["neg_risk_markets"] == 3


def test_event_consistency_flags_arbitrage():
    arb = event_consistency(to_frame(MARKETS))
    assert len(arb) == 1
    assert abs(arb.iloc[0]["yes_sum"] - 1.1) < 1e-9   # 0.5 + 0.4 + 0.2
