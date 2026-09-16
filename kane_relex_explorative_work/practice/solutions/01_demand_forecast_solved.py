#!/usr/bin/env python3
"""Solved: demand forecast baseline vs HistGradientBoosting with WMAPE + bias."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

ROOT = Path(__file__).resolve().parents[2]


def _load_01():
    spec = importlib.util.spec_from_file_location("demand01", ROOT / "practice" / "01_demand_forecast.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(mod)
    return mod


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.sort_values(["sku_location", "date"]).copy()
    g = df.groupby("sku_location", group_keys=False)
    df["lag7"] = g["units"].shift(7)
    df["lag14"] = g["units"].shift(14)
    df["roll7"] = g["units"].transform(lambda s: s.shift(1).rolling(7, min_periods=1).mean())
    df["dow"] = df["date"].dt.dayofweek
    df["weekofyear"] = df["date"].dt.isocalendar().week.astype(int)
    df["sku_id"] = df["sku_location"].astype("category").cat.codes
    return df


def main() -> None:
    m = _load_01()
    df = add_features(m.load_or_create())
    cut = df["date"].max() - pd.Timedelta(days=28)
    train = df[df["date"] <= cut].dropna(subset=["lag7", "lag14"])
    test = df[df["date"] > cut].dropna(subset=["lag7", "lag14"])

    base_pred = test["lag7"].to_numpy()
    y_test = test["units"].to_numpy()

    feats = ["lag7", "lag14", "roll7", "dow", "weekofyear", "promo", "temp_c", "sku_id"]
    model = HistGradientBoostingRegressor(
        max_depth=6, learning_rate=0.08, max_iter=200, random_state=7
    )
    model.fit(train[feats], train["units"])
    ml_pred = np.clip(model.predict(test[feats]), 0, None)

    print("=== Practice 01 — Demand forecast ===")
    print(f"Train rows={len(train)}  Test rows={len(test)}  cut={cut.date()}")
    print(f"Baseline lag7  WMAPE={m.wmape(y_test, base_pred):.3f}  bias={m.bias(y_test, base_pred):+.3f}")
    print(f"HGBR model     WMAPE={m.wmape(y_test, ml_pred):.3f}  bias={m.bias(y_test, ml_pred):+.3f}")
    improved = m.wmape(y_test, ml_pred) < m.wmape(y_test, base_pred)
    print(
        ("SUCCESS: ML beat baseline WMAPE" if improved else "CHECK: ML did not beat baseline — inspect features/leakage")
    )


if __name__ == "__main__":
    main()
