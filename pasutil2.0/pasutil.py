import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import datetime
point = 0.00001

# Create a Stratey
class Pasutil(bt.Strategy):
    params = (
        ('limit_buy_price', None),
        ('stop_loss_price', None),
        ('take_profit_price', None),
    )

    def __init__(self):
        self.candle_data = []
        self.entry_order = None  # Ордер на вход
        self.stop_order = None   # Стоп-лосс ордер
        self.take_order = None   # Тейк-профит ордер
        self.stop_placed = False


    def next(self):
        if len(self.data_close) == 0:
            print('отсутствуют данные')
            return  
        
        #print(1, flush=True)
        if self.type(0) and self.type(-1):
            if (self.data.close[0] > self.data.high[-1]):
                #self.log(f'self.data.close[0] {self.data.close[0]}, {self.type(0)}', bt.num2date(self.data.datetime[0]))
                #self.log(f'self.data.high[-1] {self.data.high[-1]}, {self.type(-1)}, {bt.num2date(self.data.datetime[-1])}')

                self.params.limit_buy_price = self.data.low[0]
                self.params.stop_loss_price = self.params.limit_buy_price - point * 300
                self.params.take_profit_price = self.params.limit_buy_price + point * 300 * 3

                if not self.position and not self.entry_order:
                    # Ордер на покупку (вход)
                    self.entry_order = self.buy(
                        exectype=bt.Order.Limit,
                        price=self.params.limit_buy_price,
                        valid=None,
                        size= 10,
                    )
                    self.stop_placed = False
                '''self.order = self.buy(
                    exectype=bt.Order.Limit,
                    price=limit_buy_price,
                    valid=None,  # действует до отмены (Good-Till-Canceled)
                    
                    stopprice=stop_loss_price,   # стоп-лосс
                    stopexec=bt.Order.Stop,     # тип стоп-ордера
                    
                    limitprice=take_profit_price,  # тейк-профит
                    limitexec=bt.Order.Limit,     # тип лимитного ордера (тейк)
                    size= 10,
                    oco=None 
                    )'''
                
                #print("take ", self.params.take_profit_price)
                #print("stop ", self.params.stop_loss_price)

        if self.position and not self.stop_placed and not self.stop_order:
            # Ордер на продажу (стоп-лосс)
            self.stop_order = self.sell(
                exectype=bt.Order.StopTrail,
                price=self.params.stop_loss_price,
                trailamount=0
            )
            self.stop_placed = True
            print("Стоп-лосс выставлен")

    def notify_order(self, order):
        if order.status == order.Completed:
            if order == self.entry_order:
                self.log(f'Входной ордер исполнен', bt.num2date(self.data.datetime[0]))
                self.entry_order = None
            elif order == self.stop_order:
                self.log(f'Стоп-лосс сработал', bt.num2date(self.data.datetime[0]))
                self.stop_order = None
            #self.orders_placed = False

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt), flush=True)

    def cancel_all_orders(self):
        for order in self.broker.get_orders_open():
            self.broker.cancel(order)
            print(f"Отменён ордер: {order.ref}")

    def stop(self):
        if self.broker.get_orders_open():
            print("Завершение симуляции - отмена всех активных ордеров")
        self.cancel_all_orders()
        print(f"Всего обработано свечей: {len(self.data)}")

    def type(self, index):
        return 1 if self.data.close[index] > self.data.open[index] else 0

class TwoCandleStrategy(bt.Strategy):
    params = (
        ('stop_loss', 300),  # стоп-лосс в пунктах
        ('risk_reward', 8),  # соотношение тейк-профит/стоп-лосс
    )

    def is_bullish(self, index):
        """Проверяет, является ли свеча бычьей"""
        return self.data.close[index] > self.data.open[index]

    def is_bearish(self, index):
        """Проверяет, является ли свеча медвежьей"""
        return self.data.close[index] < self.data.open[index]

    def __init__(self):
        # Для отслеживания свечей
        self.candle_data = []
        self.order = None
        
    def next(self):
        if self.order:
            return
        
        # Сохраняем последние 2 свечи
        if len(self.candle_data) < 2:
            self.candle_data.append(self.data.close[0])
            return
          
        # Обновляем данные свечей (храним последние 2)
        self.candle_data = [self.data.close[-1], self.data.close[0]]
        
        # Проверяем условия для покупки
        if self.is_bullish(-2) and self.is_bullish(-1):
            if self.data.high[-1] < self.data.close[-2]: 
                # Цена входа - минимум первой свечи (справа)
                entry_price = self.data.low[-2]
                stop_loss = entry_price - self.p.stop_loss * point
                take_profit = entry_price + (self.p.stop_loss * self.p.risk_reward) * point
                print(1, flush=True) 
                # Выставляем ордер на покупку
                self.buy(   exectype=bt.Order.Limit, price=entry_price, 
                            stopprice=stop_loss, limitprice=take_profit,
                            size = 1,
                            #valid=bt.num2date(bt.date2num(datetime.now()) + timedelta(hours=8))
                         )
        
        # Проверяем условия для продажи
        elif self.is_bearish(-2) and self.is_bearish(-1):
            if self.data.close[-2] < self.data.low[-1]:
                print(2, flush=True)  
                # Цена входа - максимум первой свечи (справа)
                entry_price = self.data.high[-2]
                stop_loss = entry_price + self.p.stop_loss * point
                take_profit = entry_price - (self.p.stop_loss * self.p.risk_reward) * point
                
                # Выставляем ордер на продажу
                self.sell(  exectype=bt.Order.Limit, price=entry_price, 
                            stopprice=stop_loss, limitprice=take_profit,
                            size = 1,
                            #valid=bt.num2date(bt.date2num(datetime.now()) + timedelta(hours=8))
                         )
                
