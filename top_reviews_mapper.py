import sys
import csv

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Tên sản phẩm"):  # Bỏ qua header
        continue
    reader = csv.reader([line], delimiter=',')
    row = next(reader)
    if len(row) < 7:  # Đảm bảo đủ 7 cột
        continue
    product_name = row[0].strip()
    try:
        review_count = int(row[5].replace(',', '').split()[0])  # Xử lý nếu có text kèm số
    except ValueError:
        continue
    print(f"{product_name}\t{review_count}")
