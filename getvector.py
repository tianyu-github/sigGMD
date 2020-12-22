# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


from gensim.models import FastText
model = FastText.load('fasttext100719')

wv = model.wv

data = pd.read_table("/Users/tianyu/data/data_gename60c.txt",index_col=0, delim_whitespace=True)
data = pd.read_csv('/Users/tianyu/data/GSE29087_L139_expression_tab.csv',index_col=0)
data = pd.read_table('/Users/tianyu/data/data_order420c.txt')

del data['TrLen']
data = data.iloc[:,0:92]

gene = data.index.values.tolist()
del data

gv = []

for i in gene:
    try:
        x = wv[i.lower()]
    except KeyError:
        print(i.lower())
    else:
        gv.append(wv[i.lower()])
        
gv_array = np.asarray(gv)    
  
np.savetxt('genevector1007_420c.txt',gv_array,delimiter='\t')  

