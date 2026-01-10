# date open High Low Close
import os
import pandas as pd
from pathlib import Path

def create_subtables():
    # Определяем пути
    current_dir = Path(__file__).parent  # Папка levels
    data_dir = current_dir.parent / "data"  # Папка data
    output_base_dir = current_dir  # Папка levels для сохранения
    
    # Проверяем существование папки data
    if not data_dir.exists():
        print(f"Папка {data_dir} не найдена")
        return
    
    # Получаем все CSV файлы из папки data
    csv_files = list(data_dir.glob("*.csv"))
    
    if not csv_files:
        print(f"В папке {data_dir} не найдено CSV файлов")
        return
    
    # Обрабатываем каждый CSV файл
    for csv_file in csv_files:
        print(f"Обработка файла: {csv_file.name}")
        
        try:
            # Читаем CSV файл с правильными параметрами
            df = pd.read_csv(csv_file, header= None, encoding='utf-16', sep=',', decimal='.')
            
            # Берем только первые 5 колонок
            df = df.iloc[:, :5]
            
            # Создаем папку для результатов (название без расширения .csv)
            folder_name = csv_file.stem
            output_dir = output_base_dir / folder_name
            output_dir.mkdir(exist_ok=True)
            
            # Параметры
            window_size = 11520
            step = 120  # Шаг теперь 120 строк вместо 1
            file_counter = 1
            
            # Создаем подтаблицы
            total_rows = len(df)
            start_idx = 0
            
            while start_idx + window_size <= total_rows:
                # Берем окно из 11520 строк
                sub_df = df.iloc[start_idx:start_idx + window_size]
                
                # Сохраняем в файл БЕЗ КАВЫЧЕК
                output_file = output_dir / f"{file_counter}.csv"
                # Вариант 1: без кавычек вообще
                sub_df.to_csv(output_file, header=None, index=False, quoting=3)
                # Или вариант 2: с кодировкой
                # sub_df.to_csv(output_file, index=False, quoting=3, encoding='utf-8')
                
                print(f"  Сохранено: {output_file} (строки {start_idx}-{start_idx+window_size-1})")
                
                # Увеличиваем счетчики с шагом 120
                start_idx += step
                file_counter += 1
            
            print(f"Готово для {csv_file.name}. Создано {file_counter-1} файлов.")
            print(f"Шаг смещения: {step} строк")
            
        except Exception as e:
            print(f"Ошибка при обработке файла {csv_file.name}: {str(e)}")

if __name__ == "__main__":
    create_subtables()
    print("Обработка завершена!")