import json
import os

filepath = 'pasutil1\jsons\saves.json'
def read_json():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    return data

def add_json(type, symbol, new_data):
    data = read_json()
    
    if type not in data:
        data[type] = {}
    elif isinstance(data[type], list):
        data[type] = {key: value for item in data[type] for key, value in item.items()}
    
    data[type][symbol] = new_data
    save_json(data)

def update_json(type, symbol, new_data):
    if new_data == None:
        return
    data = read_json()
    symbols_keys = list(data[type].keys())
    if symbol not in symbols_keys:
        add_json(type= type, symbol= symbol, new_data= new_data)
        return
    
    data[type][symbol] = new_data
    save_json(data)

def save_json(data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)