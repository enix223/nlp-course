"""
===================================
Information retrieval - Bool search
===================================

Word & document vector A:

        D1  D2  D3  D4  D5  ... Dn-1    Dn
w1      1   1   0   0   0   ... 0       0
w2      0   1   0   0   0   ... 0       0
w3      0   0   0   0   0   ... 0       0
...     ...
...     ...
wn      0   0   0   0   0   ... 0       1

Documents contain w1 and w2 = A[w1] & A[w2]

Usage
------------

$ python bool_search.py ../../data/chinese-novels/ '刺史 京城'
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from functools import reduce
import numpy as np

import argparse
import logging
import jieba
import sys
import os
import re

logger = logging.getLogger(__name__)
FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)


def cut(content):
    return ' '.join(jieba.cut(content))


def build_corpus(path):
    logger.debug('Building corpus...')
    corpus = []
    for f in os.listdir(path):
        if not f.endswith('.txt'):
            continue

        book_corpus = []
        for line in open(os.path.join(path, f), 'r'):
            book_corpus.append(cut(line))
        corpus.append(' '.join(book_corpus))

    logger.debug('Total documents: {}'.format(len(corpus)))
    return corpus


def search_book(corpus, search_words):
    vectorizer = TfidfVectorizer()

    # document * words vector
    logger.debug('Calculating tfidf...')
    tfidf = vectorizer.fit_transform(corpus)

    # words * document vector
    words_tfidf = tfidf.transpose()

    word_indexes = [vectorizer.vocabulary_[w] for w in search_words.split(' ')]

    word_docs = [set(np.where(words_tfidf[i].toarray()[0])[0]) for i in word_indexes]

    docs = reduce(lambda x, y: x & y, word_docs)

    logger.info('Search result for {}:'.format(search_words))
    for doc in docs:
        logger.info('=' * 100)
        content = corpus[doc]
        pat = re.compile('({})'.format('|'.join(search_words.split(' '))))
        content = pat.sub(r'########\g<1>########', content)
        logger.info(content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        type=str,
        help='Path for the book dir'
    )
    parser.add_argument(
        'search',
        type=str,
        help='Search words'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose mode'
    )
    args = parser.parse_args(sys.argv[1:])
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Build corpus
    corpus = build_corpus(args.path)
    search_book(corpus, args.search)
