#!/usr/bin/env python3
# Copyright (c) 2018 enix223 <enix223@163.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import random
import logging
import argparse

FORMAT = '[%(levelname)s]: %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
3. Random Chinese Sentence Generator
Writing a programming which could generate random Chinese sentences based on one grammar.
Your input grammar is:

simple_grammar = '''
    sentence => noun phrase verb_phrase
    noun_phrase => Article Adj* noun
    Adj* => null | Adj Adj*
    verb_phrase => verb noun_phrase
    Article => 一个 | 这个
    noun => 女人 | 篮球 | 桌子 | 小猫
    verb => 看着 | 坐在| 听着 | 看见
    Adj => 蓝色的 | 好看的 | 小小的
'''

Your task is define a function called generate, if we call generate('sentence'), you could see some
sentences like:
>> generate('sentence')
Output: 这个蓝色的女人看着一个小猫

>> generate('sentence')
Output: 这个好看的小猫坐在一个女人

Bonus: Can you modify your programming code, such that, if we change the grammar, we don’t need to
change source code, this program will generate sentence appropriately.
Of course, you may create more complicated grammar if you like


Analyst
=================

There are two steps for this parser to generate a random sentence by given input.

1. [Grammar building step] Load the grammar from the grammar definition file
2. [Sentence generating step] Generate the sentence by given user input phrase

For the grammar building step, the parser would parse the definition file to a dict which contain the
phrase and definition pair.

Meanwhile, the definition contains two types of elements:

1. A `set` which represent a possible value collections,
    eg., the possible values for `noun` is `女人`, `篮球`, `桌子`, `小猫`
2. A `tuple` which represent the components sequence for the phrase,
    eg., `verb_phrase` composite by a `verb` following by a `noun_phrase`

For example, the following line will be parse into a pair: `{'Article': set(['一个', '这个'])}`

```
Article => 一个 | 这个
```

for another grammar line below, the parser would produce: `{'verb_phrase': tuple(['verb', 'noun_phrase'])}`

```
verb_phrase => verb noun_phrase
```

So the final grammar dict may look like this:

```
{
    'sentence': ('noun_phrase', 'verb_phrase'),
    'noun_phrase': ('Article', 'Adj*', 'noun'),
    'Adj*': {('Adj', 'Adj*'), ('',)},
    'verb_phrase': ('verb', 'noun_phrase'),
    'Article': {('一个',), ('这个',)},
    'noun': {('篮球',), ('小猫',), ('女人',), ('桌子',)},
    'verb': {('坐在',), ('听着',), ('看着',), ('看见',)},
    'Adj': {('小小的',), ('蓝色的',), ('好看的',)}
}
```

For the sentence generating step, the parser will take the user input phrase, eg., `Article` and search the phrase
in the grammar dict, if definition is found, then recursively invoke the `generate` method until the definition
is not found, and the `phrase_name` would return.

Let's take `Article` as an example:

1. There is an definition entry for `Article`, and the defintion is a set, so random element would be choosen, eg., ('这个', )
2. Parser will invoke the `generate` method again for each element in tuple `('这个', )`
3. phrase_name = '这个', as this phrase is not found in our definition dict, so the phrase_name will be return directly
4. All elements from step2 are return and combine into a sentence, for this example, there is only an element,
   so the final sentence for `Article` will be '这个'.

Customize your parser
=====================

There are 5 options for you to customize your grammar when calling this script:

optional arguments:
  --grammar GRAMMAR         The path for your grammar file
  --phrase_separator        Separator for the name and the definition, default '=>'
  --collection_separator    Separator for phrase possible values, default ' | '
  --component_separator     Separator for the components to defined the whole phrase, deafult ' '
  --null_words              The null word list which will be converted to an empty string.
                            Separate the words by comma if multiple elements are provided, default 'null'
                            eg., --null_words null,nil,None
