#!/usr/local/env python

"""
===========================
Metro exchange route search
===========================

------------------
Heuristic function
------------------

1. Base on distance only

h(n) = g(n) + f(n), where g(n) denote the distance between current station to
the target station and, f(n) denote the distance between the start station to
the current station

2. Base on distance and line information

h(n) = g(n) + h(n)

       { 0, if both stations in the same line
l(n) = {
       { 1, if the two stations not in the same line

dg(n) denote the normalized distance between current station to the target station
dh(n) denote the normalized distance between start station to the target station

both dg(n) and dh(n) are normalized to 0 to 1, 0 means the shortest distance, wheras 1
denotes the longest distance

g(n) = w1 * dg(n) + w2 * l(n)
h(n) = w1 * dh(n) + w2 * l(n)

w1, w2 are the weight for the components

------------------
Metro file format
------------------
{
    'city': 'BJ',
    'lines': [
        {
            'line_name': '1号线',
            'stations': [
                {'station': '苹果园', 'lon': 116.177388, 'lat': 39.926727},
                {'station': '古城', 'lon': 116.190337, 'lat': 39.907450}
            ]
        },
        {
            'line_name': '2号线',
            'stations': [
                {'station': '西直门', 'lon': 116.177388, 'lat': 39.926727},
                {'station': '积水潭', 'lon': 116.177388, 'lat': 39.926727}
            ]
        }
    ]
}

------------------
Usage
------------------

Step 1:

Crawl the metro data with `amap_metro_api.py`

$ python amap_metro_api.py BJ amap.bj.metro.json

Step 2:

Run metro exchange program to get exchange plan

# python metro_exchange.py amap.bj.metro.json 苹果园 南锣鼓巷 1
"""

import sys
import json
import math
import heapq
import logging
import argparse
import networkx as nx
import matplotlib.pyplot as plt


def degree_to_radians(degrees):
    return math.pi / 180 * degrees


def distance_in_km_between_earth_coordinates(lat1, lon1, lat2, lon2):
    """
    Calcuate the distance between two coordinates by KM
    Ref: https://stackoverflow.com/questions/365826/calculate-distance-between-2-gps-coordinates
    """
    earthRadiusKm = 6371
    dLat = degree_to_radians(lat2 - lat1)
    dLon = degree_to_radians(lon2 - lon1)

    lat1 = degree_to_radians(lat1)
    lat2 = degree_to_radians(lat2)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earthRadiusKm * c


def distance_heuristic(stations_meta, from_node, cur_node, to_node):
    """
    Distance base heuristic function
    (A.K.A shortest path)
    """
    gn = distance_in_km_between_earth_coordinates(
        stations_meta[to_node]['lat'], stations_meta[to_node]['lon'],
        stations_meta[cur_node]['lat'], stations_meta[cur_node]['lon'],
    )
    fn = distance_in_km_between_earth_coordinates(
        stations_meta[to_node]['lat'], stations_meta[to_node]['lon'],
        stations_meta[from_node]['lat'], stations_meta[from_node]['lon'],
    )
    return gn + fn


def normalize_distance(max_dist, node1, node2):
    dist = distance_in_km_between_earth_coordinates(
        stations_meta[node1]['lat'], stations_meta[node1]['lon'],
        stations_meta[node2]['lat'], stations_meta[node2]['lon'],
    )
    return dist / max_dist


def distance_and_line_heuristic(w1=0.5, w2=0.25, w3=0.25):
    """
    Heuristic function base on distance and line information
    (A.K.A least exchange plan)
    """
    max_dist = find_max_distance_in_graph(stations_meta)

    def wrapper(stations_meta, from_node, cur_node, to_node):
        dgn = normalize_distance(max_dist, cur_node, to_node)
        dfn = normalize_distance(max_dist, from_node, cur_node)

        gn = w1 * dgn + w2 * (0 if len(stations_meta[to_node]['lines'] & stations_meta[cur_node]['lines']) != 0 else 1)
        fn = w1 * dfn + w2 * (0 if len(stations_meta[from_node]['lines'] & stations_meta[cur_node]['lines']) != 0 else 1)

        return gn + fn
    return wrapper


def heuristic(stations_meta, from_node, cur_node, to_node, algorithm):
    """
    Heuristic funciton: h(n) = f(n) + g(n)
    """
    return algorithm(stations_meta, from_node, cur_node, to_node)


