# 🏆 Vendor Performance Scorecard System

![Python](https://img.shields.io/badge/Python-3.10-blue) ![SQL](https://img.shields.io/badge/SQL-Analytics-lightgrey) ![Domain](https://img.shields.io/badge/Domain-Supply_Chain-orange)

## Overview
Automated vendor scoring engine evaluating **8 logistics vendors** across 4 weighted KPIs. Generates monthly scorecards, assigns performance tiers, and flags underperformers for contract review.

## Scoring Framework
| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Delivery Timeliness | 35% | % deliveries on or before scheduled date |
| Quantity Accuracy | 30% | % deliveries within ±5% of ordered volume |
| Documentation Accuracy | 20% | % waybills with zero discrepancies |
| Escalation Rate | 15% | Inverse of escalation incidents per 100 deliveries |

**Tiers:** 🟢 Excellent (85–100) | 🟡 Satisfactory (70–84) | 🟠 At Risk (55–69) | 🔴 Underperformer (<55)

## How to Run
```bash
pip install -r requirements.txt
python scripts/generate_data.py
python scripts/score_engine.py
```

## Skills Demonstrated
`Scorecard Design` `KPI Engineering` `Weighted Scoring` `Python` `Pandas` `SQL` `Vendor Management`

---
*Kennedy Onuorah | [LinkedIn](https://www.linkedin.com/in/kennedy-onuorah-7a3793128)*
