import json
from bs4.element import ProcessingInstruction
import requests
from time import sleep
from threading import Thread,Lock
import WS
from  WS import Entertainment

token = ""
global url
config={'url':f"https://api.telegram.org/bot{token}",'lock':Lock()}

msg = ''
old_msg=""
new_msg = ''
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

def send_inkeyboard_message(data,msg,link):
    config['lock'].acquire()

    in_keyboard={
        "inline_keyboard":[
                            [
                                {"text": f"Watch {msg} Now",
                                "url":link
                                }
                            ]
                        ],
    }

    in_keyboard = json.dumps(in_keyboard)

    send_data = {"chat_id":data["message"]["chat"]["id"], 
                "text":"🔰 Download Link Bellow 🔰",
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
                "one_time_keyboard":False
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
            del_updates(data,)
            try:
                new_msg = data["message"]["text"]
            except Exception as exception:
                send_keyboard_message(data, "Unsuported Data Type")
            if new_msg == "/start":
                send_keyboard_message(data, "Welcome")
                send_message_only(data,"This Bot Allow You to Watch Movies and Series for FREE with NO ADS")
                send_message_only(data,"Please Select Movies Or Series")
            if new_msg == "🎬 Movies":
                send_message_only(data, "Movie Name:")
            elif new_msg != old_msg and old_msg == "🎬 Movies" and new_msg !="📺 Series":
                new_msg = new_msg.replace(" ","%20").lower()
                my_url = f"https://www.imdb.com/find?q={new_msg}&s=tt&ttype=ft&ref_=fn_ft"
                WS.web_search(my_url,"m")
                if len(WS.f_result)>=3:
                    for x in range(3):
                        Thread(target=send_message_only, args=(data, WS.f_result[x].link)).start()
                        Thread(target=send_inkeyboard_message, args=(data, WS.f_result[x].name, WS.f_result[x].watch_link)).start()
                elif len(WS.f_result)==None:
                    send_message_only(data,"Nothing Found")
                    send_message_only(data,"Try Again with a Better Keyword")
                else:
                    for x in range(len(WS.f_result)):
                        Thread(target=send_message_only, args=(data, WS.f_result[x].watch_link)).start()
                        Thread(target=send_inkeyboard_message, args=(data, WS.f_result[x].name, WS.f_result[x].watch_link)).start()
                
            if new_msg == "📺 Series":
                send_message_only(data, "Series Name:")
            elif new_msg != old_msg and old_msg == "📺 Series" and new_msg !="🎬 Movies":
                new_msg = new_msg.replace(" ","%20").lower()
                my_url = f"https://www.imdb.com/find?q={new_msg}&s=tt&ttype=tv&ref_=fn_tv"
                WS.web_search(my_url,"m")
                if len(WS.f_result)>=3:
                    for x in range(3):
                        Thread(target=send_message_only, args=(data, WS.f_result[x].link)).start()
                        Thread(target=send_inkeyboard_message, args=(data, WS.f_result[x].name, WS.f_result[x].watch_link)).start()
                elif len(WS.f_result)==None:
                    send_message_only(data,"Nothing Found")
                    send_message_only(data,"Try Again with a Better Keyword")
                else:
                    for x in range(len(WS.f_result)):
                        Thread(target=send_message_only, args=(data, WS.f_result[x].watch_link)).start()
                        Thread(target=send_inkeyboard_message, args=(data, WS.f_result[x].name, WS.f_result[x].watch_link)).start()
                        
            old_msg = new_msg 
            #msg=f'{data["message"]["text"]} from: BOT'
            #print(f'{data["message"]["text"]} from: {data["message"]["chat"]["username"]}')
            
        sleep(1)

