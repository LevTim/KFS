import unittest
from P7 import Ant, City, Graph  # імпорт твоїх класів

class TestACO(unittest.TestCase):
    def test_distance(self):
        c1 = City(0, 0)
        c2 = City(3, 4)
        self.assertAlmostEqual(c1.distance(c2), 5.0)

    def test_ant_chooses_city(self):
        cities = [City(0, 0), City(1, 1), City(2, 2)]
        graph = Graph(cities)
        for i in range(len(cities)):
            for j in range(len(cities)):
                graph.pheromones[i][j] = 1.0

        ant = Ant(graph)
        ant.path = [0]
        ant.visited = {0}
        ant.current = 0

        next_city = ant.select_next_city()
        self.assertIn(next_city, [1, 2])

    def test_path_completion(self):
        cities = [City(0, 0), City(1, 1), City(2, 2)]
        graph = Graph(cities)
        for i in range(len(cities)):
            for j in range(len(cities)):
                graph.pheromones[i][j] = 1.0

        ant = Ant(graph)
        ant.path = [0]
        ant.visited = {0}
        ant.current = 0

        while len(ant.visited) < len(cities):
            next_city = ant.select_next_city()
            if next_city is None:
                break
            ant.path.append(next_city)
            ant.visited.add(next_city)
            ant.current = next_city

        self.assertEqual(len(set(ant.path)), len(cities))
        self.assertEqual(len(ant.visited), len(cities))

if __name__ == '__main__':
    unittest.main()
