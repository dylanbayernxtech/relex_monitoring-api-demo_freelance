#!/usr/bin/env python3
"""oracle_of_wmape — seasonal naive vs HistGradientBoosting; WMAPE + bias."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor


def wmape(y: np.ndarray, yhat: np.ndarray) -> float:
    denom = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / denom) if denom else float("nan")


def bias(y: np.ndarray, yhat: np.ndarray) -> float:
    denom = np.abs(y).sum()
    return float((yhat - y).sum() / denom) if denom else float("nan")


def make_retail_series(n_days: int = 420, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    dow = dates.dayofweek
    seasonal = 40 + 12 * np.sin(2 * np.pi * dates.dayofyear / 365.25)
    weekly = 8 * (dow >= 5).astype(float)
    noise = rng.normal(0, 4, n_days)
    promo = (rng.random(n_days) < 0.08).astype(float)
    units = np.clip(seasonal + weekly + 18 * promo + noise, 0, None).round(0)
    return pd.DataFrame({"date": dates, "units": units, "promo": promo, "dow": dow})


def seasonal_naive(train: pd.Series, horizon: int, season: int = 7) -> np.ndarray:
    hist = train.to_numpy()
    out = []
    for h in range(horizon):
        out.append(hist[-(season - (h % season))])
    return np.asarray(out, dtype=float)


def main() -> int:
    print("=== oracle_of_wmape: forecast duel ===")
    df = make_retail_series()
    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]

    yhat_sn = seasonal_naive(train["units"], len(test), season=7)
    print(f"  seasonal_naive  WMAPE={wmape(test['units'].to_numpy(), yhat_sn):.4f}  "
          f"bias={bias(test['units'].to_numpy(), yhat_sn):+.4f}")

    feats = ["dow", "promo"]
    # lag features from train only (leakage-aware)
    train = train.copy()
    test = test.copy()
    for lag in (1, 7, 14):
        train[f"lag{lag}"] = train["units"].shift(lag)
        test[f"lag{lag}"] = pd.concat([train["units"], test["units"]]).shift(lag).iloc[split:].to_numpy()
        feats.append(f"lag{lag}")
    train_m = train.dropna()
    Xtr, ytr = train_m[feats], train_m["units"]
    Xte = test[feats]
    model = HistGradientBoostingRegressor(max_depth=4, learning_rate=0.08, max_iter=120, random_state=7)
    model.fit(Xtr, ytr)
    yhat_ml = model.predict(Xte)
    print(f"  HistGBR         WMAPE={wmape(test['units'].to_numpy(), yhat_ml):.4f}  "
          f"bias={bias(test['units'].to_numpy(), yhat_ml):+.4f}")
    print("OK oracle_of_wmape — baselines + HGBR duel complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
