import numpy as np
import pandas as pd
from pathlib import Path
import random

from NNinput import get_input_data


class Trade:
    def __init__(self, direction, risk_percent, entry_balance, entry_price, stop_price, take_price):
        self.direction = direction         # направление
        self.entry_balance = entry_balance # баланс входа
        self.entry_price = entry_price     # цена входа
        self.risk_percent = risk_percent   # риска от депозита (0.01 = 1%)
        self.stop_price = stop_price       # цена стоп-лосса
        self.take_price = take_price       # цена тейк-профита


class Simulation:
    def __init__(self):
        # Настройки
        self.window_size = 520    # количество обрабатываемых свечей
        self.commission = 0.0002  # 0.02%
        self.spread = 0.0001      # 1 пип
        self.symbols = ["EURUSDM15", "GBPUSDM15", "GER30MM15", "US30MM15", "US500M15", "USDCHFM15", "USDJPYM15", "XAUUSDM15"] # обучаемые рынки
        
    def loadlevel(self):
        filepath = Path("pasutil_AI/levels/")
        symbol = random.randint(0, 7)
        filepath /= self.symbols[symbol]
        file_count = len([item for item in filepath.iterdir() if item.is_file()])
        file = str(random.randint(1, file_count)) + ".csv"
        filepath /= file

        print(f"загружается уровень: {filepath}", flush=True)
        try:
            df = pd.read_csv(filepath, header=None,
                            names=['datetime', 'open', 'high', 'low', 'close'],
                            date_format='%Y.%m.%d %H:%M')
            df['datetime'] = pd.to_datetime(df['datetime'], format='%Y.%m.%d %H:%M')
            df.set_index('datetime', inplace=True)

            df = df.apply(pd.to_numeric, errors='coerce')
            print("уровень загружен", flush=True)
            return df

        except Exception as e:
            print("ошибка загрузки: ", e, flush=True)
    
    def run_simulation(self, models = []):
        print("Загрузка data", flush=True)
        data = self.loadlevel()
        print("data загружен", flush=True)

        print("запуск симуляции", flush=True)
        for i in range(0, len(data) - self.window_size):
            raw_data = data.iloc[i:(i + self.window_size)]
            input_data = get_input_data(data= raw_data)
            for model in models:
                entry_candle = raw_data.iloc[-1]
                entry_price = entry_candle['close']

                # проверка модели
                model.balance = self.check_model(trades= model.trades, balance= model.balance, entry_candle= entry_candle)
                if model.balance <= 10:
                    continue

                # выставление трейда
                output = model.predict(input_data= input_data) # Направление, риск, % роста, % падения
                direction = round(output[0])
                if direction == 0: continue
                take_price = entry_price + direction * entry_price * output[2] 
                stop_price = entry_price - direction * entry_price * output[3]
                if take_price <= 0 or stop_price <=  0: continue
                model.trades.append(Trade(direction= output[0], risk_percent= output[1], entry_balance= model.balance,
                                          entry_price= entry_price, stop_price= stop_price, take_price= take_price))
            
        # выбор лучшей модели
        best_model = models[0]
        for model in models:
            if model.balance > best_model.balance:
                best_model = model
        return best_model

            
        
    def check_model(self, trades, balance, entry_candle):
        entry_price = entry_candle['close']
        entry_low = entry_candle['low']
        entry_high = entry_candle['high']
        for trade in trades.copy():
            if trade.direction == -1 and trade.stop_price <= entry_high or trade.direction == 1 and trade.stop_price >= entry_low: # закрытие по сл
                balance -= trade.entry_balance * trade.risk_percent * (trade.stop_price / trade.entry_price)
                trades.remove(trade)
            elif trade.direction == 1 and trade.take_price <= entry_high or trade.direction == -1 and trade.take_price >= entry_low: # закрытие по тп
                balance += trade.entry_balance * trade.risk_percent * (trade.take_price / trade.entry_price)
                trades.remove(trade)
            elif trade.direction == 1: balance += trade.entry_balance * (entry_price / trade.entry_price) * trade.risk_percent # изменение баланса от трейда 1
            elif trade.direction == -1: balance -= trade.entry_balance * (entry_price / trade.entry_price) * trade.risk_percent # изменение баланса от трейда -1
        return balance
    
    def _calculate_metrics(self, equity_curve, closed_trades, final_balance):
        pass