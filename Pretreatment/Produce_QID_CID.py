import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        exit()

    fp = open(sys.argv[2], "wb")
    fp_id = open(sys.argv[1], "r")
    id_list = []
    for line in fp_id:
        line = line.strip()
        if line == "":
            continue
        ID = line.split("\t")[0]
        print ID
        id_list.append(ID)
        fp.write(ID)
        fp.write("\n")
    print len(id_list)

    fp_id.close()
    fp.close()

# python Produce_QID_CID.py ./Total/pretreatment_one_result_devel_total.txt ./Total/result_devel_total_ID.txt

# python Produce_QID_CID.py ./Total/pretreatment_one_result_train_total.txt ./Total/result_train_total_ID.txt

# python Produce_QID_CID.py ./Total/pretreatment_one_result_test_total.txt ./Total/result_test_total_ID.txt
