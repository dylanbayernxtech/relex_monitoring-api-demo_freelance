# RELEX interview — talking points (8–12 punchy lines)

Say these out loud once. Pick **3 insights** + **2 questions** for the room.

---

## Insight soundbites

1. **“I’d start at SKU-location, then decide where to pool.”**  
   Store-level intermittency is the norm; pooling across stores/products beats overfit SKU-store models on the long tail.

2. **“Point forecast accuracy is necessary but not sufficient.”**  
   Replenishment cares about **service level vs inventory** — I’d pair WMAPE/bias with a probabilistic view (quantile / pinball) for safety stock.

3. **“Promo uplift without cannibalization is a fiction.”**  
   Category switches and halo effects change the *system* forecast; optimizing one SKU in isolation creates waste elsewhere.

4. **“Cold-start and newness need priors, not empty history.”**  
   Attributes, analogs, and hierarchical shrinkage beat waiting for 52 weeks of sparse sales.

5. **“Phantom inventory and on-shelf availability break the label.”**  
   If POS understates true demand when the shelf is empty, naive loss functions train on the wrong target — censoring / lost-sales adjustments matter.

6. **“ML forecast → optimize under constraints.”**  
   That’s the RELEX-shaped loop: predict demand, then MOQ, lead time, capacity, waste, and labor turn it into an actionable order.

7. **“I’d distrust RMSE-only scorecards in retail.”**  
   WMAPE for scale-free comparison, bias for systematic over/under (critical for fresh), CRPS/pinball when we stock to a quantile.

8. **“Weather and promo are causal features, not calendar dummies.”**  
   Interactions (sunny × weekend) and relative price vs category often dominate raw temperature or a flat “promo flag.”

---

## Smart questions (ask 2)

9. **Forecast → decision:** “How do you measure success for a forecasting change — forecast metrics, or downstream availability / waste / margin in production?”

10. **Hierarchy & plugins:** “As you move to more purpose-built / plugin forecasting models, how do you keep hierarchical coherence and avoid customer-specific model sprawl?”

11. **Probabilistic inventory:** “For short-shelf-life categories, how explicit is the quantile / service-level target in the product vs heuristics on top of a mean forecast?”

12. **MLOps & agents:** “With Vertex-style MLOps and Gemini agents for promo planning, where should a DS hire spend time — model science, evaluation harnesses, or tool quality for agents?”

---

## 30-second opener (optional)

> “I’m excited by RELEX because the hard problem isn’t only predicting units — it’s turning probabilistic demand into replenishment and promo decisions under waste, service level, and supply constraints, at SKU-location scale. I’ve prepped around WMAPE/bias, promo uplift, and safety-stock thinking, and I’d love to dig into how your Labs / product teams evaluate models in production.”

## Process flex
If asked how you would deliver: explore fast, then freeze a small module with a CLI entrypoint — notebooks are for narrative, not the source of truth in a plugin-forecasting shop.
