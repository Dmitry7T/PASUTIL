from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol

def make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit):
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": deviation,
        "sl": stoploss,
        "tp": takeprofit,
        "magic": 123456,
        "comment": "pasutil order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_FOK,
    }

    # Отправка ордера
    try:
        result = mt5.order_send(request)
        print(f"Ордер выставлен: {datetime.now()}")
    except Exception  as e:
        print('ошибка выставления ордера')
        print(e)