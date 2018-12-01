#!/usr/local/env python

"""
=====================
n-gram language model
=====================

P(B|A) = P(AB) / P(A) = P(A|B) * P(B) / P(A)

P(q1, q2, q3,..., qn) = P(q1) * P(q2|q1) * P(q3|q1, q2) ... P(qn|q1, q2, ..., qn-1)

1-gram
P(q1, q2, q3,..., qn) = P(q1) * P(q2) * P(q3) * ... P(qn)

2-gram:
P(q1, q2, q3,..., qn) = P(q1) * P(q2|q1) * P(q3|q2) * ... * P(qn|qn-1)

3-gram
P(q1, q2, q3,..., qn) = P(q1) * P(q2|q1) * P(q3|q2, q1) * ... * P(qn|qn-1, qn-2)

p(the dog barks STOP) = q(the|*,*)
                        * q(dog|*, the)
                        * q(barks|the, dog)
                        * q(STOP|dog, barks)

A natural estimate (the maximum likelihood estimate)

q(wi|wi-2, wi-1) = Count(wi-2, wi-1, wi) / Count(wi-2, wi-1)

eg., q(laughs|the, dog) = Count(the, dog, laughs) / Count(the, dog)

Usage example
================

```
$ python algorithm/ngram.py ./data/corpus/80k.tar.gz
```

Output
================
```
============= Unigram =============
前天晚上吃晚饭的时候 with probability: 1.4955028266700104e-31
前天晚上吃早饭的时候 with probability: 1.7401916983572983e-31

正是一个好看的小猫 with probability: 3.905027711320239e-25
真是一个好看的小猫 with probability: 1.226996189634442e-25

我无言以对，简直 with probability: 1.4806644228892432e-29
我简直无言以对 with probability: 4.314094808416538e-22

============= Bigram =============
前天晚上吃晚饭的时候 with probability: 3.830655537670635e-21
前天晚上吃早饭的时候 with probability: 9.780656732199309e-21

正是一个好看的小猫 with probability: 1.373904336105732e-16
真是一个好看的小猫 with probability: 2.9521067147550675e-17

我无言以对，简直 with probability: 8.204354844489807e-20
我简直无言以对 with probability: 1.7361296679197174e-17

============= Trigram =============
前天晚上吃晚饭的时候 with probability: 0.002522635332263671
前天晚上吃早饭的时候 with probability: 0.0015135811993582026

正是一个好看的小猫 with probability: 18.387976551092837
真是一个好看的小猫 with probability: 13.79098241331963

我无言以对，简直 with probability: 3.4321564434566185e-08
我简直无言以对 with probability: 8.237174898870543e-07
```
"""

import re
import sys
import gzip
import argparse
from functools import reduce, partial
from collections import Counter


def trim(x):
    return ''.join(re.findall(r'\w+', x.replace('\\n', '')))


def load_corpus(path):
    fopen = open
    if re.search(r'\S(.tar.gz)$', path):
        fopen = gzip.open

    with fopen(path, 'r') as f:
        raw = ''.join(re.findall(r'\w+', f.read().decode('utf-8').replace('\\n', '')))
        return raw


def get_probability_wrapper(corpus, count_fn):
    occurrencies = count_fn(corpus)
    min_value = min(occurrencies.values())
    total = sum(occurrencies.values())

    def wrapper(word):
        return occurrencies.get(word, min_value) / total

    return wrapper


# Each word's occurrency probability
get_one_word_prob = partial(
    get_probability_wrapper,
    count_fn=lambda corpus: Counter(corpus)
)


# Two conjunction words's occurrency probability
get_two_words_prob = partial(
    get_probability_wrapper,
    count_fn=lambda corpus: Counter((corpus[i:i + 2] for i in range(len(corpus) - 1)))
)

# There conjunction words's occurrency probability
get_three_words_prob = partial(
    get_probability_wrapper,
    count_fn=lambda corpus: Counter((corpus[i:i + 3] for i in range(len(corpus) - 2)))
)


