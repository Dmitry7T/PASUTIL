import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime

class TradingFeatureExtractor30:
    """Извлекает 30 признаков из ваших данных формата"""
    
    def __init__(self, lookback=100):
        self.lookback = lookback
        self.data = None
        
    def load_data(self, filepath):
        """Загружает данные из CSV с вашим форматом"""
        # Читаем данные
        raw_data = pd.read_csv(filepath)
        
        # Преобразуем время
        raw_data['datetime'] = pd.to_datetime(
            raw_data['date'], 
            format='%Y.%m.%d %H:%M', 
            errors='coerce'
        )
        
        # Удаляем строки с ошибками времени
        raw_data = raw_data.dropna(subset=['datetime'])
        
        # Приводим колонки к нижнему регистру
        raw_data.columns = [col.lower() for col in raw_data.columns]
        
        # Устанавливаем время как индекс
        raw_data.set_index('datetime', inplace=True)
        
        # Оставляем только нужные колонки
        required_cols = ['open', 'high', 'low', 'close']
        missing = [col for col in required_cols if col not in raw_data.columns]
        
        if missing:
            raise ValueError(f"Отсутствуют колонки: {missing}")
        
        self.data = raw_data[required_cols].tail(self.lookback)
        
        print(f"Загружено {len(self.data)} свечей")
        print(f"Диапазон: {self.data.index.min()} - {self.data.index.max()}")
        
        return self.data
    
    def get_30_features(self):
        """Возвращает 30 признаков для текущего момента"""
        if self.data is None or len(self.data) < 30:
            print("Недостаточно данных (нужно минимум 30 свечей)")
            return np.zeros(30)
        
        df = self.data.copy()
        features = []
        
        # 1. ТЕХНИЧЕСКИЕ ИНДИКАТОРЫ (10)
        try:
            # RSI
            rsi_val = ta.rsi(df['close'], length=14).iloc[-1]
            features.append(rsi_val / 100 if not pd.isna(rsi_val) else 0.5)
            
            # MACD гистограмма
            macd = ta.macd(df['close'])
            macd_hist = macd['MACDh_12_26_9'].iloc[-1] if not macd.empty else 0
            features.append(macd_hist * 100)
            
            # ATR
            atr_val = ta.atr(df['high'], df['low'], df['close'], length=14).iloc[-1]
            features.append(atr_val)
            features.append(atr_val / df['close'].iloc[-1] if df['close'].iloc[-1] > 0 else 0)
            
            # Bollinger позиция
            bb = ta.bbands(df['close'], length=20)
            if not bb.empty and (bb['BBU_20_2.0'].iloc[-1] != bb['BBL_20_2.0'].iloc[-1]):
                bb_pos = (df['close'].iloc[-1] - bb['BBL_20_2.0'].iloc[-1]) / \
                        (bb['BBU_20_2.0'].iloc[-1] - bb['BBL_20_2.0'].iloc[-1])
                features.append(max(0, min(1, bb_pos)))
            else:
                features.append(0.5)
            
            # Stochastic
            stoch = ta.stoch(df['high'], df['low'], df['close'])
            features.append(stoch['STOCHk_14_3_3'].iloc[-1] / 100 if not stoch.empty else 0.5)
            features.append(stoch['STOCHd_14_3_3'].iloc[-1] / 100 if not stoch.empty else 0.5)
            
            # ADX
            adx_val = ta.adx(df['high'], df['low'], df['close'], length=14)['ADX_14'].iloc[-1]
            features.append(adx_val / 100 if not pd.isna(adx_val) else 0.25)
            
            # CCI
            cci_val = ta.cci(df['high'], df['low'], df['close'], length=20).iloc[-1]
            features.append(cci_val / 100 if not pd.isna(cci_val) else 0)
            
            # Заглушка для объема (если нет колонки volume)
            features.append(1.0)  # volume_ratio
            
        except Exception as e:
            print(f"Ошибка расчета индикаторов: {e}")
            features.extend([0.5] * 10)  # Заполняем нулями
        
        # 2. ЦЕНОВАЯ СТРУКТУРА (10)
        try:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            
            # Body to range ratio
            candle_range = last['high'] - last['low']
            if candle_range > 0:
                features.append(abs(last['close'] - last['open']) / candle_range)
            else:
                features.append(0.0)
            
            # Hammer
            body = abs(last['close'] - last['open'])
            lower_wick = min(last['open'], last['close']) - last['low']
            upper_wick = last['high'] - max(last['open'], last['close'])
            is_hammer = 1.0 if (lower_wick > 2*body and upper_wick < body*0.5 and body > 0) else 0.0
            features.append(is_hammer)
            
            # Doji
            is_doji = 1.0 if body < candle_range * 0.1 and candle_range > 0 else 0.0
            features.append(is_doji)
            
            # Gap %
            if prev['close'] != 0:
                gap_pct = (last['open'] - prev['close']) / prev['close']
            else:
                gap_pct = 0
            features.append(gap_pct)
            
            # Momentum 10
            if len(df) >= 11:
                mom = df['close'].iloc[-1] / df['close'].iloc[-11] - 1
            else:
                mom = 0
            features.append(mom)
            
            # High/Low ratio 5
            if len(df) >= 5:
                high_5 = df['high'].iloc[-5:].max()
                low_5 = df['low'].iloc[-5:].min()
                if high_5 != low_5:
                    features.append((high_5 - df['close'].iloc[-1]) / (high_5 - low_5))
                else:
                    features.append(0.5)
            else:
                features.append(0.5)
            
            # Price position today (упрощенно - последние 96 свечей = 1 день для 15м)
            if len(df) >= 96:
                day_high = df['high'].iloc[-96:].max()
                day_low = df['low'].iloc[-96:].min()
                if day_high != day_low:
                    features.append((df['close'].iloc[-1] - day_low) / (day_high - day_low))
                else:
                    features.append(0.5)
            else:
                features.append(0.5)
            
            # Fractal count
            fractal_count = 0
            for i in range(2, min(7, len(df)-2)):
                if df['high'].iloc[i] > df['high'].iloc[i-2:i].max() and \
                   df['high'].iloc[i] > df['high'].iloc[i+1:i+3].max():
                    fractal_count += 1
            features.append(fractal_count / 5)
            
            # Candle sequence
            seq = 0
            if len(df) >= 3:
                for i in range(1, 3):
                    if df['close'].iloc[-i] > df['open'].iloc[-i]:
                        seq += 1
                    elif df['close'].iloc[-i] < df['open'].iloc[-i]:
                        seq -= 1
            features.append(seq / 2)
            
            # Volatility ratio
            if len(df) >= 21:
                atr7 = ta.atr(df['high'], df['low'], df['close'], length=7).iloc[-1]
                atr21 = ta.atr(df['high'], df['low'], df['close'], length=21).iloc[-1]
                features.append(atr7 / atr21 if atr21 > 0 else 1.0)
            else:
                features.append(1.0)
                
        except Exception as e:
            print(f"Ошибка расчета ценовой структуры: {e}")
            features.extend([0.0] * (30 - len(features)))
        
        # 3. ВРЕМЯ И КОНТЕКСТ (10)
        try:
            dt = df.index[-1]
            
            # Циклическое время
            hour = dt.hour + dt.minute / 60.0  # Учитываем минуты
            hour_rad = 2 * np.pi * hour / 24
            features.append(np.sin(hour_rad))
            features.append(np.cos(hour_rad))
            
            # День недели
            weekday = dt.weekday()
            weekday_rad = 2 * np.pi * weekday / 7
            features.append(np.sin(weekday_rad))
            features.append(np.cos(weekday_rad))
            
            # Торговые сессии (GMT)
            features.append(1.0 if 8 <= hour < 16 else 0.0)    # Лондон 8:00-16:00
            features.append(1.0 if 13 <= hour < 22 else 0.0)   # Нью-Йорк 13:00-22:00
            features.append(1.0 if (8 <= hour < 10) or (14 <= hour < 16) else 0.0)  # Перекрытие
            
            # Пятница
            features.append(1.0 if weekday == 4 else 0.0)
            
            # Конец месяца (последние 3 дня)
            features.append(1.0 if dt.day >= 28 else 0.0)
            
            # Рыночный режим
            adx_val = features[7] if len(features) > 7 else 0.25
            atr_ratio = features[19] if len(features) > 19 else 1.0
            if adx_val > 0.4:
                market_regime = 1.0
            elif atr_ratio > 1.2:
                market_regime = 2.0
            else:
                market_regime = 0.0
            features.append(market_regime / 2)
            
        except Exception as e:
            print(f"Ошибка расчета времени: {e}")
            features.extend([0.0] * (30 - len(features)))
        
        # Проверяем длину
        if len(features) != 30:
            print(f"ВНИМАНИЕ: получено {len(features)} признаков вместо 30")
            # Добиваем или обрезаем
            if len(features) < 30:
                features.extend([0.0] * (30 - len(features)))
            else:
                features = features[:30]
        
        return np.array(features)

