import json

file = "saves.json"

def exchange(index):
    with open(file, "r") as file_open:
        data = json.load(file_open)

    index = index.upper()
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
        signal = data['index'][f'{index}']['signal'] 
        price = data['index'][f'{index}']['price']
        closes = data['index'][f'{index}']['close']
        close = round(closes)
        accuracys = data['index'][f'{index}']['accuracy']
        accuracy = round(accuracys)
        date = data['index'][f'{index}']['date']

        msg = f"🔔Signal: {signal}\n💰Price: {price}\n🔒Close: {close}\n📅Date: {date}\n🔬Accuracy: {accuracy}"

    return msg

#print(exchange("FCHI40"))