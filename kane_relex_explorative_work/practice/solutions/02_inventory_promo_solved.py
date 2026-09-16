#!/usr/bin/env python3
"""Solved: probabilistic-ish safety stock + promo uplift on synthetic retail data."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import Ridge

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "practice" / "data" / "demand_daily.csv"


def load() -> pd.DataFrame:
    if not DATA.exists():
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "d01", ROOT / "practice" / "01_demand_forecast.py"
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        DATA.parent.mkdir(parents=True, exist_ok=True)
        mod.make_synthetic().to_csv(DATA, index=False)
    return pd.read_csv(DATA, parse_dates=["date"])


def safety_stock(df: pd.DataFrame, sku_location: str, lead_time_days: int = 5, service: float = 0.95):
    s = df.loc[df["sku_location"] == sku_location, "units"].astype(float)
    mu_d, sig_d = float(s.mean()), float(s.std(ddof=1))
    # iid daily demand ⇒ LT demand ~ mean L*mu, std sig*sqrt(L)
    mu_L = lead_time_days * mu_d
    sig_L = sig_d * np.sqrt(lead_time_days)
    z = float(stats.norm.ppf(service))
    ss = z * sig_L
    rop = mu_L + ss
    return {
        "sku_location": sku_location,
        "lead_time_days": lead_time_days,
        "service_level": service,
        "z": z,
        "daily_mean": mu_d,
        "daily_std": sig_d,
        "lt_demand_mean": mu_L,
        "lt_demand_std": sig_L,
        "safety_stock": ss,
        "reorder_point": rop,
    }


def promo_uplift(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for sku, g in df.groupby("sku_location"):
        base = g.loc[g["promo"] == 0, "units"].mean()
        promo = g.loc[g["promo"] == 1, "units"].mean()
        uplift = (promo / base - 1.0) if base and base == base else np.nan
        # regression control for temp + dow
        x = pd.DataFrame(
            {
                "promo": g["promo"],
                "temp_c": g["temp_c"],
                "dow": g["date"].dt.dayofweek,
            }
        )
        y = g["units"].astype(float)
        model = Ridge(alpha=1.0).fit(x, y)
        # marginal effect of promo approx coef
        rows.append(
            {
                "sku_location": sku,
                "mean_units_nopromo": base,
                "mean_units_promo": promo,
                "uplift_ratio": uplift,
                "ridge_promo_coef": float(model.coef_[0]),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    df = load()
    print("=== Practice 02 — Inventory / promo ===\n-- Track A: safety stock --")
    for sku in sorted(df["sku_location"].unique()):
        r = safety_stock(df, sku, lead_time_days=5, service=0.95)
        print(
            f"{r['sku_location']}: SS={r['safety_stock']:.1f}  ROP={r['reorder_point']:.1f} "
            f"(μ_L={r['lt_demand_mean']:.1f}, σ_L={r['lt_demand_std']:.1f}, z={r['z']:.2f})"
        )
    print("\nAssumption callout: iid Normal LT demand; fresh items need bias control + shorter horizon.")
    print("\n-- Track B: promo uplift --")
    u = promo_uplift(df)
    print(u.to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(
        "\nSUCCESS: SS/ROP printed for all SKU-locations; uplift table has ratio + ridge promo coef."
    )
    print("Caveat: uplift ignores cannibalization/halo — in production, model sibling SKUs too.")


if __name__ == "__main__":
    main()
