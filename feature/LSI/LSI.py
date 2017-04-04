#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gensim import models
import logging
import os.path
import sys
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora

from scipy import linalg, mat, dot

reload(sys)
sys.setdefaultencoding('utf-8')

MIN_VALUE = 1e-5
BLANK_VALUE = 1e-1

class LSI_Util:
    def __init__(self):  # step 0 train  1 devel  2 test
        # if step == 0:
        #     file_path = "LSI/train_lsi.txt"
        # elif step == 1:
        #     file_path = "LSI/devel_lsi.txt"
        # elif step == 2:
        #     file_path = "LSI/test_lsi.txt"
        file_path = "LSI/total_lsi.txt"
        self.model = self.load_file(file_path)

    def load_file(self, lda_result_file_path):
        lda_list = []
        fp = open(lda_result_file_path, "r")
        for line in fp:
            if line.strip() == "":
                lda_list.append([float(BLANK_VALUE) for i in range(10)])
            else:
                vec = line.split('\t')
                lda_list.append([float(num) for num in vec])
        fp.close()
        return lda_list

    def cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        c = dot(a, b.T) / linalg.norm(a) / linalg.norm(b)
        return c[0, 0]

    def getLSISim(self, line_num_one, line_num_two):  # num start from 0
        # print line_num_one, line_num_two

        # print self.model[line_num_one]
        # print self.model[line_num_two]

        if len(self.model[line_num_one]) != len(self.model[line_num_two]):
            print line_num_one, line_num_two
            return MIN_VALUE
        else:
            return self.cosine(self.model[line_num_one], self.model[line_num_two])


def getCorpus(infile):

    fp = open(infile, "r")

    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()


    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for line in fp:

        # strip
        line = line.strip()

        # clean and tokenize document string
        raw = line.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [word for word in tokens if word not in en_stop]

        # stem token
        stemmed_tokens = [p_stemmer.stem(word) for word in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    fp.close()
    return texts

def train_lsi(infile, outfile):

    texts = getCorpus(infile)
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=10)

    fp_out = open(outfile, "wb")
    for text in texts:
        text_bow = dictionary.doc2bow(text)
        text_lsi = lsi[text_bow]
        # print text_lsi
        topic_pro = [x[1] for x in text_lsi]
        fp_out.write('\t'.join([str(pro) for pro in topic_pro]) + '\n')

    fp_out.close()

if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)

    infile, outfile = sys.argv[1:3]
    train_lsi(infile, outfile)


# total
# python LSI.py ../../Pretreatment/Total/pretreatment_one_result_all_total_3.txt ./total_lsi.txt

# train
# python LSI.py ../../Pretreatment/Total/pretreatment_one_result_train_total_2.txt ./train_lsi.txt

# dev and test ignore
# dev
# python LSI.py ../../Pretreatment/Total/pretreatment_one_result_devel_total_2.txt ./devel_lsi.txt

# test
# python LSI.py ../../Pretreatment/Total/pretreatment_one_result_test_total_2.txt ./test_lsi.txt