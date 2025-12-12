import time
import MetaTrader5 as mt5
import schedule

from pasutil1.cycles import pas_cycle
from pasutil1.tracker import monitor_file

def worker():
    #schedule.every(11).seconds.do(pas_cycle)
    schedule.every(30).minutes.at(":00").do(pas_cycle)
    monitor_file("pasutil1\jsons\saves.json")

    while True:
        schedule.run_pending()
        time.sleep(1)


def starter():
    if not mt5.initialize():
        print("initialize() failed", flush=True)
        mt5.shutdown()
    else:
        print('Connection complete', flush=True)
        print("Launching trading bot...", flush=True)

    try:
        worker()

    except KeyboardInterrupt:
        print("Stop at the user's request", flush=True)   

    finally:
        mt5.shutdown()
        print("Stopping connection", flush=True)
        return

if __name__ == "__main__":
    starter()