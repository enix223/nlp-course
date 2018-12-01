#!/usr/local/env python

"""
================================
Good–Turing frequency estimation
================================

Reference: https://en.wikipedia.org/wiki/Good%E2%80%93Turing_frequency_estimation

X is the vocabulary set, so X = {x1, x2, x3, ..., xm}

W is a sequence with N independent sample, W = w1, w2, ..., wn, where wk ∈ X

ɵ[j] is the probability of xj being seen in the future.

Assumtion: if #(xj) = #(xk), then ɵ[j] = ɵ[k], in other word, xj and xk with the
same times in W, so they are with the same probability in general case.

θ(r) means the probability of a word occurring given that it appeared r times in W

Nr denote the number of item types that occur exactly r times in W
So, Nr = |{xj : #(xj ) = r}|.

Example, X = {the, dog, cat, bad}, W = {the, bad, cat, the, cat}
N0 = 1, cos dog not exist in W
N1 = 1, cos bad occurs 1 time
N2 = 2, cos the and cat both occurs 2 times

So, N = ∑ r * Nr

Good turning estimate for θ(r):  θ(r) = 1 / N * (1 + r) * Nr+1 / Nr

θ(0) = N1 / N

For a group of items which occur r times, the probability would be:

(1 + r) * Nr+1 / N

"""

import re
import sys
import gzip
import argparse
from collections import Counter
from matplotlib import pyplot as plt


def trim(x):
    return ''.join(re.findall(r'\w+', x.replace('\\n', '')))


def load_corpus(path):
    fopen = open
    if re.search(r'\S(.tar.gz)$', path):
        fopen = gzip.open

    with fopen(path, 'r') as f:
        raw = ''.join(re.findall(r'\w+', f.read().decode('utf-8').replace('\\n', '')))
        return raw


def get_nr(vocb: Counter, r: int):
    """
    Get number of items with occurring r times in vocabularies
    vocb = {'w1': r1, 'w2': r2, ..., 'wn': rn}

    Nr = |{xj : #(xj ) = r}|
    """
    return sum(1 if item[1] == r else 0 for item in vocb.items())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str, help='Corpus file path')
    args = parser.parse_args(sys.argv[1:])

    corpus = load_corpus(args.corpus)
    vocb = Counter(corpus)

    nrs = []
    max_freq = 1000  # max = vocb.most_common(1)[0][1]
    for i in range(max_freq):
        print('Processing r = %d' % i)
        if i == 0:
            nr = get_nr(vocb, 1)
        else:
            nr = get_nr(vocb, i)
        nrs.append(nr)

    plt.plot(range(max_freq), nrs)
    plt.xlabel('r')
    plt.ylabel('Nr')
    plt.show()
