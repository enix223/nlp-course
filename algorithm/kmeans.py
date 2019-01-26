#!/usr/bin/python

"""
==================
k-Means clustering
==================

Ref: https://en.wikipedia.org/wiki/K-means_clustering

Observations: (x1, x2, .., xn)
Each observation got m features
Partition observations into k cluster (k <= n), S = (s1, s2, ..., sk)
Target: minimize within-cluster sum of squqre:

           k                                 k
    argmin ∑   ∑    ||x - Ui||^2  =  argmin  ∑  |Si| Var Si
     S    i=1 x∊Si                      S   i=1

Equivalent to:

           k
    argmin ∑  1 / (2 * |Si|)   ∑   || x - y ||^2
      S   i=1               x,y∊Si

x2
^
|
|     o
|  o    o               x
|    o  o  o        x
|   o   o       x   x    x   x
|       o          x    x
|                x      x
|
+------------------------------> x1

Standard algorithm
==================

1) initial set of k means m1(1),...,mk(1)
2) Assignment step: Si(t) = {xp: ||xp - mi(t)||^2 <= ||xp - mj(t)||^2, for all j, i <= j <= k}
3) Update the centroid: mi(t+1) = 1 / |Si(t| * ∑ xj

Initialization methods:

1) Forgy method: Randomly choose k observations from the dataset, and use them as the initial mean
2) Random partition method: Randomly assigns a cluster to each observation, and the process the update step.

Implementation
==================

Centroid matrix (A), cm(k) denote the mth feature of the k centroid:

| (c1(1), c2(1), ..., cm(1)) |
| (c1(2), c2(2), ..., cm(2)) |
| (c1(3), c2(3), ..., cm(3)) |
|             ...            |
| (c1(k), c2(k), ..., cm(k)) |

Observation matrix (B), xm(n) denotes the mth feature of nth observation:

| ( x1(1), x2(1), ..., xm(1)) |
| ( x1(2), x2(2), ..., xm(2)) |
| ( x1(3), x2(3), ..., xm(3)) |
|             ...             |
| ( x1(n), x2(n), ..., xm(n)) |

Observation cluster class vector (C), k(Xi) denotes cluster class for Xi:

| k(X1) |
| k(X2) |
| ..    |
| k(Xn) |
"""

import pandas as pd
import numpy as np
import random


class KMeansCluster(object):
    """
    k-Meanus cluster implementation
    """
    def __init__(self, k_class: int, init_function='forgy'):
        """
        """
        self.no_of_classes = k_class
        self.cluster = None    # observations' cluster vector (C)
        self.centroids = None  # centroid matrix (A)
        self.dataset = None    # dataset (B)

        if init_function not in ('forgy', 'partition'):
            raise 'unsupport initialize method: %s' % init_function

        self.init_function = init_function

    def calculate_centroids(self, dataset):
        """Calculate centroid for each class
        """
        for k in range(self.no_of_classes):
            indexes = self.cluster[self.cluster == k].indexes
            dataset_in_cluster_k = dataset[indexes]
            self.centroids.iloc[k] = np.sum(dataset_in_cluster_k, axis=0) / dataset_in_cluster_k.shape[0]

    def init_forgy_random(self, dataset: pd.DataFrame):
        rand_samples = random.sample(range(len(self.dataset)), self.no_of_classes)
        self.centroids = dataset.loc[rand_samples, :]

    def init_random_partition(self, dataset: pd.DataFrame):
        self.cluster = pd.Series(np.random.randint(0, self.no_of_classes, dataset.shape[0]))

        # calculate centroids
        self.calculate_centroids()

    def train(self, dataset: pd.DataFrame, iterations: int):
        if self.no_of_classes > dataset.shape[0]:
            raise '# of classes should not greater than total # of observations'

        if self.init_function == 'forgy':
            self.init_forgy_random()
        elif self.init_function == 'partition':
            self.init_random_partition()
        else:
            raise 'unsupport initialize method: %s' % self.init_function

        for i in range(self.iterations):
            for x in self.dataset:
                dists = [(kcls, np.linalg.norm(x - centroid)) for kcls, centroid in self.centroids.items()]
                kclass = min(dists, key=lambda x: x[1])
                self.classes[kclass] = np.vstack((self.classes[kclass], x))


if __name__ == '__main__':
    df = pd.read_csv('../data/titanic/train.csv')
    df1 = df.loc[:, ('Age', 'Fare')].dropna(how='any')
    dataset = np.array(df1)
    model = KMeansCluster(3, dataset, 3)
    model.train()
