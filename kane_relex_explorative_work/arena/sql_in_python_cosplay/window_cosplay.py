#!/usr/bin/env python3
"""sql_in_python_cosplay - pandas window equivalents interviewers love."""
from __future__ import annotations

import numpy as np
import pandas as pd


def main() -> int:
    print("=== sql_in_python_cosplay: window functions ===")
    rng = np.random.default_rng(3)
    dates = pd.date_range("2024-01-01", periods=28, freq="D")
    rows = []
    for sku in ("X", "Y"):
        for loc in ("L1", "L2"):
            for d in dates:
                rows.append({"date": d, "sku": sku, "loc": loc, "units": int(rng.poisson(10))})
    df = pd.DataFrame(rows).sort_values(["sku", "loc", "date"])

    g = df.groupby(["sku", "loc"], group_keys=False)
    # ROW_NUMBER() OVER (PARTITION BY sku, loc ORDER BY date)
    df["rn"] = g.cumcount() + 1
    # LAG(units, 1)
    df["lag1"] = g["units"].shift(1)
    # SUM(units) OVER (PARTITION BY sku, loc ORDER BY date ROWS 6 PRECEDING)
    df["roll7"] = g["units"].transform(lambda s: s.rolling(7, min_periods=1).sum())
    # RANK by total volume
    totals = df.groupby(["sku", "loc"])["units"].sum().rank(ascending=False, method="dense")
    df["vol_rank"] = df.set_index(["sku", "loc"]).index.map(totals)

    # QUALIFY-ish: last 7 days per partition
    last7 = df[df["rn"] > df.groupby(["sku", "loc"])["rn"].transform("max") - 7]
    print(f"  rows={len(df)}  last7_rows={len(last7)}  lag1_nulls={df['lag1'].isna().sum()}")
    print(f"  sample roll7 mean={df['roll7'].mean():.1f}  distinct vol_ranks={df['vol_rank'].nunique()}")
    print("OK sql_in_python_cosplay - windows without a database")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
