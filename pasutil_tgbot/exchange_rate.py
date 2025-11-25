import json

file = "pasutil1/jsons/saves.json"

def exchange(index):
    with open(file, "r") as file_open:
        data = json.load(file_open)

    print(data['forex'])
    signal = data['forex'][f'{index}']['signal'] 
    price = data['forex'][f'{index}']['price']
    closes = data['forex'][f'{index}']['close']
    close = round(closes)
    accuracys = data['forex'][f'{index}']['accuracy']
    accuracy = round(accuracys)
    date = data['forex'][f'{index}']['date']

    msg = f"🔔Signal: {signal}\n💰Price: {price}\n🔒Close: {close}\n📅Date: {date}\n🔬Accuracy: {accuracy}"

    return msg

def exchange_all(time):
    with open(f"pasutil1/jsons/{time}.json", 'r') as f:
        data = json.load(f)['forex']

    # 2. Итерация и вывод данных
    for pair, info in data.items():
        msg = f"Signal: {info['signal']}, Price: {info['price']}, Accuracy: {info['accuracy']}, Date: {info['date']}"
        print(msg)



#print(exchange("AUDSEK"))