# ИСПОЛЬЗОВАНИЕ
def main():
    # 1. Создаем экстрактор
    extractor = TradingFeatureExtractor30(lookback=200)
    
    # 2. Загружаем данные (замените 'your_data.csv' на ваш файл)
    try:
        data = extractor.load_data('pasutil_AI/levels/EURUSDM15/1.csv')
    except FileNotFoundError:
        print("Создаем тестовые данные...")
        # Создаем тестовые данные если файла нет
        dates = pd.date_range(start='2024-01-01', periods=200, freq='15min')
        test_data = pd.DataFrame({
            'open': np.random.randn(200).cumsum() + 1.1,
            'high': np.random.randn(200).cumsum() + 1.12,
            'low': np.random.randn(200).cumsum() + 1.08,
            'close': np.random.randn(200).cumsum() + 1.1
        }, index=dates)
        
        # Сохраняем в формате как у вас
        test_data_reset = test_data.reset_index()
        test_data_reset['date'] = test_data_reset['index'].dt.strftime('%Y.%m.%d %H:%M')
        test_data_reset[['date', 'open', 'high', 'low', 'close']].to_csv('test_data.csv', index=False)
        
        print("Создан test_data.csv с тестовыми данными")
        data = extractor.load_data('pasutil_AI/levels/EURUSDM15/1.csv')
    
    # 3. Получаем признаки
    features = extractor.get_30_features()
    
    # 4. Выводим результат
    print(f"\nПолучено {len(features)} признаков:")
    print("Первые 10 значений:")
    for i, val in enumerate(features[:10]):
        print(f"  {i+1}: {val:.6f}")
    
    print("\nСтатистика по признакам:")
    print(f"  Min: {features.min():.6f}")
    print(f"  Max: {features.max():.6f}")
    print(f"  Mean: {features.mean():.6f}")
    print(f"  NaN значений: {np.isnan(features).sum()}")
    
    return features

if __name__ == "__main__":
    features = main()