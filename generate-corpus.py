import pickle
import enchant
import string
import re
import json

from nltk.corpus import stopwords

from buckets import *

import json, sys, os
sys.path.append(os.getcwd()+'/cortical/')
from cortical.client import ApiClient
from compareApi import CompareApi

# This class uses the Cortical API to calculate wordSimilarity
class Cortical:
    # Variables needed to make calls to the Cortical API
    BASE_PATH = "http://api.cortical.io/rest"
    API_KEY = "4b6b3100-bf81-11e4-b8ca-f119f1630c46"
    RETINA_NAME = "en_associative"

    # Constructor
    def __init__(self):
        self.compareApi = CompareApi(ApiClient(apiKey=self.API_KEY, apiServer=self.BASE_PATH))

    # Returns similarity between two pieces of text
    def similarity(self, s1="", s2=""):
        #        print result.weightedScoring
        #        print result.cosineSimilarity
        #        print result.jaccardDistance
        #        print result.euclideanDistance
        body = json.dumps([{"text": s1},{"text": s2}])
        result = self.compareApi.compare(self.RETINA_NAME, body)
        return result.weightedScoring

    # Uses bulk mode to get multiple similarity results in a single call
    def bulkSimilarity(self,s1="",s2=[]):
        req = '['
        for word in s2:
            req = req + json.dumps([{"text": s1},{"text": word}]) + ','
        req = req[:-1]+']'

        result = self.compareApi.compareBulk(self.RETINA_NAME,req)

        return [r.weightedScoring for r in result]

# Function uses Cortical class to obtain word similarity with base buckets (bulk mode)
def bulkBucketSimilarity(word):
    tastevector = c.bulkSimilarity(word,tasteBucket)

    healthvector = c.bulkSimilarity(word,healthBucket)

    speedvector = c.bulkSimilarity(word,speedBucket)
    print tastevector
    print healthvector
    print speedvector
    return [sum(tastevector)/len(tastevector),sum(healthvector)/len(healthvector),sum(speedvector)/len(speedvector)]

# Function uses Cortical class to obtain word similarity with base buckets
def bucketSimilarity(word):
    tastevector = []
    for bucketword in tasteBucket:
        try:
            newval = c.similarity(word,bucketword)
            tastevector.append(newval)
        except Exception:
            pass
    healthvector = []
    for bucketword in healthBucket:
        try:
            newval = c.similarity(word,bucketword)
            healthvector.append(newval)
        except Exception:
            pass
    speedvector = []
    for bucketword in speedBucket:
        try:
            newval = c.similarity(word,bucketword)
            speedvector.append(newval)
        except Exception:
            pass
    return [sum(tastevector)/len(tastevector),sum(healthvector)/len(healthvector),sum(speedvector)/len(speedvector)]

# First generate a list of business that are in the correct categories.
# We want to only pull corpus words from food reviews.
businessesFile = open('data/yelp_academic_dataset_business.json')

# Load the file containing all of the reviews
reviewsFile = open('data/yelp_academic_dataset_review.json')

# Store valid businesses here
biz_ids = set()

# Loop through all of the businesses to get the identifiers
for line in businessesFile:
    ob = json.loads(line)
    if len(list({"Restaurants", "Food"} & set(ob['categories']))) > 0:
        biz_ids.add(ob['business_id'])

# Load the NLTK list of stopwords
stopWords = set(stopwords.words("english"))

# Load the spell checking dictionary -- currently not used
dictionary = enchant.Dict("en_US")

# Create regex for special chars -- leaves all words and containing apostrophes
pattern = re.compile('[^\w\']')

# Create a set to hold all of the unique words.
wordSet = set()

# Used for printing progress. Prints out every 10K reviews. 1.6 Million total in file
index = 0

# Loop through all of the businesses and all of the associated reviews
for line in reviewsFile:
    # Increment logging index
    index += 1

    # Print for logging
    if index % 10000 == 0:
        print index

    # Get the review json
    reviewJson = json.loads(line)

    # Only parse the review IF the associated business is a restaurant
    if reviewJson['business_id'] in biz_ids:

        # Get the current review
        review = reviewJson['text'].lower()

        # Remove the stopwords from the review
        review = ' '.join(word for word in review.split() if word not in stopWords)

        # Remove the punctuation from the review
        review = pattern.sub(" ", review)

        # Check spelling of words
        # for word in review.split():
        #     if not dictionary.check(word):
        #         print word
        #         print ''
        #         print dictionary.suggest(word)
        #         print ''

        # Loop through all words in the review. Remove leading/trailing special characters.
        # Only add if not all numbers AND has more than 2 characters
        for word in review.split():
            word = word.strip(string.punctuation)
            if not word.isdigit() and len(word) > 2:
                wordSet.add(word)

        # if index > 50000:
        #     break

# Sort the word list in Alphabetical order. Caps will still come first.
sortedList = list(wordSet)
sortedList.sort()

# Write the data to the file
pklfile = open('word_corpus.pkl', 'wb')
pickle.dump(sortedList, pklfile)
pklfile.close()

c = Cortical()
print c.similarity("spicy","tasteless")
#print c.bulkSimilarity("spicy",tasteBucket)

#print bulkBucketSimilarity("terrible speed")
print bulkBucketSimilarity("spicy")
#print bulkBucketSimilarity("backrub")


#print bucketSimilarity("sluggish")

#c.similarity("terrible speed", "piquant savory savoury zesty gamy gamey juicy tasty flat flavorless flavourless insipid savorless savourless vapid smooth suave diplomatic diplomatical tasteless unexciting unstimulating")

#c.similarity("terrible speed", "speedy flying fast agile nimble ready immediate prompt straightaway fast active promptly quickly active sluggish delayed unhurried inactive laggard behind slack slacken")

#c.similarity("terrible speed", "refreshing refreshful tonic new invigorated refreshed reinvigorated unfermented clean energising energizing preserved rotten salty stale crisp crunchy firm fresh-cut pure unprocessed unsoured unspoiled unspoilt new-made oily oleaginous fat fatty insalubrious unhealthful unwholesome")
print len(sortedList)
