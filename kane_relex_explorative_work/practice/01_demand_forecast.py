#!/usr/bin/env python3
"""
RELEX-style practice 01 — Demand forecast baseline vs seasonal/ML

SUCCESS criteria
----------------
1. Build synthetic daily demand for multiple sku_location series (or load practice/data).
2. Time-based train/test split (NO random shuffle).
3. Baseline: seasonal naive (lag-7) OR trailing mean.
4. Model: seasonal features + HistGradientBoosting (or Ridge).
5. Report WMAPE + bias on holdout; model should beat baseline WMAPE
   (or print a clear diagnosis if not).
6. Finish in ~20–30 minutes in an interview setting.

Run:  python practice/01_demand_forecast.py
Hint: see practice/solutions/01_demand_forecast_solved.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "practice" / "data" / "demand_daily.csv"


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    denom = np.abs(y).sum()
    return float("nan") if denom == 0 else float(np.abs(y - yhat).sum() / denom)


def bias(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    denom = y.sum()
    return float("nan") if denom == 0 else float((yhat - y).sum() / denom)


def make_synthetic(n_days: int = 420, seed: int = 7) -> pd.DataFrame:
    """SKU-location daily demand with weekly seasonality, promo spikes, weather."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    rows = []
    catalogs = [
        ("SKU_A|STORE_1", 40, 0.35, True),
        ("SKU_A|STORE_2", 28, 0.25, True),
        ("SKU_B|STORE_1", 12, 0.15, False),  # slower / more intermittent
        ("SKU_C|STORE_1", 55, 0.40, True),
    ]
    for sku_loc, base, noise, promo_sensitive in catalogs:
        temp = 10 + 12 * np.sin(np.arange(n_days) / 365 * 2 * np.pi) + rng.normal(0, 2, n_days)
        promo = (rng.random(n_days) < 0.08).astype(int)
        for i, dt in enumerate(dates):
            dow = dt.dayofweek
            weekly = 1.0 + 0.25 * np.sin(2 * np.pi * dow / 7)
            weather = 1.0 + 0.015 * (temp[i] - 10)
            uplift = 1.0 + (0.55 if promo_sensitive else 0.15) * promo[i]
            lam = max(0.1, base * weekly * weather * uplift)
            units = rng.poisson(lam)
            # intermittent thinning for SKU_B
            if sku_loc.startswith("SKU_B") and rng.random() < 0.35:
                units = 0
            rows.append(
                {
                    "date": dt,
                    "sku_location": sku_loc,
                    "units": int(units),
                    "promo": int(promo[i]),
                    "temp_c": float(temp[i]),
                }
            )
    return pd.DataFrame(rows)


def load_or_create() -> pd.DataFrame:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    if DATA.exists():
        df = pd.read_csv(DATA, parse_dates=["date"])
    else:
        df = make_synthetic()
        df.to_csv(DATA, index=False)
        print(f"Wrote synthetic data → {DATA}")
    return df


def main(write_data_only: bool = False) -> None:
    df = load_or_create()
    if write_data_only:
        print(df.head())
        print("rows", len(df), "sku_locations", df["sku_location"].nunique())
        return

    # --- YOUR IMPLEMENTATION ---
    # TODO: time split, lag7 baseline, ML model, print WMAPE/bias comparison.
    # Delete the raise and implement, or run the solved script.
    raise NotImplementedError(
        "Implement the forecast pipeline here (see solutions/01_demand_forecast_solved.py)."
    )


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--write-data-only", action="store_true")
    args = p.parse_args()
    main(write_data_only=args.write_data_only)
