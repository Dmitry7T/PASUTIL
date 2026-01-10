import pandas as pd
import numpy as np
import pandas_ta as ta
from datetime import datetime

def get_input_data(data):
    if data is None or len(data) < 30:
        return np.zeros(30)
    
    df = data.copy()
    features = []
    
    # 1. Технические индикаторы (10)
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
    if not bb.empty and (bb['BBU_20_2.0_2.0'].iloc[-1] != bb['BBL_20_2.0_2.0'].iloc[-1]):
        bb_pos = (df['close'].iloc[-1] - bb['BBL_20_2.0_2.0'].iloc[-1]) / \
                (bb['BBU_20_2.0_2.0'].iloc[-1] - bb['BBL_20_2.0_2.0'].iloc[-1])
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
    
    # Volume (заглушка)
    features.append(1.0)
    
    # 2. Ценовая структура (10)
    last = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else last
    
    # Body ratio
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
    
    # Gap
    gap_pct = (last['open'] - prev['close']) / prev['close'] if prev['close'] != 0 else 0
    features.append(gap_pct)
    
    # Momentum 10
    mom = df['close'].iloc[-1] / df['close'].iloc[-11] - 1 if len(df) >= 11 else 0
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
    
    # Price position (день = 96 свечей 15м)
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
    
    # 3. Время и контекст (10)
    dt = df.index[-1]
    
    # Циклическое время
    hour = dt.hour + dt.minute / 60.0
    hour_rad = 2 * np.pi * hour / 24
    features.append(np.sin(hour_rad))
    features.append(np.cos(hour_rad))
    
    # День недели
    weekday = dt.weekday()
    weekday_rad = 2 * np.pi * weekday / 7
    features.append(np.sin(weekday_rad))
    features.append(np.cos(weekday_rad))
    
    # Сессии
    features.append(1.0 if 8 <= hour < 16 else 0.0)      # Лондон
    features.append(1.0 if 13 <= hour < 22 else 0.0)     # Нью-Йорк
    features.append(1.0 if (8 <= hour < 10) or (14 <= hour < 16) else 0.0)  # Перекрытие
    
    # Дни
    features.append(1.0 if weekday == 4 else 0.0)        # Пятница
    features.append(1.0 if dt.day >= 28 else 0.0)        # Конец месяца
    
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
    
    # Гарантируем 30 признаков
    if len(features) < 30:
        features.extend([0.0] * (30 - len(features)))
    elif len(features) > 30:
        features = features[:30]
    
    return np.array(features)    