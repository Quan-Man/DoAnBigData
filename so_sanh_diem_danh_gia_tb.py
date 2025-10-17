import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Biểu đồ: So sánh điểm đánh giá trung bình theo thương hiệu

# Đọc dữ liệu từ file CSV

tiki_df = pd.read_csv("tiki_clean.csv", thousands=',', encoding='utf-8')
hasaki_df = pd.read_csv("hasaki_clean.csv", thousands=',', encoding='utf-8')

# Chuẩn hóa tên cột của Hasaki để khớp với Tiki
hasaki_df = hasaki_df.rename(columns={"Danh Mục": "Danh mục"})

# Thêm cột nguồn dữ liệu
tiki_df["Nền tảng"] = "Tiki"
hasaki_df["Nền tảng"] = "Hasaki"

# Gộp hai bảng
df = pd.concat([tiki_df, hasaki_df], ignore_index=True)

# Chuẩn hóa giá trị cột "Danh mục" về chữ thường để groupby chính xác
df["Danh mục"] = df["Danh mục"].str.lower()

# Đảm bảo cột số là số thực
df["Điểm đánh giá"] = pd.to_numeric(df["Điểm đánh giá"], errors='coerce')
df["Số lượng đánh giá"] = pd.to_numeric(df["Số lượng đánh giá"], errors='coerce')

# Lấy top 8 thương hiệu có nhiều đánh giá nhất
top_brands = df.groupby("Thương hiệu")["Số lượng đánh giá"].sum().nlargest(8).index
df_top_brand = df[df["Thương hiệu"].isin(top_brands)]

# Tính điểm đánh giá trung bình theo thương hiệu và nền tảng
avg_rating = df_top_brand.groupby(["Thương hiệu", "Nền tảng"])["Điểm đánh giá"].mean().reset_index()

# Kiểm tra nếu không có thương hiệu nào
if avg_rating.empty:
    print("Không có dữ liệu để vẽ biểu đồ. Vui lòng kiểm tra dữ liệu đầu vào.")
else:
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=avg_rating,
        x="Thương hiệu",
        y="Điểm đánh giá",
        hue="Nền tảng",
        marker="o",
        linewidth=2,
        palette=["#4CAF50", "#FF5722"],  # Đồng bộ màu với barplot
    )

    plt.title("So sánh điểm đánh giá trung bình theo 8 thương hiệu phổ biến giữa Tiki và Hasaki", fontsize=14, pad=20)
    plt.xlabel("Thương hiệu", fontsize=12)
    plt.ylabel("Điểm đánh giá trung bình", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend(title="Nền tảng", fontsize=10)
    plt.tight_layout()
    plt.show()