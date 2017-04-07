#-*- coding:utf-8 -*-

import sys
import LDA.latent_dirichlet_allocation as LDA
import LSI.LSI as LSI
import bag_of_words.bag_of_words as BOW
import cuserEqualquser.cuserEqualquser as cEq
import metainfo.ParseXML_metadata as MetaData
import category_probability.category_probability as cate_pro
import word2vec.word2vecUtil as word2vecUtil
import url.ParseXML_has_url as URL
import numpy as np
import pickle as pickle
import basic_feature.basic_feature as basic_feature
import Has_Email.ParseXML_has_email as ParseXML_has_email

TRAIN_LINES = 19141
DEVEL_LINES = 1945
TEST_LINES = 2305

MIN_VALUE = 1e-5
FEATURE_NUM = 24

def main(step, task):     # 0 train, 1 devel, 2 test

    # feature
    file = ""
    if step == 0:
        file = "../Pretreatment/Total/pretreatment_one_result_train_total_3_id.txt"
        if task == 0:
            pickle_total = "./train_total_taskA.pkl"
        elif task == 1:
            pickle_total = "./train_total_taskB.pkl"
        else:
            print "task type error"
            exit()
    elif step == 1:
        file = "../Pretreatment/Total/pretreatment_one_result_devel_total_3_id.txt"
        if task == 0:
            pickle_total = "./devel_total_taskA.pkl"
        elif task == 1:
            pickle_total = "./devel_total_taskB.pkl"
        else:
            print "task type error"
            exit()
    elif step == 2:
        file = "../Pretreatment/Total/pretreatment_one_result_test_total_3_id.txt"
        if task == 0:
            pickle_total = "./test_total_taskA.pkl"
        elif task == 1:
            pickle_total = "./test_total_taskB.pkl"
        else:
            print "task type error"
            exit()
    else:
        print 'error step!'
        return

    fp = open(file, "r")    # read file
    # fp_pickle_general = open(pickle_general, "wb")
    # fp_pickle_yes_no = open(pickle_yes_no, "wb")
    fp_pickle_total = open(pickle_total, "wb")

    row_num = 0         # line number

    # features_gen = list()   # [[], [], ...]
    # feature_yes_no = list()
    features_total = list()

    # meta
    meta = MetaData.MetaData(step)

    # Basic feature
    bf = basic_feature.basic_feature(step)

    # LDA
    lda = LDA.LDA_Util()

    # LSI
    lsi = LSI.LSI_Util()

    # category_probability
    cp = cate_pro.category_util()

    # cuserEqualquser
    ceq = cEq.cuserEqualquser_Util(step)

    # URL
    url = URL.get_url_utli(step)

    # Email
    has_email = ParseXML_has_email.get_email_utli(step)

    # word2vec
    w2v = word2vecUtil.Word2VecUtil()

    # add_step
    add_step = 0        # train
    if step == 1:
        add_step = TRAIN_LINES      # dev
    elif step == 2:
        add_step = TRAIN_LINES + DEVEL_LINES      # test

    files = fp.readlines()
    print len(files)
    while row_num < len(files):

        line = files[row_num]
        lines = line.split('\t')
        rowid = lines[0].strip()
        content = lines[1].strip()

        # print rowid, content

        if "_" not in rowid and meta.getQuestionType(rowid) == "YES_NO":

            qfeature = np.zeros((FEATURE_NUM))

            qindex = row_num
            qid = rowid
            qcontent = content

            row_num += 1                # comment

            num_com = 0

            while row_num < len(files):

                line = files[row_num]
                lines = line.split('\t')
                rowid = lines[0].strip()
                content = lines[1].strip()

                if "_" not in rowid:
                    break;

                 # feature = []
                feature_data = []

                # basic feature 11
                feature_data.extend(bf.get_basic_feature(rowid))

                # LDA
                feature_data.append(lda.getLDASim(qindex + add_step, row_num + add_step))

                # LSI
                feature_data.append(lsi.getLSISim(qindex + add_step, row_num + add_step))

                # BOW
                if qcontent and content:
                    bow = BOW.BOW(qcontent, content)
                    feature_data.append(bow.getVectorSim())
                else:
                    feature_data.append(MIN_VALUE)

                # category_probability 6
                feature_data.extend(cp.get_category_vec(meta.getQuestionCat(qid)))

                # cuserEqualquser
                feature_data.append(ceq.get_cuserEqualquser_value(rowid))

                # url
                feature_data.append(url.get_url_value(rowid))

                # Has_Email
                feature_data.append(has_email.get_email_value(rowid))

                # word2vec
                feature_data.append(w2v.getSentenseSim(qcontent, content))

                # extend total data
                # feature.extend(feature_data)
                # print feature_data
                qfeature = qfeature + np.array(feature_data)

                row_num += 1
                num_com += 1



            feature = []

            # qid
            feature.append(qid)

            # qfeature = qfeature / num_com

            # features data
            feature.extend(qfeature.tolist())

            # label
            if step == 0:       # train
                feature.append(meta.getQuestionLabel(qid))

            features_total.append(feature)
        else:
            row_num += 1

    # print len(features_gen), len(feature_yes_no)
    # pickle features  labels
    # pickle.dump(features_gen, fp_pickle_general)
    # pickle.dump(feature_yes_no, fp_pickle_yes_no)
    pickle.dump(features_total, fp_pickle_total)

    # close
    fp.close()
    # fp_pickle_general.close()
    # fp_pickle_yes_no.close()
    fp_pickle_total.close()


def showFeatures(file_path):
    fp = open(file_path, "r")
    features = pickle.load(fp)
    print "Show Features!"
    # get_x_train = [feature[1:-1] for feature in features]
    # get_y_train = [feature[-1] for feature in features]
    # tmp_fp = open("clf_input.txt", "wb")
    # print features[0]
    for i in range(10):
        print features[i]
    print len(features)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "sys.argv[1]: step! (0 train, 1 devel, 2 test)"
        print "sys.argv[2]: task! (0 taskA, 1 taskB)"
        exit()

    step = int(sys.argv[1])
    task = int(sys.argv[2])
    main(step, task)
    # showFeatures("./train_total_taskB.pkl")

# bow w2v LDA TF-IDF URL Category_pro cuserComQuser

# train

# taskB
# python getFeatureVector_taskB.py 0 1


# devel

# taskB
# python getFeatureVector_taskB.py 1 1

# test

# taskB
# python getFeatureVector_taskB.py 2 1


    

    
    
    

