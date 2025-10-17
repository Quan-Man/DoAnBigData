import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Biểu đồ: So sánh trung bình số lượng đánh giá theo danh mục

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
df["Số lượng đánh giá"] = pd.to_numeric(df["Số lượng đánh giá"], errors='coerce')

# Tính trung bình số lượng đánh giá theo danh mục và nền tảng
avg_reviews = df.groupby(["Danh mục", "Nền tảng"])["Số lượng đánh giá"].mean().unstack(fill_value=0)

# Chuyển về định dạng dài
avg_reviews = avg_reviews.reset_index().melt(id_vars="Danh mục", var_name="Nền tảng", value_name="Số lượng đánh giá")

# Lấy top 8 danh mục phổ biến nhất dựa trên tổng số lượng đánh giá
top_cats = (
    df.groupby("Danh mục")["Số lượng đánh giá"]
    .sum()  # Dùng sum để phản ánh mức độ phổ biến
    .nlargest(8)
    .index
)

# Lọc dữ liệu chỉ lấy top danh mục
avg_reviews = avg_reviews[avg_reviews["Danh mục"].isin(top_cats)]

# Kiểm tra nếu không có danh mục nào
if avg_reviews.empty:
    print("Không có dữ liệu để vẽ biểu đồ. Vui lòng kiểm tra dữ liệu đầu vào.")
else:
    # Vẽ biểu đồ
    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=avg_reviews,
        x="Danh mục",
        y="Số lượng đánh giá",
        hue="Nền tảng",
        palette=["#4CAF50", "#FF5722"],  # Màu xanh lá và cam
    )

    plt.title("So sánh trung bình số lượng đánh giá theo danh mục giữa Tiki và Hasaki", fontsize=14, pad=20)
    plt.xlabel("Danh mục sản phẩm", fontsize=12)
    plt.ylabel("Số lượng đánh giá trung bình", fontsize=12)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.legend(title="Nền tảng", fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()