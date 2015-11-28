import pickle
import enchant
import string
import re

from nltk.corpus import stopwords

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

# Loop through all of the businesses and all of the associated reviews
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
