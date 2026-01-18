import random
import numpy as np
import pandas as pd
from pathlib import Path
from functools import partial
from joblib import Parallel, delayed
from progress.bar import IncrementalBar

from NNinput import get_input_data
from trade import Trade

class Simulation:
    def __init__(self):
        # Настройки
        self.window_size = 520    # количество обрабатываемых свечей
        self.commission = 0.0002  # 0.02%
        self.spread = 0.0001      # 1 пип
        self.swap = 0.000002
        self.symbols = ["EURUSDM15", "GBPUSDM15", "GER30MM15", "US30MM15", "US500M15", "USDCHFM15", "USDJPYM15", "XAUUSDM15"] # обучаемые рынки "EURUSDM15", "GBPUSDM15", "GER30MM15", "US30MM15", "US500M15", "USDCHFM15", "USDJPYM15", "XAUUSDM15"
        
    def loadlevel(self):
        filepath = Path("levels/")
        symbol = random.randint(0, len(self.symbols) - 1)
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
    
    def run_simulation(self, num, models = []):
        print("Загрузка data", num, flush=True)
        data = self.loadlevel()
        print("data загружен", num, flush=True)
        print("запуск симуляции", num, flush=True)
        #bar = IncrementalBar('Симуляция', max = len(data) - self.window_size)

        for i in range(0, len(data) - self.window_size):
            raw_data = data.iloc[i:(i + self.window_size)]
            input_data = get_input_data(data= raw_data)
            for model in models:
                if not model.flag: continue

                entry_candle = raw_data.iloc[-1]
                entry_price = entry_candle['close']
                entry_time = entry_candle.name

                # проверка модели
                if len(model.trades) != 0:
                    model.balance = self.check_model(trades= model.trades, entry_candle= entry_candle)
                    if model.balance < 0: 
                        model.balance = 0
                        model.flag = False
                        continue

                    if model.balance < model.min_balance: model.min_balance = model.balance
                    if model.balance > model.max_balance: model.max_balance = model.balance
                if model.flag == False: continue

                # выставление трейда
                output = model.predict(input_data= input_data) # Направление, риск, % роста, % падения
                direction = round(output['signal'].item())
                take_price = entry_price + direction * entry_price * output['growth_predict'].item() 
                stop_price = entry_price - direction * entry_price * output['fall_predict'].item()
                if take_price <= 0 or stop_price <= 0 or output['growth_predict'].item() < 0.00185 or output['fall_predict'].item() < 0.00185: model.fine -= 100; continue
                risk_percent = output['risk_percent'].item() / output['fall_predict'].item()
                RR = output['growth_predict'].item() / entry_price * output['fall_predict'].item()
                model.trades.append(Trade(direction= output['signal'].item(), entry_time = entry_time, risk_percent= risk_percent, entry_balance= model.balance,
                                            entry_price= entry_price, stop_price= stop_price, take_price= take_price, RR= RR))
            #bar.next()
        #bar.finish()
        fitness_scores = [self.fitness(model=model) for model in models]
        print(f"Симуляция {num} - завершена")
        return fitness_scores
        
    def check_model(self, trades, entry_candle):
        entry_price = entry_candle['close']
        entry_low = entry_candle['low']
        entry_high = entry_candle['high']
        entry_time = entry_candle.name
        balance = trades[0].entry_balance; d = 0

        for trade in trades.copy():
            if not trade.is_open: continue
            if trade.direction == -1 and trade.stop_price <= entry_high or trade.direction == 1 and trade.stop_price >= entry_low: # закрытие по сл
                d -= trade.direction * trade.entry_balance * trade.risk_percent * (1 - trade.stop_price / trade.entry_price)
                d -= balance * self.commission
                trade.is_open = False
            elif trade.direction == 1 and trade.take_price <= entry_high or trade.direction == -1 and trade.take_price >= entry_low: # закрытие по тп
                d += trade.direction * trade.entry_balance * trade.risk_percent * (trade.take_price / trade.entry_price - 1)
                d -= balance * self.commission
                trade.is_open = False
            elif trade.direction == 1: d += trade.entry_balance * (entry_price / trade.entry_price - 1) * trade.risk_percent # изменение баланса от трейда 1
            elif trade.direction == -1: d -= trade.entry_balance * (entry_price / trade.entry_price - 1) * trade.risk_percent # изменение баланса от трейда -1

            trade.profit = d
            balance += d
            swaps_count = (entry_time.date() - trade.entry_time.date()).days
            balance -= trade.entry_balance * self.swap * swaps_count
        return balance

    def fitness(self, model):
        trades = model.trades

        if len(trades) < 10:
            return 0.0001
                
        long_count = 0
        short_count = 0
        zero_count = 0
        meanRR = 0
        for trade in trades:
            if trade.direction > 0: 
                long_count += 1
                meanRR += trade.RR
            elif trade.direction < 0: 
                short_count += 1
            else: zero_count += 1


        #if zero_count <= len(trades) * 0.15: return 0.0001
        #if long_count >= len(trades) * 0.99: return 0.0001
        #if short_count >= len(trades) * 0.99: return 0.0001
        meanRR = meanRR / (long_count + short_count)
        if meanRR > 10 or meanRR < 1.1: return 0.0001

        profit = sum(t.profit for t in trades if t.profit > 0)
        loss = abs(sum(t.profit for t in trades if t.profit < 0))
        profit_factor = profit / (loss + 0.0001)

        winrate = sum(1 for t in trades if t.profit > 0) / len(trades)
        winrate_fine = max(0, 1 - abs(winrate - 0.5) * 2)

        loss_persent = 1 - model.const_balance / model.min_balance
        loss_fine = max(0, 1 - loss_persent / 0.20)

        fitness = profit_factor * winrate_fine * loss_fine
        if 1.5 <= meanRR <= 3.0:
            fitness *= 1.2
        if profit_factor < 0.8:  # Слишком убыточно
            fitness *= 0.1
        if loss_persent > 0.50:      # Просадка >50%
            fitness *= 0.01
        return fitness
    
    def simulation(self, models):
        count = 6        
        all_results = Parallel(n_jobs=-1)(
            delayed(self.run_simulation)(i, models=models) 
            for i in range(count)
        )

        result = np.array([sum(values) / count for values in zip(*all_results)]).tolist()
        max_fitness = max(result)
        best_model = models[result.index(max_fitness)]
        print("Лучший результат:", max_fitness)
        print("Результаты: ", result)
        return best_model
        