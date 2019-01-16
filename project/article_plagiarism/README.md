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
