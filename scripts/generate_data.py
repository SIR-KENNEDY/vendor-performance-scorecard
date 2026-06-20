"""generate_data.py — 8 vendors with distinct performance profiles, 12 months."""
import pandas as pd, numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(77)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(BASE, "data", "raw"); os.makedirs(RAW, exist_ok=True)

# Each vendor: (name, on_time_rate, qty_accuracy, doc_accuracy, escalation_rate)
VENDORS = {
    "V001": ("FastFuel Ltd",       0.92, 0.96, 0.97, 0.02),
    "V002": ("NigerDiesel Co",     0.75, 0.89, 0.90, 0.06),
    "V003": ("SwiftHaul NG",       0.88, 0.94, 0.95, 0.03),
    "V004": ("PrimeLogistics",     0.55, 0.80, 0.85, 0.10),
    "V005": ("EcoFuel Services",   0.48, 0.75, 0.82, 0.12),
    "V006": ("RapidSupply Co",     0.82, 0.91, 0.93, 0.04),
    "V007": ("Continental Fuels",  0.70, 0.86, 0.88, 0.07),
    "V008": ("Delta Logistics",    0.95, 0.98, 0.99, 0.01),
}
START = datetime(2023, 1, 1)
records = []
for vid, (vname, t, a, d, e) in VENDORS.items():
    for m in range(12):
        base = START + timedelta(days=30*m)
        for _ in range(np.random.randint(40, 80)):
            qty_o = round(np.random.uniform(500, 5000))
            accurate = np.random.random() < a
            var = np.random.uniform(-0.02,0.02) if accurate else np.random.uniform(-0.15,-0.05)
            on_time = np.random.random() < t
            sched = base + timedelta(days=int(np.random.randint(1,28)))
            actual = sched if on_time else sched + timedelta(days=int(np.random.randint(1,5)))
            records.append({"vendor_id":vid,"vendor_name":vname,
                "scheduled_date":sched.strftime("%Y-%m-%d"),
                "actual_date":actual.strftime("%Y-%m-%d"),
                "qty_ordered":qty_o,"qty_delivered":round(qty_o*(1+var)),
                "waybill_clean":int(np.random.random()<d),
                "escalation_flag":int(np.random.random()<e),
                "month":base.strftime("%Y-%m")})
pd.DataFrame(records).to_csv(f"{RAW}/vendor_deliveries.csv", index=False)
print(f"Generated {len(records):,} vendor delivery records.")
