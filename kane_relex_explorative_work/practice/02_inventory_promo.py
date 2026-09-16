#!/usr/bin/env python3
"""
RELEX-style practice 02 — Safety stock OR promo uplift mini-case

SUCCESS criteria (pick track A or B — solved script does BOTH)
----------------------------------------------------------------
Track A — Safety stock
  - From daily demand history, estimate mean & std of lead-time demand
  - Compute SS for a target service level (e.g. 95% → z≈1.65)
  - Produce reorder point; state assumptions (iid days, normal LT demand)
  - Show how overforecast bias would inflate waste for short shelf life

Track B — Promo uplift
  - Estimate promo uplift vs non-promo baseline (simple ratio + regression)
  - Report uplift % and note cannibalization caveat

Run:  python practice/02_inventory_promo.py
Hint: see practice/solutions/02_inventory_promo_solved.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "practice" / "data" / "demand_daily.csv"


def load_demand() -> pd.DataFrame:
    if not DATA.exists():
        # generate via 01
        import runpy

        runpy.run_path(str(ROOT / "practice" / "01_demand_forecast.py"), run_name="__gen__")
        # call maker directly
        from importlib.util import module_from_spec, spec_from_file_location

        spec = spec_from_file_location("demand01", ROOT / "practice" / "01_demand_forecast.py")
        mod = module_from_spec(spec)
        assert spec.loader
        spec.loader.exec_module(mod)
        df = mod.make_synthetic()
        DATA.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(DATA, index=False)
    return pd.read_csv(DATA, parse_dates=["date"])


def main() -> None:
    df = load_demand()
    print(f"Loaded {len(df)} rows — implement Track A and/or B (see solutions/).")
    raise NotImplementedError("Implement safety stock and/or promo uplift analysis.")


if __name__ == "__main__":
    argparse.ArgumentParser().parse_args()
    main()
