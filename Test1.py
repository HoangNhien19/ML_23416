from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- Cấu hình Chrome headless (không hiện cửa sổ) ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # chạy ngầm
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1920,1080")

# Khởi tạo driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# URL bài báo
url = "https://www.usatoday.com/story/money/2025/10/07/starbucks-hello-kitty-2025-collab-holiday-merch/86561520007/"

# mở trang
driver.get(url)

# chờ vài giây cho JS load (có thể tăng nếu mạng chậm)
time.sleep(5)

# Lấy title bài báo
title = driver.find_element(By.TAG_NAME, "h1").text
print("Title:", title)

# Lấy nội dung bài báo
# USAToday thường để các đoạn text trong div có class chứa 'gnt_ar_b'
try:
    article_body = driver.find_element(By.CSS_SELECTOR, "div.gnt_ar_b")
    paragraphs = article_body.find_elements(By.TAG_NAME, "p")
    article_text = "\n".join([p.text for p in paragraphs])
    print("\nContent:\n", article_text)
except:
    print("Không tìm thấy nội dung bài báo")

# đóng driver
driver.quit()