#!/usr/bin/env python3
"""interview_warmachine - timed mini-challenges runner for all arena drills."""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ARENA = Path(__file__).resolve().parent.parent

DRILLS = [
    ("oracle_of_wmape", "forecast_duel.py"),
    ("prophet_is_for_tourists", "ets_arima_cosplay.py"),
    ("sku_location_whisperer", "panel_pool.py"),
    ("promo_uplift_sniper", "uplift_regression.py"),
    ("safety_stock_overlord", "prob_inventory.py"),
    ("feature_forge_supreme", "leakage_aware_features.py"),
    ("metrics_that_matter", "metric_arsenal.py"),
    ("pandas_black_belt", "messy_retail_kungfu.py"),
    ("sql_in_python_cosplay", "window_cosplay.py"),
    ("viz_or_it_didnt_happen", "eda_quickplots.py"),
    ("mlops_theatre", "pipeline_holdout.py"),
    ("cold_start_alchemist", "intermittent_new_sku.py"),
]


def main() -> int:
    print("=== interview_warmachine: run_all ===")
    print(f"ARENA={ARENA}")
    t0 = time.perf_counter()
    failed = []
    for folder, script in DRILLS:
        path = ARENA / folder / script
        print(f"\n--- {folder}/{script} ---")
        ts = time.perf_counter()
        proc = subprocess.run([sys.executable, str(path)], cwd=str(ARENA / folder))
        dt = time.perf_counter() - ts
        status = "PASS" if proc.returncode == 0 else "FAIL"
        print(f">>> {status} ({dt:.1f}s)")
        if proc.returncode != 0:
            failed.append(f"{folder}/{script}")
    elapsed = time.perf_counter() - t0
    print("\n=== warmachine summary ===")
    print(f"  drills={len(DRILLS)}  failed={len(failed)}  wall={elapsed:.1f}s")
    if failed:
        print("  FAIL list:", ", ".join(failed))
        return 1
    print("OK interview_warmachine - all drills green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
