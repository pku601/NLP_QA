# -*- coding: UTF-8 -*-

from PretreatmentUtil import PretreatmentUtil
import sys

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        print "sys.argv[3]: ID File Path"
        exit()

    pre_util = PretreatmentUtil()

    fp = open(sys.argv[1], 'r')  # read file
    fp_id = open(sys.argv[3], "r")  # read id file
    fp_resout = open(sys.argv[2], 'wb')  # write result into file

    id_list = []
    for line in fp_id:
        id_list.append(line.strip())

    print len(id_list)
    count = 0
    for line in fp:
        line = line.strip()
        line_result = pre_util.getContent(line)
        line_result = id_list[count] + "\t" + line_result
        print count
        count += 1
        fp_resout.write(line_result + "\n")

    fp.close()
    fp_id.close()
    fp_resout.close()

# python Pretreatment_two_2_add_QID_CID.py Total/pretreatment_one_result_devel_total_2.txt Total/pretreatment_one_result_devel_total_3_id.txt Total/result_devel_total_ID.txt

# python Pretreatment_two_2_add_QID_CID.py Total/pretreatment_one_result_train_total_2.txt Total/pretreatment_one_result_train_total_3_id.txt Total/result_train_total_ID.txt

# python Pretreatment_two_2_add_QID_CID.py Total/pretreatment_one_result_test_total_2.txt Total/pretreatment_one_result_test_total_3_id.txt Total/result_test_total_ID.txt
