from pasutil1.Symbols import crypto, forex, index
from pasutil1.Strategies import pas
from pasutil1.Session import is_London
from pasutil1.data_load import data_load
from pasutil1.utils import update_json

def pas_cycle():
    if is_London:
        for symbol in crypto:
            try:
                log = pas(symbol= symbol)
                update_json("crypto", symbol, log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
        for symbol in forex:
            try:
                log = pas(symbol= symbol)
                update_json("forex", symbol, log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
        for symbol in index:
            try:
                log = pas(symbol= symbol)
                update_json("index", symbol, log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
    else:
        print('ожидает начала сессии', flush=True)