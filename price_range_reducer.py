import sys

counts = {}
current_range = None
total = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    prange, one = parts
    one = int(one)
    if current_range == prange:
        total += one
    else:
        if current_range:
            counts[current_range] = total
        current_range = prange
        total = one

if current_range:
    counts[current_range] = total

# Sắp xếp theo số lượng giảm dần
for prange, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{prange}\t{cnt}")
