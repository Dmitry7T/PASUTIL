from NN import SModel
import pandas as pd
from NNinput import get_input_data

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    model = SModel().load_model(path= "c:/Users/User/Desktop/All/Programming/PASUTIL/pasutil_AI/best_model.pth")

    df = pd.read_csv("c:/Users/User/Desktop/All/Programming/PASUTIL/pasutil_AI/levels/GER30MM15/1.csv", header=None,
                    names=['datetime', 'open', 'high', 'low', 'close'],
                    date_format='%Y.%m.%d %H:%M')
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y.%m.%d %H:%M')
    df.set_index('datetime', inplace=True)

    df = df.apply(pd.to_numeric, errors='coerce')
    print("уровень загружен", flush=True)

    i = 20
    raw_data = df.iloc[i:i + 512]
    input_data = get_input_data(data= raw_data)
    output = model.predict(input_data= input_data)
    print(output['signal'].item(), output['risk_percent'].item(), output['growth_predict'].item(), output['fall_predict'].item())
    entry_candle = raw_data.iloc[-1]
    entry_price = entry_candle['close']
    take_price = entry_price + output['signal'].item() * entry_price * output['growth_predict'].item() 
    stop_price = entry_price - output['signal'].item() * entry_price * output['fall_predict'].item()
    print(entry_price, take_price, stop_price)
    if output['growth_predict'].item() < 0.00185 or output['fall_predict'].item() < 0.00185:
        print("NO")
if __name__ == "__main__":
    main()