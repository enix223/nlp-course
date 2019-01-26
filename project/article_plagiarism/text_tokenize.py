"""
==================
Article plagiarism
==================

Goal
====
Build word tokens for training set and test set

Usage
=====

$ python text_tokenize.py \
    ./train.pkl \
    ./test.pkl \
    ./train.tokens.pkl \
    ./test.tokens.pkl
"""

import pandas as pd
import argparse
import logging
import jieba
import sys
import re


FORMAT = '%(asctime)-15s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def delete_punctuation(text):
    """Delete punctuation
    @ref: https://github.com/fxsjy/jieba/issues/169
    :param text The text to remove punctuations
    :return Text without punctuations
    """
    text = re.sub(r'[^0-9A-Za-z\u4E00-\u9FFF]+', ' ', text)
    return text


def cut(content):
    """Remove punctations and tokenized the content
    :param content str The content to be tokenized
    :return A list with tokens
    """
    return jieba.lcut(delete_punctuation(content))


def load_data_set(path):
    """Load data set from pkl file
    :param args command line arguments
    :return pd.DataFrame
    """
    data = pd.read_pickle(path)
    return data


def tokenize_contents(args, df: pd.DataFrame, step: int, outpath: str) -> pd.Series:
    """Tokenized the content column for dataframe df
    :param args command     line arguments
    :param df pd.DataFrame  corpus dataframe
    :param step int         # of step
    :param outpath          The tokenized output path
    :return Dataframe with extra column 'token' keeps the tokenzed result
    """
    if args.restart <= step:
        series = df['content'].astype('U').apply(cut)
        series.to_pickle(outpath)
    else:
        logger.info('Skipped')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trainpath', type=str, help='Training set pickle file path')
    parser.add_argument('testpath', type=str, help='Test set pickle file path')
    parser.add_argument('traintokenpath', type=str, help='Training set tokenized corpus output file path')
    parser.add_argument('testtokenpath', type=str, help='Test set tokenized corpus output file path')
    parser.add_argument('--restart', type=int, default=0, help='Restart from which step')
    args = parser.parse_args(sys.argv[1:])
    total_steps = 4

    logger.info('[1/%d] Loading train set...' % total_steps)
    train_set = load_data_set(args.trainpath)

    logger.info('[2/%d] Loading test set...' % total_steps)
    test_set = load_data_set(args.testpath)

    logger.info('[3/%d] Tokenizing training set "contents" column...' % total_steps)
    token_series = tokenize_contents(args, train_set, 2, args.traintokenpath)

    logger.info('[4/%d] Tokenizing test set "contents" column...' % total_steps)
    token_series = tokenize_contents(args, test_set, 3, args.testtokenpath)

    logger.info('DONE')
