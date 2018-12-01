#!/usr/local/env python

"""
==================
Bag of words model
==================

Reference:
[1]: https://en.wikipedia.org/wiki/Bag-of-words_model
[2]: https://machinelearningmastery.com/gentle-introduction-bag-words-model/

Example implementation
The following models a text document using bag-of-words. Here are two simple text documents:

(1) John likes to watch movies. Mary likes movies too.
(2) John also likes to watch football games.
Based on these two text documents, a list constructed as follows for each document:

"John","likes","to","watch","movies","Mary","likes","movies","too"

"John","also","likes","to","watch","football","games"
Representing each bag-of-words as a JSON object, and attributing to the respective Javascript variable:

BoW1 = {"John":1,"likes":2,"to":1,"watch":1,"movies":2,"Mary":1,"too":1};
BoW2 = {"John":1,"also":1,"likes":1,"to":1,"watch":1,"football":1,"games":1};
BoW3 = BoW1 + BoW2

Use the bag of words to represent the sentense:

eg.,

(1) [1, 2, 1, 1, 2, 1, 1, 0, 0, 0]
(2) [1, 1, 1, 1, 0, 0, 0, 1, 1, 1]
"""

import re
import sys
import gzip
import argparse
from collections import Counter


def trim(x):
    return ''.join(re.findall(r'\w+', x.replace('\\n', '')))


def load_corpus(path):
    fopen = open
    if re.search(r'\S(.tar.gz)$', path):
        fopen = gzip.open

    with fopen(path, 'r') as f:
        raw = ''.join(re.findall(r'\w+', f.read().decode('utf-8').replace('\\n', '')))
        return raw


def bag_of_words(corpus):
    return Counter(corpus)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str, help='Corpus file path')
    args = parser.parse_args(sys.argv[1:])

    corpus = load_corpus(args.corpus)
    bow = Counter(corpus)

    pair1 = ('前天晚上吃晚饭的时候', '前天晚上吃早饭的时候')
    pair2 = ('正是一个好看的小猫', '真是一个好看的小猫')
    pair3 = ('我无言以对，简直', '我简直无言以对')

    pair10_bow = Counter(pair1[0])
    pair11_bow = Counter(pair1[1])
    pair20_bow = Counter(pair1[0])
    pair21_bow = Counter(pair1[1])
    pair30_bow = Counter(pair1[0])
    pair31_bow = Counter(pair1[1])

    vec10 = [pair10_bow[k] if k in pair10_bow else 0 for k in bow]
    vec11 = [pair11_bow[k] if k in pair11_bow else 0 for k in bow]
    vec20 = [pair20_bow[k] if k in pair20_bow else 0 for k in bow]
    vec21 = [pair21_bow[k] if k in pair21_bow else 0 for k in bow]
    vec30 = [pair30_bow[k] if k in pair30_bow else 0 for k in bow]
    vec31 = [pair31_bow[k] if k in pair31_bow else 0 for k in bow]
