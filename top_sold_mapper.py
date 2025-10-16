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
    product_name = row[0].strip()
    try:
        sold_count = int(row[3].replace(',', ''))
    except ValueError:
        continue
    print(f"{product_name}\t{sold_count}")
