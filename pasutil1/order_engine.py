from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol

def make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit):
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "sl": stoploss,       # Stop Loss (0 - без стоп-лосса)
        "tp": takeprofit,       # Take Profit (0 - без тейк-профита)
        "deviation": deviation,
        "magic": 123456,
        "comment": "pasutil order",
        "type_time": mt5.ORDER_TIME_GTC,  # Срок действия - до отмены
        "type_filling": mt5.ORDER_FILLING_FOK,  # Тип исполнения
    }

    # Отправка ордера
    try:
        mt5.order_send(request)
        print(f"Ордер выставлен: {datetime.now()}")
    except Exception as e:
        print('ошибка выставления ордера')
        print(e)