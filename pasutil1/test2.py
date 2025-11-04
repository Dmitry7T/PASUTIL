import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import MetaTrader5 as mt5
from pasutil1.Strategies import pas
from pasutil1.cycles_utils import update_json
from pasutil1.Symbols import crypto, forex, index

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print('Подключение установлено')

'''for symbol in forex:
    try:
        log = pas(symbol= symbol)
        print(log)
        #update_json("forex", symbol, log)
    except Exception as e:
        print(f'{symbol}:', end= ' ', flush=True)
        print(e, flush=True)
        continue'''

json_string  = pas(symbol= "AUDNZD", mode= 1)
update_json("forex", '1', json_string)
mt5.shutdown()