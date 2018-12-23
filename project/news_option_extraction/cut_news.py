#!/usr/local/env python

"""
==========================
News option extraction
==========================

Usage
-----

$ python project/news_option_extraction/cut_news.py --path data/corpus/sqlResult_1558435.csv
"""

from multiprocessing import cpu_count
import pandas as pd
import argparse
import jieba
import sys


def cut_corpus(path, outpath):
    jieba.enable_parallel(cpu_count())
    df = pd.read_csv(path, encoding='gb18030')
    contents = df[~df['content'].isnull()]['content']
    with open(outpath, 'w') as of:
        for news in contents:
            tokens = jieba.cut(news)
            for token in tokens:
                of.write(token)
                of.write(' ')
            of.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--path',
        type=str,
        help='Path for the news'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose mode'
    )
    args = parser.parse_args(sys.argv[1:])

    temp_file = '/tmp/news-token.txt'
    cut_corpus(args.path, temp_file)
