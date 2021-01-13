from flask import Flask, request, abort
import requests
import json
import time 
from Project.Config import *
from uncleengineer import thaistock
API_HOST = 'https://api.bitkub.com'
app = Flask(__name__)
from songline import Sendline
token = 'IPg9MHBV3qsACogEXTxzRmjZ5EuOijFyKDFqRWXmj2I'
messenger = Sendline(token)

################################################################################################################

def checkPrice(cryptoType):
    response = requests.get(API_HOST + '/api/market/ticker')
    result = response.json()
    data = result[cryptoType]
    newPrice = data['last']
    text = '{:,.3f} บาท'.format(newPrice)
    return text
################################################################################################################

condition = {'THB_BTC':{'buy': 1110000, 'sell': 1115000}, 
            'THB_ETH':{'buy': 30000, 'sell': 40000},
            'THB_BAND':{'buy': 200, 'sell': 300},}

def checkCondition(coin, price):
    check_Buy = condition[coin]['buy']
    check_sell = condition[coin]['sell']
    textSend = ''
    if price <= check_Buy:
        text =('{} ราคาลงเเล้วไอ่นิว เหลือ {:,.3f} !! \n ราคาที่อยากซื้อ : {:,.3f}'.format(coin, price, check_Buy))
        messenger.sendtext(text)
        condition[coin]['buy'] = 0
        textSend += text +'\n'
    if price >=  check_sell:
        text =('{} ราคาขึ้นเป็น {:,.3f} !!\n ราคาที่อยากขาย : {:,.3f}'.format(coin, price, check_sell))
        messenger.sendtext(text)
        textSend += text +'\n'
        condition[coin]['sell'] = 10000000
    return textSend

def realTimePrice(cryptoType, choice, priceNeed):
    condition[cryptoType][choice] = priceNeed
    while True:
        response = requests.get(API_HOST + '/api/market/ticker')
        result = response.json()
        data = result[cryptoType]
        newPrice = data['last']
        ans = checkCondition(cryptoType, newPrice)
        if len(ans) > 0:
            print(ans)
            break
        
        else:
            time.sleep(1)
    return ans
################################################################################################################

@app.route('/webhook', methods=['POST','GET'])
def webhook():
    res = 0
    cryptoType = ''
    booleanNotify = False
    notify = ''
    choice = ''

    if request.method == 'POST':

        payload = request.json
        Reply_token = payload['events'][0]['replyToken']
        print("Reply to ken : ",Reply_token,'\n')
        message = payload['events'][0]['message']['text']
        print("Message : ",message)
        
        if "btc" in message:
            cryptoType += 'THB_BTC'
        elif "band" in message:
            cryptoType += 'THB_BAND'
        elif "eth" in message:
            cryptoType += 'THB_ETH'
        elif "xlm" in message:
            cryptoType += 'THB_XLM'
        elif "xrp" in message:
            cryptoType += 'THB_XRP'
        

        if 'ซื้อ' in message:
            choice = 'buy'
        elif 'ขาย' in message:
            choice = 'sell'


        if "เเจ้ง" in message:
            booleanNotify = True
            res += [int(i) for i in message.split() if i.isdigit()][0]
 
        if booleanNotify == True:
            notify += realTimePrice(cryptoType, choice, res)
        else:
            Reply_messasge = 'ราคา {} ขณะนี้ : {}'.format(cryptoType, checkPrice(cryptoType))
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)

        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

################################################################################################################

@app.route('/')
def hello():
    return 'hello world book',200

def ReplyMessage(Reply_token, TextMessage, Channel_access_token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Channel_access_token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage
        }]
    }

    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200