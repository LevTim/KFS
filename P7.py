import pygame
import random
import math
import sys
import time
import threading

CITY_COUNT = 30
ANT_COUNT = 50
ITERATIONS = 50
ALPHA = 1.0      # вплив феромону
BETA = 5.0       # вплив відстані
RHO = 0.5        # коефіцієнт випаровування
Q = 100          # загальна кількість феромонів, що залишає мураха

SCREEN_SIZE = 800
CITY_RADIUS = 5
FPS = 60
SPEED = 0.5  # затримка візуалізації

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

class Ant:
    def __init__(self, graph):
        self.graph = graph
        self.path = []
        self.visited = set()
        self.total_length = 0
        self.current = random.randint(0, len(graph.cities) - 1)
        self.path.append(self.current)
        self.visited.add(self.current)

    def select_next_city(self):
        probabilities = []
        current_city = self.current
        for i in range(len(self.graph.cities)):
            if i in self.visited:
                probabilities.append(0)
            else:
                pheromone = self.graph.pheromones[current_city][i] ** ALPHA
                heuristic = (1 / self.graph.distances[current_city][i]) ** BETA
                probabilities.append(pheromone * heuristic)

        total = sum(probabilities)
        if total == 0:
            return None
        probabilities = [p / total for p in probabilities]
        next_city = random.choices(range(len(self.graph.cities)), weights=probabilities)[0]
        return next_city

    def move(self):
        while len(self.visited) < len(self.graph.cities):
            next_city = self.select_next_city()
            if next_city is None:
                return
            self.total_length += self.graph.distances[self.current][next_city]
            self.current = next_city
            self.path.append(next_city)
            self.visited.add(next_city)
        self.total_length += self.graph.distances[self.path[-1]][self.path[0]]

class Graph:
    def __init__(self, cities):
        self.cities = cities
        self.distances = [[c1.distance(c2) for c2 in cities] for c1 in cities]
        self.pheromones = [[1 for _ in cities] for _ in cities]

    def evaporate_pheromones(self):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones)):
                self.pheromones[i][j] *= (1 - RHO)

    def deposit_pheromones(self, ants):
        for ant in ants:
            pheromone_deposit = Q / ant.total_length
            for i in range(len(ant.path)):
                a = ant.path[i]
                b = ant.path[(i + 1) % len(ant.path)]
                self.pheromones[a][b] += pheromone_deposit
                self.pheromones[b][a] += pheromone_deposit

def draw(graph, best_path):
    screen.fill((255, 255, 255))
    for city in graph.cities:
        pygame.draw.circle(screen, (0, 0, 255), (int(city.x), int(city.y)), CITY_RADIUS)

    if best_path:
        for i in range(len(best_path)):
            a = graph.cities[best_path[i]]
            b = graph.cities[best_path[(i + 1) % len(best_path)]]
            pygame.draw.line(screen, (255, 0, 0), (a.x, a.y), (b.x, b.y), 2)
    pygame.display.flip()

def main():
    global screen
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Ant Colony Optimization - TSP")
    clock = pygame.time.Clock()

    cities = [City(random.randint(50, SCREEN_SIZE - 50), random.randint(50, SCREEN_SIZE - 50)) for _ in range(CITY_COUNT)]
    graph = Graph(cities)
    best_path = None
    best_length = float('inf')

    for iteration in range(ITERATIONS):
        ants = [Ant(graph) for _ in range(ANT_COUNT)]
        for ant in ants:
            ant.move()
            if ant.total_length < best_length:
                best_length = ant.total_length
                best_path = ant.path.copy()

        graph.evaporate_pheromones()
        graph.deposit_pheromones(ants)
        draw(graph, best_path)
        print(f"Iteration {iteration+1}/{ITERATIONS}, Best length: {best_length:.2f}")
        time.sleep(SPEED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()
