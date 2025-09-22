import backtrader as bt

def get_data():
    data = bt.feeds.GenericCSVData(
        dataname='EURUSD_M15.csv',  
        # Параметры для правильного парсинга
        dtformat='%Y-%m-%d %H:%M:%S',  # Формат даты/времени
        datetime=0,  # Колонка с datetime
        open=1,      # Колонка с open
        high=2,      # Колонка с high
        low=3,       # Колонка с low
        close=4,     # Колонка с close
        volume=5,    # Колонка с volume
        openinterest=6,  # Колонка с openinterest
        separator=',',   # Разделитель - запятая
        timeframe=bt.TimeFrame.Minutes,  # Таймфрейм
        compression=15   # 15 минут
    )
    return data