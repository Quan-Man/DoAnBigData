#!/usr/bin/env python3
import sys

current_category = None
count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    category, c = parts
    c = int(c)

    if current_category == category:
        count += c
    else:
        if current_category:
            print(f"{current_category}\t{count}")
        current_category = category
        count = c

# In category cuối cùng
if current_category:
    print(f"{current_category}\t{count}")
