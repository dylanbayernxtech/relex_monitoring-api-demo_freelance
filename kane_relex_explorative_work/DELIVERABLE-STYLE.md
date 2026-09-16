# Deliverable style for RELEX (senior signal)

## Verdict
**Notebook-only = noob-adjacent for a senior RELEX DS / forecasting assignment.**
**Slick = modular .py you can run from a terminal + optional thin notebook that only narrates.**

RELEX ships forecasting into live customer environments (plugin models, MLOps, scale). Interviewers will weight:
- time-ordered validation (no shuffle leakage)
- WMAPE / bias (not RMSE cosplay)
- SKU-location thinking
- reproducible entrypoints (python path/to/script.py)
- clarity under ambiguity

A .ipynb full of unreproducible cell state fights that story. A notebook used as a scratchpad while you crystallize functions into modules is fine mid-session — just do not submit the scratchpad as the artifact.

## Default tomorrow
1. Work in **.py files** under practice/ or a fresh solution/ module.
2. Keep a **single runnable script** that prints metrics and exits 0.
3. If they hand you a notebook template: use it for plots/narrative, move logic into functions/modules immediately.
4. Skip spinning up Jupyter unless they explicitly ask for a notebook.

## Anti-patterns
- Hidden state / run-cells-out-of-order
- Absolute local paths only
- Metrics without a baseline
- Train/test leak via random split on time series
