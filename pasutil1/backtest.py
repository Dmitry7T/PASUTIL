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
from pasutil1.Symbols import Symbol
from pasutil1.data_load import data_load
from pasutil1.Strategies import pasutil_XAUUSD
 
# запросим статус и параметры подключения
#print(mt5.terminal_info())
# получим информацию о версии MetaTrader 5
#print(mt5.version())

def pasutil_XAUUSD_backtest_cycle():
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print('Подключение установлено')

    try:
        # год месяц число час минута
        mounth = 8
        for i in range(30):
            print(f'\n\nday: {i + 1}')
            backtest_start_day = datetime(2025, mounth, 1 + i, 10, 00)
            
            try:
                if backtest_start_day.weekday() < 5:
                    for j in range (16):
                        end_date = backtest_start_day + timedelta(minutes= j * 30) + timedelta(hours=1) + timedelta(hours=3)
                        data = data_load(Symbol.symbol_XAUUSD, end_date)
                        if pasutil_XAUUSD(0, data) == 0:
                            break
                else:
                    continue
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        print("Остановка по запросу пользователя")
    finally:
        mt5.shutdown()
        print("Остановка подключения")


if __name__ == "__main__":
    print("Запуск торгового бота в режиме бектеста")
    pasutil_XAUUSD_backtest_cycle()