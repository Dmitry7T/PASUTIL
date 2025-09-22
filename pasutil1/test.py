import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_load import data_load
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from Symbols import Symbol
from trading_engine import pasutil_XAUUSD


if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
print('Подключение установлено')

rates = data_load(Symbol.symbol_XAUUSD)
#print(rates)

pasutil_XAUUSD()

mt5.shutdown()