# -*- coding: UTF-8 -*-

import xml.sax
import logging
import os.path
import sys
import re


global global_qsubject
input_file = ""
output_file = ""
global_qtype = ""
has_url = 0
count = 0
c_subject_body = ""


class get_email_utli:
    def __init__(self, step):  # step 0 train  1 devel  2 test
        if step == 0:
            file_path = "Has_Email/train_email.txt"
        elif step == 1:
            file_path = "Has_Email/devel_email.txt"
        elif step == 2:
            file_path = "Has_Email/test_email.txt"
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

    def get_email_value(self, cid):  # comment id  eg.Q2870_C8
        return self.model[cid]


class MyXMLHandler(xml.sax.ContentHandler):

    def __init__(self, fp):
        self.CurrentData = ""
        self.CSubject = ""
        self.CBody = ""
        self.cbody = False
        self.comment_line = ""
        self.fp = fp

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag

        if tag == 'Comment':
            if 'CID' in attributes:
                self.comment_line += attributes['CID']

        if tag == 'CBody':
            self.cbody = True

        if tag == 'Question':
            if 'QTYPE' in attributes:
                global global_qtype
                global_qtype = attributes['QTYPE']

    # 元素结束事件处理
    def endElement(self, tag):
        email_pattern = '([\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+)'
        if tag == 'Question':

            global global_qtype
            global_qtype = ""

        if tag == 'CSubject':

            global c_subject_body
            c_subject_body += "\t" + self.CSubject.replace("\t", "").replace("\n", " ").strip()

        if tag == 'CBody' and self.cbody:

            c_subject_body += "\t" + self.CBody.replace("\t", "").replace("\n", " ").strip()
            self.cbody = False
            self.CBody = ""

        if tag == 'Comment':

            if re.search(email_pattern, c_subject_body):
                self.comment_line += "\t1"
            else:
                self.comment_line += "\t0"
            # print self.comment_line

            global count
            count += 1
            if count % 200 == 0:
                logger.info("Process " + str(count) + " comments")

            self.fp.write(self.comment_line + '\n')
            self.comment_line = ""
            c_subject_body = ""

            global has_url
            has_url = 0

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "CSubject":
            self.CSubject = content.replace("\t", "").strip()
        if self.CurrentData == "CBody":
            self.CBody += content


if __name__ == '__main__':

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Onput File Path"
        sys.exit(1)
    input_file, output_file = sys.argv[1:3]

    fp = open(output_file, 'wb')

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()

    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler(fp)
    parser.setContentHandler(Handler)

    # 解析输入文件
    parser.parse(input_file)
    fp.close()

# python ParseXML_has_email.py ../../CQA-QL-devel.xml devel_email.txt

# python ParseXML_has_email.py ../../CQA-QL-train.xml train_email.txt

# python ParseXML_has_email.py ../../test_task3_English.xml test_email.txt
