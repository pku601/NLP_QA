
if __name__ == "__main__":
    devel_fp = open("Total/pretreatment_one_result_devel_total_3.txt", "r")
    train_fp = open("Total/pretreatment_one_result_train_total_3.txt", "r")
    test_fp = open("Total/pretreatment_one_result_test_total_3.txt", "r")

    target_fp = open("Total/pretreatment_one_result_all_total_3.txt", "wb")

    for line in train_fp:
        target_fp.write(line)

    for line in devel_fp:
        target_fp.write(line)

    for line in test_fp:
        target_fp.write(line)

    devel_fp.close()
    train_fp.close()
    test_fp.close()
    target_fp.close()

# python join_3_file.py
