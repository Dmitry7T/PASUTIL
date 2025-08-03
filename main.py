import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time  
import datetime 
import time
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol
from trading_engine import pasutil_XAUUSD
 
# запросим статус и параметры подключения
#print(mt5.terminal_info())
# получим информацию о версии MetaTrader 5
#print(mt5.version())

def pasutil_XAUUSD_main_cycle():
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print('Подключение установлено')

    try:
        while 1:
            try:
                if datetime.time(10, 0) <= datetime.datetime.now().time() <= datetime.time(18, 30) \
                and datetime.datetime.now().weekday() < 6:
                    orders = mt5.orders_get(symbol=Symbol.symbol_XAUUSD)
                    if orders is None:
                        pasutil_XAUUSD()
                        print('ожидает...', flush=True)
                        time.sleep(900)
                else:
                    print('ожидает начала сессии', flush=True)
                    time.sleep(1800)
            except Exception as e:
                print(e)
                time.sleep(900)
                continue

    except KeyboardInterrupt:
        print("Остановка по запросу пользователя")
    finally:
        mt5.shutdown()
        print("Остановка подключения")

if __name__ == "__main__":
    print("Запуск торгового бота...")
    pasutil_XAUUSD_main_cycle()