import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
tiki = pd.read_csv('tiki_clean.csv')
hasaki = pd.read_csv('hasaki_clean.csv')

# Đếm số lượng sản phẩm theo thương hiệu
tiki_brand = tiki['Thương hiệu'].value_counts().head(10)      # Top 10 thương hiệu trên Tiki
hasaki_brand = hasaki['Thương hiệu'].value_counts().head(10)  # Top 10 thương hiệu trên Hasaki

# Tạo 2 biểu đồ tròn song song
fig, axes = plt.subplots(1, 2, figsize=(14,7))

# Biểu đồ cho Tiki
axes[0].pie(
    tiki_brand,
    labels=tiki_brand.index,
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'white'}
)
axes[0].set_title('Tỷ lệ thương hiệu trên Tiki (Top 10)', fontsize=14)

# Biểu đồ cho Hasaki
axes[1].pie(
    hasaki_brand,
    labels=hasaki_brand.index,
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops={'edgecolor': 'white'}
)
axes[1].set_title('Tỷ lệ thương hiệu trên Hasaki (Top 10)', fontsize=14)

plt.tight_layout()
plt.show()
