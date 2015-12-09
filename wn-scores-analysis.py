# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 16:25:43 2015

@author: ashwin
"""
import pickle, heapq
import numpy as np

from nltk.corpus import wordnet as wn


pklfile = open('generated_files/wn-word-corpus.pkl','rb')
sortedList = pickle.load(pklfile)
pklfile.close()

pklfile = open('generated_files/wn-word-corpus-scores.pkl','rb')
sortedListScores = pickle.load(pklfile)
pklfile.close()

pklfile = open('generated_files/base-buckets.pkl','rb')
tasteBucket,healthBucket,speedBucket = pickle.load(pklfile)
pklfile.close()

#print heapq.nlargest(50,[x[0] for x in sortedListScores])

maxTasteIndices = np.argsort([x[0] for x in sortedListScores])[::-1][:41]
tastewords = [sortedList[x] for x in maxTasteIndices]

maxHealthIndices = np.argsort([x[1] for x in sortedListScores])[::-1][:67]
healthwords = [sortedList[x] for x in maxHealthIndices]

maxSpeedIndices = np.argsort([x[2] for x in sortedListScores])[::-1][:81]
speedwords = [sortedList[x] for x in maxSpeedIndices]

tasteBucket = list(set(tasteBucket + tastewords))

healthBucket = list(set(healthBucket + healthwords))

speedBucket = list(set(speedBucket + speedwords))

print len(tasteBucket),tasteBucket
print len(healthBucket),healthBucket
print len(speedBucket),speedBucket

pklfile = open('generated_files/full-buckets.pkl','wb')
pickle.dump([tasteBucket,healthBucket,speedBucket],pklfile)
pklfile.close()
