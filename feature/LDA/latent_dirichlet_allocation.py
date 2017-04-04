# -*- coding: UTF-8 -*-

from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora
import gensim
import numpy
import sys

from scipy import linalg, mat, dot


class LDA_Util:
    def __init__(self):  # step 0 train  1 devel  2 test
        # if step == 0:
        #     file_path = "LDA/result_lda_train.txt"
        # elif step == 1:
        #     file_path = "LDA/result_lda_devel.txt"
        # elif step == 2:
        #     file_path = "LDA/result_lda_test.txt"
        file_path = "LDA/result_lda_all.txt"
        self.model = self.load_file(file_path)

    def load_file(self, lda_result_file_path):
        lda_list = []
        fp = open(lda_result_file_path, "r")
        for line in fp:
            if line.strip() == "":
                continue
            # lda_list.append(line.strip())
            lda_list.append([float(each_num) for each_num in line.strip().split()])
        fp.close()
        return lda_list

    def cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        c = dot(a, b.T) / linalg.norm(a) / linalg.norm(b)
        return c[0, 0]

    def getLDASim(self, line_num_one, line_num_two):  # num start from 0
        return self.cosine(self.model[line_num_one], self.model[line_num_two])


def get_doc_set(input_fp):
    file_list = []
    for line in input_fp:
        file_list.append(line.strip())
    return file_list


# Hellinger distance is useful for similarity between probability distributions (such as LDA topics):
def hellinger(lda_vec1, lda_vec2, num_topics):
    dense1 = gensim.matutils.sparse2full(lda_vec1, num_topics)
    dense2 = gensim.matutils.sparse2full(lda_vec2, num_topics)
    sim = numpy.sqrt(0.5 * ((numpy.sqrt(dense1) - numpy.sqrt(dense2))**2).sum())
    return sim


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        exit()

    fp = open(sys.argv[1], "r")
    fp_result = open(sys.argv[2], "wb")

    tokenizer = RegexpTokenizer(r'\w+')

    # create English stop words list
    en_stop = get_stop_words('en')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()

    # compile sample documents into a list
    doc_set = get_doc_set(fp)

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if i not in en_stop]

        # stem token
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

        # add tokens to list
        texts.append(stemmed_tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    lda_num_topics = 10  # 主题数量，根据情况设置
    lda_model = gensim.models.ldamodel.LdaModel(corpus, num_topics=lda_num_topics, id2word=dictionary, passes=20,
                                                minimum_probability=1e-8)
    # print(lda_model.print_topics(num_topics=lda_num_topics, num_words=4))

    for text in texts:
        topic_distributions = lda_model[dictionary.doc2bow(text)]
        print topic_distributions
        topic_distributions_list = [1e-8 for x in range(0, 10)]
        for each in topic_distributions:
            # topic_distributions_list.append(each[1])
            topic_distributions_list[each[0]] = each[1]
            # print each[1], str(each[1])
        one_line = "\t".join(str(td) for td in topic_distributions_list)
        print one_line
        fp_result.write(one_line)
        fp_result.write("\n")

    fp.close()
    fp_result.close()

    # print hellinger(lda_model[corpus[0]], lda_model[corpus[1]], lda_model.num_topics)

# python latent_dirichlet_allocation.py ../../Pretreatment/Total/pretreatment_one_result_devel_total_2.txt ./result_lda_devel.txt

# python latent_dirichlet_allocation.py ../../Pretreatment/Total/pretreatment_one_result_train_total_2.txt ./result_lda_train.txt

# python latent_dirichlet_allocation.py ../../Pretreatment/Total/pretreatment_one_result_test_total_2.txt ./result_lda_test.txt

# python latent_dirichlet_allocation.py ../../Pretreatment/Total/pretreatment_one_result_all_total_3.txt ./result_lda_all.txt
