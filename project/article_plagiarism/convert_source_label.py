"""
============================================================
Article plagiarism - Convert news 'source' to numeric labels
============================================================

Goal
====
Convert the training set/test set 'source' column to numerical
labels

Class 1: News from '新华社'
Class 0: News not from '新华社'


Usage
=====
$ python convert_source_label.py \
    ./train.pkl \
    ./test.pkl \
    ./train.label.pkl \
    ./test.label.pkl
"""

import pandas as pd
import argparse
import logging
import sys

LABEL_XINHUA = 1
LABEL_NON_XINHUA = 0


FORMAT = '%(asctime)-15s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def convert(df: pd.DataFrame, outpath):
    """Apply news source checking function to source column
    :param df pd.DataFrame The news dataframe
    :param outpath str The pickle path to save the labels
    """
    labels = df['source'].apply(lambda x: LABEL_XINHUA if x == '新华社' else LABEL_NON_XINHUA)
    labels.to_pickle(outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('trainpath', type=str, help='Training set pickle file path')
    parser.add_argument('testpath', type=str, help='Test set pickle file path')
    parser.add_argument('trainlabel', type=str, help='Training set label output file path')
    parser.add_argument('testlabel', type=str, help='Test set label output file path')
    args = parser.parse_args(sys.argv[1:])

    total_steps = 4

    logger.info('[1/%d] Loading train dataset...' % total_steps)
    train_set = pd.read_pickle(args.trainpath)

    logger.info('[2/%d] Making labels for train dataset...' % total_steps)
    convert(train_set, args.trainlabel)

    logger.info('[3/%d] Loading test dataset...' % total_steps)
    train_set = pd.read_pickle(args.testpath)

    logger.info('[4/%d] Making labels for test dataset...' % total_steps)
    convert(train_set, args.testlabel)

    logger.info('DONE')
