# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 21:46:40 2018

@author: tianyu
"""

import os
import numpy as np
import pandas as pd
#os.chdir('/home/tiw15008/cleanfiles/fasttextmodel/')


from gensim.models import FastText
model = FastText.load('fasttext0928')

sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]
model = FastText(sentences, min_count=1)

wv = model.wv

W = np.memmap("fastembed.dat", dtype=np.double, mode="r", shape=(424107, 300))
f = open("fastembed_clean.vocab",encoding='utf-8')
vocab_list = map(lambda x: eval(x.strip()), f.readlines())
vocab_dict = {w: k for k, w in enumerate(vocab_list)}

data = pd.read_table("data_gename.txt",index_col=0, delim_whitespace=True)
gene = data.index.values.tolist()

common = [word for word in gene if word.lower() in vocab_dict] # words in the dict





W_gene = W[[vocab_dict[w.lower()] for w in gene if w in vocab_dict]] #vector of words, W_common is an array _*300

