import pandas as pd

# --- Đọc CSV gốc ---
df = pd.read_csv("lazada_mypham_full.csv", encoding="utf-8-sig")

# --- Xóa trùng sản phẩm theo Tên ---
df.drop_duplicates(subset=["Tên sản phẩm"], inplace=True)

# --- Làm sạch cột Giá (VNĐ) ---
df["Giá (VNĐ)"] = pd.to_numeric(df["Giá (VNĐ)"], errors="coerce").fillna(0).astype(int)

# --- Làm sạch cột Đã bán ---
def parse_sold(sold_text):
    if pd.isna(sold_text):
        return 0
    sold_text = sold_text.replace("Đã bán", "").strip()
    if "K" in sold_text:
        try:
            return int(float(sold_text.replace("K","")) * 1000)
        except:
            return 0
    try:
        return int(sold_text.replace(".",""))
    except:
        return 0

df["Đã bán"] = df["Đã bán"].apply(parse_sold)

# --- Làm sạch cột Số đánh giá ---
df["Số đánh giá"] = pd.to_numeric(df["Số đánh giá"], errors="coerce").fillna(0).astype(int)

# --- Điền giá trị thiếu ở cột Danh mục ---
if "Danh mục" in df.columns:
    df["Danh mục"] = df["Danh mục"].fillna("")

# --- Xóa các dòng có Giá = 0, Số đánh giá = 0 hoặc Đã bán = 0 ---
df = df[(df["Giá (VNĐ)"] > 0) & (df["Số đánh giá"] > 0) & (df["Đã bán"] > 0)]

df = df[(df["Giá (VNĐ)"] >= 10000) & (df["Giá (VNĐ)"] <= 100000000)]

# --- Lưu CSV sạch ---
df.to_csv("lazada_mypham_clean.csv", index=False, encoding="utf-8-sig")
print(f"✅ Đã làm sạch dữ liệu và lưu {len(df)} sản phẩm vào lazada_mypham_clean.csv")
