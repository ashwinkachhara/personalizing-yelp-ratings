# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 12:46:15 2015

@author: ashwin
"""
import pickle
import math
from sklearn.cross_validation import KFold
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score

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

# Calculate the distance
def distance(f1, f2):
    return ((f2.taste - f1.taste)**2 + (f2.health - f1.health)**2 + (f2.speed - f1.speed)**2)**.5

def getRatingWeight(val):
#    We use a logarithmic function. 1star = 0, 5star = 1
    return math.log(val,5)


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

def fitting(their_reviews, labels):
    taste_array = []
    health_array = []
    speed_array = []

    wtsum = 0
    for rev in their_reviews:
        bf = FlavorRating()
        try:
            bf = bizFlavors[rev['business_id']]
        except KeyError:
            pass
        else:
            wt = getRatingWeight(rev['stars'])
            wtsum = wtsum + wt
            taste_array.append(bf.taste*wt)
            health_array.append(bf.health*wt)
            speed_array.append(bf.speed*wt)
    f = FlavorRating()
    f.set(sum(taste_array)/wtsum, sum(health_array)/wtsum, sum(speed_array)/wtsum)

    maxVal = 0
    # Loop through reviews again
    for i in range(len(their_reviews)):
        bf = FlavorRating()
        try:
            bf = bizFlavors[their_reviews[i]['business_id']]
        except KeyError:
            pass
        else:
            if labels[i]:
                maxVal = max(maxVal, distance(f,bf))
    return f, maxVal

def predict(reviews, radius, user_flavor_rating):
    predictions = []
    for rev in reviews:
        bf = FlavorRating()
        try:
            bf = bizFlavors[rev['business_id']]
        except KeyError:
            pass
        else:
            predictions.append(distance(user_flavor_rating, bf) > radius)
    return np.array(predictions)

def performAnalysis(data):
    # Use K Folds for cross-validation to perform analysis on unseen data
    k_fold = KFold(n=len(data), n_folds=5)
    scores = []
    confusion = np.array([[0, 0], [0, 0]])
    ratings = [x['stars'] > 3 for x in data]
    data = np.array(data)
    ratings = np.array(ratings)
    for train_indices, test_indices in k_fold:
        train_biz = data[train_indices]
        train_rating = ratings[train_indices]

        test_biz = data[test_indices]
        test_rating = ratings[test_indices]

        # pipeline.fit(train_text, train_y)
        # predictions = pipeline.predict(test_text)
        user_rating, rating_radius = fitting(train_biz, train_rating)
        predictions = predict(test_biz, rating_radius, user_rating)

        confusion += confusion_matrix(test_rating, predictions)
        score = f1_score(test_rating, predictions, pos_label=True)
        scores.append(score)

    #print out reporting data
    print('Total reviews analyzed:', len(data))
    print('Score:', sum(scores)/len(scores))
    print('Confusion matrix:')
    print(confusion)

    outfile.write(str(len(data))+','+str(sum(scores)/len(scores))+','+str(confusion[0][0])+','+str(confusion[0][1])+','+str(confusion[1][0])+','+str(confusion[1][1])+'\n')

outfile = file('generated_files/validation.csv','w')

for uid in top20:
    reviews = reviewsUser[uid]
    performAnalysis(reviews)

outfile.close()
