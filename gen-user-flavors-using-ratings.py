# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 17:19:13 2015

@author: ashwin
"""
# Use businesses_with_sentiment.pkl
# Need to compute flavor profile for businesses AND individual users
#     Each review has a List of sentiment analysis [ 'type', confidenceVal ] ex: [ 'pos', .9 ] (pos,neg,neutral)
#     Algorithms --
#         Business Flavor Profile
#             Sum all users values? Normalize?
#         User Flavor Profile
#             #wordMatches? business star rating? User star rating?
# Store the business ID and flavor profile into file
# Store users and their flavor profiles into a file
import pickle, math

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict

# Used for the sentiment confidence value
e = 2.718281828459045
confidenceMin = .5

# Class used to hold a flavor rating
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

#Return sentiment confidence betweeen 0 and 1
def getSentimentConfidence(conf):
    return (e ** conf) / (1 + e**conf)

#Return rating weights to calculate user FlavorRating
def getRatingWeight(val):
#    We use a logarithmic function. 1star = 0, 5star = 1
    return math.log(val,5)

# Returns the [sentiment score, weight] given a word count and sentiment value. Can expand algorithm later
def getSentimentScore(word_count, sentiment):
#    Provision for weighting positive sentiments and negative sentiments differently
    poswt = 3
    negwt = 1
    if sentiment == 'pos':
        return [poswt*word_count,poswt]
    else:
        return [-negwt*word_count,negwt]

# Returns a boolean stating if the sentiment score is valid to be added
def isValidSentimentScore(word_count, sentiment):
    return word_count > 0 and getSentimentConfidence(sentiment) > confidenceMin

# Load the file containing all of the reviews with their sentiment values (indexed by business id)
pklfile = open('generated_files/businesses_sentiment_wc.pkl', 'rb')
reviewsFile = pickle.load(pklfile)
pklfile.close()

#Load the file containting all reviews indexed by user id
pklfile = open('generated_files/reviews_user.pkl', 'rb')
reviewsUser = pickle.load(pklfile)
pklfile.close()

# Use this dictionary of lists to store all of the restaurants flavors to then generate a flavor profile
restaurantSentimentScores = defaultdict(lambda: defaultdict(list))

# Dict used to hold all of the calculated business flavor ratings, indexed by business_id
bizFlavors = {}

# Loop through the file and calculate the values
for businessReviews in reviewsFile.values():
    # Loop through all of the reviews for a given business
    tasteScores = []
    healthScores = []
    speedScores = []
    for reviewIndex in range(len(businessReviews)):
#        Arrays to store sentiment scores
        tasteScoreArray = []
        healthScoreArray = []
        speedScoreArray = []
        
#        Arrays to store weights, to normalize tasteScore for restaurant
        tasteWtsArray = []
        healthWtsArray = []
        speedWtsArray = []
        
        # Get the current review object
        reviewItem = businessReviews[reviewIndex]

        # Get the current business ID
        businessID = reviewItem['business_id']

        # Get the current User ID
        userID = reviewItem['user_id']

        # Get the sentiment list of lists
        sentimentList = reviewItem['sentiment']

        # Get the list of the current reviews matched word count
        matchedWCList = reviewItem['matchedWC']

        # Calculate the review sentiment using all the values in the list
        for index in range(len(sentimentList)):
            # Get the reviews sentiments and associated wordCounts for the algorithm
            sentiments = sentimentList[index]
            matchedWordCounts = matchedWCList[index]

            # IF neutral, do not factor in the values
            if sentiments[0] == 'neutral':
                continue
            
            if isValidSentimentScore(matchedWordCounts[0], sentiments[1]):
                sentimentScore, sentimentWt = getSentimentScore(matchedWordCounts[0], sentiments[1])
                tasteScoreArray.append(sentimentScore)
                tasteWtsArray.append(sentimentWt)

            if isValidSentimentScore(matchedWordCounts[1], sentiments[1]):
                sentimentScore, sentimentWt = getSentimentScore(matchedWordCounts[1], sentiments[1])
                healthScoreArray.append(sentimentScore)
                healthWtsArray.append(sentimentWt)

            if isValidSentimentScore(matchedWordCounts[2], sentiments[1]):
                sentimentScore, sentimentWt = getSentimentScore(matchedWordCounts[2], sentiments[1])
                speedScoreArray.append(sentimentScore)
                speedWtsArray.append(sentimentWt)

        # Apply the calculated sentiment to the review
        tasteScores.append(sum(tasteScoreArray) / float(sum(tasteWtsArray)) if len(tasteScoreArray) > 0 else 0)
        healthScores.append(sum(healthScoreArray) / float(sum(healthWtsArray)) if len(healthScoreArray) > 0 else 0)
        speedScores.append(sum(speedScoreArray) / float(sum(speedWtsArray)) if len(speedScoreArray) > 0 else 0)
    
    # Apply the calculated sentiment to the business
    f = FlavorRating()
    f.taste = sum(tasteScores)/len(tasteScores)
    f.health = sum(healthScores)/len(healthScores)
    f.speed = sum(speedScores)/len(speedScores)
    bizFlavors[businessID] = f;

# Dict used to hold all of the calculated business flavor ratings, indexed by user_id
userFlavors = {}

#Calculating the userFlavors as a weighted average of the restaurants they reviewed
for key in reviewsUser:
    tasteArray = []
    healthArray = []
    speedArray = []
    
    wtsum = 0
    try:
        theirReviews = reviewsUser[key]
    except KeyError:
        #        Excluding the case where the user might not be present in our data (from diff region, or had only <5 reviews, etc
        pass
    else:
#        We compute userFlavor if the user did not trigger a KeyError
        for rev in theirReviews:
            bf = FlavorRating()
            try:
                bf = bizFlavors[rev['business_id']]
            except KeyError:
                pass
            else:
#                bf.show()
                wt = getRatingWeight(rev['stars'])
#                print 5**wt,wt
                wtsum = wtsum + wt
                tasteArray.append(bf.taste*wt)
                healthArray.append(bf.health*wt)
                speedArray.append(bf.speed*wt)
        f = FlavorRating()
#        print tasteArray,healthArray,speedArray
        f.set(sum(tasteArray)/wtsum,sum(healthArray)/wtsum,sum(speedArray)/wtsum)
#        f.show()
        userFlavors[key] = f
    

iters = 0

#Color coding reviews on the user-their_reviews graph 0-red -> Gradient <- 4-green
ratingcolors = ['#F93C3C','#F68C2D','#F3E61E','#94F010','#1EED01']

#We create a scatter plot for each user and store it in specified directory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for key in userFlavors:
    ax.scatter(userFlavors[key].taste,userFlavors[key].health,userFlavors[key].speed,c='b',marker='p');
    try:
        theirReviews = reviewsUser[key]
    except KeyError:
        pass
#        plt.close(fig)
    else:
        iters = iters + 1
        if len(theirReviews)>=5:
            for review in theirReviews:
                f = bizFlavors[review['business_id']]
                col = ratingcolors[review['stars']-1]
                ax.scatter(f.taste, f.health, f.speed, c=col, marker='o')
            ax.set_xlabel('tasteScore')
            ax.set_ylabel('healthScore')
            ax.set_zlabel('speedScore')
#            ax.set_xlim3d(-1,1)
#            ax.set_ylim3d(-1,1)
#            ax.set_zlim3d(-1,1)
            plt.savefig('images/users/'+key+'.jpg',dpi=300)
    plt.cla()
#    if iters>50:    
#        break
plt.close()
print("Saved",iters,"figures")

pklfile = open('generated_files/business_FlavorRatings.pkl', 'wb')
pickle.dump(bizFlavors, pklfile)
pklfile.close()

pklfile = open('generated_files/users_FlavorRatings.pkl', 'wb')
pickle.dump(userFlavors, pklfile)
pklfile.close()
    
        