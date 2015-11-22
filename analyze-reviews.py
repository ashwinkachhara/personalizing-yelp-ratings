# -*- coding: utf-8 -*-
"""
Created on Sun Nov 22 13:18:25 2015

@author: ashwin
"""

import pickle

pklfile = open('reviews.pkl','rb')
reviews = pickle.load(pklfile)
pklfile.close()

pklfile = open('restaurants.pkl','rb')
restaurants = pickle.load(pklfile)
pklfile.close()

pklfile = open('reviews_user.pkl','rb')
reviews_user = pickle.load(pklfile)
pklfile.close()

pklfile = open('users.pkl','rb')
users = pickle.load(pklfile)
pklfile.close()