class testStrategy(bt.Strategy):
    params = (
        ('valid', 4),
        ('exectype', 'Limit'),
        ('perc1', 1),
    )

    def __init__(self):
        self.candle_data = []

    def next(self):
        if self.p.valid:
            valid = self.data.datetime.date(0) + \
                    datetime.timedelta(days=self.p.valid)
        else:
            valid = None

        if self.p.exectype == 'Limit':
            price = self.data.close * (1.0 - self.p.perc1 / 100.0)

            self.buy(exectype=bt.Order.Limit, price=price, valid=valid)

            if self.p.valid:
                txt = 'BUY CREATE, exectype Limit, price %.2f, valid: %s'
                self.log(txt % (price, valid.strftime('%Y-%m-%d')))
            else:
                txt = 'BUY CREATE, exectype Limit, price %.2f'
                self.log(txt % price)


    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt), flush=True)

    def stop(self):
        print()
        if self.broker.get_orders_open(): 
            print("отмена всех активных ордеров")
            count = len(self.broker.get_orders_open())
            self.cancel_all_orders()
            print(f'отмененино ордеров {count}')
        print(f"Всего обработано свечей: {len(self.data)}")

    def cancel_all_orders(self):
        for order in self.broker.get_orders_open():
            self.broker.cancel(order)
            #print(f"Отменён ордер: {order.ref}")

class OrderExecutionStrategy(bt.Strategy):
    params = (
        ('smaperiod', 15),
        ('exectype', 'Market'),
        ('perc1', 3),
        ('perc2', 1),
        ('valid', 4),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.data.datetime[0]
        if isinstance(dt, float):
            dt = bt.num2date(dt)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            self.log('ORDER ACCEPTED/SUBMITTED', dt=order.created.dt)
            self.order = order
            return

        if order.status in [order.Expired]:
            self.log('BUY EXPIRED')

        elif order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

        # Sentinel to None: new orders allowed
        self.order = None

    def __init__(self):
        # SimpleMovingAverage on main data
        # Equivalent to -> sma = btind.SMA(self.data, period=self.p.smaperiod)
        sma = btind.SMA(period=self.p.smaperiod)

        # CrossOver (1: up, -1: down) close / sma
        self.buysell = btind.CrossOver(self.data.close, sma, plot=True)

        # Sentinel to None: new ordersa allowed
        self.order = None

    def next(self):
        if self.order:
            # An order is pending ... nothing can be done
            return

        # Check if we are in the market
        if self.position:
            # In the maerket - check if it's the time to sell
            if self.buysell < 0:
                self.log('SELL CREATE, %.2f' % self.data.close[0])
                self.sell()

        elif self.buysell > 0:
            if self.p.valid:
                valid = self.data.datetime.date(0) + \
                        datetime.timedelta(days=self.p.valid)
            else:
                valid = None

            # Not in the market and signal to buy
            if self.p.exectype == 'Market':
                self.buy(exectype=bt.Order.Market)  # default if not given

                self.log('BUY CREATE, exectype Market, price %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Close':
                self.buy(exectype=bt.Order.Close)

                self.log('BUY CREATE, exectype Close, price %.2f' %
                         self.data.close[0])

            elif self.p.exectype == 'Limit':
                price = self.data.close * (1.0 - self.p.perc1 / 100.0)

                self.buy(exectype=bt.Order.Limit, price=price, valid=valid)

                if self.p.valid:
                    txt = 'BUY CREATE, exectype Limit, price %.2f, valid: %s'
                    self.log(txt % (price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Limit, price %.2f'
                    self.log(txt % price)

            elif self.p.exectype == 'Stop':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)

                self.buy(exectype=bt.Order.Stop, price=price, valid=valid)

                if self.p.valid:
                    txt = 'BUY CREATE, exectype Stop, price %.2f, valid: %s'
                    self.log(txt % (price, valid.strftime('%Y-%m-%d')))
                else:
                    txt = 'BUY CREATE, exectype Stop, price %.2f'
                    self.log(txt % price)

            elif self.p.exectype == 'StopLimit':
                price = self.data.close * (1.0 + self.p.perc1 / 100.0)

                plimit = self.data.close * (1.0 + self.p.perc2 / 100.0)

                self.buy(exectype=bt.Order.StopLimit, price=price, valid=valid,
                         plimit=plimit)

                if self.p.valid:
                    txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
                           ' valid: %s, pricelimit: %.2f')
                    self.log(txt % (price, valid.strftime('%Y-%m-%d'), plimit))
                else:
                    txt = ('BUY CREATE, exectype StopLimit, price %.2f,'
                           ' pricelimit: %.2f')
                    self.log(txt % (price, plimit))