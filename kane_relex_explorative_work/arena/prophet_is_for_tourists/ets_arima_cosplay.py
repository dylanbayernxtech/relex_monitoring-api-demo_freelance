#!/usr/bin/env python3
"""prophet_is_for_tourists - ETS / ARIMA-ish via statsmodels (no Prophet)."""
from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / d) if d else float("nan")


def synth(n: int = 365, seed: int = 11) -> pd.Series:
    rng = np.random.default_rng(seed)
    t = np.arange(n)
    level = 50 + 0.02 * t
    seas = 10 * np.sin(2 * np.pi * t / 7) + 5 * np.sin(2 * np.pi * t / 365)
    y = np.clip(level + seas + rng.normal(0, 3, n), 1, None)
    idx = pd.date_range("2024-01-01", periods=n, freq="D")
    return pd.Series(y, index=idx, name="units")


def main() -> int:
    print("=== prophet_is_for_tourists: classical TS ===")
    y = synth()
    split = int(len(y) * 0.85)
    train, test = y.iloc[:split], y.iloc[split:]

    ets = ExponentialSmoothing(train, trend="add", seasonal="add", seasonal_periods=7).fit(optimized=True)
    yhat_ets = ets.forecast(len(test))
    print(f"  ETS (HW)   WMAPE={wmape(test, yhat_ets):.4f}")

    # light SARIMA - small order for speed
    sar = SARIMAX(train, order=(1, 0, 1), seasonal_order=(1, 0, 1, 7),
                  enforce_stationarity=False, enforce_invertibility=False)
    sar_fit = sar.fit(disp=False)
    yhat_sar = sar_fit.forecast(len(test))
    print(f"  SARIMAX    WMAPE={wmape(test, yhat_sar):.4f}")
    print("OK prophet_is_for_tourists - ETS + SARIMAX without tourist Prophet")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
