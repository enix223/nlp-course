#!/usr/local/env python

"""
===================================
Dynamic programming - Edit distance
===================================

Definition:
Given two strings, a and b, the edit distance d(a, b) is the min weight series
of edit operation to transform a into b.

Insertion: insert a char in to a, and then equals to b
Deletion: delete a char in a, and the equal to b
Substitution: substitute a char in a with char in b, and the get b

Suppose we have two string: a = a1, a2, ..., an and b = b1, b2, ..., bm,
Wdel: Weight for deletion
Wins: Weight for insertion
Wsub: Weight for substitution

| d(i, 0) = ∑ Wdel(ak), k = [1, i], where 1 <= i <= n
| d(0, j) = ∑ Wins(bk), k = [1, j], where 1 <= j <= m
|
|           | d(i - 1, j - 1),                        for a(i) = b(j)
| d(i, j) = |      | d(i - 1, j) + Wins(ai)
|           | min <| d(i, j - 1) + Wdel(bj)           for a(i) <> b(j)      for 1 <= i <= n, 1 <= j <= m
|           |      | d(i - 1, j - 1) + Wsub(ai, bj)
|

Refs:
[1] https://en.wikipedia.org/wiki/Edit_distance
[2] https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm
"""

import sys
import time
import argparse
import functools


def weight_insertion(ch):
    """
    Weight for insert char `ch`
    """
    return 1


def weight_deletion(ch):
    """
    Weight for delete char `ch`
    """
    return 1


def weight_substitution(ch1, ch2):
    """
    Weight for substitude char `ch1` with `ch2`
    """
    return 2


@functools.lru_cache(maxsize=20)
def edit_distance(seq1, seq2):
    """
    Calculate edit distance between string `seq1` and `seq2`

    :param str seq1: String 1
    :param str seq2: String 2
    :return int: The edit distance
    """
    if seq1 == seq2:
        return 0

    if len(seq2) == 0:
        return sum([weight_insertion(seq1[i]) for i in range(len(seq1))])

    if len(seq1) == 0:
        return sum([weight_deletion(seq2[i]) for i in range(len(seq2))])

    return min(
        weight_insertion(seq1[-1]) + edit_distance(seq1[:-1], seq2),
        weight_deletion(seq2[-1]) + edit_distance(seq1, seq2[:-1]),
        weight_substitution(seq1[-1], seq2[-1]) + edit_distance(seq1[:-1], seq2[:-1]) if seq1[:-1] != seq2[:-1] else 0
    )


def edit_distance_with_solution(cache):
    """
    A function to calculate edit distance between string `seq1` and `seq2`

    :param str seq1: String 1
    :param str seq2: String 2
    :return int: The edit distance calculation function
    """
    @functools.lru_cache(maxsize=20)
    def wrapper(seq1, seq2):
        key = '{}:{}'.format(seq1, seq2)
        if seq1 == seq2:
            cache[key] = []
            return 0

        if len(seq2) == 0:
            cache[key] = [{'op': 'I', 'ch': seq1[i]} for i in range(len(seq1))]
            return sum([weight_insertion(seq1[i]) for i in range(len(seq1))])

        if len(seq1) == 0:
            cache[key] = [{'op': 'D', 'ch': seq2[i]} for i in range(len(seq2))]
            return sum([weight_deletion(seq2[i]) for i in range(len(seq2))])

        op, distance = min(
            ({'key': '{}:{}'.format(seq1[:-1], seq2), 'op': 'I', 'ch': seq1[-1]}, weight_insertion(seq1[-1]) + wrapper(seq1[:-1], seq2)),
            ({'key': '{}:{}'.format(seq1, seq2[:-1]), 'op': 'D', 'ch': seq2[-1]}, weight_deletion(seq2[-1]) + wrapper(seq1, seq2[:-1])),
            ({'key': '{}:{}'.format(seq1[:-1], seq2[:-1]), 'op': 'S', 'ch': seq1[-1]}, weight_substitution(seq1[-1], seq2[-1]) + wrapper(seq1[:-1], seq2[:-1])) if seq1[:-1] != seq2[:-1] else ([], 0),
            key=lambda x: x[1]
        )
        # if 'key' in op:
        #     key = op.pop('key')

        cache[key] = op
        return distance
    return wrapper


# def build_solution(cache):
#     def wrapper(seq):
#         if seq


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('seq1', type=str, help='string1')
    parser.add_argument('seq2', type=str, help='string2')
    args = parser.parse_args(sys.argv[1:])

    dist = edit_distance(args.seq1, args.seq2)
    print('Min edit distance between "{}" and "{}" is {}'.format(
        args.seq1,
        args.seq2,
        dist
    ))

    cache = {}
    dist = edit_distance_with_solution(cache)(args.seq1, args.seq2)
    print('Min edit distance between "{}" and "{}" is {}'.format(
        args.seq1,
        args.seq2,
        dist
    ))
    print(cache)
