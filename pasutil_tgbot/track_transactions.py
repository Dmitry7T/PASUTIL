import requests
from time import sleep
import datetime
from config import TONCENTER_URL, WATCH_ADDRESS_B64, headers
import time

def fetch_account_transactions(address, limit):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getTransactions",
        "params": {
            "address": address,
            "limit": limit,
            "archival": False
        }
    }

    response = requests.post(TONCENTER_URL, json=payload, headers=headers)
    response.raise_for_status()
    #print(response.json().get('result', []))  #1762958976
    transactions = response.json().get('result', [])
    
    new_transfers = []
    for tx in transactions:
        in_msg = tx.get('in_msg')
        if in_msg and in_msg.get('source') != address:
            value_ton = int(in_msg.get('value', 0)) / 1000000000
            
            new_transfers.append({
                #"tx_hash": tx['transaction_id']['hash'],
                "sender": in_msg.get('source'),
                "price": value_ton,
                "time": tx['utime']
            })
            
    return new_transfers


def transaction(expectation_price): #0.1732
    t = 0
    n = False
    st = time.time()
    while n!= True:
        transaction = fetch_account_transactions(WATCH_ADDRESS_B64, 1) 
        for x in transaction:
            if x['price'] == expectation_price and x['time'] > st:
                n = True
                dt_object_utc = datetime.datetime.fromtimestamp(x['time'], tz=datetime.timezone.utc)
                #print(f"\nTransaction on {x['price']}\nTime: {dt_object_utc}\nSender: {x['sender']}\n")
                return f"Transaction on {x['price']}\nTime: {dt_object_utc}\nSender: {x['sender']}"
            
            else:
                print('None')
                sleep(3)
                t += 3
                if t > 15*60:
                    n = True
                    return "Transaction NOT found"

print(transaction(0.1732))
