#!/usr/local/env python

"""
==========================
News option extraction
==========================

Usage
-----

$ python extraction.py ../../data/ltp_data_v3.4.0 \
    ../../data/corpus/sqlResult_1558435.csv \
    ../../data/corpus/news-model.model \
    ../../data/news/options.csv
"""

import os
import sys
import logging
import argparse
import pandas as pd

from pyltp import Parser
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

from gensim.models.word2vec import Word2Vec


FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class NewsOptionExtractor:
    def __init__(self, ltp_path, news_path, news_model, outpath):
        # Initialize
        logger.info('Initializing...')
        self.outpath = outpath

        LTP_DATA_DIR = ltp_path  # ltp模型目录的路径
        cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
        pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
        ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')
        par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')

        self.segmentor = Segmentor()
        self.segmentor.load(cws_model_path)

        self.postagger = Postagger()
        self.postagger.load(pos_model_path)

        self.recognizer = NamedEntityRecognizer()
        self.recognizer.load(ner_model_path)

        self.parser = Parser()
        self.parser.load(par_model_path)

        # Read news data
        df = pd.read_csv(news_path, encoding='gb18030')
        self.contents = df[~df['content'].isnull()]['content']

        # Word2Vec Model
        NEWS_WORD2VEC_MODEL_PATH = news_model
        self.news_model = Word2Vec.load(NEWS_WORD2VEC_MODEL_PATH)

    def get_similar_words(self, word):
        words = dict(self.news_model.wv.most_similar(word))
        words[word] = 1
        return words

    def get_all_words_related_to(words, arcs, index):
        return [words[i] for i, arc in enumerate(arcs) if arc.head == index]

    def is_sentence_end(self, w):
        return w in ["。", "!", "！"]

    def print_option(self, option):
        logger.debug('{} {} {}'.format(option['name'], option['say'], option['sentence']))

    def save_result(self, options):
        df = pd.DataFrame(options)
        df.to_csv(self.outpath)

    def process(self):
        logger.info('Start to process contents...')
        options = []
        total = len(self.contents)
        for i, content in enumerate(self.contents):
            print('\rProccessing news {}/{}...'.format(i, total), end='', flush=True)
            # 1. split words
            words = self.segmentor.segment(content.replace('\r\n', ''))

            # 2. POS
            postags = self.postagger.postag(words)

            # 3. NER
            netags = self.recognizer.recognize(words, postags)

            # 4. Extract '说' and similar words from content
            say_words_dict = self.get_similar_words('说')
            say_positions = [(w, i) for i, w in enumerate(words) if w in say_words_dict]

            # 5. NER - extract all the names from the content
            all_names_positions = [(i, tag) for i, tag in enumerate(netags) if 'Nh' in tag]
            all_names = [(words[name[0]], name[0]) for name in all_names_positions]
            names = set(map(lambda x: x[0], all_names))

            # 6. 依存句法分析
            # arcs = self.parser.parse(words, postags)
            for say_word, pos in say_positions:
                option = {'say': say_word}
                # Get the name who say the words
                for i in range(pos, 0, -1):
                    w = words[i]
                    if w in names:
                        option['name'] = w
                        break

                if 'name' not in option:
                    # No name extracted
                    continue

                sentence = ''
                for w in words[pos + 1:]:
                    sentence += w
                    if self.is_sentence_end(w):
                        option['sentence'] = sentence
                        break

                if 'sentence' not in option:
                    continue

                options.append(option)
                # self.print_option(option)

        self.save_result(options)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'ltppath',
        type=str,
        help='LTP Model path'
    )
    parser.add_argument(
        'newspath',
        type=str,
        help='News path'
    )
    parser.add_argument(
        'newsmodel',
        type=str,
        help='News word2vec model path'
    )
    parser.add_argument(
        'outpath',
        type=str,
        help='Options output csv path'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose mode'
    )
    args = parser.parse_args(sys.argv[1:])

    extractor = NewsOptionExtractor(args.ltppath, args.newspath, args.newsmodel, args.outpath)
    extractor.process()
