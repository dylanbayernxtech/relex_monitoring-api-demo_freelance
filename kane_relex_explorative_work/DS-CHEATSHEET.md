# DS cheatsheet — retail demand / inventory (RELEX-shaped)

## Metrics (memorize)

```text
WMAPE = sum(|y - ŷ|) / sum(|y|)          # scale-free; watch zeros in denominator
Bias  = sum(ŷ - y) / sum(y)              # >0 ⇒ overforecast (bad for fresh waste)
RMSE  = sqrt(mean((y-ŷ)^2))              # sensitive to spikes; not enough alone
sMAPE = mean(2|y-ŷ|/(|y|+|ŷ|))           # careful with zeros

Pinball (quantile q): mean( (q - 1{y<ŷ}) * (y - ŷ) )
CRPS: proper scoring for full predictive distribution
```

**Interview line:** optimize the metric that matches the decision (mean vs high quantile for service level).

---

## Time-based split (never random rows)

```python
df = df.sort_values("date")
cut = df["date"].max() - pd.Timedelta(days=28)
train, test = df[df["date"] <= cut], df[df["date"] > cut]
```

For many SKU-locations: split by time **globally** (same cut date), evaluate micro/macro WMAPE.

---

## Baselines worth beating

| Baseline | When |
|----------|------|
| Seasonal naive (lag-7 / lag-365) | Strong weekly/annual seasonality |
| Moving average / SES | Smooth series |
| Croston / TSB-style | Intermittent demand |
| Same-weekday last week | Fast live-coding baseline |

```python
# Seasonal naive (weekly)
train = train.copy()
# merge lag7 onto test via date alignment per sku_location
```

---

## Feature ideas (causal + calendar)

- Calendar: dow, weekofyear, month, holiday flag  
- Lag: 1, 7, 14, 28; rolling mean/std 7/28  
- **Promo:** flag, depth (% off), type, display, media  
- **Price:** own price, relative price rank in category  
- **Weather:** temp, precip (and **interactions** with weekend)  
- Hierarchy keys: sku, category, store, cluster  
- Newness: days since intro, first-receipt flag  

---

## Sklearn quick paths

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import Ridge
from statsmodels.tsa.holtwinters import ExponentialSmoothing  # if prophet/lgbm missing

model = HistGradientBoostingRegressor(max_depth=6, learning_rate=0.08)
model.fit(X_train, y_train)
pred = model.predict(X_test)
```

**LightGBM / Prophet missing?** Say so and use HistGradientBoosting or Holt-Winters — interviewers care about rigor, not the logo.

---

## WMAPE / bias helpers

```python
import numpy as np

def wmape(y, yhat):
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    denom = np.abs(y).sum()
    return np.nan if denom == 0 else np.abs(y - yhat).sum() / denom

def bias(y, yhat):
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    denom = y.sum()
    return np.nan if denom == 0 else (yhat - y).sum() / denom
```

---

## Safety stock (interviewable sketch)

Normal demand & lead-time demand approximation:

```text
SS = z_{service} * σ_{L}
σ_{L} ≈ σ_demand * sqrt(L)     # if iid daily demand; else use lead-time demand history
ROP = lead_time_demand_mean + SS
```

Better: forecast **quantile** of demand over protection period (pinball-trained) → SS emerges from quantile − mean.

**MOQ / case pack:** round order up to MOQ; call out cost of lumpiness on waste.

---

## Promo uplift mini math

```text
uplift = demand_promo / demand_baseline - 1
# or regression: units ~ promo + price + dow + ...
# always check control SKUs / cannibalized siblings
```

---

## Pandas muscle

```python
g = df.groupby(["sku_location", "date"], as_index=False)["units"].sum()
g["lag7"] = g.groupby("sku_location")["units"].shift(7)
g["roll7"] = g.groupby("sku_location")["units"].transform(
    lambda s: s.shift(1).rolling(7, min_periods=1).mean()
)
```

---

## Optimization one-liner

```text
min cost(orders, stockouts, waste)
s.t. inventory balance, MOQ, capacity, service-level / fill-rate constraints
```

Heuristic: order-up-to / (s, S) from forecast quantiles when full MILP is too heavy.

---

## Live-coding checklist

1. Clarify grain (SKU-location? daily?) and horizon  
2. Time split + leakage check (no future lags)  
3. Baseline → model → table of WMAPE/bias  
4. Call out intermittency / zeros / promo leakage  
5. Tie forecast to a decision (ROP / order qty / promo buy-in)
