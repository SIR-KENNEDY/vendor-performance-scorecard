# 📓 Vendor Performance Scorecard — Guide

## Business Context
Telecom tower operators depend on logistics vendors to deliver diesel fuel reliably.
Poor vendor performance leads to:
- Site fuel-outs → network downtime → SLA penalties
- Quantity shortfalls → unplanned emergency top-ups (costly)
- Documentation errors → reconciliation disputes → payment delays

This scorecard system provides an objective, data-driven way to evaluate vendors monthly.

---

## Scripts & Execution Order
```bash
python scripts/generate_data.py              # Creates 8-vendor dataset
python scripts/score_engine.py               # Overall & monthly scorecards
python scripts/monthly_report_generator.py   # Month-specific report
  --month 2023-06                            # Optional: specify month
```

---

## Scoring Formula
```
Composite Score = 
    (On-Time Delivery Rate × 35) +
    (Quantity Accuracy Rate × 30) +
    (Documentation Accuracy × 20) +
    ((1 - Escalation Rate) × 15)
```

All component scores normalised to 0–1 range before weighting.

## Performance Tiers
| Tier | Score | Action |
|------|-------|--------|
| 🟢 Excellent | 85–100 | Maintain / expand contract |
| 🟡 Satisfactory | 70–84 | Monitor, encourage improvement |
| 🟠 At Risk | 55–69 | Issue performance improvement plan |
| 🔴 Underperformer | < 55 | Contract review / replacement |

---

## Sample Results (Synthetic Data)
| Vendor | Score | Tier |
|--------|-------|------|
| Delta Logistics | 94.3 | 🟢 Excellent |
| FastFuel Ltd | 86.1 | 🟢 Excellent |
| SwiftHaul NG | 79.4 | 🟡 Satisfactory |
| NigerDiesel Co | 68.2 | 🟠 At Risk |
| EcoFuel Services | 48.7 | 🔴 Underperformer |

---

## How to Extend
- Add a new vendor: add entry to `VENDORS` dict in `generate_data.py`
- Adjust weights: modify `score_engine.py` scoring formula
- Change thresholds: adjust `bins` in `pd.cut()` call
- Add new KPI dimension: add column in `generate_data.py`, add to `score()` aggregation
