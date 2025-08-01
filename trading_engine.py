from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from Symbols import Symbol
from order_engine import make_order


def get_candle_type(candle):
        body_size = abs(candle['close'] - candle['open'])
        total_range = candle['high'] - candle['low']
        
        if total_range == 0:
            return "Нулевая свеча"
        
        body_ratio = body_size / total_range
        
        if body_ratio < 0.3:
            return "Додж/Маленькое тело"
        elif body_ratio > 0.7:
            if candle['close'] > candle['open']:
                return "Сильная бычья"
            else:
                return "Сильная медвежья"
        else:
            if candle['close'] > candle['open']:
                return "Бычья"
            else:
                return "Медвежья"
            
def pasutil(rates, mode = 1):
    candle = rates[-2 + (1 - mode)]

    if candle['close'] > candle['open']:
        body_size = abs(candle['close'] - candle['open'])
        lower_shadow = candle['open'] - candle['low']
        upper_shadow = candle['high'] - candle['close']

        if lower_shadow / body_size >= 2 and lower_shadow / upper_shadow >= 2:
            symbol = Symbol.symbol_EURUSD
            order_type = mt5.ORDER_TYPE_BUY
            price = mt5.symbol_info_tick(symbol).ask
            lot = 0.1
            deviation = 10  #проскальзование
            stoploss = candle['low']
            takeprofit = candle['open'] + lower_shadow * 2
            if(mode):
                make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit)
            else: 
                print('BUY')
    else:
        body_size = abs(candle['close'] - candle['open'])
        lower_shadow = candle['close'] - candle['low']
        upper_shadow = candle['high'] - candle['open']

        if upper_shadow / body_size >= 2 and upper_shadow / lower_shadow >= 2:
            symbol = Symbol.symbol_EURUSD
            order_type = mt5.ORDER_TYPE_SELL
            price = mt5.symbol_info_tick(symbol).ask
            lot = 0.1
            deviation = 10  #проскальзование
            stoploss = candle['high']
            takeprofit = candle['close'] + upper_shadow * 2
            if(mode):
                make_order(symbol, order_type, price, lot, deviation, stoploss, takeprofit)
            else: 
                print('SELL')