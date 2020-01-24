import argparse
from World import World
import numpy as np

N_ITE = 20
N_ANTS = 4
ALPHA = 1
BETA = 1
RO = 0.5
DISTANCES_PATH = 'distances/sh07_dist.txt'


def get_arguments():
    parser = argparse.ArgumentParser(description="TSPFourmAI")
    parser.add_argument("--n-ite", type=int, default=N_ITE,
                        help="Number of iterations for find best path")
    parser.add_argument("--n-ants", type=int, default=N_ANTS,
                        help="Number of ants - Generally n-ants = num cities")
    parser.add_argument("--alpha", type=int, default=ALPHA,
                        help='Alpha value for transition choice')
    parser.add_argument("--beta", type=int, default=BETA,
                        help='Beta value for transition choice')
    parser.add_argument("--ro", type=int, default=RO,
                        help='Ro value for pheromone evaporation')
    parser.add_argument("--distances", type=str, default=DISTANCES_PATH,
                        help='Path to distances matrices')
    return parser.parse_args()


args = get_arguments()

if __name__ == '__main__':
    world = World(num_ants=args.n_ants, distances=args.distances, alpha=args.alpha, beta=args.beta, ro=args.ro)
    world.run(num_iterations=args.n_ite)