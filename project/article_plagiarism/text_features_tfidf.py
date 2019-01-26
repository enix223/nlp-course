"""
============================================
Article plagiarism - Text feature extraction
============================================

Goal
====
Use TF-IDF model to train the tokens,
and finally build document vector for further usage.

Usage
=====
$ python text_features_tfidf.py \
    ./train.pkl \
    ./train.tfidf.model
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from .text_features_base import BaseTextFeatureExtractor
import pandas as pd
import pickle


class TfidfTextFeatureExtractor(BaseTextFeatureExtractor):
    """Text feature extractor base on doc2vec model
    """
    def save_model(self, model, outpath):
        with open(outpath, 'wb') as f:
            pickle.dump(model, f)

    def get_model_output_argument_help(self):
        return 'TF-IDF model output file path'

    def train_model(self, args, token_series: pd.Series):
        """Build doc2vec base on df dataframe
        :param args command line arguments
        :param df pd.DataFrame corpus dataframe
        """
        docs = token_series.values.tolist()
        # create the transform
        vectorizer = TfidfVectorizer()
        # tokenize and build vocab
        model = vectorizer.fit_transform(docs)
        return model


if __name__ == '__main__':
    model = TfidfTextFeatureExtractor()
    model.train()
