from datetime import datetime
from datetime import datetime, timedelta, time
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
            return None
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


class Strategy:
    def __init__(self, symbol):
        self.symbol = symbol
        
    def get_candle_type(self, candle):
        return 1 if candle['close'] > candle['open'] else 0
    
    def timeframe(self, timeframe_mt5):
        if timeframe_mt5 == mt5.TIMEFRAME_MN1: return timedelta(month= 1)
        if timeframe_mt5 == mt5.TIMEFRAME_W1: return timedelta(day= 7)
        if timeframe_mt5 == mt5.TIMEFRAME_D1: return timedelta(day= 1)
        if timeframe_mt5 == mt5.TIMEFRAME_H12: return timedelta(hour= 12)
        if timeframe_mt5 == mt5.TIMEFRAME_H8: return timedelta(hour= 8)
        if timeframe_mt5 == mt5.TIMEFRAME_H6: return timedelta(hour= 6)
        if timeframe_mt5 == mt5.TIMEFRAME_H4: return timedelta(hour= 4)
        if timeframe_mt5 == mt5.TIMEFRAME_H3: return timedelta(hour= 3)
        if timeframe_mt5 == mt5.TIMEFRAME_H2: return timedelta(hour= 2)
        if timeframe_mt5 == mt5.TIMEFRAME_H1: return timedelta(hour= 1)
        if timeframe_mt5 == mt5.TIMEFRAME_M30: return timedelta(minute= 30)
        if timeframe_mt5 == mt5.TIMEFRAME_M20: return timedelta(minute= 20)
        if timeframe_mt5 == mt5.TIMEFRAME_M15: return timedelta(minute= 15)
        if timeframe_mt5 == mt5.TIMEFRAME_M12: return timedelta(minute= 12)
        if timeframe_mt5 == mt5.TIMEFRAME_M10: return timedelta(minute= 10)
        if timeframe_mt5 == mt5.TIMEFRAME_M6: return timedelta(minute= 6)
        if timeframe_mt5 == mt5.TIMEFRAME_M5: return timedelta(minute= 5)
        if timeframe_mt5 == mt5.TIMEFRAME_M4: return timedelta(minute= 4)
        if timeframe_mt5 == mt5.TIMEFRAME_M3: return timedelta(minute= 3)
        if timeframe_mt5 == mt5.TIMEFRAME_M2: return timedelta(minute= 2)
        if timeframe_mt5 == mt5.TIMEFRAME_M1: return timedelta(minute= 1)
        return None
    
    def swing_high(self, data):
        for i in range(len(data)):
            candle0, candle1, candle2 = data[0 + i], data[1 + i], data[2 + i]
            if candle1["high"] > candle0["high"] and candle2["high"] > candle0["high"]:
                return {"type" : 1, "index" : i, "price" : candle1["high"]}
            if candle1["low"] < candle0["low"] and candle2["low"] < candle0["low"]:
                return {"type" : 0, "index" : i, "price" : candle1["low"]}
        return None
    
    def Session(self, timestamp = datetime.now()):
        timestamp = timestamp.time()
        if time(0, 0) <= timestamp <= time(7, 0):
            return "Asia"
        elif time(8, 0) <= timestamp <= time(13, 30):
            return "London"
        elif time(13, 30) <= timestamp <= time(21, 0):
            return "New York"
        else:
            return None


    def high_liquidity(self, timeframe = mt5.TIMEFRAME_D1):
        info = None
        i = 30
        try:
            while not (info is None):
                startdate = self.timeframe(timeframe) * i
                data = data_load(symbol= self.symbol, time=startdate)
                info = self.swing_high
                i += 1
                if i > 1000:
                    break
        except:
            pass
        return info
        
    def low_liquidity(self, timeframe = mt5.TIMEFRAME_M15):
        pass

    def OrderBlock(self):
        pass

    def FVG(self, candle0, candle1):
        return 

    def PO3(self):
        pass

    def IPDA(self):
        pass

    def signal(self):
        pass


class TestStrategy(Strategy):
    def testSwingHigh(self):
        data = data_load(self.symbol, time=timedelta(hours=9))
        return self.swing_high()