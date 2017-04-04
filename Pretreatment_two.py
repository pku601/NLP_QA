# -*- coding: UTF-8 -*-

import os
from PretreatmentUtil import PretreatmentUtil

if __name__ == '__main__':
    pre_util = PretreatmentUtil()
    # base_dir = "General/devel/"
    # base_dir = "YesNo/devel/"
    # base_dir = "YesNo/train/"
    # base_dir = "Pretreatment/Total/train/"
    base_dir = "Pretreatment/Total/devel/"
    # base_dir = "General/train/"
    # fp = open('General/pretreatment_one_result_devel_general.txt', 'r')  # read file
    # fp = open('YesNo/pretreatment_one_result_devel_yesno.txt', 'r')  # read file
    # fp = open('YesNo/pretreatment_one_result_train_yesno.txt', 'r')  # read file
    # fp = open('Pretreatment/Total/pretreatment_one_result_train_total.txt', 'r')  # read file
    fp = open('Pretreatment/Total/pretreatment_one_result_devel_total.txt', 'r')  # read file
    # fp = open('General/pretreatment_one_result_train_general.txt', 'r')  # read file
    is_qid = True
    qid = ""
    for line in fp:
        line = line.strip()
        if line == "":  # 空行
            is_qid = True
        else:  # 非空行
            if is_qid:  # 对应qid的那一行
                if line == "":
                    pass
                line_split = line.split("\t", 1)
                qid = line_split[0]
                question_content = line_split[1]
                # 创建文件夹
                if not os.path.exists(base_dir + qid):
                    os.mkdir(base_dir + qid)
                # 创建文件qid.txt并写入
                fp_qid = open(base_dir + qid + "/" + qid + ".txt", "wb")
                fp_qid.write(pre_util.getContent(question_content))  # 经过预处理后写入文件
                fp_qid.close()
            else:  # 对应cid的那一行
                line_split = line.split("\t", 1)
                if len(line_split) == 2:
                    cid = line_split[0]
                    comment_content = line_split[1]
                    # 创建文件cid.txt并写入
                    fp_cid = open(base_dir + qid + "/" + cid + ".txt", "wb")
                    fp_cid.write(pre_util.getContent(comment_content))  # 经过预处理后写入文件
                    fp_cid.close()
                else:  # 没有任何内容（如train Q2504_C3）
                    cid = line_split[0]
                    # 创建文件cid.txt并写入
                    fp_cid = open(base_dir + qid + "/" + cid + ".txt", "wb")
                    fp_cid.write("")  # 经过预处理后写入文件
                    fp_cid.close()
            is_qid = False
    fp.close()
