import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time  
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol
from data_load import data_load
from trading_engine import pasutil
 
# запросим статус и параметры подключения
#print(mt5.terminal_info())
# получим информацию о версии MetaTrader 5
#print(mt5.version())

def main():
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print('Подключение установлено')

    try:
        # год месяц число час
        end_date = datetime(2025, 7, 24, 17) + timedelta(hours=3)
        data = data_load(Symbol.symbol_EURUSD, end_date)
        pasutil(data, 0)

    except KeyboardInterrupt:
        print("Остановка по запросу пользователя")
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    print("Запуск торгового бота в режиме бектеста")
    main()