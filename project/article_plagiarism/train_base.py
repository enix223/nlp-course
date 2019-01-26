"""
================================================
Article plagiarism - Train - Logistic regression
================================================

Base class for ML model train and cross validation
"""

import pandas as pd
import argparse
import logging
import sys


class BaseTrainModel(object):
    name = ''

    def __init__(self, *args, **kwargs):
        FORMAT = '%(asctime)-15s [%(levelname)s]: %(message)s'
        logging.basicConfig(format=FORMAT)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def load_dataset(self, path):
        """Load data set from pkl file
        :param args command line arguments
        :return pd.DataFrame
        """
        dataset = pd.read_pickle(path)
        return dataset

    def add_arguments(self, parser):
        pass

    def train(self, train_set: pd.DataFrame, train_label: pd.Series, args):
        raise NotImplementedError

    def test(self, model, test_set: pd.DataFrame, test_label: pd.Series, args):
        raise NotImplementedError

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('trainvec', type=str, help='Training set vectors')
        parser.add_argument('testvec', type=str, help='Test set vectors')
        parser.add_argument('trainlabel', type=str, help='Training set label output file path')
        parser.add_argument('testlabel', type=str, help='Test set label output file path')
        self.add_arguments(parser)
        args = parser.parse_args(sys.argv[1:])
        return args

    def run(self):
        args = self.parse_arguments()
        total_steps = 6

        self.logger.info('[1/%d] Loading train vectorized dataset...' % total_steps)
        train_set = self.load_dataset(args.trainvec)

        self.logger.info('[2/%d] Loading test vectorized dataset...' % total_steps)
        test_set = self.load_dataset(args.testvec)

        self.logger.info('[3/%d] Loading training set labels...' % total_steps)
        train_labels = self.load_dataset(args.trainlabel)

        self.logger.info('[4/%d] Loading test set labels...' % total_steps)
        test_labels = self.load_dataset(args.testlabel)

        self.logger.info('[5/%d] Train %s model with training set...' % (total_steps, self.name))
        model = self.train(train_set, train_labels, args)

        self.logger.info('[6/%d] Test model with test set...' % total_steps)
        self.test(model, test_set, test_labels, args)

        self.logger.info('DONE')
