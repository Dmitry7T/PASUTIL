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

print(round(mt5.account_info().balance * 0.01 / 300, 2))

mt5.shutdown()