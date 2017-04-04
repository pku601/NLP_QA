# -*- coding: UTF-8 -*-

# calculate two string words vector

import copy
from scipy import linalg, mat, dot

class BOW:
    def __init__(self, s1, s2):
        if not (s1 and s2):
            print "Empty s1 or s2 in Class BOW __init__()!"
            exit()

        self.allBag = {}
        list1 = s1.strip().split(" ")
        list2 = s2.strip().split(" ")

        for w in list1:
            if w not in self.allBag:
                self.allBag[w] = 0
        for w in list2:
            if w not in self.allBag:
                self.allBag[w] = 0

        self.bag1 = copy.deepcopy(self.allBag)
        self.bag2 = copy.deepcopy(self.allBag)
        for w in list1:
            self.bag1[w] += 1
        for w in list2:
            self.bag2[w] += 1


    def getVector(self):
        vector1 = []
        vector2 = []
        for word in self.allBag:
            vector1.append(self.bag1[word])
            vector2.append(self.bag2[word])
        return vector1, vector2

    def cosine(self, list1, list2):
        a = mat(list1)
        b = mat(list2)
        c = dot(a, b.T) / linalg.norm(a) / linalg.norm(b)
        return c[0, 0]

    def getVectorSim(self):
        v1, v2 = self.getVector()
        return self.cosine(v1, v2)
