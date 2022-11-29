from asyncore import read
from concurrent.futures import thread
from posixpath import isabs
import requests
import locale
import ssl
import websocket
import _thread
import time
import rel
import json
import time
import threading
import io
import random
import os 
from flask import Flask, request, jsonify

import youtube

client_id = "e103fcf7d66128c319802b0cc1c113a7"
secret_client = "67925d0577bd9bd6c258c3447d8d26dd"
access_token = "wpsblit6o6cuopsvunk3qw"
channel_id = "109793075" #possandglor
# channel_id = "108698391" #Yeti!
api = Flask(__name__)
chat_token = 'CggIARCg9MWWBhL3AgovCLOerTQSJGFhY2NlMzhhLTU0MTEtNDdkNi1iODk4LWVkZWNjMjEyZmIzOSICUlUShQIIBBgGUv4BCgljb21tLWluZm8S8AFDaG9JczU2dE5CSVRPRFUxTWprNU1EVXdOamM1TWpjMk16VXpOaEpNQ0FNU0tHVXdOMlpqT1RJM05USXpPVFZoWVdFMU5qUTJPVGd6WTJOa09EUTRNakEwTjJVMVpEWXdPR1lZQWlJY0NnVXpNVEl6TmhJVE9EVTFNams1TURVd05qYzVNamMyTXpVek5ob2xHQVF3QmtvU05URTBNVFV3TmpBME9ESXlNRFl3TnpJd1dnSlNWWElGY25VdFVsVjRCQ0lkQ2h0N0luUnBaQ0k2SWpFMk5UYzRPVFV6T1RJeE9EazVOak16SW4xS0FBPT0aPAonCAEQs56tNBoeMTA5NzkzMDc1XzEwOTc5MzA3NV8xNjU3ODcxOTk5ELOerTQaB2RlZmF1bHQgs56tNA==.iJi3pWzhAUMZ-XuNgNyT3N0L6L1fTCFSVLKIT42uB-4='
isOpened = True

access_code = "2c04398aa50a7444805cae93359f2676"
refresh_token = ""
msgs = []
chnls = []
pisun = {}
iqs={}
rulet = ['Тебя убили... Но ты выжил! DansGame', 'Осечка! KappaPride', 'Мимо!',
         'Приставив ствол к виску ты обмочил штаны. Не осуждаю!', 'Здоровья погибшим, а ты скоро умрешь Kappa', '/timeout']
         
def getToken():
    global access_token
    global refresh_token
    headers = {
        'Accept': 'application/json',
        'client-id': client_id,
        'Content-Type': 'application/json',
    }

    data = '{\n    "client_secret": "'+secret_client +'",\n    "grant_type": "authorization_code",\n    "code": "'+access_code+'",\n    "redirect_uri": "http://trovo.live"\n}'

    response = requests.post(
        'https://open-api.trovo.live/openplatform/exchangetoken', headers=headers, data=data)
    print("getToken:")
    # print(response.json())
    access_token=response.json()["access_token"]
    refresh_token=response.json()["refresh_token"]
    print(refresh_token)


a = 0

dir = os.path.abspath(os.curdir)

def validateAccess():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Authorization': 'OAuth '+access_token,
    }
    print(headers)
    response = requests.get(
        'https://open-api.trovo.live/openplatform/validate', headers=headers)
    print("validate:")
    print(response.json())

timeQuest = 0
isStartedViktorina = True
answer = ""
isAnswered = True
selectedquest = ""
with open(dir+'/config/questions.txt', 'r', encoding='utf-8') as f:
    s = f.read()
    f.close()
questions = s

def Viktorina():
    global questions
    global selectedquest
    global answer
    global timeQuest
    global isAnswered
    while isStartedViktorina:
        if isAnswered:
                newQuest()
                quest = selectedquest.split("|")[0].replace("а","a").replace("о","o").replace("е","e").replace("р","p").replace("с","c")
                answer = selectedquest.split("|")[1]
                timeQuest = len(answer)*30+5
                print(quest+" - "+answer)
                podskazka = "_"*len(answer)
                isAnswered = False
        if timeQuest==(len(answer)*30):
            msgs.append("Вопрос: "+quest+" ("+str(len(answer))+" букв)")
        if timeQuest <len(answer)*30 and (len(answer)*30-timeQuest)%30==0:
            thisIndex = random.choice([i for i in range(len(podskazka)) if podskazka.startswith('_', i)])
            podskazka = list(podskazka)
            podskazka[thisIndex] = list(answer)[thisIndex]
            podskazka = "".join(podskazka)
            msgs.append("Подсказка: "+podskazka)
        if timeQuest==0 or timeQuest==1:
            msgs.append("Никто не угадал, правильный ответ: "+answer)
            timeQuest= len(answer)*30+10
            isAnswered = True
            
        time.sleep(1)
        timeQuest= timeQuest-1
