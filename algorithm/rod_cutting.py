#!/usr/local/env python

"""
=================================
Dynamic programming - Rod cutting
=================================

Refs:
[1]https://en.wikipedia.org/wiki/Dynamic_programming
"""

import sys
import time
import argparse
import functools
from collections import defaultdict


def benchmark(func):
    """
    Calcuate the running time for func
    """
    start = time.time()

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        rc = func(*args, **kwargs)
        print('Running time: {}'.format(time.time() - start))
        return rc
    return wrapper


def memo(func):
    """
    Cache the result for given function
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        try:
            return cache[key]
        except KeyError:
            rc = func(*args, **kwargs)
            cache[key] = rc
            return rc
    return wrapper


def memo_rod_cutting(price_table, cache_size=20):
    """
    Memorization version of rod cutting

    :param dict price_table: The rod pricing table
    :param int n: The length of the rod
    :param int cache_size: The cache size
    :returns: Solutions for the cutting and the optimal revenue
    """
    @functools.lru_cache(maxsize=cache_size)
    # @memo
    def wrapper(n):
        if n == 0:
            return 0

        revenue = max(
            [price_table[n - 1]] + [price_table[i - 1] + wrapper(n - i) for i in range(1, n)]
        )
        return revenue
    return wrapper


def memo_rod_cutting_with_solution(price_table, cache, cache_size=20):
    """
    Memorization version of rod cutting with solution

    :param dict price_table: The rod pricing table
    :param int cache: The dict to cache the solution
    :param int cache_size: The cache size
    :returns: A function to find optimal revenue and solution for rod cutting
    """
    @functools.lru_cache(maxsize=cache_size)
    # @memo
    def wrapper(n):
        if n == 0:
            return (0, 0)

        solution, revenue = max(
            [(n, price_table[n - 1])] + [(i, price_table[i - 1] + wrapper(n - i)) for i in range(1, n)],
            key=lambda x: x[1]
        )
        cache[n] = solution
        return revenue
    return wrapper


def solutions_builder(cache):
    """
    Build the solution with solution cache

    :param dict cache: A cache that keeps the rod cutting solutions
    """
    res = []

    def wrapper(n):
        if n not in cache:
            return res

        cut = cache[n]
        res.append(cut)
        wrapper(n - cut)
        return res
    return wrapper


@benchmark
def find_optimal_revenue(price_table, n):
    cutting = memo_rod_cutting(price_table, n)
    print('Rod with length {} optimal cutting revenue is {}'.format(
        args.length, cutting(args.length))
    )


@benchmark
def find_optimal_revenue_and_solution(price_table, n):
    cache = {}
    cutting = memo_rod_cutting_with_solution(price_table, cache, n)
    revenue = cutting(n)
    solutions = solutions_builder(cache)(n)
    print('Rod with length {} optimal cutting solution: {}, revenue: {}'.format(
        n,
        ' -> '.join(map(str, solutions)),
        revenue
    ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('length', type=int, help='The length of the rod')
    args = parser.parse_args(sys.argv[1:])

    price_table = defaultdict(lambda: -float('inf'))
    price_table.update(
        {k: r for k, r in enumerate([1, 5, 8, 9, 10, 17, 17, 20, 24, 30])}
    )

    # Find the optimal value without solution
    find_optimal_revenue(price_table, args.length)

    # Find the optimal value and solution path
    find_optimal_revenue_and_solution(price_table, args.length)
