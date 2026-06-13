"""Implied-probability distribution and the spread/liquidity picture."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot_prob_distribution(df: pd.DataFrame, out_path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.hist(df["yes"], bins=25, color="#3b6ea5", alpha=0.85)
    ax.set_title("Implied-probability distribution (YES price)", fontweight="bold")
    ax.set_xlabel("implied probability")
    ax.set_ylabel("markets")
    ax.grid(alpha=0.25)
    _save(fig, out_path)


def plot_spread_vs_liquidity(df: pd.DataFrame, out_path: str | Path) -> None:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(df["liquidity"].clip(lower=1), df["spread"] * 100, s=14, alpha=0.6, color="#2c7a4b")
    ax.set_xscale("log")
    ax.set_title("Spread vs liquidity", fontweight="bold")
    ax.set_xlabel("liquidity ($, log)")
    ax.set_ylabel("spread (cents)")
    ax.grid(alpha=0.25)
    _save(fig, out_path)


def _save(fig, out_path: str | Path) -> None:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
