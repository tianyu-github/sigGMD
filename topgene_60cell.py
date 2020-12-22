#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 14:24:49 2018

@author: tianyu
"""


import os
import numpy as np
import pandas as pd
os.chdir('/Users/tianyu/google drive/fasttext/testword2vec/data')

fp = pd.read_table('fileinfo.txt',header=None) 
mversion = fp.iloc[0,0]
filename = fp.iloc[1,0]
datacell = fp.iloc[2,0]
del fp


mversion = '1007_'
filename= 'high_300_'
datacell = '60c'


dataorg = pd.read_csv('data_all_'+ datacell+ '.csv',index_col=0)
############


def get_highexpr(dat,row):
   colsums = dat.sum(axis = 1)
   colsums = colsums.sort_values(ascending=False)
   return (dat.loc[colsums.index[0:row]])
data = get_highexpr(dataorg,300)


wv = pd.read_table('genevector' + mversion + datacell+'.txt',header = None)
wv.index = dataorg.index

W_common = wv.loc[data.index]
from sklearn.metrics import euclidean_distances
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

print (len(pairs))


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


jobs = [job_server.submit(func = myfun1, args = (pair, data.iloc[:,pair[0]], data.iloc[:,pair[1]], W_dist), modules = ('math','pyemd','numpy','pandas'), callback = mycall) for pair in pairs]
#, callback = mycall

for job in jobs:
   print ("emd score", "is", job())
   #job()


job_server.print_stats()

Result = Result+Result.T

np.savetxt(('result_'+mversion + filename + datacell+'.txt'),Result,delimiter='\t') 
###################
