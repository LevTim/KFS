import unittest

import numpy as np
from P4 import simulate_lorenz

class TestLorenzModel(unittest.TestCase):
    def test_trajectory_shape(self):
        t, sol = simulate_lorenz([1.0, 1.0, 1.0], t_max=10, dt=0.01)
        self.assertEqual(sol.shape[0], len(t))
        self.assertEqual(sol.shape[1], 3)

    def test_sensitivity_to_initial_conditions(self):
        t, sol1 = simulate_lorenz([1.0, 1.0, 1.0])
        _, sol2 = simulate_lorenz([1.0001, 1.0, 1.0])
        final_distance = np.linalg.norm(sol1[-1] - sol2[-1])
        self.assertGreater(final_distance, 1.0)

if __name__ == "__main__":
    unittest.main()