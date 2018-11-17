#!/usr/local/env python


"""
=======================
Linear regression model
=======================

A Linear regression example to train and test the relationship between
Titanic passenger's age and fare

Usage example
================

```
python algorithm/linear_regression.py data/titanic/train.csv
```

Example Output
===============

```
Total run times 3.726408s.
Linear regression model params:
a = 1.3877787807814457e-16, b = 151.49999999999568, error = 2002.5044000000132
```

"""

import pandas as pd
import numpy as np
import argparse
import time
import sys


def benchmark(fn, *args, **kwarg):
    start = time.time()
    res = fn(*args, **kwarg)
    end = time.time()
    print('Total run times {:3f}s.'.format(end - start))
    return res


def cost_function(actual, hypothesis):
    return np.sum(np.abs(actual - hypothesis))


def lr_model(a, b, ages):
    return a * ages + b


def lr_train(path, learning_rate, epsilon, verbose=False):
    train_ds = pd.read_csv(path, delimiter=',')
    # exclude Age with NaN rows
    train_ds = train_ds[(~train_ds['Age'].isnull()) & (train_ds['Fare'] < 400) & (train_ds['Fare'] > 100)]
    ages = train_ds['Age']
    fares = train_ds['Fare']
    a, b = 1, 0

    directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
    while True:
        hypothesis = lr_model(a, b, ages)
        error = cost_function(fares, hypothesis)
        if error < epsilon:
            # acceptable
            return (a, b, error)
        else:
            # need further optimise
            errors = []
            for direction in directions:
                temp_a = a + learning_rate * direction[0]
                temp_b = b + learning_rate * direction[1]
                hypothesis = lr_model(temp_a, temp_b, ages)
                err = cost_function(fares, hypothesis)
                errors.append(err)

            # Get the direction index with minimum error
            if np.min(errors) > error:
                # we have reach a local minimum
                return (a, b, error)

            direction_idx = np.argmin(errors)
            a += learning_rate * directions[direction_idx][0]
            b += learning_rate * directions[direction_idx][1]
            if verbose:
                print('a = {}, b = {}, err = {}'.format(a, b, errors[direction_idx]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('train_path', type=str, help='Train dataset path')
    parser.add_argument('--learning_rate', type=float, help='The learning rate', default=0.1)
    parser.add_argument('--epsilon', type=float, help='The thresh value for error to stop iterate', default=1000)
    parser.add_argument('--verbose', action='store_true', help='Verbose mode')
    args = parser.parse_args(sys.argv[1:])

    a, b, error = benchmark(
        lr_train,
        args.train_path,
        args.learning_rate,
        args.epsilon,
        args.verbose
    )
    print('Linear regression model params:\na = {}, b = {}, error = {}'.format(a, b, error))
