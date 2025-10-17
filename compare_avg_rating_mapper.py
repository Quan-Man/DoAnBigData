#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Tên sản phẩm"):
        continue
    reader = csv.reader([line])
    row = next(reader)
    if len(row) < 8:
        continue
    brand = row[2].strip()
    platform = row[7].strip()
    try:
        rating = float(row[4].replace(",","."))
    except:
        continue
    print(f"{brand}\t{platform},{rating}")
