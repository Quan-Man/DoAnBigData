import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ hai file
hasaki = pd.read_csv("hasaki_clean.csv")
tiki = pd.read_csv("tiki_clean.csv")

# Thêm cột 'Nguồn' để phân biệt
hasaki['Nguồn'] = 'Hasaki'
tiki['Nguồn'] = 'Tiki'

# Gộp hai tập dữ liệu
df = pd.concat([hasaki, tiki], ignore_index=True)

# Làm sạch tên cột (phòng trường hợp có khoảng trắng hoặc ký tự lạ)
df.columns = df.columns.str.strip()


# ---BĐ Mối quan hệ giữa số lượng đánh giá và giá ---
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x='Số lượng đánh giá', y='Giá (VNĐ)', hue='Nguồn', alpha=0.7)
plt.title("Quan hệ giữa số lượng đánh giá và giá sản phẩm")
plt.tight_layout()
plt.show()
