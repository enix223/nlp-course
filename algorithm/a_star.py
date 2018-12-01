#!/usr/local/env python

"""
============
A* algorithm
============

Ref: https://en.wikipedia.org/wiki/A*_search_algorithm

An example to show how to search path between two cities.

Heuristic function:

f(n) = g(n) + h(n)

g(n) denotes the from start node to current node, h(n) denotes the cost from
current node to target node


Examples
--------
$ python a_start.py ../data/geo/cities.json 海口 哈尔滨

"""

import sys
import json
import math
import heapq
import argparse


def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lon1, lat1 = origin
    lon2, lat2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def build_graph(path):
    threshold = 700
    graph = {}
    locations = {}

    with open(path, 'rb') as f:
        data = json.load(f)

    for city1 in data:
        locations[city1['name']] = city1['geoCoord']

        for city2 in data:
            if city1['name'] == city2['name']:
                continue

            dist = geo_distance(city1['geoCoord'], city2['geoCoord'])
            if dist < threshold:
                try:
                    graph[city1['name']].add(city2['name'])
                except KeyError:
                    graph[city1['name']] = set([city2['name']])

    return graph, locations


def distance_heuristic(locations, from_city, to_city, cur_city):
    """
    Distance base heuristic function

    hn = distance in km between target city and current city
    gn = distance in km between from city and current city
    """
    hn = geo_distance(
        (locations[to_city][1], locations[to_city][0]),
        (locations[cur_city][1], locations[cur_city][0]),
    )
    gn = geo_distance(
        (locations[from_city][1], locations[from_city][0]),
        (locations[cur_city][1], locations[cur_city][0]),
    )
    return gn + hn


def astar_search(graph, locations, from_node, to_node):
    """
    Find the route in `graph` from `from_node` to `to_node` with A* search
    """
    seen = set()
    pending = []
    path = []

    heuristic = distance_heuristic(locations, from_node, to_node, from_node)
    heapq.heappush(pending, (heuristic, from_node))

    while len(pending) > 0:
        _, cur_node = heapq.heappop(pending)
        if cur_node in seen:
            continue

        if cur_node == to_node:
            path.append(cur_node)
            return path

        for neighbor in graph[cur_node]:
            if neighbor in seen:
                continue

            # Heuristic function: From current city to next neighbor and the target city
            heuristic = distance_heuristic(locations, cur_node, to_node, neighbor)
            heapq.heappush(pending, (heuristic, neighbor))

        path.append(cur_node)
        seen.add(cur_node)

    return path


def print_path(path):
    print(' -> '.join(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        type=str,
        help='The cities json path'
    )
    parser.add_argument(
        'from_city',
        type=str,
        help='From city'
    )
    parser.add_argument(
        'to_city',
        type=str,
        help='To city'
    )
    args = parser.parse_args(sys.argv[1:])

    graph, locations = build_graph(args.path)
    path = astar_search(graph, locations, args.from_city, args.to_city)
    print_path(path)
