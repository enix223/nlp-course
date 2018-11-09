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
import argparse
from itertools import product

import jieba
import jieba.analyse
import jieba.posseg as pseg

"""
2. Sentence Candidates Parser
In a QA system, an ordinary task is to give some Question-Answer Pairs to a dataset. For example, we
may give a pair (“你好”, “你好，我是网银小助手”), or (“如何办理网银盾”， “您在网页下方点击 XXX
然后进行下一步即可”) to a dataset.
Actually, this QA pair could give sufficient information to a QA system. However, there are some
occasions that need some more sophisticate processing. For example, someone may give (“如何办理贵
宾卡/金卡/特惠卡”, “请在页面下方 XXX 处点击办卡”)， or (“网银/信用卡如何/怎样注销/开户”, “请在
账户管理处进行”). Therefore, we need a parser, given a sentence with ‘split mark’, which will
generate some more sentences:

e.g:

Input: 如何办理贵宾卡/金卡/特惠卡?
Output:
    如何办理贵宾卡?
    如何办理金卡?
    如何办理特惠卡?

Input 2: 网银/信用卡如何/怎样注销/开户?
Output:
    网银如何注销?
    信用卡如何注销?
    网银怎样注销?
    信用卡怎样注销?
    …
    信用卡怎样开户?
# above should exist 8 sentences.

Please write a program to solve this problem. Hint: You may need the python package “jieba”
https://github.com/fxsjy/jieba to split the sentence to corresponding words.

代码	名称	说明	举例
a	形容词	取英语形容词adjective的第1个字母	最/d 大/a 的/u
ad	副形词	直接作状语的形容词.形容词代码a和副词代码d并在一起	一定/d 能够/v 顺利/ad 实现/v 。/w
ag	形语素	形容词性语素。形容词代码为a，语素代码ｇ前面置以a	喜/v 煞/ag 人/n
an	名形词	具有名词功能的形容词。形容词代码a和名词代码n并在一起	人民/n 的/u 根本/a 利益/n 和/c 国家/n 的/u 安稳/an 。/w
b	区别词	取汉字“别”的声母	副/b 书记/n 王/nr 思齐/nr
c	连词	取英语连词conjunction的第1个字母	全军/n 和/c 武警/n 先进/a 典型/n 代表/n
d	副词	取adverb的第2个字母，因其第1个字母已用于形容词	两侧/f 台柱/n 上/ 分别/d 雄踞/v 着/u
dg	副语素	 副词性语素。副词代码为d，语素代码ｇ前面置以d	用/v 不/d 甚/dg 流利/a 的/u 中文/nz 主持/v 节目/n 。/w
e	叹词	取英语叹词exclamation的第1个字母	嗬/e ！/w
f	方位词	取汉字“方” 的声母	从/p 一/m 大/a 堆/q 档案/n 中/f 发现/v 了/u
g	语素	绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母	例如dg 或ag
h	前接成分	取英语head的第1个字母	目前/t 各种/r 非/h 合作制/n 的/u 农产品/n
i	成语	取英语成语idiom的第1个字母	提高/v 农民/n 讨价还价/i 的/u 能力/n 。/w
j	简称略语	取汉字“简”的声母	民主/ad 选举/v 村委会/j 的/u 工作/vn
k	后接成分	 	权责/n 明确/a 的/u 逐级/d 授权/v 制/k
l	习用语	习用语尚未成为成语，有点“临时性”，取“临”的声母	是/v 建立/v 社会主义/n 市场经济/n 体制/n 的/u 重要/a 组成部分/l 。/w
m	数词	取英语numeral的第3个字母，n，u已有他用	科学技术/n 是/v 第一/m 生产力/n
n	名词	取英语名词noun的第1个字母	希望/v 双方/n 在/p 市政/n 规划/vn
ng	名语素	名词性语素。名词代码为n，语素代码ｇ前面置以n	就此/d 分析/v 时/Ng 认为/v
nr	人名	名词代码n和“人(ren)”的声母并在一起	建设部/nt 部长/n 侯/nr 捷/nr
ns	地名	名词代码n和处所词代码s并在一起	北京/ns 经济/n 运行/vn 态势/n 喜人/a
nt	机构团体	“团”的声母为t，名词代码n和t并在一起	[冶金/n 工业部/n 洛阳/ns 耐火材料/l 研究院/n]nt
nx	字母专名	 	ＡＴＭ/nx 交换机/n
nz	其他专名	“专”的声母的第1个字母为z，名词代码n和z并在一起	德士古/nz 公司/n
o	拟声词	取英语拟声词onomatopoeia的第1个字母	汩汩/o 地/u 流/v 出来/v
p	介词	取英语介词prepositional的第1个字母	往/p 基层/n 跑/v 。/w
q	量词	取英语quantity的第1个字母	不止/v 一/m 次/q 地/u 听到/v ，/w
r	代词	取英语代词pronoun的第2个字母,因p已用于介词	有些/r 部门/n
s	处所词	取英语space的第1个字母	移居/v 海外/s 。/w
t	时间词	取英语time的第1个字母	当前/t 经济/n 社会/n 情况/n
tg	时语素	时间词性语素。时间词代码为t,在语素的代码g前面置以t	秋/Tg 冬/tg 连/d 旱/a
u	助词	取英语助词auxiliary 的第2个字母,因a已用于形容词	工作/vn 的/u 政策/n
ud	结构助词	 	有/v 心/n 栽/v 得/ud 梧桐树/n
ug	时态助词	 	你/r 想/v 过/ug 没有/v
uj	结构助词的	 	迈向/v 充满/v 希望/n 的/uj 新/a 世纪/n
ul	时态助词了	 	完成/v 了/ ul
uv	结构助词地	 	满怀信心/l 地/uv 开创/v 新/a 的/u 业绩/n
uz	时态助词着	 	眼看/v 着/uz
v	动词	 	举行/v 老/a 干部/n 迎春/vn 团拜会/n
vd	副动词	 	强调/vd 指出/v
vg	动语素	动词性语素。动词代码为v。在语素的代码g前面置以V	做好/v 尊/vg 干/j 爱/v 兵/n 工作/vn
vn	名动词	 指具有名词功能的动词。动词和名词的代码并在一起	股份制/n 这种/r 企业/n 组织/vn 形式/n ，/w
w	标点符号	 	生产/v 的/u ５Ｇ/nx 、/w ８Ｇ/nx 型/k 燃气/n 热水器/n
x	非语素字	非语素字只是一个符号，字母x通常用于代表未知数、符号	 
y	语气词	取汉字“语”的声母	已经/d ３０/m 多/m 年/q 了/y 。/w
z	状态词	取汉字“状”的声母的前一个字母	势头/n 依然/z 强劲/a ；/w
"""

