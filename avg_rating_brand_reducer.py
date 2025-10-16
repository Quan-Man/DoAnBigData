#!/usr/bin/env python3
import sys

current_brand = None
total_rating = 0.0
count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 3:
        continue
    brand, rating, c = parts
    rating = float(rating)
    c = int(c)

    if current_brand == brand:
        total_rating += rating
        count += c
    else:
        if current_brand:
            avg = total_rating / count
            print(f"{current_brand}\t{avg:.2f}")
        current_brand = brand
        total_rating = rating
        count = c

# In brand cuối cùng
if current_brand:
    avg = total_rating / count
    print(f"{current_brand}\t{avg:.2f}")

