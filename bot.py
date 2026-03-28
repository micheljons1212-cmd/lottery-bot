import requests
from bs4 import BeautifulSoup
import time
import re

BOT_TOKEN = "  8609998510:AAEnUrFZK4ODf8LujNzlpaiYrdRxK7ISMUA "
CHAT_ID = " 7851223849 "

sent_links = set()

def send(msg):
    try:
             f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Send error:", e)

def get_price(text):
    numbers = re.findall(r"\d+", text.replace(",", ""))
    if numbers:
        return int(numbers[0])
    return 999999

def is_good(title):
    bad_words = ["parts", "repair", "broken", "replica", "fake"]
    return not any(word in title.lower() for word in bad_words)

def generate_listing(title, price):
    sell_price = int(price * 1.6)

    return f"""
🔥 FOR SALE 🔥
{title}

✅ Tested & working
💰 Price: ${sell_price}
📍 Pickup today
⚡ First come first serve

Message me now!
"""

def scan_ebay():
    url = "https://www.ebay.com/sch/i.html?_nkw=ps5&_sop=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    items = soup.select(".s-item")

    for item in items:
        title_tag = item.select_one(".s-item__title")
        price_tag = item.select_one(".s-item__price")
        link_tag = item.select_one("a.s-item__link")

        if not title_tag or not price_tag or not link_tag:
            continue

        title = title_tag.text
        price = get_price(price_tag.text)
        link = link_tag.get("href")

        if link in sent_links:
            continue

        if price < 250 and is_good(title):
            sent_links.add(link)

            listing = generate_listing(title, price)

            msg = f"""
🎯 DEAL FOUND

{title}
💰 Buy: ${price}

{listing}

🔗 {link}
"""
            send(msg)

while True:
    send("🔎 BOT V2 scanning...")
    scan_ebay()
    time.sleep(120)