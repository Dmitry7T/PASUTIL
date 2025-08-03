import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_load import data_load
from datetime import datetime, timedelta
import MetaTrader5 as mt5
from Symbols import Symbol

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
print('Подключение установлено')

end_date = datetime(2025, 7, 3, 18, 30) + timedelta(hours=3)
print(data_load(Symbol.symbol_XAUUSD, end_date))

mt5.shutdown()