"""


class SentenceGenerator(object):
    def __init__(self,
                 phrase_separator='=>',
                 collection_separator=' | ',
                 component_separator=' ',
                 null_words=['null']):
        """Initialize a SentenceGenerator instance

        :param str phrase_separator:
            Separator for the name and the definition
        :param str collection_separator:
            Separator for phrase possible values
        :param str component_separator:
            Separator for the components to defined the whole phrase
        :param list null_words:
            The null word list which will be converted '' string
        """
        self.phrase_separator = phrase_separator
        self.collection_separator = collection_separator
        self.component_separator = component_separator
        self.null_words = null_words
        self.grammar = {}

    def escape_null_words(self, words):
        return ['' if w in self.null_words else w for w in words]

    def escape_null_word(self, word):
        return '' if word in self.null_words else word

    def load_grammar(self, path):
        """Load grammar from given `path`

        :param str path: The path to the grammar file
        """
        self.grammar.clear()
        with open(path, 'r') as f:
            for line in f:
                comps = line.split(self.phrase_separator)
                if len(comps) != 2:
                    logger.warning('Phrase definition syntax invalid: %s' % line)
                    continue

                phrase_name, definition = comps[0].strip(), comps[1].strip()

                # Test if the definition is a collection
                temp = definition.split(self.collection_separator)
                if len(temp) > 1:
                    collection = set()
                    for item in temp:
                        sub_col = item.split(self.component_separator)
                        if len(sub_col) > 1:
                            collection.add(tuple(self.escape_null_words(sub_col)))
                        else:
                            collection.add(tuple([self.escape_null_word(item)]))
                    self.grammar[phrase_name] = collection
                    continue

                # Test if the definition is a components
                temp = definition.split(self.component_separator)
                if len(temp) > 1:
                    temp = self.escape_null_words(temp)
                    self.grammar[phrase_name] = tuple(temp)
                    continue

                logger.warning('Invalid grammar syntax: %s' % line)

        logger.debug('Grammar: %s' % repr(self.grammar))

    def generate(self, phrase_name):
        """Generate a sentence from given `phrase`

        :param str phrase_name: The name of the phrase
        :return str: The random generated sentence
        """
        if not self.grammar:
            raise RuntimeError('Grammar not initialized, please call `load_grammar` first')

        phrase = self.grammar.get(phrase_name)
        if phrase is None:
            return phrase_name

        if isinstance(phrase, str):
            # A constant
            return phrase
        elif isinstance(phrase, set):
            # A collection
            token = random.sample(phrase, k=1)[0]
            if isinstance(token, tuple):
                tokens = []
                for sub_token in token:
                    tokens.append(self.generate(sub_token))
                return ''.join(tokens)
            else:
                return self.generate(token)
        elif isinstance(phrase, tuple):
            tokens = []
            for token in phrase:
                tokens.append(self.generate(token))
            return ''.join(tokens)
        else:
            raise ValueError('Phrase %s invalid' % phrase_name)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        g = SentenceGenerator()
        g.load_grammar('grammar.txt')

        logger.info('Input: sentence')
        s = g.generate('sentence')
        logger.info('Output: %s\n' % s)

        logger.info('Input: sentence')
        s = g.generate('sentence')
        logger.info('Output: %s\n' % s)

        logger.info('Input: sentence')
        s = g.generate('sentence')
        logger.info('Output: %s\n' % s)

        logger.info('Input: sentence')
        s = g.generate('sentence')
        logger.info('Output: %s\n' % s)

        logger.info('Input: noun_phrase')
        s = g.generate('noun_phrase')
        logger.info('Output: %s\n' % s)

        logger.info('Input: Adj')
        s = g.generate('Adj')
        logger.info('Output: %s\n' % s)

        logger.info('Input: verb_phrase')
        s = g.generate('verb_phrase')
        logger.info('Output: %s\n' % s)

        logger.info('Input: Article')
        s = g.generate('Article')
        logger.info('Output: %s\n' % s)

        logger.info('Input: noun')
        s = g.generate('noun')
        logger.info('Output: %s\n' % s)

        logger.info('Input: verb')
        s = g.generate('verb')
        logger.info('Output: %s\n' % s)

        logger.info('Input: Adj')
        s = g.generate('Adj')
        logger.info('Output: %s\n' % s)
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('sentence', type=str, help='The input sentence')
        parser.add_argument('--verbose', dest='verbose', action='store_true', help='Verbose mode')
        parser.add_argument(
            '--grammar',
            dest='grammar',
            type=str,
            default='grammar.txt',
            help='The path for your grammar'
        )
        parser.add_argument(
            '--phrase_separator',
            dest='phrase_separator',
            type=str,
            default='=>',
            help='Separator for the name and the definition'
        )
        parser.add_argument(
            '--collection_separator',
            dest='collection_separator',
            type=str,
            default=' | ',
            help='Separator for phrase possible values'
        )
        parser.add_argument(
            '--component_separator',
            dest='component_separator',
            type=str,
            default=' ',
            help='Separator for the components to defined the whole phrase'
        )
        parser.add_argument(
            '--null_words',
            dest='null_words',
            type=str,
            default='null',
            help='The null word list which will be converted to empty string, list elements separated by comma'
        )
        args = parser.parse_args(sys.argv[1:])
        if args.verbose:
            logger.setLevel(logging.DEBUG)

        g = SentenceGenerator(
            phrase_separator=args.phrase_separator,
            collection_separator=args.collection_separator,
            component_separator=args.component_separator,
            null_words=args.null_words.split(',')
        )
        g.load_grammar(args.grammar)
        s = g.generate(args.sentence)
        logger.info(s)
