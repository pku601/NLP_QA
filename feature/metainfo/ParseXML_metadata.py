# -*- coding: UTF-8 -*-

import xml.sax
import sys

# general and yes_no label to int
def labelToInt(label, type): # 0 general, 1 yes_no
    value = 0
    if type == 0:
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
    elif type == 1:
        if(label == "Yes"):
            value = 0
        elif(label == "No"):
            value = 1
        elif(label == "Unsure"):
            value = 2
        else:           # other
            # print "other type"
            value = 3
        return value
    else:
        print "error"
        return -1



class MetaData:
    def __init__(self, step):    # 0 train, 1 devel, 2 test
        file_path = ""
        if step == 0:
            file_path = "metainfo/train/metadata_total.txt"
        elif step == 1:
            file_path = "metainfo/dev/metadata_total.txt"
        elif step == 2:
            file_path = "metainfo/test/metadata_total.txt"
        else:
            print "error step"
            exit()

        self.data = {}
        fp = open(file_path, "r")
        for line in fp:
            row = [t.strip() for t in line.split('\t')]
            self.data[row[0]] = row[1:]

    def getQuestionCat(self, qid):          # Living
        return self.data[qid][0]

    def getQuestionType(self, qid):         # GENERAL/YES_NO
        return self.data[qid][2]

    def getQuestionLabel(self, qid):        # YES/NO/Unsure
        qType = self.getQuestionType(qid)
        if qType == "GENERAL":
            print "error"
            exit()
        elif qType == "YES_NO":
            return labelToInt(self.data[qid][3], 1)

    def getCommentType(self, cid, qid):     #
        qType = self.getQuestionType(qid)
        if qType == "GENERAL":
            return labelToInt(self.data[cid][1], 0)
        elif qType == "YES_NO":
            return labelToInt(self.data[cid][1]+"_"+self.data[cid][2], 1)


class MyXMLHandler(xml.sax.ContentHandler):
    def __init__(self, outDir, file_type):
        self.qtype = ''
        self.ftype = file_type
        fp_general = outDir + 'metadata_general.txt'
        fp_yes_no = outDir + 'metadata_yes_no.txt'
        fp_total = outDir + 'metadata_total.txt'
        self.fp_total = open(fp_total, 'wb')
        self.fp_general = open(fp_general, 'wb')
        self.fp_yes_no = open(fp_yes_no, 'wb')

    # 元素开始事件处理
    def startElement(self, tag, attributes):

        if tag == 'Question':

            qline = ''
            if self.ftype == 2:
                qline = attributes['QID'] + "\t" + attributes['QCATEGORY'] + "\t" + \
                         attributes['QUSERID'] +"\t" + attributes['QTYPE'] + "\n"
            else:
                qline = attributes['QID'] + "\t" + attributes['QCATEGORY'] + "\t" + \
                         attributes['QUSERID'] +"\t" + attributes['QTYPE'] + "\t" + \
                         attributes['QGOLD_YN'] + "\n"

            self.fp_total.write(qline)
            if attributes['QTYPE'] == 'GENERAL':
                self.qtype = 'GENERAL'
                self.fp_general.write(qline)
            else:
                self.qtype = 'YES_NO'
                self.fp_yes_no.write(qline)

        elif tag == 'Comment':

            cline = ''
            if self.ftype == 2:
                cline = attributes['CID'] + "\t" + attributes['CUSERID'] + "\n"
            else:
                cline = attributes['CID'] + "\t" + attributes['CUSERID'] + "\t" + \
                         attributes['CGOLD'] +"\t" + attributes['CGOLD_YN'] + "\n"


            self.fp_total.write(cline)
            if self.qtype == 'GENERAL':
                self.fp_general.write(cline)
            else:
                self.fp_yes_no.write(cline)

        self.fp_total.close()
        self.fp_yes_no.close()
        self.fp_general.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "sys.argv[1]: Parse File Path"
        print "sys.argv[2]: Data Type (train 0, dev 1, test 2)"
        exit()

    outDir = ''             # 文件夹
    file_type = ''          # 文件类型

    if sys.argv[2] == '0':
        outDir = "./train/"
        file_type = 0
    elif sys.argv[2] == '1':
        outDir = "./dev/"
        file_type = 1
    elif sys.argv[2] == '2':
        outDir = "./test/"
        file_type = 2
    else:
        print 'error'
        exit()

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler(outDir, file_type)
    parser.setContentHandler(Handler)

    # 解析文件
    parser.parse(sys.argv[1])

    print "parse " + sys.argv[1] + " done!"


# train file
# python ParseXML_metadata.py CQA-QL-train.xml 0

# dev file
# python ParseXML_metadata.py CQA-QL-devel.xml 1

# test file
# python ParseXML_metadata.py test_task3_English.xml 2


