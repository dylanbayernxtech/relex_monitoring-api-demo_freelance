# oracle_of_wmape

**Skill:** Demand forecasting duel — seasonal naive baseline vs sklearn `HistGradientBoostingRegressor`, scored with **WMAPE** and **bias** (not RMSE-only).

**RELEX relevance:** Forecast quality at SKU-location feeds replenishment; RELEX (Helsinki HQ) lives on WMAPE/bias language for retail F&R.

**Run:**
```bash
python arena/oracle_of_wmape/forecast_duel.py
```
Synthetic daily retail series; time-ordered holdout; prints OK line on success.
