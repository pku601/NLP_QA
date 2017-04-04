# -*- coding: UTF-8 -*-

from PretreatmentUtil import PretreatmentUtil
import sys

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        exit()

    pre_util = PretreatmentUtil()

    fp = open(sys.argv[1], 'r')  # read file
    fp_resout = open(sys.argv[2], 'wb')  # write result into file

    for line in fp:
        line = line.strip()
        line_result = pre_util.getContent(line)
        fp_resout.write(line_result + "\n")

    fp.close()
    fp_resout.close()

# python Pretreatment_two_2.py Total/pretreatment_one_result_devel_total_2.txt Total/pretreatment_one_result_devel_total_3.txt

# python Pretreatment_two_2.py Total/pretreatment_one_result_train_total_2.txt Total/pretreatment_one_result_train_total_3.txt

# python Pretreatment_two_2.py Total/pretreatment_one_result_test_total_2.txt Total/pretreatment_one_result_test_total_3.txt
