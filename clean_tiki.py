# clean_tiki.py
import pandas as pd

# Đọc file dữ liệu thô
df = pd.read_csv("tiki_raw.csv")

# 1. Bỏ sản phẩm không có giá hoặc tên
df = df.dropna(subset=["Tên sản phẩm", "Giá (VNĐ)"])

# 2. Chuẩn hóa cột "Thương hiệu"
df["Thương hiệu"] = df["Thương hiệu"].fillna("Không rõ").str.strip().str.title()

# 3. Chuẩn hóa "Tên sản phẩm" để dễ đọc
df["Tên sản phẩm"] = (
    df["Tên sản phẩm"]
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# 4. Lọc bỏ sản phẩm giá 0 hoặc quá thấp
df = df[df["Giá (VNĐ)"] > 10000]

# 5. Làm tròn điểm đánh giá và thay giá trị NaN
df["Điểm đánh giá"] = df["Điểm đánh giá"].fillna(0).round(1)

# 6. Thay NaN trong "Số lượng đánh giá" bằng 0
df["Số lượng đánh giá"] = df["Số lượng đánh giá"].fillna(0).astype(int)

# 7. Loại trùng bằng tên + thương hiệu
df = df.drop_duplicates(subset=["Tên sản phẩm", "Thương hiệu"], keep="first")

df["Đã bán"] = df["Đã bán"].fillna(0).astype(int)

df["Danh mục"] = df["Danh mục"].str.strip().str.title()

df = df[(df["Điểm đánh giá"] <= 5) & (df["Số lượng đánh giá"] >= 0)]

print(f"📊 Sau làm sạch: {len(df)} sản phẩm hợp lệ")

df.to_csv("tiki_clean.csv", index=False, encoding="utf-8-sig")
print("📁 Đã lưu file tiki_clean.csv (đã làm sạch)")
