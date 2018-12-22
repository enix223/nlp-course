#!/usr/local/env python

"""
========================
Maximum subarray problem
========================

Ref: https://en.wikipedia.org/wiki/Maximum_subarray_problem

Problem
-------

Suppose we have an array: [−2, 1, −3, 4, −1, 2, 1, −5, 4], and the largest sum
is [4, −1, 2, 1], with sum 6.

Usage Example
-------------

# Find max subarray with given input
$ python algorithm/find_max_subarray.py

# Show divide and conquer and exhaustion search performance comparison
$ python algorithm/find_max_subarray.py --performance
"""

from matplotlib import pyplot as plt
import numpy as np
import argparse
import time
import sys


def benchmark(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = fn(*args, **kwargs)
        end = time.time()
        return res, end - start

    return wrapper


@benchmark
def find_max_subarray_with_divide_and_conquer(arr):
    """
    Find the maximum subarray with divide and conquer algorithm
    """
    def find_max_crossing_subarray(arr, lft, mid, rgh):
        lft_total = float('-inf')
        subsum = 0
        lft_bound = mid
        for i in range(mid, lft - 1, -1):
            subsum += arr[i]
            if subsum > lft_total:
                lft_bound = i
                lft_total = subsum

        rgh_total = float('-inf')
        subsum = 0
        rgh_bound = mid
        for i in range(mid + 1, rgh + 1):
            subsum += arr[i]
            if subsum > rgh_total:
                rgh_bound = i
                rgh_total = subsum

        return lft_bound, rgh_bound, lft_total + rgh_total

    def find_max_sub_array(arr, lft, rgh):
        if lft == rgh:
            # base case
            return lft, rgh, arr[lft]
        else:
            mid = (rgh - lft) // 2 + lft
            # Max subarray in the left half side
            llft, lrgh, lft_max = find_max_sub_array(arr, lft, mid)
            # Max subarray in the right half side
            rlft, rrgh, rgh_max = find_max_sub_array(arr, mid + 1, rgh)
            # Max subarray cross middle
            mlft, mrgh, cross_max = find_max_crossing_subarray(arr, lft, mid, rgh)

            if lft_max >= rgh_max and lft_max >= cross_max:
                return llft, lrgh, lft_max
            elif rgh_max >= lft_max and rgh_max >= cross_max:
                return rlft, rrgh, rgh_max
            else:
                return mlft, mrgh, cross_max

    return find_max_sub_array(arr, 0, len(arr) - 1)


@benchmark
def find_max_subarray_with_exhaustion_search(arr):
    totalsum = float('-inf')
    lft, rgh = -1, -1
    for i in range(0, len(arr)):
        subsum = 0
        for j in range(i, len(arr)):
            subsum += arr[j]
            if subsum > totalsum:
                lft, rgh, totalsum = i, j, subsum

    return lft, rgh, totalsum


@benchmark
def find_max_subarray_with_shortest_path(arr):
    pass


@benchmark
def find_max_subarray_with_dynamic_programming(arr):
    pass


@benchmark
def find_max_subarray_with_kadane_algorithm(arr):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Show performance'
    )
    args = parser.parse_args(sys.argv[1:])

    if not args.performance:
        arr_str = input('Please input the array, item separated by space: ')
        arr = list(map(int, arr_str.split(' ')))

        (lft, rgh, subsum), elpase = find_max_subarray_with_divide_and_conquer(arr)
        print('[Divide and conquer] subarray: {}, sum: {}, elapse time: {}'.format(arr[lft:rgh + 1], subsum, elpase))

        (lft, rgh, subsum), elpase = find_max_subarray_with_exhaustion_search(arr)
        print('[Method of exhaustion] subarray: {}, sum: {}, elapse time: {}'.format(arr[lft:rgh + 1], subsum, elpase))
    else:
        dc_times = []
        es_times = []
        sizes = []
        arr_size = 1000
        arr = np.random.randint(-10, 10, arr_size)
        for size in range(10, arr_size + 10, 10):
            print('\rSize: {}/{}'.format(size, arr_size), end='', flush=True)
            _, dc_elpase = find_max_subarray_with_divide_and_conquer(arr[:size])
            _, es_elpase = find_max_subarray_with_exhaustion_search(arr[:size])
            dc_times.append(dc_elpase)
            es_times.append(es_elpase)
            sizes.append(size)

        fig, (ax1, ax2) = plt.subplots(2)
        split_point = 20
        ax1.plot(sizes[:split_point], dc_times[:split_point], label='Divide and conquer')
        ax1.plot(sizes[:split_point], es_times[:split_point], label='Exaustion search')

        ax2.plot(sizes[split_point:], dc_times[split_point:], label='Divide and conquer')
        ax2.plot(sizes[split_point:], es_times[split_point:], label='Exaustion search')

        ax1.set_title('Maximum Subarray Problem')
        plt.xlabel('Question size')
        plt.ylabel('Elapse times (sec.)')
        plt.legend()
        plt.show()
