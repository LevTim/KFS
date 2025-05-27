import random
import concurrent.futures
from tsp import generate_cities, compute_fitness, total_distance, crossover, mutate

def initialize_population(pop_size, city_count):
    return [random.sample(range(city_count), city_count) for _ in range(pop_size)]

def evaluate_population(population, cities):
    return [compute_fitness(individual, cities) for individual in population]

def select_parents(population, fitnesses, k=3):
    selected = []
    for _ in range(len(population)):
        contenders = random.sample(list(zip(population, fitnesses)), k)
        selected.append(max(contenders, key=lambda x: x[1])[0])
    return selected

def reproduce(parents, crossover_rate, mutation_rate):
    next_gen = []
    for i in range(0, len(parents), 2):
        if i + 1 < len(parents):
            p1, p2 = parents[i], parents[i+1]
            child1, child2 = crossover(p1, p2, crossover_rate)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            next_gen.extend([child1, child2])
    return next_gen

def next_generation(population, offspring, cities, elite_size=2):
    combined = population + offspring
    combined_fitness = evaluate_population(combined, cities)
    sorted_population = [x for _, x in sorted(zip(combined_fitness, combined), reverse=True)]
    return sorted_population[:len(population)]

def should_terminate(iteration, max_iters, no_improve, max_no_improve):
    return iteration >= max_iters or no_improve >= max_no_improve

def get_best(population, cities):
    fitnesses = evaluate_population(population, cities)
    best_idx = fitnesses.index(max(fitnesses))
    return population[best_idx], fitnesses[best_idx]

def run_parallel_ga(city_count=20, num_populations=4, pop_size=50, max_iters=100,
                    mutation_rate=0.05, crossover_rate=0.8, max_no_improve=20):
    cities = generate_cities(city_count)
    populations = [initialize_population(pop_size, city_count) for _ in range(num_populations)]
    best_global = None
    best_score = float('-inf')
    no_improve = 0

    for iteration in range(max_iters):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for pop in populations:
                futures.append(executor.submit(evolve_population, pop, cities,
                                               crossover_rate, mutation_rate))
            populations = [f.result() for f in futures]

        for pop in populations:
            candidate, score = get_best(pop, cities)
            if score > best_score:
                best_score = score
                best_global = candidate
                no_improve = 0
            else:
                no_improve += 1

        print(f"Iteration {iteration+1}: Best Distance = {1 / best_score:.2f}")

        if should_terminate(iteration+1, max_iters, no_improve, max_no_improve):
            break

    print("\nBest Route:", best_global)
    print("Shortest Distance:", 1 / best_score)

def evolve_population(pop, cities, crossover_rate, mutation_rate):
    fitnesses = evaluate_population(pop, cities)
    parents = select_parents(pop, fitnesses)
    offspring = reproduce(parents, crossover_rate, mutation_rate)
    return next_generation(pop, offspring, cities)
