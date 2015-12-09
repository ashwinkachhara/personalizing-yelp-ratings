# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 07:48:33 2015

@author: ashwin
"""

import pickle
import json

from buckets import *

import sys, os

from nltk.corpus import wordnet as wn

pklfile = open('generated_files/word_corpus.pkl','rb')
sortedList = pickle.load(pklfile)
pklfile.close()


initsize = len(sortedList)
removalsIndex = []
for i in range(initsize):
#    print word,"*********",wn.synsets(word)
#    if (i%10000 == 0):
#        print i
    if len(wn.synsets(sortedList[i])) == 0:
        removalsIndex.append(sortedList[i])
print len(removalsIndex),len(sortedList)

for index in removalsIndex:
    print index
    sortedList.remove(index)

pklfile = open('generated_files/wn-word-corpus.pkl','wb')
pickle.dump(sortedList,pklfile)
pklfile.close()
