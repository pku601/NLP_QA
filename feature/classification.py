# -*- coding: utf-8 -*-

import sys
from sklearn import tree
from sklearn import svm
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB

import numpy as np
import pickle

GENERAL_NUM_CLASS = 6
YES_NO_NUML_CLASS = 3


#notice, we only use gbdt, essemble, tree, knn and svm classifier
#you can add others if you need

def getOneHotVec(X, num_class):
    X = np.array([int(x) for x in X])
    one_hot = np.zeros((X.shape[0], num_class))
    one_hot[np.arange(X.shape[0]), X] = 1
    return one_hot


class Classification:
    def __init__(self, classifier, trainFile, testFile):

        data = pickle.load(open(trainFile, "r"))
        data = np.array(data)

        test_data = pickle.load(open(testFile, "r"))
        test_data = np.array(test_data)

        # f = open(trainFile, "r")
        # data = np.loadtxt(f)
        # features = pickle.load(f)
        # get_x_train = [feature[1:-1] for feature in features]
        # get_y_train = [feature[-1] for feature in features]
        
        # select columns 1 through end
        X_train = data[:, 1:-1]         # cid features label
        y_train = data[:, -1]
        # y_train = getOneHotVec(y_train, GENERAL_NUM_CLASS)
            
        # f = open(devFile)
        # pre = np.loadtxt(f)
        X_test = test_data[:, 1:]       # cid features
        # y_test = test_data[:, -1]
        self.cid = test_data[:, 0]
        # self.qid = test_data[:, 1]
        
        # min_max_scaler = MinMaxScaler()
        # X_train = min_max_scaler.fit_transform(X_train)
        # X_test = min_max_scaler.fit_transform(X_test)

        # fit transform if there exit NAN or INFINITE
        # otherwise you'll get error when clf.predict()
        # X_test = Imputer().fit_transform(X_test)
        # if np.isnan(X_test).any():
        #     print "nan in X_test!"
        #     exit()
            
        # self.y_test = pre[:, 0]
        # f.close()
        
        if classifier == 'tree':
            # max_depth = 4 is best
            # max_depth = np.arange(1, 10)
            # clf = GridSearchCV(tree.DecisionTreeClassifier(), param_grid = {'max_depth': max_depth})
            clf = tree.DecisionTreeClassifier(max_depth = 4)
            
        elif classifier == 'knn':
            # n_neighbors = 9 is best
            # but default is 5, better than 9?
            # n_neighbors = np.arange(1, 10)  
            # clf = GridSearchCV(KNeighborsClassifier(), param_grid = {'n_neighbors': n_neighbors})
            clf = KNeighborsClassifier(n_neighbors = 9)
            
        elif classifier == 'svm':
            # {'kernel': 'rbf', 'C': 100, 'gamma': 0.001}
            # param_grid = [{'C': [1, 10, 100, 1000], 'kernel': ['linear']},
            # {'C': [1, 10, 100, 1000], 'gamma': [0.001, 0.0001], 'kernel': ['rbf']}]
            # clf = GridSearchCV(svm.SVC(), param_grid)
            clf = svm.SVC(kernel='rbf', gamma = 0.001, C = 100)
            
        elif classifier == 'gbdt':
            # max_depth = np.arange(1, 10)
            # n_estimators = [10, 100, 1000]
            # learning_rate = [0.1, 0.2, 0.3, 0.4, 0.5]
            # clf = GridSearchCV(GradientBoostingClassifier(), param_grid =
            # {'max_depth': max_depth, 'n_estimators': n_estimators, 'learning_rate': learning_rate})  2 6
            clf = GradientBoostingClassifier(n_estimators = 41, learning_rate=0.2, max_depth = 2, random_state=10)
            
        elif classifier == 'essemble':
            # {'n_estimators': 10, 'max_depth': 6}
            # max_depth = np.arange(1, 10)
            # n_estimators = [10, 100, 1000]
            # clf = GridSearchCV(RandomForestClassifier(), param_grid =
            # {'max_depth': max_depth, 'n_estimators': n_estimators})
            clf = RandomForestClassifier(n_estimators = 20,  max_depth=20, random_state=50)  # 100,90,46%
            
        elif classifier == 'nb':
            clf = MultinomialNB()
            print clf
        else:
            print "Invalid classifier in Class Classification __init__()!"
            exit()

        # print X_train.shape
        # print y_train.shape
        clf.fit(X_train, y_train) 
        # print clf.best_params_
        
        self.y_pred = clf.predict(X_test)
        
        '''
        #test usage!
        self.calculate_result(self.y_test, self.y_pred)
        print( "ACC:  %f " %accuracy_score(y_test,y_pred))
        '''
    def int2Label(self, lbid, type):
        if type == 0:   # general
            if lbid == 0:
                return "Good"
            elif lbid == 1:
                return "Bad"
            elif lbid == 2:
                return "Potential"
            elif lbid == 3:
                return "Dialogue"
            elif lbid == 4:
                return "Not English"
            elif lbid == 5:
                return "Other"
            else:
                return "error"
        elif type == 1:         # yes no
            if lbid == 0:
                return "Yes"
            elif lbid == 1:
                return "No"
            elif lbid == 2:
                return "Unsure"
        else:
            return "error"

    def getPreResult(self, outputFile, type):
        fout = open(outputFile,"w+")
        if type == 0:   # taskA
            for idx, each in enumerate(self.y_pred):
                fout.write(self.cid[idx] + "\t" + self.int2Label(int(each), 0) + "\n")
        fout.close()        
   
    # this function is used for testing!
    def calculate_result(self):  
        m_precision = metrics.precision_score(self.y_test, self.y_pred)
        m_recall = metrics.recall_score(self.y_test, self.y_pred) 
        print 'precision:{0:.3f}'.format(m_precision)  
        print 'recall:{0:0.3f}'.format(m_recall) 
        print 'f1-score:{0:.3f}'.format(metrics.f1_score(self.y_test, self.y_pred))    
    
if __name__ == "__main__":
    if len(sys.argv) < 6:
        print "sys.argv[1]: classifier"  # svm and so on
        print "sys.argv[2]: trainFile"
        print "sys.argv[3]: devFile"
        print "sys.argv[3]: outputFile"
        print "sys.argv[4]: task type(0 taskA, 1 taskB)"
        exit()

    cfInstance = Classification(sys.argv[1], sys.argv[2], sys.argv[3])
    cfInstance.getPreResult(sys.argv[4], int(sys.argv[5]))

# devel
# taskA
# python classification.py essemble ./train_total_taskA.pkl ./devel_total_taskA.pkl  ./devel_subtaskA_result.txt 0

# perl taskA
# perl SemEval2015-task3-scorer-subtaskA.pl CQA-QL-devel-gold.txt devel_subtaskA_result.txt

# test
# taskA
# python classification.py essemble ./train_total_taskA.pkl ./test_total_taskA.pkl  ./test_subtaskA_result.txt 0

# perl taskA
# perl SemEval2015-task3-scorer-subtaskA.pl CQA-QL-test-gold.txt test_subtaskA_result.txt
