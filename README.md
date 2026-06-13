# Prediction-Market Analytics (Polymarket)

Pull **live Polymarket markets** and turn them into tradeable signals: implied
probabilities, the favorite–longshot price distribution, spreads/liquidity, and — the
real edge — **cross-outcome arbitrage** on multi-outcome (neg-risk) events.

## The edge

The outcomes of a neg-risk event are mutually exclusive and exhaustive, so their YES
prices must sum to ~1. When they don't, there's a **static arbitrage**: if three
mutually-exclusive outcomes price at 0.5 / 0.4 / 0.2 (sum 1.1), shorting the basket
locks in the 0.10 overround (minus fees). `event_consistency` scans every event for
exactly this and ranks the deviations by size and volume.

```
Neg-risk arbitrage candidates (outcome prices off 1):
 event_title  n_outcomes  yes_sum  deviation   volume
   The Match           3      1.10      +0.10    2,700
```

## What it computes

- **Implied probabilities** from `outcomePrices` and their distribution (the
  favorite–longshot lens).
- **Event consistency / arbitrage** (`analysis.event_consistency`) — the signal above.
- **Spreads & liquidity** — where the tradeable, liquid markets actually are.

## Run

```bash
uv sync
uv run python scripts/run_analysis.py   # live Polymarket pull -> summary, arb list, figures
uv run pytest                           # analysis logic on a fixture (offline)
```

The first run pulls live markets from the Polymarket Gamma API and caches them; output
(summary, `arbitrage_candidates.csv`, charts) lands in `reports/`.

## Structure

```
prediction-markets/
├── src/predmarkets/
│   ├── client.py     # Polymarket Gamma API client (public, cached)
│   ├── analysis.py   # implied probs, neg-risk arbitrage, book summary
│   └── viz.py        # probability distribution + spread/liquidity
├── scripts/run_analysis.py
└── tests/            # analysis logic on a real-shaped fixture
```

## Notes

- **Real data, no synthetic.** Markets come live from Polymarket; the unit tests run on
  a small fixture shaped like the real API response so the arbitrage logic is checked
  deterministically and offline.
- Arbitrage figures are gross of fees and gas; treat flagged events as candidates to
  size against the book, not free money.

---

*Built by Tejas Pandya — NYU MSFE.*
