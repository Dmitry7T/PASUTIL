import json

file = "pasutil1/jsons/saves.json"

def exchange(index):
    with open(file, "r") as file_open:
        loaded_data = json.load(file_open)

    #print(loaded_data['forex'][f'{index}']['price'])
    signal = loaded_data['forex'][f'{index}']['signal'] 
    price = loaded_data['forex'][f'{index}']['price']
    close = loaded_data['forex'][f'{index}']['close']
    accuracys = loaded_data['forex'][f'{index}']['accuracy']
    accuracy = round(accuracys)
    date = loaded_data['forex'][f'{index}']['date']

    msg = f"🔔Signal: {signal}\n💰Price: {price}\n🔒Close: {close}\n📅Date: {date}\n🔬Accuracy: {accuracy}"

    return msg

#print(exchange("AUDSEK"))