import numpy as np


class Ant:

    def __init__(self, distances, visibility, pheromones, alpha, beta):
        self.distances = distances
        self.visibility = visibility
        self.start_pos = np.random.randint(0, self.distances.shape[0])
        self.location = self.start_pos
        self.visited = [self.location]
        self.unvisited = self.unvisited = [i for i in range(self.distances.shape[0]) if self.location != i]
        self.path = []
        self.len_path = 0.0
        self.pheromones = pheromones
        self.pheromones[self.location] = 1e-1
        self.alpha = alpha
        self.beta = beta

    def init_states(self):
        self.location = self.start_pos
        self.visited = [self.location]
        self.unvisited = self.unvisited = [i for i in range(self.distances.shape[0]) if self.location != i]
        self.path = []
        self.len_path = 0.0

    def find_path(self):
        move = self.transition()
        while move != -1:
            self.location = move[1]
            self.len_path += self.distances[move]
            self.path.append(move)
            self.visited.append(move[1])
            self.unvisited.remove(move[1])
            move = self.transition()
        self.finish_tour()
        self.spread_pheromones()

    def finish_tour(self):
        move = (self.visited[-1], self.start_pos)
        self.location = self.start_pos
        self.len_path += self.distances[move]
        self.path.append(move)

    def spread_pheromones(self):
        for arc in self.path:
            self.pheromones[arc] = 1/self.len_path

    def transition(self):
        best_move = -1
        best_prob = 0
        for j in self.unvisited:
            gamma = np.random.uniform(0, 1)
            num_p = gamma + self.pheromones[self.location, j]**self.alpha * self.visibility[self.location, j]**self.beta
            den_p = np.sum([gamma + self.pheromones[self.location, i]**self.alpha * self.visibility[self.location, i]**self.beta for i in self.unvisited])
            p = num_p/den_p
            if p > best_prob:
                best_prob = p
                best_move = (self.location, j)
        return best_move


