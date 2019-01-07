# Mini search engine for Chinese classic novels

## Usage

1. Crawl the novels from website

```
# Crawl the data from website, and save the content to {book}-{chapter}.txt
python crawler_china_classic_novels.py ../../data/chinese-novels
```

2. Use bool search to search keywords in these novels

```
# Search chapter which both contain '刺史' and '京城'
python bool_search.py ../../data/chinese-novels/ '刺史 京城'
```

----

## TODO

1. Save the corpus tokenized result to file and reuse the result for next search
2. Investigate to save the word TF-IDF result to file for next search
