import bittensor as bt
import os
from dotenv import load_dotenv
import requests
import time
import math
import numpy as np
import openai

load_dotenv()

def round_down(x, decimals=5):
    multiplier = 10 ** decimals
    return math.floor(x * multiplier) / multiplier
def send_tele_message(message):
    try:
        print(f"https://api.telegram.org/bot{os.getenv('telegram_token')}/sendMessage")
        response = requests.post(f"https://api.telegram.org/bot{os.getenv('telegram_token')}/sendMessage", json={
            "chat_id": os.getenv('telegram_chat_id'),
            "text": message,
            "message_thread_id": os.getenv('telegram_status_thread_id'),
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

# while (True):
metagraph = bt.metagraph(int(os.getenv('netuid')), network=os.getenv('network'))
coldkeys = os.getenv('track_coldkey').split(",")
openai_api_key=os.getenv('openai_api_key').split(",")
netColdkeys = metagraph.coldkeys
nodeUrl = metagraph.axons

incentive_data = metagraph.incentive
array_incentive_data = incentive_data.numpy()
sorted_incentive_data = np.sort(array_incentive_data)
print(sorted_incentive_data)
search_index = {}
nodeData = {}
while(True):
    for coldkey in coldkeys:
        indices = []
        for i, value in enumerate(netColdkeys):
            if value == coldkey:
                port = nodeUrl[i].port
                ip = nodeUrl[i].ip
                print(port, ip)
                try:
                    response = requests.get(f"http://{ip}:{port}", timeout=8)
                    if (len(response.text) > 5):
                        indices.append({
                            "uid": i,
                            "running": True,
                            "incentive": incentive_data[i],
                            "host": f"{ip}:{port}"
                        })
                    else:
                        indices.append({
                            "uid": i,
                            "running": False,
                            "incentive": incentive_data[i],
                            "host": f"{ip}:{port}"
                        })
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while requesting the URL: {e}")
                    indices.append({
                        "uid": i,
                        "running": False,
                        "incentive": incentive_data[i],
                        "host": f"{ip}:{port}"
                    })
        search_index[coldkey] = indices
    formatedMessage = ""
    for coldkey in coldkeys:
        fmColdkey = ""
        for node in search_index[coldkey]:
            print(node["incentive"], str(node["incentive"]))
            print(np.where(sorted_incentive_data == int(node["incentive"])))
            fmColdkey  = fmColdkey + f"""
<b>{node["uid"]}</b>:{round_down(node["incentive"], 5)} <b>{"" if node["running"] == True else f"Not Running {os.getenv('telegram_tag_user')}" }</b>      <a href="http://${node["host"]}>{node["host"]}</a>"""
        formatedMessage = formatedMessage + f"\n<b>{coldkey}</b>\n" + f"{fmColdkey}"
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