import torch
import copy
from backtest import Simulation
from NN import SModel

class GA:
    def __init__(self, mutation_rate = 0.1, mutation_strength = 0.05, population = 100):
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.population = population
        try:
            self.bestmodel = SModel().load_model(path= "c:/Users/User/Desktop/All/Programming/PASUTIL/pasutil_AI/best_model.pth")
        except:
            self.bestmodel = SModel()
        self.simulation = Simulation()

    def mutate(self, model):
        mutated_model = copy.deepcopy(model)
        with torch.no_grad():
            for param in mutated_model.parameters():
                if param.requires_grad:  # Только те, что учатся
                    mask = torch.rand_like(param) < self.mutation_rate
                    
                    if mask.any():  # Если есть что менять
                        noise = torch.randn_like(param) * self.mutation_strength
                        param[mask] += noise[mask]
        
        return mutated_model
    
    def process(self):
        print("создание моделей", flush=True)
        models = []
        models.append(self.bestmodel)
        for _ in range(self.population - 1):
            models.append(self.mutate(self.bestmodel))
        bestmodel = self.simulation.simulation(models)
        bestmodel.save_model(path= "c:/Users/User/Desktop/All/Programming/PASUTIL/pasutil_AI/best_model.pth")
        self.bestmodel = SModel().load_model(path= "c:/Users/User/Desktop/All/Programming/PASUTIL/pasutil_AI/best_model.pth")
        return self.bestmodel