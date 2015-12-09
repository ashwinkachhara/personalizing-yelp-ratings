# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:16:51 2015

@author: ashwin
"""
import json
from sets import Set
import pickle


def convert(ob):
    for k, v in ob.items():
        if isinstance(v, list):
            ob[k] = ','.join(v)
        elif isinstance(v, dict):
            for kk, vv in v.items():
                ob['%s_%s' % (k, kk)] = vv
            del ob[k]
    return ob

filePrefix = "yelp_academic_dataset_"

interest_categories = ["Restaurants", "Food"] # "Nightlife"
interest_state = ['NV', 'AZ', 'PA', 'IL', 'WI', 'NC']
state_index = 3 # We chose IL as test dataset because it had 334 businesses. Next was WI - 1249

restaurants = []
reviews = {}
users = []
reviews_user = {}

businessesFile = open('data/'+ filePrefix + 'business.json')
reviewsFile = open('data/'+ filePrefix + 'review.json')
usersFile = open('data/'+ filePrefix + 'user.json')

for line in businessesFile:
    ob = json.loads(line)
    if ob['state'] == interest_state[state_index] and len(list(set(interest_categories) & set(ob['categories']))) > 0:
        restaurants.append(ob)

print "Loaded",len(restaurants),"restaurants in",interest_state[state_index]

biz_ids = [d['business_id'] for d in restaurants]
#print biz_ids[:10]

for i in range(len(restaurants)):
    reviews[biz_ids[i]] = []

user_ids = Set([])
#print filter(lambda biz: biz['business_id'] == biz_ids[0], restaurants)

numReviews = 0
for line in reviewsFile:
    ob = json.loads(line)
    if ob['business_id'] in biz_ids:
        reviews[ob['business_id']].append(ob)
        user_ids.add(ob['user_id'])
        numReviews += 1

print "Found",numReviews,"reviews"

user_ids = list(user_ids)

for line in usersFile:
    ob = json.loads(line)
    if ob['user_id'] in user_ids and ob['review_count'] >= 5:
        users.append(ob)

print "Found", len(users), "users"

suff_users = [u['user_id'] for u in users]

for i in suff_users:
    reviews_user[i] = []


for biz_id,biz in reviews.iteritems():
    for review in biz:
        if review['user_id'] in suff_users:
#            print review['user_id']
            reviews_user[review['user_id']].append(review)

pklfile = open('generated_files/reviews.pkl','wb')
pickle.dump(reviews,pklfile)
pklfile.close()

pklfile = open('generated_files/restaurants.pkl','wb')
pickle.dump(restaurants,pklfile)
pklfile.close()

pklfile = open('generated_files/reviews_user.pkl','wb')
pickle.dump(reviews_user,pklfile)
pklfile.close()

pklfile = open('generated_files/users.pkl','wb')
pickle.dump(users,pklfile)
pklfile.close()
