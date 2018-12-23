#!/usr/local/env python

"""
==========================
News option extraction
==========================

Usage
-----

$ python project/news_option_extraction/train.py --inpath data/corpus/news-token.txt --outpath data/corpus/news-model.model
"""

from gensim.models.word2vec import Word2Vec, LineSentence
from multiprocessing import cpu_count
import argparse
import sys


def train_model(inpath, outpath):
    model = Word2Vec(LineSentence(inpath), workers=cpu_count())
    model.save(outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--inpath',
        type=str,
        help='Path for the news'
    )
    parser.add_argument(
        '--outpath',
        type=str,
        help='Path for the news'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose mode'
    )
    args = parser.parse_args(sys.argv[1:])
    train_model(args.inpath, args.outpath)
