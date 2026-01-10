import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Optional

class Model(nn.Module):
    def __init__(self, input_size = 30):
        super(Model, self).__init__()
        
        # Определяем размеры слоев
        self.input_size = input_size
        self.layer1_size = 128
        self.layer2_size = 64
        self.layer3_size = 16
        self.output_size = 4
        
        # Полносвязные слои
        self.fc1 = nn.Linear(input_size, self.layer1_size)  # Слой 1: 30 -> 128
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
        
        # Разделяем выходы и применяем разные функции активации
        signal = torch.tanh(x[:, 0])  # 1. Сигнал: tanh, диапазон -1...+1
        # 2. % риска: sigmoid и масштабирование до 0...2%
        risk_percent = torch.sigmoid(x[:, 1]) * 0.02
        # 3. Прогноз роста: softplus, результат в процентах
        growth_predict = F.softplus(x[:, 2])  # 0...∞%
        # 4. Прогноз падения: softplus, результат в процентах
        fall_predict = F.softplus(x[:, 3])  # 0...∞%
        return signal, risk_percent, growth_predict, fall_predict
    
    def predict(self, input_data) -> dict:
        input_tensor = torch.from_numpy(input_data)
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
            'model_config': {
                'input_size': self.input_size,
                'layer1_size': self.layer1_size,
                'layer2_size': self.layer2_size,
                'layer3_size': self.layer3_size,
                'output_size': self.output_size
            }
        }, path)
        print(f"Модель сохранена в {path}", flush=True)
    
    @classmethod
    def load_model(cls, path: str, device: Optional[str] = None):
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        checkpoint = torch.load(path, map_location=device)
        
        # Создаем экземпляр модели
        model = cls(input_size=checkpoint['model_config']['input_size'])
        
        # Загружаем веса
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        
        print(f"Модель загружена из {path}", flush=True)
        return model


class SModel(Model):
    def __init__(self):
        super().__init__()
        self.balance = 10000
        self.trades = list()