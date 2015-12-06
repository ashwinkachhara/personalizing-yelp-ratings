# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 12:46:15 2015

@author: ashwin
"""
import pickle

class FlavorRating:
    def __init__(self):
        self.health = 0
        self.speed = 0
        self.taste = 0
        self.reviewCount = 0
        self.totalMatchedWordCount = 0
        
#    Sets values of t,h,s
    def set(self,t,h,s):
        self.health = h
        self.speed = s
        self.taste = t
        
#    Prints to console
    def show(self):
        print self.taste,self.health,self.speed


pklfile = open('generated_files/business_FlavorRatings.pkl', 'rb')
bizFlavors = pickle.load(pklfile)
pklfile.close()

#Load the file containting all reviews indexed by user id
pklfile = open('generated_files/reviews_user.pkl', 'rb')
reviewsUser = pickle.load(pklfile)
pklfile.close()

def getKey(item):
    return len(reviewsUser[item])

top20 = sorted(reviewsUser.keys(),key=getKey)[::-1][:20]