"""
================================================
Article plagiarism - Train - Logistic regression
================================================

Ref: https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression

Goal
====
Use logistic regression to train the document vectors dataset, and
output a model for test

Usage
=====
$ python train_logistic_regression.py \
    ./train.features.pkl \
    ./test.features.pkl \
    ./train.label.pkl \
    ./test.label.pkl
"""

from sklearn.linear_model import LogisticRegression
from train_base import BaseTrainModel
import pandas as pd


class LogisticRegressionModel(BaseTrainModel):
    name = 'logistic regression'

    """Train and cross validate with Logistic regression model
    """
    def train(train_set: pd.DataFrame, train_label: pd.Series, args):
        """Train with logistic regression model
        :param train_set pd.DataFrame The vectorized training dataset
        :param train_label pd.Series The training set label
        :return Logistic regression model
        """
        clf = LogisticRegression(
            random_state=0, solver='lbfgs', multi_class='multinomial'
        ).fit(train_set, train_label)

        return clf

    def test(self, model, test_set: pd.DataFrame, test_label: pd.Series, args):
        """Test the model with test set
        :param test_set pd.DataFrame The vectorized test dataset
        :param test_label pd.Series The test set label
        """
        score = model.score(test_set, test_label)
        self.logger.info('Test set score: %.2f' % score)


if __name__ == '__main__':
    model = LogisticRegressionModel()
    model.run()
