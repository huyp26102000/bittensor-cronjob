import bittensor as bt
import os
from dotenv import load_dotenv
import requests
import time
import math
import numpy as np
from utils import round_down, send_tele_message

load_dotenv()

metagraph = bt.metagraph(int(os.getenv('netuid')), network=os.getenv('network'))
coldkeys = os.getenv('track_coldkey').split(",")
netColdkeys = metagraph.coldkeys
nodeUrl = metagraph.axons

incentive_data = metagraph.incentive
array_incentive_data = incentive_data.numpy()
sorted_incentive_data = np.sort(array_incentive_data)
print(sorted_incentive_data)
search_index = {}
nodeData = {}
formatedMessage = ""
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
for coldkey in coldkeys:
    fmColdkey = ""
    for node in search_index[coldkey]:
        print(node["incentive"], str(node["incentive"]))
        print(np.where(sorted_incentive_data == int(node["incentive"])))
        fmColdkey  = fmColdkey + f"""
<b>{node["uid"]}</b>:{round_down(node["incentive"], 5)} <b>{"" if node["running"] == True else f"Not Running {os.getenv('telegram_tag_user')}" }</b>      <code>{node["host"]}</code>"""
    formatedMessage = formatedMessage + f"\n<b>{coldkey}</b>\n" + f"{fmColdkey}"
send_tele_message(formatedMessage)