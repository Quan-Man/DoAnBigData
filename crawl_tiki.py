# crawl_tiki.py
import requests
import pandas as pd
import time

all_data = []
categories = {
    "Chăm sóc da mặt": 1582,
    "Trang điểm": 1584,
    "Dưỡng thể": 1610,
    "Chăm sóc móng": 1590,
    "Sữa rửa mặt": 1583
}

for cat_name, cat_id in categories.items():
    print(f"📦 Đang cào danh mục: {cat_name}")
    for page in range(1, 11):  # mỗi danh mục 10 trang
        url = f"https://tiki.vn/api/personalish/v1/blocks/listings?limit=50&page={page}&category={cat_id}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if res.status_code != 200:
            print(f"⚠️ Lỗi trang {page} danh mục {cat_name}")
            continue

        try:
            items = res.json().get("data", [])
        except ValueError:
            print(f"⚠️ Lỗi JSON trang {page} danh mục {cat_name}")
            continue
        items = res.json().get("data", [])
        for item in items:
            all_data.append({
                "Tên sản phẩm": item.get("name"),
                "Giá (VNĐ)": int(item.get("price") or 0),
                "Thương hiệu": item.get("brand_name"),
                "Đã bán": int(item.get("quantity_sold", {}).get("value") if isinstance(item.get("quantity_sold"), dict) else (item.get("quantity_sold") or 0)),
                "Điểm đánh giá": item.get("rating_average"),
                "Số lượng đánh giá": item.get("review_count"),
                "Danh mục": cat_name
            })
        print(f"✅ {cat_name} - Trang {page} xong, tổng {len(all_data)}")
        time.sleep(1)  # tránh bị chặn

df = pd.DataFrame(all_data)

df.to_csv("tiki_raw.csv", index=False, encoding="utf-8-sig")
print("📁 Đã lưu file tiki_raw.csv (dữ liệu thô)")
