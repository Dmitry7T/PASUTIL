import torch
import torch.nn as nn
import copy

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def debug_model_structure(model, name="Model"):
    print(f"\n{'='*60}")
    print(f"DEBUG: {name}")
    print(f"{'='*60}")
    
    # 1. Базовая информация
    print(f"Тип объекта: {type(model)}")
    print(f"ID объекта: {id(model)}")
    
    # 2. Проверка наследования
    print(f"\nПроверка наследования:")
    print(f"Является nn.Module? {isinstance(model, nn.Module)}")
    print(f"MRO (порядок разрешения методов):")
    for cls in type(model).__mro__:
        print(f"  - {cls}")
    
    # 3. Проверка атрибутов
    print(f"\nПроверка атрибутов:")
    print(f"Есть ли 'parameters'? {hasattr(model, 'parameters')}")
    print(f"Есть ли 'modules'? {hasattr(model, 'modules')}")
    
    # 4. Пробуем получить параметры
    print(f"\nПопытка получить параметры:")
    try:
        params = list(model.parameters())
        print(f"УСПЕХ! Найдено параметров: {len(params)}")
        for i, p in enumerate(params):
            print(f"  Параметр {i}: форма={p.shape}, requires_grad={p.requires_grad}")
    except Exception as e:
        print(f"ОШИБКА: {e}")
        print(f"Тип ошибки: {type(e).__name__}")
    
    # 5. Проверка слоев
    print(f"\nПрямая проверка слоев:")
    if hasattr(model, 'fc1'):
        print(f"  fc1 найден: {type(model.fc1)}")
    if hasattr(model, 'fc2'):
        print(f"  fc2 найден: {type(model.fc2)}")
    if hasattr(model, 'fc3'):
        print(f"  fc3 найден: {type(model.fc3)}")
    if hasattr(model, 'fc4'):
        print(f"  fc4 найден: {type(model.fc4)}")

# Создадим тестовые классы по твоему описанию
class Model(nn.Module):
    def __init__(self, input_size=30):
        super(Model, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 16)
        self.fc4 = nn.Linear(16, 4)
        
    def forward(self, x):
        return self.fc4(torch.relu(self.fc3(torch.relu(self.fc2(torch.relu(self.fc1(x)))))))

class SModel(Model):
    def __init__(self):
        super().__init__()  # Вызываем родительский конструктор
        self.balance = 10000
        self.trades = []

# Тестируем
print("Тест 1: Создание Model")
model1 = Model()
debug_model_structure(model1, "Model instance")

print("\n\nТест 2: Создание SModel")
smodel1 = SModel()
debug_model_structure(smodel1, "SModel instance")

print("\n\nТест 3: Копирование")
smodel2 = copy.deepcopy(smodel1)
debug_model_structure(smodel2, "Copied SModel")

print("\n\nТест 4: Проверка что это разные объекты")
print(f"Разные объекты? {smodel1 is not smodel2}")
print(f"Разные веса fc1? {smodel1.fc1.weight.data_ptr() != smodel2.fc1.weight.data_ptr()}")