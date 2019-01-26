"""
============================================
Article plagiarism - Text feature extraction
============================================

Goal
====
Use skilearn CountVectorizer model to train the tokens.

Usage
=====
$ python text_features_countvec.py \
    ./train.pkl \
    ./train.countvec.model
"""

from sklearn.feature_extraction.text import CountVectorizer
from .text_features_base import BaseTextFeatureExtractor
import pandas as pd
import pickle


class CounterVecTextFeatureExtractor(BaseTextFeatureExtractor):
    """Text feature extractor base on CountVectorizer model
    """
    def save_model(self, model, outpath):
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

    def get_model_output_argument_help(self):
        return 'CountVectorizer model output file path'

    def train_model(self, args, token_series: pd.Series):
        """Build CountVectorizer model base on df dataframe
        :param args command line arguments
        :param df pd.DataFrame corpus dataframe
        """
        docs = token_series.values.tolist()
        # create the transform
        vectorizer = CountVectorizer()
        # tokenize and build vocab
        vector = vectorizer.fit_transform(docs)
        vector.save(args.modelpath)


if __name__ == '__main__':
    model = CounterVecTextFeatureExtractor()
    model.train()
