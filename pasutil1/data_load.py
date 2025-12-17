import MetaTrader5 as mt5
from datetime import datetime, timedelta

def data_load(symbol,
              end_date = datetime.now(), time = timedelta(),
              timeframe = mt5.TIMEFRAME_M30):
    start_date = end_date - time

    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
    if rates is None:
        return rates
    else:
        rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 100)
        return rates