# loop through all sentences
# use buckets of words along with sentences to generate sentiment
# Compare words in sentence to words in bucket. If word matched perform a sentiment analysis.
# Possible algorithm
# wordMatches * sentiment  summed over all sentences
import json, sys, os

from random import randrange
from nltk.tokenize import sent_tokenize

from sentiment.info import setup, MyDict, classify2, classify_demo
setup()

# Create Flavor Class to store values
class FlavorRating:
    def __init__(self):
        self.health = 0
        self.speed = 0
        self.taste = 0


# Create helper functions
def get_sentiment(text):
    # Get the sentiment
    sentiment = classify2(text)
    # print sentiment

    if sentiment[0] and (sentiment[1] > .5):
        return 'pos'

    if not sentiment[0] and (sentiment[1] > .5):
        return 'neg'
    return 'net'


def taste_algorithm():
    return .2


# Get a set of words for all of the grouping buckets
tasteBucket = {"goldberg", "test1", "test2"}
healthBucket = {"test", "general", "test2"}
speedBucket = {"trying", "have", "test2"}

# Load the file containing all of the reviews
# NOTE: TEMP FILE FOR TESTING
reviewsFile = open('data/yelp_academic_dataset_review.json')

# Create arrays to hold flavor values, we will average after processing all reviews
healthScoreArray = []
speedScoreArray = []
tasteScoreArray = []

index = 0;
# Loop through all of the reviews -- should either be for a user OR a business
for line in reviewsFile:
    index += 1
    # Get the review json
    reviewJson = json.loads(line)

    # Get the review text
    review = reviewJson['text']

    # Tokenize each of the sentences from the review
    reviewSentences = sent_tokenize(review)

    # Loop through all of the sentences
    for sentence in reviewSentences:
        # Lowercase the sentence for matching
        sentence = sentence.lower()

        # Get the set of words in the sentence
        sentenceWordSet = set(sentence.split())

        # Check to see if the sentence contains any of the key-words
        hasTaste = True if tasteBucket & sentenceWordSet else False
        hasSpeed = True if speedBucket & sentenceWordSet else False
        hashealth = True if healthBucket & sentenceWordSet else False

        # Get which grouping the sentence falls under
        sentimentGroup = get_sentiment(sentence)

        # If neutral, skip this sentence
        if sentimentGroup == 'net':
            break

        print sentence
        print sentimentGroup

        # Try all of the buckets that matched
        if hasTaste:
            tasteScoreArray.append(-1 * taste_algorithm() if sentimentGroup == 'neg' else taste_algorithm())

        if hasSpeed:
            speedScoreArray.append(-1 * taste_algorithm() if sentimentGroup == 'neg' else taste_algorithm())

        if hashealth:
            healthScoreArray.append(-1 * taste_algorithm() if sentimentGroup == 'neg' else taste_algorithm())

    if index > 50:
        break

# Generate an overall flavorRating
flavorRating = FlavorRating()

# Set the flavor rating values
flavorRating.health = sum(healthScoreArray) / float(len(healthScoreArray)) if len(healthScoreArray) > 0 else 0
flavorRating.taste = sum(tasteScoreArray) / float(len(tasteScoreArray)) if len(tasteScoreArray) > 0 else 0
flavorRating.speed = sum(speedScoreArray) / float(len(speedScoreArray)) if len(speedScoreArray) > 0 else 0

print flavorRating.taste
print flavorRating.health
print flavorRating.speed

# http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# GET word frequency
# def get_word_features(wordlist):
#     wordlist = nltk.FreqDist(wordlist)
#     word_features = wordlist.keys()
#     return word_features
