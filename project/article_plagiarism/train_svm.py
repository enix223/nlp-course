"""
================================
Article plagiarism - Train - SVM
================================

Ref: https://scikit-learn.org/stable/modules/svm.html#support-vector-machines

Goal
====
Use SVM to train the document vectors dataset, and
output a model for test

Usage
=====
$ python train_svm.py \
    ./train.features.pkl \
    ./test.features.pkl \
    ./train.label.pkl \
    ./test.label.pkl
"""

from train_base import BaseTrainModel
from sklearn import svm
import pandas as pd
import numpy as np


class SVMModel(BaseTrainModel):
    name = 'SVM'

    """Train and cross validate with SVM model
    """
    def train(self, train_set: pd.DataFrame, train_label: pd.Series, args):
        """Train with logistic regression model
        :param train_set pd.DataFrame The vectorized training dataset
        :param train_label pd.Series The training set label
        :return SVM model
        """
        clf = svm.SVC(gamma='scale')
        clf.fit(train_set, train_label)

        return clf

    def test(self, model, test_set: pd.DataFrame, test_label: pd.Series, args):
        """Test the model with test set
        :param test_set pd.DataFrame The vectorized test dataset
        :param test_label pd.Series The test set label
        """
        test_predict = model.predict(test_set)
        score = np.where(test_predict == test_label)[0].shape[0] / test_label.shape[0]
        self.logger.info('Test set score: %.2f' % score)


if __name__ == '__main__':
    model = SVMModel()
    model.run()
