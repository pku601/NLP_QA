# -*- coding: UTF-8 -*-

import sys


class cuserEqualquser_Util:
    def __init__(self, step):  # step 0 train  1 devel  2 test
        if step == 0:
            file_path = "cuserEqualquser/train_cuserEqualquser.txt"
        elif step == 1:
            file_path = "cuserEqualquser/dev_cuserEqualquser.txt"
        elif step == 2:
            file_path = "cuserEqualquser/test_cuserEqualquser.txt"
        self.model = self.load_file(file_path)

    def load_file(self, lda_result_file_path):
        lda_dic = {}
        fp = open(lda_result_file_path, "r")
        for line in fp:
            if line.strip() == "":
                continue
            line = line.strip().split("\t")
            lda_dic[line[0]] = float(line[1])
        fp.close()
        return lda_dic

    def get_cuserEqualquser_value(self, cid):
        return self.model[cid]


def getFeature(meta_file, file_type):

    in_file = open(meta_file, 'r')
    out_file = open(file_type + '_cuserEqualquser.txt', 'wb')

    print meta_file, file_type
    quser = 0
    # test, question 4, comment 2
    if file_type == 'test':
        for line in in_file:
            feats = line.strip('\n').split('\t')
            if(len(feats) == 4):
                quser = feats[2]
            elif (len(feats) == 2):
                cid = feats[0]
                cuser = feats[1]
                if quser == cuser:
                    out_file.write(cid + "\t" + "1\n")
                else:
                    out_file.write(cid + "\t" + "0\n")
            else:
                out_file.write(cid + "\t" + "error\n")

    # train and dev, question 5, comment 4
    else:
        for line in in_file:
            feats = line.strip('\n').split('\t')
            if(len(feats) == 5):
                quser = feats[2]
            elif (len(feats) == 4):
                cid = feats[0]
                cuser = feats[1]
                if quser == cuser:
                    out_file.write(cid + "\t" + "1\n")
                else:
                    out_file.write(cid + "\t" + "0\n")
            else:
                out_file.write(cid + "\t" + "error\n")

    in_file.close()
    out_file.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: metadata File Path"
        print "sys.argv[2]: Data Type (train 0, dev 1, test 2)"
        exit()

    file_type = ''          # 文件类型

    if sys.argv[2] == '0':
        file_type = 'train'
    elif sys.argv[2] == '1':
        file_type = 'dev'
    elif sys.argv[2] == '2':
        file_type = 'test'
    else:
        print 'error'
        exit()

    getFeature(sys.argv[1], file_type)
    print "feature cuserEqualquser " + sys.argv[1] + " done!"

# train
# python cuserEqualquser.py ../metainfo/train/metadata_total.txt 0

# dev
# python cuserEqualquser.py ../metainfo/dev/metadata_total.txt 1

# test
# python cuserEqualquser.py ../metainfo/test/metadata_total.txt 2