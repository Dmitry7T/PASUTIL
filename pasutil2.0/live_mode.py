import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import backtrader as bt
import MetaTrader5 as mt5
import datetime
from pasutil import UnifiedTradingStrategy


def run_live_trading():
    cerebro = bt.Cerebro()
    
    # Настройка соединения с MT5
    from backtrader_mt5 import MT5Store
    store = MT5Store()
    
    # Получение данных в реальном времени
    data = store.getdata(dataname='EURUSD', timeframe=bt.TimeFrame.Minutes, compression=15)
    cerebro.adddata(data)
    
    # Добавляем стратегию
    cerebro.addstrategy(UnifiedTradingStrategy, use_mt=True)
    
    # Начальный капитал (будет взят из брокера)
    cerebro.broker.setcash(10000.0)
    
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    try:
        cerebro.run()
    except KeyboardInterrupt:
        print("Trading stopped by user")
    
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    run_live_trading()