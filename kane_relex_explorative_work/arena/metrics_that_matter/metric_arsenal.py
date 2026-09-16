#!/usr/bin/env python3
"""metrics_that_matter — WMAPE, bias, pinball, CRPS-ish, MAPE traps."""
from __future__ import annotations

import numpy as np


def wmape(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float(np.abs(y - yhat).sum() / d) if d else float("nan")


def bias(y, yhat) -> float:
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    d = np.abs(y).sum()
    return float((yhat - y).sum() / d) if d else float("nan")


def mape_trap(y, yhat) -> float:
    """Classic MAPE: explodes / undefined on zeros — retail intermittent trap."""
    y, yhat = np.asarray(y, float), np.asarray(yhat, float)
    mask = y != 0
    if not mask.any():
        return float("nan")
    return float(np.mean(np.abs((y[mask] - yhat[mask]) / y[mask])))


def pinball(y, yhat_q, q: float) -> float:
    y, yhat_q = np.asarray(y, float), np.asarray(yhat_q, float)
    e = y - yhat_q
    return float(np.mean(np.where(e >= 0, q * e, (q - 1) * e)))


def crps_gaussian(y, mu, sigma) -> float:
    """Closed-form CRPS for N(mu, sigma^2) — probabilistic forecast score."""
    y, mu, sigma = np.asarray(y, float), np.asarray(mu, float), np.asarray(sigma, float)
    z = (y - mu) / sigma
    # CRPS = sigma * ( z(2Phi(z)-1) + 2phi(z) - 1/sqrt(pi) )
    from scipy.stats import norm
    term = z * (2 * norm.cdf(z) - 1) + 2 * norm.pdf(z) - 1 / np.sqrt(np.pi)
    return float(np.mean(sigma * term))


def main() -> int:
    print("=== metrics_that_matter: arsenal ===")
    rng = np.random.default_rng(9)
    y = rng.poisson(8, 200).astype(float)
    y[::7] = 0  # intermittent zeros
    yhat = y * 0.9 + rng.normal(0, 1, len(y))
    print(f"  WMAPE={wmape(y, yhat):.4f}  bias={bias(y, yhat):+.4f}")
    print(f"  MAPE(on nonzeros)={mape_trap(y, yhat):.4f}  ← ignores zeros; still a trap in storytelling")
    q50 = np.full_like(y, np.median(y))
    q90 = np.full_like(y, np.quantile(y, 0.9))
    print(f"  pinball@0.5={pinball(y, q50, 0.5):.4f}  pinball@0.9={pinball(y, q90, 0.9):.4f}")
    print(f"  CRPS_gauss={crps_gaussian(y, mu=y.mean(), sigma=y.std()):.4f}")
    print("  RELEX vibe: WMAPE/bias for point; pinball/CRPS for quantile replenishment")
    print("OK metrics_that_matter — arsenal locked and loaded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
