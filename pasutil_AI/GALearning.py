from GA import GA

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    ga = GA(population= 30, mutation_rate=0.5, mutation_strength=0.5) # mutation_rate=0.5, mutation_strength=0.5

    try:
        print("запуск обучения", flush=True)
        i = 1
        while 1:
            print('=' * 50)
            print("Поколение", i)
            best_model = ga.process()
            i += 1
        

    except KeyboardInterrupt:
        print("остоновка симуляции", flush=True)

if __name__ == "__main__":
    main()