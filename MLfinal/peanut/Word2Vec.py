#!/usr/bin/env python
# coding: utf-8

# In[62]:


import json
import numpy as np
import csv
import keras
import jieba
import sys
from gensim.models.word2vec import Word2Vec
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Sequential, load_model, Model
from keras.layers import Embedding, GRU, Dense, LSTM, Dropout, SimpleRNN, Bidirectional, Input
from keras.layers.normalization import BatchNormalization
import csv


# In[2]:


data = np.load("TD_data.npy")


# In[3]:


n = data.shape[0]
jieba.load_userdict('news_data_1/dict.txt.big')


# In[4]:


x_train = []

for i in range(n):
    x_train.append([])
for i in range(n):
    x_train[i].append(jieba.lcut(data[i,0]))


# In[5]:


x_wv = []
for i in range(n):
    x_wv.append(x_train[i][0])


# In[6]:


WordVec = Word2Vec(x_wv,min_count = 5, size=200, sg = 1)


# In[7]:


w2v_model = WordVec


# In[ ]:


embedding_matrix = np.zeros((len(w2v_model.wv.vocab.items()) + 1, w2v_model.vector_size))
word2idx = {}

vocab_list = [(word, w2v_model.wv[word]) for word, _ in w2v_model.wv.vocab.items()]
for i, vocab in enumerate(vocab_list):
    word, vec = vocab
    embedding_matrix[i + 1] = vec
    word2idx[word] = i + 1


# In[ ]:


embedding_layer = Embedding(input_dim=embedding_matrix.shape[0],
                            output_dim=embedding_matrix.shape[1],
                            mask_zero=True,
                            weights=[embedding_matrix],
                            trainable=True)


# In[ ]:


def text_to_index(corpus):
    new_corpus = []
    for doc in corpus:
        new_doc = []
        for word in doc:
            try:
                new_doc.append(word2idx[word])
            except:
                new_doc.append(0)
        new_corpus.append(new_doc)
    return np.array(new_corpus)


# In[ ]:


PADDING_LENGTH = 500
X = text_to_index(x_wv)
X = pad_sequences(X, maxlen=PADDING_LENGTH)
print("Shape:", X.shape)
print("Sample:", X[100])


# In[80]:


def new_model():
    model = Sequential()
    model.add(embedding_layer)
    model.add(LSTM(64,activation='softmax',return_sequences=True))
    model.add(Dropout(0.5))
    model.add(LSTM(128))
    model.add(Dropout(0.5))
#    model.add(Dense(16, activation='relu'))
#    model.add(Dropout(0.5))
    model.add(Dense(4, activation='softmax'))
    
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    return model
def proposed_sequence_classifier():
    rnn_width = 32
    input = Input(shape=(32))
    x = LSTM(rnn_width, return_sequences=True)(input)
    x = LSTM(rnn_width*2, return_sequences=True)(x)
    x = LSTM(rnn_width*4, return_sequences=True)(x)
    x = LSTM(4, activation='softmax')(x)
    return Model(input, x)


# In[79]:


#model = new_model()
model = new_model()
model.summary()
model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])


# In[15]:


TD = np.load("TD.npy")
Y = np.uint8(TD[:,2])


# In[22]:


X[0:230].shape


# In[77]:


model.fit(x=X[0:230], y=Y[0:230], batch_size=20, epochs = 10)


# In[84]:


tmp = []
save = TD[0,0]
for i in range(n):
    if TD[i,0] != save:
        save = TD[i,0]
        tmp.append(i)

