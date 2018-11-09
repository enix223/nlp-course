# Environment setup

This lib written in `python3` and require the following packages:

```
jieba
```

Install requirements
```
pip install -r requirements.txt
```

# Usage

## 1. Spiral memory

```
# Run unittest
./spiral_mem.py

# Calculate the distance with given input
./spiral_mem.py 2345678

# Output: The Manhattan Distance between 2345678 to 1 is 1347
```

## 2. Sentence Candidates Parser

Note: 

If the parser could not separate your sentence correctly, please add your corpus to `userdict.txt`, eg., the parser split `特惠卡` into two tokens: `特惠` and `卡` and you want it as a whole, you need to add the following line into `userdict.txt`

```
特惠卡 n
```

This parser treat the tokens with the same `POS` as the substitutable values, so the possible values separated by `/` should have the same `POS`. If the default parser could not recognize the `POS` of the word, you need to add the word and POS into `userdict.txt`, eg.,

```
办理 v
贵宾卡 n
```

The above user dict tell the parser `办理` is a `verb`, whereas `贵宾卡` is a `noun`, 

```
# Run example sets
./sentence_parser.py

# Generate sentences with given input
./sentence_parser.py 网银/信用卡如何/怎样注销/开户?
```

## 3. Random Chinese Sentence Generator

1. Customize your gramma in `gramma.txt`

2. Run the following commands:

```
# Run example sets
./random_chinese.py

# Generate a random sentence with given input
./random_chinese.py sentence
./random_chinese.py noun_phrase
./random_chinese.py noun

# More command options:
./random_chinese.py -h

# With customized grammar
./random_chinese.py sentence --grammar custom-grammar.txt \
    --null_words null,nil,None \
    --phrase_separator ':' \
    --collection_separator ' , ' \
    --component_separator '+' \
    --verbose
```
