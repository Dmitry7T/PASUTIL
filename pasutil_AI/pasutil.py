import numpy as np

class NeuralNetwork:
    def __init__(self, layers):
        self.layers = layers
        self.weights = []
        self.biases = []
        
        # Инициализация весов
        for i in range(len(layers)-1):
            self.weights.append(np.random.randn(layers[i], layers[i+1]))
            self.biases.append(np.random.randn(layers[i+1]))
        
        print(self.layers)
        print(self.weights)
        print(self.biases)
    
    def forward(self, x):
        for i in range(len(self.weights)):
            x = np.tanh(np.dot(x, self.weights[i]) + self.biases[i])
        return x
    
class GeneticAlgorithm:
    def __init__(self, population_size, network_architecture, mutation_rate=0.1):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = [NeuralNetwork(network_architecture) 
                          for _ in range(population_size)]
    
    def fitness_function(self, network, X, y):
        # Пример фитнес-функции (чем меньше ошибка, тем лучше)
        predictions = np.array([network.forward(x) for x in X])
        error = np.mean((predictions - y) ** 2)
        return 1.0 / (1.0 + error)  # Преобразуем ошибку в фитнес
    
    def select_parents(self, fitness_scores):
        # Турнирная селекция
        tournament_size = 3
        selected = []
        
        for _ in range(2):  # Выбираем двух родителей
            contestants = np.random.choice(
                len(self.population), tournament_size, replace=False
            )
            best = contestants[np.argmax([fitness_scores[i] for i in contestants])]
            selected.append(self.population[best])
        
        return selected
    
    def crossover(self, parent1, parent2):
        child = NeuralNetwork([len(parent1.weights[0]), len(parent1.weights[0][0])])
        
        # Одноточечное скрещивание для весов
        for i in range(len(parent1.weights) - 1):
            crossover_point = np.random.randint(0, parent1.weights[i].size)
            flat_weights1 = parent1.weights[i].flatten()
            flat_weights2 = parent2.weights[i].flatten()
            
            # Скрещивание
            child_flat = np.concatenate([
                flat_weights1[:crossover_point],
                flat_weights2[crossover_point:]
            ])
            child.weights[i] = child_flat.reshape(parent1.weights[i].shape)
        
        return child
    
    def mutate(self, network):
        for i in range(len(network.weights)):
            # Мутация весов
            mutation_mask = np.random.random(network.weights[i].shape) < self.mutation_rate
            network.weights[i] += mutation_mask * np.random.randn(*network.weights[i].shape) * 0.1
            
            # Мутация смещений
            mutation_mask = np.random.random(network.biases[i].shape) < self.mutation_rate
            network.biases[i] += mutation_mask * np.random.randn(*network.biases[i].shape) * 0.1
    
    def evolve(self, X, y, generations=100):
        best_fitness_history = []
        
        for generation in range(generations):
            # Оценка fitness
            fitness_scores = [self.fitness_function(network, X, y) 
                            for network in self.population]
            
            # Новая популяция
            new_population = []
            
            # Элитизм - сохраняем лучшую особь
            best_index = np.argmax(fitness_scores)
            new_population.append(self.population[best_index])
            
            # Создаем остальных особей
            while len(new_population) < self.population_size:
                # Селекция
                parent1, parent2 = self.select_parents(fitness_scores)
                
                # Скрещивание
                child = self.crossover(parent1, parent2)
                
                # Мутация
                self.mutate(child)
                
                new_population.append(child)
            
            self.population = new_population[:self.population_size]
            
            # Логирование
            best_fitness = max(fitness_scores)
            best_fitness_history.append(best_fitness)
            print(f"Поколение {generation}: Лучший фитнес = {best_fitness:.4f}")
        
        return best_fitness_history
    
# Создаем тестовые данные (задача XOR)
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

# Настраиваем ГА
ga = GeneticAlgorithm(
    population_size=1,
    network_architecture=[2, 4, 1],  # 2 входа, 4 скрытых нейрона, 1 выход
    mutation_rate=0.8
)

# Запускаем эволюцию
fitness_history = ga.evolve(X, y, generations=2)

# Тестируем лучшую сеть
best_network = ga.population[0]
for i in range(len(X)):
    prediction = best_network.forward(X[i])
    print(f"Вход: {X[i]} -> Предсказание: {prediction[0]:.3f} (Ожидалось: {y[i][0]})")