%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import HTML
# Стани клітин
TREE = 0
BURNING = 1
EMPTY = 2

# Кольори для візуалізації
colors = ['green', 'red', 'black']
cmap = plt.matplotlib.colors.ListedColormap(colors)
def initialize_forest(size, initial_burning=5):
    forest = np.full((size, size), TREE)
    for _ in range(initial_burning):
        x, y = np.random.randint(0, size, size=2)
        forest[x, y] = BURNING
    burn_time = np.zeros_like(forest, dtype=int)
    return forest, burn_time
def step(forest, burn_time, P_burn, T_burn):
    new_forest = forest.copy()
    new_burn_time = burn_time.copy()
    size = forest.shape[0]

    for i in range(size):
        for j in range(size):
            if forest[i, j] == TREE:
                neighbors = forest[max(i - 1, 0):min(i + 2, size),
                                   max(j - 1, 0):min(j + 2, size)]
                if np.any(neighbors == BURNING):
                    if np.random.rand() < P_burn:
                        new_forest[i, j] = BURNING
                        new_burn_time[i, j] = 1
            elif forest[i, j] == BURNING:
                if burn_time[i, j] >= T_burn:
                    new_forest[i, j] = EMPTY
                else:
                    new_burn_time[i, j] += 1
    return new_forest, new_burn_time
def simulate_fire(size=50, P_burn=0.3, T_burn=3, steps=50, initial_burning=5):
    forest, burn_time = initialize_forest(size, initial_burning)
    history = [forest.copy()]

    for _ in range(steps):
        forest, burn_time = step(forest, burn_time, P_burn, T_burn)
        history.append(forest.copy())

    return history
def animate_simulation(history):
    fig, ax = plt.subplots()
    img = ax.imshow(history[0], cmap=cmap, vmin=0, vmax=2)
    ax.set_title("Forest Fire Simulation")

    def update(frame):
        img.set_data(history[frame])
        ax.set_title(f"Step {frame}")
        return [img]

    anim = animation.FuncAnimation(fig, update, frames=len(history), interval=200, repeat=False)
    return anim
history = simulate_fire(size=50, P_burn=0.1, T_burn=10, steps=100)
anim = animate_simulation(history)

# Показати анімацію в Jupyter як HTML
HTML(anim.to_jshtml())