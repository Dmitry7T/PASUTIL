import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()
else:
    print('Подключение установлено')
    
def get_symbols(group_name):
    symbols = mt5.symbols_get()
    return [s for s in symbols if group_name.lower() in s.path.lower()]

forex_symbols = get_symbols('forex'); forex_symbols = [s.name for s in forex_symbols[::]]
crypto_symbols = get_symbols('crypto'); crypto_symbols = [s.name for s in crypto_symbols[::]]
index_symbols = get_symbols('index'); index_symbols = [s.name for s in index_symbols[::]]

print(forex_symbols)
print(crypto_symbols)
print(index_symbols)