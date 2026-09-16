# Arena — arrogant senior DS drill packs

Self-contained Python drills for RELEX Solutions (Finland) DS interviews.
Each folder: `__init__.py`, `README.md`, one runnable main script (synthetic data, no network).

## Folders

| Folder | One-liner |
|--------|-----------|
| `oracle_of_wmape/` | Seasonal naive vs HistGBR; WMAPE + bias |
| `prophet_is_for_tourists/` | ETS + SARIMAX without Prophet |
| `sku_location_whisperer/` | Sparse SKU-location panel pooling |
| `promo_uplift_sniper/` | Promo uplift with confounders |
| `safety_stock_overlord/` | Service level / lead time / waste tradeoff |
| `feature_forge_supreme/` | Leakage-aware calendar/lag/rolling |
| `metrics_that_matter/` | WMAPE, bias, pinball, CRPS, MAPE traps |
| `pandas_black_belt/` | groupby, resample, merge_asof |
| `sql_in_python_cosplay/` | Window functions in pandas |
| `viz_or_it_didnt_happen/` | Matplotlib EDA quick plots |
| `mlops_theatre/` | Pipeline train/save/load + holdout |
| `cold_start_alchemist/` | Intermittent + new SKU neighbors |
| `interview_warmachine/` | `run_all.py` timed gauntlet |

```bash
# from repo root (activate .venv first)
python arena/interview_warmachine/run_all.py
```
