import numpy as np
from gensim.models import word2vec
from keras.models import Sequential
from keras.preprocessing.sequence import pad_sequences
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import LSTM, GRU, LeakyReLU, BatchNormalization
from keras.models import load_model
import json as js
import jieba
from keras.layers import Embedding
import sys
import csv
"""
model = word2vec.Word2Vec.load("wordToVec1000.model")
data = np.load("TD_data.npy")
with open('word_terms_freq.json') as f:
	word_terms_freq = js.load(f)
data_y = np.load("TD.npy")
"""
jieba.set_dictionary('./final/dict.txt.big')
index2url={}
count=0
with open('./final/news_data_1/NC_1.csv', newline='') as csvFile:
#with open('/Users/peter yang/Downloads/train.csv', newline='') as csvFile:
	rows = csv.reader(csvFile, delimiter=',')
	for row in rows:
		if count==0:
			count+=1
			continue
		index2url[row[0]]=row[1]
		count+=1



dictionary_size = 1000
document_num = 100000

stopword = {"，", "。", "！", "？", "：", ",", ".", "!", "?", ":", "、"}
ignore = {'\n','\r', '\t', '\a', '\b', '\f', '\v'}
train_x = []

num = 0
#for i in range(data.shape[0]):
    #news_seg = list(jieba.cut(data[i][0],cut_all=False))
with open('./final/url2content.json') as f:
	texts = js.load(f)
header={}
tail={}
for url in texts:
	trans=texts[url].split('\n')
	header[url]=(trans[0])
	tail[url]=(trans[len(trans)-1])

alltail=[]
for url in tail:
	a=jieba.cut(tail[url])
	alltail.append(list(a))
w2v_model = word2vec.Word2Vec(alltail,size=300,min_count=5,sg=0)
#data=data.values
#data = pd.DataFrame(data)
w2v_model.save('tail.model')
#w2v_model=word2vec.Word2Vec.load('word.model')

embedding_matrix = np.zeros((len(w2v_model.wv.vocab.items()) + 1, w2v_model.vector_size))
word2idx = {}

vocab_list = [(word, w2v_model.wv[word]) for word, _ in w2v_model.wv.vocab.items()]
for i, vocab in enumerate(vocab_list):
    word, vec = vocab
    embedding_matrix[i + 1] = vec
    word2idx[word] = i + 1

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
PADDING_LENGTH = 500

count=0
data=[]
y=[]
with open('./final/news_data_1/TD.csv', newline='',encoding="utf-8-sig") as csvFile:
#with open('/Users/peter yang/Downloads/train.csv', newline='') as csvFile:
	rows = csv.reader(csvFile, delimiter=',')
	for row in rows:
		if count==0:
			count+=1
			continue
		if(row[2]=='0' or row[2]=='3'or row[2]=='2'):
			data.append(row[1])
		if(row[2]=='0'):
			y.append(0)
		elif(row[2]=='3'or row[2]=='2'):
			y.append(1)
	#	data.append(emoji.demojize(row[1]))
		count+=1
print(y)
header=[]
tail=[]
for i in range(len(data)):
	trans=texts[index2url[data[i]]].split('\n')
	header.append(trans[0])
	tail.append(trans[len(trans)-1])


newtail=[]
for i in tail:
	a=jieba.cut(i)
	newtail.append(list(a))
print(a)
X = text_to_index(newtail)
X = pad_sequences(X, maxlen=PADDING_LENGTH)

count=0

y=np.array(y,dtype=float)
y=np.reshape(y,(len(y),1))
HIDDEN_LAYER_SIZE = 128
X=np.array(X,dtype=int)
print(X.shape)
model = Sequential()
embedding_layer = Embedding(input_dim=embedding_matrix.shape[0],
                            output_dim=embedding_matrix.shape[1],
                            weights=[embedding_matrix],
                            trainable=True)
model.add(embedding_layer)
model.add(LSTM(HIDDEN_LAYER_SIZE, dropout=0.5, recurrent_dropout=0.5))
model.add(BatchNormalization())
model.add(Dense(1))
model.add(Activation("sigmoid"))
model.compile(loss="binary_crossentropy", optimizer="adam",metrics=["accuracy"])
model.summary()
BATCH_SIZE = 128
NUM_EPOCHS = 20
model.fit(X, y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS,validation_split=0.2)

model.save('my_model.h5')
alltail=text_to_index(alltail)
alltail = pad_sequences(alltail, maxlen=PADDING_LENGTH)
ans=model.predict(alltail)
print(ans)
np.save("news_standpoint.npy", ans)
"""


for url in texts:
    if(num==0):
        print(texts[url])
    news_seg = list(jieba.cut(texts[url],cut_all=False))
    temp = np.zeros((dictionary_size))
    sentence = []
    count = 0
    for i in news_seg:
        if(i in ignore):
            continue
        elif(i in stopword):
            if(count != 0):
                sentence.append(temp/count)
                temp = np.zeros((dictionary_size))
                count = 0
        elif(i in model.wv and i in word_terms_freq):
            temp += model.wv[i]*np.power(np.log10(document_num/word_terms_freq[i]), 1.1)
            count += 1
    train_x.append(sentence)
    num+=1
    if(num == 734):
        break
    

PADDING_LENGTH = 500
train_x = pad_sequences(train_x, dtype='float', maxlen=PADDING_LENGTH, padding='pre')

model = load_model("standpoint.h5")
y = model.predict(train_x)
np.save("news_standpoint.npy", y)
"""

"""
num = 0
train_y = []
for i in range(data_y.shape[0]):
    #query_seg = list(jieba.cut(data_y[i][0],cut_all=False))
    #for i in query_seg:
    #    if(i in model.wv and i in word_terms_freq):
    #        temp += model.wv[i]*np.power(np.log10(document_num/word_terms_freq[i]), 0.9) / len(query_seg)
    #train_y.append(temp)
    train_y.append(int(data_y[i][2])/3)
    num += 1
    if(num == 734):
        break

train_x = np.reshape(train_x, (734, 500, dictionary_size))         #data.shape[0]
train_y = np.reshape(train_y, (734, 1))

model = Sequential()
model.add(GRU(units = 16, input_shape = (500, dictionary_size), return_sequences = False, activation='sigmoid' ))  # (time_step, vector_length)
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(8))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(16))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(32))
model.add(LeakyReLU(alpha=0.03))
model.add(BatchNormalization())
model.add(Dropout(0.5))

model.add(Dense(1, activation="sigmoid"))

# Compiling
model.compile(optimizer = 'adam', loss = 'MSE')#categorical_crossentropy
# training
model.fit(train_x, train_y, epochs = 60, batch_size = 100, validation_split=0.1)
model.save("standpoint.h5")
"""