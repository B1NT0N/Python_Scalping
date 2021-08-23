import json
import requests
from time import sleep
from threading import Thread,Lock
import WS
token = "1968465819:AAHyJfjtfhcTOnwGBWj3j2v6kybcixM1JbA"
global url
config={'url':f"https://api.telegram.org/bot{token}",'lock':Lock()}

msg = ''
old_msg=""
def del_updates(data):
    config['lock'].acquire()
    requests.post(f"{config['url']}/getUpdates",{'offset':data["update_id"]+1})
    config['lock'].release()

def send_message_only(data, msg):
    config['lock'].acquire()

    send_data = {"chat_id":data["message"]["chat"]["id"], 
                "text":str(msg)
    }

    #print(send_data)
    requests.post(f"{config['url']}/sendMessage",send_data)
    config['lock'].release()

def send_inkeyboard_message(data,msg):
    config['lock'].acquire()

    in_keyboard={
        "inline_keyboard":[
                            [
                                {"text": " 🎬 Movies",
                                "callback_data":"m",
                                "url":"https://github.com/B1NT0N"
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

    send_data = {"chat_id":data["message"]["chat"]["id"], 
                "text":str(msg),
                "reply_markup":in_keyboard
    }

    #print(send_data)
    requests.post(f"{config['url']}/sendMessage",send_data)
    config['lock'].release()
    
def send_keyboard_message(data,msg):
    config['lock'].acquire()


    keyboard = {
                "keyboard":[
                            [
                                {"text": " 🎬 Movies"}
                            ],
                            [
                                {"text": " 📺 Series"}
                            ]
                        ],
                'resize_keyboard':True,
                "one_time_keyboard":True
                }

    keyboard = json.dumps(keyboard)

    send_data = {"chat_id":data["message"]["chat"]["id"], 
                "text":str(msg),
                "reply_markup":keyboard
    }

    #print(send_data)
    requests.post(f"{config['url']}/sendMessage",send_data)
    config['lock'].release()

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
            Thread(target=send_keyboard_message, args=(data, msg)).start()
            new_msg = data["message"]["text"]
            if new_msg == "🎬 Movies":
                send_message_only(data, "Movie Name:")
            elif new_msg != old_msg and old_msg == "🎬 Movies" and new_msg !="📺 Series":
                   my_url = f"https://www.imdb.com/find?q={new_msg}&s=tt&ttype=ft&ref_=fn_ft"
                   print(my_url)
            if new_msg == "📺 Series":
                send_message_only(data, "Series Name:")
            elif new_msg != old_msg and old_msg == "📺 Series" and new_msg !="🎬 Movies":
                   my_url = f"https://www.imdb.com/find?q={new_msg}&s=tt&ttype=tv&ref_=fn_tv"
                   print(my_url)
            old_msg = new_msg 
            #msg=f'{data["message"]["text"]} from: BOT'
            #print(f'{data["message"]["text"]} from: {data["message"]["chat"]["username"]}')
            
        sleep(1)

