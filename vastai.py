import requests
import os
from dotenv import load_dotenv
from utils import round_down, send_tele_message, days_until_end_timestamp

load_dotenv()
vastai_apikeys = os.getenv('vastai_apikey').split(",")
thread_id = os.getenv('vastai_telegram_thread_id')
tag_user_str = str(os.getenv('vastai_tag_user_str'))
formatedMessage = ""
def fetch_vastai_credit (apikey):
    url = "https://cloud.vast.ai/api/v0/users/current/"
    headers = {
        "Authorization": f"Bearer {apikey}"  # Replace with your Vastai API key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        username = data.get('username', 'Unknown User')
        credit = data.get('credit', 0)
        return f"{username} {round_down(credit, 2)}$ {'' if int(credit) >= 20 else 'balance < 20 ' + tag_user_str}"

    else:
        print(f"Error: {response.status_code}")
def fetch_instants (apikey):
    instant_formated_text = ""
    url = "https://cloud.vast.ai/api/v0/instances/"
    headers = {
        "Authorization": f"Bearer {apikey}"  # Replace with your Vastai API key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        instants = data.get('instances')
        for instant in instants:
            end_date = instant.get('end_date')
            status = instant.get('cur_state') == "running"
            disk_space = instant.get('disk_space')
            disk_usage = instant.get('disk_usage')
            geolocation = instant.get('geolocation')
            remaining_days = days_until_end_timestamp(end_date)
            instant_str = (
                f"\n🔫<b>{geolocation}</b> "
                f"<b>{'OK' if status else f'Not Running' + os.getenv('telegram_tag_user')}</b>\n"
                f"<b>{remaining_days}</b> days  Disk: {disk_space}/{disk_usage}Gb"
            )
            instant_formated_text = instant_formated_text + instant_str
        return instant_formated_text
    else:
        print(f"Error: {response.status_code}")
for vastai_apikey in vastai_apikeys:
    balance_str = fetch_vastai_credit(vastai_apikey)
    instants_str = fetch_instants(vastai_apikey)
    formatedMessage = formatedMessage + f"{balance_str}\n" + instants_str + "\n\n"

send_tele_message(formatedMessage, thread_id)
