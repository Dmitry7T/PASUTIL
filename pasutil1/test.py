# mt5_rest_client.py
import requests
import time
import json
import logging
from datetime import datetime

class MT5RESTClient:
    def __init__(self, login, password, server, host="https://mt5-api.mql5.com"):
        self.host = host
        self.login = login
        self.password = password
        self.server = server
        self.token = None
        self.session = requests.Session()
        
    def authenticate(self):
        """Аутентификация на сервере MT5"""
        url = f"{self.host}/api/auth/login"
        payload = {
            "login": self.login,
            "password": self.password,
            "server": self.server
        }
        
        try:
            response = self.session.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                print("Аутентификация успешна")
                return True
            else:
                print(f"Ошибка аутентификации: {response.status_code}")
                return False
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def get_symbols(self):
        """Получить список символов"""
        if not self.token:
            print("Необходима аутентификация")
            return None
            
        url = f"{self.host}/api/symbols"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        response = self.session.get(url, headers=headers)
        return response.json() if response.status_code == 200 else None
    
    def get_ticks(self, symbol, count=100):
        """Получить тики для символа"""
        if not self.token:
            print("Необходима аутентификация")
            return None
            
        url = f"{self.host}/api/ticks/{symbol}"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"count": count}
        
        response = self.session.get(url, headers=headers, params=params)
        if response.status_code == 200:
            ticks = response.json()
            # Конвертируем timestamp в читаемый формат
            for tick in ticks:
                if 'time' in tick:
                    tick['time_str'] = datetime.fromtimestamp(tick['time']).strftime('%Y-%m-%d %H:%M:%S')
            return ticks
        else:
            print(f"Ошибка получения тиков: {response.status_code}")
            return None
    
    def get_bars(self, symbol, timeframe="M1", count=100):
        """Получить свечи для символа"""
        if not self.token:
            print("Необходима аутентификация")
            return None
            
        url = f"{self.host}/api/bars/{symbol}/{timeframe}"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"count": count}
        
        response = self.session.get(url, headers=headers, params=params)
        return response.json() if response.status_code == 200 else None

# Пример использования
def example_usage():
    # Конфигурация (замените на свои данные)
    client = MT5RESTClient(
        login="ваш_логин",
        password="ваш_пароль",
        server="ваш_сервер"
    )
    
    # Аутентификация
    if client.authenticate():
        print("=" * 50)
        print("Успешно подключено к MT5")
        print("=" * 50)
        
        # Получаем список символов
        symbols = client.get_symbols()
        if symbols:
            print(f"Доступно символов: {len(symbols)}")
        
        # Получаем тики для EURUSD
        print("\nПолучаю тики для EURUSD...")
        ticks = client.get_ticks("EURUSD", count=10)
        if ticks:
            for tick in ticks[-5:]:  # Последние 5 тиков
                print(f"Время: {tick.get('time_str')}, "
                      f"Bid: {tick.get('bid')}, "
                      f"Ask: {tick.get('ask')}")
        
        # Получаем свечи
        print("\nПолучаю свечи для GBPUSD...")
        bars = client.get_bars("GBPUSD", "M15", count=5)
        if bars:
            for bar in bars:
                print(f"Время: {bar.get('time')}, "
                      f"Open: {bar.get('open')}, "
                      f"High: {bar.get('high')}, "
                      f"Low: {bar.get('low')}, "
                      f"Close: {bar.get('close')}")

# Автоматическое обновление данных
def auto_update_data():
    client = MT5RESTClient("логин", "пароль", "сервер")
    
    if client.authenticate():
        while True:
            try:
                ticks = client.get_ticks("EURUSD", count=1)
                if ticks and len(ticks) > 0:
                    last_tick = ticks[-1]
                    print(f"{datetime.now().strftime('%H:%M:%S')} - "
                          f"EURUSD: Bid={last_tick.get('bid')}, "
                          f"Ask={last_tick.get('ask')}")
                
                # Обновляем каждые 10 секунд
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\nЗавершение работы...")
                break
            except Exception as e:
                print(f"Ошибка: {e}")
                time.sleep(30)  # Ждем перед повторной попыткой

if __name__ == "__main__":
    # Запустите один из примеров
    example_usage()
    # или
    # auto_update_data()