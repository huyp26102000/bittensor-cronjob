import math
import requests
import os
from datetime import datetime

def round_down(x, decimals=5):
    multiplier = 10 ** decimals
    return math.floor(x * multiplier) / multiplier
def send_tele_message(message, thread_id = os.getenv('telegram_status_thread_id')):
    try:
        print(f"https://api.telegram.org/bot{os.getenv('telegram_token')}/sendMessage")
        response = requests.post(f"https://api.telegram.org/bot{os.getenv('telegram_token')}/sendMessage", json={
            "chat_id": os.getenv('telegram_chat_id'),
            "text": message,
            "message_thread_id": thread_id,
            "parse_mode": "html",
            "disable_web_page_preview": True,
        }, headers={
            "Content-Type": "application/json",
            "cache-control": "no-cache",
            "Access-Control-Allow-Origin": "*",
        })
        print(response)
    except:
        print("Send tele fail")


def days_until_end_timestamp(end_timestamp):
    end_date = datetime.fromtimestamp(end_timestamp)
    current_date = datetime.now()
    remaining_days = (end_date - current_date).days
    return remaining_days