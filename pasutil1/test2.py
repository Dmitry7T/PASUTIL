import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import json
import MetaTrader5 as mt5
from pasutil1.Strategies import pas
from pasutil1.utils import update_json

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print('Подключение установлено')

json_string  = pas(symbol= "XAUUSD")
print(json_string)
update_json("forex", 1, json_string)
mt5.shutdown()