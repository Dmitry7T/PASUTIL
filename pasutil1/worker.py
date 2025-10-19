import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import MetaTrader5 as mt5
import asyncio

from pasutil1.Symbols import Symbol
from pasutil1.Strategies import pas
from pasutil1.Session import is_London
from pasutil1.data_load import data_load
from pasutil1.utils import update_json

async def pas_cycle():
    while 1:
            print()
            if is_London:
                for symbol_name in dir(Symbol):
                    try:
                        if not symbol_name.startswith('__'):
                            symbol = getattr(Symbol, symbol_name)
                            log = pas(symbol= symbol)
                            if log != None:
                                update_json("forex", symbol, log)
                    except Exception as e:
                        print(f'{symbol}:', end= ' ', flush=True)
                        print(e, flush=True)
                        continue
                print('ожидает...', flush=True)
                time.sleep(900)
            else:
                print('ожидает начала сессии', flush=True)
                time.sleep(1800)

def starter():
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    else:
        print('Подключение установлено')
        print("Запуск торгового бота...")

    try:
        asyncio.run(pas_cycle())

    except KeyboardInterrupt:
        print("Остановка по запросу пользователя")   

    finally:
        mt5.shutdown()
        print("Остановка подключения")
        return

if __name__ == "__main__":
    starter()