#!/usr/bin/env python3
"""safety_stock_overlord - service level, lead time, probabilistic stock."""
from __future__ import annotations

import numpy as np
from scipy import stats


def safety_stock(sigma_demand: float, lead_time_days: float, service_level: float) -> float:
    """SS = z * sigma * sqrt(L) for normal demand, constant lead time."""
    z = stats.norm.ppf(service_level)
    return float(z * sigma_demand * np.sqrt(lead_time_days))


def main() -> int:
    print("=== safety_stock_overlord: probabilistic inventory ===")
    rng = np.random.default_rng(42)
    # daily demand samples (SKU-location vibe)
    daily = rng.normal(loc=25, scale=6, size=500).clip(0)
    mu, sigma = float(daily.mean()), float(daily.std(ddof=1))
    lead = 5.0  # days
    for sl in (0.90, 0.95, 0.99):
        ss = safety_stock(sigma, lead, sl)
        rop = mu * lead + ss  # reorder point
        # Monte Carlo: stockouts over lead time
        lt_demand = rng.normal(mu * lead, sigma * np.sqrt(lead), size=8000).clip(0)
        fill = float((lt_demand <= rop).mean())
        print(f"  SL_target={sl:.0%}  SS={ss:.1f}  ROP={rop:.1f}  MC_in_stock?{fill:.1%}")

    # waste vs stockout tradeoff sketch
    holding_cost = 0.4  # per unit over-stock at LT end
    stockout_cost = 3.0
    best = None
    for q in np.linspace(mu * lead, mu * lead + 4 * sigma * np.sqrt(lead), 40):
        excess = np.maximum(q - lt_demand, 0).mean()
        short = np.maximum(lt_demand - q, 0).mean()
        cost = holding_cost * excess + stockout_cost * short
        if best is None or cost < best[0]:
            best = (cost, q, excess, short)
    print(f"  cost_min?{best[0]:.2f} at Q={best[1]:.1f}  E[waste]={best[2]:.1f} E[stockout]={best[3]:.1f}")
    print("OK safety_stock_overlord - service levels & waste/stockout tradeoff")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
