# Finland senior DS / Python bar (RELEX-shaped)

What Finnish senior technical interviewers and RELEX-style DS engineers usually expect in a **finished task artifact**:

1. **Runnable from terminal** — \python solution.py\ (or \python -m package\) exits 0 and prints key metrics.
2. **Time-aware validation** — no random shuffle on demand series; explicit train/holdout cut.
3. **Business metrics** — WMAPE + bias (and a baseline). RMSE alone is weak.
4. **SKU-location awareness** — say if you pooled stores or modeled at SKU-store grain.
5. **Assumptions written once** — lead time, service level, promo definition, missing data.
6. **Small, readable modules** — functions > 200-line cell soup; notebooks only as thin narrative.
7. **Reproducibility** — seed where stochastic; pin deps in requirements if you add packages.
8. **Honest limits** — what would break in production (cold start, intermittency, leakage).

Keep it simple. Prefer one clear script over a clever framework.
