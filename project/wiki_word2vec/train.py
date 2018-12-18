#!/usr/local/env python

"""
==========================
Wikipedia - Word2Vec train
==========================

Usage Example

$ python train.py ../../data/zhwiki/ ../../data/zhwiki.model
"""

import os
import sys
import glob
import time
import jieba
import random
import logging
import argparse
import functools
from multiprocessing import Process
from multiprocessing import cpu_count

from gensim.models.word2vec import LineSentence
from gensim.models import Word2Vec

FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


def tokenize_corpus(path, index):
    logger.info('Processing {}'.format(path))
    with open('/tmp/tokenize.{}.cache'.format(index), 'a') as out:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                for token in jieba.cut(line):
                    out.write(token)
                    out.write(' ')
                out.write('\n')


def clear_cache():
    logger.debug('Clearing cache...')
    for fpath in glob.glob('/tmp/tokenize.*.cache'):
        os.remove(fpath)


@benchmark
def tokenize_corpus_task(source):
    """
    [1, 2, 3, 4], [5, 6, 7, 8]. [9, 10]
    """
    clear_cache()

    files = glob.glob(source + '/*/wiki_*')
    worker_cnt = cpu_count()

    workers = []
    i = 0
    for idx, fpath in enumerate(files):
        logger.debug('Spawning process {} for worker {}...'.format(idx, i))
        p = Process(target=tokenize_corpus, args=(fpath, i))
        workers.append(p)
        p.start()
        i += 1

        if idx != 0 and (idx + 1) % worker_cnt == 0 or idx == len(files) - 1:
            i = 0
            for p in workers:
                p.join()
            workers = []

    logger.info('Tokenize done')


@benchmark
def combine_cache_files(outpath):
    logger.info('Combining tokenized corpus...')
    with open(outpath, 'w') as out:
        for fpath in glob.glob('/tmp/tokenize.*.cache'):
            with open(fpath, 'r') as infile:
                for line in infile:
                    out.write(line)


@benchmark
def train_model(corpus_path, outpath):
    logger.info('Training model...')
    model = Word2Vec(LineSentence(corpus_path), workers=cpu_count())
    model.save(outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'source',
        type=str,
        help='The wikipedia source dir'
    )
    parser.add_argument(
        'outpath',
        type=str,
        help='The output path for word2vec model'
    )
    args = parser.parse_args(sys.argv[1:])

    temp_file = '/tmp/train.{}.cache'.format(random.randint(10000, 99999))
    tokenize_corpus_task(args.source)
    combine_cache_files(temp_file)
    train_model(temp_file, args.outpath)
