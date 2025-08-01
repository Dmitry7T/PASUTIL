import MetaTrader5 as mt5
from datetime import datetime, timedelta

def data_load(symbol,
              end_date = datetime.now() + timedelta(hours=3),
              timeframe = mt5.TIMEFRAME_H1):
    start_date = end_date - timedelta(weeks=2)

    # Запрашиваем исторические данные
    rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

    return rates