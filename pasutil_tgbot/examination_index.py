import json

file = "pasutil1/jsons/saves.json"

def examination(index):
    with open(file, "r") as file_open:
        loaded_data = json.load(file_open)

    if index in loaded_data['forex']:
        return True
    
    else:
        return False
#print(loaded_data['forex'])