# validateAccess()
seks = 0
def newQuest():
    global questions
    global answer
    global timeQuest 
    global selectedquest 
    selectedquest = random.choice(questions.split("\n"))
    answer = selectedquest.split("|")[1]
    timeQuest = len(answer)*30+5


t3 = threading.Thread(target=Viktorina)

def asd(message,chnl,username):
    global seks
    global isAnswered
    global answer
    global isStartedViktorina
    global scores
    global t3
    if username in scores.keys():
        scores[username]=scores[username]+1
    else:
        scores[username] = 1
    if message.startswith(u'!шар'):
        if 'когда' in message:
            msgs.append(random.choice(when))
            chnls.append(chnl)
        elif 'почему' in message:
            msgs.append(random.choice(because))
            chnls.append(chnl)
        else:
            msgs.append(random.choice(foo))
            chnls.append(chnl)
    if message== "!старт":
        isStartedViktorina = True
        t3 = threading.Thread(target=Viktorina)
        t3.start()
    if message== "!стоп":
        isStartedViktorina = False
        
    if message.startswith('!факт'):
        msgs.append(random.choice(facts))
        chnls.append(chnl)
    if message.lower() == answer.lower():
        if username in scores.keys():
            scores[username]=scores[username]+10
        else:
            scores[username] = 1
        msgs.append(username+" дал правильный ответ!")
        isAnswered = True
    if message.startswith('!статус'):
        msgs.append(random.choice(status))
        chnls.append(chnl)
    if message.startswith('!писюн'):
        if username in pisun:
            msgs.append(pisun[username])
        else:
            pisun[username]="Писюн " + username+" длинной целых " + str(random.randint(1, 35))+" см! PogChamp"
            msgs.append(pisun[username])
        chnls.append(chnl)
    if message.startswith('!рулетка'):
        com = random.choice(rulet)
        if com == '/timeout':
            com='/ban'
            timeBan = random.randint(0, 400)
            com += ' @'+username+' '+str(timeBan)
            msgs.append(username+" отлетел на "+str(timeBan)+" KappaPride")
            chnls.append(chnl)
        msgs.append(com)
        chnls.append(chnl)
    if message.startswith("!m"):
        youtube.addToList(message.split(" ")[1])
    if ' + ' in message:
        r = message.split('+')
        msgs.append(r[0]+'любит'+r[1]+' на ' +
                    str(random.randint(0, 100))+'%')
        chnls.append(chnl)
    if ' !- ' in message:
        r = message.split('!-')
        msgs.append(r[0]+'ненавидит'+r[1]+' на ' +
                    str(random.randint(0, 100))+'%')
        chnls.append(chnl)
    # if '!set' in message:
    #     global chat
    #     chat = pytchat.create(video_id=message.split(' ')[1])
    #     thread1
    if '!секс' in message:
        seks= seks+1
        msgs.append("Секс "+ str(seks))
        chnls.append(chnl)
    if '!очки' in message:
        msgs.append("Твои очки "+ str(scores[username]))
    if ' <> ' in message:
        r = message.split('<>')
        msgs.append(random.choice(r))
        chnls.append(chnl)
    # if message.startswith('!join'):
    #     r = message[6:]
    #     s.send(bytes("JOIN #" + r+" \r\n", "UTF-8"))
    #     f = open("config/nick.txt","a+")
    #     f.write(r+"\n")
    #     f.close()
    # if message.startswith('!leave') :
    #     s.send(bytes("PART #" + chnl+" \r\n", "UTF-8"))
    #     f = open("config/nick.txt","r+")
    #     sss = f.readlines()
    #     f.close()
    #     print(sss)
    #     sss.remove(chnl+"\n")

    #     f = open("config/nick.txt","w+")
    #     for a in sss:
    #         f.write(a)
    #     f.close()
    if message.startswith('!прогноз'):
        r = message[9:]
        msgs.append(r+' вероятно на ' +
                    str(random.randint(0, 100))+'%')
        chnls.append(chnl)
    if message.startswith('!love'):
        r = message[6:]
        msgs.append(username+' любит '+r+' на ' +
                    str(random.randint(0, 100))+'%')
        chnls.append(chnl)
    if message.startswith('!шанс'):
        msgs.append("Шанс вырастить дополнительную хромосому у "+username+' составляет ' +
                    str(random.randint(0, 100))+'% PogChamp')
        chnls.append(chnl)
    # if message.startswith('!фильм'):
    #     msgs.append(filmname)
    #     chnls.append(chnl)
    if message.startswith('!цитата'):
        if len(message) > 7:
            cit = []
            print(message.split(' ')[1])
            for i in quotes:
                if message.split(' ')[1] in i:
                    cit.append(i)
                    print(i)
            msgs.append(random.choice(cit))
            chnls.append(chnl)
        else:
            msgs.append(random.choice(quotes))
            chnls.append(chnl)
    if message.startswith('!фап '):
        msgs.append(message[5:] + ' фапабельно на ' +
                    str(random.randint(0, 100)) + '%')
        chnls.append(chnl)
    if "Слава Україні!" in message:
        msgs.append("Слава нації!")
        chnls.append(chnl)
    if message.startswith('!+ '):
        quotes.append(message[3:])
        with open(dir+'/config/quotes.txt', 'a+',encoding="utf-8") as f:
            f.write(message[3:]+"\n")
        msgs.append("Цитата добавлена")
        chnls.append(chnl)
    if message.startswith('!iq'):
        if 3 < len(message):
            msgs.append('IQ '+message[4:]+' = ' +
                        str(random.randint(0, 200)))
            chnls.append(chnl)
        else:
            if username in iqs:
                msgs.append(iqs[username])
            else:
                iqs[username]='IQ '+username+' = '+str(random.randint(0, 200))
                msgs.append(iqs[username])
            chnls.append(chnl)

