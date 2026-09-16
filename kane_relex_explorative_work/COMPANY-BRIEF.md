# RELEX Solutions — Company Brief (≈10 min skim)

*Research-backed from relexsolutions.com + Google Cloud customer story (2025–2026 materials). Facts can move — treat numbers as talking points, not scripture.*

---

## Snapshot

| | |
|--|--|
| **What** | AI-native unified platform for retail & supply-chain planning |
| **Founded** | 2005, Finland — Mikko Kärkkäinen, Johanna Småros, Michael Falck |
| **Name** | **RE**tail + **EX**cellence |
| **Scale** | ~**2,300** employees, **21** countries / ~20 offices; **600+** retail/CPG/wholesale/manufacturing customers |
| **Mission vibe** | Plan better → sell more → **waste less** (availability ↑, excess & spoilage ↓) |

Founders were supply-chain scientists frustrated by waste of product, time, and money in the consumer-goods value chain.

---

## Product surface (unified platform)

One data/decision fabric across:

1. **Demand forecasting** (ML + causal drivers)
2. **Inventory / replenishment** (incl. probabilistic thinking / safety stock)
3. **Merchandising / space**
4. **Pricing & promotions**
5. **Workforce** planning
6. **Manufacturing / production** planning

**Architecture of intelligence (how they talk about AI):**
- **Specialized AI** — ML + **mathematical optimization** + **heuristics** (the workhorse)
- **Generative AI** — e.g. **Rebot** (knowledge / best-practice assistant)
- **Agentic AI** — goal-oriented agents on top of specialized tools + near-real-time data (e.g. promo/pricing agent narratives on GCP)

**RELEX Labs / R&D signal:** centralized DS/AI R&D; publicly they invest heavily in R&D (~25% of revenue claimed in AI materials). Pattern: **ML forecast as base → optimize decisions on top**.

---

## DS problems they actually care about

- **Granular demand:** day × **SKU-location** (store/DC/channel), not only chain totals  
- **Drivers:** seasonality, weekday, **promo** (type, display, media), **price elasticity / relative price**, **weather**, local events, assortment/display changes  
- **Hard retail reality:** intermittency / long-tail, **cold-start / newness**, cannibalization & halo, phantom inventory, short-shelf-life / fresh  
- **Inventory:** service level vs stock investment; lead time; MOQ; capacity; waste vs stockout tradeoff  
- **Evaluation beyond RMSE:** **WMAPE**, **bias**, probabilistic scores (**pinball**, **CRPS**), hierarchical coherence  
- **Production:** plugin-style forecasting models, MLOps (monitor, version, redeploy as markets shift)

**Sustainability hook:** food retail/wholesale customers often cut food waste **10–40%**; RELEX cites ~**350 million kg** food waste saved for food retail customers in **2024** (~1.2M t CO₂e equivalent in their framing).

---

## Tech signals (interview-safe)

| Layer | Signals |
|-------|---------|
| Data / ML logic | **Python** |
| Backend | **Java / Kotlin** |
| Frontend | **React + TypeScript** |
| Runtime | **Kubernetes**, CI/CD, IaC |
| Cloud / data (public GCP story) | Cloud Storage, **BigQuery**, **Dataflow**, **Vertex AI** (forecast MLOps migration), **Gemini** agentic layer, **GKE** |
| Also mentioned in materials | Microsoft / **Azure**, **Snowflake** in some customer/partner contexts |

Google Cloud case study highlights: promo/pricing complexity (~20% of retail sales on promo); campaign ops **4+ hours → <2 minutes** with agent assist; Vertex AI for model lifecycle; NPS figures cited in that story (~62).

---

## Talking points that show research (use 2–3 max)

1. **“Forecast ≠ plan.”** RELEX differentiates by pairing ML demand with **optimization/heuristics** under real constraints — I’d expect DS work to be judged on decision quality (availability, waste, margin), not only point-forecast RMSE.  
2. **Causal retail features.** Promo uplift without cannibalization/halo and relative price is incomplete; weather × weekend interactions matter for fresh/BBQ-type categories.  
3. **Long-tail & hierarchy.** Sparse SKU-store series need **pooling / multilevel** structure; hierarchical reconciliation keeps store and chain coherent.  
4. **MLOps is the product.** Moving forecasting onto Vertex-style managed MLOps matches how a platform serves hundreds of customers with plugin models.  
5. **Waste is a first-class KPI.** Fresh + short shelf life turns overforecasting into CO₂ and margin — probabilistic safety stock and service-level targeting beat naive high buffers.

---

## Role-shaped expectations (from public careers)

- Own modelling **end-to-end** into live customer environments  
- Comfort with **production** data/pipelines, not only notebooks  
- Increasing emphasis on **AI-assisted / agentic** engineering  
- Domain: grocery/DIY/retail planning, pricing/promos, manufacturing optimization

---

## Sources to remember (if asked “where did you read that?”)

- relexsolutions.com/about/  
- relexsolutions.com/resources/ai-at-relex/  
- relexsolutions.com/resources/machine-learning-in-retail-demand-forecasting/  
- cloud.google.com/customers/relex  
- Careers engineering posts (Python / Kotlin-Java / React-TS / K8s)
