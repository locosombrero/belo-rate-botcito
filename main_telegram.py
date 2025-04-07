import os
import requests
import json

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def get_best_rate(crypto):
    url = f"https://criptoya.com/api/{crypto}/ars/1"
    res = requests.get(url)
    data = res.json()

    best_exchange = None
    best_price = float('-inf')  # Queremos el precio más alto

    for exchange, info in data.items():
        price = info.get("totalBid")
        if price and price > best_price:
            best_price = price
            best_exchange = exchange

    belo_price = data.get("belo", {}).get("totalBid")
    is_belo_best = best_exchange == "belo"
    return is_belo_best, belo_price, best_price, best_exchange

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

def main():
    msg = ""
    for crypto in ["usdc", "usdt"]:
        is_best, belo_price, best_price, best_exchange = get_best_rate(crypto)
        if is_best:
            msg += f"*Belo tiene la mejor cotización para vender {crypto.upper()} hoy*: ${belo_price:.2f}\n"
        else:
            msg += f"{crypto.upper()} en Belo: ${belo_price:.2f} (la mejor es {best_exchange} a ${best_price:.2f})\n"

    send_telegram_message(msg)

if __name__ == "__main__":
    main()