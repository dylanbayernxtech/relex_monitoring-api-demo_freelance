#!/usr/bin/env python3
"""cold_start_alchemist - new SKU + intermittent demand tricks."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def croston_like(demand: np.ndarray, alpha: float = 0.1) -> float:
    """Simple Croston-ish point forecast: a / q where a=demand size, q=interval."""
    demand = np.asarray(demand, float)
    nz = np.flatnonzero(demand > 0)
    if len(nz) == 0:
        return 0.0
    sizes = demand[nz]
    intervals = np.diff(nz, prepend=nz[0] - (nz[1] - nz[0] if len(nz) > 1 else 7))
    a, q = float(sizes.mean()), float(max(intervals.mean(), 1.0))
    # EWMA nudge
    a_s = sizes[0]
    q_s = intervals[0] if intervals[0] > 0 else q
    for s, iv in zip(sizes[1:], intervals[1:]):
        a_s = alpha * s + (1 - alpha) * a_s
        q_s = alpha * iv + (1 - alpha) * q_s
    return float(a_s / max(q_s, 1.0))


def main() -> int:
    print("=== cold_start_alchemist: new SKU + intermittent ===")
    rng = np.random.default_rng(99)
    # intermittent series
    n = 120
    dem = np.zeros(n)
    hits = rng.choice(n, size=18, replace=False)
    dem[hits] = rng.integers(1, 8, size=18)
    crost = croston_like(dem)
    naive = dem.mean()
    print(f"  intermittent  croston?{crost:.3f}  mean_naive={naive:.3f}  nonzero_rate={ (dem>0).mean():.1%}")

    # cold-start new SKU: borrow from similar attributes
    catalog = pd.DataFrame({
        "sku": [f"S{i}" for i in range(20)],
        "category": rng.integers(0, 4, 20),
        "price_band": rng.integers(0, 3, 20),
        "brand_tier": rng.integers(0, 3, 20),
        "avg_daily": rng.uniform(2, 30, 20),
    })
    cols = ["category", "price_band", "brand_tier"]
    new = pd.DataFrame([[1, 2, 1]], columns=cols)
    nn = NearestNeighbors(n_neighbors=5).fit(catalog[cols])
    dist, idx = nn.kneighbors(new)
    proxy = float(catalog.iloc[idx[0]]["avg_daily"].mean())
    print(f"  cold_start_proxy_avg_daily={proxy:.2f}  neighbor_dists={np.round(dist[0], 2)}")
    print("OK cold_start_alchemist - intermittent + attribute neighbors transmuted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
