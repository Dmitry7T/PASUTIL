from datetime import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol
from order_engine import make_order
from data_load import data_load


def get_candle_type(candle):
    if candle['close'] > candle['open']:
        return 1
    return 0


# пасутил ЗОЛОТО/ДОЛЛАР            
def pasutil_XAUUSD(mode = 1, rates = None):
    if rates is None:
        rates = data_load(Symbol.symbol_XAUUSD)
    candle_first_index = -2 + (1 - mode)
    candle0 = rates[candle_first_index]
    candle1 = rates[candle_first_index - 1]

    if  get_candle_type(candle0) or  get_candle_type(candle1):
        if get_candle_type(candle0) != get_candle_type(candle1):
            return
        else:
            # бычья бычья
            delta = candle0['close'] - candle1['high']
            if delta / 0.01 >= 20:
                symbol = Symbol.symbol_XAUUSD
                order_type = mt5.ORDER_TYPE_BUY_LIMIT
                price = candle0['low']
                lot = round(mt5.account_info().balance * 0.01 / 300, 2)
                deviation = 10  #проскальзование
                stoploss = price - 0.01 * 300
                takeprofit = price + 0.01 * 300 * 8
                if(mode):
                    make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit)
                    print(f"BUY_LIMIT:\nprice: {price}\nlot: {lot}\nstoploss: {stoploss}\n\
takeprofit: {takeprofit}\ndate: {datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)}\ndelta = {delta}", flush=True)
                    return
                else: 
                    print('____________________')
                    print(f"BUY_LIMIT:\nprice: {price}\nlot: {lot}\nstoploss: {stoploss}\n\
takeprofit: {takeprofit}\ndate: {datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)}\ndelta = {delta}")
                    return mode
    else:     
        # медвежья медвежья
        delta = candle1['low'] - candle0['close']
        if delta / 0.01 >= 20:
            symbol = Symbol.symbol_XAUUSD
            order_type = mt5.ORDER_TYPE_SELL_LIMIT
            price = candle0['high']
            lot = round(mt5.account_info().balance * 0.01 / 300, 2)
            deviation = 10  #проскальзование
            stoploss = price + 0.01 * 300
            takeprofit = price - 0.01 * 300 * 8
            if(mode):
                make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit)
                print(f"SELL_LIMIT:\nprice: {price}\nlot: {lot}\nstoploss: {stoploss}\n\
takeprofit: {takeprofit}\ndate: {datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)}\ndelta = {delta}", flush=True)
                return
            else: 
                print('____________________')
                print(f"SELL_LIMIT:\nprice: {price}\nlot: {lot}\nstoploss: {stoploss}\n\
takeprofit: {takeprofit}\ndate: {datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)}\ndelta = {delta}")
                return mode
    return -1