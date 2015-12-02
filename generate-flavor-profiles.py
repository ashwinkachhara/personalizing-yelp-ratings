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
        
    def set(self,t,h,s):
        self.health = h
        self.speed = s
        self.taste = t


def getSentimentConfidence(conf):
    return (e ** conf) / (1 + e**conf)

def getRatingWeight(val):
    return math.log(val,5)

# Returns the sentiment score given a word count and sentiment value. Can expand algorithm later
def getSentimentScore(word_count, sentiment):
    return 1 * word_count if sentiment == 'pos' else -1 * word_count

# Returns a boolean stating if the sentiment score is valid to be added
def isValidSentimentScore(word_count, sentiment):
    return word_count > 0 and getSentimentConfidence(sentiment) > confidenceMin

# Load the file containing all of the reviews with their sentiment values
pklfile = open('generated_files/businesses_sentiment_wc.pkl', 'rb')
reviewsFile = pickle.load(pklfile)
pklfile.close()

pklfile = open('generated_files/reviews_user.pkl', 'rb')
reviewsUser = pickle.load(pklfile)
pklfile.close()


# Use this dictionary of lists to store all of the users flavors to then generate a flavor profile
userSentimentScores = defaultdict(lambda: defaultdict(list))

# Use this dictionary of lists to store all of the restaurants flavors to then generate a flavor profile
restaurantSentimentScores = defaultdict(lambda: defaultdict(list))

# List used to hold all of the calculated business flavor ratings
bizFlavors = {}

# Loop through the file and calculate the values
for businessReviews in reviewsFile.values():
    # Loop through all of the reviews for a given business
    tasteScores = []
    healthScores = []
    speedScores = []
    for reviewIndex in range(len(businessReviews)):
        tasteScoreArray = []
        healthScoreArray = []
        speedScoreArray = []
        
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
                sentimentScore = getSentimentScore(matchedWordCounts[0], sentiments[1])
                tasteScoreArray.append(sentimentScore)
                userSentimentScores[userID]['taste'].append(sentimentScore)

            if isValidSentimentScore(matchedWordCounts[1], sentiments[1]):
                sentimentScore = getSentimentScore(matchedWordCounts[1], sentiments[1])
                healthScoreArray.append(sentimentScore)
                userSentimentScores[userID]['health'].append(sentimentScore)

            if isValidSentimentScore(matchedWordCounts[2], sentiments[1]):
                sentimentScore = getSentimentScore(matchedWordCounts[2], sentiments[1])
                speedScoreArray.append(sentimentScore)
                userSentimentScores[userID]['score'].append(sentimentScore)

        # Apply the calculated sentiment to the review
        tasteScores.append(sum(tasteScoreArray) / float(len(tasteScoreArray)) if len(tasteScoreArray) > 0 else 0)
        healthScores.append(sum(healthScoreArray) / float(len(healthScoreArray)) if len(healthScoreArray) > 0 else 0)
        speedScores.append(sum(speedScoreArray) / float(len(speedScoreArray)) if len(speedScoreArray) > 0 else 0)
    
    # Apply the calculated sentiment to the business
    f = FlavorRating()
    f.taste = sum(tasteScores)/len(tasteScores)
    f.health = sum(healthScores)/len(healthScores)
    f.speed = sum(speedScores)/len(speedScores)
    bizFlavors[businessID] = f;


# Plot graph of flavor ratings
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#for f in bizFlavors.values():
#    print word, wnBucketScores(word)
#    ax.scatter(f.taste, f.health, f.speed, c='r', marker='o')
    
#ax.set_xlabel('tasteScore')
#ax.set_ylabel('healthScore')
#ax.set_zlabel('speedScore')

# plt.show()
#fig.savefig('images/businesses.jpg', dpi=300)

userFlavors = {}

# Draw all of the unique users flavor profiles on a 3D chart
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
for key in userSentimentScores:
    userHealthList = userSentimentScores[key]['health']
    userTasteList = userSentimentScores[key]['taste']
    userSpeedList = userSentimentScores[key]['speed']

    healthValue = sum(userHealthList) / float(len(userHealthList)) if len(userHealthList) > 0 else 0
    tasteValue = sum(userTasteList) / float(len(userTasteList)) if len(userTasteList) > 0 else 0
    speedValue = sum(userSpeedList) / float(len(userSpeedList)) if len(userSpeedList) > 0 else 0
    
    f = FlavorRating()
    f.set(tasteValue,healthValue,speedValue)
    userFlavors[key] = f

#    ax.scatter(tasteValue, healthValue, speedValue, c='r', marker='o')

#ax.set_xlabel('tasteScore')
#ax.set_ylabel('healthScore')
#ax.set_zlabel('speedScore')

#plt.show()
#fig.savefig('images/users.jpg', dpi=300)
# plt.show()

iters = 0

ratingcolors = ['#F93C3C','#F68C2D','#F3E61E','#94F010','#1EED01']

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for key in userFlavors:
    iters = iters + 1
    ax.scatter(userFlavors[key].taste,userFlavors[key].health,userFlavors[key].speed,c='b',marker='p');
    try:
        theirReviews = reviewsUser[key]
    except KeyError:
        pass
#        plt.close(fig)
    else:
        for review in theirReviews:
            f = bizFlavors[review['business_id']]
            col = ratingcolors[review['stars']-1]
            ax.scatter(f.taste, f.health, f.speed, c=col, marker='o')
        ax.set_xlabel('tasteScore')
        ax.set_ylabel('healthScore')
        ax.set_zlabel('speedScore')
        plt.savefig('images/users/'+key+'.jpg',dpi=300)
#        plt.close(fig)
    plt.cla()
#    plt.clf()
#    if iters>50:    
#        break
plt.close()
print("Saved",iters,"figures")
    
        