jieba.load_userdict('userdict.txt')
SPECIAL_CHAR = '/'


def split_sentence(sentence, verbose=False):
    """Split sentence and annotate the words

    网银/信用卡如何/怎样注销/开户 => 网银 / 信用卡 如何 / 怎样 注销 / 开户

        /       如何       /         /         ?
      |   |             |   |     |   |
    网银  信用卡        如何  怎样  注销  开户
    """
    tokens = pseg.cut(sentence)

    seg, flag, pos = [], False, 0
    for w in tokens:
        if w.word == SPECIAL_CHAR:
            flag = True
            continue

        if flag:
            token = seg[pos - 1]
            if w.flag == token[0].flag:
                token.append(w)
            else:
                seg.append([w])
                pos += 1
            flag = False
            continue

        flag = False
        seg.append([w])
        pos += 1

    if verbose:
        print('Split tokens: {}'.format(seg))

    return seg


def build_candidate_sentences(seg: list, sep: str=''):
    """Build candidate sentence set with given `seg` list

    :param list seg: The sentence segment list
    :param list: A list of candidate sentence

    [(a, b), (c, ), (d, e, f)] =>

    a - c - d
    b /   \ e
          \ f
    """
    sentences = []
    for s in product(*seg):
        tokens = []
        for w in s:
            tokens.append(w.word)
        sentences.append(''.join(tokens))
    return sentences


if __name__ == '__main__':
    if len(sys.argv) == 1:
        s = '网银/信用卡如何/怎样注销/开户?'
        seg = split_sentence(s)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % s)
        print('Output:')
        print('\n'.join(sentences))
        print()

        s = '如何办理贵宾卡/金卡/特惠卡?'
        seg = split_sentence(s)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % s)
        print('Output:')
        print('\n'.join(sentences))
        print()

        s = '如何办理网银盾?'
        seg = split_sentence(s)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % s)
        print('Output:')
        print('\n'.join(sentences))
        print()

        s = '你好，我是网银小助手'
        seg = split_sentence(s)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % s)
        print('Output:')
        print('\n'.join(sentences))
        print()

        s = '如何/怎样/打开/开/我/你的电脑/手机'
        seg = split_sentence(s)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % s)
        print('Output:')
        print('\n'.join(sentences))
        print()
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument('sentence', type=str, help='The input sentence')
        parser.add_argument('--verbose', dest='verbose', action='store_true', help='Verbose')
        args = parser.parse_args(sys.argv[1:])

        seg = split_sentence(args.sentence, verbose=args.verbose)
        sentences = (build_candidate_sentences(seg))
        print('Input: %s' % args.sentence)
        print('Output:')
        print('\n'.join(sentences))
