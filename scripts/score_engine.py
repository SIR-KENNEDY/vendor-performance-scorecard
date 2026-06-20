"""
score_engine.py — Weighted vendor scoring, tier assignment, trend charts.
Run after generate_data.py.
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt, os

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW     = os.path.join(BASE,"data","raw")
OUTPUTS = os.path.join(BASE,"outputs"); os.makedirs(OUTPUTS, exist_ok=True)

df = pd.read_csv(f"{RAW}/vendor_deliveries.csv", parse_dates=["scheduled_date","actual_date"])
df["on_time"]     = (df["actual_date"] <= df["scheduled_date"]).astype(int)
df["qty_accurate"]= (df["qty_delivered"]/df["qty_ordered"]).between(0.95,1.05).astype(int)

def score(data):
    g = data.groupby(["vendor_id","vendor_name"]).agg(
        deliveries=("qty_ordered","count"),
        timeliness=("on_time","mean"),
        qty_acc=("qty_accurate","mean"),
        doc_acc=("waybill_clean","mean"),
        esc_rate=("escalation_flag","mean"),
    ).reset_index()
    g["score"] = (g["timeliness"]*35 + g["qty_acc"]*30 + g["doc_acc"]*20 + (1-g["esc_rate"])*15).round(2)
    g["tier"]  = pd.cut(g["score"],[0,55,70,85,100],labels=["🔴 Underperformer","🟠 At Risk","🟡 Satisfactory","🟢 Excellent"])
    return g.sort_values("score",ascending=False)

overall = score(df)
print("=== VENDOR SCORECARD ===")
print(overall[["vendor_name","deliveries","score","tier"]].to_string(index=False))
overall.to_csv(f"{OUTPUTS}/vendor_scorecard.csv", index=False)

# Monthly trend
rows = []
for m in df["month"].unique():
    s = score(df[df["month"]==m]).assign(month=m)
    rows.append(s)
pd.concat(rows).to_csv(f"{OUTPUTS}/vendor_monthly_trend.csv", index=False)

# Chart
fig, axes = plt.subplots(1,2,figsize=(14,6))
fig.suptitle("Vendor Performance Scorecard", fontsize=14, fontweight="bold")
cmap = {"🔴 Underperformer":"#e74c3c","🟠 At Risk":"#e67e22","🟡 Satisfactory":"#f1c40f","🟢 Excellent":"#27ae60"}
bcolors = [cmap.get(str(t),"steelblue") for t in overall["tier"]]
bars = axes[0].barh(overall["vendor_name"], overall["score"], color=bcolors)
for b,sc in zip(bars,overall["score"]):
    axes[0].text(b.get_width()+0.5, b.get_y()+b.get_height()/2, f"{sc:.1f}", va="center", fontsize=9)
for v,c,l in [(85,"green","Excellent"),(70,"orange","OK"),(55,"red","Review")]:
    axes[0].axvline(v,color=c,linestyle="--",alpha=0.6,linewidth=1)
axes[0].set_title("Composite Score by Vendor"); axes[0].set_xlim(0,110)

trend_df = pd.concat(rows)
for vname in overall["vendor_name"]:
    vd = trend_df[trend_df["vendor_name"]==vname].sort_values("month")
    axes[1].plot(vd["month"], vd["score"], marker="o", label=vname, linewidth=1.5)
axes[1].set_title("Score Trend by Vendor (12 months)")
axes[1].set_ylabel("Score"); axes[1].tick_params(axis="x",rotation=45)
axes[1].legend(fontsize=7); axes[1].axhline(70,color="orange",linestyle="--",alpha=0.5)

plt.tight_layout()
plt.savefig(f"{OUTPUTS}/vendor_scorecard_charts.png", dpi=150, bbox_inches="tight")
print("\n✅ Scorecard complete. Charts saved.")
