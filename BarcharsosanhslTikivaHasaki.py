import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
tiki = pd.read_csv('tiki_clean.csv')
hasaki = pd.read_csv('hasaki_clean.csv')

# Thêm cột 'Nguồn' để phân biệt sàn
tiki['Nguồn'] = 'Tiki'
hasaki['Nguồn'] = 'Hasaki'

# Gộp 2 bảng lại thành 1
df = pd.concat([tiki, hasaki])

# Đếm số lượng sản phẩm theo thương hiệu và nguồn
brand_counts = df.groupby(['Nguồn', 'Thương hiệu']).size().reset_index(name='Số lượng')

# Pivot bảng cho dễ vẽ biểu đồ
brand_pivot = brand_counts.pivot(index='Thương hiệu', columns='Nguồn', values='Số lượng').fillna(0)

# Lọc top 10 thương hiệu có tổng sản phẩm nhiều nhất (trên cả 2 sàn)
top_brands = brand_pivot.sum(axis=1).sort_values(ascending=False).head(10).index
brand_pivot = brand_pivot.loc[top_brands]

# Vẽ biểu đồ Bar Chart
brand_pivot.plot(kind='bar', figsize=(12,6))
plt.title('So sánh số lượng sản phẩm theo thương hiệu giữa Tiki và Hasaki', fontsize=14)
plt.xlabel('Thương hiệu', fontsize=12)
plt.ylabel('Số lượng sản phẩm', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.legend(title='Nguồn dữ liệu')
plt.tight_layout()
plt.show()
