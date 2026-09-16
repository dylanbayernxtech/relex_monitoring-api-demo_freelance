# Agent context — RELEX Solutions interview prep

**Who:** Dylan Kane  
**What:** Data science interview with **RELEX Solutions** (Finland)  
**Where (Windows):** `C:\Users\Dylan Kane\xPathfinderLabs\relex-interview-prep\`  
**Machine:** DESKTOP-B58J3QQ (`81eb253b-e9d3-4d99-853f-990d760d9eb5`)

## Non-negotiables
- Local files only — **no gh auth**, **no emails**, **no SendKeys / GUI focus stealing**.
- Prefer editing files under this folder; keep practice data synthetic.
- If installing packages: use `.venv` here; no CUDA stacks. Skip LightGBM/Prophet if they fail; use HistGradientBoosting / ExponentialSmoothing.

## RELEX in one paragraph
Finnish AI-native retail/CPG planning platform (founded 2005 by Mikko Kärkkäinen, Johanna Småros, Michael Falck). ~2300 employees, 21 countries, 600+ customers. Unified suite: demand forecasting, replenishment/inventory, merchandising, pricing/promotions, workforce, manufacturing. DS core = ML forecast → mathematical optimization / heuristics on top. Big public claim: ~350M kg food waste saved for food retail customers in 2024. Tech signals: Python (data/optimization), Java/Kotlin backend, React/TS frontend, K8s; Google Cloud (BigQuery, Dataflow, Vertex AI, Gemini agents) plus Azure/Snowflake in some materials.

## Interview vocabulary to reinforce
SKU-location, service level vs inventory, intermittency, cold-start/newness, promo uplift & cannibalization/halo, lead time, MOQ, phantom inventory, WMAPE/bias/pinball/CRPS, hierarchical forecasting, causal features (promo/price/weather), constraint optimization, MLOps.

## Pack map
- `README.md` — 5-min warm-up path
- `COMPANY-BRIEF.md` — 10-min skim
- `TALKING-POINTS.md` — soundbites + smart questions
- `DS-CHEATSHEET.md` — pandas/forecast/opt cheat sheet
- `practice/` — timed coding drills + `solutions/`
- `warmup.py` — env sanity check
- `bootstrap-windows.ps1` — create Windows `.venv` + pip install

When helping Dylan: keep answers interview-ready, metric-aware (not RMSE-only), and tied to retail replenishment reality.
