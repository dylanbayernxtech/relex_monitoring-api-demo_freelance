#!/usr/bin/env python3
"""10-second env + practice-data sanity check for RELEX interview morning."""
from __future__ import annotations

import importlib.util
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    t0 = time.perf_counter()
    print("=== RELEX prep warmup ===")
    print(f"ROOT: {ROOT}")

    pkgs = ["numpy", "pandas", "sklearn", "matplotlib", "plotly", "statsmodels", "scipy"]
    missing = []
    for name in pkgs:
        try:
            importlib.import_module(name)
            print(f"  OK  {name}")
        except Exception as e:  # noqa: BLE001
            missing.append(name)
            print(f"  MISSING  {name}: {e}")

    optional = []
    for name in ("lightgbm", "prophet"):
        try:
            importlib.import_module(name)
            print(f"  OK  {name} (optional)")
            optional.append(name)
        except Exception:
            print(f"  skip {name} (optional) — use HistGradientBoosting / ExponentialSmoothing")

    # Ensure synthetic data exists and solved scripts run quickly
    spec = importlib.util.spec_from_file_location("d01", ROOT / "practice" / "01_demand_forecast.py")
    d01 = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(d01)
    df = d01.load_or_create()
    assert len(df) > 100 and {"date", "sku_location", "units"} <= set(df.columns)
    print(f"  OK  practice data rows={len(df)} sku_locations={df['sku_location'].nunique()}")

    # Tiny metric smoke
    y = df["units"].to_numpy()[:50]
    yhat = y * 0.9
    w = d01.wmape(y, yhat)
    b = d01.bias(y, yhat)
    print(f"  OK  wmape_smoke={w:.3f} bias_smoke={b:+.3f}")

    elapsed = time.perf_counter() - t0
    if missing:
        print(f"\nENV INCOMPLETE ({elapsed:.1f}s) — missing: {', '.join(missing)}")
        print("Run bootstrap-windows.ps1 (Windows) or: python -m venv .venv && pip install -r requirements.txt")
        return 1

    print(f"\nENV OK ({elapsed:.1f}s) — optional loaded: {optional or 'none'}")
    print("Next: skim TALKING-POINTS.md, then python practice/solutions/01_demand_forecast_solved.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
