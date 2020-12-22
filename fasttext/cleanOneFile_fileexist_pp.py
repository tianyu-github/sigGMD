#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 17:05:31 2018

@author: tianyu
"""

import stat
import fileinput
import os
import time
import random
import sys, traceback
import subprocess
from subprocess import Popen, PIPE
import cPickle
import string 
import re 
import pp
import multiprocessing

# import nltk
# from nltk.corpus import stopwords
# from nltk.probability import FreqDist
# from nltk import word_tokenize

from func2cleanASentence4github import * 


class Myfile(object):
    def __init__(self, dirname):
        self.dirname = dirname
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            if '.DS_Store' in fname:
                continue
            for ffname in os.listdir(os.path.join(self.dirname, fname)):
                if '.DS_Store' in ffname:
                    continue
                for fffname in os.listdir(os.path.join(self.dirname, fname, ffname)):
                    if '.DS_Store' in fffname:
                        continue
                    filepathname = os.path.join(self.dirname, fname, ffname,fffname)
                    yield [filepathname, fffname]


def submitJobs (fileInPath,fileInName, fileoutpath):
        print ('111')
    #if fileInName not in os.listdir(fileoutpath):
        fileOutName = os.path.join(fileoutpath, fileInName)
        #read in a file
        f = open(fileInPath, 'r')
        textInFile = f.read() ## whole file
        f.close()
        #clean a file
        textInFile = cleanSentencesInFile (textInFile,1,1) 
        f = open(fileOutName,"w")
        f.write(textInFile)
 




### -------------------------------------------------------
	
if len(sys.argv)<2:
    print("Usage: \n")
    sys.exit(1)
else:
    ppservers = ()
    job_server = pp.Server(ppservers=ppservers)
    job_server.get_ncpus()
    jobs = [job_server.submit(func = submitJobs, args = (fileInPath,fileInName,sys.argv[2] ), modules = ('stat',
                              'fileinput','os','time','random','sys','traceback','subprocess','cPickle','string','re')) for fileInPath,fileInName in Myfile(sys.argv[1])]
    job_server.print_stats()


	
	
