# loop through all sentences
# use buckets of words along with sentences to generate sentiment
# Compare words in sentence to words in bucket. If word matched perform a sentiment analysis.
# Possible algorithm
# wordMatches * sentiment  summed over all sentences
import json
import pickle
import requests
import urllib

from nltk.tokenize import sent_tokenize

# Import the old sentiment analyzer -- will replace.
from sentiment.info import setup, MyDict, classify2
setup()

# Get a set of words for all of the grouping buckets
pklfile = open('generated_files/full-buckets.pkl', 'rb')
tasteBucket, healthBucket, speedBucket = pickle.load(pklfile)
pklfile.close()

#remove \r if the words have it appended -- windows only
for index in range(len(tasteBucket)):
    tasteBucket[index] = tasteBucket[index].replace('\r', '')

for index in range(len(healthBucket)):
    healthBucket[index] = healthBucket[index].replace('\r', '')

for index in range(len(speedBucket)):
    speedBucket[index] = speedBucket[index].replace('\r', '')

tasteBucket = set(tasteBucket)
healthBucket = set(healthBucket)
speedBucket = set(speedBucket)

speedBucket.remove("pokey")

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
        return ['pos', sentiment[1]]
    if not sentiment[0] and (sentiment[1] > .5):
        return ['neg', sentiment[1]]
    return ['neutral', 0]


# Convert to this when finalizing and have data writing to file properly. -- should only use this on 1 run
def get_sentiment_two(text2):
    r = requests.post('http://text-processing.com/api/sentiment/', data="text=" + text2)
    try:
        sentiment_json = json.loads(r.text)
    except:
        print text2,'|',r.status_code,'|',r.text
        r = requests.post('http://text-processing.com/api/sentiment/', data="text=" + urllib.quote_plus(text2))
        sentiment_json = json.loads(r.text)
    return [sentiment_json['label'], sentiment_json['probability']['neg'], sentiment_json['probability']['neutral'], sentiment_json['probability']['pos'] ]


def taste_algorithm():
    return 1


# Load the file containing all of the reviews
pklfile = open('generated_files/reviews.pkl', 'rb')
reviewsFile = pickle.load(pklfile)
pklfile.close()

# Create arrays to hold flavor values, we will average after processing all reviews
# healthScoreArray = []
# speedScoreArray = []
# tasteScoreArray = []


index = 0
# Loop through all of the reviews -- Currently all of the reviews for the dataset we pulled
for businesses in reviewsFile.values():
    index += 1
    print "Analyzing biz",index
    for i in range(len(businesses)):
#        index += 1

        # Get the review json
        reviewItem = businesses[i]
        # reviewJson = json.loads(line)

        # Get the review text
        review = reviewItem['text']

        # Tokenize each of the sentences from the review
        reviewSentences = sent_tokenize(review)

        # Add the sentiment array to the current reviewItem
        reviewItem['sentiment'] = []
        # Add the wc array to the current reviewItem [[wc#taste, wc#health, wc#speed],[...], ... ]
        reviewItem['matchedWC'] = []

        # Loop through all of the sentences
        for sentence in reviewSentences:
            # Lowercase the sentence for matching
            sentence = sentence.lower()

            # Get the set of words in the sentence
            sentenceWordSet = set(sentence.split())

            # Check to see if the sentence contains any of the key-words
            hasTaste = True if tasteBucket & sentenceWordSet else False
            hasSpeed = True if speedBucket & sentenceWordSet else False
            hasHealth = True if healthBucket & sentenceWordSet else False

            # Get which grouping the sentence falls under
            sentimentGroup = get_sentiment(sentence)

            # Add the sentences sentiment value to the array of sentiments
            reviewItem['sentiment'].append(sentimentGroup)
            # Add the sentences wc value to the array of wc
            reviewItem['matchedWC'].append([len(tasteBucket & sentenceWordSet),len(healthBucket & sentenceWordSet),len(speedBucket & sentenceWordSet)])

            # If neutral, skip this sentence
#            if sentimentGroup[0] == 'neutral':
#                break

            # Try all of the buckets that matched
            # if hasTaste:
            #     # print sentence
            #     # print 't:' + sentimentGroup
            #     tasteScoreArray.append(-1 * taste_algorithm() if sentimentGroup[0] == 'neg' else taste_algorithm())
            #
            # if hasSpeed:
            #     # print sentence
            #     # print 's:' + sentimentGroup
            #     speedScoreArray.append(-1 * taste_algorithm() if sentimentGroup[0] == 'neg' else taste_algorithm())
            #
            # if hashealth:
            #     # print sentence
            #     # print 'h:' + sentimentGroup
            #     healthScoreArray.append(-1 * taste_algorithm() if sentimentGroup[0] == 'neg' else taste_algorithm())


# Generate an overall flavorRating
#flavorRating = FlavorRating()

# Set the flavor rating values
#flavorRating.health = sum(healthScoreArray) / float(len(healthScoreArray)) if len(healthScoreArray) > 0 else 0
#flavorRating.taste = sum(tasteScoreArray) / float(len(tasteScoreArray)) if len(tasteScoreArray) > 0 else 0
#flavorRating.speed = sum(speedScoreArray) / float(len(speedScoreArray)) if len(speedScoreArray) > 0 else 0

#print flavorRating.taste
#print flavorRating.health
#print flavorRating.speed

pklfile = open('generated_files/businesses_sentiment_wc.pkl', 'wb')
pickle.dump(reviewsFile, pklfile)
pklfile.close()

# http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/
# GET word frequency
# def get_word_features(wordlist):
#     wordlist = nltk.FreqDist(wordlist)
#     word_features = wordlist.keys()
#     return word_features
