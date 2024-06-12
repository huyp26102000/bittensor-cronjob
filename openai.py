import openai
import os
import requests
import time
import utils
from dotenv import load_dotenv
from utils import send_tele_message

load_dotenv()
openai_api_key=os.getenv('openai_api_key').split(",")

while(True):
    formatedMessage = ""
    for apikey in openai_api_key:
        try:
            openai.api_key = apikey
            print(openai.api_key)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": "hello"}
                ],
                max_tokens=10
            )
            print(response)
        except:
            print(f"API Error")
            formatedMessage = formatedMessage + f"\n{apikey} {os.getenv('telegram_tag_user')}"
    send_tele_message(formatedMessage)
    time.sleep(300)