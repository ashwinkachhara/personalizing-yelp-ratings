# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:18:25 2015

@author: ashwin
"""

import pickle
## $ pip install pattern
from pattern.web import Twitter
from pattern.web import plaintext
from pattern.en.wordlist import PROFANITY

## $ pip install vaderSentiment
from vaderSentiment.vaderSentiment import sentiment

pklfile = open('reviews.pkl','rb')
reviews = pickle.load(pklfile)
pklfile.close()

pklfile = open('restaurants.pkl','rb')
restaurants = pickle.load(pklfile)
pklfile.close()

pklfile = open('reviews_user.pkl','rb')
reviews_user = pickle.load(pklfile)
pklfile.close()

pklfile = open('users.pkl','rb')
users = pickle.load(pklfile)
pklfile.close()


snooty = []
allwords = []
mytest = reviews.values()[0]
for i in range(len(mytest)):
    review = mytest[i]['text']
#    print review
#    ptreview = plaintext(review['text']).encode('utf-8')
    # word list
    words = review.split()
#    print words
    allwords += words
    snooty += [w for w in words if w in PROFANITY]
    
    # sentiment
    print review
    vs = sentiment(review)
    print str(vs),'\n', mytest[i]['stars'],'\n', mytest[i]['votes'], '\n'
