
import sys
import pickle as pickle


class basic_feature:

    def __init__(self, step):   # step 0 train  1 devel  2 test
        if step == 0:
            file_path = "basic_feature/train.pkl"
        elif step == 1:
            file_path = "basic_feature/devel.pkl"
        elif step == 2:
            file_path = "basic_feature/test.pkl"
        self.features_dict = pickle.load(open(file_path, "r"))   # {cid:list(11)}

    def get_basic_feature(self, cid):
        return self.features_dict[cid]


def word_count(word, line_words):
    line_tokens = line_words.split(" ")
    count = 0
    for token in line_tokens:
        if token == word:
            count += 1
    return float(count)


def word_count_two(word_one, word_two, line_words):
    count = 0
    line_tokens = line_words.split(" ")
    for token in line_tokens:
        if token == word_one or token == word_two:
            count += 1
    return float(count)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        exit(1)

    fp = open(sys.argv[1], "r")
    output = open(sys.argv[2], "wb")

    feature_dict = dict()
    feature_list = list()

    for line in fp:
        line = line.strip()

        col_id = line.split("\t")[0]
        feature_list.append(col_id)

        if len(line.split("\t")) > 1:           # 9
            feature_word = ["yes", "no", "sure", "can", "neither", "good", "sorry"]
            for each_word in feature_word:
                feature_list.append(word_count(each_word, line.split("\t")[1]))
            feature_list.append(word_count_two("okay", "ok", line.split("\t")[1]))
            feature_list.append(word_count_two("thank", "thanks", line.split("\t")[1]))
        else:
            for i in range(9):
                feature_list.append(float(0))

        start_with_yes = float(0)           # 1
        if len(line.split("\t")) > 1 and line.split("\t")[1] == "yes":
            start_with_yes = float(1)
        feature_list.append(start_with_yes)

        if len(line.split("\t")) > 1:       # 1
            feature_list.append(float(len(line.split("\t")[1])))
        else:
            feature_list.append(float(0))

        feature_dict[feature_list[0]] = feature_list[1:]
        feature_list = []

    pickle.dump(feature_dict, output)
    fp.close()
    output.close()

# python basic_feature.py ../../Pretreatment/Total/pretreatment_one_result_train_total_3_id.txt train.pkl

# python basic_feature.py ../../Pretreatment/Total/pretreatment_one_result_devel_total_3_id.txt devel.pkl

# python basic_feature.py ../../Pretreatment/Total/pretreatment_one_result_test_total_3_id.txt test.pkl
