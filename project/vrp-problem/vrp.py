#!/usr/bin/env python3

"""
=============================
VRP - Vehicle routing problem
=============================

https://en.wikipedia.org/wiki/Vehicle_routing_problem

             o
    o      /   `
    | `   /     `
    |   o - - - - o
    | / |`
    o   |  `
        |    `
        o - - - o

Suppose we have 5 cities (C1, C2, C3, C4, C5), and 2 vehicles (A, B)

C1 C2 C3 C4 C5

+-----------------------------+
|  |  |  |  |  |  |  |  |  |  |
+-----------------------------+
|------ A -----|------ B -----|

Possible path 1:

+-----------------------------+
|C2|C1|  |C4|  |  |C5|  |  |C3|  => A: C0 -> C2 -> C1 -> C4 -> C0
+-----------------------------+     B: C0 -> C5 -> C3 -> C0
|------ A -----|------ B -----|

Usage
-----

# Run with random generated coordinates (7 cities, 2 vehicles)
python vrp.py --vehicles 2 --coors 7

# Run with `cities.txt` dataset and 2 vehicles
python vrp.py --path ../data/vrp/cities.txt --vehicles 2

# Run with `cities.txt` dataset and 3 vehicles
python vrp.py --path ../data/vrp/cities.txt --vehicles 3

Todo
-----

The search space is huge, need to prune to reduce search space
"""

from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import itertools
import argparse
import logging
import sys


FORMAT = '[%(levelname)s] %(asctime)s: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def distance(lft_coor, rgh_coor):
    """
    Calculate the euclidean distance for given two coordinates
    """
    return np.linalg.norm(lft_coor - rgh_coor)


def generate_coordinates(size):
    """
    Generate random coordinate points

    :param int size: How many points to create
    :returns: An size * 2 dim np.array
    """
    lat = np.random.uniform(22.0, 39.7, (size, 1))
    lng = np.random.uniform(100, 119, (size, 1))
    coors = np.hstack((lng, lat))
    return coors


def get_node_distances(coordinates):
    """
    Get distance mapping for each point in coordinates
    """
    distances = defaultdict(lambda: 0)
    distances.update({
        (i, j): distance(coordinates[i], coordinates[j])
        for i in range(coordinates.shape[0]) for j in range(coordinates.shape[0]) if i != j
    })
    return distances


def build_path_cost(distances):
    def path_cost(plan):
        """
        Calculate the path cost
        """
        # [[0, 1, 2, 3, 4], [], [], []]
        # Cost(orign -> 0 -> 1 -> 2 -> 3 -> 4 -> orig)
        cost = 0
        for path in plan:
            temp_path = path[1:]
            prev = path[0]
            for coor in temp_path:
                cost += distances[(prev, coor)]
                prev = coor
        return cost
    return path_cost


def solve_vrp(coordinates, full_node_distances, no_vehicles):
    """
    Solve the VRP problem with given coordinates and #Vehicles
    (The first coordindate is the origin)

    :param np.array coordinates: The city coordinate points, point = (lng, lat)
    :param int no_vehicles: How many vehicles for the problem
    :returns list: Return the optimal paths
    """
    logger.debug('G(V, E) = G({}, {})'.format(len(coordinates), len(full_node_distances)))
    no_cities = len(coordinates) - 1

    def possible_paths():
        """
        0 1 2 3 4

        0 - (0, 0)
        1 - (0, 1)
        2 - (0, 2)
        3 - (1, 0)
        4 - (1, 1)

        [[0, 1, 2], [3,4]]
        """
        path_indexes = itertools.permutations(range(1, no_cities * no_vehicles), no_cities)

        def build_path(p):
            paths = [[0] for _ in range(no_vehicles)]
            for i, j in enumerate(p):
                paths[j // no_cities].append(i + 1)
            for path in paths:
                path.append(0)
            return paths

        paths = map(build_path, path_indexes)
        return paths

    path_cost = build_path_cost(full_node_distances)
    min_path = min(possible_paths(), key=path_cost)
    min_cost = path_cost(min_path)

    return min_path, min_cost


def draw_optimal_path_graph(paths, coordinates, full_node_distances, vehicles):
    full_node_distances = {k: round(v, 2) for k, v in full_node_distances.items()}
    graph = nx.DiGraph()

    # add all nodes
    graph.add_nodes_from(range(len(coordinates)))

    # Draw edges for all citie pairs
    nx.draw_networkx_edges(graph, pos=coordinates, edgelist=full_node_distances.keys(), edge_color='#999999', arrows=False)
    nx.draw_networkx_edge_labels(graph, pos=coordinates, edge_labels=full_node_distances, font_size=8, alpha=0.5)

    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'w']
    for i, path in enumerate(optimal_path):
        prev = path[0]
        for index in path[1:]:
            graph.add_edge(prev, index, color=colors[i % len(colors)], weight=1.5)
            prev = index

    # Ref: https://stackoverflow.com/questions/25639169/networkx-change-color-width-according-to-edge-attributes-inconsistent-result
    edges = graph.edges()
    colors = [graph[u][v]['color'] for u, v in edges]
    weights = [graph[u][v]['weight'] for u, v in edges]
    nx.draw(graph, pos=coordinates, with_labels=True, font_color='w', edges=edges, edge_color=colors, width=weights)
    plt.title('VRP Optimal solution for {} cities and {} vehicles'.format(len(coordinates) - 1, vehicles))
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        type=str,
        help='Path for city coordinates'
    )
    parser.add_argument(
        '--coors',
        type=int,
        default=7,
        help='No. of city coordinates to random generate'
    )
    parser.add_argument(
        '--vehicles',
        type=int,
        default=2,
        help='No. of vehicles'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose mode'
    )
    args = parser.parse_args(sys.argv[1:])

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.path is None:
        logger.info('Creating random coordinates...')
        coordinates = generate_coordinates(args.coors)
        logger.info(coordinates)
    else:
        logger.info('Loading coordinates from {}'.format(args.path))
        coordinates = np.genfromtxt(args.path, delimiter=',')

    full_node_distances = get_node_distances(coordinates)
    optimal_path, optimal_cost = solve_vrp(coordinates, full_node_distances, args.vehicles)
    logger.info('Optimal path: {}'.format(optimal_path))
    logger.info('Optimal cost: {}'.format(optimal_cost))

    # Present the solution
    draw_optimal_path_graph(optimal_path, coordinates, full_node_distances, args.vehicles)
