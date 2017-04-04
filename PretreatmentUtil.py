# -*- coding: UTF-8 -*-

import string
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sp

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class PretreatmentUtil:

    def getContent(self, content):
        # 文本预处理
        # 2.分割成句子
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        sents = sent_tokenizer.tokenize(content)

        # 3.去掉数字标点和非字母字符
        cleanLines = [self.CleanLines(line.encode("utf-8")) for line in sents]

        # 4.nltk.word_tokenize分词
        words = [self.WordTokener(cl) for cl in cleanLines]

        # 5.去停用词和小写去短词
        cleanWords = self.CleanWords(words)

        # 6.使用Wordnet进行词干化
        stemWords = self.StemWords(cleanWords)

        # 7.
        strLine = self.WordsToStr(stemWords)

        return " ".join(strLine)

    def CleanLines(self, line):
        identify = string.maketrans('', '')
        delEStr = string.punctuation + string.digits  # ASCII 标点符号，数字
        # cleanLine = line.translate(identify,delEStr) #去掉ASCII 标点符号和空格
        cleanLine = line.translate(identify, delEStr)  # 去掉ASCII 标点符号
        return cleanLine

    def WordTokener(self, sent):  # 将单句字符串分割成词
        wordsInStr = nltk.word_tokenize(sent)
        return wordsInStr

    def CleanWords(self,wordsInStr): # 去掉标点符号，长度小于3的词以及non-alpha词，小写化
        cleanWords = []
        # stopwords = {}.fromkeys([line.rstrip() for line in open('stopwords_short.txt')])
        stops = set(sp.words('english'))
        for words in wordsInStr:
            cleanWords += [[w.lower() for w in words if w.lower() not in stops]]
        return cleanWords

    def StemWords(self, cleanWordsList):
        stemWords = []
        for words in cleanWordsList:
            stemWords += [[wn.morphy(w) for w in words]]
        return stemWords

    def WordsToStr(self, stemWords):
        strLine = []
        for words in stemWords:
            strLine += [w for w in words if w is not None]
        return strLine