def refreshAccess():
    global access_token
    global refresh_token
    while isOpened:
        time.sleep(14390)
        headers = {
            'Accept': 'application/json',
            'client-id': client_id,
            'Content-Type': 'application/json',
        }

        data = '{\n    "client_secret": '+secret_client+',\n    "grant_type": "refresh_token",\n    "refresh_token": '+refresh_token+'\n}'

        response = requests.post('https://open-api.trovo.live/openplatform/refreshtoken', headers=headers, data=data)
        print("refreshtoken:")
        print(response.json())


def getChannelInfo(nick):
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"user":["'+nick+'"]}'

    response = requests.post(
        'https://open-api.trovo.live/openplatform/getusers', headers=headers, data=data)
    print("getchannelInfo:")
    
    print(response.json())


def sendMessageToChannel(text):
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Authorization': 'OAuth '+access_token,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }

    data = '{"content": "'+text+'", "channel_id": "'+channel_id+'"}'
    print(data)
    data = data.encode()
    response = requests.post(
        'https://open-api.trovo.live/openplatform/chat/send', headers=headers, data=data)
    print("sendMessageToChannel:")

    print(response.json())


def sendMessageToMe():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Authorization': 'OAuth '+access_token,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    print(headers)

    data = '{"content": "test"}'

    response = requests.post(
        'https://open-api.trovo.live/openplatform/chat/send', headers=headers, data=data)
    print("sendMessageToMe:")
    print(response.json())

# sendMessageToMe()


def getInfo():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Authorization': 'OAuth '+access_token,
    }

    response = requests.get(
        'https://open-api.trovo.live/openplatform/channel', headers=headers)
    print("GetInfo:")


def getFollowers():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"limit":5,"cursor":0}'

    response = requests.post('https://open-api.trovo.live/openplatform/channels/' +
                             channel_id+'/followers', headers=headers, data=data)
    print(response.json())

# getFollowers()


def infofromid():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"channel_id":"'+channel_id+'"}'

    response = requests.post(
        'https://open-api.trovo.live/openplatform/channels/id', headers=headers, data=data)
    print("InfoFromId:")
    print(response.json())


