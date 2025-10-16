from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# --- Cấu hình Chrome ---
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

urls = {
    "Chăm sóc da mặt": "https://hasaki.vn/danh-muc/cham-soc-da-mat-c4.html?page={page}",
    "Trang điểm": "https://hasaki.vn/danh-muc/trang-diem-c23.html?page={page}",
    "Dưỡng thể": "https://hasaki.vn/danh-muc/duong-the-c1897.html?page={page}",
    "Chăm sóc móng": "https://hasaki.vn/danh-muc/cham-soc-mong-c61.html?page={page}",
    "Sữa rửa mặt": "https://hasaki.vn/danh-muc/sua-rua-mat-c19.html?page={page}"
}

all_data = []

for cat_name, base_url in urls.items():
    print(f"\n📦 Đang lấy danh mục: {cat_name}")
    page = 1
    while True:
        print(f"➡️ Trang {page} ...")
        driver.get(base_url.format(page=page))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # chờ load
            
        # Chờ sản phẩm load xong
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[aria-label^='View']"))
        )
        products = driver.find_elements(By.CSS_SELECTOR, "a[aria-label^='View']")
        if not products:
            print("⚠️ Không còn sản phẩm, kết thúc.")
            break

        for p in products:
            try:
                # Tên sản phẩm
                title = p.find_element(By.CSS_SELECTOR, "h2.line-clamp-2").text.strip()
                
                # Giá
                try:
                    price_text = p.find_element(By.CSS_SELECTOR, "span.text-orange.font-bold").text
                    price = int(price_text.replace("₫","").replace(".","").strip())
                except:
                    price = 0

                # Thương hiệu
                try:
                    brand = p.find_element(By.CSS_SELECTOR, "strong.text-primary").text.strip()
                except:
                    brand = ""

                # Đã bán
                try:
                    sold_count = p.find_element(
                        By.XPATH,
                        ".//span[contains(text(),'tháng')]"
                    ).text.strip()
                except:
                    sold_count = "0"

                # Điểm đánh giá
                try:
                    rating_average = p.find_element(
                        By.CSS_SELECTOR, "div.bg-orange div.font-semibold"
                    ).text.strip()
                except:
                    rating_average = "0"

                # Số lượng đánh giá
                try:
                    review_count = p.find_element(
                        By.CSS_SELECTOR, "div.bg-orange + span"
                    ).text.strip().replace("(","").replace(")","")
                except:
                    review_count = "0"

                all_data.append({
                    "Tên sản phẩm": title,
                    "Giá (VNĐ)": price,
                    "Thương hiệu": brand,
                    "Đã bán": sold_count,
                    "Điểm đánh giá": rating_average,
                    "Số lượng đánh giá": review_count,
                    "Danh Mục": cat_name
                })
            except:
                continue

        page += 1
        if page > 11: 
            break
        
driver.quit()

# --- Xuất CSV ---
df = pd.DataFrame(all_data)
df.drop_duplicates(subset=["Tên sản phẩm"], inplace=True)
df.to_csv("hasaki_mypham.csv", index=False, encoding="utf-8-sig")
print(f"📁 Đã lưu {len(df)} sản phẩm vào hasaki_mypham.csv")
