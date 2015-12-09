Social Data Project
===================
Ashwin Kachhara; Tyler Hastings
===============================

FILES:
data/             : Unzip the Yelp Dataset here
generated_files/  : Files that we generate appear here
images/
  good_users/     : Saved images of some "good" users (NOT_EMPTY)
  users/          : Where images in general will be stored (EMPTY)
  businesses.jpg  : Plot of all business FlavorRating
  copygoodimg.sh  : Shows you all images in users/ one by one and if you press y, copies current image into good_users/
  users.jpg       : Plot of all user FlavorRating
sentiment/        : Sentiment Analysis library that we used. https://github.com/vivekn/sentiment

CODE:
1.  testdata-extraction.py            : Reads json files -> indexes reviews by user_id and business_id
2.  buckets.py                        : Create base-buckets
3.  generate-corpus.py                : Compiles word corpus from all the reviews in Yelp Academic Dataset
4.  word-classify.py                  : Removes words from corpus that don’t have a single synset in wordnet
5.  wn-word-classify.py               : Runs wordnet path similarity between base buckets and corpus words
6.  wn-scores-analysis.py             : Uses scores for corpus and base-buckets to classify corpus and generate the full-buckets
7.  perform-analysis.py               : Appends sentiment and matchedWC to reviews
8.  gen-user-flavors-using-ratings.py : Generates business flavors AND user flavors. Saves user-their_review graphs in directory
9.  validation.py                     : Performs validation on top20 users in IL dataset
