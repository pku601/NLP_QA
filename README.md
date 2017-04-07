# NLP_QA

## SemEval-2015 Task 3: Answer Selection in Community Question Answering
http://alt.qcri.org/semeval2015/task3/

CQA-QL-train.xml: 训练数据<br>
CQA-QL-devel.xml: 开发数据<br>
test_task3_English.xml: 测试数据<br>

Pretreatment: 预处理<br>
Pretreatment_one.py：预处理1<br>
Pretreatment_one.py：预处理2<br>
PretreatmentUtil.py：预处理工具类<br>

README.md: this file<br>

## feature/url<br>
ParseXML_has_url.py: 判断CSubject、CBody是否包括链接<br>
train_has_url.txt: 训练数据，1表示有，0表示无<br>
devel_has_url.txt<br>
test_has_url.txt<br>

## feature/metainfo
ParseXML_metadata.py：获取train,dev,test的元数据信息

## feature/cuserEqualquser
cuserEqualquser.py：判断question的用户ID和comment的用户ID是否相同

## feature/category_probability
category_probability.py：记录每个种类的问题，各种标签的概率


