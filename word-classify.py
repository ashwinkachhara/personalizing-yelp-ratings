# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 07:48:33 2015

@author: ashwin
"""

import pickle
import json

from buckets import *

import sys, os
sys.path.append(os.getcwd()+'/cortical/')
from cortical.client import ApiClient
from compareApi import CompareApi

from nltk.corpus import wordnet as wn


class Cortical:
    BASE_PATH = "http://api.cortical.io/rest"
    API_KEY = "4b6b3100-bf81-11e4-b8ca-f119f1630c46"
    RETINA_NAME = "en_associative"
    def __init__(self):
        self.compareApi = CompareApi(ApiClient(apiKey=self.API_KEY, apiServer=self.BASE_PATH))

    def similarity(self, s1="", s2=""):
        body = json.dumps([{"text": s1},{"text": s2}])
        result = self.compareApi.compare(self.RETINA_NAME, body)
        
#        print result.weightedScoring
#        print result.cosineSimilarity
#        print result.jaccardDistance
#        print result.euclideanDistance
        return result.weightedScoring
    def bulkSimilarity(self,s1="",s2=[]):
        req = '['
        for word in s2:
            req = req + json.dumps([{"text": s1},{"text": word}]) + ','
        req = req[:-1]+']'
        
        result = self.compareApi.compareBulk(self.RETINA_NAME,req)
        
        return [r.weightedScoring for r in result]
            

def bulkBucketSimilarity(word):
    tastevector = c.bulkSimilarity(word,tasteBucket)
    
    healthvector = c.bulkSimilarity(word,healthBucket)
    
    speedvector = c.bulkSimilarity(word,speedBucket)
    
    tastevector = [x for x in tastevector if x!=0.0]
    healthvector = [x for x in healthvector if x!=0.0]
    speedvector = [x for x in speedvector if x!=0.0]
#    print tastevector
#    print healthvector
#    print speedvector
#    val1=0,val2=0,val3=0
    try:
        val1 = sum(tastevector)/len(tastevector)
    except (ZeroDivisionError,Exception):
        val1 = 0
    try:
        val2 = sum(healthvector)/len(healthvector)
    except (ZeroDivisionError,Exception):
        val2 = 0
    try:
        val3 = sum(speedvector)/len(speedvector)
    except (ZeroDivisionError,Exception):
        val3 = 0
    
    
    return [val1,val2,val3]
      

def bucketSimilarity(word):
    tastevector = []
    for bucketword in tasteBucket:
        try:
            newval = c.similarity(word,bucketword)
#            print newval,bucketword
            tastevector.append(newval)
        except Exception:
            pass
    
    healthvector = []
    for bucketword in healthBucket:
        try:
            newval = c.similarity(word,bucketword)
#            print newval,bucketword
            healthvector.append(newval)
        except Exception:
            pass
    
    speedvector = []
    for bucketword in speedBucket:
        try:
            newval = c.similarity(word,bucketword)
#            print newval,bucketword
            speedvector.append(newval)
        except Exception:
            pass
    
    return [sum(tastevector)/len(tastevector),sum(healthvector)/len(healthvector),sum(speedvector)/len(speedvector)]


pklfile = open('word_corpus.pkl','rb')
sortedList = pickle.load(pklfile)
pklfile.close()

c = Cortical()
print c.similarity("spicy","tasteless")
#print c.bulkSimilarity("spicy",tasteBucket)

#print bulkBucketSimilarity("terrible speed")
#print bulkBucketSimilarity("spicy")


#simvalues = []
#
#for word in sortedList[6000:6010]:
#    if sortedList.index(word)%10000 == 0:
#        print sortedList.index(word)
#    simvalues.append(bulkBucketSimilarity(word))
#    
##pklfile = open('bucketsim.pkl','wb')
##pickle.dump(simvalues,pklfile)
##pklfile.close()
#print simvalues

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
    
pklfile = open('wn-word-corpus.pkl','wb')
pickle.dump(sortedList,pklfile)
pklfile.close()

