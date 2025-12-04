import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from pasutil1.data_load import data_load
import MetaTrader5 as mt5

# запросим статус и параметры подключения
#print(mt5.terminal_info())
# получим информацию о версии MetaTrader 5
#print(mt5.version())

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print('Подключение установлено')

print(mt5.terminal_info())
data = data_load(symbol="EURUSD")
print(data)


mt5.shutdown()