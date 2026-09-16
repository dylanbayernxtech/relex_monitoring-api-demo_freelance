#!/usr/bin/env python3
"""promo_uplift_sniper - before/after + regression with confounders."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def make_promo_panel(n_days: int = 300, seed: int = 33) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n_days, freq="D")
    base = 60 + 8 * np.sin(2 * np.pi * dates.dayofyear / 365)
    dow = dates.dayofweek
    weekend = (dow >= 5).astype(float)
    # promos clustered on weekends (confounder!)
    promo = ((rng.random(n_days) < 0.12) | ((weekend == 1) & (rng.random(n_days) < 0.25))).astype(float)
    price = 4.5 - 0.8 * promo + rng.normal(0, 0.1, n_days)
    weather = rng.normal(0, 1, n_days)  # mild demand driver
    true_uplift = 22.0
    units = base + 10 * weekend + true_uplift * promo - 3 * (price - 4.0) + 2 * weather + rng.normal(0, 4, n_days)
    return pd.DataFrame({
        "date": dates, "units": np.clip(units, 0, None), "promo": promo,
        "price": price, "weekend": weekend, "weather": weather,
    })


def main() -> int:
    print("=== promo_uplift_sniper: causal-ish uplift ===")
    df = make_promo_panel()
    # naive before/after ignoring confounders
    naive = df.loc[df["promo"] == 1, "units"].mean() - df.loc[df["promo"] == 0, "units"].mean()
    print(f"  naive_diff_in_means uplift={naive:.2f}  (confounded by weekend)")

    # regression controlling for weekend, price, weather
    X = df[["promo", "weekend", "price", "weather"]]
    y = df["units"]
    reg = LinearRegression().fit(X, y)
    print(f"  regression_uplift (promo coef)={reg.coef_[0]:.2f}  intercept={reg.intercept_:.2f}")
    print(f"  other coefs weekend={reg.coef_[1]:.2f} price={reg.coef_[2]:.2f} weather={reg.coef_[3]:.2f}")
    print("OK promo_uplift_sniper - confounders clipped, uplift sniped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
