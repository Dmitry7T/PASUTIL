import json

file = "saves.json"

def examination(index):
    with open(file, "r") as file_open:
        loaded_data = json.load(file_open)
        
    if index.upper() in loaded_data['forex'] or index.upper() in loaded_data['index']:
        return True
    
    else:
        return False
#print(loaded_data['forex'])

