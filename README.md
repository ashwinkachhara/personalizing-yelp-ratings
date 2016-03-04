Personalizing Yelp Ratings to Culinary Preferences
===================
Ashwin Kachhara; Tyler Hastings
===============================
The problem that we propose is:
- To generate quantization of the profile of a restaurant across various scales covering  certain aspects of evaluation that we/users are interested in
- To generate a quantization of aspects that users value in restaurants based on what restaurants these users rated highly and the profile of these restaurants

We aim to accomplish both of the above without any user interviews. Rather we propose to utilize information that can be extracted from the large corpus of restaurant reviews and reviews associated with users available on Yelp.

Overall, we conclude that there is some merit to the idea of computing a user’s personalized flavor profile to aid in restaurant selection. We have many cases that show we were able to positively predict that a user would give a particular restaurant either a four or five star rating.


FILES:
- data/             : Unzip the Yelp Dataset here
- generated_files/  : Files that we generate appear here
- images/
  - good_users/     : Saved images of some "good" users (NOT_EMPTY)
  - users/          : Where images in general will be stored (EMPTY)
  - businesses.jpg  : Plot of all business FlavorRating
  - copygoodimg.sh  : Shows you all images in users/ one by one and if you press y, copies current image into 
- good_users/
  - users.jpg       : Plot of all user FlavorRating
- sentiment/        : Sentiment Analysis library that we used. https://github.com/vivekn/sentiment

CODE:
- testdata-extraction.py            : Reads json files -> indexes reviews by user_id and business_id
- buckets.py                        : Create base-buckets
- generate-corpus.py                : Compiles word corpus from all the reviews in Yelp Academic Dataset
- word-classify.py                  : Removes words from corpus that don’t have a single synset in wordnet
- wn-word-classify.py               : Runs wordnet path similarity between base buckets and corpus words
- wn-scores-analysis.py             : Uses scores for corpus and base-buckets to classify corpus and generate the full-buckets
- perform-analysis.py               : Appends sentiment and matchedWC to reviews
- gen-user-flavors-using-ratings.py : Generates business flavors AND user flavors. Saves user-their_review graphs in directory
- validation.py                     : Performs validation on top20 users in IL dataset
