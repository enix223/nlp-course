"""
==================
Article plagiarism
==================

Goal
=====

Load news corpus from csv file, exclude missing data, and split dataframe
into training set and test set, and save to pickle files for further use.

Usage
=====

$ python prepare.py \
    ../../data/corpus/sqlResult_1558435.csv \
    ./train.pkl \
    ./test.pkl
"""

import pandas as pd
import numpy as np
import argparse
import logging
import sys


FORMAT = '%(asctime)-15s [%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def split_data(df: pd.DataFrame):
    """Split the dataframe into train set (80%) and test set (20%)
    :param df pd.DataFrame The dataframe need to split
    :return (pd.DataFrame, pd.DataFrame) Train set and test set
    """
    size = int(df.shape[0] * 0.8)
    indexes = np.random.choice(df.index, size, replace=False)
    train_set = df.loc[indexes]
    test_set = df.loc[~df.index.isin(indexes)]
    return train_set, test_set


def prepare_data(args):
    """Load csv into dataframe and exclude missing data
    :param args The command line arguments
    """
    logger.info('Loading dataframe from %s' % args.newspath)
    df = pd.read_csv(args.newspath, encoding='gb18030')
    logger.info('Dataframe size: %d observations %d features after loaded' % (df.shape[0], df.shape[1]))

    # exclude rows with column source == NaN
    logger.info('Data cleansing...')
    df = df[~pd.isna(df['source'])]
    logger.info('Dataframe size: %d observations %d features after data cleansing' % (df.shape[0], df.shape[1]))

    # split the dataframe into training set and test set
    logger.info('Making training set & test set...')
    train_set, test_set = split_data(df)
    logger.info('Traning set size: %d' % train_set.shape[0])
    logger.info('Test set size: %d' % test_set.shape[0])

    # save the train set and test set to picke files
    logger.info('Save dataframes to files...')
    train_set.to_pickle(args.trainpath)
    test_set.to_pickle(args.testpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('newspath', type=str, help='News corpus path')
    parser.add_argument('trainpath', type=str, help='Training set output path')
    parser.add_argument('testpath', type=str, help='Test set output path')
    args = parser.parse_args(sys.argv[1:])

    prepare_data(args)
    logger.info('DONE')
