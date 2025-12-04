import json
import os
from datetime import datetime, timedelta

class JSONManagerOutput:
    def __init__(self):
        self.path = 'pasutil1\jsons\\'

    def read(self):
        path = self.path + 'saves.json'
        if os.path.exists(path):
            with open(path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        return data

    def update(self):
        data = self.read()
        output_data = {}
        with open("pasutil1\\symbols\\top_pairs.txt", 'r') as f:
            top_list = eval(f.read().strip())
        top_data = {}
        time_threshold = datetime.now() - timedelta(seconds=10)

        for data_type, symbols in data.items():
            output_data[data_type] = {}
            for symbol, symbol_data in symbols.items():
                try:
                    symbol_date_str = symbol_data.get("date", "")
                    if symbol_date_str:
                        symbol_date = datetime.strptime(symbol_date_str, "%Y-%m-%d %H:%M:%S")
                        if symbol_date <= time_threshold:
                            output_data[data_type][symbol] = symbol_data
                            if symbol in top_list:
                                top_data[data_type][symbol] = symbol_data

                            
                except ValueError as e:
                    print(f"Ошибка парсинга даты для {data_type}.{symbol}: {e}")
                    continue

        self.save(output_data, "output.json")
        self.save(top_data, "top_pairs.json")

    def save(self, data, file):
        path = self.path + file
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)



class JSONManagerSaves:
    def __init__(self):
        path = 'pasutil1\jsons\saves.json'

    def read(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}
        return data

    def add(self, type, symbol, new_data):
        data = self.read()
        
        if type not in data:
            data[type] = {}
        elif isinstance(data[type], list):
            data[type] = {key: value for item in data[type] for key, value in item.items()}
        
        data[type][symbol] = new_data
        self.save(data)

    def update(self, type, symbol, new_data):
        if new_data == None:
            return
        data = self.read()
        symbols_keys = list(data[type].keys())
        if symbol not in symbols_keys:
            self.add(type= type, symbol= symbol, new_data= new_data)
            return
        
        data[type][symbol] = new_data
        self.save(data)

    def save(self, data):
        with open(self.path, 'w') as f:
            json.dump(data, f)