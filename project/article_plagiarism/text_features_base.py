"""
============================================
Article plagiarism - Text feature extraction
============================================

Base class of text features extraction
"""
import pandas as pd
import argparse
import logging
import sys


class BaseTextFeatureExtractor(object):
    """Text feature extractor base class
    """
    def __init__(self, *args, **kwargs):
        self.total_steps = 6

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

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('traintokenpath', type=str, help='Training set tokenized pickle file path')
        parser.add_argument('testtokenpath', type=str, help='Test set tokenized pickle file path')
        parser.add_argument('modelpath', type=str, help=self.get_model_output_argument_help())
        parser.add_argument('trainvec', type=str, help='Training set vectors')
        parser.add_argument('testvec', type=str, help='Test set vectors')
        parser.add_argument('--restart', type=int, help='Restart from which step, total steps: %d' % self.total_steps)
        self.add_extra_arguments(parser)
        return parser.parse_args(sys.argv[1:])

    def train(self):
        args = self.parse_arguments()

        self.logger.info('[1/%d] Loading tokenized train set...' % self.total_steps)
        train_tokens = self.load_dataset(args.traintokenpath)

        self.logger.info('[2/%d] Loading tokenized test set...' % self.total_steps)
        test_tokens = self.load_dataset(args.testtokenpath)

        self.logger.info('[3/%d] Tarinig model...' % self.total_steps)
        if args.restart <= 3:
            model = self.train_model(args, train_tokens)
        else:
            self.logger.info('Skipped training model, load from %s' % args.modelpath)
            model = self.load_model(args.modelpath)

        self.logger.info('[4/%d] Saving model...' % self.total_steps)
        if args.restart <= 3:
            self.save_model(model, args.modelpath)
        else:
            self.logger.info('Skipped')

        self.logger.info('[5/%d] Converting training set to vectors...' % self.total_steps)
        if args.restart <= 5:
            self.convert_doc_to_vector(model, train_tokens, args.trainvec)
        else:
            self.logger.info('Skipped')

        self.logger.info('[6/%d] Converting test set to vectors...' % self.total_steps)
        if args.restart <= 6:
            self.convert_doc_to_vector(model, test_tokens, args.testvec)
        else:
            self.logger.info('Skipped')

        self.logger.info('DONE')

    def add_extra_arguments(self, parser):
        pass

    def train_model(self, args, token_series: pd.Series):
        raise NotImplementedError('Should be implemented by subclass')

    def load_model(self, modelpath):
        raise NotImplementedError('Should be implemented by subclass')

    def save_model(self, model, outpath):
        raise NotImplementedError('Should be implemented by subclass')

    def convert_doc_to_vector(self, model, token_series, outpath):
        raise NotImplementedError('Should be implemented by subclass')

    def get_model_output_argument_help(self):
        raise NotImplementedError('Should be implemented by subclass')
