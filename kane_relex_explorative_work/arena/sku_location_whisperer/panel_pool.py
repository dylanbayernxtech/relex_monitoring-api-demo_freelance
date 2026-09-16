#!/usr/bin/env python3
"""sku_location_whisperer — sparse SKU-location panel + hierarchical pooling."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / d) if d else float("nan")


def make_panel(n_sku: int = 12, n_loc: int = 8, n_days: int = 180, seed: int = 21) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-06-01", periods=n_days, freq="D")
    sku_effect = {f"S{s:02d}": rng.uniform(4, 28) for s in range(n_sku)}
    loc_effect = {f"L{loc:02d}": rng.uniform(0.45, 1.9) for loc in range(n_loc)}
    rows = []
    for s, sb in sku_effect.items():
        for loc, lb in loc_effect.items():
            # late-start / sparse cells → local history thin
            start_delay = int(rng.choice([0, 0, 50, 90, 130], p=[0.3, 0.15, 0.2, 0.2, 0.15]))
            sparse_mult = float(rng.choice([1.0, 0.25, 0.08], p=[0.45, 0.35, 0.2]))
            base = sb * lb * sparse_mult
            for i, d in enumerate(dates):
                if i < start_delay:
                    units = 0
                else:
                    units = int(max(0, rng.poisson(base * (1.3 if d.dayofweek >= 5 else 1.0))))
                rows.append({"date": d, "sku": s, "location": loc, "units": units})
    return pd.DataFrame(rows)


def hierarchical_predict(train: pd.DataFrame, test: pd.DataFrame, prior_strength: float = 20.0) -> np.ndarray:
    """Empirical-Bayes blend: shrink SKU-location mean toward sku×loc hierarchy."""
    g = float(train["units"].mean())
    sku_m = train.groupby("sku")["units"].mean()
    loc_m = train.groupby("location")["units"].mean()
    # multiplicative prior: E[sku,loc] ≈ sku_mean * (loc_mean / global)
    prior = test["sku"].map(sku_m).fillna(g) * (test["location"].map(loc_m).fillna(g) / max(g, 1e-6))
    stats = train.groupby("sku_location")["units"].agg(["mean", "count"])
    local = test["sku_location"].map(stats["mean"])
    n = test["sku_location"].map(stats["count"]).fillna(0).to_numpy(float)
    local_f = local.fillna(prior).to_numpy(float)
    prior_f = prior.to_numpy(float)
    w = n / (n + prior_strength)
    return w * local_f + (1 - w) * prior_f


def main() -> int:
    print("=== sku_location_whisperer: hierarchical pooling ===")
    df = make_panel()
    df["sku_location"] = df["sku"] + "|" + df["location"]
    df["dow"] = df["date"].dt.dayofweek
    split_date = df["date"].min() + (df["date"].max() - df["date"].min()) * 0.7
    train = df[df["date"] <= split_date]
    test = df[df["date"] > split_date]

    # pure local mean; cold cells fall back to global (brutal)
    counts = train.groupby("sku_location").size()
    local = train.groupby("sku_location")["units"].mean()
    yhat_local = test["sku_location"].map(local).fillna(train["units"].mean()).to_numpy()
    print(f"  local_mean        WMAPE={wmape(test['units'], yhat_local):.4f}")

    yhat_hier = np.clip(hierarchical_predict(train, test), 0, None)
    print(f"  hierarchy_shrink  WMAPE={wmape(test['units'], yhat_hier):.4f}")

    # bonus: Ridge with SKU+loc+dow (interview talking point)
    Xtr = pd.get_dummies(train[["sku", "location", "dow"]], columns=["sku", "location"], drop_first=False)
    Xte = pd.get_dummies(test[["sku", "location", "dow"]], columns=["sku", "location"], drop_first=False)
    Xte = Xte.reindex(columns=Xtr.columns, fill_value=0)
    ridge = Ridge(alpha=1.0).fit(Xtr, train["units"])
    yhat_ridge = np.clip(ridge.predict(Xte), 0, None)
    print(f"  ridge_pooled      WMAPE={wmape(test['units'], yhat_ridge):.4f}")

    cold = counts[counts < 40].index
    cold_mask = test["sku_location"].isin(cold).to_numpy()
    if cold_mask.any():
        print(
            f"  cold_cells WMAPE  local={wmape(test.loc[cold_mask, 'units'], yhat_local[cold_mask]):.4f}  "
            f"hier={wmape(test.loc[cold_mask, 'units'], yhat_hier[cold_mask]):.4f}"
        )
    sparse_share = float((train.groupby("sku_location")["units"].mean() < 1).mean())
    print(f"  sparse_sku_loc_share={sparse_share:.2%}")
    print("OK sku_location_whisperer — sparse panel pooling done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
