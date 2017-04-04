# -*- coding: UTF-8 -*-

import xml.sax
import sys

global global_qsubject
global_qsubject = ""
global_qbody = ""
global_qtype = ""


class MyXMLHandler(xml.sax.ContentHandler):
    def __init__(self, fp):
        self.fp = fp
        self.CurrentData = ""
        self.QID = ""
        self.QSubject = ""
        self.QBody = ""
        self.qbody = False
        self.CSubject = ""
        self.CBody = ""
        self.cbody = False
        self.comment_line = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'Comment':
            pass
            # if 'CID' in attributes:
            #     self.comment_line += attributes['CID']
            # if 'CGOLD' in attributes:
            #     self.comment_line += "\t" + attributes['CGOLD']
        if tag == 'QBody':
            self.qbody = True
        if tag == 'CBody':
            self.cbody = True
        if tag == 'Question':
            if 'QTYPE' in attributes:
                global global_qtype
                global_qtype = attributes['QTYPE']
            if 'QID' in attributes:
                self.QID = attributes['QID']

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == 'Question':
            global global_qsubject
            global_qsubject = ""
            global global_qbody
            global_qbody = ""
            global global_qtype
            # if global_qtype == "GENERAL":
            if global_qtype == "YES_NO" or global_qtype == "GENERAL":
                self.fp.write(self.comment_line)
                print self.comment_line
            self.comment_line = ""
            global_qtype = ""
        if tag == 'QSubject':
            # self.comment_line += self.QID + "\t" + self.QSubject
            self.comment_line += self.QSubject
        if tag == "QBody":
            self.comment_line += " " + self.QBody.replace("\t", "").replace("\n", " ").strip() + "\n"
            self.qbody = False
            self.QBody = ""
        if tag == 'CSubject':
            # self.comment_line += "\t" + self.CSubject
            self.comment_line += self.CSubject
        if tag == 'CBody' and self.cbody:
            self.comment_line += " " + self.CBody.replace("\t", "").replace("\n", " ").strip() + "\n"
            self.cbody = False
            self.CBody = ""
        # if tag == 'Comment':
        #     global_qsubject
        #     global_qbody
        #     self.comment_line += "\t" + global_qsubject + "\t" + global_qbody
        #     print self.comment_line
        #     global_qtype
        #     if global_qtype == "GENERAL":
        #         fp
        #         fp.write(self.comment_line + '\n')
        #     self.comment_line = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "QSubject":
            self.QSubject = content.replace("\t", "").strip()
            global global_qsubject
            global_qsubject += content.replace("\t", "").strip()
        if self.CurrentData == "QBody":
            self.QBody += content
            global global_qbody
            global_qbody += content.replace("\t", "").strip()
        if self.CurrentData == "CSubject":
            self.CSubject = content.replace("\t", "").strip()
        if self.CurrentData == "CBody":
            self.CBody += content


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "sys.argv[1]: Input File Path"
        print "sys.argv[2]: Output File Path"
        exit()

    fp = open(sys.argv[2], 'wb')

    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = MyXMLHandler(fp)
    parser.setContentHandler(Handler)

    parser.parse(sys.argv[1])
    fp.close()

# python Pretreatment_one_2.py ../CQA-QL-devel.xml Total/pretreatment_one_result_devel_total_2.txt

# python Pretreatment_one_2.py ../CQA-QL-train.xml Total/pretreatment_one_result_train_total_2.txt

# python Pretreatment_one_2.py ../test_task3_English.xml Total/pretreatment_one_result_test_total_2.txt
