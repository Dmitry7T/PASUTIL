import pandas as pd

# Читаем исходный файл
df = pd.read_csv('XAUUSD_M15.csv', sep='\t')

# Преобразуем дату и время
df['datetime'] = pd.to_datetime(df['<DATE>'] + ' ' + df['<TIME>'])

# Создаем новый DataFrame в нужном формате
new_df = pd.DataFrame({
    'datetime': df['datetime'],
    'open': df['<OPEN>'],
    'high': df['<HIGH>'],
    'low': df['<LOW>'],
    'close': df['<CLOSE>'],
    'volume': df['<TICKVOL>'],
    'openinterest': 0
})

# Сохраняем в новый CSV
new_df.to_csv('converted_for_backtrader.csv', index=False)