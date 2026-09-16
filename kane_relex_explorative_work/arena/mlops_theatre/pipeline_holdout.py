#!/usr/bin/env python3
"""mlops_theatre — train/save/load sklearn pipeline + time holdout (Vertex AI cosplay)."""
from __future__ import annotations

import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / d) if d else float("nan")


def make_data(n: int = 500, seed: int = 2) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2024-01-01", periods=n, freq="D")
    loc = rng.choice(["HEL", "TMP", "OUL"], n)
    promo = (rng.random(n) < 0.1).astype(int)
    dow = dates.dayofweek
    units = 20 + 5 * (dow >= 5) + 12 * promo + rng.normal(0, 3, n)
    return pd.DataFrame({"date": dates, "location": loc, "promo": promo, "dow": dow,
                         "units": np.clip(units, 0, None)})


def main() -> int:
    print("=== mlops_theatre: pipeline + holdout protocol ===")
    df = make_data()
    split = int(len(df) * 0.8)
    train, test = df.iloc[:split], df.iloc[split:]
    feats = ["location", "promo", "dow"]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["location"]),
        ("num", "passthrough", ["promo", "dow"]),
    ])
    pipe = Pipeline([
        ("pre", pre),
        ("model", HistGradientBoostingRegressor(max_iter=60, max_depth=3, random_state=0)),
    ])
    pipe.fit(train[feats], train["units"])
    pred = pipe.predict(test[feats])
    print(f"  holdout_WMAPE={wmape(test['units'], pred):.4f}")

    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "relex_demand_pipe.joblib"
        joblib.dump(pipe, path)
        loaded = joblib.load(path)
        pred2 = loaded.predict(test[feats])
        assert np.allclose(pred, pred2)
        print(f"  saved+loaded {path.name}  preds_match=True")
    print("  protocol: time-ordered holdout → fit pipeline → artifact → reload smoke")
    print("OK mlops_theatre — Vertex-flavored theatre, real sklearn bones")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
