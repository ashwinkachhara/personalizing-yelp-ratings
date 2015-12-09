# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:36:16 2015

@author: ashwin
"""
import pickle
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from buckets import *

import sys, os

from nltk.corpus import wordnet as wn

def wnBucketScores(word):
    tasteScore = 0
    healthScore = 0
    speedScore = 0
    score = 0
    scorenum = 0
    for taste in wnTasteBucket:
    #    print taste
        for s in wn.synsets(word):
            sim = taste.path_similarity(s)
            if sim:
                score = score + sim
                scorenum = scorenum+1
    #        print taste,s,sim,word
    if scorenum>0:
        tasteScore = score/scorenum
    else:
        tasteScore = 0

    score = 0
    scorenum = 0
    for taste in wnHealthBucket:
    #    print taste
        for s in wn.synsets(word):
            sim = taste.path_similarity(s)
            if sim:
                score = score + sim
                scorenum = scorenum+1
    #        print taste,s,sim,word
    if scorenum>0:
        healthScore = score/scorenum
    else:
        healthScore = 0

    score = 0
    scorenum = 0
    for taste in wnSpeedBucket:
    #    print taste
        for s in wn.synsets(word):
            sim = taste.path_similarity(s)
            if sim:
                score = score + sim
                scorenum = scorenum+1
    #        print taste,s,sim,word
    if scorenum>0:
        speedScore = score/scorenum
    else:
        speedScore = 0

    return [tasteScore,healthScore,speedScore]

pklfile = open('generated_files/wn-word-corpus.pkl','rb')
sortedList = pickle.load(pklfile)
pklfile.close()

sortedListScores = []

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for word in sortedList:
#    print word, wnBucketScores(word)
    vals = wnBucketScores(word)
    sortedListScores.append(vals)
    ax.scatter(vals[0], vals[1], vals[2],c='r',marker='o')

ax.set_xlabel('tasteScore')
ax.set_ylabel('healthScore')
ax.set_zlabel('speedScore')

plt.show()

pklfile = open('generated_files/wn-word-corpus-scores.pkl','wb')
pickle.dump(sortedListScores,pklfile)
pklfile.close()
