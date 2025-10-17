#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from collections import defaultdict

brand_data = defaultdict(lambda: {"Tiki": [], "Hasaki": []})

for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    try:
        brand, platform, price = line.split("\t")
        price = float(price)
        if platform in ["Tiki", "Hasaki"]:
            brand_data[brand][platform].append(price)
    except:
        continue

# Output trung bình giá theo brand và chênh lệch %
for brand, data in brand_data.items():
    tiki_avg = sum(data["Tiki"]) / len(data["Tiki"]) if data["Tiki"] else 0.0
    hasaki_avg = sum(data["Hasaki"]) / len(data["Hasaki"]) if data["Hasaki"] else 0.0
    diff_percent = ((tiki_avg - hasaki_avg) / hasaki_avg * 100) if hasaki_avg != 0 else 0.0
    print(f"{brand}\tTiki_avg: {tiki_avg:.2f}\tHasaki_avg: {hasaki_avg:.2f}\tDiff%: {diff_percent:.2f}")

