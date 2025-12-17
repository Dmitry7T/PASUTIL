import MetaTrader5 as mt5
from pasutil_graphmaker.graph import Graph
from pasutil1.Strategies import TestStrategy as Strategy
from pasutil1.data_load import data_load

if not mt5.initialize():
    print("initialize() failed", flush=True)
    mt5.shutdown()
else:
    print('Connection complete', flush=True)


def backtest():
    graph = Graph()
    data = data_load("EURUSD")
    graph.load(data)







    graph.exit()

if __name__ == "__main__":
    backtest()