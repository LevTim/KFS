import unittest
from tsp import compute_fitness, total_distance

class TestFitness(unittest.TestCase):
    def test_total_distance(self):
        cities = [(0,0), (3,0), (3,4)]
        tour = [0, 1, 2]
        self.assertAlmostEqual(total_distance(tour, cities), 12.0)

    def test_fitness(self):
        cities = [(0,0), (3,0), (3,4)]
        tour = [0, 1, 2]
        fitness = compute_fitness(tour, cities)
        self.assertAlmostEqual(fitness, 1/12)

if __name__ == '__main__':
    unittest.main()
