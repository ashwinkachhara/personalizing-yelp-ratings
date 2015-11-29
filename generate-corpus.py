import pickle
import enchant
import string
import re

from nltk.corpus import stopwords

from buckets import *

import json, sys, os
sys.path.append(os.getcwd()+'/cortical/')
from cortical.client import ApiClient
from compareApi import CompareApi

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
    print tastevector
    print healthvector
    print speedvector
    return [sum(tastevector)/len(tastevector),sum(healthvector)/len(healthvector),sum(speedvector)/len(speedvector)]
      

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
    
#    return sum(tastevector)/len(tastevector)


# Load the file containing all of the reviews
reviewsFile = open('reviews.pkl', 'rb')
reviews = pickle.load(reviewsFile)
reviewsFile.close()

# Load the NLTK list of stopwords
stopWords = set(stopwords.words("english"))

# Load the spell checking dictionary
dictionary = enchant.Dict("en_US");

# Create punctuation map used for removing punctuation from reviews -- not used right now
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
# review = review.translate(remove_punctuation_map)

# Create regex for special chars
pattern = re.compile("[^\w']")

# Create a set to hold all of the unique words.
wordSet = set()

# Loop through all of the businesses and all of the associated reviewsnl
for i in range(len(reviews.values())):
    for j in range(len(reviews.values()[i])):
        # Get the current review
        review = reviews.values()[i][j]['text']

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
        for word in review.split():
            wordSet.add(word)

# Sort the word list in Alphabetical order. Caps will still come first.
sortedList = list(wordSet)
sortedList.sort()

# Write the data to the file
pklfile = open('temp.pkl', 'wb')
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
