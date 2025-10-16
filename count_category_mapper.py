#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Tên sản phẩm"):
        continue
    reader = csv.reader([line])
    row = next(reader)
    if len(row) < 7:
        continue
    category = row[6].strip()
    print(f"{category}\t1")
