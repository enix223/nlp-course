"""
============================================
Article plagiarism - Text feature extraction
============================================

Goal
====
Use doc2vec model to train the tokens,
and finally build document vector for further usage.

Usage
=====
$ python text_features_doc2vec.py \
    ./train.tokens.pkl \
    ./test.tokens.pkl \
    ./train.doc2vec.model \
    ./train.features.pkl \
    ./test.features.pkl
"""

from text_features_base import BaseTextFeatureExtractor

from gensim.models import doc2vec
import pandas as pd
import numpy as np


class Doc2VecTextFeatureExtractor(BaseTextFeatureExtractor):
    """Text feature extractor base on doc2vec model
    """
    def save_model(self, model, outpath):
        """Save model to given outpath
        :param model doc2vec.Doc2Vec The doc2vec model to save
        :param outpath str The output path for the doc2vec model
        """
        model.save(outpath)

    def load_model(self, modelpath):
        """Load doc2vec model from modelpath
        :param modelpath str The path for the doc2vec model
        :return doc2vec.Doc2Vec Doc2Vec model instance
        """
        return doc2vec.Doc2Vec.load(modelpath)

    def get_model_output_argument_help(self):
        return 'Doc2vec model output file path'

    def train_model(self, args, token_series: pd.Series):
        """Build doc2vec base on df dataframe
        :param args command line arguments
        :param df pd.DataFrame corpus dataframe
        """
        model = doc2vec.Doc2Vec(vector_size=100, min_count=2, epochs=40)
        docs = list(map(lambda x: doc2vec.TaggedDocument(x, []), token_series.values.tolist()))
        model.build_vocab(docs)
        model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)
        return model

    def convert_doc_to_vector(self, model: doc2vec.Doc2Vec, token_series: pd.Series, outpath):
        # Convert document tokens to numerical vector
        doc_mat = np.vstack([model.infer_vector(doc) for doc in token_series])
        # Build dataframe with above document vector
        df = pd.DataFrame(data=doc_mat, index=token_series.index)
        df.to_pickle(outpath)


if __name__ == '__main__':
    model = Doc2VecTextFeatureExtractor()
    model.train()
