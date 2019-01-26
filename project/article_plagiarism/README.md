# Article Plagiarism

## Plan

### 1. What's your goal?    
Given an article, try to classify its source, with two class: `Published by Xinhua News` or `Not Published by Xinhua News`.

### 2. What's the main phrases for this task?    

1. Data cleansing & preprocessing. Exclude the training samples with `NaN` source in the corpus.  

2. Divide the corpus into two parts: `training` dataset (80%) and `test` dataset (20%)

3. Use jieba to cut the contents in the corpus, and build TF-IDF / Word2Vec vectors as training set features

4. Train the models with following algorithms
    * Use `logistic regression` to train the above training set. And use test set to test the model.
    * Use `kNN` to train the above training set. And use test set to test the model.
    * Use `Support vector machine` to train the above training set. And use test set to test the model.
    * Use `Decision tree` to train the above training set. And use test set to test the model.
    * Use `Random forest` to train the above training set. And use test set to test the model.
    * Use `XGBoost` to train the above training set. And use test set to test the model.
    * Use `K-means` to train the above training set. And use test set to test the model.

5. Compare the models' precision from step 4, and choose the best model as the final model

### 3. In each phrase, what’s your excepted, what’s the output?

* For step 1, the expected output should be a dataframe excluding records with `NaN` source
* For step 2, the expected output should be two dataframes, training set dataframe and test set dataframe
* For step 3, the expected output should be a TF-IDF vector or a Word2Vec vector
* For step 4, the expected output should be a set of trained models corresponding to different training algorithms.
* For step 5, the expected output should be the final trained model with the high precision.


## Implementation

### 1. Prepare dataset

Remove `NaN` data from the dataset, and split the data into training set (80%) and test set (20%)

* Related program: [prepare.py](prepare.py)

* Usage:

    ```shell
    python prepare.py \
        ../../data/corpus/sqlResult_1558435.csv \   # news corpus
        ./train.pkl \   # output training set pickle file
        ./test.pkl      # output test set pickle file
    ```

### 2. Build text tokens

Tokenize the document with jieba, and save the result to pickle

* Related program: [text_tokenize.py](text_tokenize.py)

* Usage:

    ```
    python text_tokenize.py \
        ./train.pkl \
        ./test.pkl \
        ./train.tokens.pkl \
        ./test.tokens.pkl
    ```

### 3. Build Text features

Build text features with doc2vec/CountVectorizer/TF-IDF

* Related programs
  * [text_features_doc2vec.py](text_features_doc2vec.py)
  * [text_features_countvec.py](text_features_countvec.py)
  * [text_features_tfidf.py](text_features_tfidf.py)

* Usage

    ```
    # Doc2Vec
    python text_features_doc2vec.py \
        ./train.pkl \
        ./train.doc2vec.model

    # Or CountVectorizer
    python text_features_countvec.py \
        ./train.pkl \
        ./train.countvec.model

    # Or TF-IDF
    python text_features_tfidf.py \
        ./train.pkl \
        ./train.tfidf.model
    ```

### 4. Convert training/test set 'source' column to numeric

Class 1: source = '新华社'
Class 0: source != '新华社'

* Related programs
  * [convert_source_label.py](convert_source_label.py)

