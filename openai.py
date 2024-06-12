import os
import requests
import time
from dotenv import load_dotenv
from utils import send_tele_message

load_dotenv()
openai_api_key=os.getenv('openai_api_key').split(",")


while(True):
    formatedMessage = ""
    for apikey in openai_api_key:
        # try:
        url = "https://api.openai.com/v1/models"
        headers = {
            "Authorization": f"Bearer {apikey}"
        }
        try:
            response = requests.get(url, headers=headers)
            print(response)
            if(response.status_code != 200):
                formatedMessage = formatedMessage + f"\n{apikey} {os.getenv('telegram_tag_user')}"
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            formatedMessage = formatedMessage + f"\n{apikey} {os.getenv('telegram_tag_user')}"
    if len(formatedMessage) > 0:
        send_tele_message(formatedMessage)
    time.sleep(300)