def calculate_pair_prob(pair, model_fn):
    sentence1_prob = model_fn(pair[0])
    sentence2_prob = model_fn(pair[1])

    print('{} with probability: {}'.format(pair[0], sentence1_prob))
    print('{} with probability: {}'.format(pair[1], sentence2_prob))
    print()


def unigram_model(sentence, prob_fn):
    """
    Unigram model:
    P(w1, w2, w3, ..., wn) = P(w1) * P(w2) * P(w3) * ... * P(wn)
    """
    sentence_word_probs = (prob_fn(w) for w in sentence)
    sentence_prob = reduce(lambda x, y: x * y, sentence_word_probs)
    return sentence_prob


def bigram_model(sentence, word_prob_fn, two_words_prob_fn):
    """
    Bigram model:
    P(w1, w2, w3, ..., wn) = P(w1) * P(w2|w1) * P(w3|w2) * ... * P(wn|wn-1)
    where P(wn|wn-1) = P(wn, wn-1) / P(wn-1)

    P(w1, w2, w3, ..., wn) = P(w1) * P(w2, w1) / P(w1) * P(w3, w2) / P(w2) * ... * P(wn, wn-1) / P(wn-1)
    """
    first_word_prob = word_prob_fn(sentence[0])
    prob = first_word_prob
    for i in range(1, len(sentence) - 1):
        prob *= two_words_prob_fn(sentence[i - 1:i + 1]) / word_prob_fn(sentence[i - 1])
    return prob


def trigram_model(sentence, word_prob_fn, two_words_prob_fn, three_words_prob_fn):
    """
    Trigram model:
    P(w1, w2, w3, ..., wn) = P(w1) * P(w2|w1) * P(w3|w2, w1) * ... * P(wn|wn-1, wn-2)
    where P(wn|wn-1, wn-2) = P(wn-2, wn-1, wn) / P(wn-2, wn-1)
    """
    first_word_prob = word_prob_fn(sentence[0])
    second_words_prob = two_words_prob_fn(sentence[0:2]) / first_word_prob
    prob = first_word_prob * second_words_prob
    for i in range(2, len(sentence) - 2):
        prob *= three_words_prob_fn(sentence[i - 2:i + 1]) / two_words_prob_fn(sentence[i - 2:i])
    return prob


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('corpus', type=str, help='Corpus file path')
    args = parser.parse_args(sys.argv[1:])

    corpus = load_corpus(args.corpus)

    # Unigram
    get_one_word_probability = get_one_word_prob(corpus)
    unigram_model_fn = partial(unigram_model, prob_fn=get_one_word_probability)

    pair1 = ('前天晚上吃晚饭的时候', '前天晚上吃早饭的时候')
    pair2 = ('正是一个好看的小猫', '真是一个好看的小猫')
    pair3 = ('我无言以对，简直', '我简直无言以对')

    print('============= Unigram =============')
    calculate_pair_prob(pair1, unigram_model_fn)
    calculate_pair_prob(pair2, unigram_model_fn)
    calculate_pair_prob(pair3, unigram_model_fn)

    # Bigram
    print('============= Bigram =============')
    get_two_words_probability = get_two_words_prob(corpus)
    bigram_model_fn = partial(
        bigram_model,
        word_prob_fn=get_one_word_probability,
        two_words_prob_fn=get_two_words_probability,
    )

    calculate_pair_prob(pair1, bigram_model_fn)
    calculate_pair_prob(pair2, bigram_model_fn)
    calculate_pair_prob(pair3, bigram_model_fn)

    # Trigram
    print('============= Trigram =============')
    get_three_words_probability = get_three_words_prob(corpus)
    trigram_model_fn = partial(
        trigram_model,
        word_prob_fn=get_one_word_probability,
        two_words_prob_fn=get_one_word_probability,
        three_words_prob_fn=get_three_words_probability,
    )

    calculate_pair_prob(pair1, trigram_model_fn)
    calculate_pair_prob(pair2, trigram_model_fn)
    calculate_pair_prob(pair3, trigram_model_fn)
