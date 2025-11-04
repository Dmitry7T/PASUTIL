from datetime import datetime
from datetime import datetime, timedelta
import MetaTrader5 as mt5

from pasutil1.data_load import data_load

def get_candle_type(candle):
    if candle['close'] > candle['open']:
        return 1
    return 0


# price action strategy
def pas(symbol, rates = None, mode = 1):
    if rates is None:
        rates = data_load(symbol)

    point = 0.00001
    candle_first_index = -2 + (1 - mode)
    candle0 = rates[candle_first_index]
    candle1 = rates[candle_first_index - 1]

    if  get_candle_type(candle0) or  get_candle_type(candle1):
        if get_candle_type(candle0) != get_candle_type(candle1):
            return
        else:
            # бычья бычья
            delta = candle0['close'] - candle1['high']
            if delta / point >= 20:
                price = candle0['low']
                log = {
                    "signal" :'BUY',
                    "price" : price,
                    "close" : price + 0.01 * 300 * 8,
                    "accuracy" : delta / point,
                    "date" : f'{datetime.fromtimestamp(candle0[0]) - timedelta(hours=2)}',
                }
                return log 
    else:     
        # медвежья медвежья
        delta = candle1['low'] - candle0['close']
        if delta / point >= 20:
                price = candle0['low']
                log = {
                    "signal" : 'SELL',
                    "price" : price,
                    "close" : price + 0.01 * 300 * 8,
                    "accuracy" : delta / point,
                    "date" : f'{datetime.fromtimestamp(candle0[0]) - timedelta(hours=2)}',
                }
                return log 
    return None