import bittensor as bt
import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()


def sendTeleMessage(message):
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

acceptedResp = """{"message":"Synapse name '' not found. Available synapses ['Synapse', 'ImageGenerating', 'TextGenerating']"}"""
while (True):
    metagraph = bt.metagraph(int(os.getenv('netuid')), network=os.getenv('network'))
    coldkeys = os.getenv('track_coldkey').split(",")
    netColdkeys = metagraph.coldkeys
    nodeUrl = metagraph.axons
    incentiveData = metagraph.I
    searchIndex = {}
    nodeData = {}
    for coldkey in coldkeys:
        indices = []
        for i, value in enumerate(netColdkeys):
            if value == coldkey:
                port = nodeUrl[i].port
                ip = nodeUrl[i].ip
                print(port, ip)
                try:
                    response = requests.get(f"http://{ip}:{port}", timeout=3)
                    if (response.text.__contains__(acceptedResp)):
                        indices.append({
                            "uid": i,
                            "running": True,
                            "incentive": incentiveData[i],
                            "host": f"{ip}:{port}"
                        })
                    else:
                        indices.append({
                            "uid": i,
                            "running": False,
                            "incentive": incentiveData[i],
                            "host": f"{ip}:{port}"
                        })
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while requesting the URL: {e}")
                    indices.append({
                        "uid": i,
                        "running": False,
                        "incentive": incentiveData[i],
                        "host": f"{ip}:{port}"
                    })
        searchIndex[coldkey] = indices
    formatedMessage = ""
    for coldkey in coldkeys:
        fmColdkey = ""
        for node in searchIndex[coldkey]:
            fmColdkey  = fmColdkey + f"""
<b>{node["uid"]}</b>: <b>{"OK" if node["running"] == True else "Not Running @hiro_trk @tian_ng" }</b> <code>{node["host"]}</code>"""
        formatedMessage = formatedMessage + f"\n{coldkey}" + f"{fmColdkey}"
    sendTeleMessage(formatedMessage)
    time.sleep(300)