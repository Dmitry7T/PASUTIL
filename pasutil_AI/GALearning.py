import matplotlib.pyplot as plt
from GA import GA

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    ga = GA()

    #try:
    plt.ion()
    fig, ax = plt.subplots()
    history = []
    line, = ax.plot([], [])
    print("запуск обучения", flush=True)
    while 1:
        best_model = ga.process()
        history.append(best_model.balance)
        line.set_data(range(len(history)), history)
        plt.draw(), plt.pause(0.001)
        

    #except KeyboardInterrupt:
        #print("остоновка симуляции", flush=True)

if __name__ == "__main__":
    main()