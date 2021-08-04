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


    keyboard = {
                "keyboard":[
                            [
                                {"text": " 🎬 Movies"}
                            ],
                            [
                                {"text": " 📺 Series"}
                            ],
                            [
                                {"text": " 🔙 Back"}
                            ]
                        ],
                'resize_keyboard':True,
                "one_time_keyboard":True
                }
    in_keyboard={
        "inline_keyboard":[
                            [
                                {"text": " 🎬 Movies",
                                "callback_data":"m",
                                "url":"https://core.telegram.org/bots/api#inlinekeyboardmarkup"
                                }
                            ],
                            [
                                {"text": " 📺 Series",
                                "callback_data":"s"
                                }
                            ]
                        ],
    }

    in_keyboard = json.dumps(in_keyboard)
    keyboard = json.dumps(keyboard)

    send_data = {"chat_id":data["message"]["chat"]["id"], 
                "text":str(msg),
                "reply_markup":in_keyboard
     
    }

    #print(send_data)
    requests.post(f"{config['url']}/sendMessage",send_data)
    config['lock'].release()
    
# "reply_markup":{'keyboard':[[{"text":"1"}],[{"text":"2"}]], 'resize_keyboard':True, "one_time_keyboard":False}
while True:

    json_load=''
    while 'result' not in json_load:
        try:
            json_load = json.loads(requests.get(f"{config['url']}/getUpdates").text)
        except Exception as exception:
            json_load = ''
            if 'Failed to establish a new connection' in str(exception):
                print("Connection failed")
            else:
                print(f"Unknow Error: {exception}")

    if len(json_load["result"]) > 0:
        for data in json_load["result"]:
            Thread(target=del_updates, args=(data,)).start()
            msg=f'{data["message"]["text"]} from:BOT'
            print(f'{data["message"]["text"]} from:{data["message"]["chat"]["username"]}')
            #Thread(target=send_message, args=(data, msg)).start()
            send_message(data, msg)
        sleep(1)

