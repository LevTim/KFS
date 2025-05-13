import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def lorenz(t, state, sigma=10, beta=8 / 3, rho=28):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return [dx, dy, dz]


def simulate_lorenz(initial_state, t_max=40, dt=0.01):
    t_span = (0, t_max)
    t_eval = np.arange(0, t_max, dt)
    result = solve_ivp(lorenz, t_span, initial_state, t_eval=t_eval)
    return result.t, result.y.T


def plot_sensitivity():
    initial_state1 = [1.0, 1.0, 1.0]
    initial_state2 = [1.0001, 1.0, 1.0]

    t, sol1 = simulate_lorenz(initial_state1)
    _, sol2 = simulate_lorenz(initial_state2)

    distance = np.linalg.norm(sol1 - sol2, axis=1)

    plt.figure(figsize=(10, 6))
    plt.plot(t, distance)
    plt.yscale('log')
    plt.title('Розходження траєкторій Лоренца (лог шкала)')
    plt.xlabel('Час')
    plt.ylabel('Відстань між траєкторіями')
    plt.grid(True)
    plt.show()


def plot_attractor():
    initial_state = [1.0, 1.0, 1.0]
    _, sol = simulate_lorenz(initial_state)

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(projection='3d')
    ax.plot(*sol.T, lw=0.5)
    ax.set_title("Атрактор Лоренца")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.show()

if __name__ == "__main__":
    plot_attractor()

    plot_sensitivity()




