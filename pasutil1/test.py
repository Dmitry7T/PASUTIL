import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pasutil1.data_load import data_load
import MetaTrader5 as mt5
from pasutil1.Symbols import Symbol

# запросим статус и параметры подключения
#print(mt5.terminal_info())
# получим информацию о версии MetaTrader 5
#print(mt5.version())

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print('Подключение установлено')

'''symbols = mt5.symbols_get()
print("Доступные символы:", [s.name for s in symbols[:10]])'''

symbol = "EURUSD"
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"Символ {symbol} не найден")
else:
    print(f"Символ {symbol} доступен")
    print(f"Торговые сессии: {symbol_info.session_deals}")

for symbol_name in dir(Symbol):
    if not symbol_name.startswith('__'):
        symbol = getattr(Symbol, symbol_name)
        rates = data_load(symbol= symbol)
        print(rates)

mt5.shutdown()