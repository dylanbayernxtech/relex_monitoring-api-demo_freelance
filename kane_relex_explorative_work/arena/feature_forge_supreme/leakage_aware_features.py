#!/usr/bin/env python3
"""feature_forge_supreme - calendar, lag, rolling; time-split without leakage."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / d) if d else float("nan")


def make_df(n: int = 400, seed: int = 5) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    units = np.asarray(
        30 + 10 * np.sin(2 * np.pi * dates.dayofyear / 365)
        + 6 * (dates.dayofweek >= 5).astype(float)
        + rng.normal(0, 3, n),
        dtype=float,
    )
    units = np.clip(units, 0, None)
    return pd.DataFrame({"date": dates, "units": np.round(units, 1)})


def forge(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["dow"] = out["date"].dt.dayofweek
    out["month"] = out["date"].dt.month
    out["is_weekend"] = (out["dow"] >= 5).astype(int)
    out["doy_sin"] = np.sin(2 * np.pi * out["date"].dt.dayofyear / 365.25)
    out["doy_cos"] = np.cos(2 * np.pi * out["date"].dt.dayofyear / 365.25)
    for lag in (1, 7, 14, 28):
        out[f"lag_{lag}"] = out["units"].shift(lag)
    # rolling mean of *past* only: shift(1) then rolling
    out["roll7_mean"] = out["units"].shift(1).rolling(7).mean()
    out["roll28_mean"] = out["units"].shift(1).rolling(28).mean()
    out["roll7_std"] = out["units"].shift(1).rolling(7).std()
    return out


def main() -> int:
    print("=== feature_forge_supreme: leakage-aware forge ===")
    raw = make_df()
    feat = forge(raw)
    feat = feat.dropna()
    split = int(len(feat) * 0.8)
    train, test = feat.iloc[:split], feat.iloc[split:]
    cols = [c for c in feat.columns if c not in ("date", "units")]
    # intentional bad example: using future info would inflate - we don't
    model = HistGradientBoostingRegressor(max_iter=80, max_depth=3, random_state=0)
    model.fit(train[cols], train["units"])
    pred = model.predict(test[cols])
    print(f"  features={len(cols)}  holdout_WMAPE={wmape(test['units'], pred):.4f}")
    print("  note: rollings use shift(1) so no same-day leakage - interview gold")
    print("OK feature_forge_supreme - calendar+lag+rolling forged cleanly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
