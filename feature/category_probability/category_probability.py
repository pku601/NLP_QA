# -*- coding: UTF-8 -*-

import sys

# general
# qid category label_probability


class category_util:
    def __init__(self):
        file_path = "category_probability/train_category_probability.txt"
        self.model = self.load_file(file_path)

    def load_file(self, file_path):
        cate_dict = {}
        fp = open(file_path)
        for line in fp:
            line = line.strip()
            line_tokens = line.split("\t")
            cate_list = [float(each) for each in line_tokens[1:]]
            cate_dict[line_tokens[0]] = cate_list
        fp.close()
        return cate_dict

    def get_category_vec(self, category):
        return self.model[category]


def labelToInt(label):
        if(label == "Good"):
            value = 0
        elif(label == "Bad"):
            value = 1
        elif(label == "Potential"):
            value = 2
        elif(label == "Dialogue"):
            value = 3
        elif(label == "Not English"):
            value = 4
        elif(label == "Other"):
            value = 5
        else:          # error
            value = 6
        return value

# 记录每个category对应的question的comment的类别的频数
def getProDict():
    prob = {}
    for i in range(6):
        prob[i] = 0.0
    return prob

def getFeature(meta_file, file_type):

    in_file = open(meta_file, 'r')
    out_file = open(file_type + '_category_probability.txt', 'wb')

    category = {}  # {category:{0:1, 1:2, 2:3, 3:4, 4:5, 5:6}}
    cname = ''
    # test, question 4, comment 2
    if file_type == 'test':
        # for line in in_file:
        #     feats = line.strip('\n').split('\t')
        #     if(len(feats) == 4):        # question
        #         cname = feats[1]
        #         if(cname not in category):
        #             category[cname] = getProDict()
        #     elif (len(feats) == 2):     # comment
        #         cgold = feats[2]
        #         category[cname][labelToInt(cgold)] += 1
        return

    # train and dev, question 5, comment 4
    else:
        for line in in_file:
            feats = line.strip('\n').split('\t')
            if(len(feats) == 5):        # question
                cname = feats[1]
                if(cname not in category):
                    category[cname] = getProDict()

            elif (len(feats) == 4):     # comment
                cgold = feats[2]
                category[cname][labelToInt(cgold)] += 1

    for name,pro in category.iteritems():
        total_num = sum(pro.values())
        for p in pro:
            pro[p] = pro[p] / total_num
        out_file.write(name + "\t" + '\t'.join([str(x) for x in pro.values()]) + '\n')

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
    print "feature category_probability " + sys.argv[1] + " done!"

# train
# python category_probability.py ../metainfo/train/metadata_total.txt 0

# dev and test ignore
# dev
# python category_probability.py ../metainfo/dev/metadata_total.txt 1

# test
# python category_probability.py ../metainfo/test/metadata_total.txt 2