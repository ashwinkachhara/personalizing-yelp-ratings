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
import pickle

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

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


def getSentimentConfidence(conf):
    return (e ** conf) / (1 + e**conf)


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

# List used to hold all of the calculated business flavor ratings
bizFlavors = []

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
        
        matchedWCList = reviewItem['matchedWC']

        # Calculate the review sentiment using all the values in the list
        for index in range(len(sentimentList)):
            # Get the reviews sentiments and associated wordCounts for the algorithm
            sentiments = sentimentList[index]
            matchedWordCounts = matchedWCList[index]

            # IF neutral, do not factor in the values
            if sentiments[0] == 'neutral':
                continue
            
            if isValidSentimentScore(matchedWordCounts[0], sentiments[0]):
                tasteScoreArray.append(getSentimentScore(matchedWordCounts[0], sentiments[0]))

            if isValidSentimentScore(matchedWordCounts[1], sentiments[1]):
                healthScoreArray.append(getSentimentScore(matchedWordCounts[1], sentiments[1]))

            if isValidSentimentScore(matchedWordCounts[2], sentiments[2]):
                speedScoreArray.append(getSentimentScore(matchedWordCounts[2], sentiments[2]))

        # Apply the calculated sentiment to the review
        tasteScores.append(sum(tasteScoreArray) / float(len(tasteScoreArray)) if len(tasteScoreArray) > 0 else 0)
        healthScores.append(sum(healthScoreArray) / float(len(healthScoreArray)) if len(healthScoreArray) > 0 else 0)
        speedScores.append(sum(speedScoreArray) / float(len(speedScoreArray)) if len(speedScoreArray) > 0 else 0)
    
    # Apply the calculated sentiment to the business
    f = FlavorRating()
    f.taste = sum(tasteScores)/len(tasteScores)
    f.health = sum(healthScores)/len(healthScores)
    f.speed = sum(speedScores)/len(speedScores)
    bizFlavors.append(f)


# After looping through the file, finalize all calculations for Businesses and Users

# Save data to either 1 or multiple files

# Plot graph of flavor ratings
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for f in bizFlavors:
#    print word, wnBucketScores(word)
    ax.scatter(f.taste, f.health, f.speed, c='r', marker='o')
    
ax.set_xlabel('tasteScore')
ax.set_ylabel('healthScore')
ax.set_zlabel('speedScore')

# plt.show()
# fig1 = plt.gcf()
fig.savefig('test.jpg', dpi=300)