* Usage

    ```
    python convert_source_label.py \
        ./train.pkl \
        ./test.pkl \
        ./train.label.pkl \
        ./test.label.pkl
    ````

### 5. Train and test with single algorithm

Train the above data with different algorithm, and compare the result

Algorithms used in this project:

* [Logistic regression](https://en.wikipedia.org/wiki/Logistic_regression)
* [SVM](https://en.wikipedia.org/wiki/Support-vector_machine)
* [Decision tree](https://en.wikipedia.org/wiki/Decision_tree)
* [Random forest](https://en.wikipedia.org/wiki/Random_forest)

Usage

* `Logistic Regression`

    ```
    python train_logistic_regression.py \
        ./train.features.pkl \
        ./test.features.pkl \
        ./train.label.pkl \
        ./test.label.pkl
    ```

    Output:
    ```
    2019-01-26 17:36:36,836 [INFO]: [1/6] Loading train vectorized dataset...
    2019-01-26 17:36:36,982 [INFO]: [2/6] Loading test vectorized dataset...
    2019-01-26 17:36:37,037 [INFO]: [3/6] Loading training set labels...
    2019-01-26 17:36:37,048 [INFO]: [4/6] Loading test set labels...
    2019-01-26 17:36:37,052 [INFO]: [5/6] Train logistic regression model with training set...
    2019-01-26 17:36:38,237 [INFO]: [6/6] Test model with test set...
    2019-01-26 17:36:38,268 [INFO]: Test set score: 0.92
    2019-01-26 17:36:38,268 [INFO]: DONE
    ```

* `SVM`

    ```
    python train_svm.py \
        ./train.features.pkl \
        ./test.features.pkl \
        ./train.label.pkl \
        ./test.label.pkl
    ```

    Output:
    ```
    2019-01-26 19:31:36,544 [INFO]: [1/6] Loading train vectorized dataset...
    2019-01-26 19:31:36,747 [INFO]: [2/6] Loading test vectorized dataset...
    2019-01-26 19:31:36,790 [INFO]: [3/6] Loading training set labels...
    2019-01-26 19:31:36,802 [INFO]: [4/6] Loading test set labels...
    2019-01-26 19:31:36,807 [INFO]: [5/6] Train SVM model with training set...
    2019-01-26 19:37:40,318 [INFO]: [6/6] Test model with test set...
    2019-01-26 19:38:12,537 [INFO]: Test set score: 0.94
    2019-01-26 19:38:12,537 [INFO]: DONE
    ```

* `Decision Tree`

    ```
    python train_decision_tree.py \
        ./train.features.pkl \
        ./test.features.pkl \
        ./train.label.pkl \
        ./test.label.pkl
    ```

    Output:
    ```
    2019-01-26 19:28:11,434 [INFO]: [1/6] Loading train vectorized dataset...
    2019-01-26 19:28:11,548 [INFO]: [2/6] Loading test vectorized dataset...
    2019-01-26 19:28:11,587 [INFO]: [3/6] Loading training set labels...
    2019-01-26 19:28:11,596 [INFO]: [4/6] Loading test set labels...
    2019-01-26 19:28:11,599 [INFO]: [5/6] Train Decision tree model with training set...
    2019-01-26 19:28:47,150 [INFO]: [6/6] Test model with test set...
    2019-01-26 19:28:47,205 [INFO]: Test set score: 0.87
    2019-01-26 19:28:47,205 [INFO]: DONE
    ```

* `Random forest`

    ```
    python train_random_forest.py \
        ./train.features.pkl \
        ./test.features.pkl \
        ./train.label.pkl \
        ./test.label.pkl
    ```

    Output:
    ```
    2019-01-26 21:03:48,635 [INFO]: [1/6] Loading train vectorized dataset...
    2019-01-26 21:03:48,804 [INFO]: [2/6] Loading test vectorized dataset...
    2019-01-26 21:03:48,874 [INFO]: [3/6] Loading training set labels...
    2019-01-26 21:03:48,891 [INFO]: [4/6] Loading test set labels...
    2019-01-26 21:03:48,897 [INFO]: [5/6] Train Random forest model with training set...
    2019-01-26 21:04:03,044 [INFO]: [6/6] Test model with test set...
    2019-01-26 21:04:03,121 [INFO]: Test set score: 0.91
    2019-01-26 21:04:03,121 [INFO]: DONE
    ```

## Reference

1. [How to Prepare Text Data for Machine Learning with scikit-learn](https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/)
2. [Wikipedia Plagiarism detection](https://en.wikipedia.org/wiki/Plagiarism_detection)
3. [Sciki-learn Feature extraction](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction)
4. [Doc2Vec Tutorial on the Lee Dataset](https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/doc2vec-lee.ipynb)
5. [Logistic regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html)
6. [Random forest](https://www.cnblogs.com/maybe2030/p/4585705.html)