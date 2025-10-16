from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

# --- Cấu hình Chrome ---
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

urls = {
    "Chăm sóc da mặt": "https://www.lazada.vn/catalog/?spm=a2o4n.searchlist.cate_4.1.e7311feetBVQ1h&q=Ch%C4%83m%20S%C3%B3c%20Da&from=hp_categories&src=all_channel&page={page}",
    "Trang điểm": "https://www.lazada.vn/catalog/?spm=a2o4n.searchlist.cate_4.2.57414855ko0VIl&q=Trang%20%C4%90i%E1%BB%83m&from=hp_categories&src=all_channel&page={page}",
    "Dưỡng thể": "https://www.lazada.vn/catalog/?spm=a2o4n.searchlist.cate_4.4.6f674855PyjmO9&q=Ch%C4%83m%20S%C3%B3c%20C%C6%A1%20Th%E1%BB%83&from=hp_categories&src=all_channel&page={page}",
    "Chăm sóc móng": "https://www.lazada.vn/catalog/?q=Ch%C4%83m%20S%C3%B3c%20M%C3%B3ng&src=all_channel&page={page}",
    "Sữa rửa mặt": "https://www.lazada.vn/catalog/?spm=a2o4n.searchlist.cate_4_1.3.524f7cf86zRCok&q=S%E1%BB%AFa%20R%E1%BB%ADa%20M%E1%BA%B7t&from=hp_categories&src=all_channel&page={page}"
}

all_data = []

for cat_name, base_url in urls.items():
    print(f"\n📦 Đang lấy danh mục: {cat_name}")
    page = 1
    while True:
        print(f"➡️ Trang {page} ...")
        driver.get(base_url.format(page=page))
        time.sleep(5)  # chờ load

        # --- Scroll xuống để load hết sản phẩm ---
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            
        products = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-locator='product-item']")
        if not products:
            print("⚠️ Không còn sản phẩm, kết thúc.")
            break

        for p in products:
            try:
                title = p.find_element(By.CSS_SELECTOR, "div.RfADt a[title]").get_attribute("title")
                
                price_text = p.find_element(By.CSS_SELECTOR, "div.aBrP0 span.ooOxS").text.replace("₫","").replace(".","").strip()
                try:
                    price = int(price_text)
                except:
                    price = 0
                    
                try:
                    sold_info = p.find_element(By.CSS_SELECTOR, "div._6uN7R span._1cEkb span").text
                except:
                    sold_info = ""

                try:
                    rating_text = p.find_element(By.CSS_SELECTOR, "div._6uN7R span.qzqFw").text.replace("(", "").replace(")", "").replace("+","")
                    rating_count = int(rating_text)
                except:
                    rating_count = 0

                all_data.append({
                    "Tên sản phẩm": title,
                    "Giá (VNĐ)": price,
                    "Đã bán": sold_info,
                    "Số đánh giá": rating_count,
                    "Danh mục": cat_name
                })
            except:
                continue

        page += 1
        # Bạn có thể giới hạn số page nếu muốn tránh quá lâu
        if page > 10: 
            break

driver.quit()

# --- Xuất CSV ---
df = pd.DataFrame(all_data)
df.drop_duplicates(subset=["Tên sản phẩm"], inplace=True)
df.to_csv("lazada_mypham_full.csv", index=False, encoding="utf-8-sig")
print(f"📁 Đã lưu {len(df)} sản phẩm vào lazada_mypham_full.csv")
