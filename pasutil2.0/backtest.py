from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from data_load import get_data
from pasutil import Pasutil, TwoCandleStrategy, testStrategy, OrderExecutionStrategy

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(testStrategy)
    data = get_data()
    cerebro.adddata(data)    
    cerebro.broker.setcash(10000)    
    #cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    #cerebro.broker.setcommission(commission=0.001)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue(), '\n', flush=True)

    cerebro.run()

    print('\nFinal Portfolio Value: %.2f' % cerebro.broker.getvalue(), flush=True)

    # Plot the result
    cerebro.plot()