#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import numpy as np
import csv
import keras
import jieba
import sys
from gensim.models.word2vec import Word2Vec
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Embedding, GRU, Dense, LSTM, Dropout, SimpleRNN, Bidirectional
from keras.layers.normalization import BatchNormalization
import csv


# In[2]:


with open('url.json' , 'r') as reader:
    jf = json.loads(reader.read())


# In[11]:


jf


# In[3]:


names = ['id','data']
formats = ['string','string']
dtype = dict(names = names, formats=formats)
data = np.array(list(jf.items()))


# In[4]:


word_length = 0
for i in range(data.shape[0]):
    word_length += len(data[i])


# In[6]:


NC = []
for i in range(100000):
    NC.append([])
    
count = 0  
with open('./news_data_1/NC_1.csv', 'r', newline = '') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if row[0] != "News_Index":
            NC[count].append(row[0])
            NC[count].append(row[1])
            count += 1
NC = np.array(NC)

TD = []
for i in range(4742):
    TD.append([])

count = 0
with open('./news_data_1/TD.csv', 'r', newline = '', encoding='utf-8') as csvfile:
    rows = csv.reader(csvfile)
    for row in rows:
        if row[0] != "Query":
            TD[count].append(row[0])
            TD[count].append(row[1])
            TD[count].append(row[2])            
            count += 1
TD = np.array(TD)   


# In[7]:


x = []
for i in range(4742):
    x.append([])

count = 0
for i in range(4742):
    num = int(TD[i,1][5:])
    x[i].append(jf[NC[num-1,1]])
    
    print(num)
x = np.array(x)
x[1,0] = x[1,0][632:748]


# In[8]:


np.save("TD_data.npy", x)


# In[9]:


np.save("TD.npy", TD)
np.save("NC.npy", NC)


# In[10]:


x

