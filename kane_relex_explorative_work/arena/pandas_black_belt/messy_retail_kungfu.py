#!/usr/bin/env python3
"""pandas_black_belt — groupby, merge_asof, resample on messy retail tables."""
from __future__ import annotations

import numpy as np
import pandas as pd


def main() -> int:
    print("=== pandas_black_belt: messy retail kung fu ===")
    rng = np.random.default_rng(17)
    # irregular POS-like events
    n = 400
    ts = pd.to_datetime("2024-03-01") + pd.to_timedelta(rng.integers(0, 60 * 24 * 40, n), unit="m")
    pos = pd.DataFrame({
        "ts": ts.sort_values().to_numpy(),
        "sku": rng.choice(["A", "B", "C"], n),
        "location": rng.choice(["HEL", "TMP", "TKU"], n),
        "units": rng.integers(1, 6, n),
        "price": rng.choice([2.9, 3.5, 4.2], n),
    })
    # price list changes (asof join target)
    price_book = pd.DataFrame({
        "ts": pd.to_datetime(["2024-03-01", "2024-03-15", "2024-04-01"]),
        "list_price": [3.0, 3.2, 3.4],
    }).sort_values("ts")

    daily = (
        pos.set_index("ts")
        .groupby(["sku", "location"])
        .resample("D")["units"]
        .sum()
        .fillna(0)
        .reset_index()
    )
    print(f"  resampled daily rows={len(daily)} sku_loc={daily.groupby(['sku','location']).ngroups}")

    asof = pd.merge_asof(
        pos.sort_values("ts"),
        price_book,
        on="ts",
        direction="backward",
    )
    asof["vs_list"] = asof["price"] - asof["list_price"]
    print(f"  merge_asof matched={asof['list_price'].notna().mean():.0%}  mean_vs_list={asof['vs_list'].mean():+.3f}")

    top = (
        daily.groupby(["sku", "location"], as_index=False)["units"]
        .sum()
        .sort_values("units", ascending=False)
        .head(3)
    )
    print("  top SKU-locations by volume:")
    for _, r in top.iterrows():
        print(f"    {r['sku']}@{r['location']}: {int(r['units'])}")
    print("OK pandas_black_belt — groupby/resample/merge_asof landed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
