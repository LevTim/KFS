from parallel_ga import run_parallel_ga

if __name__ == "__main__":
    run_parallel_ga(
        city_count=20,         # кількість міст
        num_populations=4,     # кількість паралельних популяцій
        pop_size=50,           # розмір кожної популяції
        max_iters=100,         # максимальна кількість ітерацій
        mutation_rate=0.05,    # ймовірність мутації
        crossover_rate=0.8,    # ймовірність кросоверу
        max_no_improve=20      # опція "до останнього живого"
    )
