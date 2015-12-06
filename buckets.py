# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 18:18:15 2015

@author: ashwin
"""
from nltk.corpus import wordnet as wn
import pickle

# wnTasteBucket, wnHealthBucket, wnSpeedBucket contain base buckets with semantic connotations
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

# We convert a synset list into a wordlist
for s in wnSpeedBucket:
    speedBucket = speedBucket + [x for x in s.lemma_names() if '_' not in x]
for s in wnTasteBucket:
    tasteBucket = tasteBucket + [x for x in s.lemma_names() if '_' not in x]
for s in wnHealthBucket:
    healthBucket = healthBucket + [x for x in s.lemma_names() if '_' not in x]

speedBucket = list(set(speedBucket))
healthBucket = list(set(healthBucket))
tasteBucket = list(set(tasteBucket))

# Save base-buckets.pkl
pklfile = open('generated_files/base-buckets.pkl','wb')
pickle.dump([tasteBucket,healthBucket,speedBucket],pklfile)
pklfile.close()
