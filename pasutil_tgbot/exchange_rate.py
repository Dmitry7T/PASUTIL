import json

file = "pasutil1/saves.json"

def exchange(index):
    with open(file, "r") as file_open:
        loaded_data = json.load(file_open)

    #print(loaded_data['forex'][f'{index}']['price'])
    position = loaded_data['forex'][f'{index}']['position'] 
    symbol = loaded_data['forex'][f'{index}']['symbol'] 
    price = loaded_data['forex'][f'{index}']['price']
    lot = loaded_data['forex'][f'{index}']['lot']
    stoploss = loaded_data['forex'][f'{index}']['stoploss']
    takeprofit = loaded_data['forex'][f'{index}']['takeprofit']
    date = loaded_data['forex'][f'{index}']['date']

    msg = f"📍Position: {position}\n🔣Symbol: {symbol}\n💰Price: {price}\n📦Lot: {lot}\n⛔️Stoploss: {stoploss}\n✅Takeprofit: {takeprofit}\n📅Date: {date}"

    return msg
