#!/usr/bin/env python3
"""viz_or_it_didnt_happen - matplotlib EDA plots (Agg, no display required)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main() -> int:
    print("=== viz_or_it_didnt_happen: EDA plots ===")
    rng = np.random.default_rng(12)
    dates = pd.date_range("2024-01-01", periods=120, freq="D")
    df = pd.DataFrame({
        "date": dates,
        "units": (40 + 10 * np.sin(np.arange(120) / 7) + rng.normal(0, 4, 120)).clip(0),
        "promo": (rng.random(120) < 0.1).astype(int),
    })
    out_dir = Path(__file__).resolve().parent / "_plots"
    out_dir.mkdir(exist_ok=True)

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    axes[0].plot(df["date"], df["units"], color="#1f4e79", lw=1.2, label="units")
    axes[0].scatter(df.loc[df["promo"] == 1, "date"], df.loc[df["promo"] == 1, "units"],
                    c="#c0392b", s=28, zorder=3, label="promo")
    axes[0].set_ylabel("units")
    axes[0].legend(loc="upper right")
    axes[0].set_title("Demand + promos (SKU-location vibe)")

    axes[1].bar(df["date"], df["units"] - df["units"].rolling(7, min_periods=1).mean(),
                color="#7f8c8d", width=1.0)
    axes[1].axhline(0, color="k", lw=0.6)
    axes[1].set_ylabel("vs 7d MA")
    axes[1].set_xlabel("date")
    fig.tight_layout()
    path = out_dir / "demand_eda.png"
    fig.savefig(path, dpi=100)
    plt.close(fig)
    print(f"  wrote {path}")
    print("OK viz_or_it_didnt_happen - if you didn't plot it, it didn't happen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
