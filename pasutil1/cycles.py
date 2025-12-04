from pasutil1.Symbols import crypto, forex, index
from pasutil1.Strategies import pas
from pasutil1.Session import is_London
from pasutil1.JSONmanegers import JSONManagerSaves

def pas_cycle():
    jms = JSONManagerSaves()
    if is_London:
        for symbol in crypto:
            try:
                log = pas(symbol= symbol)
                jms.update(type="crypto", symbol=symbol, new_data=log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
        for symbol in forex:
            try:
                log = pas(symbol= symbol)
                jms.update(type="forex", symbol=symbol, new_data=log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
        for symbol in index:
            try:
                log = pas(symbol= symbol)
                jms.update(type="index", symbol=symbol, new_data=log)
            except Exception as e:
                print(f'{symbol}:', end= ' ', flush=True)
                print(e, flush=True)
                continue
    else:
        print('ожидает начала сессии', flush=True)