#!/usr/bin/env python3
import sys
from collections import defaultdict

data = defaultdict(lambda: {"Tiki": [0,0], "Hasaki": [0,0]})

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    parts = line.split("\t")
    if len(parts) != 2:
        continue
    brand, value = parts
    try:
        platform, rating = value.split(",")
        rating = float(rating)
    except:
        continue
    if platform in ["Tiki","Hasaki"]:
        data[brand][platform][0] += rating
        data[brand][platform][1] += 1

print("brand_name\tavg_rating_Tiki\tavg_rating_Hasaki")
for brand, d in data.items():
    avg_tiki = d["Tiki"][0]/d["Tiki"][1] if d["Tiki"][1]>0 else 0
    avg_hasaki = d["Hasaki"][0]/d["Hasaki"][1] if d["Hasaki"][1]>0 else 0
    print(f"{brand}\t{avg_tiki:.2f}\t{avg_hasaki:.2f}")
