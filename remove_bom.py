import os

def remove_bom(filename):
    with open(filename, "rb") as f:
        data = f.read()
    if data.startswith(b'\xef\xbb\xbf'):
        with open(filename, "wb") as f:
            f.write(data[3:])
        print(f" Đã loại bỏ BOM khỏi: {filename}")
    else:
        print(f" Không có BOM trong: {filename}")

# Xử lý tất cả file CSV trong thư mục hiện tại
for file in os.listdir('.'):
    if file.endswith('.csv'):
        remove_bom(file)

