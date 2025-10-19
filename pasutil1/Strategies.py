from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import MetaTrader5 as mt5
from pasutil1.Symbols import Symbol

from pasutil1.data_load import data_load


def get_candle_type(candle):
    if candle['close'] > candle['open']:
        return 1
    return 0


# price action strategy
def pas(rates = None, symbol= Symbol.symbol_XAUUSD, mode = 1):
    if rates is None:
        rates = data_load(symbol)

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
                price = candle0['low']
                lot = round(mt5.account_info().balance * 0.01 / 300, 2)
                stoploss = price - 0.01 * 300
                takeprofit = price + 0.01 * 300 * 8
                date = datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)
                text = f'"position": "buy_limit", "symbol": "{symbol}", "price": {price}, "lot": {lot}, "stoploss": {stoploss}, "takeprofit": {takeprofit}, "date" : "{date}"'
                json_string  = '{' + text + '}'
                return json_string 
    else:     
        # медвежья медвежья
        delta = candle1['low'] - candle0['close']
        if delta / 0.01 >= 20:
            price = candle0['high']
            lot = round(mt5.account_info().balance * 0.01 / 300, 2)
            stoploss = price + 0.01 * 300
            takeprofit = price - 0.01 * 300 * 8
            date = datetime.fromtimestamp(candle0[0]) - timedelta(hours=3)
            text = f'"position": "sell_limit", "symbol": "{symbol}", "price": {price}, "lot": {lot}, "stoploss": {stoploss}, "takeprofit": {takeprofit}, "date" : "{date}"'
            json_string  = '{' + text + '}'
            return json_string
    return None