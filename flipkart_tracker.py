import requests
from bs4 import BeautifulSoup
import time

# ==== USER CONFIGURATION ====
FLIPKART_URL = "https://www.flipkart.com/fortune-soya-health-refined-soyabean-oil-pouch/p/itm02c0a242f0642?pid=EDOEUHJMAUZG6ZVT"
DESIRED_PRICE = 115
PINCODE = "827010"
CHECK_INTERVAL = 900  # seconds (15 min)

# Telegram
BOT_TOKEN = "7584266876:AAHfsdqzOyWxLjmrQBSbc7wnneIg10_mlV4"
CHAT_ID = "1442539679"


# ==== FUNCTIONS ====

def send_telegram_alert(price, stock_status):
    message = f"🛒 *Flipkart Alert!*\n\n*Product:* Fortune Soya Oil\n*Price:* ₹{price}\n*Stock:* {stock_status}\n\n[View Product]({FLIPKART_URL})"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    })

def check_flipkart():
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(FLIPKART_URL, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # PRICE
    price_tag = soup.find("div", {"class": "_30jeq3 _16Jk6d"})
    price = int(price_tag.text.replace("₹", "").replace(",", "")) if price_tag else 9999

    # STOCK
    delivery = soup.find("div", {"class": "_16FRp0"})
    stock_status = "In Stock" if delivery and PINCODE in delivery.text else "Out of Stock"

    # Alert if both conditions are met
    if price <= DESIRED_PRICE and stock_status == "In Stock":
        send_telegram_alert(price, stock_status)
        
    print(f"[DEBUG] Price: ₹{price}, Stock: {stock_status}")
