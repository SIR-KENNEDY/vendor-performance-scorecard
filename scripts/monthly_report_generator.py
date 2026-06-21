"""
monthly_report_generator.py
============================
Generates a monthly vendor performance report:
  - Scores each vendor for the specified month
  - Compares to prior month (MoM change)
  - Flags vendors whose score dropped >10 points
  - Saves a formatted summary report to outputs/

Usage: python scripts/monthly_report_generator.py --month 2023-06
"""
import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW     = os.path.join(BASE, "data", "raw")
OUTPUTS = os.path.join(BASE, "outputs")
os.makedirs(OUTPUTS, exist_ok=True)

parser = argparse.ArgumentParser()
parser.add_argument("--month", default="2023-06", help="Month to report (YYYY-MM)")
args = parser.parse_args()
REPORT_MONTH = args.month

df = pd.read_csv(f"{RAW}/vendor_deliveries.csv", parse_dates=["scheduled_date","actual_date"])
df["on_time"]      = (df["actual_date"] <= df["scheduled_date"]).astype(int)
df["qty_accurate"] = ((df["qty_delivered"]/df["qty_ordered"]).between(0.95,1.05)).astype(int)

def score_month(data, month_label):
    sub = data[data["month"] == month_label]
    if len(sub) == 0: return pd.DataFrame()
    g = sub.groupby(["vendor_id","vendor_name"]).agg(
        deliveries=("qty_ordered","count"),
        timeliness=("on_time","mean"),
        accuracy=("qty_accurate","mean"),
        doc_acc=("waybill_clean","mean"),
        esc_rate=("escalation_flag","mean"),
    ).reset_index()
    g["score"] = (g["timeliness"]*35 + g["accuracy"]*30 + g["doc_acc"]*20 + (1-g["esc_rate"])*15).round(2)
    return g.set_index("vendor_id")

# Find prior month
current_dt = datetime.strptime(REPORT_MONTH, "%Y-%m")
month_num  = current_dt.month - 1 if current_dt.month > 1 else 12
year_num   = current_dt.year if current_dt.month > 1 else current_dt.year - 1
PRIOR_MONTH = f"{year_num}-{month_num:02d}"

current = score_month(df, REPORT_MONTH)
prior   = score_month(df, PRIOR_MONTH)

if current.empty:
    print(f"No data found for month: {REPORT_MONTH}")
    exit()

report = current[["vendor_name","deliveries","score"]].copy()
if not prior.empty:
    report["prior_score"]   = prior["score"]
    report["score_change"]  = (report["score"] - report["prior_score"]).round(2)
    report["trend"]         = report["score_change"].apply(
        lambda x: "📈 UP" if x > 2 else ("📉 DOWN" if x < -2 else "➡️ STABLE"))
    report["flag"]          = report["score_change"].apply(
        lambda x: "⚠️ ALERT: Dropped >10pts" if x < -10 else "")

report["tier"] = pd.cut(report["score"],[0,55,70,85,100],
    labels=["🔴 Underperformer","🟠 At Risk","🟡 Satisfactory","🟢 Excellent"])
report = report.sort_values("score", ascending=False)

print(f"\n{'='*60}")
print(f"  VENDOR PERFORMANCE REPORT — {REPORT_MONTH}")
print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{'='*60}")
print(report.to_string())

alerts = report[report.get("flag","").str.contains("ALERT", na=False)] if "flag" in report.columns else pd.DataFrame()
if len(alerts):
    print(f"\n⚠️  ALERTS — Vendors requiring immediate review:")
    for _, row in alerts.iterrows():
        print(f"   {row['vendor_name']}: score dropped {abs(row['score_change']):.1f} pts to {row['score']:.1f}")

fname = f"{OUTPUTS}/vendor_report_{REPORT_MONTH}.csv"
report.to_csv(fname)
print(f"\n✅ Report saved: {fname}")
