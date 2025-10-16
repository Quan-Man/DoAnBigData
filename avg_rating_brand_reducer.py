import sys

ratings = {}
current_brand = None
total_rating = 0.0
count = 0

for line in sys.stdin:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue
    brand, rating = parts
    rating = float(rating)
    if current_brand == brand:
        total_rating += rating
        count += 1
    else:
        if current_brand:
            ratings[current_brand] = total_rating / count
        current_brand = brand
        total_rating = rating
        count = 1

if current_brand:
    ratings[current_brand] = total_rating / count

for brand, avg in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
    print(f"{brand}\t{avg:.2f}")
