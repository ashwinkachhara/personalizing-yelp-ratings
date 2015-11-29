# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:18:15 2015

@author: ashwin
"""
from nltk.corpus import wordnet as wn
import pickle


#tasteBucket = ["piquant","savory","savoury","zesty","gamy","gamey","juicy","tasty","flat","flavorless","flavourless","insipid","savorless","savourless",    "vapid","smooth","suave","diplomatic","diplomatical","tasteless","unexciting","unstimulating","salty"]
#
#healthBucket = ["refreshing","refreshful","tonic","new","invigorated","refreshed","reinvigorated","unfermented","clean","energising","energizing","preserved","rotten","stale","crisp","crunchy","firm","fresh-cut","pure","unprocessed","unsoured","unspoiled","unspoilt","new-made","oily","oleaginous","fat","fatty","insalubrious","unhealthful","unwholesome"]
#
#speedBucket = ["speedy","flying","fast","agile","nimble","ready","immediate","prompt","straightaway","fast","active","promptly","quickly","active","sluggish","delayed","unhurried","inactive","laggard","behind","slack","slacken"]

#wnTasteBucket = []

#for word in tasteBucket:
#    ss = wn.synsets(word)
#    query = word+':'+'\n'
#    for i in range(len(ss)):
#        query = query +str(i)+str(ss[i])+':'+ss[i].definition()+'\n'
#    selection = 0
#    while selection!=-1:
#        selection = int(raw_input(query+"select: "))
#        if selection != -1:
#            wnTasteBucket.append(ss[selection])
##            print wnTasteBucket
#        else:
#            break
    
wnTasteBucket = [wn.synset('piquant.s.02'),
 wn.synset('savory.a.01'),
 wn.synset('mouth-watering.s.01'),
 wn.synset('piquant.s.01'),
 wn.synset('zestful.s.01'),
 wn.synset('juicy.a.01'),
 wn.synset('tasty.a.01'),
 wn.synset('bland.s.01'),
 wn.synset('bland.s.02'),
 wn.synset('insipid.s.02'),
 wn.synset('vapid.s.02'),
 wn.synset('politic.s.02'),
 wn.synset('tasteless.a.01'),
 wn.synset('unstimulating.a.01'),
 wn.synset('unexciting.a.02'),
 wn.synset('salty.a.02')]

#wnHealthBucket = []
#
#for word in healthBucket:
#    ss = wn.synsets(word)
#    query = word+':'+'\n'
#    for i in range(len(ss)):
#        query = query +str(i)+str(ss[i])+':'+ss[i].definition()+'\n'
#    selection = 0
#    while selection!=-1:
#        selection = int(raw_input(query+"select: "))
#        if selection != -1:
#            wnHealthBucket.append(ss[selection])
##            print wnTasteBucket
#        else:
#            break
        
wnHealthBucket = [wn.synset('oily.s.03'),
 wn.synset('fresh-cut.s.01'),
 wn.synset('inspire.v.01'),
 wn.synset('decayed.s.01'),
 wn.synset('freshen.v.02'),
 wn.synset('greasy.s.01'),
 wn.synset('novel.s.02'),
 wn.synset('unwholesome.a.01'),
 wn.synset('insalubrious.s.01'),
 wn.synset('preserve.v.04'),
 wn.synset('unhealthful.a.02'),
 wn.synset('refresh.v.02'),
 wn.synset('stimulate.v.04'),
 wn.synset('refresh.v.04'),
 wn.synset('clean.a.01'),
 wn.synset('uncorrupted.s.02'),
 wn.synset('stale.a.01'),
 wn.synset('clean.a.07'),
 wn.synset('fresh.s.09'),
 wn.synset('fresh.s.08'),
 wn.synset('enliven.v.02'),
 wn.synset('fatty.a.01'),
 wn.synset('excite.v.07'),
 wn.synset('greasy.s.02'),
 wn.synset('icky.s.01'),
 wn.synset('unsoured.a.01'),
 wn.synset('rotten.s.03'),
 wn.synset('bracing.s.01'),
 wn.synset('good.s.20'),
 wn.synset('new-made.s.01'),
 wn.synset('crisp.s.04'),
 wn.synset('invigorate.v.04'),
 wn.synset('energizing.n.01'),
 wn.synset('preserved.a.01'),
 wn.synset('unrefined.a.01'),
 wn.synset('unsanitary.a.01'),
 wn.synset('quicken.v.03')]

#wnSpeedBucket = []
#
#for word in speedBucket:
#    ss = wn.synsets(word)
#    query = word+':'+'\n'
#    for i in range(len(ss)):
#        query = query +str(i)+str(ss[i])+':'+ss[i].definition()+'\n'
#    selection = 0
#    while selection!=-1:
#        selection = int(raw_input(query+"select: "))
#        if selection != -1:
#            wnSpeedBucket.append(ss[selection])
##            print wnTasteBucket
#        else:
#            break
        
wnSpeedBucket = [wn.synset('fast-flying.s.01'),
 wn.synset('ready.n.01'),
 wn.synset('fly.v.02'),
 wn.synset('quick.s.04'),
 wn.synset('quick.s.01'),
 wn.synset('inactive.a.07'),
 wn.synset('dilatory.s.01'),
 wn.synset('rapid.s.02'),
 wn.synset('dull.s.08'),
 wn.synset('prompt.s.01'),
 wn.synset('prompt.s.02'),
 wn.synset('promptly.r.02'),
 wn.synset('promptly.r.03'),
 wn.synset('promptly.r.01'),
 wn.synset('ready.s.04'),
 wn.synset('ready.s.02'),
 wn.synset('inert.s.03'),
 wn.synset('active.a.07'),
 wn.synset('fast.a.03'),
 wn.synset('quickly.r.01'),
 wn.synset('dawdler.n.01'),
 wn.synset('slow.v.02'),
 wn.synset('ready.a.01'),
 wn.synset('slack.s.02'),
 wn.synset('fast.r.01'),
 wn.synset('delay.v.02'),
 wn.synset('delay.v.01'),
 wn.synset('immediate.s.05'),
 wn.synset('slack.v.04'),
 wn.synset('sluggish.s.01'),
 wn.synset('immediate.s.01'),
 wn.synset('immediately.r.01'),
 wn.synset('unhurried.a.01'),
 wn.synset('agile.s.02'),
 wn.synset('agile.s.01')]


tasteBucket = []
healthBucket = []
speedBucket = []

for s in wnSpeedBucket:
    speedBucket = speedBucket + [x for x in s.lemma_names() if '_' not in x]
for s in wnTasteBucket:
    tasteBucket = tasteBucket + [x for x in s.lemma_names() if '_' not in x]
for s in wnHealthBucket:
    healthBucket = healthBucket + [x for x in s.lemma_names() if '_' not in x]
    
speedBucket = list(set(speedBucket))
healthBucket = list(set(healthBucket))
tasteBucket = list(set(tasteBucket))

#print len(tasteBucket), tasteBucket
#print len(healthBucket), healthBucket
#print len(speedBucket), speedBucket

pklfile = open('base-buckets.pkl','wb')
pickle.dump([tasteBucket,healthBucket,speedBucket],pklfile)
pklfile.close()


