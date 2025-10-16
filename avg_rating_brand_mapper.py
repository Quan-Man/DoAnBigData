import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Tên sản phẩm"):
        continue
    reader = csv.reader([line], delimiter=',')
    row = next(reader)
    if len(row) < 7:
        continue
    brand_name = row[2].strip()
    try:
        rating_average = float(row[4].replace(',', '.'))
    except ValueError:
        continue
    print(f"{brand_name}\t{rating_average}")
