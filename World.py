import numpy as np
import copy
from Fourmis import Fourmis

distances = np.array([[0, 2, 2, 5, 7],
                      [2, 0, 4, 8, 2],
                      [2, 4, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])

dist = np.array([[0.0,  3.0,  4.0,  2.0,  7.0],
                [3.0  ,0.0  ,4.0  ,6.0 , 3.0],
                [4.0  ,4.0,  0.0 , 5.0 , 8.0],
                [2.0 , 6.0 , 5.0 , 0.0 , 6.0],
                [7.0 , 3.0 , 8.0 , 6.0 , 0.0]])
class World:

    def __init__(self, num_ants, distances, ro=0.5):
        self.num_ants = num_ants
        self.distances = distances
        self.visibility = 1/(self.distances+0.01)
        self.pheromones = copy.copy(self.visibility)
        self.ants = [Fourmis(self.distances, copy.deepcopy(self.visibility), copy.deepcopy(self.pheromones)) for _ in range(self.num_ants)]
        self.ro = ro

    def run(self, num_iterations):
        best_ant = None
        best_path = np.inf
        delta = copy.deepcopy(self.pheromones)
        for ite in range(num_iterations):
            for ant in self.ants:
                ant.find_path()
                delta += ant.pheromones
                if ant.len_path < best_path:
                    best_ant = ant
                    best_path = ant.len_path
                    print('Best path :', best_ant.path, 'with path len of', best_ant.len_path)
                ant.init_states()
            self.update_pheromone(delta)


    def update_pheromone(self, delta):
        self.pheromones = self.ro * self.pheromones + delta
        for ant in self.ants:
            ant.pheromones = copy.deepcopy(self.pheromones)

if __name__ == '__main__':
    world = World(5, distances)
    world.run(10)
