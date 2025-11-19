import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import time
import MetaTrader5 as mt5
import schedule

from pasutil1.cycles import pas_cycle
from pasutil1.utils_b import update_jsons

def worker():
    #schedule.every(11).seconds.do(pas_cycle)
    schedule.every(30).minutes.at(":00").do(pas_cycle)

    #schedule.every(15).seconds.do(update_jsons, 15, 'saves15.json')
    #schedule.every(30).seconds.do(update_jsons, 30, 'saves30.json')
    #schedule.every(60).seconds.do(update_jsons, 60, 'saves60.json')
    schedule.every(15).minutes.at(":00").do(update_jsons, 15, 'saves15.json')
    schedule.every(30).minutes.at(":00").do(update_jsons, 30, 'saves30.json')
    schedule.every(60).minutes.at(":00").do(update_jsons, 60, 'saves60.json')

    while True:
        schedule.run_pending()
        time.sleep(1)


def starter():
    if not mt5.initialize():
        print("initialize() failed", flush=True)
        mt5.shutdown()
    else:
        print('Подключение установлено', flush=True)
        print("Запуск торгового бота...", flush=True)

    try:
        worker()

    except KeyboardInterrupt:
        print("Остановка по запросу пользователя", flush=True)   

    finally:
        mt5.shutdown()
        print("Остановка подключения", flush=True)
        return

if __name__ == "__main__":
    starter()