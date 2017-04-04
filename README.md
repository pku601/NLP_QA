# NLPProjectOne
CQA-QL-train.xml: 训练数据<br>
CQA-QL-devel.xml: 开发数据<br>
test_task3_English.xml: 测试数据<br>

预处理<br>
ParseXML.py: 解析CQA-QL-train.xml中的General问题<br>
ParseXML_for_yes_no.py: 解析CQA-QL-train.xml中的yes-no问题<br>

README.md: this file<br>
Pretreatment_one.py：预处理1<br>
Pretreatment_one.py：预处理2<br>
PretreatmentUtil.py：预处理工具类<br>
test: 测试<br>

## feature/url<br>
ParseXML_has_url.py: 判断CSubject、CBody是否包括链接<br>
result_train_has_url.txt: 训练数据，1表示有，0表示无<br>
result_devel_has_url.txt<br>
result_test_has_url.txt<br>

## General一般类型问题(预处理结果)
devel：开发数据<br>
train：训练数据<br>
pretreatment_one_result_devel_general.txt：预处理中间结果<br>
pretreatment_one_result_train_general.txt：预处理中间结果<br>

## metainfo
ParseXML_metadata.py：获取train,dev,test的元数据信息

## feature/cuserEqualquser
cuserEqualquser.py：判断question的用户ID和comment的用户ID是否相同

## feature/category_probability
category_probability.py：记录每个种类的问题，各种标签的概率


