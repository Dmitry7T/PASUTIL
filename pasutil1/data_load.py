import MetaTrader5 as mt5
from datetime import datetime, timedelta

def data_load(symbol,
              end_date = datetime.now() + timedelta(hours=3),
              timeframe = mt5.TIMEFRAME_M30):
    start_date = end_date - timedelta(hours=8, minutes=30)

    # Запрашиваем исторические данные
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

    return rates