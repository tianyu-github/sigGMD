# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 16:56:03 2018

@author: tianyu
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

import os
import gensim
from sklearn.metrics import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
from pyemd import emd

from sklearn.neighbors import DistanceMetric
from datetime import datetime


os.chdir('/home/tiw15008/gene2vec')

W = np.memmap("wordembed.dat", dtype=np.double, mode="r", shape=(380594, 250))
f = open("wordembed.vocab")
vocab_list = map(str.strip, f.readlines())
vocab_dict = {w: k for k, w in enumerate(vocab_list)}

filename=open('filename.txt', 'r').read()
kk=open('fileparallel.txt', 'r').read()
bias = open('filebias0.txt', 'r').read()

bias = int(bias)
kk = int(kk)
data = pd.read_table('topgene_'+filename+'.txt',delim_whitespace=True,index_col=0)
common = data.index.values.tolist()
W_common = W[[vocab_dict[w.lower()] for w in common]] #vector of words, W_common is an array _*300


W_dist = euclidean_distances(W_common)
#W_dist = cosine_similarity(W_common)
#data = data.iloc[:,0:30]
data = data/np.sum(data,axis=0)

import copy

def combine(l, n): 
    answers = []
    one = [0] * n 
    def next_c(li = 0, ni = 0):
        if ni == n:
            answers.append(copy.copy(one))
            return
        for lj in range(li, len(l)):
            one[ni] = l[lj]
            next_c(lj + 1, ni + 1)
    next_c()
    return answers

pairs= combine(range(0,data.shape[1]), 2)

print pairs[0]


import pp
import pyemd


Result= np.zeros( [data.shape[1], data.shape[1]])
   
def myfun1(pair, datai, dataj, W_dist):
    value = pyemd.emd(datai.values, dataj.values, W_dist)
    return (value, pair) 

def mycall(res):
    Result[res[1][0], res[1][1]] = res[0]
    return Result

ppservers = ()
job_server = pp.Server(ppservers=ppservers)
job_server.get_ncpus()


jobs = [job_server.submit(func = myfun1, args = (pair, data.iloc[:,pair[0]], data.iloc[:,pair[1]], W_dist), modules = ('math','pyemd','numpy','pandas'), callback = mycall) for pair in pairs[(len(pairs)/kk+bias):(len(pairs)/kk*2+bias)]]
#, callback = mycall

for job in jobs:
   print "emd score", "is", job()
   #job()


job_server.print_stats()

Result = Result+Result.T

np.savetxt('result_'+filename+'_1.txt',Result,delimiter='\t') 
print '111'
