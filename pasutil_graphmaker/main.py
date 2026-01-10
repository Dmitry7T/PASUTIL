import sys
import pandas as pd
import numpy as np
from PySide6.QtWidgets import *
from PySide6.QtCore import QTimer, Qt
import pyqtgraph as pg
from random import gauss
from collections import deque

class CandlestickItem(pg.GraphicsObject):
    """Кастомный графический элемент для отрисовки японских свечей"""
    
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.data = data  # данные в формате: [time, open, high, low, close]
        self.generatePicture()
    
    def generatePicture(self):
        self.picture = pg.QtGui.QPicture()
        p = pg.QtGui.QPainter(self.picture)
        
        # Настройки цветов и толщины
        w = 0.6  # ширина свечи
        pen_white = pg.mkPen('w')  # контур
        
        for (time, open, high, low, close) in self.data:
            # Определяем цвет свечи
            if open < close:
                # Бычья свеча (зеленая)
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))
            else:
                # Медвежья свеча (красная)
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            
            # Рисуем тело свечи
            p.drawRect(pg.QtCore.QRectF(time - w/2, min(open, close), w, abs(close-open)))
            
            # Рисуем тени
            p.setPen(pg.mkPen('k'))  # черный цвет для теней
            p.drawLine(pg.QtCore.QPointF(time, low), pg.QtCore.QPointF(time, high))
        
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        return pg.QtCore.QRectF(self.picture.boundingRect())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Algorithm Debug Terminal - Candlestick")
        self.setGeometry(100, 100, 1600, 900)

        # Инициализация данных для свечей
        self.candle_data = []  # формат: [time, open, high, low, close]
        self.current_time = 0
        
        # Создаем центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # --- Создаем график для свечей ---
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.setTitle("Candlestick Chart", color='b', size='20pt')
        self.graph_widget.setLabel('left', 'Price', color='red')
        self.graph_widget.setLabel('bottom', 'Time', color='red')
        self.graph_widget.addLegend()
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)

        # Элемент для свечей
        self.candlestick_item = None

        layout.addWidget(self.graph_widget, 3)

        # --- Создаем правую панель ---
        right_panel = QVBoxLayout()

        # Кнопки управления
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.add_candle_btn = QPushButton("Add Random Candle")
        self.stop_btn.setEnabled(False)

        right_panel.addWidget(self.start_btn)
        right_panel.addWidget(self.stop_btn)
        right_panel.addWidget(self.add_candle_btn)

        # Таблица для отображения последних свечей
        self.table = QTableWidget(5, 6)
        self.table.setHorizontalHeaderLabels(["Time", "Open", "High", "Low", "Close", "Type"])
        right_panel.addWidget(QLabel("Last Candles:"))
        right_panel.addWidget(self.table)

        # Лог
        right_panel.addWidget(QLabel("Log:"))
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        right_panel.addWidget(self.log_text)

        # Добавляем правую панель в основной layout
        panel_widget = QWidget()
        panel_widget.setLayout(right_panel)
        layout.addWidget(panel_widget, 1)

        # --- Таймер для имитации обновления данных ---
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_candles)
        self.counter = 0

        # --- Подключаем сигналы кнопок ---
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.add_candle_btn.clicked.connect(self.add_random_candle)

        self.log("Application started. Ready to display candlesticks.")

    def start(self):
        self.timer.start(500)  # Обновление каждые 500 мс
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log("Candlestick stream started.")

    def stop(self):
        self.timer.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log("Candlestick stream stopped.")

    def add_random_candle(self):
        """Добавляет случайную свечу (для демонстрации)"""
        self.current_time += 1
        base_price = 100
        
        # Генерируем случайные значения для OHLC
        open_price = base_price + np.random.normal(0, 2)
        close_price = open_price + np.random.normal(0, 1)
        high_price = max(open_price, close_price) + abs(np.random.normal(0, 1))
        low_price = min(open_price, close_price) - abs(np.random.normal(0, 1))
        
        new_candle = [self.current_time, open_price, high_price, low_price, close_price]
        self.candle_data.append(new_candle)
        
        # Ограничиваем количество отображаемых свечей
        if len(self.candle_data) > 50:
            self.candle_data.pop(0)
        
        self.update_candlestick_chart()
        self.update_candle_table(new_candle)
        
        candle_type = "BULL" if open_price < close_price else "BEAR"
        self.log(f"Added candle: Time={self.current_time}, O={open_price:.2f}, H={high_price:.2f}, L={low_price:.2f}, C={close_price:.2f} ({candle_type})")

    def update_candles(self):
        """Автоматическое добавление свечей по таймеру"""
        self.add_random_candle()

    def update_candlestick_chart(self):
        """Обновляет свечной график"""
        if self.candle_data:
            # Очищаем предыдущие свечи
            self.graph_widget.clear()
            
            # Создаем новый свечной элемент
            self.candlestick_item = CandlestickItem(self.candle_data)
            self.graph_widget.addItem(self.candlestick_item)
            
            # Автоматическое масштабирование
            if len(self.candle_data) > 1:
                times = [c[0] for c in self.candle_data]
                lows = [c[3] for c in self.candle_data]
                highs = [c[2] for c in self.candle_data]
                
                self.graph_widget.setXRange(min(times), max(times))
                self.graph_widget.setYRange(min(lows) * 0.999, max(highs) * 1.001)

    def update_candle_table(self, candle):
        """Обновляет таблицу последними свечами"""
        time, open_price, high_price, low_price, close_price = candle
        candle_type = "BULL" if open_price < close_price else "BEAR"
        
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem(str(time)))
        self.table.setItem(0, 1, QTableWidgetItem(f"{open_price:.2f}"))
        self.table.setItem(0, 2, QTableWidgetItem(f"{high_price:.2f}"))
        self.table.setItem(0, 3, QTableWidgetItem(f"{low_price:.2f}"))
        self.table.setItem(0, 4, QTableWidgetItem(f"{close_price:.2f}"))
        self.table.setItem(0, 5, QTableWidgetItem(candle_type))
        
        # Удаляем старые строки
        if self.table.rowCount() > 5:
            self.table.removeRow(self.table.rowCount() - 1)

    def load_mt5_candles(self, mt5_candles_array):
        """Загружает данные из MetaTrader 5"""
        self.log("Loading MT5 candles...")
        
        # Очищаем текущие данные
        self.candle_data = []
        self.current_time = 0
        
        # Конвертируем данные MT5 в наш формат
        for i in range(len(mt5_candles_array)):
            # Предполагаем, что данные MT5 содержат time, open, high, low, close
            # Возможно, вам нужно адаптировать эту часть под ваш конкретный формат
            candle = mt5_candles_array[i]
            time = i
            open_price = candle['open']
            high_price = candle['high']
            low_price = candle['low']
            close_price = candle['close']
            
            candle = [time, open_price, high_price, low_price, close_price]
            self.candle_data.append(candle)
            self.current_time = time
        
        self.update_candlestick_chart()
        self.log(f"Loaded {len(self.candle_data)} candles from MT5")

    def log(self, message):
        """Добавляет сообщение в лог"""
        self.log_text.append(f"[{self.counter}] {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    # Пример: как бы вы использовали данные из MT5
    # Предположим, у вас есть функция get_mt5_candles(), которая возвращает массив свечей
    # mt5_candles = your_mt5_connection.get_candles("EURUSD", mt5.TIMEFRAME_M15, 100)

    
    sys.exit(app.exec())