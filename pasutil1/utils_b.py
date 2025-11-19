import json
import os
from datetime import datetime, timedelta

filepath = 'pasutil1\jsons\\'
def read_json():
    path = filepath + 'saves.json'
    if os.path.exists(path):
        with open(path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}
    return data

def update_jsons(timeframe, file):
    print(timeframe)
    data = read_json()
    filtered_data = {}
    
    current_time = datetime.now()
    time_threshold = current_time - timedelta(minutes=2 * timeframe)
    
    for data_type, symbols in data.items():
        filtered_data[data_type] = {}
        
        for symbol, symbol_data in symbols.items():
            try:
                symbol_date_str = symbol_data.get("date", "")
                if symbol_date_str:
                    symbol_date = datetime.strptime(symbol_date_str, "%Y-%m-%d %H:%M:%S")
                    if symbol_date >= time_threshold:
                        filtered_data[data_type][symbol] = symbol_data
            except ValueError as e:
                print(f"Ошибка парсинга даты для {data_type}.{symbol}: {e}")
    
    save_json(filtered_data, file)

def save_json(data, file):
    path = filepath + file
    with open(path, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)