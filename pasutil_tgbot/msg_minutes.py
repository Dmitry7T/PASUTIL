import json
from time import sleep
from bot import bot

def min15(index):
    pass

def min30(index, mci):
    pass

def min60(index, mci):
    f = "pasutil1/jsons/saves60.json"
    with open(f, "r") as f_open:
        data = json.load(f_open)
    if index in data['forex']:
        signal = data['forex'][f'{index}']['signal'] 
        price = data['forex'][f'{index}']['price']
        closes = data['forex'][f'{index}']['close']
        close = round(closes)
        accuracys = data['forex'][f'{index}']['accuracy']
        accuracy = round(accuracys)
        date = data['forex'][f'{index}']['date']

        msg = f"🔔Signal: {signal}\n💰Price: {price}\n🔒Close: {close}\n📅Date: {date}\n🔬Accuracy: {accuracy}"
    else:
        return "Error"

    while 1:
        sleep(1*60)
        bot.send_message(mci, msg)
