import random
import math

def generate_cities(n):
    return [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

def total_distance(tour, cities):
    dist = sum(math.dist(cities[tour[i]], cities[tour[(i+1)%len(tour)]]) for i in range(len(tour)))
    return dist

def compute_fitness(individual, cities):
    return 1 / total_distance(individual, cities)

def crossover(parent1, parent2, rate=0.8):
    if random.random() > rate:
        return parent1[:], parent2[:]
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child1 = [-1]*size
    child1[start:end] = parent1[start:end]
    fill = [x for x in parent2 if x not in child1]
    child1 = [x if x != -1 else fill.pop(0) for x in child1]
    return child1, child1[::-1]

def mutate(individual, rate=0.05):
    for i in range(len(individual)):
        if random.random() < rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
