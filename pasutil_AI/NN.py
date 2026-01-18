import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Optional

class Model(nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        
        # Определяем размеры слоев
        self.input_size = 30
        self.layer1_size = 128
        self.layer2_size = 64
        self.layer3_size = 16
        self.output_size = 4
        
        # Полносвязные слои
        self.fc1 = nn.Linear(self.input_size, self.layer1_size)  # Слой 1: 30 -> 128
        self.fc2 = nn.Linear(self.layer1_size, self.layer2_size)  # Слой 2: 128 -> 64
        self.fc3 = nn.Linear(self.layer2_size, self.layer3_size)  # Слой 3: 64 -> 16
        self.fc4 = nn.Linear(self.layer3_size, self.output_size)  # Слой 4: 16 -> 4
        
        # Инициализация весов (рекомендуемая для tanh и sigmoid)
        self._initialize_weights()
        
    def _initialize_weights(self):
        """Инициализация весов для лучшей сходимости"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                # Xavier инициализация для слоев с tanh
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
    
    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, 
                                                torch.Tensor, torch.Tensor]:
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        
        signal = torch.tanh(x[:, 0])  
        risk_percent = torch.sigmoid(x[:, 1]) * 0.02
        growth_predict = torch.sigmoid(x[:, 2]) * 0.03
        fall_predict = torch.sigmoid(x[:, 3]) * 0.03 
        return signal, risk_percent, growth_predict, fall_predict
    
    def predict(self, input_data) -> dict:
        input_tensor = torch.from_numpy(input_data).float()
        if len(input_tensor.shape) == 1:
            input_tensor = input_tensor.unsqueeze(0)
        
        signal, risk_percent, growth_predict, fall_predict = self.forward(input_tensor)
        
        return {
            'signal': signal.detach().numpy(),
            'risk_percent': risk_percent.detach().numpy(),
            'growth_predict': growth_predict.detach().numpy(),
            'fall_predict': fall_predict.detach().numpy()
        }
    
    def save_model(self, path: str):
        torch.save({
            'model_state_dict': self.state_dict(),
            # Убрать 'model_config' если параметры фиксированные
        }, path)
        print(f"Модель сохранена в {path}", flush=True)
    
    @classmethod
    def load_model(cls, path: str, device: Optional[str] = None):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'

        checkpoint = torch.load(path, map_location=device)

        # Создаем экземпляр модели БЕЗ АРГУМЕНТОВ
        model = cls()  # <-- ИЗМЕНЕНИЕ ЗДЕСЬ
        
        # Загружаем веса
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)

        print(f"Модель загружена из {path}", flush=True)
        return model


class SModel(Model):
    def __init__(self, balance = 10000):
        super(SModel, self).__init__()
        self.flag = True
        self.trades = list()

        # fitness
        self.balance = balance
        self.fine = 0
        self.const_balance = balance
        self.max_balance = balance
        self.min_balance = balance
        self.fitness = 0
