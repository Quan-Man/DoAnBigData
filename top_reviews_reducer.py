import sys

counts = {}
current_product = None
total_reviews = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    product, reviews = parts
    reviews = int(reviews)
    if current_product == product:
        total_reviews += reviews
    else:
        if current_product:
            counts[current_product] = total_reviews
        current_product = product
        total_reviews = reviews

if current_product:
    counts[current_product] = total_reviews

# Sắp xếp giảm dần và lấy top 10
sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
for product, rev in sorted_items:
    print(f"{product}\t{rev}")
