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

os.chdir('/home/tiw15008/cleanfiles')
fp = pd.read_table('fileinfo.txt',header=None) 
mversion = fp.iloc[0,0]
filename = fp.iloc[1,0]
datacell = fp.iloc[2,0]
num = int(fp.iloc[3,0])
del fp


dataorg = pd.read_csv('data_tdidf_'+ datacell+ '.csv',index_col=0)

def get_highexpr(dat,row):
   colsums = dat.sum(axis = 1)
   colsums = colsums.sort_values(ascending=False)
   return (dat.loc[colsums.index[0:row]])
data = get_highexpr(dataorg,num)

wv = pd.read_table('genevector' + mversion + datacell+'.txt',header = None)
wv.index = dataorg.index

W_common = wv.loc[data.index]
W_dist = euclidean_distances(W_common)

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

print(pairs[0])


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


jobs = [job_server.submit(func = myfun1, args = (pair, data.iloc[:,pair[0]], data.iloc[:,pair[1]], W_dist), modules = ('math','pyemd','numpy','pandas'), callback = mycall) for pair in pairs[0:(len(pairs)/8)]]
#, callback = mycall

for job in jobs:
   print("emd score", "is", job())
   #job()


job_server.print_stats()

Result = Result+Result.T

np.savetxt('result_'+mversion+filename+datacell+'_0.txt',Result,delimiter='\t') 
print('111')