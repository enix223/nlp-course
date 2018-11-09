#!/usr/bin/env python3

from functools import partial

"""
==========================
BFS - Breadth-first search
==========================

Intro: https://en.wikipedia.org/wiki/Breadth-first_search

BFS starts from the tree root, and explores all the neighbor nodes at the
present depth prior to moving on the nodes at the next depth level.

A
| \
B  D - F
|  |   |
C  G - I
| /
E

Suppose we have the tree as above, BFS starts from node `A`, and explores all
its descendant `B`, `D` before exploring the descendant of `B` and `D`.

The BFS loop sequence would be looked like this:

1) Traverse: A, seen: {'A'}, pending: ['B', 'D']
2) Traverse: B, seen: {'A', 'B'}, pending: ['D', 'C']
3) Traverse: D, seen: {'A', 'B', 'D'}, pending: ['C', 'F', 'G']
4) Traverse: C, seen: {'A', 'B', 'D', 'C'}, pending: ['F', 'G', 'E']
5) Traverse: F, seen: {'A', 'B', 'D', 'C', 'F'}, pending: ['G', 'E', 'I']
6) Traverse: G, seen: {'A', 'B', 'D', 'C', 'F', 'G'}, pending: ['E', 'I', 'E']
7) Traverse: E, seen: {'A', 'B', 'D', 'C', 'F', 'G', 'E'}, pending: ['I', 'E']
7) Traverse: I, seen: {'A', 'B', 'D', 'C', 'F', 'G', 'E', 'I'}, pending: ['E']
9) 'E' already seen, so skip it
10) pending is empty, loop finished.

==========================
DFS - Depth-first search
==========================

Intro: https://en.wikipedia.org/wiki/Depth-first_search

Let's also take the tree above as an example, the DFS loop sequence would look
like this:

1) Traverse: A, seen: {'A'}, pending: ['B', 'D']
2) Traverse: B, seen: {'A', 'B'}, pending: ['C', 'D']
3) Traverse: C, seen: {'A', 'B', 'C'}, pending: ['E', 'D']
4) Traverse: E, seen: {'A', 'B', 'C', 'E'}, pending: ['G', 'D']
5) Traverse: G, seen: {'A', 'B', 'C', 'E', 'G'}, pending: ['D', 'I', 'D']
6) Traverse: D, seen: {'A', 'B', 'C', 'E', 'G', 'D'}, pending: ['F', I', 'D']
7) Traverse: F, seen: {'A', 'B', 'C', 'E', 'G', 'D', 'F'}, pending: ['I', 'D']
8) Traverse: I, seen: {'A', 'B', 'C', 'E', 'G', 'D', 'F', 'I'}, pending: ['D']
9) 'D' already seen, so skip it
10) pending is empty, loop finished.
"""


def search_neighbor_first(tree, start_node, target):
    """
    Search all the neighbor nodes first before exploring the descendants
    If target is found, then return the path for the search.
    Otherwise, return empty list []

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start search
    :param target: The target node you need to find
    """
    seen = set()
    pending = [start_node]
    res = []

    while len(pending) > 0:
        node = pending.pop(0)
        if node in seen:
            continue

        descendant = tree[node]
        for item in descendant:
            if item not in seen:
                # Append the descendant nodes in the last of the list
                # So they would be explored later
                pending.append(item)

        seen.add(node)
        res.append(node)

        if node == target:
            return res

    return []


def search_descendant_first(tree, start_node, target):
    """
    Search the descendant nodes first before exploring the neighbors
    If target is found, then return the path for the search.
    Otherwise, return empty list []

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start search
    :param target: The target node you need to find
    """
    seen = set()
    pending = [start_node]
    res = []

    while len(pending) > 0:
        node = pending.pop(0)
        if node in seen:
            continue

        descendant = tree[node]
        for item in descendant:
            if item not in seen:
                # Insert the descendant nodes in the head of the list
                # So they would be explored first
                pending.insert(0, item)

        seen.add(node)
        res.append(node)

        if node == target:
            return res

    return []


def tranverse_neighbor_first(tree, start_node):
    """
    Tranverse all the neighbor nodes first before exploring the descendants

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start tranverse
    """
    seen = set()
    pending = [start_node]
    res = []

    while len(pending) > 0:
        node = pending.pop(0)
        if node in seen:
            continue

        descendant = tree[node]
        for item in descendant:
            if item not in seen:
                # Append the descendant nodes in the last of the list
                # So they would be explored later
                pending.append(item)

        seen.add(node)
        res.append(node)
    return res


def tranverse_descendant_first(tree, start_node):
    """
    Tranverse the descendant nodes first before exploring the neighbors

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start tranverse
    """
    seen = set()
    pending = [start_node]
    res = []

    while len(pending) > 0:
        node = pending.pop(0)
        if node in seen:
            continue

        descendant = tree[node]
        for item in descendant:
            if item not in seen:
                # Insert the descendant nodes in the head of the list
                # So they would be explored first
                pending.insert(0, item)

        seen.add(node)
        res.append(node)
    return res


def tranverse(func, tree, start_node):
    """
    Tranverse the tree

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start tranverse
    """
    return func(tree, start_node)


def print_tranverse_path(seq):
    """
    Print the tranverse path
    """
    for node in seq:
        print('I saw: {}'.format(node))


def search(func, tree, start_node, target):
    """
    Search the tree with target from start_node and return the path

    :param dict tree: A dictionary represent the tree
    :param start_node: The key of node to start search
    :param target: The target node you need to find
    """
    return func(tree, start_node, target)


def print_search_path(seq):
    """
    Print the search path
    """
    for idx, node in enumerate(seq):
        if idx == len(seq) - 1:
            print('I got you: {}'.format(node))
        else:
            print('I saw: {}'.format(node))


# Breadth-first tranverse
bft = partial(tranverse, tranverse_neighbor_first)

# Depth-first tranverse
dft = partial(tranverse, tranverse_descendant_first)

# Breadth-first search
bfs = partial(search, search_neighbor_first)

# Depth-first search
dfs = partial(search, search_neighbor_first)


if __name__ == '__main__':
    tree = {
        'A': 'B D',
        'B': 'A C',
        'C': 'B E',
        'D': 'A F G',
        'E': 'C G',
        'F': 'D I',
        'G': 'D E I',
        'I': 'F G',
    }

    tree = {k: set(v.split(' ')) for k, v in tree.items()}

    # Breadth-first tranverse
    print('Breadth-first tranverse from "A"...')
    res = bft(tree, 'A')
    print_tranverse_path(res)

    # Depth-first tranverse
    print('Depth-first tranverse from "A"...')
    res = dft(tree, 'A')
    print_tranverse_path(res)

    # Breadth-first tranverse
    print('Breadth-first tranverse from "E"...')
    res = bft(tree, 'E')
    print_tranverse_path(res)

    # Depth-first tranverse
    print('Depth-first tranverse from "E"...')
    res = dft(tree, 'E')
    print_tranverse_path(res)

    # Search
    print('Breadth-first search from "A" to find "F"...')
    res = bfs(tree, 'A', 'F')
    print_search_path(res)

    print('Depth-first search from "A" to find "F"...')
    res = dfs(tree, 'A', 'F')
    print_search_path(res)
