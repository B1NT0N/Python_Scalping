import json
import requests
from time import sleep
from threading import Thread,Lock


token = "1854693768:AAEMp18eBDS0zI8FzI1eqsArRYItZvLULnw"
global url
config={'url':f"https://api.telegram.org/bot{token}",'lock':Lock()}

msg = 'Im listening and anwsering'

def del_updates(data):
    config['lock'].acquire()
    requests.post(f"{config['url']}/getUpdates",{'offset':data["update_id"]+1})
    config['lock'].release()

def send_message(data, msg):
    config['lock'].acquire()
    requests.post(f"{config['url']}/sendMessage",{'chat_id':data["message"]["chat"]["id"], 'text':str(msg)})
    config['lock'].release()

while True:

    while True:
        try:
            json_load = json.loads(requests.get(f"{config['url']}/getUpdates").text)
            break
        except Exception as exception:
            json_load = {"result": []}
            if 'Failed to establish a new connection' in str(exception):
                print("Connection failed")
            else:
                print(f"Unknow Error: {exception}")

    if len(json_load["result"]) > 0:
        for data in json_load["result"]:
            Thread(target=del_updates, args=(data,)).start()
            msg=f'{data["message"]["text"]} from:BOT'
            print(f'{data["message"]["text"]} from:{data["message"]["chat"]["username"]}')
            Thread(target=send_message, args=(data, msg)).start()
        sleep(1)

