class Trade:
    def __init__(self, direction, entry_time, risk_percent, entry_balance, entry_price, stop_price, take_price, RR):
        self.entry_time = entry_time       # врямя входа 
        self.direction = direction         # направление
        self.entry_balance = entry_balance # баланс входа
        self.entry_price = entry_price     # цена входа
        self.risk_percent = risk_percent   # риска от депозита (0.01 = 1%)
        self.stop_price = stop_price       # цена стоп-лосса
        self.take_price = take_price       # цена тейк-профита
        self.RR = RR
        self.is_open = True
        # fitness
        self.profit = 0

    def log(self):
        print("direction: ", self.direction, flush=True)
        print("entry_balance: ", self.entry_balance, flush=True)
        print("entry_price: ", self.entry_price, flush=True)
        print("risk_percent: ", self.risk_percent, flush=True)
        print("stop_price: ", self.stop_price, flush=True)
        print("take_price: ", self.take_price, flush=True)