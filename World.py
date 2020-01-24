import numpy as np
import pylab as plt
import copy
from Ant import Ant
import networkx as nx


class World:

    def __init__(self, num_ants, distances, alpha=1, beta=1, ro=0.5):
        self.num_ants = num_ants
        self.distance_path = distances
        self.distances = np.loadtxt(distances)
        self.visibility = 1/(self.distances+0.01)
        self.pheromones = copy.copy(self.visibility)
        self.ants = [Ant(self.distances, copy.deepcopy(self.visibility), copy.deepcopy(self.pheromones), alpha=alpha, beta=beta) for _ in range(self.num_ants)]
        self.ro = ro

    def run(self, num_iterations):
        best_ant = None
        best_path = np.inf
        best_len = np.inf
        delta = copy.deepcopy(self.pheromones)
        for ite in range(num_iterations):
            for ant in self.ants:
                ant.find_path()
                delta += ant.pheromones
                if ant.len_path < best_len:
                    best_ant = ant
                    best_path = best_ant.path
                    best_len = best_ant.len_path
                    print('-- Update best path --')
                    print('Best path find :', best_path, 'with path len of', best_len)
                ant.init_states()
            self.update_pheromone(delta)
        self.plot_graph(best_path, all_path=True)
        self.plot_graph(best_path, all_path=False)

    def update_pheromone(self, delta):
        self.pheromones = self.ro * self.pheromones + delta
        for ant in self.ants:
            ant.pheromones = copy.deepcopy(self.pheromones)

    def plot_graph(self, best_path, all_path=True):
        G = nx.from_numpy_matrix(self.distances, create_using=nx.DiGraph())
        labels = {}
        for n in range(len(self.distances)):
            for m in range(len(self.distances) - (n + 1)):
                G.add_edge(n, n + m + 1)
                if all_path:
                    labels[(n, n + m + 1)] = str(self.distances[n][n + m + 1])
                else:
                    if (n, n + m + 1) in best_path:
                        labels[(n, n + m + 1)] = str(self.distances[n][n + m + 1])

        red_edges = best_path
        black_edges = []
        for edge in G.edges():
            if edge not in red_edges and tuple(np.flip(edge)) not in red_edges:
                black_edges.append(edge)

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_size=650)
        nx.draw_networkx_labels(G, pos, font_size=15)
        nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True, width=2)
        if all_path:
            nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False, width=2)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=15)
            plt.savefig(self.distance_path[:-4] + '_all_path.png')
        else:
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=15)
            plt.savefig(self.distance_path[:-4] + '_best_path.png')
        plt.show()




