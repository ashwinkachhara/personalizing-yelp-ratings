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


# Class used to hold a flavor rating
class FlavorRating:
    def __init__(self):
        self.health = 0
        self.speed = 0
        self.taste = 0
        self.reviewCount = 0


# Load the file containing all of the reviews with their sentiment values
pklfile = open('generated_files/businesses_with_sentiment', 'rb')
reviewsFile = pickle.load(pklfile)
pklfile.close()

# Loop through the file and calculate the values
for businessReviews in reviewsFile.values():
    # Loop through all of the reviews for a given business
    for reviewIndex in range(len(businessReviews)):
        # Get the current review object
        reviewItem = businessReviews[reviewIndex]

        # Get the review text
        reviewText = reviewItem['text']
