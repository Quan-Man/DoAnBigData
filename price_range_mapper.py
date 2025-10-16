import sys
import csv

def get_price_range(price):
    if price <= 100000:
        return "0-100k"
    elif price <= 300000:
        return "100k-300k"
    elif price <= 500000:
        return "300k-500k"
    elif price <= 1000000:
        return "500k-1tr"
    else:
        return "1tr+"

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Tên sản phẩm"):
        continue
    reader = csv.reader([line], delimiter=',')
    row = next(reader)
    if len(row) < 7:
        continue
    try:
        price_str = row[1].replace(',', '').replace(' VND', '').split()[0]
        price = int(price_str)
    except ValueError:
        continue
    price_range = get_price_range(price)
    print(f"{price_range}\t1")