def astar_search_with_priority_queue(graph, stations_meta, from_node, to_node, strategy):
    """
    A* search with priority queue
    Find the route in `graph` from `from_node` to `to_node` with A* search

    :params dict graph:         The metro station grap
    :params dict stations_meta: A dict for metro station meta data
    :param str from_node:       Station from, eg., 苹果园
    :param str to_node:         To which station, eg., 南锣鼓巷
    :param int strategy:        The exchange strategy, 1 - shortest distance, 2 - less exchange
    :returns: A optimal path from `from_node` to `to_node`
    """
    assert strategy in [1, 2], 'not support strategy {}'.format(strategy)

    if strategy == 1:
        strategy_func = distance_heuristic
    else:
        strategy_func = distance_and_line_heuristic()

    pending = []
    seen = set()
    path = []

    dist = heuristic(stations_meta, from_node, from_node, to_node, strategy_func)
    heapq.heappush(pending, (dist, from_node))

    while len(pending) > 0:
        cur_node = heapq.heappop(pending)[1]
        if to_node == cur_node:
            path.append(cur_node)
            return path

        if cur_node in seen:
            continue

        neighbors = graph[cur_node]
        for neighbor in neighbors:
            if neighbor not in pending:
                dist = heuristic(stations_meta, from_node, neighbor, to_node, strategy_func)
                heapq.heappush(pending, (dist, neighbor))

        path.append(cur_node)
        seen.add(cur_node)


FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def draw_graph(graph):
    gph = nx.Graph(graph)
    plt.subplot()
    nx.draw(gph, with_labels=True, node_size=4, font_size='8')
    plt.show()
    input()


def build_metro_stations_meta(metro):
    """
    Build a metro stations meta data map:
    {
        '苹果园', {'lon': 116.177388, 'lat': 39.926727, lines: ['1号线']},
        '古城': {'lon': 116.190337, 'lat': 39.907450, lines: ['1号线']},
        ...
    }
    """
    try:
        meta = {}
        for line in metro['lines']:
            for st in line['stations']:
                st_name = st['station']
                try:
                    item = meta[st_name]
                    item['lines'].add(line['line_name'])
                except KeyError:
                    meta[st_name] = {
                        'lon': st['lon'],
                        'lat': st['lat'],
                        'lines': set([line['line_name']])
                    }
        return meta
    except Exception:
        logger.exception('metro file format not correct')


def build_metro_graph(metro):
    """
    Build a metro station map like this:
    {
        "鼓楼大街": {"安德里北街", "积水潭", "安定门", "什刹海"},
        "苹果园": {"古城"},
        ...
    }
    """
    try:
        lines = metro['lines']
        stations = {}
        for line in lines:
            prev_st = ''
            nodes = line['stations']
            for node in nodes:
                st_name = node['station']
                if st_name not in stations:
                    stations[st_name] = set()

                if prev_st != '':
                    stations[st_name].add(prev_st)
                    stations[prev_st].add(st_name)

                prev_st = st_name

        return stations
    except Exception:
        logger.exception('metro file format not correct')


def find_max_distance_in_graph(stations_meta):
    """
    Find the max distance between two nodes in the graph
    """
    return max([
        distance_in_km_between_earth_coordinates(
            stations_meta[left]['lat'], stations_meta[left]['lon'],
            stations_meta[right]['lat'], stations_meta[right]['lon'],
        )
        for left in stations_meta.keys() for right in stations_meta.keys() if left != right
    ])


def load_metro(path):
    with open(path, 'r') as f:
        metro = json.load(f)
        return metro


def print_path(path):
    print(' -> '.join(path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'data',
        type=str,
        help='The metro map json'
    )
    parser.add_argument(
        'from_station',
        type=str,
        help='From station'
    )
    parser.add_argument(
        'to_station',
        type=str,
        help='To station'
    )
    parser.add_argument(
        'strategy',
        type=int,
        help='Exchange strategy, 1 - Less exchange, 2 - Less stations, 3 - More stations'
    )
    args = parser.parse_args(sys.argv[1:])

    metro = load_metro(args.data)
    graph = build_metro_graph(metro)
    # draw_graph(graph)

    stations_meta = build_metro_stations_meta(metro)

    dist = distance_in_km_between_earth_coordinates(
        stations_meta[args.from_station]['lat'], stations_meta[args.from_station]['lon'],
        stations_meta[args.to_station]['lat'], stations_meta[args.to_station]['lon'],
    )
    print('Distance between {} and {} is {:.2f}km'.format(
        args.from_station,
        args.to_station,
        dist,
    ))

    path = astar_search_with_priority_queue(
        graph, stations_meta, args.from_station, args.to_station, args.strategy
    )
    print_path(path)