def infofromname():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = '{"username":"possandglor"}'

    response = requests.post(
        'https://open-api.trovo.live/openplatform/channels/id', headers=headers, data=data)
    print("infoFromName:")
    print(response.json())


with open(dir+'/config/scores.json', 'r', encoding='utf-8') as f:
    s = f.read()
scores = json.loads(s)

fname = 'ball.txt'
with open(dir+'/config/'+fname, 'r', encoding='utf-8') as f:
    s = f.read()
foo = s.split('\n')
with open(dir+'/config/fact.txt', 'r', encoding='utf-8') as f:
    s = f.read()
facts = s.split('\n')
with open(dir+'/config/quotes.txt', 'r', encoding='utf-8') as f:
    s = f.read()
quotes = s.split('\n')
with open(dir+'/config/when.txt', 'r', encoding='utf-8') as f:
    s = f.read()
when = s.split('\n')
with open(dir+'/config/because.txt', 'r', encoding='utf-8') as f:
    s = f.read()
because = s.split('\n')
with open(dir+'/config/status.txt', 'r', encoding='utf-8') as f:
    s = f.read()
status = s.split('\n')

with open(dir+'/config/lolnicks.txt', 'r', encoding='utf-8') as f:
    s = f.read()
lolnicks = s.split('\n')
lolNicksArray = []
for i in lolnicks:
    lolNicksArray.append(i.split('|')[0])
with open(dir+'/config/nick.txt', 'r', encoding='utf-8') as f:
    nicks = f.read().split('\n')
seks = 0

# sendMessageToChannel()

# ws = websocket.WebSocket()
# ws.connect("wss://open-chat.trovo.live/chat",ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS))

# async def hello():
#     async with websockets.connect('wss://open-chat.trovo.live/chat',ssl=ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)) as websocket:
#         data = 'hi'
#         await websocket.send(data)
#         print("> {}".format(data))

#         response = await websocket.recv()
#         print("< {}".format(response))
# hello()

def getChatToken():
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
        'Authorization': 'OAuth '+access_token,
    }

    response = requests.get('https://open-api.trovo.live/openplatform/chat/token', headers=headers)
    print("getChattoken:")
    print(response.json())
# getChatToken()

def getMyChatToken():
    global chat_token
    headers = {
        'Accept': 'application/json',
        'Client-ID': client_id,
    }

    response = requests.get('https://open-api.trovo.live/openplatform/chat/channel-token/'+channel_id, headers=headers)
    print("getMyChattoken:")
    print(response.json())
    chat_token = response.json()["token"]
getToken()

t0 = threading.Thread(target=refreshAccess)
t0.start()

getMyChatToken()
def ping():
    global scores
    time.sleep(5)
    while isOpened:
        a = {
            "type": "PING",
            "nonce": "zxcmnvfg",
        }
        ws.send(json.dumps(a))
        time.sleep(30)
        with open(dir+'/config/scores.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(scores))
            f.close()
t1 = threading.Thread(target=ping)
t1.start()

def sendes():
    while isOpened:
        if len(msgs) > 0:
            sendMessageToChannel(msgs[0])
            msgs.pop(0)
            try:
                chnls.pop(0)
            except:
                print("chnls pustoi")
            time.sleep(1.5)
t2 = threading.Thread(target=sendes)
t2.start()
def on_message(ws, message):
    if json.loads(message)["type"] != "PONG":
        text = json.loads(message)["data"]["chats"][0]["content"]
        username = json.loads(message)["data"]["chats"][0]["nick_name"]
        # print(message)
        chnl = "possandglor"
        asd(text,chnl,username)

    # print(message)


def on_error(ws, error):
    isOpened = False
    print(error)


def on_close(ws, close_status_code, close_msg):
    isOpened = False
    print("### closed ###")



def on_open(ws):
    a = {
        "type": "AUTH",
        "nonce": "zxcmnv",
        "error": "asd",
        "data": {
            "token": chat_token
        }
    }
    ws.send(json.dumps(a))
    # print(a)
    print("Opened connection")

ws = websocket.WebSocketApp("wss://open-chat.trovo.live/chat",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
def start():
    # websocket.enableTrace(True)
    

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    rel.signal(2, rel.abort)  # Keyboard Interrupt

    rel.dispatch()

start()

