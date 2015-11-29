import pickle
import enchant
import string
import re
import json

from nltk.corpus import stopwords

# First generate a list of business that are in the correct categories.
# We want to only pull corpus words from food reviews.
businessesFile = open('yelp_academic_dataset_business.json')

# Load the file containing all of the reviews
reviewsFile = open('yelp_academic_dataset_review.json')

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

print len(sortedList)
