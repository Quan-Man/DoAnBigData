import sys

counts = {}
current_product = None
total_sold = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    product, sold = parts
    sold = int(sold)
    if current_product == product:
        total_sold += sold
    else:
        if current_product:
            counts[current_product] = total_sold
        current_product = product
        total_sold = sold

if current_product:
    counts[current_product] = total_sold

sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
for product, sold in sorted_items:
    print(f"{product}\t{sold}")
