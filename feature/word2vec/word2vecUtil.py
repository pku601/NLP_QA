#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os.path
import sys
import multiprocessing
import numpy as np

from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
from scipy import linalg, mat, dot

vector_len = 400

class Word2VecUtil:

    def __init__(self):   # 0 train, 1 devel, 2 test
        file = "word2vec/total_w2v.model"
        # if step == 0:
        #     file = "word2vec/train_w2v.model"
        # elif step == 1:
        #     file = "word2vec/devel_w2v.model"
        # elif step == 2:
        #     file = "word2vec/test_w2v.model"
        self.model = Word2Vec.load(file)

    def cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        if linalg.norm(a) < 1e-3 or linalg.norm(b) < 1e-3:
            return 10
        c = dot(a,b.T)/linalg.norm(a)/linalg.norm(b)
        return c[0,0]

    def getSentenseSim(self, s1, s2):

        v1 = np.zeros(vector_len)
        v2 = np.zeros(vector_len)
        for word in s1.split():
            if word in self.model.wv:
                v1 += self.model.wv[word]
        for word in s2.split():
            if word in self.model.wv:
                v2 += self.model.wv[word]
        return self.cosine(v1, v2)

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
    inp, out = sys.argv[1:3]

    model = Word2Vec(LineSentence(inp), size=400, window=5, min_count=5, sample=1e-5,
            workers=multiprocessing.cpu_count())

    model.save(out)
    model.wv.save_word2vec_format("total_w2v.vector")
    # model = Word2Vec.load(out)

# total
# python word2vecUtil.py ../../Pretreatment/Total/pretreatment_one_result_all_total_3.txt ./total_w2v.model

# train
# python word2vecUtil.py ../../Pretreatment/Total/pretreatment_one_result_train_total_2.txt ./train_w2v.model

# dev and test ignore
# dev
# python word2vecUtil.py ../../Pretreatment/Total/pretreatment_one_result_devel_total_2.txt ./devel_w2v.model

# test
# python word2vecUtil.py ../../Pretreatment/Total/pretreatment_one_result_test_total_2.txt ./test_w2v.model